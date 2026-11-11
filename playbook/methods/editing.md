# Methods: editing (voice, captions, render)

Method notes, not rules: they record how we currently do things and are updated by measuring and testing. Rules live in the owner files (see the master playbook). Copied from the pre-reorganisation playbook (tag `pre-pro-system`), with the original line numbers in brackets; superseded parts are left out and recorded in `history.md`.

## Voice edit [PB:173–204]
   - **English:** transcribe with faster-whisper small.en at 16 kHz.
   - **Telugu:** transcribe per phrase with the CT2 te_med model. For retake-heavy passages, do a fine pass: energy segments with a 0.12 s merge, then whisper per segment, to find exact boundaries.
   - Run whisper jobs sequentially; the machine has only 2 CPUs.
   - Pick the best take of each line. When pieces overlap, clamp each end to the next start. Mark hand-tuned boundaries 'raw'.
   - **Denoise, join and tighten:**
     - Denoise first.
     - **Shorts:** join pieces with 70 ms gaps, then compress pauses over 0.16 s to 0.10 s with crossfades.
     - **Long videos:** NEVER use the Shorts squeeze; it made the first long cut 204 wpm and the user said it sounded like reading. Use the **Why? Pace Model** (pacing.py + make_voice_v2.py, build_long) instead.
   - **Why? Pace Model v2 (long-form; user-approved Oct 25 2026). v1 at 159 wpm with 0.5 s sentence gaps felt slow ("can't watch it"); v2 uses a fast baseline with beats only where they work:**
     - Every piece gets a role, and the role sets the pause after it and how much internal pause is kept.
     - Fast roles: HOOK (whole intro up to "Let me explain"), TEASE (quick recaps), LIST (rapid-fire names and items, from story structure, never auto-detected), CTA. They get about 0.10–0.16 s gaps and internal pauses capped 0.16 → 0.10.
     - ASK (the mid-video subscribe ask) is warm and quick: about 0.2 s gaps.
     - EXPLAIN: 0.18 s after '.', 0.10 s after ',', 0.45 s after '?', and internal pauses capped 0.20 → 0.12.
     - QUESTION gets a 0.45–0.50 s beat before the answer, including questions in the middle of a line, where the internal pause is kept at ≥ 0.35 s.
     - PUNCH or reveal ("Power wasn't their problem", "A new beginning") gets a 0.50 s breath before it.
     - Every chapter start gets a 1.30 s pause before it, filled with a music dip, swell and boom.
     - Classify short lines by spoken duration, not word count (Telugu words are longer).
     - **Targets:** EN overall about 172–176 wpm; EXPLAIN parts about 170; fast parts about 180+; about 2 deliberate beats per minute. Telugu: the same roles, and about 1.3× the Shorts-cut length.
     - **Evidence:**
       - Popular YouTube speech is about 171 wpm median; top TED talks about 175.
       - Explainer and documentary narration is advised at about 135–160 wpm.
       - Deliberate pauses run 0.6–1.5 s; speakers speed up for interest and slow down for weight.
       - Calibrated to the narrator's raw pauses: '.' 0.6 s, ',' 0.4 s, '?' 0.66 s.
   - **Chain:** de-esser, then pedalboard EQ, two compressors and a limiter. Finish with loudnorm -14.
   - **Re-records:** denoise them with their own noise profile and match the tone (e.g. +2 dB high shelf at 3 kHz). Append them to the source with a 1 s gap and splice them in. Use 'raw' bounds so plosives such as the "P" in "Power" aren't trimmed.
   - **Verify:** re-transcribe the final track and check every splice in isolation. Whisper blends neighbouring words in context.
   - **Captions:**
     - English: align the exact SCRIPT text to the whisper word times (difflib, interpolating unmatched words). Never patch whisper's spelling word by word, because whisper output varies between runs.
     - Telugu: the script line per piece, with word times spread over that piece's voiced frames.
   - **Scene timing:** anchor scenes to spoken phrases, not fixed times, so re-records re-time everything automatically.

