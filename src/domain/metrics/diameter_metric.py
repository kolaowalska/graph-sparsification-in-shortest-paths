from __future__ import annotations

import networkx as nx

from src.domain.graph_model import Graph, RunParams
from src.domain.metrics.base import Metric, MetricInfo, MetricResult
from src.domain.metrics.registry import register_metric

# TODO: decide whether diameter should be inf or the diameter of the largest connected component
@register_metric("diameter")
class DiameterMetric(Metric):
    INFO = MetricInfo(
        name="diameter",
        version="0.1.0",
        description="diameter; if disconnected uses largest connected component."
    )

    def _compute(self, graph: Graph, params: RunParams) -> MetricResult:
        G = graph.to_networkx(copy=False)
        UG = G.to_undirected() if isinstance(G, nx.DiGraph) else G

        if UG.number_of_nodes() == 0:
            return MetricResult(metric=self.INFO.name, summary={"diameter": 0})

        if nx.is_connected(UG):
            d = nx.diameter(UG)
        else:
            largest = max(nx.connected_components(UG), key=len)
            H = UG.subgraph(largest).copy()
            d = nx.diameter(H)

        return MetricResult(metric=self.INFO.name, summary={"diameter": d})
