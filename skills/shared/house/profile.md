# Campaign profile

A profile holds one campaign's numbers and habits, so the house rules and
the prep core fit that game. It lives with the campaign, never in this
repository:

- In a claude.ai Project: a doc named `Table-Keeper Profile`.
- In a vault: `table-keeper-profile.md` in the `_meta` folder, or in the
  vault's own meta folder when it uses another name.

When a profile and the campaign's own documents disagree, the campaign's
documents win, and the GM is told which profile line to fix. With no
profile, `profile-template.md` is the profile, and the GM is told so once.

Check a profile file with
`python3 "<shared>/house/profile_check.py" <path to profile>`.

## Format

The title is `# Table-Keeper Profile: <campaign name>`. Each section below
is a `##` heading, and each field is a bullet written
`- **Field:** value`. Fields marked *optional* may be left out. Anything
else in the doc is ignored by the checker, so a GM can add notes.

### Table

- **Format:** `open table`, `drop-in` or `steady party`.
- **Session length:** hours, such as `3 to 4` or `2`.
- **Party size for budgets:** a whole number. Default 5.
- **Story center:** `world` (the job and the world are the story; personal
  plots are optional scenes) or `characters` (player characters' arcs lead).
- **Creative lead:** *optional*. `gm` (the default: the GM settles the
  premise, scenes and truths, and prep parks the rest as open questions)
  or `shared` (prep drafts it all, labels reversible assumptions, and
  asks only when an answer would change the design).
- **Session unit:** what one session's prep is called, such as `dispatch`
  or `session`. It stands in for the original skills' chapter and session
  where they file prep.
- **Start and end:** *optional*. Where every session starts and ends, such
  as `the Society safehouse`.

### Encounters

- **Main fight band:** written with `>`, `>=`, `<` or `<=`, an optional
  multiplier, and a 2024 budget name (`Low`, `Moderate`, `High`), joined by
  `and`, or `judgment` when the campaign sets no fixed band. Examples:
  `> Moderate and <= High`, `>= 1.5x High`, `judgment`. With `judgment`,
  still give the XP against the 2024 budgets and the swinginess flags, and
  leave the call to the GM.
- **Other fights:** `unconstrained` or a band written the same way.
- **Monster hit points:** `as written`, `average`, `max`, or a percentage
  of the most the hit dice can roll, such as `75%`.
- **Boss standard:** *optional*. Free text, such as legendary resistances,
  legendary and lair actions, minion count.
- **Risk note:** `yes` to give one line on how the main fight plays at the
  lowest and highest eligible level, `no` otherwise.

### Travel

- **Travel:** `cut` (travel is skipped unless it matters), `nodes` (a route
  through named map nodes with danger words), `hexes` or `pointcrawl`.
- **Travel complications:** *optional*. When they are rolled, such as
  `only when travel matters, never homeward`.

### Prep

- **Plan style:** `bullets` (the original skills' style) or `table-ready`
  (read-aloud where it fits, NPC blocks, DCs written in the scene).
- **Rumors per session:** a whole number, 0 for none.
- **World taste:** `yes` for a few sentences on the world before the
  briefing, `no` otherwise.
- **Archive clues:** *optional*. How many optional larger-mystery clues a
  session may carry, such as `up to 1`.
- **Required elements:** *optional*. A comma list of what every session
  needs, such as `one combat, a hopeful beat, a non-combat ending`.

### Record

- **Record:** `project docs` or `vault`.
- **Where:** the Project name or the vault folder.
- **Key docs:** *optional*. A comma list of the docs that hold the rules,
  such as `Design Document, Campaign Brief`.

### Voice

- **Player-facing voice:** free text, such as the skill or style to use.
- **GM voice:** free text.

### Overrides

*Optional section.* Bullets of house rules this campaign changes, each
naming the house rule and the campaign's version. Example:
`- **The world:** faction turns also run after each play-by-post week.`
