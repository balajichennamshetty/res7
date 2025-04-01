import streamlit as st
import os
import tempfile
from resume_parser import ResumeParser
from matching_engine import MatchingEngine

def main():
    st.set_page_config(page_title="Resume Screening & Ranking System", layout="wide")
    st.title("Resume Screening & Ranking System")

    # Initialize parser and matching engine
    parser = ResumeParser()
    matcher = MatchingEngine()

    # File upload section
    st.header("Upload Resumes")
    uploaded_files = st.file_uploader("Choose resume files", 
                                    type=['pdf', 'docx'], 
                                    accept_multiple_files=True)

    # Job description input
    st.header("Job Description")
    job_description = st.text_area("Enter the job description", height=200)

    if uploaded_files and job_description and st.button("Analyze and Rank"):
        with st.spinner('Processing resumes...'):
            candidates = []

            # Process each resume
            for uploaded_file in uploaded_files:
                # Save uploaded file temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    temp_path = tmp_file.name

                try:
                    # Parse resume
                    resume_info = parser.parse_resume(temp_path)
                    
                    # Add to candidates list
                    candidates.append({
                        'name': uploaded_file.name,
                        'resume_info': resume_info
                    })
                except Exception as e:
                    st.error(f"Error processing {uploaded_file.name}: {str(e)}")
                finally:
                    # Clean up temporary file
                    os.unlink(temp_path)

            # Rank candidates
            if candidates:
                ranked_candidates = matcher.rank_candidates(candidates, job_description)

                # Display results
                st.header("Ranking Results")
                for rank, candidate in enumerate(ranked_candidates, 1):
                    with st.expander(f"#{rank} - {candidate['name']} (Match Score: {candidate['scores']['overall_match']:.2f})"):
                        st.subheader("Match Scores")
                        scores = candidate['scores']
                        st.write(f"Overall Match: {scores['overall_match']:.2f}")
                        st.write(f"Skills Match: {scores['skills_match']:.2f}")
                        st.write(f"Experience Match: {scores['experience_match']:.2f}")
                        st.write(f"Education Match: {scores['education_match']:.2f}")

                        st.subheader("Extracted Information")
                        resume_info = candidate['resume_info']
                        
                        # Display skills
                        st.write("Skills:")
                        st.write(", ".join(resume_info.get('skills', [])))
                        
                        # Display education
                        st.write("Education:")
                        for edu in resume_info.get('education', []):
                            st.write(f"- {edu}")
                        
                        # Display experience
                        st.write("Experience:")
                        for exp in resume_info.get('experience', []):
                            st.write(f"- {exp}")

if __name__ == "__main__":
    main()