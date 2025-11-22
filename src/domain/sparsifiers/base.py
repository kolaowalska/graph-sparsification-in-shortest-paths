from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Mapping, Optional, Dict
import random

from ..graph_model import Graph, RunParams, OperationDescriptor


@dataclass(frozen=True)
class ParamSpec:
    """lightweight specifications for validating params"""
    type: str
    required: bool
    default: Any = None
    description: str = ""
    min: float | None = None
    max: float | None = None
    choices: tuple[Any, ...] | None = None


@dataclass(frozen=True)
class SparsifierInfo:
    name: str
    version: str = "1.0.0"
    supports_directed: bool = True
    supports_weighted: bool = True
    deterministic: bool = False
    param_schema: Mapping[str, ParamSpec] = field(default_factory=dict)

    def descriptor(self) -> OperationDescriptor:
        return OperationDescriptor(kind="sparsify", name=self.name, version=self.version)


class Sparsifier(ABC):
    """separated interface for sparsification algorithms"""
    INFO: SparsifierInfo = SparsifierInfo(name="abstract")

    def info(self) -> SparsifierInfo:
        return self.INFO

    def descriptor(self) -> OperationDescriptor:
        return self.info().descriptor()

    def run(
            self,
            graph: Graph,
            params: Mapping[str, Any] | RunParams = RunParams(),
            *,
            rng: Optional[random.Random] = None,
    ) -> Graph:
        """template method: validate params -> do work -> return new Graph object"""
        rp = params if isinstance(params, RunParams) else RunParams(dict(params))
        self.validate_params(rp)

        if rng is None:
            seed = rp.get("seed", None)
            rng = random.Random(seed) if seed is not None else random.Random()

        out = self.sparsify(graph, rp, rng=rng)

        if out is graph:
            pass
        return out

    @abstractmethod
    def sparsify(self, graph: Graph, params: RunParams, *, rng: random.Random) -> Graph:
        raise NotImplementedError


    def validate_params(self, params: RunParams) -> None:
        schema = self.info().param_schema
        if not schema:
            return

        for k, spec in schema.items():
            if spec.required and k not in params.values:
                raise ValueError(f"missing required parameter '{k}'")
            if k not in params.values and spec.default is not None:
                # ??
                continue

            if k in params.values:
                v = params.values[k]
                if spec.type == "int" and not isinstance(v, int):
                    raise TypeError(f"parameter '{k}' must be int, got {type(v).__name__}")
                if spec.type == "float" and not isinstance(v, (int,float)):
                    raise TypeError(f"parameter '{k}' must be float, got {type(v).__name__}")
                if spec.type == "bool" and not isinstance(v, bool):
                    raise TypeError(f"parameter '{k}' must be bool, got {type(v).__name__}")
                if spec.type == "str" and not isinstance(v, str):
                    raise TypeError(f"parameter '{k}' must be str, got {type(v).__name__}")

                if spec.min is not None and isinstance(v, (int, float)) and v < spec.min:
                    raise ValueError(f"parameter '{k}' must be ≥ {spec.min}, got {v}")
                if spec.max is not None and isinstance(v, (int, float)) and v > spec.max:
                    raise ValueError(f"parameter '{k}' must be ≤ {spec.max}, got {v}")
                if spec.choices is not None and v not in spec.choices:
                    raise ValueError(f"parameter '{k}' must be one of {spec.choices}, got {v}")