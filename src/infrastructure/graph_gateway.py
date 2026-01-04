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

