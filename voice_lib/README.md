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

## Delhi Rain film (Nov 12 2026), tag `delhirain_film`
148 clips (74 EN + 74 TE), one take per script line, narrator only (Sandeep clones), eleven_v4.
Extra fields: `speaker`, `line` (film script line number in `videos/2026-11-15_long_delhi_make_it_rain/production_brief.md`), `delivery` (light tag used, if any), `dur`, `tts_prompt` (exact text sent, with numbers spelled out).
Reuse in the six Delhi Rain Shorts: filter by `tag == "delhirain_film"` and `line`, per the film-to-Short reuse matrix in the brief.
- **EN 6.0 retake (Nov 12, user-approved):** take 1 said "Dehi". Take 2 (`active: true`, `take: 2`) is the one to use; take 1 stays in the library with `active: false` and a SUPERSEDED note. When two entries share the same text, use the one with `active: true`.
