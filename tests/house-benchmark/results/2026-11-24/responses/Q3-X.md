# Old Ma Tessaly, for The Bell Under the Water

Her vault note gives a role, one want and one secret, but leaves out who cut the rope. I filled that and a few other gaps myself (no one was here to ask). Everything new below is DRAFT until you confirm it.

**Calls I made:**

- **Who cut the rope: Sister Wren**, forty years ago, when she and Tessaly were girls. Wren was a young Reedwife then, and the coven cut the rope so nobody could ring the bell and wake the parish's fresh dead. This uses an existing NPC and makes Tessaly's secret proof that the coven knows ringing wakes the drowned, which is the opposite of what it tells people. If you'd rather keep Wren out of it, use "the Reedwives' eldest of that year, long dead" instead. Her other lines still work.
- **Her grandson is Tobin**, about fifteen. He's the punt-boy who came back on Tuesday. He's a new name.
- **Coven clock:** the Reedwives bought rope in Session 2 (step 1 of 2). The next step is the diving bell, and they want Tobin to pole it out. So in this job, the coven is about to take that step. Nothing here moves the clock; a completed session does that.
- **Stats:** Commoner as written (SRD 5.2). She's a talker, not a fighter.

Ready to file over `NPCs/Old Ma Tessaly.md` once you approve. campaign-organizer can file it, and campaign-qa can check it after.

---

