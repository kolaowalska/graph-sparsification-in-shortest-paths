from __future__ import annotations

import networkx as nx

from application.experiment_service import ExperimentService
from infrastructure.graph_gateway import GraphSource


def run_smoke() -> None:
    svc = ExperimentService()

    gkey = svc.import_graph(GraphSource(kind="memory", value=nx.path_graph(8), name="smoke_path8"))
    print("graphs:", svc.list_graphs())

    out_key = svc.run_sparsifier(gkey, "random", {"p": 0.7, "seed": 123})
    print("graphs:", svc.list_graphs())

    results = svc.compute_metrics(out_key, ["diameter"])
    print("SMOKE OK")
    for r in results:
        print(r.metric, r.summary)

