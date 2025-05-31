from .base import Sparsifier
from utils.core import GraphWrapper
from collections import defaultdict, deque
import networkx as nx
import numpy as np
import random


class KOLSSparsifier(Sparsifier):
    def __init__(self,
                 k: int = 3,
                 rho: float = 0.5,
                 rescale: bool = True,
                 seed: int = None):
        assert 0 < rho <= 1
        self._k = k
        self._rho = rho
        self._rescale = rescale
        self._seed = seed

    def name(self) -> str:
        return (f"kols (k = {self._k}, "
                f"rho = {self._rho}")

    def sparsify(self, graph: GraphWrapper, rho: float = None) -> GraphWrapper:
        assert 0 <= rho <= 1
        G = graph.G

        if self._seed is not None:
            random.seed(self._seed)

        edge_freq = defaultdict(int)
        nodes = list(G.nodes)

        if len(nodes) < self._k:
            raise ValueError(f"graph has only {len(nodes)} nodes but k={self._k} BFS runs requested")

        start_vertices = random.sample(nodes, self._k)

        for start in start_vertices:
            visited = set([start])
            queue = deque([start])

            while queue:
                u = queue.popleft()
                for v in G.neighbors(u):
                    if v not in visited:
                        visited.add(v)
                        edge = tuple(sorted((u, v)))
                        edge_freq[edge] += 1
                        queue.append(v)

        if not edge_freq:
            return GraphWrapper(G.nodes(data=True), G.edges(data=True), directed=G.is_directed())

        total_frequencies = sum(edge_freq.values())
        frequencies = {e: f / total_frequencies for e, f in edge_freq.items()}

        freq_values = list(frequencies.values())
        tau = np.percentile(freq_values, 40)
        tau = max(tau, 1e-6)

        scores = {e: min(1.0, frequencies[e] / tau) for e in frequencies}

        rho = rho if rho is not None else self._rho
        keep_count = max(1, int(rho * G.number_of_edges()))
        top = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:keep_count]

        final_edges = []
        for (u, v), _ in top:
            og_weight = G[u][v].get('weight', 1)
            f = edge_freq[(u, v)] if G.is_directed() else edge_freq[tuple(sorted((u, v)))]
            new_weight = round(og_weight * f / self._k) if self._rescale else og_weight
            final_edges.append((u, v, {'weight': new_weight}))

        H_wrapper = GraphWrapper(G.nodes(data=True), final_edges, directed=G.is_directed())

        # nowa atrakcja (ktora nie dziala):
        # zapewnienie spojnosci poprzez odbudowanie mostow dla grafow nieskierowanych
        if not G.is_directed() and not nx.is_connected(H_wrapper.G):
            for u, v in nx.bridges(G):
                if not H_wrapper.G.has_edge(u, v):
                    H_wrapper.G.add_edge(u, v, weight=G[u][v].get('weight', 1))

        return H_wrapper
