"""Command-line entry point: python3 -m healthreport"""

import argparse
import socket
import sys
from pathlib import Path

from healthreport.report import format_report
from healthreport.runner import run_all
from healthreport.telegram import TelegramError, send_message


def main() -> int:
    parser = argparse.ArgumentParser(prog="healthreport")
    parser.add_argument(
        "--checks-dir",
        type=Path,
        default=Path("checks"),
        help="folder with check scripts (default: ./checks)",
    )
    parser.add_argument(
        "--send",
        action="store_true",
        help="send the report to Telegram",
    )
    args = parser.parse_args()

    results, failures = run_all(args.checks_dir)

    report = format_report(results, failures, socket.gethostname())
    print(report)

    if args.send:
        try:
            send_message(report)
        except TelegramError as exc:
            print(f"Telegram delivery failed: {exc}", file=sys.stderr)
            return 2

    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
    