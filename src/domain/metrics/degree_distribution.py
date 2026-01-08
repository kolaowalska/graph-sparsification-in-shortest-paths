from __future__ import annotations

from src.domain.graph_model import Graph, RunParams
from src.domain.metrics.base import Metric, MetricInfo, MetricResult
from src.domain.metrics.registry import register_metric


@register_metric("degree_distribution")
class APSPMetric(Metric):
    INFO = MetricInfo(
        name="degree distribution",
        description="todo"
    )

    # TODO
    def compute(self, graph: Graph, params: RunParams) -> MetricResult:
        G = graph.to_networkx(copy=False)

        return MetricResult(
            metric=self.INFO.name,
            summary={
            }
        )
