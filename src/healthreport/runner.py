"""Discover, run and parse check script."""

import json
import os
import subprocess
from dataclasses import dataclass
from pathlib import Path

TIMEOUT_SECONDS = 20
REQUIRED_KEYS = {"check", "value", "unit", "target"}

@dataclass
class Result:
    check: str
    value: float | None
    unit: str
    target: str
    source: str

@dataclass
class Failure:
    source: str
    reason: str

def discover(checks_dir: Path) -> list[Path]:
    """Return executable .sh files in name order."""
    return sorted(
        p for p in checks_dir.iterdir()
        if p.is_file() and p.suffix == ".sh" and os.access(p, os.X_OK)
    )

def parse_line(line: str, source: str) -> Result:
    """Turn one JSON line into a Result. Raises ValueError if invalid."""
    data = json.loads(line)
    missing = REQUIRED_KEYS - data.keys()
    if missing:
        raise ValueError(f"missing keys: {sorted(missing)}")
    return Result(
        check=data["check"],
        value=data["value"],
        unit=data["unit"],
        target=data["target"],
        source=source,
    )

def run_check(path: Path) -> tuple[list[Result], list[Failure]]:
    results: list[Result] = []
    failures: list[Failure] = []
    try:
        proc = subprocess.run(
            [str(path)],
            capture_output=True,
            text=True,
            check=False,
            timeout=TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired:
        return [], [Failure(path.name, f"timed out after {TIMEOUT_SECONDS}s")]

    if proc.returncode != 0:
        reason = proc.stderr.strip() or f"exit code {proc.returncode}"
        failures.append(Failure(path.name, reason))

    for line in proc.stdout.splitlines():
        if not line.strip():
            continue
        try:
            results.append(parse_line(line, path.name))
        except (json.JSONDecodeError, ValueError) as exc:
            failures.append(Failure(path.name, f"bad output: {exc}"))

    return results, failures

def run_all(checks_dir: Path) -> tuple[list[Result], list[Failure]]:
    """Run every check and combine the results."""
    all_results: list[Result] = []
    all_failures: list[Failure] = []
    for path in discover(checks_dir):
        results, failures = run_check(path)
        all_results.extend(results)
        all_failures.extend(failures)
    return all_results, all_failures
