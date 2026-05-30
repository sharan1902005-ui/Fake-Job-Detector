from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from url_utils import extract_from_url
from explain import get_reasons as shap_get_reasons
import joblib
import os
import re
import numpy as np
from scipy.sparse import hstack, csr_matrix

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "..", "models")

model = joblib.load(
    os.path.join(MODELS_DIR, "fraud_model.pkl")
)

vectorizer = joblib.load(
    os.path.join(MODELS_DIR, "vectorizer.pkl")
)

class JobRequest(BaseModel):
    text: str

class URLRequest(BaseModel):
    url: str

def get_reasons(text):
    suspicious_words = [
        "earn", "money", "cash", "income", "urgent",
        "work from home", "no experience", "quick money",
        "apply now", "commission"
    ]
    text = text.lower()
    found = []
    for word in suspicious_words:
        if word in text:
            found.append(word)
    return found[:5]
def extract_extra_features(text: str):
    job_length = len(text)
    has_profile = 0
    requirements_length = 0
    url_count = len(re.findall(r"http[s]?://", text))
    money_words = ["salary", "income", "earn", "money", "cash"]
    money_mentions = sum(text.lower().count(w) for w in money_words)
    return csr_matrix([[job_length, has_profile, requirements_length, url_count, money_mentions]])

@app.get("/")
def home():
    return {
        "message":
        "Fake Job Detector API Running"
    }

@app.post("/predict")
def predict(job: JobRequest):

    X_tfidf = vectorizer.transform([job.text])
    X_extra = extract_extra_features(job.text)
    vector = hstack([X_tfidf, X_extra])

    prediction = model.predict(vector)[0]
    probability = model.predict_proba(vector)[0][1]
    reasons = shap_get_reasons(job.text)

    return {
        "prediction": "Fake" if prediction else "Real",
        "fraud_probability": round(float(probability), 4),
        "risk_level": (
            "High" if probability > 0.8
            else "Medium" if probability > 0.4
            else "Low"
        ),
        "reasons": reasons
    }

@app.post("/predict-url")
def predict_url(req: URLRequest):
    text = extract_from_url(req.url)

    if not text:
        return {"error": "Unable to extract text"}

    X_tfidf = vectorizer.transform([text])
    X_extra = extract_extra_features(text)
    vector = hstack([X_tfidf, X_extra])

    prediction = model.predict(vector)[0]
    probability = model.predict_proba(vector)[0][1]

    return {
        "prediction": "Fake" if prediction else "Real",
        "fraud_probability": round(float(probability), 4),
        "risk_level": (
            "High" if probability > 0.8
            else "Medium" if probability > 0.4
            else "Low"
        ),
        "preview": text[:300]
    }
