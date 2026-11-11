# GS 5/6 voice report (Nov 11)
One take per approved NEW line, eleven_v4, cloned voices (Sandeep English/Telugu, Sowmya English/Telugu). All other narration = approved S5 film/Short audio, cut only inside measured pauses.

| | English | Telugu |
|---|---|---|
| Voice track (incl. 2.0 s end-slide gap + loop line) | **2:17.2** | **2:45.9** |
| Expected final video (+ ~1 s tail) | ≈ 2:18 | ≈ 2:47 |
| Under 3:00 | ✅ (42 s margin) | ✅ (13 s margin) |

**Credits used: 2,072** (EN 950 · TE 1,122), as billed per generation: EN 53A 109 · PILOT 475 · FORCE 180 · L 50 · Q1 53 · Q2 42 · Q3 41; TE 53A 134 · PILOT 497 · OLD 99 · FORCE 190 · L 54 · Q1 63 · Q2 47 · Q3 38. ElevenLabs flow: "GS 5/6 voice (Nov 10)".

## Speech checks
- EN: Whisper (small) on every new take: word match 0.91–1.00; full assembled track reads complete and in order.
- TE: Telugu Whisper (medium, chunked at pauses) on every new take and on the full assembled track: every sentence present and in order. (A first unchunked pass dropped a middle segment of the pilot line; that was the ASR, not the audio: the chunked pass reads all of it.)
- Every splice edge sits in silence (all edges < −25 dB re speech).
- New takes level-matched to the film narration (raw differences: Anna +3.3 to +4.8 dB, Chelli −4 to −7 dB, all normalised).

## Listen for (possible concerns)
1. EN pilot: "they **called** the Hindus of Calicut" may sound like "call" (both ASR models hear "call").
2. EN pilot: "tells us **little**": the small model heard "a little", the medium model "little". If it sounds like "a little", the meaning flips; a regenerate of the pilot line costs ≈ 475.
3. EN "crew's" sounds close to "cruise" (same as the approved film line 5.7, so consistent).
4. Same-line splice: NEW sentence 1 of line 3 runs straight into the film's Malacca sentence (0.30 s gap). Check that the two voices match in tone (EN and TE).
5. TE pilot says "కాలికట్" a little differently from the film's "కాలికట్టు"; harmless, but noted.
6. TE runs 14 s longer than the 2:32 estimate (the new Telugu takes are slower than the film pace). Still under 3:00.
