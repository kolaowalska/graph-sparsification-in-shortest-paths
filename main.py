from graphs.generators import generate_random_graph
from graphs.graph import Graph
from sparsifiers.kols_sparsifier import KOLSSparsifier
from sparsifiers.k_neighbor_sparsifier import KNeighborSparsifier
from sparsifiers.ld_sparsifier import LocalDegreeSparsifier
from sparsifiers.mst_sparsifier import MSTSparsifier
from sparsifiers.random_sparsifier import RandomSparsifier
from sparsifiers.t_spanner import TSpannerSparsifier
from visualization.drawer import GraphDrawer
from visualization.summary import summarize_results
from metrics.collector import MetricsCollector


def main():
    wrapper = Graph.from_nx(
        generate_random_graph(40, 5, 0.3, (1, 10), 17, directed=False)
    )

    collector = MetricsCollector(wrapper)
    seed = 31
    strategies = [
        KOLSSparsifier(k=3, rho=0.85, seed=seed),
        RandomSparsifier(p=0.7, seed=seed),
        KNeighborSparsifier(k=3, seed=seed),
        LocalDegreeSparsifier(alpha=0.9),
        MSTSparsifier(),
        RandomSparsifier(p=0.75, seed=seed),
        TSpannerSparsifier(t=2.0),
    ]

    for s in strategies:
        H = s.sparsify(wrapper)
        collector.add(s.name(), H)
        GraphDrawer.draw_graphs(wrapper, H, sparsifier_name=s.name())

    collector.report()
    summarize_results(collector.results)


if __name__ == '__main__':
    main()
