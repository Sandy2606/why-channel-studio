# Voice line library (ElevenLabs clones only)
- `index.json`: one entry per generated line — lang, exact text, file, voice, model, source video, tag (`cta` = reusable ending lines).
- Before any ElevenLabs generation: normalise each script line (trim, collapse spaces) and look it up by exact text + lang. Reuse matches; generate only the rest.
- Reuse at **whole sentence / phrase level only** — never splice single words (intonation sounds stitched).
- Generate per line (same credit cost) so every line is saved as its own clip; add new lines to the index after each video.
- Only clone voices (Sandeep English / Sandeep Telugu) go here, never the user's own recordings (tone differs).
