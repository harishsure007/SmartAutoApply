import streamlit as st
import pandas as pd
import os
from login import login

# ✅ Handle login session
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login()
    st.stop()
# Load matched jobs
def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        df.columns = df.columns.str.strip().str.lower()
        return df
    except FileNotFoundError:
        st.error("🚫 matched_jobs.csv not found.")
        return pd.DataFrame()

# Load applied job links
def load_applied_links(path="applied_jobs.csv"):
    if os.path.exists(path):
        try:
            df = pd.read_csv(path)
            if "link" in df.columns:
                return set(df["link"].dropna().tolist())
        except pd.errors.EmptyDataError:
            pass
    return set()

# Save applied job links
def save_applied_links(applied_links, path="applied_jobs.csv"):
    pd.DataFrame({"Link": list(applied_links)}).to_csv(path, index=False)

def main():
    st.set_page_config(page_title="Smart Auto-Apply Dashboard", layout="wide")
    st.image("smart_auto_apply_logo.png", width=160)
    st.title("💼 Smart Auto-Apply")
    st.markdown("Visualize and manage job matches from your resume.")

    df = load_data("matched_jobs.csv")
    if df.empty:
        return

    required_cols = ["title", "company", "location", "link", "matchscore"]
    for col in required_cols:
        if col not in df.columns:
            st.error(f"Missing required column: {col}")
            return

    # Sidebar filters
    st.sidebar.header("🔍 Filter Options")
    company_text = st.sidebar.text_input("🏢 Company Name", placeholder="e.g., Google")
    min_score = st.sidebar.slider("Minimum Match Score", 0.0, 1.0, 0.5, 0.01)
    keyword_search = st.sidebar.text_input("🔍 Keyword Search (Title, Company, Location)")
    show_unapplied_only = st.sidebar.checkbox("📌 Show Only Unapplied Jobs")

    emp_type_filter = st.sidebar.multiselect("Employment Type", ["Full time", "Part time", "Contract", "Third Party", "Internship"])
    posted_date_filter = st.sidebar.radio("Posted Date", ["No preference", "Today", "Last 3 days", "Last 7 days"])
    work_setting_filter = st.sidebar.multiselect("Work Setting", ["Remote", "Hybrid", "On-Site"])
    easy_apply_only = st.sidebar.checkbox("Easy Apply Only")
    radius_filter = st.sidebar.selectbox("Distance", ["No Preference", "Up to 10 miles", "Up to 30 miles", "Up to 50 miles", "Up to 75 miles"])
    min_company_rating = st.sidebar.slider("Minimum Company Rating", 0.0, 5.0, 0.0, 0.1)
    sponsorship_filter = st.sidebar.checkbox("Willing to Sponsor")
    employer_type_filter = st.sidebar.multiselect("Employer Type", ["Direct hire", "Recruiter", "Other"])
    selected_companies = st.sidebar.text_input("Specific Companies (comma-separated)")
    community_filter = st.sidebar.text_input("Community Tags")

    applied_links = load_applied_links()
    updated_applied_links = set(applied_links)

    # Apply sidebar filters
    filtered_df = df[df["matchscore"] >= min_score]
    if company_text:
        filtered_df = filtered_df[filtered_df["company"].str.contains(company_text, case=False, na=False)]
    if selected_companies:
        selected_list = [c.strip().lower() for c in selected_companies.split(",")]
        filtered_df = filtered_df[filtered_df["company"].str.lower().isin(selected_list)]
    if keyword_search:
        filtered_df = filtered_df[filtered_df[["title", "company", "location"]]
                                  .apply(lambda row: row.astype(str).str.contains(keyword_search, case=False).any(), axis=1)]
    if show_unapplied_only:
        filtered_df = filtered_df[~filtered_df["link"].isin(applied_links)]

    # 🔍 Compact Input Row Above Job Listings
    st.markdown("### 🔎 Refine Results")
    col1, col2 = st.columns([3, 1])

    combined_input = col1.text_input(
        label="",
        placeholder="🔍 Enter Job Title / Skill / Company",
        label_visibility="collapsed"
    )

    location_input = col2.text_input(
        label="",
        placeholder="📍 Enter Location (City, State, Zip)",
        label_visibility="collapsed"
    )

    if combined_input:
        filtered_df = filtered_df[
            filtered_df[["title", "company"]]
            .apply(lambda row: row.astype(str).str.contains(combined_input, case=False).any(), axis=1)
        ]
    if location_input:
        filtered_df = filtered_df[filtered_df["location"].str.contains(location_input, case=False, na=False)]

    # Display results
    st.markdown(f"### 📊 Showing {len(filtered_df)} matched jobs")
    st.metric("Total Matches", len(filtered_df))
    if not filtered_df.empty:
        st.metric("Top Match Score", f"{filtered_df['matchscore'].max():.2f}")

    st.download_button("📥 Download Filtered Jobs", filtered_df.to_csv(index=False), "matched_jobs.csv", "text/csv")

    if not filtered_df.empty:
        for index, row in filtered_df.iterrows():
            with st.container():
                col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 2, 1])
                # ✅ Job title as clickable link
                col1.markdown(f"**[{row['title']}]({row['link']})**")
                col2.write(row['company'])
                col3.write(row['location'])
                col4.write(f"{row['matchscore']:.2f}" if row['matchscore'] <= 0.75 else f"✅ **{row['matchscore']:.2f}**")
                applied = row['link'] in applied_links
                is_checked = col5.checkbox("Applied", value=applied, key=row['link'])

                if is_checked and not applied:
                    updated_applied_links.add(row['link'])
                elif not is_checked and applied:
                    updated_applied_links.discard(row['link'])

        if updated_applied_links != applied_links:
            save_applied_links(updated_applied_links)
            st.success("✅ Applied status updated.")
    else:
        st.warning("No jobs match the current filters.")

if __name__ == "__main__":
    main()
