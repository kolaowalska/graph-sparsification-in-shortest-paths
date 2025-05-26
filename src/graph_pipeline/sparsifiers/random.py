from .base import Sparsifier
from utils.core import GraphWrapper
import random


class RandomSparsifier(Sparsifier):
    def __init__(self, rho: float = 0.5, seed: int = None):
        self._rho = rho
        self._seed = seed

    def name(self): return f"random (p = {self._rho})"

    def sparsify(self, graph: GraphWrapper, rho: float = None) -> GraphWrapper:
        assert 0 <= rho <= 1
        G = graph.G
        final_edges = []

        if self._seed is not None:
            random.seed(self._seed)

        p = 1 - rho if rho is not None else self._rho

        for u, v, data in G.edges(data=True):
            if random.random() < p:
                final_edges.append((u, v, data))

        return GraphWrapper(G.nodes(data=True), final_edges, directed=G.is_directed())
