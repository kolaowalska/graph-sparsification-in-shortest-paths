from .base import Sparsifier
from utils.core import GraphWrapper
from utils.symmetrizer import symmetrize_graph
from collections import defaultdict, deque
import networkx as nx
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

        if G.is_directed():
            symG = symmetrize_graph(G, weight_attr='weight', mode='sum')
            tree_undirected = nx.minimum_spanning_tree(symG, weight='weight')

            T0 = set()
            for u, v in tree_undirected.edges():
                if G.has_edge(u, v) and G.has_edge(v, u):
                    w_uv = G[u][v].get('weight', 1)
                    w_vu = G[v][u].get('weight', 1)
                    if w_uv <= w_vu:
                        T0.add((u, v))
                    else:
                        T0.add((v, u))
                elif G.has_edge(u, v):
                    T0.add((u, v))
                else:
                    T0.add((v, u))
        else:
            tree_undirected = nx.minimum_spanning_tree(G, weight='weight')
            T0 = set(tuple(sorted((u, v))) for u, v in tree_undirected.edges())

        edge_freq = defaultdict(int)
        nodes = list(G.nodes())
        if len(nodes) < self._k:
            raise ValueError(
                f"graph has only {len(nodes)} nodes but k = {self._k} BFS runs were requested"
            )
        start_vertices = random.sample(nodes, self._k)

        for seed in start_vertices:
            visited = set([seed])
            queue = deque([seed])
            while queue:
                u = queue.popleft()
                neighbors = G.successors(u) if G.is_directed() else G.neighbors(u)
                for v in neighbors:
                    e = (u, v) if G.is_directed() else tuple(sorted((u, v)))
                    edge_freq[e] += 1
                    if v not in visited:
                        visited.add(v)
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


