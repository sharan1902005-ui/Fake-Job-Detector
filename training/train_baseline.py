import pandas as pd

from sklearn.model_selection import train_test_split

from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.linear_model import LogisticRegression

from sklearn.metrics import classification_report
from sklearn.metrics import (
    confusion_matrix,
    ConfusionMatrixDisplay,
    roc_auc_score,
    RocCurveDisplay
)

import matplotlib.pyplot as plt

# Load processed data
df = pd.read_csv("../data/processed_jobs.csv")

X = df["clean_text"]

y = df["fraudulent"]

# TF-IDF
vectorizer = TfidfVectorizer(
    max_features=5000,
    stop_words="english"
)

X = vectorizer.fit_transform(X)

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Train
model = LogisticRegression(
    class_weight="balanced",
    max_iter=1000
)

model.fit(X_train, y_train)

# Predict
preds = model.predict(X_test)

print(
    classification_report(
        y_test,
        preds
    )
)

# Confusion Matrix
cm = confusion_matrix(y_test, preds)

print("\nConfusion Matrix:")
print(cm)

ConfusionMatrixDisplay.from_predictions(
    y_test,
    preds
)

plt.show()

# ROC-AUC Score
probs = model.predict_proba(X_test)[:, 1]

roc = roc_auc_score(y_test, probs)

print(f"\nROC AUC Score: {roc:.4f}")

# Top Fraud Indicators
feature_names = vectorizer.get_feature_names_out()

coefficients = model.coef_[0]

top_fraud = coefficients.argsort()[-20:]

print("\nTop Fraud Indicators:\n")

for idx in reversed(top_fraud):
    print(
        feature_names[idx],
        round(coefficients[idx], 3)
    )

# Top Real Indicators
top_real = coefficients.argsort()[:20]

print("\nTop Real Indicators:\n")

for idx in top_real:
    print(
        feature_names[idx],
        round(coefficients[idx], 3)
    )
