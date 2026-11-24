#!/usr/bin/env python3
"""Score a table-keeper house benchmark run: original gm-apprentice vs table-keeper.

A run folder holds, for each question, two blinded responses and the
evaluator's verdicts:

  tests/house-benchmark/results/<run>/
    key.json              which label (X or Y) is which arm, per question
    responses/Q1-X.md     one response per question and label
    judgments.json        {"Q1": {"<item id>": {"X": true, "Y": false}}}

`--prepare <run>` makes the folder and a random key. Responses are then
written by the two arms under the labels the key gives them, and the blind
evaluator fills judgments.json for the `judge` items without seeing the key.
`--score <run>` runs the automatic checks, unblinds and writes summary.md.

Run: python3 scripts/house_bench_score.py --prepare 2026-11-24
     python3 scripts/house_bench_score.py --score 2026-11-24
"""

import argparse
import json
import random
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BENCH = ROOT / "tests" / "house-benchmark"
ARMS = ("original", "table-keeper")
EM_DASH = "—"


def load_questions(bench: Path = BENCH) -> list[dict]:
    return json.loads((bench / "questions.json").read_text(encoding="utf-8"))["questions"]


def auto_check(item: dict, text: str) -> bool | None:
    """The automatic verdict for one rubric item, or None for a judge item."""
    kind = item["check"]
    if kind == "no_em_dash":
        return EM_DASH not in text
    if kind == "absent":
        return re.search(item["pattern"], text) is None
    if kind == "present":
        return re.search(item["pattern"], text) is not None
    if kind == "judge":
        return None
    raise ValueError(f"unknown check {kind!r} on item {item['id']}")


def prepare(run_dir: Path, questions: list[dict], seed: int | None = None) -> dict:
    rng = random.Random(seed)
    key = {}
    for q in questions:
        arms = list(ARMS)
        rng.shuffle(arms)
        key[q["id"]] = {"X": arms[0], "Y": arms[1]}
    (run_dir / "responses").mkdir(parents=True, exist_ok=True)
    (run_dir / "key.json").write_text(json.dumps(key, indent=2) + "\n", encoding="utf-8")
    return key


def score(run_dir: Path, questions: list[dict]) -> dict:
    """{qid: {"items": [(id, text, {arm: verdict})], "totals": {arm: (passed, scored)}}}"""
    key = json.loads((run_dir / "key.json").read_text(encoding="utf-8"))
    jpath = run_dir / "judgments.json"
    judged = json.loads(jpath.read_text(encoding="utf-8")) if jpath.is_file() else {}
    out = {}
    for q in questions:
        qid = q["id"]
        texts = {}
        for label in ("X", "Y"):
            path = run_dir / "responses" / f"{qid}-{label}.md"
            texts[label] = path.read_text(encoding="utf-8") if path.is_file() else None
        rows, totals = [], {arm: [0, 0] for arm in ARMS}
        for item in q["rubric"]:
            verdicts = {}
            for label, arm in key[qid].items():
                if texts[label] is None:
                    verdicts[arm] = None
                    continue
                v = auto_check(item, texts[label])
                if v is None:
                    v = judged.get(qid, {}).get(item["id"], {}).get(label)
                verdicts[arm] = v
                if v is not None:
                    totals[arm][1] += 1
                    totals[arm][0] += int(bool(v))
            rows.append((item["id"], item["text"], verdicts))
        out[qid] = {"items": rows, "totals": {a: tuple(t) for a, t in totals.items()}}
    return out


def _mark(v) -> str:
    return "-" if v is None else ("yes" if v else "no")


def summary_md(results: dict, run: str) -> str:
    lines = [f"# House benchmark: {run}", "",
             "| Question | original | table-keeper |", "|---|---|---|"]
    grand = {arm: [0, 0] for arm in ARMS}
    for qid, r in results.items():
        cells = []
        for arm in ARMS:
            p, n = r["totals"][arm]
            grand[arm][0] += p
            grand[arm][1] += n
            cells.append(f"{p}/{n}")
        lines.append(f"| {qid} | {cells[0]} | {cells[1]} |")
    lines.append(f"| **All** | {grand['original'][0]}/{grand['original'][1]} | "
                 f"{grand['table-keeper'][0]}/{grand['table-keeper'][1]} |")
    for qid, r in results.items():
        lines += ["", f"## {qid}", "", "| Item | original | table-keeper |", "|---|---|---|"]
        for iid, _text, v in r["items"]:
            lines.append(f"| {iid} | {_mark(v['original'])} | {_mark(v['table-keeper'])} |")
    lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--prepare", metavar="RUN")
    group.add_argument("--score", metavar="RUN")
    args = parser.parse_args(argv)
    questions = load_questions()
    run = args.prepare or args.score
    run_dir = BENCH / "results" / run
    if args.prepare:
        prepare(run_dir, questions)
        print(f"Prepared {run_dir.relative_to(ROOT)}")
        return 0
    text = summary_md(score(run_dir, questions), run)
    (run_dir / "summary.md").write_text(text, encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
