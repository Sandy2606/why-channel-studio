# Golden Sparrow S1: recording report (measured from the recorded audio)

All lines are recorded in both languages at natural pace: **no tempo change and no pause squeezing**. Edge trims and Pace Model gaps are the only edits. The cold open and the final question use the approved test takes, and the cold-open gaps are kept exactly as in the test. 0.2 was re-recorded with the new wording.

## Film

| | English | Telugu |
|---|---|---|
| **Total runtime** (incl. title card and 5 s Season 2 end card) | **13:51** (831.0 s) | **16:54** (1014.2 s) |
| Cold open → title sting | 00:35.8 | 00:44.8 |
| Ch 1 · Was India really that rich? | 01:03.5 | 01:13.1 |
| Ch 2 · The cloth the world wanted | 02:32.8 | 02:53.4 |
| Ch 3 · Golconda and Machilipatnam | 04:46.2 | 05:32.9 |
| Ch 4 · Who controlled the wealth? | 06:39.9 | 08:06.6 |
| Ch 5 · Europe didn't discover India | 08:27.4 | 10:27.4 |
| Ch 6 · The company that came to trade | 10:00.0 | 12:15.3 |
| Ending (7.1) starts | 12:44.7 | 15:30.4 |
| Final question (7.9) | 13:39.8–13:45.1 (5.3 s) | 16:42.3–16:48.4 (6.0 s) |
| Season 2 card lands | 13:46.0 | 16:49.2 |
| Narration above music (speech regions) | 22.3 dB | 22.7 dB |

Loudness for every master is −14 LUFS integrated, with true peak ≤ −0.9 dBTP.

## Shorts

| Short | English | Telugu |
|---|---|---|
| S1 | 1:22 (81.8 s) | 1:29 (89.1 s) |
| S2 | 2:15 (134.6 s) | 2:39 (158.8 s) |
| S3 | 1:35 (94.7 s) | 2:06 (125.7 s) |
| S4 | 1:48 (107.5 s) | 2:22 (142.2 s) |
| S5 | 1:29 (89.2 s) | 1:39 (99.1 s) |
| S6 | 2:39 (159.0 s) | 2:47 (167.1 s) |

Every Short is under 3:00, and the story sets the length. The music tail after the last word is 1.1 s.

## Mix
- **Voice:** pro chain, on top. Music is ducked 65 % under speech, so narration sits about 22 dB above the music across both films and all Shorts.
- **Music map:**
  - Cold open: *Beneath the Rising Current*.
  - Ch 1–3: *Where the River Bends*.
  - Ch 4: *Before the World Wakes*.
  - Ch 5 (the ocean): *Beneath the Heavy Swell*.
  - Ch 6: *Beneath the Rising Current*, from a later section.
  - Ending: *The Last Threshold*, which builds into the cliffhanger.
- **Season 2 ending, darker and more suspenseful:**
  - It uses *The Last Threshold* (a dark track the user made in Gemini), starting 15 s in so its loudest stretch lands on the final question. The top end is softened above 4.5 kHz to keep it under the voice.
  - A distant boom and a slow heartbeat sit under the question.
  - A synth riser runs into the impact on the card.
- **Structural SFX (real library files only):**
  - Chapter cards: air woosh, then a distant boom on the card.
  - Big reveals: a low knock.
  - Cold open: wind bed.
  - Scene-level SFX follow once the picture is locked.
- **QC:**
  - All 89 EN film lines and 13 EN Short pickups were checked with Whisper; no missing or garbled words. "23 June 1757" is read as "June 23, 1757".
  - TE take lengths were checked against the timing model; there are no truncations or long dead air (the longest internal pause is 0.7 s).

## Files (out/)
- `GS_S1_film_EN.mp3` / `_TE.mp3`: full mix.
- `*_voice.wav`: narration stem.
- `GS_S1_S1…S6_{EN,TE}.mp3`: Short mixes.
- `timeline_{en,te}.json`: every line's start and end.
- `shorts_{en,te}.json`: Short segment marks.
