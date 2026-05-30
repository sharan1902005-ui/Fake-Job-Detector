import pandas as pd
import re

# Load dataset
df = pd.read_csv("../data/fake_job_postings.csv")

# Fill missing text fields
text_cols = [
    "title",
    "company_profile",
    "description",
    "requirements",
    "benefits"
]

for col in text_cols:
    df[col] = df[col].fillna("")

# Combine text
df["combined_text"] = (
    df["title"] + " " +
    df["company_profile"] + " " +
    df["description"] + " " +
    df["requirements"] + " " +
    df["benefits"]
)

# Clean text
def clean_text(text):

    text = str(text).lower()

    text = re.sub(r"http\S+", "", text)

    text = re.sub(r"[^a-zA-Z ]", " ", text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()

df["clean_text"] = df["combined_text"].apply(clean_text)

print(df["clean_text"].iloc[0][:500])
df.to_csv(
    "../data/processed_jobs.csv",
    index=False
)

print("Processed dataset saved!")