from .base import Sparsifier
from graphs.graph import Graph
import math
import networkx as nx


class LocalDegreeSparsifier(Sparsifier):
    def __init__(self, alpha: float = 0.5):
        assert 0 <= alpha <= 1
        self._alpha = alpha

    def name(self) -> str:
        return f"local_degree (alpha = {self._alpha})"

    def sparsify(self, graph: Graph) -> Graph:
        G = graph.G
        H = Graph(directed=G.is_directed(),
                  weighted='weight' in nx.get_edge_attributes(G, 'weight'))
        H.G.add_nodes_from(G.nodes(data=True))

        # if G is directed, then edges := out_edges, degree := out_degree
        for v in G.nodes():
            edges = list(G.edges(v, data=True))
            d_out = len(edges)
            if d_out == 0:
                continue
            k = max(1, math.floor(d_out ** self._alpha))
            ranked = sorted(edges,
                            key=lambda e: G.degree(e[1]),
                            reverse=True)

            for u, w, data in ranked[:k]:
                H.G.add_edge(u, w, **data)

        return H

