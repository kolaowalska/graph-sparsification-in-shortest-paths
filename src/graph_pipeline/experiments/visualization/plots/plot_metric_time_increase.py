import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


# change in metric computation time across families
# DONE

def plot_metric_time_increase(df: pd.DataFrame, plots_dir: Path):
    required_cols = ['metric_time', 'method', 'graph_family']
    if not all(col in df.columns for col in required_cols):
        print("skipping 'metric time by method' plot: required columns are missing")
        return

    df = df[df['metric_time'].notna()]

    original_times = (
        df[df['method'] == 'original']
        .groupby('graph_family', as_index=False)['metric_time']
        .mean()
        .rename(columns={'metric_time': 'original_time'})
    )

    other_methods = (
        df[df['method'] != 'original']
        .groupby(['graph_family', 'method'], as_index=False)['metric_time']
        .mean()
    )

    merged = pd.merge(other_methods, original_times, on='graph_family', how='inner')
    merged['normalized_metric_time'] = merged['metric_time'] - merged['original_time']

    plt.figure(figsize=(10, 8))
    sns.barplot(
        data=merged,
        x='method',
        y='normalized_metric_time',
        hue='graph_family',
        palette='crest',
        errorbar=None
    )

    plt.ylabel('change in metric computation time vs original (s)', fontsize=12)
    plt.xlabel('sparsification method', fontsize=12)
    plt.legend(title='graph family')
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()

    plot_filename = plots_dir / 'normalized_metric_time_by_method_and_family.png'
    plots_dir.mkdir(parents=True, exist_ok=True)
    plt.savefig(plot_filename)
    print(f"plot saved: {plot_filename}")
    plt.close()
