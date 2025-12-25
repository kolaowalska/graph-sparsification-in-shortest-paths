from __future__ import annotations

import importlib
import pkgutil
from types import ModuleType


def discover_modules(package_name: str) -> list[ModuleType]:
    pkg = importlib.import_module(package_name)

    if not hasattr(pkg, "__path__"):
        return [pkg]

    imported: list[ModuleType] = []
    for m in pkgutil.iter_modules(pkg.__path__, pkg.__name__ + "."):
        imported.append(importlib.import_module(m.name))
    return imported
