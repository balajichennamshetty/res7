from transformers import AutoTokenizer, AutoModel
import torch
import numpy as np
from typing import List, Dict, Any
from sklearn.metrics.pairwise import cosine_similarity

class MatchingEngine:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
        self.model = AutoModel.from_pretrained('bert-base-uncased')
        self.model.eval()

    def get_bert_embedding(self, text: str) -> np.ndarray:
        """Generate BERT embeddings for input text"""
        # Tokenize and prepare input
        inputs = self.tokenizer(text, return_tensors='pt', padding=True, truncation=True, max_length=512)
        
        # Generate embeddings
        with torch.no_grad():
            outputs = self.model(**inputs)
            # Use the [CLS] token embedding as the sentence embedding
            embedding = outputs.last_hidden_state[:, 0, :].numpy()
        
        return embedding

    def calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate semantic similarity between two texts"""
        embedding1 = self.get_bert_embedding(text1)
        embedding2 = self.get_bert_embedding(text2)
        
        similarity = cosine_similarity(embedding1, embedding2)[0][0]
        return float(similarity)

    def match_resume_to_job(self, resume_info: Dict[str, Any], job_description: str) -> Dict[str, float]:
        """Match resume information against job description"""
        # Prepare resume text sections
        skills_text = ' '.join(resume_info.get('skills', []))
        education_text = ' '.join(resume_info.get('education', []))
        experience_text = ' '.join(resume_info.get('experience', []))

        # Calculate similarity scores for different sections
        scores = {
            'skills_match': self.calculate_similarity(skills_text, job_description),
            'education_match': self.calculate_similarity(education_text, job_description),
            'experience_match': self.calculate_similarity(experience_text, job_description)
        }

        # Calculate overall match score (weighted average)
        weights = {'skills_match': 0.4, 'experience_match': 0.4, 'education_match': 0.2}
        scores['overall_match'] = sum(score * weights[key] for key, score in scores.items() if key in weights)

        return scores

    def rank_candidates(self, candidates: List[Dict[str, Any]], job_description: str) -> List[Dict[str, Any]]:
        """Rank candidates based on their match with job description"""
        # Calculate scores for each candidate
        for candidate in candidates:
            candidate['scores'] = self.match_resume_to_job(candidate['resume_info'], job_description)

        # Sort candidates by overall match score
        ranked_candidates = sorted(candidates, 
                                 key=lambda x: x['scores']['overall_match'], 
                                 reverse=True)

        return ranked_candidates