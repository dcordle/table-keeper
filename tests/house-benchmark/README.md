# House benchmark

Compares table-keeper against the original gm-apprentice skills on a small
D&D 2024 open-table campaign, so a house rule counts as better only when it
scores better.

- `campaign/` is the Grey Ferry, an original marsh-town open table with a
  table-keeper profile in `_meta/`, two played sessions and a job board. Its
  monsters come from the SRD.
- `questions.json` holds six questions and the rubric for each. A `judge`
  item is scored by a blind evaluator; every other item is scored by
  `scripts/house_bench_score.py`.
- `results/<run>/` holds one run: the key, the blinded responses, the
  evaluator's verdicts and `summary.md`.

## Running it

1. Prepare the run. This writes a random key that says, for each question,
   which arm answers as X and which as Y.

   ```text
   python3 scripts/house_bench_score.py --prepare <run>
   ```

2. Set up the two arms. The original arm is the upstream commit that main
   was last merged from, checked out on its own:

   ```text
   git worktree add /tmp/original <upstream commit>
   ```

   The table-keeper arm is this repository's main branch. Both arms read the
   same campaign folder in this repository.

3. Answer each question once per arm, each in a fresh session that sees only
   its own arm's skills. Tell it to read `skills/<skill>/SKILL.md` in its arm
   and follow it, give it the question's prompt and the campaign path, and
   have it write only its answer to `results/<run>/responses/<Q>-<label>.md`
   under the label the key gives that arm. It never sees the rubric, the key
   or the other arm.

4. Judge. A fresh evaluator gets the `judge` items from `questions.json` and
   both responses for each question, labeled X and Y, with no key. It writes
   `results/<run>/judgments.json` as
   `{"Q1": {"<item id>": {"X": true, "Y": false}}}`.

5. Score and unblind:

   ```text
   python3 scripts/house_bench_score.py --score <run>
   ```

   `summary.md` gives each arm's passed items per question and in total, then
   the item-by-item table. Read the responses too: a count alone does not show
   which answer is more usable at the table.
