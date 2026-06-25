# Weather-type Forecast project plugin.
import json
from pathlib import Path

from core.spec import Field, ModelInfo, ProjectSpec
from core.views import make_blueprint

from .predictor import load, predict

_METRICS = Path(__file__).resolve().parent / "model" / "metrics.json"


def _accuracy(default: str = "85%") -> str:
    try:
        return json.loads(_METRICS.read_text()).get("accuracy", default)
    except Exception:
        return default


PROJECT = ProjectSpec(
    id="weather_forecast",
    name="Weather Forecast",
    icon="bi-cloud-sun",
    color="#0ea5e9",
    category="Environment",
    short_description="Classify the day's weather from atmospheric readings.",
    description="Predicts the weather type (sun, rain, drizzle, snow or fog) from precipitation, maximum and minimum temperature and wind speed using a Random Forest classifier.",
    accuracy=_accuracy(),
    kind="tabular",
    model_info=ModelInfo(
        algorithm="Random Forest Classifier",
        features=["Precipitation", "Max temperature", "Min temperature", "Wind"],
        accuracy=_accuracy(),
        dataset="Daily weather observation dataset."),
    fields=[
        Field("precipitation", "Precipitation (mm)", type="number", min=0, placeholder="e.g. 10.9"),
        Field("temp_max", "Max temperature (C)", type="number", placeholder="e.g. 10.6"),
        Field("temp_min", "Min temperature (C)", type="number", placeholder="e.g. 2.8"),
        Field("wind", "Wind speed (m/s)", type="number", min=0, placeholder="e.g. 4.5"),
    ],
    load=load,
    predict=predict,
)

bp = make_blueprint(PROJECT, __name__)
