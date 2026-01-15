from __future__ import annotations
import networkx as nx
import random

from src.domain.transforms.base import GraphTransform
from src.domain.transforms.registry import register_transform
from src.domain.graph_model import Graph, RunParams


@register_transform("simplify_parallel_edges")
class SimplifyParallelEdges(GraphTransform):
    def run(self, graph: Graph, params: RunParams) -> Graph:
        # TODO
        raise NotImplementedError("implement simplify_parallel_edges first")