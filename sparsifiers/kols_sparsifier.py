from .base import Sparsifier
from graphs.graph import Graph
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

    def sparsify(self, graph: Graph) -> Graph:
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

                if G.is_directed():
                    neighbors = list(G.successors(current))
                else:
                    neighbors = list(G.neighbors(current))

                for nb in neighbors:
                    if G.is_directed():
                        edge_freq[(current, nb)] += 1
                    else:
                        edge_freq[(min(current, nb), max(current, nb))] += 1

                    if nb not in visited:
                        queue.append(nb)

        total_frequencies = sum(edge_freq.values())
        if total_frequencies == 0:
            return Graph.from_nx(G)  # nic si eni estalo :((((((((((((((((

        frequencies = {e: f / total_frequencies for e, f in edge_freq.items()}
        median = sorted(frequencies.values())[len(frequencies) // 2]
        tau = median

        # computing retention scores (min(1, freq / τ))
        scores = {e: min(1.0, frequencies[e] / tau) for e in frequencies}

        # sorting edges by score descending and keeping top rho-fraction
        keep_count = max(1, int(self._rho * G.number_of_edges()))
        top = sorted(scores.items(),
                     key=lambda x: x[1],
                     reverse=True)[:keep_count]

        H = Graph(directed=G.is_directed(),
                  weighted='weight' in nx.get_edge_attributes(G, 'weight'))
        H.G.add_nodes_from(G.nodes(data=True))

        for (u, v), _ in top:
            og_weight = G[u][v].get('weight', 1)
            f = edge_freq[(u, v)]
            new_weight = round(og_weight * f / self._k) if self._rescale else og_weight
            H.G.add_edge(u, v, weight=new_weight)

        # nowa atrakcja (ktora nie dziala):
        # zapewnienie spojnosci poprzez odbudowanie mostow dla grafow nieskierowanych
        if not G.is_directed():
            if not nx.is_connected(H.G):
                components = list(nx.connected_components(H.G))
                for component in components:
                    for u, v in nx.bridges(G):
                        c_u = next(c for c in components if u in c)
                        c_v = next(c for c in components if v in c)
                        if c_u != c_v:
                            H.G.add_edge(u, v, weight=G[u][v].get('weight', 1))

        return H
