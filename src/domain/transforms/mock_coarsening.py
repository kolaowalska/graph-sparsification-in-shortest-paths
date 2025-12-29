from .base import GraphTransform, TransformInfo
from .registry import register_transform
from ..graph_model import Graph, RunParams
import random


@register_transform("mock_coarsening")
class MockCoarsening(GraphTransform):
    """
    a placeholder the future implementation of graph coarsening
    """

    INFO = TransformInfo(name="mock_coarsening")

    def apply(self, graph: Graph, params: RunParams, *, rng: random.Random) -> Graph:
        print(f"--- [mock] performing graph coarsening on {graph.name} ---")
        return graph