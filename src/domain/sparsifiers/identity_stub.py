from abc import ABC

from .base import Sparsifier
from .registry import register_sparsifier
from ..graph_model import Graph, RunParams


@register_sparsifier("identity_stub")
class IdentitySparsifier(Sparsifier, ABC):
    """
    placeholder to satisfy the domain's sparsifier interface and allow testing
    """
    def run(self, graph: Graph, params: RunParams) -> Graph:
        return Graph.from_networkx(
            graph.to_networkx(copy=True),
            name=f"{graph.name}_identity",
            metadata=graph.metadata
        )

