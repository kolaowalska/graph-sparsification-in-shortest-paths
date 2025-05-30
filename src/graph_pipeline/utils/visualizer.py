import networkx as nx
from pathlib import Path
from matplotlib import gridspec
from matplotlib import pyplot as plt


def visualize_sparsification(original, sparsified_dict, graph_name, output_dir):
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    num_sparsifiers = len(sparsified_dict)
    sparsifier_items = list(sparsified_dict.items())

    fig = plt.figure(figsize=(18, 10))
    spec = gridspec.GridSpec(2, 4, width_ratios=[1, 1, 1, 1])

    layout = nx.kamada_kawai_layout(original.G)

    def draw_with_edge_weights(G, ax, title):
        nx.draw(
            G, pos=layout, ax=ax, with_labels=True,
            node_color='thistle' if title.startswith("original") else 'palevioletred',
            edge_color='gray' if title.startswith("original") else 'black'
        )
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos=layout, edge_labels=edge_labels, ax=ax, font_size=8)
        ax.set_title(title)

    ax_orig = fig.add_subplot(spec[:, 0])
    draw_with_edge_weights(original.G, ax_orig, f"original (|E|={original.m})")

    for i, (name, H) in enumerate(sparsifier_items):
        row = 0 if i < 3 else 1
        col = (i % 3) + 1
        ax = fig.add_subplot(spec[row, col])
        draw_with_edge_weights(H.G, ax, f"{name} (|E'|={H.m})")

    plt.tight_layout()
    out_path = Path(output_dir) / f"{graph_name}_comparison.png"
    plt.savefig(out_path, dpi=300)
    plt.close()
