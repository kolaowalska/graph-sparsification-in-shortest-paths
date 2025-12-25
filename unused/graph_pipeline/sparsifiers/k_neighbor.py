import math
import numpy as np
from .base import Sparsifier
from utils.core import GraphWrapper
from utils.symmetrizer import symmetrize_graph



class KNeighborSparsifier(Sparsifier):
    def __init__(self, seed: int = None):
        self._seed = seed

    def name(self) -> str:
        return f"k_neighbor"

    def sparsify(self, graph: GraphWrapper, rho: float = None) -> GraphWrapper:
        assert 0 <= rho <= 1
        G = graph.G

        if G.is_directed():
            G = symmetrize_graph(G, weight_attr='weight', mode='sum')

        kept_edges = set()

        for v in G.nodes():
            edges = list(G.edges(v, data=True))
            d_out = len(edges)

            if d_out == 0:
                continue

            k_v = max(1, math.floor(d_out ** rho))

            if d_out <= k_v:
                for u, w, data in edges:
                    weight = data.get('weight', 1)
                    kept_edges.add((u, w, weight))
            else:
                weights = [data.get('weight', 1) for _, _, data in edges]
                total_weight = sum(weights)
                probs = [w / total_weight for w in weights]

                sampled_indices = np.random.choice(d_out, size=k_v, replace=False, p=probs)

                for idx in sampled_indices:
                    u, w, data = edges[idx]
                    weight = data.get('weight', 1)
                    kept_edges.add((u, w, weight))

        final_edges = list(kept_edges)
        return GraphWrapper(G.nodes(data=True), final_edges, directed=G.is_directed())


