import sys
import argparse
from src.interfaces.smoke import run_smoke


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(description="graph sparsification pipeline")
    parser.add_argument("--smoke", action="store_true", help="run a quick smoke test")

    parsed_args = parser.parse_args(args)

    if parsed_args.smoke:
        print("running smoke test...")
        run_smoke()
        return 0

    print("no arguments provided, try --smoke")
    return 0


if __name__ == "__main__":
    sys.exit(main())