from .base import Sparsifier
from utils.core import GraphWrapper
from utils.symmetrizer import symmetrize_graph
import networkx as nx


class MSTSparsifier(Sparsifier):
    def name(self) -> str:
        return "mst"

    def sparsify(self, graph: GraphWrapper, rho: float = None) -> GraphWrapper:
        G = graph.G
        if G.is_directed():
            G = symmetrize_graph(G, weight_attr='weight', mode='avg')

        final_edges = [(u, v, data)
                       for u, v, data in nx.minimum_spanning_edges(G, data=True, weight='weight')]

        return GraphWrapper(G.nodes(data=True), final_edges, directed=False)
