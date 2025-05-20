import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from pathlib import Path


RESULTS_FILE = Path("../results/results.csv")
PLOTS_DIR = Path("./plots")


def plot_results(results_path: Path = RESULTS_FILE):
    if not results_path.exists():
        print(f"results file not found: {results_path} :(")
        return

    df = pd.read_csv(results_path)
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)
    print(f"loaded {len(df)} rows from {results_path}")
    print("available columns: ", df.columns.tolist())

    plt.figure(figsize=(12, 7))
    sns.boxplot(data=df, x='sparsifier', y='edges_ratio', hue='graph_family')
    plt.title('edge ratio by sparsication method & graph family')
    plt.ylabel('edges ratio (sparse/original)')
    plt.xlabel('sparsification algorithm')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / 'edges_ratio_by_sparsifier_family.png')
    plt.show()

    if 'stretch_avg' in df.columns and 'rho' in df.columns:
        for family in df['graph_family'].unique():
            family_df = df[df['graph_family'] == family]
            plt.figure(figsize=(12, 7))
            sns.lineplot(data=df, x='rho', y='stretch_avg', hue='sparsifier', marker='o')
            plt.title(f'average stretch vs rho for {family} graphs')
            plt.ylabel('average stretch')
            plt.xlabel('sparsification parameter rho')
            plt.grid(True, linestyle='--', alpha=0.7)
            plt.tight_layout()
            plt.savefig(PLOTS_DIR / f'stretch_avg_vs_rho_{family}.png')
            plt.show()
    else:
        print("columns not found for plotting")


if __name__ == "__main__":
    plot_results()
