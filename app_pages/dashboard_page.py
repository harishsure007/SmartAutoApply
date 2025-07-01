import streamlit as st
import pandas as pd
import os
import re
import spacy
import PyPDF2  # Required for PDF parsing

from login import clear_session
from app_pages.compare_resume_page import compare_resume_page
from utils import load_data, load_applied_links, load_saved_jobs, save_job

nlp = spacy.load("en_core_web_sm")

# ---------- DASHBOARD ----------
def dashboard():
    st.title("💼 Smart Auto-Apply")

    global_search = st.text_input("🔍 Search jobs (title, company, location, etc.)", "")
    
    # ----------- Initialize session state variables -----------
    if "resume_list" not in st.session_state:
        st.session_state.resume_list = []
    if "job_description" not in st.session_state:
        st.session_state.job_description = ""
    if "uploaded_resume" not in st.session_state:
        st.session_state.uploaded_resume = ""
    if "page" not in st.session_state:
        st.session_state.page = "dashboard"
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False  # ✅ No clear_session here

    # ----------- Top Navigation Bar -----------
    top_col1, top_col2 = st.columns([10, 2])
    with top_col2:
        menu_options = ["👤 Account", "🔓 Logout"]
        selected = st.selectbox("", menu_options, label_visibility="collapsed")
        if selected == "🔓 Logout":
            # ✅ Logout: clear session and redirect
            st.session_state.clear()
            clear_session()
            st.session_state.page = "login"
            st.rerun()

    # ----------- Load and normalize matched job data -----------
    df = load_data("matched_jobs.csv")

    if df.empty:
        st.warning("📂 No matched jobs found.")
        return

    df.columns = df.columns.str.strip().str.lower()

    required_cols = ["title", "company", "location", "link", "matchscore"]
    for col in required_cols:
        if col not in df.columns:
            st.error(f"🛒 Missing required column: {col}")
            return

    # ----------- Sidebar Filters -----------
    st.sidebar.header("🔍 Filter Options")
    company_text = st.sidebar.text_input("🏢 Company Name")
    min_score_percent = st.sidebar.slider("Minimum Match Score (%)", 0, 100, 50, 1)
    min_score = min_score_percent / 100
    keyword_search = st.sidebar.text_input("🔍 Keyword Search")
    show_unapplied_only = st.sidebar.checkbox("📌 Show Only Unapplied Jobs")
    emp_type_filter = st.sidebar.multiselect(
        "💼 Employment Type",
        ["Full time", "Part time", "Contract", "Third Party", "Internship"]
    )
    posted_date_filter = st.sidebar.radio(
        "📅 Posted Date", ["No preference", "Today", "Last 3 days", "Last 7 days"]
    )
    work_setting_filter = st.sidebar.multiselect(
        "🏠 Work Setting", ["Remote", "Hybrid", "On-Site"]
    )
    easy_apply_only = st.sidebar.checkbox("⚡ Easy Apply Only")
    radius_filter = st.sidebar.selectbox(
        "📍 Distance", ["No Preference", "Up to 10 miles", "Up to 30 miles", "Up to 50 miles", "Up to 75 miles"]
    )
    min_company_rating = st.sidebar.slider("⭐ Minimum Company Rating", 0.0, 5.0, 0.0, 0.1)
    sponsorship_filter = st.sidebar.checkbox("🛂 Willing to Sponsor")
    employer_type_filter = st.sidebar.multiselect(
        "🧑‍💼 Employer Type", ["Direct hire", "Recruiter", "Other"]
    )
    selected_companies = st.sidebar.text_input("🏢 Specific Companies (comma-separated)")
    community_filter = st.sidebar.text_input("🏷️ Community Tags")

    # ----------- Apply Filters -----------
    filtered_df = df[df["matchscore"] >= min_score]

    if company_text:
        filtered_df = filtered_df[
            filtered_df["company"].str.contains(company_text, case=False, na=False)
        ]

    if keyword_search:
        keyword = keyword_search.lower()
        filtered_df = filtered_df[
            filtered_df.apply(lambda row: keyword in str(row).lower(), axis=1)
        ]

    applied_links = load_applied_links()
    if show_unapplied_only and "link" in filtered_df.columns:
        filtered_df = filtered_df[~filtered_df["link"].isin(applied_links)]

    # ----------- Display Filtered Jobs -----------
    st.markdown(f"### 📄 Showing {len(filtered_df)} filtered job(s)")
    if not filtered_df.empty:
        for i, row in filtered_df.iterrows():
            with st.expander(f"🔹 {row['title']} at {row['company']}"):
                st.write(f"**📍 Location:** {row['location']}")
                st.write(f"**🎯 Match Score:** {round(row['matchscore'] * 100, 2)}%")
                st.write(f"[🔗 View Job Posting]({row['link']})")

                if st.button(f"📎 Save Job #{i}", key=f"save_{i}"):
                    if save_job(row):
                        st.success("✅ Job saved!")
                    else:
                        st.info("ℹ️ Already saved.")
    else:
        st.warning("⚠️ No job listings match your current filters.")
        st.markdown(
            """
            ### 💡 Tips to Find More Jobs:
            - Try **removing some filters** like location, company, or score thresholds.
            - Widen your **Minimum Match Score** range.
            - Use **broader keywords** (e.g., “analyst” instead of “data analyst”).
            - Make sure your `matched_jobs.csv` contains updated job data.
            """
        )
        if st.button("🔄 Reset Filters"):
            st.rerun()  # ✅ Updated

    # ----------- Resume & JD Upload + Comparison Section -----------
    st.markdown("### 📊 Resume vs Job Description Matcher")
    matcher_col1, matcher_col2 = st.columns(2)

    # ----------- Resume Upload -----------
    with matcher_col1:
        uploaded_resumes = st.file_uploader(
            "📄 Upload Resumes (.txt or .pdf)", 
            type=["txt", "pdf"], 
            accept_multiple_files=True, 
            key="resumes_multi"
        )
        resumes = []
        if uploaded_resumes:
            for file in uploaded_resumes:
                if file.type == "text/plain":
                    text = file.read().decode("utf-8")
                elif file.type == "application/pdf":
                    reader = PyPDF2.PdfReader(file)
                    text = "\n".join([page.extract_text() or "" for page in reader.pages])
                else:
                    text = ""
                resumes.append((file.name, text))
            st.session_state.resume_list = resumes

            # Store first resume text for CV Builder / Resume Optimizer
            if resumes:
                st.session_state.uploaded_resume = resumes[0][1]

    # ----------- Job Description Upload -----------
    with matcher_col2:
        jd_file = st.file_uploader(
            "📅 Upload Job Description (.txt or .pdf)", 
            type=["txt", "pdf"], 
            key="jd_single"
        )
        if jd_file:
            if jd_file.type == "text/plain":
                jd_text = jd_file.read().decode("utf-8")
            elif jd_file.type == "application/pdf":
                reader = PyPDF2.PdfReader(jd_file)
                jd_text = "\n".join([page.extract_text() or "" for page in reader.pages])
            else:
                jd_text = ""
            st.session_state.job_description = jd_text
            st.session_state.jd_text = jd_text

    # ----------- Compare Button and Status -----------
    resume_list = st.session_state.get("resume_list", [])
    job_description = st.session_state.get("job_description", "")

    if resume_list and job_description:
        st.success(f"✅ {len(resume_list)} resume(s) and job description uploaded.")
        if st.button("🔍 Compare Now"):
            st.session_state.page = "📄 Compare Resume"
            st.rerun()  # ✅ Updated
    else:
        st.info("📂 Upload both resumes and job description to enable comparison.")
