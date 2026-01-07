from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

from src.domain.graph_model import Graph, RunParams


@dataclass(frozen=True)
class MetricInfo:
    name: str
    version: str = "0.1.0"
    description: str = ""


@dataclass(frozen=True)
class MetricResult:
    metric: str
    summary: dict[str, Any] = field(default_factory=dict)


class Metric(ABC):
    INFO: MetricInfo

    def compute(self, graph: Graph, params: RunParams) -> MetricResult:
        self.validate_params(params)
        return self._compute(graph, params)

    def validate_params(self, params: RunParams) -> None:
        return

    @abstractmethod
    def _compute(self, graph: Graph, params: RunParams) -> MetricResult:
        raise NotImplementedError
