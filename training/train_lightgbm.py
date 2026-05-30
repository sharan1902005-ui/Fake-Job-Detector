import pandas as pd
import numpy as np
import joblib
import json

from scipy.sparse import hstack, csr_matrix

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import (
    classification_report,
    precision_score,
    recall_score,
    f1_score
)
from lightgbm import LGBMClassifier

# Load data
df = pd.read_csv("../data/featured_jobs.csv")

# Text
X_text = df["clean_text"]

# Target
y = df["fraudulent"]

# TF-IDF
vectorizer = TfidfVectorizer(
    max_features=10000,
    stop_words="english",
    ngram_range=(1, 2)
)

X_tfidf = vectorizer.fit_transform(X_text)

# Engineered features
extra_features = df[
    [
        "job_length",
        "has_profile",
        "requirements_length",
        "url_count",
        "money_mentions"
    ]
].fillna(0)

X_extra = csr_matrix(extra_features.values)

# Combine TF-IDF + engineered features
X = hstack([X_tfidf, X_extra])

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# LightGBM
model = LGBMClassifier(
    n_estimators=300,
    learning_rate=0.05,
    num_leaves=31,
    class_weight="balanced",
    random_state=42
)

# Train
model.fit(X_train, y_train)

# Predict
preds = model.predict(X_test)

print(classification_report(y_test, preds))

# Save model
joblib.dump(
    model,
    "../models/fraud_model.pkl"
)

joblib.dump(
    vectorizer,
    "../models/vectorizer.pkl"
)

print("Model saved!")

# Save metrics
metrics = {
    "precision": float(
        precision_score(y_test, preds)
    ),
    "recall": float(
        recall_score(y_test, preds)
    ),
    "f1": float(
        f1_score(y_test, preds)
    )
}

with open(
    "../models/model_metrics.json",
    "w"
) as f:
    json.dump(metrics, f, indent=4)

print("Metrics saved!")
