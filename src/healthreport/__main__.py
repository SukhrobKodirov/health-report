"""Command-line entry point: python3 -m healthreport"""

import argparse
import sys
from pathlib import Path

from healthreport.runner import run_all


def main() -> int:
    parser = argparse.ArgumentParser(prog="healthreport")
    parser.add_argument(
        "--checks-dir",
        type=Path,
        default=Path("checks"),
        help="folder which checks scripts (default: ./checks)",
    )
    args = parser.parse_args()

    results, failures = run_all(args.checks_dir)

    for r in results:
        print(f"{r.check:<20} {r.value!s:>6} {r.unit:<8} {r.target:<6} ({r.source})")
    for f in failures:
        print(f"FAILED {f.source}: {f.reason}", file=sys.stderr)

    return 1 if failures else 0

if __name__ == "__main__":
    sys.exit(main())

