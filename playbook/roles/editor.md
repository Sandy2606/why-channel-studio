# Role: Editor (voice, captions, mix, render)

**Inputs:** the approved script, the generated voice, the scene code, and the music and sound cue sheets.
**Responsibilities:** voice edit, timing, captions, mix, render and exports.
**Outputs:** four files per Short (→ FMT-09); per-line voice clips; `voice_lib` entries.

## Rules
- **[ED-01]** (P, user Oct 24–25) Give the audio a professional edit: remove silences and noises. Shorts get a tight, engaging pace. Long films use the Why? Pace Model v2 (user-approved Oct 25) and never the Shorts squeeze. Never use even 0.5 s pauses after every sentence.
- **[ED-02]** (P, user Oct 30) Information lines and branding lines run a little faster; the Subscribe/Follow line itself runs at regular pace.
- **[ED-03]** (P, playbook) Loudness is −14 LUFS integrated, with true peak at −1 dB or lower. The voice stays clearly above music and SFX.
- **[ED-04]** (P, playbook) Verify every Telugu line with the te_med model; generic Whisper is not reliable on Telugu. English captions align the exact script text to Whisper word times; never patch Whisper's spelling word by word.
- **[ED-05]** (P, playbook) Anchor scenes to spoken phrases, not to fixed times.

## Checklist
1. Runtime is measured after the standard edit, with margin, under 3:00 (→ FMT-01).
2. Pauses follow ED-01 and ED-02.
3. Captions are exact and in their lane (→ LAY-02).
4. Loudness and peak meet ED-03.
5. Telugu has been verified (→ ED-04).
6. Four exports, same body (→ FMT-09).
7. Reusable lines are saved to `voice_lib` (→ CR-03).

**Failure conditions:** over-squeezed long-form audio; caption text that differs from the script; missing exports.
**Handoff:** the files go to QC.

Methods (Pace Model numbers, Whisper windows, render, gotchas, measured credit rates): `../methods/editing.md`.
