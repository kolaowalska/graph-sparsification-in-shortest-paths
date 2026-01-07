# from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, MutableMapping, Optional, Dict, Iterable, Tuple, NewType
import uuid
import networkx as nx

# ============ VALUE OBJECTS ============

GraphID = NewType('GraphID', str)
RunID = NewType('RunID', str)
ArtifactHandle = NewType('ArtifactHandle', str)

def new_graph_id() -> GraphID:
    return GraphID(str(uuid.uuid4()))

def new_run_id() -> RunID:
    return RunID(str(uuid.uuid4()))

@dataclass(frozen=True)
class RunParams:
    """immutable collection of parameters used by any runnable operation"""
    values: Mapping[str, Any] = field(default_factory=dict)

    def get(self, key:str, default: Any = None) -> Any:
        return self.values.get(key, default)

    def with_overrides(self, **overrides: Any) -> "RunParams":
        merged = dict(self.values)
        merged.update(overrides)
        return RunParams(merged)

@dataclass(frozen=True)
class MetricResult:
    """results returned by Metric.compute()"""
    summary: Mapping[str, float | int | str] = field(default_factory=dict)
    artifacts: Mapping[str, ArtifactHandle] = field(default_factory=dict)

@dataclass(frozen=True)
class OperationDescriptor:
    """which algorithm produced an output (algorithm name & version)"""
    kind: str
    name: str
    version: str = "1.0.0"


# DOMAIN MODEL

class Graph:
    __slots__ = (
        "_nx", "id", "name", "directed", "weighted", "source", "metadata"
    )

    def __init__(
        self,
        nx_graph: nx.Graph | nx.DiGraph,
        *,
        id: Optional[GraphID] = None,
        name: Optional[str] = None,
        source: Optional[str] = None,
        metadata: Optional[MutableMapping[str, Any]] = None,
        weight_attr: str = "weight",
    ) -> None:
        self._nx = nx_graph
        self.id: GraphID = id or new_graph_id()
        self.name: str = name or f"graph-{self.id}"
        self.directed: bool = nx_graph.is_directed()
        self.weighted: bool = any("weight" in d for _, _, d in nx_graph.edges(data=True) or weight_attr != "weight")
        self.source: Optional[str] = source
        self.metadata: Dict[str, Any] = dict(metadata or {})

    @property
    def node_count(self) -> int:
        return self._nx.number_of_nodes()

    @property
    def edge_count(self) -> int:
        return self._nx.number_of_edges()

    def is_directed(self) -> bool:
        return self.directed

    def is_weighted(self) -> bool:
        return self.weighted

    # ============ metadata ============

    def meta(self) -> Mapping[str, Any]:
        return self.metadata

    # def with_meta(self, **pairs: Any) -> "Graph":

    def to_networkx(self, copy: bool = False) -> nx.Graph | nx.DiGraph:
        """use with caution; prefer Graph methods in domain code and set copy=True for mutations"""
        return self._nx.copy() if copy else self._nx

    def copy(self, with_nodes_attrs: bool = True, with_edge_attrs: bool = True) -> "Graph":
        nx_copy = self._nx.__class__()
        nx_copy.add_nodes_from(
            self._nx.nodes(data=True) if with_nodes_attrs else self._nx.nodes()
        )
        nx_copy.add_edges_from(
            self._nx.edges(data=True) if with_edge_attrs else self._nx.edges()
        )
        return Graph(
            nx_copy,
            id=new_graph_id(),
            name=self.name + "_copy",
            source=self.source,
            metadata=self.metadata.copy(),
        )

    def nodes(self) -> Iterable[Any]:
        return self._nx.nodes()

    def edges(self, data: bool = False) -> Iterable[Tuple[Any, Any] | Tuple[Any, Any, Mapping[str, Any]]]:
        return self._nx.edges(data) if data else self._nx.edges() # ??

    def degree(self, v: Any) -> float:
        return self._nx.degree[v]

    def edge_weight(self, u: Any, v: Any, default: float = 1.0, weight_attr: str = "weight") -> float:
        data = self._nx.get_edge_data(u, v, default=None)
        if not data:
            raise KeyError(f"edge ({u}, {v}) not found :(")
        if isinstance(data, dict):
            return float(data.get(weight_attr, default))
        return float(min(d.get(weight_attr, default) for d in data.values()))

    @staticmethod
    def from_networkx(g: nx.Graph | nx.DiGraph, *, name: Optional[str] = None, source: Optional[str] = None,
                      metadata: Optional[Mapping[str, Any]] = None) -> "Graph":
        return Graph(g, name=name, source=source, metadata=dict(metadata or {}))

    def __repr__(self) -> str:
        kind = "DiGraph" if self.directed else "Graph"
        return f"<graph {self.id} {kind} n={self.node_count} m={self.edge_count} name={self.name!r}>"
        


