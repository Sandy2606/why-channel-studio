# Delhi Rain 2/6 "Can smoke make rain?" · QC report (Nov 16) · AWAITING THE USER'S FINAL VIEWING APPROVAL, NOT FOR PUBLISHING YET

Files (local only): `DelhiRain2_{EN,TE}_{YT,IG}.mp4`. EN runs 1:59.8 and TE 2:20.7 (both under the 3:00 Shorts limit). Approved voice tracks only; no new credits spent in this phase.

## The five refinements (user review of the preview, Nov 16)
1. **Full vertical frame; two faces zoomed in turn.**
   - On "silver" the silver face fills the frame (1000 × 860) while ice spreads over it.
   - On "iodine" it slides out and the iodine face fills the frame, showing patches but no continuous layer.
   - On "real cloud" both faces sit side by side, with the 2026 source card and "IN A REAL CLOUD: STILL BEING STUDIED".
   - On the cleaved slab, the silver/iodine legend now sits below the atoms, not over them.
2. **No temporary labels.** Every stub is gone; each shot has its own scene.
3. **Phone readability:**
   - Face titles are 44–56 px and face labels 30–40 px.
   - Source cards: title 40 px, key line 30 px, source line 26 px (was 23).
   - The lab line is 34 px, the citation 28 px.
4. **Telugu takes and loudness:**
   - All four new Telugu takes were checked against the approved script (Whisper medium, phonetic transcript); every phrase is present.
   - Final files measured one by one, using ffmpeg ebur128, true peak:

| File | Integrated | True peak |
|---|---|---|
| EN YT / EN IG | −14.0 LUFS | −1.5 dBTP |
| TE YT / TE IG | −14.0 LUFS | −2.1 dBTP |

   - The −15.4 / −14.6 LUFS readings came from short preview excerpts; integrated loudness over a short excerpt doesn't represent the whole mix.
5. **Rhythm:**
   - The slower Telugu cleaving is kept.
   - The motion added for this round has a job in the story: the camera closes in on the freezer bottle before the tap; vapour drifts into the salt; the WMO key line is underlined as it is read; the seeding flights repeat over the clear sky (the particles just thin out) and over the suitable cloud (a few drops fall).

## Scenes built (the same storytelling treatment throughout)
- **Hook:** the G6 plane at native pixels.
  - Flare particles are drawn as tiny particles. They never become drops.
  - "TINY PARTICLES" leader label, then "ONLY UNDER THE RIGHT CONDITIONS".
- **Cloud journey:**
  - The monsoon painting dissolves into its droplets: "BILLIONS OF TINY DROPLETS", then a sunbeam with "SO LIGHT THEY FLOAT".
  - One droplet gathers its neighbours, grows and drops.
  - A thermometer falls below 0 °C: "BELOW 0 °C · STILL LIQUID".
  - The freezer bottle, labelled ANALOGY: tap, ice spreads bottom-up over about 2 s, "it can happen, not always".
  - SUPERCOOLED droplets waiting under dashed hexagons.
- **Template:** the crystal grows while the droplets around it shrink (they give up their water). It falls through the 0 °C line and melts into a raindrop.
- **Salt:**
  - Cold clouds vs warmer clouds.
  - The salt jar, labelled ANALOGY: over hours it goes damp and lumpy, and vapour flows in.
  - "IT PULLS WATER FROM THE AIR".
- **Collisions:** a salt-grain droplet with collisions, merges and near-misses, labelled "CAN HELP DROPLETS GROW" (no race, no winner).
- **Check:** silver iodide and salt both point to one cloud: ✓ A CLOUD, ✓ THE RIGHT KIND OF CLOUD.
- **WMO:**
  - SOURCE card, then a clear sky ("NOTHING TO WORK ON") beside a suitable cloud ("MAY RESPOND · NOT GUARANTEED").
  - Only the WMO's own claim is shown.

## Automated checks
| Check | EN YT | EN IG | TE YT | TE IG |
|---|---|---|---|---|
| qc_video (format, loop, loudness, TP, captions) | PASS | PASS | PASS | PASS |
| freezes | PASS, holds marked | PASS, holds marked | PASS, holds marked | PASS, holds marked |
| sharpness | REVIEW (flat diagrams; the freezer bottle at 0.86–1.0 scale) | same | REVIEW (S1b dissolve, bottle) | same |
| check_exports (format, identical bodies, audio sync, endings) | PASS | PASS | PASS | PASS |
| check_copy | PASS, 0 FAIL; REVIEW: secondary-source limits, PUB-07 human review | | | |

- **Marked holds (`qc/holds_*.json`), each with live motion measured:**
  - EN WMO card read.
  - TE: cleaving (approved pace), the lab caveat read, salt vapour, the WMO comparison.
- **Frame review:**
  - Stills sheets for both languages were checked frame by frame. They stay local because they include the host.
  - Text overlap fixed: the salt jar's two labels, the slab legend, and cloud shapes fading in (now drawn as one layer).

## Open for the user
- Final viewing approval of all four files.
- PUB-05 for the illustrated host (the same question as 1/6).
