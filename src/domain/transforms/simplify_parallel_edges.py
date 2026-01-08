# from __future__ import annotations
#
# import networkx as nx
# import random
#
# from .base import GraphTransform, TransformInfo
# from ..graph_model import Graph, RunParams
# from ..sparsifiers.base import ParamSpec
# from .registry import TransformRegistry
#
# # TODO: take care of this
#
# @TransformRegistry.register("simplify_parallel_edges")
# class SimplifyParallelEdges(GraphTransform):
#     INFO = TransformInfo(
#         name="simplify_parallel_edges",
#         version="1.0.0",
#         supports_directed=True,
#         supports_weighted=True,
#         deterministic=True,
#         param_schema={
#             "weight_attr": ParamSpec(type="str", required=False, default="weight"),
#             "merge": ParamSpec(type="str", required=False, default="min", choices=("min", "max", "sum", "avg")),
#         },
#     )
#
#     def apply(self, graph: Graph, params: RunParams, *, rng: random.Random) -> Graph:
#         G = graph.to_networkx(copy=True)
#         w = params.get("weight_attr", "weight")
#         merge = params.get("merge", "min")
#
#         if not isinstance(G, (nx.MultiGraph, nx.MultiDiGraph)):
#             return Graph.from_networkx(G, name=f"{graph.name}_simplified")
#
#         # multigraph to simple graph conversion (merging parallel edges)
#         H = nx.DiGraph() if G.is_directed() else nx.Graph()
#         H.add_nodes_from(G.nodes(data=True))
#
#         for u, v, data in G.edges(data=True):
#             weight = float(data.get(w, 1.0))
#             if H.has_edge(u, v):
#                 cur = float(H[u][v].get(w, 1.0))
#                 if merge == "min":
#                     new = min(cur, weight)
#                 elif merge == "max":
#                     new = max(cur, weight)
#                 elif merge == "sum":
#                     new = cur + weight
#                 else:  # avg
#                     new = (cur + weight) / 2.0
#                 H[u][v][w] = new
#             else:
#                 H.add_edge(u, v, **{w: weight})
#
#         return Graph.from_networkx(H, name=f"{graph.name}_simplified")
