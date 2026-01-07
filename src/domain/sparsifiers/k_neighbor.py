from __future__ import annotations

import random
import networkx as nx

from src.domain.graph_model import Graph, RunParams
from src.domain.sparsifiers.base import Sparsifier, SparsifierInfo
from src.domain.sparsifiers.registry import register_sparsifier


@register_sparsifier("k_neighbor")
class KNeighborSparsifier(Sparsifier):
    INFO = SparsifierInfo(
        name="k_neighbor",
        version="0.1.0",
        deterministic=True
    )

    def validate_params(self, params: RunParams) -> None:
        if "k" not in params:
            raise ValueError("k_neighbor sparsifier requires param 'k'")
        k = int(params["k"])
        if k < 1:
            raise ValueError("param 'k' must be >= 1")

    def sparsify(self, graph: Graph, params: RunParams, *, rng: random.Random) -> Graph:
        k = int(params["k"])
        weight_attr = params.get("weight_attr", "weight")

        G = graph.to_networkx(copy=True)
        UG = G.to_undirected() if isinstance(G, nx.DiGraph) else G

        H = nx.Graph()
        H.add_nodes_from(UG.nodes(data=True))

        for u in UG.nodes():
            candidates = []
            for v in UG.neighbors(u):
                data = UG.get_edge_data(u, v, default={})
                w = float(data.get(weight_attr, 1.0))
                candidates.append((v, w, data))

            # sort by weight descending
            # TODO: deterministic tie-break by chosen strategy instead of node id repr?
            candidates.sort(key=lambda t: (t[1], repr(t[0])), reverse=True)

            for v, w, data in candidates[:k]:
                if not H.has_edge(u, v):
                    H.add_edge(u, v, **data)

        return Graph.from_networkx(H, name=f"{graph.name}_k{k}")
