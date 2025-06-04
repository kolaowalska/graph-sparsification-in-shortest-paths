from .base import Sparsifier
from utils.core import GraphWrapper
import math


class LocalDegreeSparsifier(Sparsifier):
    def name(self) -> str:
        return f"local_degree"

    def sparsify(self, graph: GraphWrapper, rho: float = None) -> GraphWrapper:
        assert 0 <= rho <= 1
        G = graph.G
        kept_edges = set()

        for v in G.nodes():
            edges = list(G.edges(v, data=True))
            d_out = len(edges)
            if d_out == 0:
                continue

            k = max(1, math.floor(d_out ** rho))
            ranked = sorted(edges,
                            key=lambda e: G.degree(e[1]),
                            reverse=True)
            top_k = ranked[:k]

            for u, w, data in top_k:
                kept_edges.add((u, w, data.get('weight', 1)))

        final_edges = list(kept_edges)
        return GraphWrapper(G.nodes(data=True), final_edges, directed=G.is_directed())
