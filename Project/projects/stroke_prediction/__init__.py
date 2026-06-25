# Stroke-risk Prediction project plugin.
import json
from pathlib import Path

from core.spec import Field, ModelInfo, ProjectSpec
from core.views import make_blueprint

from .predictor import load, predict

_METRICS = Path(__file__).resolve().parent / "model" / "metrics.json"


def _accuracy(default: str = "95%") -> str:
    try:
        return json.loads(_METRICS.read_text()).get("accuracy", default)
    except Exception:
        return default


PROJECT = ProjectSpec(
    id="stroke_prediction",
    name="Stroke Risk Prediction",
    icon="bi-heart-pulse",
    color="#ec4899",
    category="Healthcare",
    short_description="Estimate stroke risk from patient health profile.",
    description="Estimates the likelihood of stroke from demographic and clinical indicators such as age, glucose level, BMI, hypertension and smoking status. Intended as a screening and awareness aid.",
    accuracy=_accuracy(),
    kind="tabular",
    model_info=ModelInfo(
        algorithm="Logistic Regression (class-balanced)",
        features=["Gender", "Age", "Hypertension", "Heart disease", "Marital status", "Work type",
                  "Residence", "Glucose level", "BMI", "Smoking status"],
        accuracy=_accuracy(),
        dataset="Public healthcare stroke dataset (~5,000 records).",
        notes="Screening aid only - not a medical diagnosis."),
    fields=[
        Field("gender", "Gender", type="select", options=[("Female", 0), ("Male", 1), ("Other", 2)]),
        Field("age", "Age", type="number", min=0, max=120, step="1", placeholder="e.g. 67"),
        Field("hypertension", "Hypertension", type="select", options=[("No", 0), ("Yes", 1)]),
        Field("heart_disease", "Heart disease", type="select", options=[("No", 0), ("Yes", 1)]),
        Field("ever_married", "Ever married", type="select", options=[("No", 0), ("Yes", 1)]),
        Field("work_type", "Work type", type="select",
              options=[("Private", 0), ("Self-employed", 1), ("Govt job", 2), ("Children", 3), ("Never worked", 4)]),
        Field("residence_type", "Residence type", type="select", options=[("Rural", 0), ("Urban", 1)]),
        Field("avg_glucose_level", "Average glucose level", type="number", min=0, placeholder="e.g. 145.6"),
        Field("bmi", "BMI", type="number", min=0, placeholder="e.g. 29.5"),
        Field("smoking_status", "Smoking status", type="select",
              options=[("Formerly smoked", 0), ("Never smoked", 1), ("Smokes", 2), ("Unknown", 3)]),
    ],
    load=load,
    predict=predict,
)

bp = make_blueprint(PROJECT, __name__)
