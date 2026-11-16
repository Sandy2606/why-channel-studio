# Delhi Rain 3/6 "Delhi's worst air, the wrong sky" · QC report (Nov 16) · AWAITING THE USER'S FINAL VIEWING APPROVAL, NOT FOR PUBLISHING YET

Files (local only): `DelhiRain3_{EN,TE}_{YT,IG}.mp4`. EN 2:10.2, TE 2:39.7 (under 3:00). New voice: 5 lines per language, 1,046 credits; 12 film clips reused.

## The user's corrections (Nov 16) and where they are
1. **~80% benchmark (line 12):**
   - Spoken and shown as the benchmark this preliminary analysis uses (BENCHMARK USED IN THIS ANALYSIS · for clouds that form and last).
   - Altitude stated as ≈1.5 km above sea level (850 hPa), with a small altitude marker.
   - PRELIMINARY · NOT PEER-REVIEWED tag throughout.
2. **90% statement (line 9):**
   - The grid is titled PEAK POLLUTION EVENTS ONLY · not all winter days.
   - The 20% grid is titled ALL WINTER.
   - Both are attributed to Ghude (IITM).
3. **Cross-section (lines 13–15):**
   - The smog is a soft gradient, thickest at the rooftops and thinning with height (MOST SMOG · BELOW ≈2 KM).
   - Potentially seedable clouds sit at ≈2–5 km.
   - There's no wall or lid, and the heavy rain falls through the smog to the ground.
   - Takeaway: SUITABLE CONDITIONS ARE HARD TO FIND.
   - Line 11's "calm, dry air" shows rising air giving up low, not a barrier.
- **Kept:** the hook, Anu's story, the cloud kitchen and the final question.
- **Host:** one host turn (line 7 "That's Delhi's winter sky").
- **Reminders:**
  - Subscribe (YT) / Follow (IG), 62% scale at the bottom, 1.9 s, one soft click.
  - EN: 31.7, 62.5, 101.1 s. TE: 32.1, 62.7, 93.4, 123.8, 145.3 s.
  - Each sits in a pause. Captions are kept clear of them, and evidence never sits in that strip.
  - The ending CTA is unchanged.
- **Anu indoors:** uses the approved A3 picture inside the window until A2 (disappointed) is uploaded. The renderer switches to `assets/A2_anu.*` automatically; one 16 s chunk then needs re-rendering.

## Rhythm fixes made after the first QC pass (purposeful motion only)
- Hook: the smog closes in during "most polluted days".
- Telugu only: the parents appear on "ఒక తెలుగు కుటుంబం" (the Telugu line names the family).
- Agrawal: the source card arrives on the attribution (in Telugu, after the numbers), and the water surface moves.
- Kitchen: the rising-air arrows actually rise.
- Cloud-cover grid: the winter's tiles appear one by one.
- Humidity: source card, then altitude marker, then gauge, then benchmark, in spoken order.
- The cross-section begins on "one more problem".
- Remaining still moments are evidence-reading holds, marked in `qc/holds_*.json`.

## Checks
| Check | EN YT | EN IG | TE YT | TE IG |
|---|---|---|---|---|
| qc_video (format, loop, frame 1, captions, dropouts) | PASS | PASS | PASS | PASS |
| integrated loudness / true peak | −14.0 LUFS / −2.0 dBTP | −14.0 / −2.0 | −14.1 / −2.2 | −14.1 / −2.2 |
| freezes | PASS (holds marked) | PASS | PASS | PASS |
| sharpness | REVIEW (balcony smog, flat diagrams) | same | same | same |
| check_exports | PASS (0 FAIL) | | | |
| check_copy | 0 FAIL | | | |

- **Voice:** all ten new takes checked with Whisper. The film cuts of 3.4 and 3.8 start on the right phrase.
- **Frame review:** stills sheets for both languages checked. They stay local because they include the host.
- **Telugu glyphs:** ≈ is spelled out as దాదాపు in all Telugu labels.

## Open for the user
- Final viewing approval.
- The A2 upload, if you want Anu's disappointed face indoors.
- PUB-05 for the illustrated host.
