import pandas as pd
import re

df = pd.read_csv("../data/processed_jobs.csv")

# Feature 1: Job Description Length
df["job_length"] = df["description"].fillna("").str.len()

# Feature 2: Company Profile Exists
df["has_profile"] = (
    df["company_profile"]
    .fillna("")
    .str.len() > 0
).astype(int)

# Feature 3: Requirements Length
df["requirements_length"] = (
    df["requirements"]
    .fillna("")
    .str.len()
)

# Feature 4: URL Count
def count_urls(text):
    return len(
        re.findall(
            r"http[s]?://",
            str(text)
        )
    )

df["url_count"] = (
    df["combined_text"]
    .apply(count_urls)
)

# Feature 5: Money Words
money_words = [
    "salary",
    "income",
    "earn",
    "money",
    "cash"
]

def money_count(text):
    text = str(text).lower()
    return sum(
        text.count(word)
        for word in money_words
    )

df["money_mentions"] = (
    df["combined_text"]
    .apply(money_count)
)

print(
    df[
        [
            "job_length",
            "has_profile",
            "requirements_length",
            "url_count",
            "money_mentions"
        ]
    ].head()
)

df.to_csv(
    "../data/featured_jobs.csv",
    index=False
)

print("Features saved.")
