"""table-keeper's house layer: hooks, plugin name and override anchors.

Run: python3 -m pytest tests/test_house_layer.py -q
"""
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location(
    "house_check", ROOT / "scripts" / "house_check.py")
hc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(hc)

HOOK = hc.load_config()["hook"]
SKILL = "---\nname: x\ndescription: y\n---\n\nBody line.\n"


def test_the_repo_house_layer_is_whole():
    assert hc.check() == []


def test_apply_hook_puts_one_hook_at_the_end():
    out = hc.apply_hook(SKILL, HOOK)
    assert hc.hook_problem(out, HOOK) is None
    assert out.count(HOOK) == 1
    assert out.startswith(SKILL.rstrip("\n"))
    assert out.endswith(HOOK + "\n")


def test_apply_hook_is_stable():
    once = hc.apply_hook(SKILL, HOOK)
    assert hc.apply_hook(once, HOOK) == once


def test_apply_hook_moves_a_misplaced_hook():
    moved = SKILL.replace("Body line.", f"{HOOK}\n\nBody line.")
    assert hc.hook_problem(moved, HOOK) is not None
    assert hc.hook_problem(hc.apply_hook(moved, HOOK), HOOK) is None


def test_a_missing_hook_is_reported():
    assert hc.hook_problem(SKILL, HOOK) == "hook missing"


def test_a_changed_anchor_is_reported(tmp_path):
    import shutil
    for rel in ["skills", ".claude-plugin"]:
        shutil.copytree(ROOT / rel, tmp_path / rel)
    rule = hc.load_config()["overrides"][0]
    target = tmp_path / rule["file"]
    target.write_text(target.read_text(encoding="utf-8")
                      .replace(rule["anchor"], "Rewritten upstream."),
                      encoding="utf-8")
    problems = hc.check(tmp_path)
    assert any("upstream changed" in p for p in problems)
