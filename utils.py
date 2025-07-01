import os
import json
import pandas as pd
import streamlit as st

# ---------- SESSION PAGE PERSISTENCE ----------

LAST_PAGE_FILE = "last_page.json"

def save_current_page(page):
    with open(LAST_PAGE_FILE, "w") as f:
        json.dump({"page": page}, f)

def load_last_page():
    if os.path.exists(LAST_PAGE_FILE):
        with open(LAST_PAGE_FILE, "r") as f:
            data = json.load(f)
            return data.get("page")
    return "dashboard"  # Default page


# ---------- DATA LOADING HELPERS ----------

def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        df.columns = df.columns.str.strip().str.lower()
        return df
    except FileNotFoundError:
        st.error(f"🚫 File not found: {file_path}")
        return pd.DataFrame()
    except pd.errors.EmptyDataError:
        st.warning(f"⚠️ File is empty: {file_path}")
        return pd.DataFrame()


# ---------- SAVED JOB HANDLING ----------

SAVED_JOBS_FILE = "saved_jobs.csv"

def load_saved_jobs():
    if os.path.exists(SAVED_JOBS_FILE):
        return pd.read_csv(SAVED_JOBS_FILE)
    return pd.DataFrame(columns=["title", "company", "location", "matchscore", "link"])

def save_job(job_row):
    saved_jobs = load_saved_jobs()
    if job_row["link"] not in saved_jobs["link"].values:
        saved_jobs = pd.concat([saved_jobs, pd.DataFrame([job_row])], ignore_index=True)
        saved_jobs.to_csv(SAVED_JOBS_FILE, index=False)
        return True
    return False


# ---------- APPLIED JOB HANDLING ----------

def load_applied_links(path="applied_jobs.csv"):
    if os.path.exists(path):
        try:
            df = pd.read_csv(path)
            if "link" in df.columns:
                return set(df["link"].dropna().tolist())
        except pd.errors.EmptyDataError:
            return set()
    return set()
