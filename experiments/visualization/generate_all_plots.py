import pandas as pd
from pathlib import Path

from experiments.visualization.plots.plot_edge_ratio import plot_edge_ratio
from experiments.visualization.plots.plot_sparsification_time import plot_sparsification_time
from experiments.visualization.plots.plot_stretch_vs_edge_ratio import plot_stretch_vs_edges_ratio
from experiments.visualization.plots.plot_degree_distributions import plot_degree_distributions

RESULTS_FILE = Path("../../src/graph_pipeline/results/results.csv")
PLOTS_DIR = Path("./plots/images")


def ensure_plots_dir(plots_dir: Path):
    plots_dir.mkdir(parents=True, exist_ok=True)


def generate_plots(results_path: Path = RESULTS_FILE, plots_dir: Path = PLOTS_DIR):
    if not results_path.exists():
        print(f"error: results file not found at {results_path}")
        print("ensure run_experiments.py has been executed successfully and results.csv exists")
        print(f"current working directory: {Path.cwd()}")
        print(f"attempted to find file at: {Path.cwd() / results_path}")
        return

    try:
        df = pd.read_csv(results_path)
    except Exception as e:
        print(f"error loading csv file: {e}")
        return

    if df.empty:
        print("the results.csv file is empty, no data to plot")
        return

    ensure_plots_dir(plots_dir)
    print(f"loaded {len(df)} rows from {results_path}")
    print("available columns:", df.columns.tolist())

    plot_edge_ratio(df, plots_dir)
    plot_sparsification_time(df, plots_dir)
    plot_stretch_vs_edges_ratio(df, plots_dir)
    plot_degree_distributions(df, plots_dir)

    print(f"\nall plots attempted. check the '{plots_dir}' directory")


if __name__ == "__main__":
    generate_plots()
