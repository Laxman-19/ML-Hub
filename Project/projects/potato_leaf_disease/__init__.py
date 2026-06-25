# Potato-leaf Disease Detection project plugin (image classification).
import json
from pathlib import Path

from core.spec import Field, ModelInfo, ProjectSpec
from core.views import make_blueprint

from .predictor import load, predict

_METRICS = Path(__file__).resolve().parent / "model" / "metrics.json"


def _accuracy(default: str = "97%") -> str:
    try:
        return json.loads(_METRICS.read_text()).get("accuracy", default)
    except Exception:
        return default


PROJECT = ProjectSpec(
    id="potato_leaf_disease",
    name="Potato Leaf Disease Detection",
    icon="bi-flower1",
    color="#22c55e",
    category="Agriculture",
    short_description="Detect potato-leaf disease from an uploaded photo.",
    description="A convolutional neural network that classifies a potato-leaf image as Early Blight, Late Blight or Healthy. Upload a leaf photo to get the predicted disease class with a confidence score.",
    accuracy=_accuracy(),
    kind="image",
    model_info=ModelInfo(
        algorithm="Convolutional Neural Network (Keras / TensorFlow)",
        features=["RGB leaf image (256x256)"],
        accuracy=_accuracy(),
        dataset="PlantVillage potato-leaf image dataset (3 classes).",
        notes="Accepts JPG, JPEG and PNG images up to 8 MB."),
    fields=[
        Field("image", "Leaf image", type="file", required=True,
              help_text="Upload a clear photo of a single potato leaf (JPG, JPEG or PNG)."),
    ],
    load=load,
    predict=predict,
)

bp = make_blueprint(PROJECT, __name__)
