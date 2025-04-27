import pandas as pd
import os
import PyPDF2
import docx
import re

def extract_text_from_pdf(file_path):
    with open(file_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

def parse_resume_text(resume_text):
    # Simple parsing logic to extract name, skills, and experience
    # This is a basic example; you may need to adjust the regex patterns based on your resume format
    name_pattern = r'(?<=Name:)(.*?)(?=\n)'  # Assuming the name is prefixed with "Name:"
    skills_pattern = r'(?<=Skills:)(.*?)(?=\n)'  # Assuming skills are prefixed with "Skills:"
    experience_pattern = r'(?<=Experience:)(.*?)(?=\n)'  # Assuming experience is prefixed with "Experience:"

    name = re.search(name_pattern, resume_text)
    skills = re.search(skills_pattern, resume_text)
    experience = re.search(experience_pattern, resume_text)

    return {
        'Name': name.group(0).strip() if name else "Unknown",
        'Skills': skills.group(0).strip() if skills else "N/A",
        'Experience': experience.group(0).strip() if experience else "N/A"
    }

def load_candidate_data_from_resumes(uploaded_files):
    candidates = []
    
    for uploaded_file in uploaded_files:
        file_path = os.path.join("data", uploaded_file.name)
        
        # Save the uploaded file temporarily
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Extract text based on file type
        if uploaded_file.type == "application/pdf":
            resume_text = extract_text_from_pdf(file_path)
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            resume_text = extract_text_from_docx(file_path)
        else:
            continue  # Skip unsupported file types
        
        # Parse the resume text to extract candidate information
        candidate_info = parse_resume_text(resume_text)
        candidates.append(candidate_info)
    
    # Create a DataFrame from the list of candidates
    return pd.DataFrame(candidates)
