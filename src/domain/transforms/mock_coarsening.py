from __future__ import annotations
import networkx as nx
import random

from src.domain.transforms.base import GraphTransform
from src.domain.transforms.registry import register_transform
from src.domain.graph_model import Graph, RunParams


@register_transform("mock_coarsening")
class MockCoarsening(GraphTransform):
    def run(self, graph: Graph, params: RunParams) -> Graph:
        G = graph.to_networkx(copy=True)

        target_reduction = params.get("reduction_ratio", 0.5)
        seed = params.get("seed", 420)
        rng = random.Random(seed)

        target_nodes = int(G.number_of_nodes() * (1 - target_reduction))
        target_nodes = max(1, target_nodes)

        # mock random edge contraction
        while G.number_of_nodes() < target_nodes:
            if G.number_of_nodes() == 0:
                break

            edges = list(G.edges(data=True))
            u, v = rng.choice(edges)

            # stub contraction
            G = nx.contracted_nodes(G, u, v, self_loops=False, copy=False)

        return Graph.from_networkx(
            G,
            name=f"{graph.name}_coarsened",
            metadata={
                "operation": "mock_coarsening",
                "target_reduction": target_reduction,
            }
        )