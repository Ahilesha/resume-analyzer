import streamlit as st
import PyPDF2
import spacy
from pdf2image import convert_from_bytes
import pytesseract
import io

# Load NLP model
nlp = spacy.load("en_core_web_sm")

# Function to extract text from PDF
def extract_text_from_pdf(uploaded_file):
    text = ""

    # Convert Streamlit's UploadedFile to a file-like object
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.getvalue()))

    for page in pdf_reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    print("Extracted Text:", text)  # Debugging

    return text
# Function to analyze resume content
def analyze_resume(text):
    doc = nlp(text)
    text_words= set(word.lower() for word in text.split())
    skills = {
        "Python", "Java", "SQL", "Machine Learning", "Deep Learning", 
        "Data Science", "C++", "JavaScript(Angular)", "React", "Node.js", "Django",
        "Flask", "Cloud Computing", "AWS", "Azure", "Linux"
    }

    found_skills = skills.intersection(text_words)
    print("Extracted Words:", text_words)
    print("Matched Skills:", found_skills)
    job_titles = set()

    for token in doc:
        if token.text in skills:
            found_skills.add(token.text)

    for ent in doc.ents:
        if ent.label_ == "ORG" or ent.label_ == "PERSON":
            job_titles.add(ent.text)

    return {
        "Entities": [(ent.text, ent.label_) for ent in doc.ents],  
        "Skills Matched": list(found_skills),
        "Possible Job Titles": list(job_titles)
    }

# Streamlit UI
st.title("📄 Resume Analyzer")
st.write("Upload a resume (PDF) to analyze skills and job titles.")

uploaded_file = st.file_uploader("uploaded_resume", type="pdf")

if uploaded_file:
    resume_text = extract_text_from_pdf(uploaded_file)
    st.subheader("Extracted Resume Text:")
    st.write(resume_text)
    analysis_result = analyze_resume(resume_text)

    st.subheader("Analysis Results")
    st.write("### 📌 Skills Matched:")
    st.write(", ".join(analysis_result["Skills Matched"]))
    
    st.write("### 💼 Possible Job Titles:")
    st.write(", ".join(analysis_result["Possible Job Titles"]))

    st.write("### 🔍 Extracted Entities:")
    st.json(analysis_result["Entities"])
