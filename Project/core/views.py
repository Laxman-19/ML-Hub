# Generic, reusable view logic for project blueprints.
# Every project calls make_blueprint() to get a working GET/POST prediction
# page. Tabular and image projects share the same flow; the only difference
# is whether a field has type "file".
import logging
import os
from typing import Any

from flask import Blueprint, current_app, flash, render_template, request, url_for

from core.spec import ProjectSpec
from core.utils import ValidationError, coerce_field, save_upload

logger = logging.getLogger(__name__)


# Load the project's model once and cache it on the spec.
def _model_for(spec: ProjectSpec):
    if spec._model is None:
        spec._model = spec.load()
    return spec._model


# Attach the standard index (form + prediction) route to bp.
def register_routes(bp: Blueprint, spec: ProjectSpec) -> None:
    # Use a project-specific template if present, else the shared one.
    template = [f"{spec.id}/predict.html", "project_predict.html"]

    @bp.route("/", methods=["GET", "POST"])
    def index():
        result, uploaded_image_url, form_values = None, None, {}
        if request.method == "POST":
            try:
                inputs: dict[str, Any] = {}
                for field in spec.fields:
                    if field.type == "file":
                        path = save_upload(request.files.get(field.name),
                                           current_app.config["UPLOAD_FOLDER"],
                                           current_app.config["ALLOWED_IMAGE_EXTENSIONS"])
                        inputs[field.name] = path
                        uploaded_image_url = url_for("uploaded_file", filename=os.path.basename(path))
                    else:
                        raw = request.form.get(field.name)
                        form_values[field.name] = raw
                        inputs[field.name] = coerce_field(field, raw)
                result = spec.predict(_model_for(spec), inputs)
                logger.info("[%s] prediction: %s", spec.id, result.label)
            except ValidationError as exc:
                flash(str(exc), "warning")
            except Exception as exc:
                logger.exception("Prediction failed for %s", spec.id)
                flash(f"Prediction failed: {exc}", "danger")
        return render_template(template, project=spec, result=result,
                               form_values=form_values, uploaded_image_url=uploaded_image_url)


# Create a project blueprint with templates served from the package.
def make_blueprint(spec: ProjectSpec, import_name: str) -> Blueprint:
    bp = Blueprint(spec.id, import_name, template_folder="templates", url_prefix=f"/project/{spec.id}")
    register_routes(bp, spec)
    return bp
