# Core data structures every project plugin fills in.
# Field = one input on the form, PredictionResult = a predictor's output,
# ModelInfo = the model-details box, ProjectSpec = all metadata for a project.
from dataclasses import dataclass, field
from typing import Any, Callable, Optional


# One dynamic form input. type maps to the rendered control:
# number | text | textarea | select | file.
@dataclass
class Field:
    name: str
    label: str
    type: str = "number"
    options: Optional[list[tuple[str, Any]]] = None  # selects: (label, value)
    placeholder: str = ""
    help_text: str = ""
    required: bool = True
    step: str = "any"
    min: Optional[float] = None
    max: Optional[float] = None
    default: Any = None


# Normalised predictor output consumed by the templates.
@dataclass
class PredictionResult:
    label: str
    confidence: Optional[float] = None  # 0..1
    detail: str = ""
    extra: dict[str, Any] = field(default_factory=dict)

    @property
    def confidence_pct(self) -> Optional[float]:
        return None if self.confidence is None else round(self.confidence * 100, 2)


# Human-readable description of the model powering a project.
@dataclass
class ModelInfo:
    algorithm: str
    features: list[str]
    accuracy: str
    dataset: str
    notes: str = ""


# Everything the hub needs to know about one ML project.
@dataclass
class ProjectSpec:
    id: str          # url slug, e.g. "fracture_analysis"
    name: str
    icon: str        # bootstrap-icon name, e.g. "bi-bandaid"
    short_description: str
    description: str
    category: str
    accuracy: str    # display string, e.g. "92%"
    kind: str        # "tabular" | "image"
    model_info: ModelInfo
    fields: list[Field]
    load: Callable[[], Any]                      # load the model once
    predict: Callable[[Any, dict], "PredictionResult"]  # run inference (model, inputs)
    color: str = "#6366f1"
    blueprint: Any = None   # bound by the registry
    _model: Any = None      # cached model artifact

    # Blueprint endpoint name for the predict page.
    @property
    def endpoint(self) -> str:
        return f"{self.id}.index"
