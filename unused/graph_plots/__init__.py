from pathlib import Path
import pandas as pd

from .plot_degree_distributions import plot_degree_distributions
# from .plot_edge_ratio_per_graph import plot_edge_ratio_per_graph


def plot_per_graph(df: pd.DataFrame, plots_dir: Path):
    per_graph_dir = plots_dir / "per_graph"
    per_graph_dir.mkdir(parents=True, exist_ok=True)

    for _, row in df.iterrows():
        graph_id = row['graph']
        # e.g.: plot_degree_distribution_per_graph(row, per_graph_dir)
        # e.g.: plot_edge_ratio_per_graph(row, per_graph_dir)
        pass

    print(f"[graph_plots] saved all per-graph plots under {per_graph_dir}")
