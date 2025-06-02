import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


def plot_sparsification_time(df_agg: pd.DataFrame, plots_dir: Path):
    """
    Compare average sparsification time across families. Assumes `df_agg` is already
    aggregated (one row per graph_family × method) with averaged 'sparsify_time'.

    Expects columns:
      - 'graph_family'
      - 'method'
      - 'sparsify_time'

    Saves one PNG:
      plots_dir / "sparsify_time_across_families.png"
    """
    required = {'graph_family', 'method', 'sparsify_time'}
    if not required.issubset(df_agg.columns):
        print("skipping 'sparsification time across families' plot: required columns are missing")
        return

    # Filter out any missing values
    df_plot = df_agg[df_agg['sparsify_time'].notna()].copy()
    if df_plot.empty:
        print("no valid sparsify_time in aggregated data; skipping")
        return

    # Ensure plots directory exists
    plots_dir.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(10, 8))
    sns.barplot(
        data=df_plot,
        x='graph_family',
        y='sparsify_time',
        hue='method',
        palette="mako",
        order=sorted(df_plot['graph_family'].unique()),
        dodge=True,
        errorbar=None
    )
    plt.title("Average sparsification time across families", fontsize=16)
    plt.ylabel("sparsification time (s)", fontsize=12)
    plt.xlabel("graph family", fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.legend(title='method', bbox_to_anchor=(1.02, 1), loc='upper left')
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()

    fname = plots_dir / "sparsify_time_across_families.png"
    plt.savefig(fname)
    print(f"plot saved: {fname}")
    plt.close()
