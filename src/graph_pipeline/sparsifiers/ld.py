from .base import Sparsifier
from src.graph_pipeline.core import GraphWrapper
import math


class LocalDegreeSparsifier(Sparsifier):
    def name(self) -> str:
        return f"local_degree (alpha = {self._alpha})"

    def sparsify(self, graph: GraphWrapper, rho: float = None) -> GraphWrapper:
        assert 0 <= rho <= 1
        G = graph.G

        # if G is directed, then edges := out_edges, degree := out_degree
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
                kept_edges.add((u, w, data))

        final_edges = list(kept_edges)
        return GraphWrapper(G.nodes(data=True), final_edges, directed=G.is_directed())
