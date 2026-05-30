import shap
import joblib
import numpy as np
import re
from scipy.sparse import hstack, csr_matrix

model = joblib.load("../models/fraud_model.pkl")
vectorizer = joblib.load("../models/vectorizer.pkl")

explainer = shap.TreeExplainer(model)

def extract_extra_features(text):
    job_length = len(text)
    has_profile = 0
    requirements_length = 0
    url_count = len(re.findall(r"http[s]?://", text))
    money_words = ["salary", "income", "earn", "money", "cash"]
    money_mentions = sum(text.lower().count(w) for w in money_words)
    return csr_matrix([[job_length, has_profile, requirements_length, url_count, money_mentions]])

def get_reasons(text, top_n=5):
    X_tfidf = vectorizer.transform([text])
    X_extra = extract_extra_features(text)
    vector = hstack([X_tfidf, X_extra]).astype(np.float32)

    shap_values = explainer.shap_values(vector)

    # Convert to dense and flatten to 1D array
    raw = shap_values[1] if isinstance(shap_values, list) else shap_values
    if hasattr(raw, "toarray"):
        raw = raw.toarray()
    values = np.array(raw).flatten()

    feature_names = list(vectorizer.get_feature_names_out()) + [
        "job_length", "has_profile", "requirements_length", "url_count", "money_mentions"
    ]

    pairs = sorted(zip(feature_names, values), key=lambda x: abs(float(x[1])), reverse=True)

    reasons = [word for word, score in pairs if float(score) > 0][:top_n]

    return reasons
