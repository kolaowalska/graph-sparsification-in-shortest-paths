from __future__ import annotations

from typing import Callable, Dict, Type

from .base import GraphTransform
from src.domain.common.plugin_discovery import discover_modules

_TRANSFORMS: Dict[str, Type[GraphTransform]] = {}
_DISCOVERED = False


class TransformRegistry:
    @staticmethod
    def register(name: str) -> Callable[[Type[GraphTransform]], Type[GraphTransform]]:
        if not isinstance(name, str) or not name.strip():
            raise ValueError("transform name must be a non-empty string!!")
        key = name.strip()

        def _decorator(cls: Type[GraphTransform]) -> Type[GraphTransform]:
            if key in _TRANSFORMS and _TRANSFORMS[key] is not cls:
                raise ValueError(f"transform '{key}' already registered by {_TRANSFORMS[key].__name__}")
            _TRANSFORMS[key] = cls
            return cls

        return _decorator

    @staticmethod
    def discover() -> None:
        global _DISCOVERED
        if _DISCOVERED:
            return
        discover_modules("srcdomain.transforms")
        _DISCOVERED = True

    @staticmethod
    def ensure_discovered() -> None:
        if not _DISCOVERED:
            TransformRegistry.discover()

    @staticmethod
    def get(name: str) -> GraphTransform:
        TransformRegistry.ensure_discovered()
        key = name.strip()
        try:
            cls = _TRANSFORMS[key]
        except KeyError as e:
            available = ", ".join(sorted(_TRANSFORMS.keys()))
            raise KeyError(f"unknown transform '{key}'. available: [{available}]") from e
        return cls()

    @staticmethod
    def list() -> list[str]:
        TransformRegistry.ensure_discovered()
        return sorted(_TRANSFORMS.keys())


register_transform = TransformRegistry.register
