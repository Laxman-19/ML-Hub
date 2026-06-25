# Motor Predictive-Maintenance project plugin.
import json
from pathlib import Path

from core.spec import Field, ModelInfo, ProjectSpec
from core.views import make_blueprint

from .predictor import load, predict

_METRICS = Path(__file__).resolve().parent / "model" / "metrics.json"


def _accuracy(default: str = "Unsupervised") -> str:
    try:
        return json.loads(_METRICS.read_text()).get("accuracy", default)
    except Exception:
        return default


PROJECT = ProjectSpec(
    id="motor_maintenance",
    name="Motor Predictive Maintenance",
    icon="bi-gear-wide-connected",
    color="#f59e0b",
    category="Industrial",
    short_description="Flag motors that need servicing from sensor telemetry.",
    description="Analyses live motor telemetry - current, voltage, temperature, humidity and vibration - and flags whether a unit is healthy or likely to need maintenance, enabling proactive servicing.",
    accuracy=_accuracy(),
    kind="tabular",
    model_info=ModelInfo(
        algorithm="K-Means clustering + Random Forest",
        features=["Current", "Voltage", "Temperature", "Humidity", "Vibration"],
        accuracy=_accuracy(),
        dataset="Motor sensor telemetry log.",
        notes="Unsupervised clustering surfaces anomalous operating patterns."),
    fields=[
        Field("current", "Current (A)", type="number", placeholder="e.g. 5.8"),
        Field("voltage", "Voltage (V)", type="number", placeholder="e.g. 232"),
        Field("temperature", "Temperature (C)", type="number", placeholder="e.g. 59.2"),
        Field("humidity", "Humidity (%)", type="number", placeholder="e.g. 68"),
        Field("vibration", "Vibration level", type="select", options=[("Low / Normal (0)", 0), ("High (1)", 1)]),
    ],
    load=load,
    predict=predict,
)

bp = make_blueprint(PROJECT, __name__)
