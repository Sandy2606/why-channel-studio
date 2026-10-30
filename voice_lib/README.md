# Voice line library (ElevenLabs clones only)
- `index.json`: one entry per generated line — lang, exact text, file, voice, model, source video, tag (`cta` = reusable ending lines).
- Before any ElevenLabs generation: normalise each script line (trim, collapse spaces) and look it up by exact text + lang. Reuse matches; generate only the rest.
- Reuse at **whole sentence / phrase level only** — never splice single words (intonation sounds stitched).
- Generate per line (same credit cost) so every line is saved as its own clip; add new lines to the index after each video.
- Only clone voices (Sandeep English / Sandeep Telugu) go here, never the user's own recordings (tone differs).

## Diwali Long (Nov 1 2026), tag `diwali_long`
162 clips (81 EN + 81 TE), one per script line, two speakers: ANNA (Sandeep clones) and CHELLI (Sowmya clones, subtle tags).
Extra fields: `speaker`, `line` (script line number), `delivery` (tag used), `dur` (seconds).
Reuse in the Diwali Shorts: filter `index.json` by `tag == "diwali_long"` and `line`. Line→file map: `videos/2026-11-01_long_diwali_explained/voice_takes.json`.
