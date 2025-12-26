from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Mapping, Optional
import random

from ..graph_model import Graph, RunParams, OperationDescriptor
from ..sparsifiers.base import ParamSpec


@dataclass(frozen=True)
class TransformInfo:
    """
    metadata for a GraphTransform plugin
    similar to SparsifierInfo, but for generic graph-to-graph operations hopefully in the future
    """
    name: str
    version: str = "1.0.0"
    supports_directed: bool = True
    supports_weighted: bool = True
    deterministic: bool = False
    param_schema: Mapping[str, ParamSpec] = field(default_factory=dict)

    def descriptor(self) -> OperationDescriptor:
        return OperationDescriptor(kind="transform", name=self.name, version=self.version)


class GraphTransform(ABC):
    """
    separated interface for generic graph transformations
    (simplification, coarsening, filtering, contraction, normalization, etc.)
    """

    INFO: TransformInfo = TransformInfo(name="abstract_transform")

    def info(self) -> TransformInfo:
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
        rp = params if isinstance(params, RunParams) else RunParams(dict(params))
        rp = self.normalize_params(rp)

        self.validate_params(rp, graph=graph)

        if rng is None:
            seed = rp.get("seed", None)
            rng = random.Random(seed) if seed is not None else random.Random()

        out = self.apply(graph, rp, rng=rng)

        return out

    @abstractmethod
    def apply(self, graph: Graph, params: RunParams, *, rng: random.Random) -> Graph:
        """return a new graph transformed from input"""
        raise NotImplementedError


    def normalize_params(self, params: RunParams) -> RunParams:
        # TODO
        return params

    def validate_params(self, params: RunParams, *, graph: Graph) -> None:

        schema = self.info().param_schema
        if schema:
            for k, spec in schema.items():
                if spec.required and k not in params.values:
                    raise ValueError(f"Missing required parameter '{k}'")
                if k in params.values:
                    v = params.values[k]
                    if spec.type == "int" and not isinstance(v, int):
                        raise TypeError(f"parameter '{k}' must be int, got {type(v).__name__}")
                    if spec.type == "float" and not isinstance(v, (int, float)):
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

        # capability checks based on input graph properties
        if graph.is_directed() and not self.info().supports_directed:
            raise ValueError(f"{self.info().name} does not support directed graphs")
        if graph.is_weighted() and not self.info().supports_weighted:
            raise ValueError(f"{self.info().name} does not support weighted graphs")
