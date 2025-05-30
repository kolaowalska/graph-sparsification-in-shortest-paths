import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


# average stretch per sparsification method
def plot_avg_stretch_vs_sparsifier(df: pd.DataFrame, plots_dir: Path):
    plot_filename = plots_dir / 'stretch_per_sparsifier.png'
    plots_dir.mkdir(parents=True, exist_ok=True)

    if not all(col in df.columns for col in ['stretch_avg', 'method']):
        print("skipping 'stretch vs sparsifier' plot: required columns are missing")
        return

    df = df.copy()
    df['stretch_avg'] = pd.to_numeric(df['stretch_avg'], errors='coerce')
    df = df.dropna(subset=['stretch_avg'])

    if df.empty:
        print("no valid data to plot after dropping nan's")
        return

    try:
        plt.figure(figsize=(10, 8))
        sns.boxplot(data=df, x='method', y='stretch_avg', hue='method', palette='viridis')
        plt.title(f'average stretch by sparsification method', fontsize=16)
        plt.ylabel('average stretch', fontsize=12)
        plt.xlabel('sparsification method', fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', title='method')
        plt.tight_layout(rect=[0, 0, 0.88, 1])

        plt.savefig(plot_filename)
        print(f"plot saved: {plot_filename}")

        # plt.show()
        plt.close()
    except Exception as e:
        print(f"failed to plot avg stretch per sparsifier method")
