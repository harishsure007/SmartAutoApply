import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from resume_parser import parse_resume

def load_resume_keywords(resume_file):
    parsed_data = parse_resume(resume_file)
    skills = parsed_data.get("Skills", [])
    return " ".join(skills)

def run_matching(resume_file, jobs_file="dice_jobs.csv", output_file="matched_jobs.csv"):
    try:
        jobs_df = pd.read_csv(jobs_file)
    except pd.errors.EmptyDataError:
        print(f"❌ {jobs_file} is empty or missing headers.")
        return

    # Normalize column names
    jobs_df.columns = jobs_df.columns.str.strip().str.lower()

    # Rename known variants to expected column names
    rename_map = {
        'job title': 'title',
        'title': 'title',
        'company name': 'company',
        'employer': 'company',
        'location': 'location',
        'job location': 'location',
        'apply': 'link',
        'apply link': 'link',
        'url': 'link',
    }
    jobs_df.rename(columns=rename_map, inplace=True)

    # Final check for required columns
    required_columns = ["title", "company", "location", "link"]
    missing = [col for col in required_columns if col not in jobs_df.columns]

    if missing:
        print(f"❌ Missing columns: {missing}")
        print("🧪 Detected columns:", list(jobs_df.columns))
        return

    # Combine job text
    jobs_df["combinedtext"] = jobs_df["title"].fillna('') + " " + \
                              jobs_df["company"].fillna('') + " " + \
                              jobs_df["location"].fillna('')

    resume_text = load_resume_keywords(resume_file)

    # TF-IDF + cosine similarity
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(jobs_df["combinedtext"].tolist() + [resume_text])
    cosine_similarities = cosine_similarity(tfidf_matrix[-1:], tfidf_matrix[:-1]).flatten()

    jobs_df["matchscore"] = cosine_similarities

    matched_jobs = jobs_df.sort_values(by="matchscore", ascending=False)
    matched_jobs.to_csv(output_file, index=False)

    print(f"✅ Matching complete. Top matches saved to {output_file}")
    print(matched_jobs[["title", "company", "location", "matchscore"]].head(10))

if __name__ == "__main__":
    run_matching("Harish kumar 5.pdf", jobs_file="dice_jobs.csv")
