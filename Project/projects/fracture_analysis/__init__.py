# Fracture / Bone-density Analysis project plugin.
# Exposes PROJECT (metadata + form spec) and bp (the blueprint).
import json
from pathlib import Path

from core.spec import Field, ModelInfo, ProjectSpec
from core.views import make_blueprint

from .predictor import load, predict

_METRICS = Path(__file__).resolve().parent / "model" / "metrics.json"


# Read the accuracy written by training, with a fallback.
def _accuracy(default: str = "92%") -> str:
    try:
        return json.loads(_METRICS.read_text()).get("accuracy", default)
    except Exception:
        return default


PROJECT = ProjectSpec(
    id="fracture_analysis",
    name="Fracture & Bone Health Analysis",
    icon="bi-bandaid",
    color="#ef4444",
    category="Healthcare",
    short_description="Classify bone health from clinical risk factors.",
    description="Predicts a patient's bone-health status (Normal, Osteopenia or Osteoporotic) from age, sex and clinical history - a quick screening aid for fracture and osteoporosis risk.",
    accuracy=_accuracy(),
    kind="tabular",
    model_info=ModelInfo(
        algorithm="Decision Tree Classifier",
        features=["Age", "Sex", "Associated medical problems", "Injury / surgery history", "Drug history"],
        accuracy=_accuracy(),
        dataset="Clinical bone-density dataset (~enriched patient records).",
        notes="Screening aid only - not a substitute for clinical diagnosis."),
    fields=[
        Field("age", "Age", type="number", min=1, max=120, step="1", placeholder="e.g. 58"),
        Field("sex", "Sex", type="select", options=[("Female", 0), ("Male", 1)]),
        Field("asso_medical", "Associated medical problem", type="select",
              options=[("None", 0), ("Diabetes", 1), ("Diabetes + BP", 2), ("Blood pressure", 3),
                       ("Diabetes + Heart blockage", 4), ("Kidney stone", 5),
                       ("Increased heart rate", 6), ("Diabetes + Kidney stone", 7)]),
        Field("injury_history", "Injury / surgery history", type="select",
              options=[("None", 0), ("Varicose vein surgery", 1), ("Uterus removal", 2),
                       ("Kidney stone operation", 3), ("Uterus surgery", 4), ("Diverticulitis", 5),
                       ("Shoulder surgery", 6), ("Knee surgery", 7), ("Open heart surgery", 8)]),
        Field("drug_history", "Drug history", type="select",
              options=[("None", 0), ("Yes", 1), ("Yes (Ecosprin)", 2)]),
    ],
    load=load,
    predict=predict,
)

bp = make_blueprint(PROJECT, __name__)
