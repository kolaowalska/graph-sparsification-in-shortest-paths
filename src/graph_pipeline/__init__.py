from pathlib import Path
from tqdm import tqdm
from utils.preprocessing import process_unprocessed
from utils.parsers import infer_and_parse
from utils.visualizer import visualize_sparsification
from sparsifiers import sparsifiers_registry
from experiments import run_experiments as rexp
from experiments.visualization import generate_all_plots as plot
from experiments.visualization.plots.plot_stretch_vs_rho import plot_stretch_vs_rho

UNPROCESSED_DIR = Path("small_data/unprocessed")
PROCESSED_DIR = Path("small_data/processed")
RESULTS_DIR = Path("./small_results")
IMAGES_DIR = RESULTS_DIR / "images"

MULTI_RHO = False
# RHO = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0] if MULTI_RHO else [0.2]
RHO = 0.2

## TODO:
'''
- dodac wykresy pokazujace rozbieznosc roznych metryk w zaleznosci od prune rate 
dla kazdego sparsyfikatora w obrebie 1 rodziny grafow?? za duzo slow to jest
- przepuscic wieksze grafy przez ten kolchoz 
- cos jeszcze wymysle
'''


def draw_small_graphs(family: str):
    try:
        example_path = PROCESSED_DIR / family / f"{family}1.edgelist"
        G = infer_and_parse(example_path, family)
        sparsified_versions = {}

        for method_name, sparsifier in sparsifiers_registry.items():
            H = sparsifier(G, RHO)
            if isinstance(H, tuple):
                H = H[0]
            sparsified_versions[method_name] = H

        image_output_dir = RESULTS_DIR / "images"
        visualize_sparsification(G, sparsified_versions, f"{family}_example", image_output_dir)

    except Exception as e:
        tqdm.write(f"visualization skipped for {family}: {e}")


if __name__ == "__main__":
    '''
    input_unprocessed = Path("./data/unprocessed")
    processed_dir = Path("./data/processed")
    results_dir = Path("./results")
    rho = 0.2  # desired prune rate, 0 <= rho <= 1
    '''

    families = None

    process_unprocessed(UNPROCESSED_DIR, PROCESSED_DIR)

    if families is None:
        families = [d.name for d in PROCESSED_DIR.iterdir() if d.is_dir()]

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    for family in families:
        print("\n")
        data_dir = PROCESSED_DIR / family
        if not data_dir.exists():
            tqdm.write(f"skipping missing family: {family}")
            continue

        out_file = RESULTS_DIR / f"{family}_results.csv"
        tqdm.write(f"running experiments for '{family}', output → {out_file}")

        setattr(rexp, 'data_dir', data_dir)
        setattr(rexp, 'out_file', out_file)
        setattr(rexp, 'family', family)

        rexp.main(rho=RHO, data_dir=data_dir, out_file=out_file, family=family)
        plot.generate_plots(out_file, RESULTS_DIR / f"{family}_plots")
        draw_small_graphs(family)


    '''
        for rho in RHO_VALUES:
        suffix = f"rho_{str(rho).replace('.', '_')}" if MULTI_RHO else "main"
        rho_dir = RESULTS_DIR / suffix
        rho_dir.mkdir(parents=True, exist_ok=True)

        for family in families:
            print(f"\nRunning experiments for '{family}' at rho = {rho}")

            data_dir = PROCESSED_DIR / family
            if not data_dir.exists():
                tqdm.write(f"Skipping missing family: {family}")
                continue

            out_file = rho_dir / f"{family}_results.csv"

            setattr(rexp, 'data_dir', data_dir)
            setattr(rexp, 'out_file', out_file)
            setattr(rexp, 'family', family)

            rexp.main(rho=rho, data_dir=data_dir, out_file=out_file, family=family)

            # plot.generate_plots(out_file, rho_dir / f"{family}_plots")

            if MULTI_RHO:
                plot_stretch_vs_rho(
                    base_results_dir=RESULTS_DIR,
                    out_path=RESULTS_DIR / "collective_plots" / "stretch_vs_rho.png"
                )
    '''

