import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


def summarize_results(results: dict):
    df = pd.DataFrame(results).T

    df['diameter_change'] = df['diameter_sparsified'] - df['diameter_original']
    df['connected'] = df['connected_sparsified'].astype(bool)

    columns = [
        'edges_ratio',
        'stretch_avg',
        'stretch_var',
        'diameter_change'
    ]

    colors = ['violet', 'hotpink', 'orchid', 'pink',
              'palevioletred', 'thistle', 'plum']

    num_bars = len(df.index)
    if num_bars > len(colors):
        raise ValueError(f"zabraklo dziewczynskich kolorkow")

    # print("\n~~~~~ summary table ~~~~~~")
    # print(df[columns])

    mpl.rcParams.update({
        "font.family": "serif",
        "font.serif": ["DejaVu Serif"],
        "axes.titlesize": 12,
        "axes.labelsize": 8,
        "xtick.labelsize": 8,
        "ytick.labelsize": 8
    })

    ncols = 2
    nrows = (len(columns) + ncols - 1) // ncols
    fig, axs = plt.subplots(nrows, ncols, figsize=(8, 2.5 * nrows))
    axs = axs.flatten()

    for i, metric in enumerate(columns):
        axs[i].bar(df.index, df[metric], color=colors)
        # axs[i].set_title(f'{metric.replace("_", " ").title()}', fontsize=16)
        axs[i].set_ylabel(f'{metric.replace("_", " ").lower()}', fontsize=10)
        axs[i].tick_params(axis='x', labelrotation=30)
        axs[i].set_xticks(range(len(df.index)))

        new_labels = []
        for label in df.index:
            if '(' in label:
                label_parts = label.split('(')
                label_parts[1] = '(' + label_parts[1]
                new_label = '\n'.join(label_parts)
            else:
                new_label = label
            new_labels.append(new_label)

        axs[i].set_xticklabels(new_labels, ha='right', fontsize=6)

        for j, value in enumerate(df[metric]):
            if np.isfinite(value):
                axs[i].text(j, value + 0.01, f'{value:.2f}', ha='center', fontsize=7)

    # fig.suptitle('sparsification overview', fontsize=20)
    plt.tight_layout(rect=[0, 0, 1, 0.97])
    plt.show()
