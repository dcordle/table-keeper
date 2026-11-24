#!/usr/bin/env python3
"""Check table-keeper's house layer after a merge from upstream gm-apprentice.

It checks that:
- skills/shared/house/HOUSE.md exists;
- every skill holds the house hook once, as its last line;
- no skill is missing from the hooked list (a new upstream skill needs one);
- the plugin and marketplace carry the table-keeper name;
- the upstream text each house rule overrides is still there. When it is
  gone, upstream changed that section, and the rule needs a fresh look.

- the profile template passes the profile checker.

Run: python3 scripts/house_check.py            (report, exit 1 on a problem)
     python3 scripts/house_check.py --profile PATH  (also check a profile)
     python3 scripts/house_check.py --apply-hooks   (put missing hooks back)
"""

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HOUSE = ROOT / "skills" / "shared" / "house"
CONFIG = HOUSE / "overrides.json"


def load_config(root: Path = ROOT) -> dict:
    return json.loads((root / "skills" / "shared" / "house" / "overrides.json")
                      .read_text(encoding="utf-8"))


def frontmatter_end(lines: list[str]) -> int | None:
    """Index of the line that closes the frontmatter, or None."""
    if not lines or lines[0].strip() != "---":
        return None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return i
    return None


def hook_problem(text: str, hook: str) -> str | None:
    """What is wrong with a skill's hook, or None when it is right."""
    count = text.count(hook)
    if count > 1:
        return f"hook appears {count} times"
    if frontmatter_end(text.splitlines()) is None:
        return "no frontmatter found"
    if count == 0:
        return "hook missing"
    last = next((ln for ln in reversed(text.splitlines()) if ln.strip()), "")
    if last != hook:
        return "hook is not the last line of the file"
    return None


def apply_hook(text: str, hook: str) -> str:
    """The text with exactly one hook as its last line. The hook goes at
    the end so no upstream line moves: upstream tests pin some skill lines
    by number."""
    if frontmatter_end(text.splitlines()) is None:
        raise ValueError("no frontmatter found")
    lines = [ln for ln in text.split("\n") if ln != hook]
    body = "\n".join(lines).rstrip("\n")
    return f"{body}\n\n{hook}\n"


def squash(text: str) -> str:
    return re.sub(r"\s+", " ", text)


def check(root: Path = ROOT) -> list[str]:
    cfg = load_config(root)
    hook = cfg["hook"]
    problems = []

    if not (root / "skills" / "shared" / "house" / "HOUSE.md").is_file():
        problems.append("skills/shared/house/HOUSE.md is missing")

    found = sorted(p.parent.name for p in (root / "skills").glob("*/SKILL.md")
                   if p.parent.name != "shared")
    for name in sorted(set(found) - set(cfg["hooked_skills"])):
        problems.append(f"skills/{name}: new skill, add it to hooked_skills "
                        f"in overrides.json and run --apply-hooks")
    for name in cfg["hooked_skills"]:
        path = root / "skills" / name / "SKILL.md"
        if not path.is_file():
            problems.append(f"skills/{name}: listed in hooked_skills but gone")
            continue
        issue = hook_problem(path.read_text(encoding="utf-8"), hook)
        if issue:
            problems.append(f"skills/{name}/SKILL.md: {issue}")

    want = cfg["plugin_name"]
    plugin = json.loads((root / ".claude-plugin" / "plugin.json")
                        .read_text(encoding="utf-8"))
    market = json.loads((root / ".claude-plugin" / "marketplace.json")
                        .read_text(encoding="utf-8"))
    names = {"plugin.json name": plugin.get("name"),
             "marketplace.json name": market.get("name")}
    for i, entry in enumerate(market.get("plugins", [])):
        names[f"marketplace.json plugins[{i}].name"] = entry.get("name")
    for where, got in names.items():
        if got != want:
            problems.append(f".claude-plugin {where} is {got!r}, not {want!r}")

    for rule in cfg["overrides"]:
        path = root / rule["file"]
        if not path.is_file():
            problems.append(f"override '{rule['house_rule']}': {rule['file']} "
                            f"is gone upstream; review the rule")
        elif squash(rule["anchor"]) not in squash(path.read_text(encoding="utf-8")):
            problems.append(f"override '{rule['house_rule']}': upstream changed "
                            f"{rule['file']}; check the rule still fits, then "
                            f"update its anchor")
    template = root / "skills" / "shared" / "house" / "profile-template.md"
    if template.is_file():
        for issue in _profile_check(root).check_text(
                template.read_text(encoding="utf-8")):
            problems.append(f"profile-template.md: {issue}")
    else:
        problems.append("skills/shared/house/profile-template.md is missing")
    return problems


def _profile_check(root: Path = ROOT):
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "profile_check", root / "skills" / "shared" / "house" / "profile_check.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--apply-hooks", action="store_true",
                        help="put the hook back in every listed skill")
    parser.add_argument("--profile", metavar="PATH",
                        help="also check a campaign profile file")
    args = parser.parse_args(argv)
    if args.apply_hooks:
        cfg = load_config()
        for name in cfg["hooked_skills"]:
            path = ROOT / "skills" / name / "SKILL.md"
            text = path.read_text(encoding="utf-8")
            new = apply_hook(text, cfg["hook"])
            if new != text:
                path.write_text(new, encoding="utf-8")
                print(f"hooked skills/{name}/SKILL.md")
    problems = check()
    if args.profile:
        problems += [f"profile: {p}" for p in _profile_check().check_text(
            Path(args.profile).read_text(encoding="utf-8"))]
    for p in problems:
        print(f"PROBLEM: {p}")
    if not problems:
        print("House layer OK.")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
