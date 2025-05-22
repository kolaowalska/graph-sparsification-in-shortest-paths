import argparse
from pathlib import Path
from tqdm import tqdm
from experiments import run_experiments as rexp


def main():
    parser = argparse.ArgumentParser(
        description="run sparsification for each processed graph family"
    )
    parser.add_argument(
        "--input-dir", "-i",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "data" / "processed",
        help="root directory containing processed graph families"
    )
    parser.add_argument(
        "--output-dir", "-o",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "results",
        help="directory to write per-family result csv's"
    )
    parser.add_argument(
        "--rho", "-r",
        type=float,
        default=0.2,
        help="sparsification prune rate"
    )
    parser.add_argument(
        "--families", "-f",
        nargs="*",
        default=None,
        help="names of specific families to run (default: all subdirectories)"
    )
    args = parser.parse_args()

    # input_root = args.input_dir
    # output_root = args.output_dir
    # rho = args.rho

    input_root = Path("data/processed")
    output_root = Path("results")
    rho = 0.2

    if args.families:
        families = args.families
    else:
        families = [d.name for d in input_root.iterdir() if d.is_dir()]

    output_root.mkdir(parents=True, exist_ok=True)

    for family in tqdm(families, desc="families", unit="family"):
        data_dir = input_root / family
        if not data_dir.exists():
            tqdm.write(f"skipping missing family folder: {family}")
            continue

        rexp.DATA_DIR = data_dir
        out_file = output_root / f"{family}_results.csv"
        rexp.OUT_FILE = out_file
        tqdm.write(f"running experiments for '{family}', output → {out_file}")
        rexp.main(rho=rho)


if __name__ == "__main__":
    main()
