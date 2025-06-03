from .base import Sparsifier
from utils.core import GraphWrapper
from collections import defaultdict, deque
import random
import math


class KOLSSparsifier(Sparsifier):
    def __init__(self, k: int = 3, rho: float = 0.5, seed: int = None):
        assert 0 < rho <= 1
        self._k = k
        self._rho = rho
        self._seed = seed

    def name(self) -> str:
        return f"kols (k={self._k}, rho={self._rho})"

    def sparsify(self, graph: GraphWrapper, rho: float = None) -> GraphWrapper:
        G = graph.G
        n = G.number_of_nodes()
        m = G.number_of_edges()

        if self._seed is not None:
            random.seed(self._seed)

        rho = self._rho if rho is None else rho
        assert 0 < rho <= 1
        keep_count = max(n - 1, int(math.floor(rho * m)))

        nodes = list(G.nodes())
        if len(nodes) < self._k:
            raise ValueError(f"graph has only {len(nodes)} nodes but k = {self._k} BFS runs were requested")
        start_vertices = random.sample(nodes, self._k)

        first_seed = start_vertices[0]
        visited = {first_seed}
        queue = deque([first_seed])
        T0 = set()
        while queue:
            u = queue.popleft()
            neighbors = G.successors(u) if G.is_directed() else G.neighbors(u)
            for v in neighbors:
                if v not in visited:
                    visited.add(v)
                    e0 = (u, v) if G.is_directed() else tuple(sorted((u, v)))
                    T0.add(e0)
                    queue.append(v)

        edge_freq = defaultdict(int)
        for seed in start_vertices:
            visited = {seed}
            queue = deque([seed])
            while queue:
                u = queue.popleft()
                neighbors = G.successors(u) if G.is_directed() else G.neighbors(u)
                for v in neighbors:
                    if v not in visited:
                        visited.add(v)
                        e = (u, v) if G.is_directed() else tuple(sorted((u, v)))
                        edge_freq[e] += 1
                        queue.append(v)

        other_edges = []
        if G.is_directed():
            for u, v in G.edges():
                if (u, v) not in T0:
                    other_edges.append((u, v))
        else:
            for u, v in G.edges():
                euv = tuple(sorted((u, v)))
                if euv not in T0:
                    other_edges.append((u, v))

        def freq_score(uv):
            key = uv if G.is_directed() else tuple(sorted(uv))
            return edge_freq.get(key, 0)

        other_edges.sort(key=freq_score, reverse=True)

        final_edges = list(T0)
        needed = keep_count - len(final_edges)
        if needed > 0:
            final_edges.extend(other_edges[:needed])

        H_edges = []
        for uv in final_edges:
            u, v = uv
            orig_w = G[u][v].get("weight", 1)
            H_edges.append((u, v, {"weight": orig_w}))

        return GraphWrapper(G.nodes(data=True), H_edges, directed=G.is_directed())
