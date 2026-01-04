from __future__ import annotations

import networkx as nx

from application.experiment_service import ExperimentService
from infrastructure.graph_gateway import GraphSource
from src.infrastructure.persistence.stubs import InMemoryGraphRepository


def run_smoke() -> None:
    repo = InMemoryGraphRepository()
    service = ExperimentService(graph_repo=repo)

    source = GraphSource(kind="memory", value=None, name="mock-demo-graph")
    service.import_graph(source)

    report = service.run_experiment("mock-demo-graph", "identity_stub", ["diameter"])

    print(f"nodes: {report.nodes_before} -> {report.nodes_after}")
    print(f"mock data: {report.metadata['path_redundancy_score']}")