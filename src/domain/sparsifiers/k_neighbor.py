from .base import Sparsifier, SparsifierInfo, ParamSpec
from ..graph_model import Graph, RunParams
import random
import networkx as nx

class KNeighborSparsifier(Sparsifier):
    INFO = SparsifierInfo(
        name="k_neighbor",
        version="1.0.0",
        supports_directed=False,
        supports_weighted=True,
        deterministic=True,
        param_schema={
            "k": ParamSpec(type="int", required=True, min=1, description="keeps at most k neighbors per node"),
            "weight_attr": ParamSpec(type="str", required=False, default="weight"),
            "break_ties": ParamSpec(type="str", required=False, default="random",
                                    choices=("random", "min_id", "max_id")),
            "seed": ParamSpec(type="int", required=False, description="random seed for tie-breaking"),
        },
    )

    #TODO: verify seed

    def sparsify(self, graph: Graph, params: RunParams, *, rng: random.Random) -> Graph:
        G = graph.to_networkx(copy=True)
        if G.is_directed():
            raise ValueError("k_neighbor sparsifier expects an undirected graph")

        k = int(params.get("k", 1))
        w = params.get("weight_attr", "weight")
        tie = params.get("break_ties", "random")

        H = nx.Graph()
        H.add_nodes_from(G.nodes(data=True))

        for u in G.nodes():
            neighbors = []
            for v in G.neighbors(u):
                data = G.get_edge_data(u, v, default={})
                weight = data.get(w, 1.0)
                neighbors.append((v, weight))

            # if there's a tie between neighbors to keep, a custom strategy is chosen
            if tie == "random":
                rng.shuffle(neighbors)
            elif tie == "min_id":
                neighbors.sort(key=lambda x: x[0])
            elif tie == "max_id":
                neighbors.sort(key=lambda x: x[0], reverse=True)

            neighbors.sort(key=lambda x: x[1], reverse=True)
            for v, weight in neighbors[:k]:
                if not H.has_edge(u, v):
                    H.add_edge(u, v, **{w: weight})

        return Graph.from_networkx(H, name=f"{graph.name}_k{k}")
