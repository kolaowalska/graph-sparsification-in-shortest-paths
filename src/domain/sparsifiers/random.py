from .base import Sparsifier, SparsifierInfo, ParamSpec
from ..graph_model import Graph, RunParams
import random
import networkx as nx

class RandomSparsifier(Sparsifier):
    INFO = SparsifierInfo(
        name="random",
        version="1.0.0",
        supports_directed=True,
        supports_weighted=True,
        deterministic=False,
        param_schema={
            "p" : ParamSpec(type="float", required=True, min=0.0, max=1.0, description="edge-keeping probability"),
            "seed": ParamSpec(type="int", required=False, description="random seed")
        }
    )

# TODO: utilize seed

def sparsify(self, graph: Graph, params: RunParams, *, rng: random.Random) -> Graph:
    G = graph.to_networkx(copy=True)
    p = params.get("p", 0.5)

    seed = params.get("seed")
    H = nx.Graph()
    H.add_nodes_from(G.nodes(data=True))
    random.seed = self.seed
    edges=[]

    for u, v, data in G.edges(data=True):
        if random.random() < self.p:
            edges.append((u, v, data))

    return Graph.from_networkx(H, name=f"{graph.name}_random{p}")

