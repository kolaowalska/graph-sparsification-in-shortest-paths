from pathlib import Path
from tqdm import tqdm
from src.graph_pipeline.utils.preprocessing import process_unprocessed
from src.graph_pipeline.experiments import run_experiments as rexp

if __name__ == "__main__":
    input_unprocessed = Path("./data/unprocessed")
    processed_dir = Path("./data/processed")
    results_dir = Path("./results")
    rho = 0.2
    families = None

    process_unprocessed(input_unprocessed, processed_dir)

    if families is None:
        families = [d.name for d in processed_dir.iterdir() if d.is_dir()]

    results_dir.mkdir(parents=True, exist_ok=True)

    for family in families:
        data_dir = processed_dir / family
        if not data_dir.exists():
            tqdm.write(f"skipping missing family folder: {family}")
            continue

        out_file = results_dir / f"{family}_results.csv"
        tqdm.write(f"running experiments for '{family}', output → {out_file}")

        setattr(rexp, 'data_dir', data_dir)
        setattr(rexp, 'out_file', out_file)
        setattr(rexp, 'family', family)

        rexp.main(rho=rho, data_dir=data_dir, out_file=out_file, family=family)
