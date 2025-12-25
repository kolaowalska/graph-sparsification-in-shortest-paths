from __future__ import annotations

import random
import networkx as nx

from .base import Sparsifier, SparsifierInfo, ParamSpec
from .registry import register_sparsifier
from ..graph_model import Graph, RunParams


@register_sparsifier("random")
class RandomSparsifier(Sparsifier):
    INFO = SparsifierInfo(
        name="random",
        version="1.0.0",
        deterministic=False,
        param_schema={
            "p": ParamSpec(type="float", required=True, min=0.0, max=1.0, description="Keep each edge with prob p"),
            "seed": ParamSpec(type="int", required=False, description="random seed"),
        },
    )

    def sparsify(self, graph: Graph, params: RunParams, *, rng: random.Random) -> Graph:
        G = graph.to_networkx(copy=True)
        p = float(params.get("p"))
        H = G.__class__()
        H.add_nodes_from(G.nodes(data=True))
        for u, v, data in G.edges(data=True):
            if rng.random() <= p:
                H.add_edge(u, v, **data)
        return Graph.from_networkx(H, name=f"{graph.name}_rand{p}")
