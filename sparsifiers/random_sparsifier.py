from .base import Sparsifier
from graphs.graph import Graph
import networkx as nx
import random


class RandomSparsifier(Sparsifier):
    def __init__(self, p: float = 0.5, seed: int = None):
        self._p = p
        self._seed = seed

    def name(self): return f"random (p = {self._p})"

    def sparsify(self, graph: Graph) -> Graph:
        G = graph.G

        H = Graph(directed=G.is_directed(),
                  weighted='weight' in nx.get_edge_attributes(G, 'weight'))

        H.G.add_nodes_from(G.nodes(data=True))

        if self._seed is not None:
            random.seed(self._seed)
        for u, v, data in G.edges(data=True):
            if random.random() < self._p:
                H.G.add_edge(u, v, **data)

        return H
