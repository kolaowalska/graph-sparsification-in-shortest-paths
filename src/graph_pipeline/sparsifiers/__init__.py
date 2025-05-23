from .random import RandomSparsifier
from .kols import KOLSSparsifier
from .k_neighbor import KNeighborSparsifier
from .mst import MSTSparsifier
from .ld import LocalDegreeSparsifier
from .t_spanner import TSpannerSparsifier


seed = 39

sparsifiers_registry = {
    "kols": KOLSSparsifier(k=5, seed=seed).sparsify,
    "random": RandomSparsifier(seed=seed).sparsify,
    "k_neighbor": KNeighborSparsifier(seed=seed).sparsify,
    "local_degree": LocalDegreeSparsifier().sparsify,
    "mst": MSTSparsifier().sparsify,
    "t_spanner": TSpannerSparsifier(t=2.0).sparsify,
}
