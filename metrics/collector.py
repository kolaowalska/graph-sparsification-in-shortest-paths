from graphs.graph import Graph
from metrics.structural import (
    degree_distribution,
    is_connected,
    laplacian_quadratic_form
)
from metrics.distance import (
    apsp_matrix,
    graph_diameter,
    unreachable_pairs_ratio,
    local_stretch,
    stretch_avg,
    stretch_var,
    max_stretch
)


class MetricsCollector:
    def __init__(self, original: Graph):
        self.original = original
        self.results = {}
        G0 = getattr(original, '_G', original)
        self._x = {v: G0.degree(v, weight='weight') for v in G0.nodes()}

    def add(self, name: str, sparsified: Graph):
        G = getattr(self.original, '_G', self.original)
        H = getattr(sparsified, '_G', sparsified)

        # distance metrics
        G_dist = apsp_matrix(G, weight='weight')
        H_dist = apsp_matrix(H, weight='weight')
        stretch = local_stretch(G_dist, H_dist)

        # structural metrics
        G_distribution = degree_distribution(G)
        H_distribution = degree_distribution(H)
        qf_G = laplacian_quadratic_form(G, x=self._x)
        qf_H = laplacian_quadratic_form(H, x=self._x)

        self.results[name] = {
            'edges_ratio': H.number_of_edges() / G.number_of_edges(),
            'connected_original': is_connected(G),
            'connected_sparsified': is_connected(H),
            'diameter_original': graph_diameter(G_dist),
            'diameter_sparsified': graph_diameter(H_dist),
            'unreachable_pairs_ratio': unreachable_pairs_ratio(H_dist, G.number_of_nodes()),
            'stretch_avg': stretch_avg(local_stretch(G_dist, H_dist)),
            'stretch_var': stretch_var(local_stretch(G_dist, H_dist)),
            'stretch_max': max_stretch(local_stretch(G_dist, H_dist)),
            'degree_distribution_original' : G_distribution,
            'degree_distribution_sparsified': H_distribution,
            'laplacian_qf_original': qf_G,
            'laplacian_qf_sparsified': qf_H
        }

    def report(self):
        for name, metrics in self.results.items():
            print("\n")
            print(f"--- {name} ---")
            for k, v in metrics.items():
                print(f"{k}: {v}")
