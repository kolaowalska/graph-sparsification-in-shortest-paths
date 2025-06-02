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

'''
def generate_plots(raw_csv: Path, output_plots_dir: Path):
    # 1) Load raw (unaggregated) data:
    df_raw = pd.read_csv(raw_csv)
    df_raw['graph_family'] = df_raw['graph_family'].astype(str).str.strip()
    df_raw['method'] = df_raw['method'].astype(str).str.strip()
    output_plots_dir.mkdir(parents=True, exist_ok=True)

    # 2) Within-family plots
    print("→ plotting unaggregated (within-family) data …")
    plot_within_family(df_raw, output_plots_dir)

    # 3) (Optional) per-graph
    # print("→ plotting per-graph data …")
    # plot_per_graph(df_raw, output_plots_dir)

    # 4) Across-families plots, using the aggregated CSV:
    family = raw_csv.parent.name
    agg_csv = raw_csv.parent / f"{family}_aggregated.csv"
    if agg_csv.exists():
        df_agg = pd.read_csv(agg_csv)
        df_agg['graph_family'] = df_agg['graph_family'].astype(str).str.strip()
        df_agg['method'] = df_agg['method'].astype(str).str.strip()

        print("→ plotting aggregated (across-families) data …")
        plot_across_families(df_agg, output_plots_dir)
    else:
        print(f"aggregated CSV not found at {agg_csv}, skipping across-families plots.")


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Usage: python generate_plots.py <raw_results_csv> <output_plots_dir>")
        sys.exit(1)

    raw_csv_arg = Path(sys.argv[1])
    output_plots_arg = Path(sys.argv[2])
    generate_plots(raw_csv_arg, output_plots_arg)

'''


def generate_plots(results_path: Path = None, plots_dir: Path = None):
    if not results_path.exists():
        print(f"error: results file not found at {results_path}")
        print(f"current working directory: {Path.cwd()}")
        print(f"attempted to find file at: {Path.cwd() / results_path}")
        return

    try:
        df = pd.read_csv(results_path)
        df['graph'] = df['graph'].astype(str).str.strip()
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
    generate_plots()
