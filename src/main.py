from __future__ import annotations

import argparse


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser()
    p.add_argument("--smoke", action="store_true", help="Run minimal end-to-end smoke test")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.smoke:
        from interfaces.smoke import run_smoke
        run_smoke()
        return 0
    return -1

    # na pozniej
    # from interfaces.cli import run_cli
    # return run_cli(argv)


if __name__ == "__main__":
    raise SystemExit(main())
