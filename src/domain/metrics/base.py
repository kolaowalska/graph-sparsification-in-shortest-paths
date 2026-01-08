from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Mapping

from src.domain.graph_model import Graph, RunParams, ArtifactHandle


@dataclass(frozen=True)
class MetricInfo:
    name: str
    version: str = "0.1.0"
    description: str = ""

@dataclass(frozen=True)
class MetricResult:
    """results returned by Metric.compute()"""
    metric: str
    summary: Mapping[str, float | int | str] = field(default_factory=dict)
    artifacts: Mapping[str, ArtifactHandle] = field(default_factory=dict)


class Metric(ABC):
    INFO: MetricInfo

    def compute(self, graph: Graph, params: RunParams) -> MetricResult:
        # self.validate_params(params)
        # return self._compute(graph, params)
        pass

    # def validate_params(self, params: RunParams) -> None:
    #     return
    #
    # @abstractmethod
    # def _compute(self, graph: Graph, params: RunParams) -> MetricResult:
    #     raise NotImplementedError