```markdown
---
name: "Old Ma Tessaly"
type: npc
canon_status: DRAFT
createdSession: "Session 2"
asOfSession: "Session 2"
lastUpdated: "Session 2"
aliases:
  - "Ma Tessaly"
  - "the eel-seller"
gm_aliases: []
tags: []
occupation: "eel-seller"
age: 62
gender: "female"
status: alive
location: "[[Market Stair]]"
relationships:
  - target: "[[Market Stair]]"
    type: located_at
    tone: friendly
    strength: 8
    bidirectional: false
    description: "Has kept the same eel stall on the stair for forty years"
  - target: "[[Tobin]]"
    type: family
    tone: friendly
    strength: 10
    bidirectional: true
    description: "Her grandson; punts for the Reedwives"
  - target: "[[The Reedwives]]"
    type: wary_of
    tone: hostile
    strength: 6
    bidirectional: false
    description: "They employ her grandson; she wants him out"
  - target: "[[Drowned Chapel]]"
    type: knows
    tone: hostile
    strength: 8
    bidirectional: false
    description: "Was a girl in its parish the night it sank"
  - target: "[[Sister Wren]]"
    type: knows
    tone: hostile
    strength: 9
    bidirectional: false
    gm_only: true
    description: "Saw Wren cut the bell rope the night the chapel sank"
---

## Overview

Ma Tessaly sells eels at the Market Stair, live in a tub or smoked on a string. She grew up in the parish that sank with the chapel, and she is the one who told the crew the bell had started ringing again. Nobody asked her.

## Appearance & Manner

She's small and broad, with forearms like rope and a leather apron gone black with eel slime. She talks while she guts, and she never looks down at the knife.

## History

She was a girl in the chapel's parish before it sank, forty years ago. Her family moved up onto the stair after, and she's sold eels there ever since.

## Related

- **People:** [[Tobin]]: her grandson, a punt-boy
- **Places:** [[Market Stair]]: her stall; [[Drowned Chapel]]: her old parish
- **Groups:** [[The Reedwives]]: Tobin punts for them, and she doesn't like it

## Campaign Log

- **[[Session 02 - The Toll Ledger]]**: sold Mira and Ivy eels and told them, unasked, that the chapel bell was ringing again.

<!-- gm-only -->

## GM Notes

### Stats

**Old Ma Tessaly** (Commoner, SRD 5.2, as written)
*Medium Humanoid*

**AC** 10 · **Initiative** +0 (10) · **HP** 4 (1d8) · **Speed** 30 ft.

|     | Score | Mod | Save |
|-----|-------|-----|------|
| STR | 10 | +0 | +0 |
| DEX | 10 | +0 | +0 |
| CON | 10 | +0 | +0 |
| INT | 10 | +0 | +0 |
| WIS | 10 | +0 | +0 |
| CHA | 10 | +0 | +0 |

**Senses** Passive Perception 10 · **Languages** Common
**CR** 0 (XP 0; PB +2)

**Actions**
- ***Club (her eel-maul).*** *Melee Attack Roll:* +2, reach 5 ft. *Hit:* 2 (1d4) bludgeoning damage.

**Tactics:** She doesn't fight. If steel comes out, she shouts for the stair, and the eel families come. They still resent the Tollgate men over the market fire.

### Playing Them

- **Speech:** Marsh-flat and quick. She answers a question with a price ("That's a smoked one's worth of asking") and calls everyone "duck."
- **Tell:** She slaps the gutting board flat with her palm before she says anything true.
- **Line:** "Bell's ringing, duck. No rope on it forty years, and it's ringing. You buying or gawping?"

### Wants

She wants Tobin kept away from the chapel. He came back alone on Tuesday, white as a fish belly and not talking, and the coven has already asked him to go back out. If the crew takes the job, she's on their side, as long as their plan doesn't put Tobin in the punt.

### Knows

**Will share** for the price of buying eels and listening. She gives these freely:

- The bell rang the night the chapel sank. It rang while the water came in, and then it stopped short. "Like someone took its tongue."
- The way out: down the Reedwater, keep the dead willow on your left, and stop when the reeds go grey. The tower roof shows at low water.
- Tobin went out Tuesday with the Hask boy. Only Tobin came back. He said the bell was ringing *under him*, and that there were people standing in the water.
- Sister Wren bought new rope off the chandler last week. "Forty fathom. Nobody needs forty fathom of rope in a marsh. You'd only need that to reach something deep."

**Will share for a promise** to keep Tobin off the water, or once the crew has actually done it:

- The coven wants Tobin to pole something heavy out to the chapel at the new moon. She thinks it's the diving bell from the salvage yard.
- The bell rope didn't rot. It was cut, on purpose, the night the chapel sank. She saw it happen.

**Hides:** who cut it. See Secrets.

**What makes her say the name** (any one of these):

- The crew brings Tobin home, or keeps him safely off the coven's punt. Ask no roll.
- The crew shows her the coven means to ring the bell (the rope, the diving bell, Wren's own words). Persuasion or Insight-led talk, DC 13.
- Threats and bribes don't work. Insight DC 10 tells the crew she's holding back out of fear, not greed.

### Under Pressure

She bargains. Push her with threats and she goes quiet and loud at once: she stops talking to you and starts talking to the whole stair about you. Show her real care for Tobin and she gives up everything.

### Hidden Ties

- [[Sister Wren]]: they were girls together. Tessaly watched Wren cut the bell rope with a reed-knife from the belfry ladder as the water came in. Neither has spoken of it since. Wren knows Tessaly saw.

### Secrets

- **Surface:** She's frightened for Tobin, and it shows under the patter.
- **Investigation:** The rope was cut, not rotted, so the bell couldn't be rung again.
- **Deep:** **Sister Wren cut it.** Forty years ago the coven cut the rope so nobody could ring the bell and wake the parish's drowned. Now Wren buys rope and wants it rung "to lay them to rest." Anyone who hears this has proof that the coven knows what ringing really does.

### At the Table (this job)

- **Where:** her stall on the Market Stair, which the crew passes on the way from the Ferryhouse to the Reedwater. The Stair is Quiet, so travel matters little here.
- **First move for a new player:** buy an eel and ask about the bell. That alone gets them the way out and Tobin's story.
- **A non-combat ending she makes possible:** with her name for the rope-cutter, the crew can face Sister Wren in front of the eel families on the Stair. Session 1's crew shamed Sergeant Dace the same way. If the families learn the coven cut the rope once to keep the dead asleep, the coven loses its punt-boys, and the new-moon ringing has no one to pole it out. That works even if whatever is ringing the bell survives.
- **Hopeful beat:** if Tobin's safe at the debrief, Ma Tessaly sends a string of smoked eels up to the Ferryhouse for the crew, with Tobin carrying them.
- **Faces they know:** Ivy has met her twice, and Mira once. She remembers anyone who's bought from her, and she's warm to anyone who stood up to the Tollgate men at the market fire.
```
