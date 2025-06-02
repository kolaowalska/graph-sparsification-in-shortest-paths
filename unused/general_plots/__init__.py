from pathlib import Path
import pandas as pd

from .avg_degree_distribution import plot_avg_degree_distributions
# from .edge_ratio_method import plot_edge_ratio
from .sparsification_time import plot_sparsification_time
from .metric_time import plot_metric_time


def plot_across_families(df_agg: pd.DataFrame, plots_dir: Path):

    plots_dir.mkdir(parents=True, exist_ok=True)

    plot_avg_degree_distributions(df_agg, plots_dir)
    # plot_edge_ratio(df_agg, plots_dir)
    plot_sparsification_time(df_agg, plots_dir)
    plot_metric_time(df_agg, plots_dir)

    print(f"[general_plots] saved all across-families plots under {plots_dir}")
