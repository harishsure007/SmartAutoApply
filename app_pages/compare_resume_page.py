import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import spacy

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# ------------------------- Helper Functions -------------------------

def extract_keywords(text):
    doc = nlp(text)
    return {
        token.text.lower()
        for token in doc
        if token.pos_ in ["NOUN", "VERB", "PROPN"] and not token.is_stop and token.is_alpha
    }

def highlight_keywords(text, matches, missing, color_matched="green", color_missing="red"):
    words = text.split()
    highlighted = []
    for word in words:
        clean_word = re.sub(r"[^\w\s]", "", word).lower()
        if clean_word in matches:
            highlighted.append(f"<span style='color:{color_matched}; font-weight:bold'>{word}</span>")
        elif clean_word in missing:
            highlighted.append(f"<span style='color:{color_missing};'>{word}</span>")
        else:
            highlighted.append(word)
    return " ".join(highlighted)

def get_top_tfidf_keywords(text, top_n=10):
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform([text])
    feature_names = tfidf.get_feature_names_out()
    scores = tfidf_matrix.toarray()[0]
    keyword_scores = list(zip(feature_names, scores))
    keyword_scores.sort(key=lambda x: x[1], reverse=True)
    top_keywords = [kw for kw, score in keyword_scores[:top_n]]
    return set(top_keywords)

# ------------------------- Main Page Function -------------------------

def compare_resume_page():
    st.title("📘 Resume vs Job Description Comparison")

    # 🛠️ Debug current page and JD length
    st.markdown(f"🛠️ DEBUG: Current page = 📄 Compare Resume")
    jd_text = st.session_state.get("jd_text", "")
    resumes = st.session_state.get("resume_list", [])

    st.write(f"📝 Job Description length: {len(jd_text)} characters")

    if not resumes:
        st.warning("⚠️ No resumes found. Please upload your resume(s) first.")
        return

    if not jd_text.strip():
        st.warning("⚠️ No job description found. Please enter or upload a job description first.")
        return

    for idx, (name, resume_text) in enumerate(resumes):
        st.markdown(f"## 📝 Resume: `{name}`")

        # TF-IDF similarity between resume and JD
        tfidf = TfidfVectorizer(stop_words='english')
        vectors = tfidf.fit_transform([resume_text, jd_text])
        similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
        score_percent = similarity * 100

        st.markdown(
            f"""
            <div style='font-size: 20px; font-weight: bold;'>🎯 Resume Match Accuracy</div>
            <div style='font-size: 28px; color: green; font-weight: bold;'>{score_percent:.0f}%</div>
            """,
            unsafe_allow_html=True
        )

        # Extract top keywords
        main_jd_keywords = get_top_tfidf_keywords(jd_text, top_n=10)
        resume_keywords = extract_keywords(resume_text)
        jd_keywords = extract_keywords(jd_text)

        matched = jd_keywords & resume_keywords
        missing = jd_keywords - resume_keywords

        st.markdown("### 🎯 Main Keywords in Job Description (Top 10)")
        st.markdown(", ".join(sorted(main_jd_keywords)) or "No main keywords found.")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("✅ **Matched Keywords**")
            st.markdown(", ".join(sorted(matched)) or "No matches found.")
        with col2:
            st.markdown("❌ **Missing Keywords**")
            st.markdown(", ".join(sorted(missing)) or "No missing keywords.")

        st.markdown("### 🧾 Resume Highlight")
        st.markdown(highlight_keywords(resume_text, matched, set()), unsafe_allow_html=True)

        st.markdown("### 📄 Job Description Highlight")
        st.markdown(highlight_keywords(jd_text, matched, missing), unsafe_allow_html=True)

        # Save to session state for CV Builder page
        if idx == 0:
            st.session_state.selected_resume = resume_text
            st.session_state.selected_jd = jd_text
            st.session_state.missing_keywords = list(missing)

        if st.button(f"🚀 Improve Resume: {name}", key=f"improve_resume_{idx}"):
            st.session_state.selected_resume = resume_text
            st.session_state.selected_jd = jd_text
            st.session_state.missing_keywords = list(missing)
            st.session_state.page = "📄 Resume Optimizer"
            st.experimental_rerun()

        st.markdown("---")

    if st.button("⬅️ Back to Dashboard"):
        st.session_state.page = "📈 Dashboard"
        st.experimental_rerun()
