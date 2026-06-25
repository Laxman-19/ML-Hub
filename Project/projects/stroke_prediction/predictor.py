# Predictor for the Stroke-risk project.
from pathlib import Path

import joblib
import numpy as np

from core.spec import PredictionResult

MODEL_DIR = Path(__file__).resolve().parent / "model"
FEATURE_ORDER = ["gender", "age", "hypertension", "heart_disease", "ever_married",
                 "work_type", "residence_type", "avg_glucose_level", "bmi", "smoking_status"]


# Load the model and its scaler (called once, then cached by the hub).
def load():
    return {"model": joblib.load(MODEL_DIR / "model.pkl"), "scaler": joblib.load(MODEL_DIR / "scaler.pkl")}


def predict(model, inputs):
    vector = np.array([[inputs[n] for n in FEATURE_ORDER]], dtype=float)
    scaled = model["scaler"].transform(vector)
    clf = model["model"]
    pred = int(clf.predict(scaled)[0])
    proba = clf.predict_proba(scaled)[0]
    label = "High Stroke Risk" if pred == 1 else "Low Stroke Risk"
    detail = ("Model flags elevated stroke risk - recommend clinical evaluation." if pred == 1
              else "Model estimates low stroke risk based on the provided factors.")
    return PredictionResult(label=label, confidence=float(np.max(proba)), detail=detail,
                            extra={"stroke_probability": round(float(proba[1]) * 100, 1)})
