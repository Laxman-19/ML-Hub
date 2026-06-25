# Reusable helpers shared across the hub and its projects.
import logging
import os
import uuid
from typing import Any

from werkzeug.datastructures import FileStorage

from core.spec import Field

logger = logging.getLogger(__name__)


# Configure root logging once, with a concise format.
def configure_logging(level: str = "INFO") -> None:
    logging.basicConfig(level=getattr(logging, level.upper(), logging.INFO),
                        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")


def allowed_image(filename: str, allowed: set[str]) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed


# Validate and persist an uploaded image, returning its absolute path.
# The stored filename is randomised to avoid collisions and path tricks.
def save_upload(file: FileStorage, upload_folder: str, allowed: set[str]) -> str:
    if not file or not file.filename:
        raise ValueError("No file was uploaded.")
    if not allowed_image(file.filename, allowed):
        raise ValueError(f"Unsupported file type. Allowed: {', '.join(sorted(allowed))}.")
    ext = file.filename.rsplit(".", 1)[1].lower()
    os.makedirs(upload_folder, exist_ok=True)
    dest = os.path.join(upload_folder, f"{uuid.uuid4().hex}.{ext}")
    file.save(dest)
    logger.info("Saved upload to %s", dest)
    return dest


# Raised when submitted form values fail validation.
class ValidationError(ValueError):
    pass


# Coerce and validate a single submitted form value.
def coerce_field(field: Field, raw: Any) -> Any:
    if raw is None or (isinstance(raw, str) and raw.strip() == ""):
        if field.required and field.default is None:
            raise ValidationError(f"'{field.label}' is required.")
        return field.default

    if field.type == "number":
        try:
            value = float(raw)
        except (TypeError, ValueError):
            raise ValidationError(f"'{field.label}' must be a number.")
        if field.min is not None and value < field.min:
            raise ValidationError(f"'{field.label}' must be >= {field.min}.")
        if field.max is not None and value > field.max:
            raise ValidationError(f"'{field.label}' must be <= {field.max}.")
        return int(value) if field.step in ("1", 1) else value

    if field.type == "select":
        for _, v in field.options or []:
            if str(v) == str(raw):
                return v
        raise ValidationError(f"Invalid choice for '{field.label}'.")

    # text / textarea
    text = str(raw).strip()
    if field.required and not text:
        raise ValidationError(f"'{field.label}' is required.")
    return text
