# Delhi Rain · opening motion test (v1) and asset breakdown

**Files:** `poc/DelhiRain_opening_POC_EN.mp4`, `poc/DelhiRain_opening_POC_TE.mp4` (20 s, 1920×1080, 30 fps).
**Cost:** no paid generation, no ElevenLabs credits. Captions stand in for the approved narration (lines 0.1, 0.2, 0.3, 0.6, 0.9). Sounds are real recordings from `sfx/`; music is `the_quiet_meridian` (yours, → MU-01).

## What the test shows (→ DIR-02, DIR-03, DIR-04)
Every shot has an action or change that carries the line. The camera stays still in all four shots: the objects move and the shots cut, with no zoom-ins.

| Time | Shot | Action or change on screen | Sound |
|---|---|---|---|
| 0–5.6 s | Outside, looking in through the balcony door | Anu (A0 cutout) steps into the doorway with her bat. Her legs are hidden by the parapet, so there's no fake walk cycle, just a light bob and sway. The towels on the line and the tulsi move in the breeze. The morning light breathes | Her footsteps |
| 5.6–10.4 s | Her view over the railing | The opposite block **disappears into drifting haze** (animated noise layers, not a fade). The towels **stop swaying** as the air goes still, which sets up line 3.7 | Thin wind ambience rising |
| 10.4–14.4 s | Back to the door, now hazy, cooler and dimmer | Mum steps in behind her. Anu **turns** to her (front → three-quarter view, 0.3 s), and the **bat goes back against the door frame** | Mum's footsteps; a soft set-down knock |
| 14.4–20 s | The windowsill | The **paper boat is set down** (its shadow lands); outside, haze drifts. Then a HOLD on the dry boat (deliberate: "no rain"), with only dust motes moving | Paper slide |

## Review of A0 (master reference)
**Matches the spec:**
- Anu: bob with fringe, round red glasses, gap tooth, mustard hoodie, teal scarf, navy track pants, white canvas shoes, taped bat.
- Mum: bun, bindi, maroon saree, grey cardigan.
- Dad: sweater over checked shirt, rectangular glasses, moustache.
- Clearly distinct from Chelli.
- Consistent across the three Anu views.

**What A0 doesn't have (the gaps the test exposed):**
1. **No back view and no expression close-ups.** All three Anu views are smiling. For "Not today. Again." she needs a disappointed pose. In the test she still smiles behind the haze, which is the biggest weakness.
2. **Resolution 1672 × 941** is under the 1920 px minimum (→ ART-06). Fine as a master reference, and the cutouts are only ever scaled down. Final scene images must be ≥1920 px.
3. **Style check (→ PUB-05):** painterly, with visible brush texture, but the faces are quite lifelike. YouTube's policy lists clearly stylised animation as exempt and realistic depictions as needing disclosure. A semi-realistic painted look is the "genuinely ambiguous" case, so it's **your decision**. My reading: it's an illustrated style with an ILLUSTRATIVE tag, so No, with that reason recorded.

**Accept A0 as the master for faces and outfits?** If so, everything below is made by editing A0 in the same Gemini chat, not by new generations.

## Asset breakdown (whole opening and the other Anu scenes)
Each final image is its own high-resolution file (no collages). Characters go on a plain warm-grey background so they can be cut out. Sets go **empty**, with people and props as separate layers.

| Batch | ID | Asset | How | Used in |
|---|---|---|---|---|
| **0 (pending)** | B0 | Balcony, view across the road, sill, paper boat | Prompt already sent | Every Anu scene |
| **1 · Anu poses** (edit A0) | A1 | Anu, back view, bat on her shoulder, two stride poses (left foot / right foot) | Edit A0 | 0.1 walk away from camera (a real two-pose stride instead of a slide) |
| | A2 | Anu, three-quarter, **disappointed**: head slightly down, bat lowered | Edit A0 | 0.3, 3.5, 4.6 |
| | A3 | Anu, three-quarter, **looking up, hopeful** | Edit A0 | 0.4, 0.8, 3.10 |
| | A4 | Anu, **delighted**, crouching by a puddle | Edit A0 | 4.2 |
| **2 · Mum and Dad** (edit A0) | A5 | Mum, three-quarter, one hand reaching to a child's shoulder, a gentle "not today" look | Edit A0 | 0.3 |
| | A6 | Mum holding her phone, screen turned away | Edit A0 | 0.4 |
| | A7 | Mum and Dad, three-quarter back view, looking up | Edit A0 | 0.8 |
| **3 · Empty sets** (edit B0) | P1 | Outside looking in: door, room, parapet. No people | Edit B0 | 0.1–0.3, 3.10 |
| | P2 | Her view: the opposite block, clear sky, railing as a **separate** foreground layer | Edit B0 | 0.2, 3.6, 4.2, 4.6, 6.1 |
| | P3 | Windowsill with the window, no boat | Edit B0 | 0.6, 0.9, 7.6, 7.7 |
| | P4 | The lane below after rain, with a puddle, no people | Edit B0 | 4.2 |
| **4 · Props** | R1 | The paper boat, isolated, three angles | Edit B0 | Every boat beat |
| | R2 | Anu's bat, isolated | Edit A0 | 0.3 |
| | R3 | Anu's hands folding the boat (close-up, mustard cuffs) | Edit A0 + B0 | 0.6 |
| **5 · Later** | A8 | Anu a year older (same look, slightly taller) | Edit A0 | 6.1 |
| | F0 | Solapur farmer: master + one pose (ILLUSTRATIVE) | New | 5.1 |

**Made in code, not generated:** haze, light changes, towels and plants, rain and puddle ripples, dust motes, the flight line and map, all labels and captions.

**Existing effects used elsewhere in the film:** Map Route, Day Counter, Before & After, Money Stack (Remotion); 3D Explainer, 3D Data Chart, Domino Reveal (Python). Inside the cloud uses real footage plus realistic reconstructions (ART-03), separate from this pack.

## Known limits of this test (all fixed by the assets above, nothing to fix in the motion approach)
- The sets are flat stand-ins drawn in code, so they don't match A0's painted look. P1–P3 fix that.
- Anu smiles throughout. A2 fixes that.
- The entrance is a lateral step-in with hidden legs. A1 makes it a real walk away from camera, as in the script.
- The cut-out bat carries a sliver of her hand. R2 fixes that.
- The Telugu captions use the English timing. The final is timed from each language's recording (→ ED-05).
