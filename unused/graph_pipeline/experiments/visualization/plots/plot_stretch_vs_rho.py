import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


def plot_stretch_vs_rho(base_results_dir: Path, out_path: Path):
    records = []

    for rho_dir in sorted(base_results_dir.glob("rho_*")):
        rho = float(rho_dir.name.replace("rho_", "").replace("_", "."))

        for result_file in rho_dir.glob("*_results.csv"):
            try:
                df = pd.read_csv(result_file)
                avg_stretch = (
                    df[df['method'] != 'original']
                    .groupby('method')['stretch_avg']
                    .mean()
                    .reset_index()
                )
                avg_stretch["rho"] = rho
                avg_stretch["graph_family"] = df["graph_family"].iloc[0]
                records.append(avg_stretch)
            except Exception as e:
                print(f"error loading {result_file}: {e}")

    if not records:
        print("No records to plot.")
        return

    all_df = pd.concat(records, ignore_index=True)

    plt.figure(figsize=(12, 8))
    sns.lineplot(data=all_df, x="rho", y="stretch_avg", hue="method", marker="o")

    plt.title("average path stretch vs rho", fontsize=16)
    plt.xlabel("prune rate (rho)", fontsize=12)
    plt.ylabel("average path stretch", fontsize=12)
    plt.grid(True)
    plt.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path)
    print(f"plot saved to: {out_path}")
    plt.close()
