import pandas as pd
import numpy as np
from pathlib import Path
# from experiments.visualization.family_plots import plot_within_family
# from experiments.visualization.general_plots import plot_across_families

from experiments.visualization.plots.plot_edge_ratio import plot_edge_ratio
from experiments.visualization.plots.plot_sparsification_time import plot_sparsification_time
from experiments.visualization.plots.plot_avg_stretch_vs_edge_ratio import plot_stretch_vs_edges_ratio
from experiments.visualization.plots.plot_degree_distributions import plot_degree_distributions
from experiments.visualization.plots.plot_avg_stretch_per_sparsifier import plot_avg_stretch_vs_sparsifier
from experiments.visualization.plots.plot_metric_time_by_method import plot_metric_time_by_method


# RESULTS_FILE = Path("../../results")
# RESULTS_FILE = Path("../../results/directed_results.csv")
# PLOTS_DIR = Path("plots/images")
# PLOTS_DIR = Path("../../results")

def ensure_plots_dir(plots_dir: Path):
    plots_dir.mkdir(parents=True, exist_ok=True)


def generate_aggregated_plots(results_path: Path = None, plots_dir: Path = None):
    if not results_path.exists():
        print(f"error: results file not found at {results_path}")
        print(f"current working directory: {Path.cwd()}")
        print(f"attempted to find file at: {Path.cwd() / results_path}")
        return

    try:
        df = pd.read_csv(results_path)
        df['graph_family'] = df['graph_family'].astype(str).str.strip()
        df['method'] = df['method'].astype(str).str.strip()

    except Exception as e:
        print(f"error loading csv file: {e}")
        return

    if df.empty:
        print("the results file is empty, no data to plot")
        return

    ensure_plots_dir(plots_dir)
    print(f"\nloaded {len(df)} rows from {results_path}")

    plot_edge_ratio(df, plots_dir)
    plot_sparsification_time(df, plots_dir)
    plot_stretch_vs_edges_ratio(df, plots_dir)
    plot_degree_distributions(df, plots_dir)
    plot_avg_stretch_vs_sparsifier(df, plots_dir)
    plot_metric_time_by_method(df, plots_dir)

    print(f"\nall plots attempted. check the '{plots_dir}' directory")


if __name__ == "__main__":
    generate_aggregated_plots()
