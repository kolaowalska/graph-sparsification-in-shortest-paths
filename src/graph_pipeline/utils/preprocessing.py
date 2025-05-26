from pathlib import Path
from utils.converter import convert_file
from utils.parsers import infer_and_parse


def process_unprocessed(input_dir: Path, output_dir: Path) -> None:
    for family_dir in input_dir.iterdir():
        if not family_dir.is_dir():
            continue

        family = family_dir.name
        target_dir = output_dir / family
        target_dir.mkdir(parents=True, exist_ok=True)

        for raw_path in family_dir.iterdir():
            if not raw_path.is_file():
                continue

            if raw_path.suffix.lower() in {".mtx", ".csv"}:
                out_path = target_dir / raw_path.name
            else:
                out_path = target_dir / f"{raw_path.stem}.edgelist"

            convert_file(raw_path, out_path)

            G = infer_and_parse(out_path, graph_family=family)

            print(f"processed {raw_path.name} → {family}/{out_path.name}: {G}")
