from __future__ import annotations

import networkx as nx

from src.domain.graph_model import Graph, RunParams
from src.domain.metrics.base import Metric, MetricInfo, MetricResult
from src.domain.metrics.registry import register_metric

# TODO: decide whether diameter should be inf or the diameter of the largest connected component
@register_metric("avg_path_length")
class AvgPathLength(Metric):
    INFO = MetricInfo(
        name="average path length",
        description="average shortest path length on largest connected component",
    )

    def compute(self, graph: Graph, params: RunParams) -> MetricResult:
        G = graph.to_networkx(copy=False)
        weight_arg = "weight" if graph.is_weighted() else None

        UG = G.to_undirected() if G.is_directed() else G

        if UG.number_of_nodes() <= 1:
            val = 0.0
        else:
            if nx.is_connected(UG):
                subgraph = UG
            else:
                largest_cc = max(nx.connected_components(UG), key=len)
                subgraph = UG.subgraph(largest_cc)

            try:
                val = nx.average_shortest_path_length(subgraph, weight=weight_arg)
            except Exception:
                val = -1.0

        return MetricResult(
            metric=self.INFO.name,
            summary={"avg": float(val), "weighted": bool(weight_arg)}
        )
