"""table-keeper's house benchmark: campaign, questions and scorer.

Run: python3 -m pytest tests/test_house_benchmark.py -q
"""
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BENCH = ROOT / "tests" / "house-benchmark"


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


hb = _load("house_bench_score", ROOT / "scripts" / "house_bench_score.py")
pc = _load("profile_check", ROOT / "skills" / "shared" / "house" / "profile_check.py")


def test_questions_are_well_formed():
    questions = hb.load_questions()
    ids = [q["id"] for q in questions]
    assert len(ids) == len(set(ids))
    for q in questions:
        assert q["prompt"].strip() and q["skill"]
        assert (ROOT / "skills" / q["skill"] / "SKILL.md").is_file()
        item_ids = [i["id"] for i in q["rubric"]]
        assert len(item_ids) == len(set(item_ids))
        for item in q["rubric"]:
            assert item["text"].strip()
            hb.auto_check(item, "")  # raises on an unknown check


def test_the_campaign_profile_passes():
    text = (BENCH / "campaign" / "_meta" / "table-keeper-profile.md").read_text(encoding="utf-8")
    assert pc.check_text(text) == []


def test_the_campaign_passes_schema_validation():
    done = subprocess.run([sys.executable, str(ROOT / "scripts" / "validate_schema.py"),
                           str(BENCH / "campaign")], cwd=ROOT,
                          capture_output=True, text=True)
    assert done.returncode == 0, done.stdout + done.stderr


def test_the_campaign_passes_the_version_gate(tmp_path):
    import shutil
    vault = tmp_path / "campaign"
    shutil.copytree(BENCH / "campaign", vault)
    done = subprocess.run([sys.executable, str(ROOT / "skills" / "shared" / "scripts" / "gma.py"),
                           "vault-check", str(vault), "version"], cwd=ROOT,
                          capture_output=True, text=True)
    rows = [ln for ln in done.stdout.splitlines() if ln and not ln.startswith("#")]
    assert rows, done.stdout + done.stderr
    # MISMATCH is fine after an upstream merge: the skills update the vault and go on.
    assert rows[0].split("\t")[0] in {"OK", "MISMATCH"}, rows[0]


def test_prepare_refuses_an_existing_run(tmp_path):
    import pytest
    questions = [{"id": "Q1", "skill": "session-prep", "prompt": "p", "rubric": []}]
    hb.prepare(tmp_path / "run", questions, seed=1)
    with pytest.raises(FileExistsError):
        hb.prepare(tmp_path / "run", questions, seed=2)


def test_auto_checks():
    dash = {"id": "d", "text": "t", "check": "no_em_dash"}
    assert hb.auto_check(dash, "plain - text") is True
    assert hb.auto_check(dash, "a — b") is False
    present = {"id": "p", "text": "t", "check": "present", "pattern": "2,?500"}
    assert hb.auto_check(present, "High 2,500") is True
    assert hb.auto_check(present, "High 2,000") is False
    assert hb.auto_check({"id": "j", "text": "t", "check": "judge"}, "x") is None


def test_prepare_score_and_unblind(tmp_path, monkeypatch):
    questions = [{"id": "Q1", "skill": "session-prep", "prompt": "p", "rubric": [
        {"id": "no-em-dash", "text": "t", "check": "no_em_dash"},
        {"id": "judged", "text": "t", "check": "judge"}]}]
    run = tmp_path / "run"
    key = hb.prepare(run, questions, seed=1)
    x_arm = key["Q1"]["X"]
    (run / "responses" / "Q1-X.md").write_text("clean answer", encoding="utf-8")
    (run / "responses" / "Q1-Y.md").write_text("dash — answer", encoding="utf-8")
    (run / "judgments.json").write_text(json.dumps(
        {"Q1": {"judged": {"X": True, "Y": False}}}), encoding="utf-8")
    res = hb.score(run, questions)
    y_arm = key["Q1"]["Y"]
    assert res["Q1"]["totals"][x_arm] == (2, 2)
    assert res["Q1"]["totals"][y_arm] == (0, 2)
    md = hb.summary_md(res, "run")
    assert "| **All** |" in md
