from __future__ import annotations
import networkx as nx
import pytest

from src.application.experiment_service import ExperimentService
from src.infrastructure.graph_gateway import GraphSource
from src.infrastructure.persistence.stubs import InMemoryGraphRepository, InMemoryExperimentRepository


def test_pipeline():

    graph_repo = InMemoryGraphRepository()
    exp_repo = InMemoryExperimentRepository()
    svc = ExperimentService(graph_repo, exp_repo)

    nx_g = nx.path_graph(10)

    gkey = svc.import_graph(GraphSource(kind="memory", value=nx_g, name="test_graph"))

    dto = svc.run_experiment(gkey, "identity_stub", ["diameter"])

    # assert "execution_time" in dto.metadata
    # assert dto.metadata["algorithm"] == "IdentitySparsifier"
    # print(f"Transform took {dto.metadata['execution_time']}s")
    #
    # saved_graphs = graph_repo.list_names()
    #
    # assert len(saved_graphs) >= 1
    # assert any("identity" in name for name in saved_graphs)
    #
    # assert len(exp_repo._storage) == 1