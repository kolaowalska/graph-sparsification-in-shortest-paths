import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


def plot_sparsification_time(df: pd.DataFrame, plots_dir: Path):
    """
    For each distinct graph_family in `df` (raw, unaggregated),
    compute the average sparsification time per method and save a bar plot.

    Expects columns:
      - 'graph' or 'graph_family'
      - 'method'
      - 'sparsify_time'

    Saves one PNG per family:
      plots_dir / f"sparsify_time_family_{family}.png"
    """
    # Check required columns
    required = {'graph_family', 'method', 'sparsify_time'}
    if not required.issubset(df.columns):
        print("skipping 'sparsification time within family' plot: required columns are missing")
        return

    # Ensure plots directory exists
    plots_dir.mkdir(parents=True, exist_ok=True)

    # Iterate over each family
    families = sorted(df['graph_family'].dropna().unique())
    if not families:
        print("no families found; skipping sparsification-time plots")
        return

    for fam in families:
        df_fam = df[df['graph_family'] == fam].copy()
        df_fam = df_fam[df_fam['sparsify_time'].notna()]

        if df_fam.empty:
            print(f"[{fam}] no valid sparsify_time data; skipping")
            continue

        # Group by method and take mean of sparsify_time
        grouped = (
            df_fam
            .groupby('method', as_index=False)['sparsify_time']
            .mean()
        )

        plt.figure(figsize=(8, 6))
        sns.barplot(
            data=grouped,
            x='method',
            y='sparsify_time',
            palette="mako",
            order=sorted(grouped['method'].unique()),
            errorbar=None
        )
        plt.title(f"Average sparsification time for family '{fam}'", fontsize=16)
        plt.ylabel("sparsification time (s)", fontsize=12)
        plt.xlabel("sparsification method", fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y', linestyle='--', alpha=0.6)
        plt.tight_layout()

        fname = plots_dir / f"sparsify_time_family_{fam}.png"
        plt.savefig(fname)
        print(f"plot saved: {fname}")
        plt.close()
