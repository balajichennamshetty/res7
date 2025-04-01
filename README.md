# Resume Screening & Ranking System

A powerful resume screening and ranking system that uses Natural Language Processing (NLP) and BERT transformers to automatically parse resumes, extract key information, and rank candidates based on job descriptions.

## Features

- Resume parsing (PDF and DOCX support)
- Automatic information extraction (skills, education, experience)
- BERT-based semantic matching
- Candidate ranking based on job description relevancy
- User-friendly web interface

## Installation

1. Clone the repository
2. Install the required dependencies:
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

## Usage

1. Start the application:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to the provided URL (typically http://localhost:8501)

3. Upload resumes (PDF or DOCX format)

4. Enter the job description

5. Click "Analyze and Rank" to process the resumes

## System Components

- `resume_parser.py`: Handles document processing and information extraction using spaCy
- `matching_engine.py`: Implements BERT-based semantic matching and candidate ranking
- `app.py`: Streamlit web interface for user interaction

## Technologies Used

- Python
- Streamlit
- spaCy
- BERT (Transformers)
- PyTorch
- scikit-learn