from __future__ import annotations

import networkx as nx

from application.experiment_service import ExperimentService
from infrastructure.graph_gateway import GraphSource


def test_dummy_pipeline_random_and_diameter():
    svc = ExperimentService()

    nx_g = nx.path_graph(8)
    gkey = svc.import_graph(GraphSource(kind="memory", value=nx_g, name="t_path8"))

    out_key = svc.run_sparsifier(gkey, "random", {"p": 0.7, "seed": 123})

    # basic structural invariants
    g_in = svc.get_graph(gkey)
    g_out = svc.get_graph(out_key)

    assert g_in.node_count == 8
    assert g_out.node_count == 8
    assert 0 <= g_out.edge_count <= g_in.edge_count

    results = svc.compute_metrics(out_key, ["diameter"])
    assert len(results) == 1
    r = results[0]

    assert r.metric == "diameter"
    assert "diameter" in r.summary
    assert isinstance(r.summary["diameter"], int)
    assert r.summary["diameter"] >= 0
