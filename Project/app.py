# ML Hub - Flask application factory.
# Hosts multiple ML projects behind one app using a plugin architecture:
# every folder in projects/ that exposes PROJECT + bp is discovered and wired
# up automatically, so adding a project never touches this file.
import logging
import os
from datetime import datetime
from pathlib import Path

from flask import Flask, render_template, send_from_directory

from core.registry import registry
from core.utils import configure_logging

logger = logging.getLogger(__name__)
BASE_DIR = Path(__file__).resolve().parent


# Build and configure the Flask app.
def create_app() -> Flask:
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.update(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev-only-change-me"),
        UPLOAD_FOLDER=os.environ.get("UPLOAD_FOLDER", str(BASE_DIR / "uploads")),
        MAX_CONTENT_LENGTH=int(os.environ.get("MAX_CONTENT_LENGTH", 8 * 1024 * 1024)),
        ALLOWED_IMAGE_EXTENSIONS={"jpg", "jpeg", "png"},
    )
    configure_logging(os.environ.get("LOG_LEVEL", "INFO"))
    Path(app.config["UPLOAD_FOLDER"]).mkdir(parents=True, exist_ok=True)

    # Discover and register every project plugin.
    registry.discover("projects")
    for spec in registry.all():
        app.register_blueprint(spec.blueprint)
    logger.info("Registered %d ML projects", len(registry))

    _register_routes(app)
    _register_globals(app)
    _register_errors(app)
    return app


def _register_routes(app: Flask) -> None:
    @app.route("/")
    def home():
        return render_template("home.html", projects=registry.all(), categories=registry.categories())

    # Serve user-uploaded images so they can be shown on result pages.
    @app.route("/uploads/<path:filename>")
    def uploaded_file(filename: str):
        return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

    @app.route("/model-summary")
    def model_summary():
        return render_template("model_summary.html", projects=registry.all(), stats=_collect_stats())

    @app.route("/health")
    def health():
        return {"status": "ok", "projects": len(registry)}, 200


def _register_globals(app: Flask) -> None:
    @app.context_processor
    def inject_globals():
        return {"registry": registry, "current_year": datetime.utcnow().year, "app_name": "ML Hub"}


def _register_errors(app: Flask) -> None:
    @app.errorhandler(404)
    def not_found(_):
        return render_template("errors/404.html"), 404

    @app.errorhandler(413)
    def too_large(_):
        return render_template("errors/generic.html", code=413, message="The uploaded file is too large."), 413

    @app.errorhandler(500)
    def server_error(_):
        return render_template("errors/500.html"), 500


# Gather model-inventory facts from the filesystem for the Model Summary page.
def _collect_stats() -> dict:
    projects_info, total_size, total_files = [], 0, 0
    for spec in registry.all():
        model_dir = BASE_DIR / "projects" / spec.id / "model"
        files, last_trained = [], None
        for f in sorted(model_dir.glob("*")):
            if f.suffix in {".pkl", ".h5", ".joblib"}:
                size = f.stat().st_size
                total_size += size
                total_files += 1
                mtime = datetime.fromtimestamp(f.stat().st_mtime)
                last_trained = max(last_trained, mtime) if last_trained else mtime
                files.append({"name": f.name, "size": _human_size(size)})
        projects_info.append({
            "spec": spec, "files": files, "healthy": bool(files),
            "last_trained": last_trained.strftime("%Y-%m-%d %H:%M") if last_trained else "-",
        })
    return {
        "num_projects": len(registry), "num_models": total_files,
        "total_model_size": _human_size(total_size),
        "categories": registry.categories(), "projects": projects_info,
    }


def _human_size(num: int) -> str:
    size = float(num)
    for unit in ("B", "KB", "MB", "GB"):
        if size < 1024 or unit == "GB":
            return f"{size:.0f} {unit}" if unit == "B" else f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} GB"


# Module-level app for gunicorn (app:app).
app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
