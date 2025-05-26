from unused.graphs import generate_random_graph
from unused.graphs import Graph
from sparsifiers.kols import KOLSSparsifier
from sparsifiers.k_neighbor import KNeighborSparsifier
from sparsifiers.ld import LocalDegreeSparsifier
from sparsifiers.mst import MSTSparsifier
from sparsifiers.random import RandomSparsifier
from sparsifiers.t_spanner import TSpannerSparsifier
from unused.visualization.drawer import GraphDrawer
from unused.visualization.summary import summarize_results
from metrics.collector import MetricsCollector


def main():
    wrapper = Graph.from_nx(
        generate_random_graph(40, 5, 0.3, (1, 10), 17, directed=False)
    )

    collector = MetricsCollector(wrapper)
    seed = 31
    strategies = [
        KOLSSparsifier(k=3, rho=0.85, seed=seed),
        RandomSparsifier(rho=0.7, seed=seed),
        KNeighborSparsifier(k=3, seed=seed),
        LocalDegreeSparsifier(alpha=0.9),
        MSTSparsifier(),
        RandomSparsifier(rho=0.75, seed=seed),
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
