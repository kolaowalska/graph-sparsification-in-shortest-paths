from __future__ import annotations

from src.domain.graph_model import Graph, RunParams
from src.domain.sparsifiers.base import Sparsifier
from src.domain.sparsifiers.registry import register_sparsifier


@register_sparsifier("mst")
class MSTSparsifier(Sparsifier):
    def run(self, graph: Graph, params: RunParams) -> Graph:
        # TODO
        raise NotImplementedError("implement mst sparsifier first")