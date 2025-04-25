from .base import Sparsifier
from graphs.graph import Graph
from graphs.utils import symmetrize_graph
import random
import networkx as nx


class KNeighborSparsifier(Sparsifier):
    def __init__(self, k: int, seed: int = None):
        assert k >= 1
        self._k = k
        self._seed = seed

    def name(self) -> str:
        return f"k_neighbor (k = {self._k})"

    def sparsify(self, graph: Graph) -> Graph:
        G = graph.G
        if G.is_directed():
            G = symmetrize_graph(G, weight_attr='weight', mode='avg')
        H = Graph(directed=G.is_directed(),
                  weighted='weight' in nx.get_edge_attributes(G, 'weight'))
        H.G.add_nodes_from(G.nodes(data=True))

        if self._seed is not None:
            random.seed(self._seed)

        # if G is directed, then edges := out_edges
        for v in G.nodes():
            edges = list(G.edges(v, data=True))
            if len(edges) <= self._k:
                for u, w, data in edges:
                    H.G.add_edge(u, w, **data)
            else:
                weights = [data.get('weight', 1) for _, _, data in edges]
                total_weight = sum(weights)
                probs = [w / total_weight for w in weights]

                selected = random.choices(edges, weights=probs, k=self._k)
                seen = set()
                for u, w, data in selected:
                    if (u, w) not in seen:
                        H.G.add_edge(u, w, **data)
                        seen.add((u, w))
                    if len(seen) >= self._k:
                        break

        return H

