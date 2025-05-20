from .base import Sparsifier
from src.graph_pipeline.core import GraphWrapper
from unused.graphs.utils import symmetrize_graph
import random
import math


class KNeighborSparsifier(Sparsifier):
    def __init__(self, seed: int = None):
        self._seed = seed

    def name(self) -> str:
        return f"k_neighbor (rho-dependent)"

    def sparsify(self, graph: GraphWrapper, rho: float = None) -> GraphWrapper:
        assert 0 <= rho <= 1
        G = graph.G

        if G.is_directed():
            G = symmetrize_graph(G, weight_attr='weight', mode='avg')

        if self._seed is not None:
            random.seed(self._seed)

        # if G is directed, then edges := out_edges
        kept_edges = set()
        for v in G.nodes():
            edges = list(G.edges(v, data=True))
            d_out = len(edges)

            if d_out == 0:
                continue

            k_v = max(1, math.floor(d_out ** rho))

            if d_out <= k_v:
                # kept_edges.update(edges)
                for edge in edges:
                    kept_edges.add((edge[0], edge[1], edge[2].get('weight', 1)))
            else:
                weights = [data.get('weight', 1) for _, _, data in edges]
                selected = random.choices(edges, weights=weights, k=k_v)
                # kept_edges.update(selected)
                for edge in selected:
                    kept_edges.add((edge[0], edge[1], edge[2].get('weight', 1)))

        final_edges = list(kept_edges)
        return GraphWrapper(G.nodes(data=True), final_edges, directed=G.is_directed())

