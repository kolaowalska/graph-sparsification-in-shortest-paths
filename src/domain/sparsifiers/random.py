from __future__ import annotations

import random

from src.domain.graph_model import Graph, RunParams
from src.domain.sparsifiers.base import Sparsifier, SparsifierInfo
from src.domain.sparsifiers.registry import register_sparsifier


@register_sparsifier("random")
class RandomSparsifier(Sparsifier):
    INFO = SparsifierInfo(
        name="random",
        version="0.1.0",
        deterministic=False
    )

    def validate_params(self, params: RunParams) -> None:
        p = params.get("p", None)
        if p is None:
            raise ValueError("random sparsifier requires param 'p'")
        p = float(p)
        if not (0.0 <= p <= 1.0):
            raise ValueError("param 'p' must be in [0, 1]")

    def sparsify(self, graph: Graph, params: RunParams, *, rng: random.Random) -> Graph:
        p = float(params.get("p"))
        G = graph.to_networkx(copy=True)

        H = G.__class__()
        H.add_nodes_from(G.nodes(data=True))

        for u, v, data in G.edges(data=True):
            if rng.random() <= p:
                H.add_edge(u, v, **data)

        return Graph.from_networkx(H, name=f"{graph.name}_rand{p}")
