from __future__ import annotations
import os

from src.application.experiment_service import ExperimentService
from src.infrastructure.graph_gateway import GraphSource
from src.infrastructure.persistence.stubs import InMemoryGraphRepository, InMemoryExperimentRepository


def run_smoke() -> None:
    graph_repo = InMemoryGraphRepository()
    exp_repo = InMemoryExperimentRepository()
    service = ExperimentService(graph_repo=graph_repo, experiment_repo=exp_repo) # inject into service

    # defining source
    data_path = "src/data/toy.edgelist"

    if not os.path.exists(data_path):
        print(f"WARNING: {data_path} does not exist, using memory fallback")
        source = GraphSource(kind="memory", value=None, name="mock-demo-graph")
    else:
        source = GraphSource(kind="file", value=data_path, name="toy-graph")

    # import
    graph_key = service.import_graph(source)
    print(f"graph imported successfully with key {graph_key}")

    # running the experiment
    report = service.run_experiment(graph_key, "identity_stub", ["diameter"])

    print("-" * 30)
    print("SMOKE TEST SUCCESS")
    print(f"target: {report.graph_name}")
    print(f"reduction: {report.nodes_before} -> {report.nodes_after} nodes")
    print(f"results: {report.metric_results}")
    print("-" * 30)