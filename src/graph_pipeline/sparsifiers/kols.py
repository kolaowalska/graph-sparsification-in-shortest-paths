from .base import Sparsifier
from src.graph_pipeline.utils.core import GraphWrapper
import random
from collections import defaultdict
import networkx as nx
# TODO: add user-defined tau


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

        for _ in range(self._k):
            start = random.choice(nodes)
            visited, queue = set(), [start]

            while queue:
                current = queue.pop(0)
                if current in visited:
                    continue
                visited.add(current)

                neighbors = list(G.successors(current) if G.is_directed() else G.neighbors(current))

                for nb in neighbors:
                    edge = (current, nb) if G.is_directed() else tuple(sorted([current, nb]))
                    edge_freq[edge] += 1

                    if nb not in visited:
                        queue.append(nb)

        total_frequencies = sum(edge_freq.values())
        if total_frequencies == 0:
            return GraphWrapper(G.nodes(data=True), G.edges(data=True), directed=G.is_directed())  # nic si eni estalo :((((((((((((((((

        frequencies = {e: f / total_frequencies for e, f in edge_freq.items()}
        median = sorted(frequencies.values())[len(frequencies) // 2]
        tau = median

        # computing retention scores (min(1, freq / τ))
        scores = {e: min(1.0, frequencies[e] / tau) for e in frequencies}

        # sorting edges by score descending and keeping top rho-fraction
        rho = rho if rho is not None else self._rho
        keep_count = max(1, int(rho * G.number_of_edges()))
        top = sorted(scores.items(),
                     key=lambda x: x[1],
                     reverse=True)[:keep_count]

        final_edges = []
        for (u, v), _ in top:
            og_weight = G[u][v].get('weight', 1)
            f = edge_freq[(u, v)]
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
