# Predictor for the Fracture / Bone-density project.
from pathlib import Path

import joblib
import numpy as np

from core.spec import PredictionResult

MODEL_PATH = Path(__file__).resolve().parent / "model" / "model.pkl"

# Order must match the training feature order.
FEATURE_ORDER = ["age", "sex", "asso_medical", "injury_history", "drug_history"]

_ADVICE = {"Normal": "Bone density appears within the normal range.",
           "Osteopenia": "Indicates lower-than-normal bone density; clinical follow-up advised.",
           "Osteoporotic": "Indicates significant bone-density loss; specialist consultation recommended."}


# Load the trained model (called once, then cached by the hub).
def load():
    return joblib.load(MODEL_PATH)


# Run a prediction. model is whatever load() returned; inputs are the form values.
def predict(model, inputs):
    vector = np.array([[inputs[n] for n in FEATURE_ORDER]], dtype=float)
    label = str(model.predict(vector)[0])
    confidence = float(np.max(model.predict_proba(vector)[0])) if hasattr(model, "predict_proba") else None
    return PredictionResult(label=label, confidence=confidence, detail=_ADVICE.get(label, ""))
