from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

from domain.graph_model import Graph, RunParams
from domain.sparsifiers.registry import SparsifierRegistry
from domain.metrics.registry import MetricRegistry
from domain.metrics.base import MetricResult
from infrastructure.graph_gateway import GraphGateway, GraphSource


# SERVICE LAYER

@dataclass
class ExperimentService:
    gateway: GraphGateway = field(default_factory=GraphGateway)

    _graphs: dict[str, Graph] = field(default_factory=dict)

    def import_graph(self, source: GraphSource) -> str:
        """
        imports a graph into the service store and returns an internal handle
        """
        graph = self.gateway.load(source)

        key = graph.name
        if key in self._graphs:
            i = 2
            while f"{key}_{i}" in self._graphs:
                i += 1
            key = f"{key}_{i}"
            graph = Graph.from_networkx(graph.to_networkx(copy=True), name=key, metadata=dict(graph.metadata))

        self._graphs[key] = graph
        return key

    def get_graph(self, graph_key: str) -> Graph:
        try:
            return self._graphs[graph_key]
        except KeyError as e:
            available = ", ".join(sorted(self._graphs.keys()))
            raise KeyError(f"unknown graph '{graph_key}'. available: [{available}]") from e

    def list_graphs(self) -> list[str]:
        return sorted(self._graphs.keys())

    def run_sparsifier(
        self,
        graph_key: str,
        sparsifier_name: str,
        params: dict[str, Any] | RunParams,
        *,
        output_name: Optional[str] = None,
    ) -> str:
        """
        applies a sparsifier to a stored graph, stores output graph, and returns new graph key
        """
        SparsifierRegistry.discover()

        g = self.get_graph(graph_key)
        sparsifier = SparsifierRegistry.get(sparsifier_name)

        rp: RunParams
        if isinstance(params, dict):
            rp = params
        else:
            rp = params

        out = sparsifier.run(g, rp)

        new_key = output_name or out.name
        if new_key in self._graphs:
            i = 2
            while f"{new_key}_{i}" in self._graphs:
                i += 1
            new_key = f"{new_key}_{i}"
            out = Graph.from_networkx(out.to_networkx(copy=True), name=new_key, metadata=dict(out.metadata))

        self._graphs[new_key] = out
        return new_key

    def compute_metrics(
        self,
        graph_key: str,
        metric_names: list[str],
        params: Optional[dict[str, Any]] = None,
    ) -> list[MetricResult]:
        """
        computes a list of metrics on a stored graph
        """
        MetricRegistry.discover()

        g = self.get_graph(graph_key)
        p = params or {}

        results: list[MetricResult] = []
        for name in metric_names:
            metric = MetricRegistry.get(name)
            results.append(metric.compute(g, p))
        return results
