import math
import networkx as nx
from .base import Sparsifier
from utils.symmetrizer import symmetrize_graph
from utils.core import GraphWrapper


class TSpannerSparsifier(Sparsifier):
    def __init__(self, t: float = 2.0):
        assert t >= 1.0
        self._t = t

    def name(self) -> str:
        return f"t-spanner (t={self._t})"

    def sparsify(self, graph: GraphWrapper, rho: float = None) -> GraphWrapper:
        G = graph.G
        directed = G.is_directed()

        G = symmetrize_graph(G) if directed else G
        H = nx.DiGraph() if directed else nx.Graph()
        H.add_nodes_from(G.nodes(data=True))

        edges = sorted(
            G.edges(data=True),
            key=lambda e: e[2].get('weight', 1.0)
        )

        for u, v, data in edges:
            w = data.get('weight', 1.0)
            try:
                d = nx.shortest_path_length(H, u, v, weight='weight')
            except (nx.NetworkXNoPath, nx.NodeNotFound):
                d = math.inf  # ??? moze wypadaloby to ladniej obsluzyc

            if d > self._t * w:
                if directed:
                    if G.has_edge(u, v):
                        H.add_edge(u, v, **G[u][v])
                    if G.has_edge(v, u):
                        H.add_edge(v, u, **G[v][u])
                else:
                    H.add_edge(u, v, **data)

        return GraphWrapper(G.nodes(data=True), H.edges(data=True), directed=directed)

