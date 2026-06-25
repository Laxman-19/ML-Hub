# Predictor for the Motor predictive-maintenance project.
import json
from pathlib import Path

import joblib
import numpy as np

from core.spec import PredictionResult

MODEL_DIR = Path(__file__).resolve().parent / "model"
FEATURE_ORDER = ["current", "voltage", "temperature", "humidity", "vibration"]


# Load the classifier and the cluster->status map (cached by the hub).
def load():
    return {"model": joblib.load(MODEL_DIR / "model.pkl"),
            "label_map": json.loads((MODEL_DIR / "label_map.json").read_text())}


def predict(model, inputs):
    vector = np.array([[inputs[n] for n in FEATURE_ORDER]], dtype=float)
    clf = model["model"]
    cluster = int(clf.predict(vector)[0])
    label = model["label_map"].get(str(cluster), "Unknown")
    confidence = float(np.max(clf.predict_proba(vector)[0])) if hasattr(clf, "predict_proba") else None
    detail = ("Sensor pattern resembles units that needed servicing - schedule maintenance."
              if label == "Maintenance Required" else "Sensor readings are within the healthy operating envelope.")
    return PredictionResult(label=label, confidence=confidence, detail=detail)
