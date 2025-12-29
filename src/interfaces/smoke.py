from __future__ import annotations

import networkx as nx

from application.experiment_service import ExperimentService
from infrastructure.graph_gateway import GraphSource


def run_smoke() -> None:
    service = ExperimentService()

    # gkey = svc.import_graph(GraphSource(kind="memory", value=nx.path_graph(8), name="smoke_path8"))
    # print("graphs:", svc.list_graphs())
    #
    # out_key = svc.run_sparsifier(gkey, "random", {"p": 0.7, "seed": 123})
    # print("graphs:", svc.list_graphs())
    #
    # results = svc.compute_metrics(out_key, ["diameter"])
    # print("SMOKE OK")
    # for r in results:
    #     print(r.metric, r.summary)

    source = GraphSource(kind="memory", value=None, name="mock-demo-graph")
    service.import_graph(source)

    report = service.run_experiment("mock-demo-graph", "identity_stub", ["diameter"])

    print(f"nodes: {report.nodes_before} -> {report.nodes_after}")
    print(f"mock data: {report.metadata['path_redundancy_score']}")