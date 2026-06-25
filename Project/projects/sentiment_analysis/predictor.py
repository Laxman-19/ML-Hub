# Predictor for the Sentiment-analysis project.
from pathlib import Path

import joblib
import numpy as np

from core.spec import PredictionResult

MODEL_DIR = Path(__file__).resolve().parent / "model"

_DETAIL = {"Positive": "The text expresses an overall positive sentiment.",
           "Negative": "The text expresses an overall negative sentiment.",
           "Neutral": "The text reads as neutral / mixed."}


# Load the model and the TF-IDF vectorizer (cached by the hub).
def load():
    return {"model": joblib.load(MODEL_DIR / "model.pkl"), "vectorizer": joblib.load(MODEL_DIR / "vectorizer.pkl")}


def predict(model, inputs):
    vec = model["vectorizer"].transform([str(inputs["text"]).strip()])
    clf = model["model"]
    label = str(clf.predict(vec)[0])
    return PredictionResult(label=label, confidence=float(np.max(clf.predict_proba(vec)[0])),
                            detail=_DETAIL.get(label, ""))
