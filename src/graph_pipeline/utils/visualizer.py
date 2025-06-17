import networkx as nx
from pathlib import Path
from matplotlib import gridspec
from matplotlib import pyplot as plt


def visualize_sparsification(original, sparsified_dict, graph_name, output_dir):
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    num_sparsifiers = len(sparsified_dict)
    sparsifier_items = list(sparsified_dict.items())

    fig = plt.figure(figsize=(16, 8))
    spec = gridspec.GridSpec(2, 4, width_ratios=[1, 1, 1, 1])

    layout = nx.spring_layout(original.G, seed=42, k=1.5/len(original.G), scale=2.0)

    def draw_with_edge_weights(G, ax, title):
        nx.draw(
            G, pos=layout, ax=ax, with_labels=True,
            node_color='thistle' if title.startswith("original") else 'palevioletred',
            edge_color='gray' if title.startswith("original") else 'black',
            node_size=500, font_size=10
        )
        # edge_labels = nx.get_edge_attributes(G, 'weight')
        edge_labels = {e: int(w) for e, w in nx.get_edge_attributes(G, 'weight').items()}
        nx.draw_networkx_edge_labels(G, pos=layout, edge_labels=edge_labels, ax=ax, font_size=8)
        ax.set_title(title)
        ax.set_axis_off()

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
