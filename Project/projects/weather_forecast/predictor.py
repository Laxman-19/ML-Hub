# Predictor for the Weather-type project.
from pathlib import Path

import joblib
import numpy as np

from core.spec import PredictionResult

MODEL_PATH = Path(__file__).resolve().parent / "model" / "model.pkl"
FEATURE_ORDER = ["precipitation", "temp_max", "temp_min", "wind"]

_FORECAST = {"drizzle": "light drizzle expected", "rain": "rain likely", "sun": "clear / sunny conditions",
             "snow": "snowfall likely", "fog": "foggy conditions"}


def load():
    return joblib.load(MODEL_PATH)


def predict(model, inputs):
    vector = np.array([[inputs[n] for n in FEATURE_ORDER]], dtype=float)
    label = str(model.predict(vector)[0])
    confidence = float(np.max(model.predict_proba(vector)[0])) if hasattr(model, "predict_proba") else None
    return PredictionResult(label=label.capitalize(), confidence=confidence,
                            detail=f"Forecast: {_FORECAST.get(label, label)}.")
