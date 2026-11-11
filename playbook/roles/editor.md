# Role: Editor (voice, captions, mix, render)

**Inputs:** the approved script, the generated voice, the scene code, and the music and sound cue sheets.
**Responsibilities:** voice edit, timing, captions, mix, render and exports.
**Outputs:** four files per Short (→ FMT-09); per-line voice clips; `voice_lib` entries.

## Rules
- **[ED-01]** (P, v2 user Oct 24–25 and Nov 10) Give the audio a professional edit that removes silences and noises. Long films never get the Shorts squeeze or uniform 0.5 s pauses after every sentence. The Why? Pace Model v2 (user-approved Oct 25) is the preferred long-form method; its numbers are in `methods/editing.md`.
- **[ED-02]** (C, v2 user Oct 30 and Nov 10) Line pacing is an editing judgment. Usual practice: information and branding lines run a little faster, and the Subscribe/Follow line runs at regular pace.
- **[ED-03]** (P, playbook) Loudness is −14 LUFS integrated, with true peak at −1 dB or lower. The voice stays clearly above music and SFX.
- **[ED-04]** (P, playbook) Verify every Telugu line with the te_med model; generic Whisper is not reliable on Telugu. English captions align the exact script text to Whisper word times; never patch Whisper's spelling word by word.
- **[ED-05]** (C, v2 user Nov 10) Phrase-anchored scene timing (scenes tied to spoken phrases, not fixed times) is the preferred editing method; it is not a universal pass/fail rule.

## Checklist
1. Runtime is measured after the standard edit, with margin, under 3:00 (→ FMT-01).
2. Pauses follow ED-01 and ED-02.
3. Captions are exact and readable, and cover no essential information (→ LAY-02).
4. Loudness and peak meet ED-03.
5. Telugu has been verified (→ ED-04).
6. Four exports, same body (→ FMT-09).
7. Reusable lines are saved to `voice_lib` (→ CR-03).

**Failure conditions:** over-squeezed long-form audio; caption text that differs from the script; missing exports.
**Handoff:** the files go to QC.

Methods (Pace Model numbers, Whisper windows, render, gotchas, measured credit rates): `../methods/editing.md`.
