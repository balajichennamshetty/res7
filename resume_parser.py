import spacy
import docx
from pdfminer.high_level import extract_text
from typing import Dict, Any

class ResumeParser:
    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF file"""
        try:
            return extract_text(pdf_path)
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
            return ""

    def extract_text_from_docx(self, docx_path: str) -> str:
        """Extract text from DOCX file"""
        try:
            doc = docx.Document(docx_path)
            return ' '.join([paragraph.text for paragraph in doc.paragraphs])
        except Exception as e:
            print(f"Error extracting text from DOCX: {e}")
            return ""

    def extract_information(self, text: str) -> Dict[str, Any]:
        """Extract key information from resume text"""
        doc = self.nlp(text)
        
        # Initialize sections
        sections = {
            'skills': set(),
            'education': [],
            'experience': [],
            'contact': {}
        }

        # Extract skills (looking for technical terms and proper nouns)
        for token in doc:
            if token.pos_ in ['PROPN', 'NOUN'] and len(token.text) > 2:
                sections['skills'].add(token.text)

        # Extract education and experience (looking for organizations and dates)
        for ent in doc.ents:
            if ent.label_ == 'ORG':
                # Check context for education-related terms
                context = doc[max(0, ent.start-5):min(len(doc), ent.end+5)].text.lower()
                if any(term in context for term in ['university', 'college', 'school', 'degree']):
                    sections['education'].append(ent.text)
                else:
                    sections['experience'].append(ent.text)
            elif ent.label_ == 'PERSON':
                sections['contact']['name'] = ent.text
            elif ent.label_ == 'EMAIL':
                sections['contact']['email'] = ent.text

        # Convert skills set to list for JSON serialization
        sections['skills'] = list(sections['skills'])
        
        return sections

    def parse_resume(self, file_path: str) -> Dict[str, Any]:
        """Main method to parse resume file"""
        if file_path.endswith('.pdf'):
            text = self.extract_text_from_pdf(file_path)
        elif file_path.endswith('.docx'):
            text = self.extract_text_from_docx(file_path)
        else:
            raise ValueError("Unsupported file format. Please provide PDF or DOCX file.")

        if not text:
            raise ValueError("Failed to extract text from the document.")

        return self.extract_information(text)