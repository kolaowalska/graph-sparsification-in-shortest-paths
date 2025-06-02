#!/usr/bin/env python3
import pandas as pd
from pathlib import Path


def aggregate_by_family(input_csv: Path=None, output_csv: Path=None):
    if not input_csv.exists():
        raise FileNotFoundError(f"cannot find {input_csv}")

    df = pd.read_csv(input_csv)
    df['graph_family'] = df['graph_family'].astype(str).str.strip()
    df['method'] = df['method'].astype(str).str.strip()

    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()

    grouped = (
        df
        .groupby(['graph_family', 'method'], as_index=False)[numeric_cols]
        .mean()
    )

    output_csv.parent.mkdir(parents=True, exist_ok=True)
    grouped.to_csv(output_csv, index=False)
    # print(f"wrote {len(grouped)} rows to {output_csv}")


if __name__ == "__main__":
    aggregate_by_family()
