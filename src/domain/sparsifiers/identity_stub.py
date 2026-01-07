import random
from .base import Sparsifier, SparsifierInfo
from .registry import register_sparsifier
from ..graph_model import Graph, RunParams


# SERVICE STUB & STRATEGY

@register_sparsifier("identity_stub")
class IdentitySparsifier(Sparsifier):
    """
    placeholder to satisfy the domain's sparsifier interface and allow testing
    """
    INFO = SparsifierInfo(name="identity_stub", deterministic=True)

    def sparsify(self, graph: Graph, params: RunParams, *, rng: random.Random) -> Graph:
        print(f"[strategy stub] identity sparsification on {graph.name}")
        return graph.copy()

