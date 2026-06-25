# Sentiment-analysis project plugin.
import json
from pathlib import Path

from core.spec import Field, ModelInfo, ProjectSpec
from core.views import make_blueprint

from .predictor import load, predict

_METRICS = Path(__file__).resolve().parent / "model" / "metrics.json"


def _accuracy(default: str = "88%") -> str:
    try:
        return json.loads(_METRICS.read_text()).get("accuracy", default)
    except Exception:
        return default


PROJECT = ProjectSpec(
    id="sentiment_analysis",
    name="Sentiment Analysis",
    icon="bi-chat-heart",
    color="#8b5cf6",
    category="NLP",
    short_description="Detect positive, negative or neutral tone in text.",
    description="Classifies free text (such as a product review or comment) as Positive, Negative or Neutral using a TF-IDF and Naive Bayes model trained on tens of thousands of real reviews.",
    accuracy=_accuracy(),
    kind="tabular",
    model_info=ModelInfo(
        algorithm="TF-IDF + Multinomial Naive Bayes",
        features=["Review / comment text"],
        accuracy=_accuracy(),
        dataset="Amazon product-review corpus."),
    fields=[
        Field("text", "Text to analyse", type="textarea",
              placeholder="e.g. This product exceeded my expectations!",
              help_text="Paste any sentence, review or comment."),
    ],
    load=load,
    predict=predict,
)

bp = make_blueprint(PROJECT, __name__)
