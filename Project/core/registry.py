# Project registry - the heart of the plugin architecture.
# On startup it imports every sub-package of projects/ that exposes a
# module-level PROJECT (ProjectSpec) and bp (Blueprint), and registers it.
# Adding a new ML project means dropping in a folder - no edits to the hub.
import importlib
import logging
import pkgutil
from typing import Iterator

from core.spec import ProjectSpec

logger = logging.getLogger(__name__)

# Homepage display order (projects not listed fall to the end).
_PREFERRED_ORDER = [
    "fracture_analysis", "stroke_prediction", "potato_leaf_disease",
    "sentiment_analysis", "motor_maintenance", "weather_forecast",
]


# Holds all discovered ProjectSpec objects.
class ProjectRegistry:
    def __init__(self) -> None:
        self._projects: dict[str, ProjectSpec] = {}

    # Import every project sub-package and register valid specs.
    def discover(self, package_name: str = "projects") -> None:
        package = importlib.import_module(package_name)
        for _, mod_name, is_pkg in pkgutil.iter_modules(package.__path__):
            if not is_pkg:
                continue
            full_name = f"{package_name}.{mod_name}"
            try:
                module = importlib.import_module(full_name)
            except Exception:
                logger.exception("Failed to import project package %s", full_name)
                continue
            spec = getattr(module, "PROJECT", None)
            bp = getattr(module, "bp", None)
            if not isinstance(spec, ProjectSpec) or bp is None:
                continue
            spec.blueprint = bp
            self._projects[spec.id] = spec
            logger.info("Registered project: %s (%s)", spec.id, spec.name)

    def get(self, project_id: str) -> ProjectSpec | None:
        return self._projects.get(project_id)

    # All projects in the preferred display order.
    def all(self) -> list[ProjectSpec]:
        def key(spec: ProjectSpec) -> tuple[int, str]:
            order = _PREFERRED_ORDER.index(spec.id) if spec.id in _PREFERRED_ORDER else len(_PREFERRED_ORDER)
            return (order, spec.id)
        return sorted(self._projects.values(), key=key)

    def categories(self) -> list[str]:
        return sorted({p.category for p in self._projects.values()})

    def __iter__(self) -> Iterator[ProjectSpec]:
        return iter(self.all())

    def __len__(self) -> int:
        return len(self._projects)


# Singleton used across the app.
registry = ProjectRegistry()
