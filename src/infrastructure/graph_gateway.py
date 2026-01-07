from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional
import networkx as nx
from pathlib import Path

from src.domain.graph_model import Graph


@dataclass
class GraphSource:
    """
    DTO specifying where to find a graph
    """
    kind: str
    name: str
    value: Any = None
    fmt: Optional[str] = "edgelist"


class GraphGateway:
    """
    gateway to external graph data
    """

    def load(self, source: GraphSource) -> Graph:
        print(f"[gateway] loading graph '{source.name}' from {source.kind}...")

        nx_graph = None

        if source.kind == "file":
            path = Path(source.value)
            if not path.exists():
                raise FileNotFoundError(f"graph file not found: {path.absolute()}")

            if source.fmt == "edgelist":
                nx_graph = nx.read_edgelist(str(path), nodetype=int)
            else:
                raise ValueError(f"Unsupported format: {source.fmt}")

        elif source.kind == "memory":
            if source.value is None:
                # fallback for smoke tests if no graph is provided
                nx_graph = nx.cycle_graph(5)
            else:
                nx_graph = source.value

        else:
            raise ValueError(f"Unknown source kind: {source.kind}")

        # conversion to domain entity
        return Graph.from_networkx(nx_graph, name=source.name)