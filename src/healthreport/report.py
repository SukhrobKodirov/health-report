"""Turn result into human-readable text."""

from healthreport.runner import Failure, Result


def format_report(results: list[Result], failures: list[Failure], hostname: str) -> str:
    lines = [f"Health Report: {hostname}", ""]
    for r in results:
        lines.append(f"{r.check} ({r.target}): {r.value} {r.unit}")
    if failures:
        lines.append("")
        lines.append("Failures:")
        for f in failures:
            lines.append(f"- {f.source}: {f.reason}")
    return "\n".join(lines)