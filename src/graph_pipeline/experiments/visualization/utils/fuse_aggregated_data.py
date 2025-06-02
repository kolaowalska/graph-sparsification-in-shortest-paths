import pandas as pd
from pathlib import Path
from tqdm import tqdm


def fuse_aggregated_families(results_dir: Path, output_csv: Path):
    aggregated_frames = []

    for family_dir in results_dir.iterdir():
        if family_dir.is_dir():
            family_name = family_dir.name
            agg_file = family_dir / f"{family_name}_aggregated.csv"
            if agg_file.exists():
                df = pd.read_csv(agg_file)
                df['family'] = family_name
                aggregated_frames.append(df)
            else:
                tqdm.write(f"missing aggregated file: {agg_file}, skipping")

    if aggregated_frames:
        combined_df = pd.concat(aggregated_frames, ignore_index=True)
        output_csv.parent.mkdir(parents=True, exist_ok=True)
        combined_df.to_csv(output_csv, index=False)
        tqdm.write(f"global aggregated file saved to {output_csv}")
    else:
        tqdm.write("no aggregated family files found to combine")
