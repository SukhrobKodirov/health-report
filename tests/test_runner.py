import pytest

from healthreport.runner import parse_line, run_check


def test_parse_line_valid():
    r = parse_line('{"check":"disk_used","value":53,"unit":"percent","target":"/"}', "x.sh")
    assert r.check == "disk_used"
    assert r.value == 53
    assert r.source == "x.sh"


def test_parse_line_missing_key():
    with pytest.raises(ValueError, match="missing keys"):
        parse_line('{"check":"disk_used","value":53}', "x.sh")


def make_script(tmp_path, body):
    path = tmp_path / "check.sh"
    path.write_text(f"#!/usr/bin/env bash\n{body}\n")
    path.chmod(0o755)
    return path


def test_run_check_good(tmp_path):
    path = make_script(tmp_path, """echo '{"check":"a","value":1,"unit":"u","target":"t"}'""")
    results, failures = run_check(path)
    assert len(results) == 1
    assert failures == []


def test_run_check_crash_keeps_going(tmp_path):
    path = make_script(tmp_path, 'echo "not json"; exit 3')
    results, failures = run_check(path)
    assert results == []
    assert len(failures) == 2