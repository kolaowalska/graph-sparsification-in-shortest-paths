from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Union

import networkx as nx

from domain.graph_model import Graph

@dataclass(frozen=True)
class GraphSource:
    kind: str
    value: object
    fmt: Optional[str] = None
    name: Optional[str] = None


# GATEWAY PATTERN

class GraphGateway:
    def load(self, source: any) -> Graph:
        print(f"[gatway stub] loading mock graph from source: {source}")
        nx_g = nx.erdos_renyi_graph(n=10, p=0.3)
        return Graph(nx_g, name="mock-demo-graph")


#
# class GraphGateway:
#     def load(self, source: GraphSource) -> Graph:
#         if source.kind == "memory":
#             if not isinstance(source.value, (nx.Graph, nx.DiGraph, nx.MultiGraph, nx.MultiDiGraph)):
#                 raise TypeError("GraphSource(kind='memory') expects a NetworkX graph as value")
#             name = source.name or "memory_graph"
#             return Graph.from_networkx(source.value, name=name, metadata={"source_kind": "memory"})
#
#         if source.kind == "file":
#             path = Path(str(source.value))
#             if not path.exists():
#                 raise FileNotFoundError(str(path))
#
#             fmt = (source.fmt or self._infer_format(path)).lower()
#             nx_graph = self._load_from_file(path, fmt)
#             name = source.name or path.stem
#             return Graph.from_networkx(
#                 nx_graph,
#                 name=name,
#                 metadata={"source_kind": "file", "path": str(path), "fmt": fmt},
#             )
#
#         raise ValueError(f"unknown GraphSource.kind={source.kind!r}")
#
#     def _infer_format(self, path: Path) -> str:
#         ext = path.suffix.lower().lstrip(".")
#         if ext in ("txt", "edges", "edgelist"):
#             return "edgelist"
#         if ext in ("graphml", "xml"):
#             return "graphml"
#         if ext in ("gexf",):
#             return "gexf"
#         if ext in ("gpickle", "pickle", "pkl"):
#             return "gpickle"
#         if ext in ("adjlist",):
#             return "adjlist"
#         return ext
#
#     def _load_from_file(self, path: Path, fmt: str) -> nx.Graph:
#         if fmt == "edgelist": # default: space-separated u v [weight]
#             return nx.read_edgelist(path, data=(("weight", float),), create_using=nx.Graph())
#         if fmt == "adjlist":
#             return nx.read_adjlist(path, create_using=nx.Graph())
#         if fmt == "graphml":
#             return nx.read_graphml(path)
#         if fmt == "gexf":
#             return nx.read_gexf(path)
#         if fmt == "gpickle":
#             return nx.read_gpickle(path)
#
#         raise ValueError(
#             f"unsupported graph format {fmt!r} for path={path}. "
#             f"supported: edgelist, adjlist, graphml, gexf, gpickle"
#         )
