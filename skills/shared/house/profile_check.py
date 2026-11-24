#!/usr/bin/env python3
"""Check a table-keeper campaign profile against the format in profile.md.

Run: python3 profile_check.py <profile.md>
Prints each problem and exits 1, or prints "Profile OK." and exits 0.
"""

import re
import sys
from pathlib import Path

FIELD = re.compile(r"^\s*-\s+\*\*(?P<name>[^*]+?):\*\*\s*(?P<value>.*?)\s*$")
BAND_PART = re.compile(
    r"^(?P<op>>=|<=|>|<)\s*(?:(?P<mult>\d+(?:\.\d+)?)x\s+)?(?P<budget>Low|Moderate|High)$",
    re.I)

# section -> {field: (required, check)}; check is a set of allowed values,
# a function returning an error or None, or None for free text.


def _whole(value: str) -> str | None:
    return None if re.fullmatch(r"\d+", value) and int(value) > 0 else \
        "must be a whole number above 0"


def _whole0(value: str) -> str | None:
    return None if re.fullmatch(r"\d+", value) else "must be a whole number"


def _hours(value: str) -> str | None:
    return None if re.fullmatch(r"\d+(\.\d+)?( to \d+(\.\d+)?)?", value) else \
        "must be hours, such as '3 to 4' or '2'"


def band_error(value: str) -> str | None:
    if value.lower() == "judgment":
        return None
    parts = [p.strip() for p in re.split(r"\band\b", value, flags=re.I)]
    if not parts or any(not p for p in parts):
        return "must be 'judgment' or like '> Moderate and <= High' or '>= 1.5x High'"
    for p in parts:
        if not BAND_PART.match(p):
            return f"'{p}' is not like '> Moderate' or '>= 1.5x High'"
    return None


def _other(value: str) -> str | None:
    return None if value.lower() == "unconstrained" else band_error(value)


def _hp(value: str) -> str | None:
    if value.lower() in {"as written", "average", "max"}:
        return None
    m = re.fullmatch(r"(\d+)%", value)
    if m and 0 < int(m.group(1)) <= 100:
        return None
    return "must be 'as written', 'average', 'max' or a percentage like '75%'"


SPEC = {
    "Table": {
        "Format": (True, {"open table", "drop-in", "steady party"}),
        "Session length": (True, _hours),
        "Party size for budgets": (True, _whole),
        "Story center": (True, {"world", "characters"}),
        "Session unit": (True, None),
        "Start and end": (False, None),
    },
    "Encounters": {
        "Main fight band": (True, band_error),
        "Other fights": (True, _other),
        "Monster hit points": (True, _hp),
        "Boss standard": (False, None),
        "Risk note": (True, {"yes", "no"}),
    },
    "Travel": {
        "Travel": (True, {"cut", "nodes", "hexes", "pointcrawl"}),
        "Travel complications": (False, None),
    },
    "Prep": {
        "Plan style": (True, {"bullets", "table-ready"}),
        "Rumors per session": (True, _whole0),
        "World taste": (True, {"yes", "no"}),
        "Archive clues": (False, None),
        "Required elements": (False, None),
    },
    "Record": {
        "Record": (True, {"project docs", "vault"}),
        "Where": (True, None),
        "Key docs": (False, None),
    },
    "Voice": {
        "Player-facing voice": (True, None),
        "GM voice": (True, None),
    },
}
OPTIONAL_SECTIONS = {"Overrides"}


def parse(text: str) -> tuple[str | None, dict[str, dict[str, str]]]:
    """The title and {section: {field: value}}."""
    title, sections, current = None, {}, None
    for line in text.splitlines():
        if line.startswith("# ") and title is None:
            title = line[2:].strip()
        elif line.startswith("## "):
            current = line[3:].strip()
            sections.setdefault(current, {})
        elif current is not None:
            m = FIELD.match(line)
            if m:
                sections[current][m.group("name").strip()] = m.group("value")
    return title, sections


def check_text(text: str) -> list[str]:
    title, sections = parse(text)
    problems = []
    if not title or not title.startswith("Table-Keeper Profile:") or \
            not title.split(":", 1)[1].strip():
        problems.append("title must be '# Table-Keeper Profile: <campaign name>'")
    for section, fields in SPEC.items():
        if section not in sections:
            problems.append(f"missing section '## {section}'")
            continue
        got = sections[section]
        for name, (required, rule) in fields.items():
            value = got.get(name)
            if value is None or not value.strip():
                if required:
                    problems.append(f"{section}: missing field '{name}'")
                continue
            if isinstance(rule, set):
                if value.lower() not in rule:
                    allowed = ", ".join(sorted(rule))
                    problems.append(f"{section}: '{name}' is '{value}', "
                                    f"must be one of: {allowed}")
            elif rule is not None:
                err = rule(value)
                if err:
                    problems.append(f"{section}: '{name}' {err}")
        for name in sorted(set(got) - set(fields)):
            problems.append(f"{section}: unknown field '{name}'")
    for section in sorted(set(sections) - set(SPEC) - OPTIONAL_SECTIONS):
        problems.append(f"unknown section '## {section}'")
    return problems


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__.strip().splitlines()[2])
        return 2
    problems = check_text(Path(argv[1]).read_text(encoding="utf-8"))
    for p in problems:
        print(f"PROBLEM: {p}")
    if not problems:
        print("Profile OK.")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
