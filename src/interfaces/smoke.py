from __future__ import annotations

import networkx as nx

from ..domain.graph_model import Graph
from ..domain.sparsifiers.registry import SparsifierRegistry
from ..domain.metrics.registry import MetricRegistry


def run_smoke() -> None:
    SparsifierRegistry.discover()
    MetricRegistry.discover()

    g = Graph.from_networkx(nx.path_graph(8), name="smoke_path8")

    s = SparsifierRegistry.get("random")
    out = s.run(g, {"p": 0.7, "seed": 123})

    m = MetricRegistry.get("diameter")
    res = m.compute(out, {})

    print("SMOKE OK")
    print("in :", g)
    print("out:", out)
    print("metric summary:", dict(res.summary))
