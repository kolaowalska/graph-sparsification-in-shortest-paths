from .base import Sparsifier
from utils.core import GraphWrapper
from collections import defaultdict, deque
import networkx as nx
import numpy as np
import random
import math


class KOLSSparsifier(Sparsifier):
    def __init__(self, k: int = 5, rho: float = 0.5, rescale: bool = True, seed: int = None):
        assert 0 < rho <= 1
        self._k = k
        self._rho = rho
        self._rescale = rescale
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
            raise ValueError(f"graph has only {len(nodes)} nodes but k = {self._k} bfs runs were requested")
        start_vertices = random.sample(nodes, self._k)

        first_seed = start_vertices[0]
        visited = {first_seed}
        queue = deque([first_seed])
        T0 = set()  # this stores either (u,v) for directed or sorted((u,v)) for undirected

        while queue:
            u = queue.popleft()
            for v in (G.successors(u) if G.is_directed() else G.neighbors(u)):
                if v not in visited:
                    visited.add(v)

                    # if G is directed, using exactly (u,v); if undirected, sorted ((u, v))
                    if G.is_directed():
                        e0 = (u, v)
                    else:
                        e0 = tuple(sorted((u, v)))
                    T0.add(e0)

                    queue.append(v)

        # running bfs k times to count how many times each edge is used as a tree‐edge
        edge_freq = defaultdict(int)
        for seed in start_vertices:
            visited = {seed}
            queue = deque([seed])

            while queue:
                u = queue.popleft()
                for v in (G.successors(u) if G.is_directed() else G.neighbors(u)):
                    if v not in visited:
                        visited.add(v)

                        # if G is directed, using exactly (u,v); if undirected, sorted ((u, v))
                        if G.is_directed():
                            e = (u, v)
                        else:
                            e = tuple(sorted((u, v)))

                        edge_freq[e] += 1
                        queue.append(v)

        scores = {e: edge_freq[e] / float(self._k) for e in edge_freq}

        other_edges = []
        if G.is_directed():
            for (u, v) in G.edges():
                if (u, v) not in T0:
                    other_edges.append((u, v))
        else:
            for (u, v) in G.edges():
                e_und = tuple(sorted((u, v)))
                if e_und not in T0:
                    other_edges.append((u, v))

        def get_edge_score(uv):
            if G.is_directed():
                return scores.get(uv, 0.0)
            else:
                e_undirected = tuple(sorted(uv))
                return scores.get(e_undirected, 0.0)

        other_edges_sorted = sorted(other_edges,
                                    key=lambda uv: get_edge_score(uv),
                                    reverse=True)

        final_edges = list(T0)
        needed = keep_count - len(final_edges)
        if needed > 0:
            needed = min(needed, len(other_edges_sorted))
            final_edges.extend(other_edges_sorted[:needed])

        H_edges = []
        for uv in final_edges:
            if G.is_directed():
                (u, v) = uv
            else:
                (u, v) = uv
            orig_w = G[u][v].get('weight', 1)

            if self._rescale:
                if G.is_directed():
                    f = edge_freq.get((u, v), 0)
                else:
                    f = edge_freq.get(tuple(sorted((u, v))), 0)
                new_w = round(orig_w * (f / float(self._k)))
            else:
                new_w = orig_w

            H_edges.append((u, v, {"weight": new_w}))

        H_wrapper = GraphWrapper(G.nodes(data=True), H_edges, directed=G.is_directed())
        return H_wrapper
