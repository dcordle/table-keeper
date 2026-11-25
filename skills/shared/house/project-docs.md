# Project-docs mode

Use this when the profile's `Record` is `project docs`: the campaign's
record is a claude.ai Project's docs, read and written with the Projects
tool, and there is no vault.

## What to skip

Skip all of the original skills' vault machinery: the version gate, every
`gma` command, `vault-write` and `session-new`, `_meta/` files, chapter
and scene folders, frontmatter, canon status, wiki-links, entity filing
through campaign-organizer, and picture steps. Never ask for a vault path.
Skip the reference files that only describe the vault (`vault-access.md`,
`vault-structure.md`, `entity-schema.md`, `canon-status.md`,
`session-document-chain.md`, `reconcile.md`).

## Reading the record

- Read the profile first, then the docs its `Key docs` field names, with
  `project_read`. Use `project_search` to find anything else.
- Read the doc before stating a rule, number, name or state from it.
  Never quote a rule or number from memory.
- The campaign's own Project instructions and docs win over the skills.
  When two docs disagree, say which and follow the campaign's own order
  of sources if it has one.

## Each skill

- **session-prep:** build the session from the campaign's own template doc
  when it has one, and follow `prep-core.md`. To pick up from the last
  session, read the latest entry in the campaign's session log doc.
  Deliver the prep in chat, and write it as a doc only when the GM asks.
- **session-play:** answer from `project_search`, short and fast. Write
  nothing.
- **session-wrapup:** from notes or a transcript, give the recap, then run
  the after-session order in `prep-core.md`, naming the doc each change
  belongs in. Show the doc changes in chat and write them once the GM
  confirms.
- **campaign-qa:** run the checks by reading docs: contradictions between
  docs, three clues per fact the crew must learn, names too alike, state
  labels with no visible effect, and lines a later decision replaced.
  Report each finding with its doc, and fix only what the GM approves.
  The graph and vault checks do not apply.
- **ttrpg-expert:** works as usual. House rules come from the campaign's
  docs, not the vault's campaign overview.
- **the-midwife:** gives the brief in chat, or as a doc when asked.
- **campaign-organizer, vault-ingest, publish-site:** these work on vaults.
  Say so, and offer the nearest Project-docs step: an index doc of the
  record, or turning uploaded files into new docs once the GM approves.

## Writing back

- Docs hold settled decisions only. Proposals stay in chat until the GM
  settles them. Put no process notes, audit trails or change logs inside
  a doc.
- Before each `project_write`, read the doc fresh, change only what was
  settled, and write the whole doc back. One doc per write.
