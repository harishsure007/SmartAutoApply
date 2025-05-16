import fitz  # PyMuPDF
import docx
import spacy
import re
import os

nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(path):
    doc = fitz.open(path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_text_from_docx(path):
    doc = docx.Document(path)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_email(text):
    match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    return match.group(0) if match else None

def extract_phone(text):
    match = re.search(r'(\+?\d{1,3}[\s-]?)?(\(?\d{3}\)?[\s-]?)?\d{3}[\s-]?\d{4}', text)
    return match.group(0) if match else None

def extract_name(text):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    return None

def extract_skills(text):
    skills_keywords = ['python', 'sql', 'excel', 'tableau', 'power bi', 'aws', 'machine learning']
    found = []
    text_lower = text.lower()
    for skill in skills_keywords:
        if skill in text_lower:
            found.append(skill)
    return list(set(found))

def parse_resume(file_path):
    ext = os.path.splitext(file_path)[-1].lower()
    if ext == ".pdf":
        text = extract_text_from_pdf(file_path)
    elif ext == ".docx":
        text = extract_text_from_docx(file_path)
    else:
        raise ValueError("Unsupported file format")

    parsed_data = {
        "Name": extract_name(text),
        "Email": extract_email(text),
        "Phone": extract_phone(text),
        "Skills": extract_skills(text)
    }

    return parsed_data

# Example usage
if __name__ == "__main__":
    resume_path = "Harish Kumar 5.pdf"  # or your_resume.docx
    data = parse_resume(resume_path)
    print("Parsed Resume Info:\n", data)
