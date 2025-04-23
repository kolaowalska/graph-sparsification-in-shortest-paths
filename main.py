import networkx as nx
from graphs.generators import generate_random_graph
from sparsifiers.kols_sparsifier import kols_sparsifier
from sparsifiers.k_neighbor_sparsifier import k_neighbor_sparsifier
from sparsifiers.ld_sparsifier import local_degree_sparsifier
from sparsifiers.mst_sparsifier import mst_sparsifier
from sparsifiers.random_sparsifier import random_sparsifier
from utils.draw import draw_graphs
from metrics.structural_metrics import (
    degree_distribution,
    is_connected
)
from metrics.distance_metrics import (
    apsp_matrix,
    graph_diameter,
    unreachable_pairs_ratio,
    local_stretch,
    stretch_avg,
    stretch_var,
    max_stretch
)


def compare_graphs(G, sparsified_graphs: dict, weight='weight'):
    print("\nmetric comparison <3")
    G_dist = apsp_matrix(G, weight='weight')
    n = G.number_of_nodes()

    for name, H in sparsified_graphs.items():
        print(f"\n{name.upper()} SPARSIFIER:")
        H_dist = apsp_matrix(H, weight='weight')

        print(f"edges: {H.number_of_edges()} / {G.number_of_edges()}")
        print(f"connected_G:", is_connected(G))
        print(f"connected_H:", is_connected(H))
        print("diameter_G:", graph_diameter(G_dist))
        print("diameter_H:", graph_diameter(H_dist))
        print("unreachable pairs ratio:", unreachable_pairs_ratio(H_dist, n))

        stretch = local_stretch(G_dist, H_dist)
        print("stretch_avg:", round(stretch_avg(stretch), 3))
        print("stretch_var:", round(stretch_var(stretch), 3))
        print("max_stretch:", round(max_stretch(stretch), 3))


if __name__ == "__main__":
    '''
    G2 = nx.DiGraph()
    G2.add_weighted_edges_from([
        (0, 1, 2), (1, 2, 3), (2, 3, 4), (0, 3, 1),
        (3, 0, 2), (2, 0, 1), (1, 3, 1)
    ])
    '''
    rs = 42
    G = generate_random_graph(n=30, k=6, p=0.3, weight_range=(1, 10), seed=rs)

    H_kola = kols_sparsifier(G, k=3, rho=0.65, rescale=True, seed=rs)
    H_k = k_neighbor_sparsifier(G, k=3, seed=rs)
    H_ld = local_degree_sparsifier(G, alpha=0.8)
    H_r = random_sparsifier(G, p=0.7, seed=rs)
    H_mst = mst_sparsifier(G)

    # print(f"original graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
    # print(f"sparsified graph: {H_kola.number_of_nodes()} nodes, {H_kola.number_of_edges()} edges")
    # print(f"sparsified graph: {H_k.number_of_nodes()} nodes, {H_k.number_of_edges()} edges")

    draw_graphs(G, H_kola, title_h="kols_sparsifier")
    draw_graphs(G, H_k, title_h="k_neighbor_sparsifier")
    draw_graphs(G, H_ld, title_h="local_degree_sparsifier (α=0.8)")
    draw_graphs(G, H_r, title_h="random_sparsifier")
    draw_graphs(G, H_mst, title_h="mst_sparsifier")

    compare_graphs(G, {'kols': H_kola,
                       'k_neighbor': H_k,
                       'local_degree': H_ld,
                       'random': H_r,
                       'mst': H_mst})

