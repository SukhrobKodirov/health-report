from healthreport.report import format_report
from healthreport.runner import Failure, Result


def test_report_lists_every_result():
    results = [Result("disk_used", 53, "percent", "/", "10-disk.sh")]
    text = format_report(results, [], "box")
    assert text.startswith("Health Report: box")
    assert "disk_used (/): 53 percent" in text
    assert "Dailures" not in text


def test_report_shows_failures():
    failures = [Failure("99-broken.sh", "exit code 3")]
    text = format_report([], failures, "box")
    assert "Failures:" in text
    assert "- 99-broken.sh: exit code 3" in text
    