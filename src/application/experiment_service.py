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

class ExperimentService:
    def __init__(self, graph_repo: GraphRepository, gateway: Optional[GraphGateway] = None):
        self.graph_repo = graph_repo
        self.gateway = gateway or GraphGateway()

    def import_graph(self, source: GraphSource) -> str:
        """
        imports a graph into the service store and returns an internal handle
        """
        graph = self.gateway.load(source)
        key = graph.name

        if self.graph_repo.get(key) is not None:
            i = 2
            while self.graph_repo.get(f"{key}_{i}") is not None:
                i += 1
            key = f"{key}_{i}"
            graph = Graph.from_networkx(
                graph.to_networkx(copy=True),
                name=key,
                metadata=dict(graph.metadata)
            )
        self.graph_repo.save(graph)
        return key

    def get_graph(self, graph_key: str) -> Graph:
        graph = self.graph_repo.get(graph_key)
        if graph is None:
            available = ", ".join(self.graph_repo.list_names())
            raise KeyError(f"graph not found: {graph_key}, available graphs: [{available}]")
        return graph

    def list_graphs(self) -> list[str]:
        return self.graph_repo.list_names()

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
            rp = RunParams(params)
        else:
            rp = params

        out = sparsifier.run(g, rp)
        new_key = output_name or out.name

        # collision check
        if self.graph_repo.get(new_key) is not None:
            i = 2
            while self.graph_repo.get(f"{new_key}_{i}") is not None:
                i += 1
            new_key = f"{new_key}_{i}"
            out = Graph.from_networkx(
                out.to_networkx(copy=True),
                name=new_key,
                metadata=dict(out.metadata)
            )
        self.graph_repo.save(out)
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
        p = RunParams(params or {})

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

