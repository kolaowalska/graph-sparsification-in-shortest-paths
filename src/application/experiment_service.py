from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

from src.domain.graph_model import Graph, RunParams
from src.domain.sparsifiers.registry import SparsifierRegistry
from src.domain.metrics.registry import MetricRegistry
from src.domain.metrics.base import MetricResult
from src.infrastructure.graph_gateway import GraphGateway, GraphSource
from src.infrastructure.persistence.repo import GraphRepository
from src.application.dto import ExperimentDTO


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

# SERVICE LAYER ORCHESTRATION

    def run_experiment(
        self,
        graph_key: str,
        sparsifier_name: str,
        metric_names: list[str],
    ) -> ExperimentDTO:
        """
        uses the DTO to return a complete snapshot of experiment results
        """

        G = self.get_graph(graph_key)
        n_pre, m_pre = G.node_count, G.edge_count

        key_new = self.run_sparsifier(graph_key, sparsifier_name, {})
        H = self.get_graph(key_new)

        metric_results = self.compute_metrics(key_new, metric_names)

        return ExperimentDTO(
            graph_name=graph_key,
            nodes_before=n_pre,
            edges_before=m_pre,
            nodes_after=H.node_count,
            edges_after=H.edge_count,
            sparsifier_name=sparsifier_name,
            metric_results=metric_results,
            metadata={
                "path_redundancy_score": 0.0, "is_coarsened": False
            }
        )

