import streamlit as st
import openai
import re
import spacy
from PyPDF2 import PdfReader
import base64

# Load spaCy model with error handling
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    st.error("SpaCy model 'en_core_web_sm' not found. Run `python -m spacy download en_core_web_sm`.")
    st.stop()

# ----------- Utility Functions -----------

def clean_resume_text(text):
    if not text:
        return ""
    text = text.replace('\r\n', ' ').replace('\r', ' ').replace('\n', ' ')
    return re.sub(r'\s+', ' ', text).strip()

def extract_keywords(text):
    doc = nlp(text)
    keywords = set()
    for token in doc:
        if token.pos_ in ["NOUN", "VERB", "PROPN"] and not token.is_stop and token.is_alpha:
            keywords.add(token.lemma_.lower())
    return sorted(list(keywords))[:30]

def extract_text_from_pdf(file):
    try:
        reader = PdfReader(file)
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return ""

def insert_keywords_into_resume(resume_text, keywords):
    for kw in keywords:
        if kw.lower() not in resume_text.lower():
            resume_text += f"\n• {kw.capitalize()}"
    return resume_text.strip()

def generate_resume_from_jd(jd_text):
    prompt = f"Generate a professional resume tailored for this job description:\n{jd_text.strip()}"
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional resume generator."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"OpenAI API Error: {e}")
        return None

def generate_resume_from_command(command_text):
    prompt = f"Based on this command, generate a professional resume:\n{command_text.strip()}"
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that creates professional resumes."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"OpenAI API Error: {e}")
        return None

def download_button(text, filename):
    b64 = base64.b64encode(text.encode()).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="{filename}">📥 Download Updated Resume</a>'
    st.markdown(href, unsafe_allow_html=True)

# ----------- Main Page -----------

def cv_builder_page():
    st.title("📄 ATS Resume Optimizer Bot")
    st.markdown("---")

    # PDF Upload
    uploaded_file = st.file_uploader("📄 Upload Resume PDF (optional)", type=["pdf"])
    if uploaded_file:
        text = extract_text_from_pdf(uploaded_file)
        if text:
            st.session_state["uploaded_resume"] = text
            st.success("✅ PDF Resume uploaded and text extracted.")
            st.experimental_rerun()

    if "uploaded_resume" not in st.session_state and "job_description" not in st.session_state:
        st.warning("⚠️ Please upload your resume or provide a job description in the **Dashboard**.")
        return

    # Show Job Description length
    if "job_description" in st.session_state:
        jd_text = st.session_state["job_description"]
        st.write(f"📝 Job Description length: {len(jd_text)} characters")

    # Case: Generate resume from JD if no resume exists
    if "job_description" in st.session_state and "uploaded_resume" not in st.session_state:
        st.info("No resume uploaded. You can generate one from Job Description.")
        if st.button("🤖 Generate Resume from JD"):
            with st.spinner("Generating resume..."):
                resume = generate_resume_from_jd(st.session_state["job_description"])
                if resume:
                    st.session_state["uploaded_resume"] = resume
                    st.success("✅ Resume generated.")
                    st.experimental_rerun()
        return

    # Keyword Extraction
    st.markdown("---")
    st.subheader("🔑 Extracted Keywords")
    if "job_description" in st.session_state and st.session_state["job_description"]:
        keywords = extract_keywords(st.session_state["job_description"])
        st.info("Keywords extracted from Job Description.")
    else:
        keywords = extract_keywords(st.session_state["uploaded_resume"])
        st.info("Keywords extracted from Resume.")

    if keywords:
        st.markdown(f"**Top Keywords:** {', '.join(keywords)}")
    else:
        st.warning("No keywords found.")

    # Resume Editor
    st.markdown("---")
    st.subheader("✏️ Edit Resume")

    resume_text = clean_resume_text(st.session_state["uploaded_resume"])
    edited_text = st.text_area("Your Resume:", value=resume_text, height=500)

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("💾 Save Resume"):
            st.session_state["uploaded_resume"] = edited_text
            st.success("✅ Resume updated.")
            st.experimental_rerun()

    with col2:
        if st.button("✨ Enhance with Keywords"):
            enhanced = insert_keywords_into_resume(edited_text, keywords)
            st.session_state["uploaded_resume"] = enhanced
            st.success("✅ Keywords added.")
            st.experimental_rerun()

    # Resume Download
    st.markdown("### 📥 Download Resume")
    download_button(st.session_state["uploaded_resume"], "optimized_resume.txt")

    # Chat Command Generator
    st.markdown("---")
    st.subheader("💬 Generate Resume with Instructions")

    command_input = st.text_area("🗒️ Enter command (e.g., 'Create a resume for a Data Analyst role with Python & SQL')", height=150)
    if st.button("🧠 Generate Resume from Command"):
        if command_input.strip():
            with st.spinner("Generating..."):
                gen_resume = generate_resume_from_command(command_input)
                if gen_resume:
                    st.session_state["uploaded_resume"] = gen_resume
                    st.success("✅ Resume created from your command.")
                    st.experimental_rerun()
        else:
            st.warning("❗ Please enter a command.")


    # ⬅️ Back to Dashboard Button
    st.markdown("---")
    if st.button("⬅️ Back to Dashboard"):
        st.session_state.page = "📈 Dashboard"
        st.experimental_rerun()


# Optional standalone execution
if __name__ == "__main__":
    cv_builder_page()
