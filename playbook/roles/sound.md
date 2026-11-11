# Role: Sound designer

**Inputs:** the scene sheet, `sfx/catalog.json` and the user's topic-specific uploads.
**Responsibilities:** SFX events, ambience and the sound requests in the resource list.
**Outputs:** the SFX column of the scene sheet and the sound list in the resource request.

## Rules
- **[SD-01]** (P, user Oct 2026) Use real recorded sounds only. No generated or AI SFX, no hissy whooshes or risers, and no "kids' video" pings, bells, sparkles or pops.
- **[SD-02]** (P, user Oct 2026) Sound follows what happens on screen (graphics, cards, maps), never the spoken words: no literal ambience such as trees for "Jammi" or an elephant for "Mysuru".
- **[SD-03]** (C, user Oct 2026) Variety, one sound per job: a real tap or click where a button is tapped, a beat with an effect at a new chapter. Don't sound every movement; vary the sound families.
- **[SD-04]** (P, CLAUDE.md) `sfx/catalog.json` is the inventory, giving each sound's role and hit point. Ask the user for topic-specific extras in the visuals list; he uploads them to `sfx/`.
- **[SD-05]** (C, playbook) Ambience is only faint real ambience under real event footage, never in the explaining parts. Reject recordings with modern gunfire, intelligible modern speech or engine hum.

## Checklist
1. Every sound is in the catalog or was uploaded by the user (→ SD-01, SD-04).
2. Each event is tied to an on-screen action (→ SD-02).
3. No sound family repeats monotonously (→ SD-03).
4. SFX stay under the voice.
5. A listening check was made (→ QC-04).
6. Each sound file is aligned on its catalog hit point.

**Wanted (still missing from `sfx/`):** the exact highlighter sound (Pixabay 385295) and a real sub drop.

**Failure conditions:** a synthetic sound; literal sound for words; SFX masking the voice.
**Handoff:** SFX events go to the editor's mix.

Methods: `../methods/audio.md`.
