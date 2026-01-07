from __future__ import annotations
import networkx as nx

from src.application.experiment_service import ExperimentService
from src.infrastructure.graph_gateway import GraphSource
from src.infrastructure.persistence.stubs import InMemoryGraphRepository


def test_dummy_pipeline_logic():
    # setup
    repo = InMemoryGraphRepository()
    svc = ExperimentService(graph_repo=repo)

    # creating input
    nx_g = nx.path_graph(8)
    gkey = svc.import_graph(GraphSource(kind="memory", value=nx_g, name="t_path8"))

    # executing action (eg. running a sparsifier)
    out_key = svc.run_sparsifier(gkey, "identity_stub", {})

    g_in = svc.get_graph(gkey)
    g_out = svc.get_graph(out_key)

    # assertions/validations
    assert g_out.edge_count <= g_in.edge_count

    # checking metrics
    results = svc.compute_metrics(out_key, ["diameter"])
    assert len(results) == 1
    assert results[0].metric == "diameter"