## Runtime planning [PB:388, 395]
- **Runtime check method:** always measure runtime AFTER the standard Shorts edit (proasm.squeeze maxgap 0.24/keep 0.15, tempo EN 1.08 / TE 1.10, 0.22–0.35 s line gaps). Raw-take totals overstate runtime by ~20%.
- Budget the script by real speech rate before voicing (Sandeep EN ≈ 2.4 words/s; Telugu runs ≈ 15% longer than EN), never by a guess. Diwali 1/6 was scripted as "≈2:30 / ≈3:00" but recorded 3:12 / 3:41. Keep an internal safety margin under 3:00 (→ FMT-01).

## Captions [PB:341, 359, 374, 265]
- **Telugu captions:** PIL + RAQM (cairo toy fonts can't shape Telugu). Timing: sentence boundaries from the TTS pause map, words spread by length.
- **Caption fix (Oct 29):** whisper drops/duplicates words at chunk edges on generated voice. Transcribe in ~25 s windows, then snap to the exact script text with difflib (fixw.py) and interpolate missing words. TE captions: map spelled-out numbers to digits (CAPMAP in tealign5.py).
- **Whisper on generated voice:** use overlapping ~22 s windows (keep words that end before window−0.6 s) and snap to the script with difflib; a single pass drops 10 s chunks.
- **Telugu checks (Nov 8):** verify every generated or reused Telugu line with the te_med model (generic Whisper gives garbage on Telugu). Mixed-script captions: measure each word with its own font, or Latin words overlap Telugu ones.

## Render [PB:214–217, 220, 267, 314, 317 (masters)]
   - PIL frames piped to ffmpeg: libx264, CRF 19–20, 30 fps.
   - Lead 0.15 s. Tail 0.7 s (Shorts) or 3 s (long).
   - Render in 2 parallel parts. Long video speed is about 0.17 s per frame, so about 25 min for 5 min of video.
- **Render speed (Nov 8):** render the shared body once per language and only the slide + loop tail per platform, then concat with stream copy (2-CPU box: four 1.5-min versions in about 12 min).
- **Film grain cost (Nov 6):** per-frame random grain at σ≈5.5 drove x264 to ~50 Mbps (900 MB for 2.4 min). Use ≤ σ 3, or temporal denoise before the final encode (hqdn3d=2:2:8:8, crf 22, maxrate 10M ≈ 7.5 Mbps).
- Deliver masters over 400 MB as byte-exact split parts (copy /b or cat).
- Render long videos in chunks with done-files (or atomic renames) so a restart only loses one chunk.

## Measured voice credit rates (evidence) [PB:337, 353]
- Gold 4 (Oct 28): about 1 credit per character measured (the earlier 0.46 estimate was wrong). Numbers spelled out in Telugu add a lot of characters. Count the TTS characters, not the script words.
- GS 4/6 (Nov 10): 15 new lines, 1,037 credits (EN 418, TE 619).

## Gotchas [PB:228–230, 342, 382]
- Never `pkill -f` / `pgrep -f` with a pattern that also matches the shell's own command line; it kills the shell (exit 144). Kill by PID from `ps` filtered with `grep -v grep`.
- Don't run heavy whisper jobs alongside renders unless you have to. Both slow to a crawl on 2 CPUs.
- **Gotcha:** pill/scale(0) → cairo singular matrix → "out of memory" crash mid-render; guard s<=0.01.
- **Gotchas (Oct 30):** cairo `paint_with_alpha` ignores a rectangle path: clip to it first (painted whole cards amber). Telugu text through PIL at scale 0 → cairo "out of memory": txt() now returns early on a singular matrix. Noto Sans Telugu has no → glyph: Telugu strings swap it for "-". Never wait on `pgrep -f '<pattern>'` from a shell whose own command line contains the pattern; wait on PIDs or done-files. Render long videos in 4 chunks with done-files so a container restart only loses one chunk.

