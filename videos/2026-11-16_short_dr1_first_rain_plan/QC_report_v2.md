# Delhi Rain 1/6 · v2 "cinematic evidence-driven" rebuild · QC report (Nov 14) · AWAITING THE USER'S FINAL REVIEW, NOT FOR PUBLISHING YET

**Files** (local only; the repository is public):
- `DelhiRain1_v2_EN_YT.mp4` and `DelhiRain1_v2_EN_IG.mp4`: 1:55.8
- `DelhiRain1_v2_TE_YT.mp4` and `DelhiRain1_v2_TE_IG.mp4`: 2:19.8
- All 1080×1920, 30 fps. Same approved voice tracks; no new credits.

**Approvals this rebuild follows (user, Nov 14):**
- The v2 direction: evidence first, host as punctuation.
- The 1971–72 preview, with five adjustments:
  1. meaningful rhythm only;
  2. verified evidence cards in our own layout;
  3. silver iodide shown as particles;
  4. the smog never clears;
  5. no invented 1971–72 numbers.
- Composition refinements: use the full frame; Delhi winter haze, not snow; a labelled metaphor with visible uncertainty.
- Full-frame captions overlay allowed. No host-time quota.

## What changed from v1
- **Host on screen:**
  - v1 had about 57 s per version, including a 28 s board stretch.
  - v2 keeps the hook (about 7 s), his in-scene reveal on the 1957 lawn (from the approved Mix A+C), "Not proof" with "But here's what really changed", and the loop.
  - Telugu adds the closing question (about 2.7 s). English has no room for it before "why", so it goes straight to the WHY? reveal.
- **1957 lawn:** labels and animation explain each step on the spoken words:
  - JULY 1957 / MIDDAY;
  - a leader line to the National Physical Laboratory;
  - a salt-into-water diagram;
  - SPRAYED INTO THE AIR;
  - rising-air arrows to the clouds.
- **Results:**
  - An original SOURCE card: Roy, Ramana Murty, Srivastava & Khemani · MAUSAM 12(3) · 1961.
  - The 18 dots fill on the spoken numbers, with "?" in the inconclusive four.
  - The paper's own verdict ("no fully dependable conclusion") appears, then KEEP TESTING.
- **1971–72:** the approved preview, enlarged:
  - timeline flip, with cool haze instead of snow;
  - a self-drawing generator, released particles;
  - big calendar tiles (11 + 11, COMPARE);
  - the IITM source card (as reported by PTI);
  - the balance with an uncertainty wedge, labelled "illustration · not measured rainfall";
  - an ice-on-particle magnifier.
- **More rain → 2025:**
  - The monsoon plate (S1b, new) behind the 1957 and 1971–72 cards.
  - A dolly along the rail to a 2025 card, whose window opens onto Delhi in smog (P2 with Anu's parents from A7).
  - THE GOAL: CLEANER AIR, "a hope, not a result". The smog never clears.
- **Flight:**
  - A larger map with a large date title.
  - G6 (new) for "fires flares… silver iodide and salt", labelled ILLUSTRATION.
  - Back to the map for the flare rings over the three areas.
- **Waiting:** G4 (Anu's family), then an illustrative radar screen for "the scientists watch the sky", then G4 again.
- **Result:**
  - The real headline in our own card: "Second cloud seeding trials fail in Delhi", Business Standard, Oct 29, 2025. Wording checked against the article on Nov 14.
  - DELHI: NO RAIN, then the dry gauge with the IMD / Delhi government report figures.
- **"Nearly seventy years":** a 1957 → 2025 counter over the series rail (salt spray · silver iodide · flares), with 68 YEARS OF TRYING.

## Technical QC (`qc_video.py`, each file separately)
| File | Loudness | True peak | Black | Unmarked freezes | Sharpness | Loop seam |
|---|---|---|---|---|---|---|
| EN YT / IG | −14.0 LUFS | −1.5 dBTP | 0 | 0 (slide and loop holds marked) | 24 scenes, none low | PASS |
| TE YT / IG | −14.0 LUFS | −1.6 dBTP | 0 | 0 (8 inside marked holds; see below) | 28 scenes, none low | PASS |

- **Exports** (`check_exports.py`): PASS. The body is identical at 8 points per language.
- **Telugu holds (honest):**
  - A breath after "four couldn't tell".
  - The verdict pill's read time.
  - The date title, while "అక్టోబర్ 28, 2025" is spoken slowly.
  - The headline's read time.
  - Two map moments where the plane and flare rings are moving but small (detector false positives).
  - The slide and the loop.
- **Picture scale:** every painted plate is shown at ≤ 1.0 (G1, G2, G3, G4, G6, S1b, P2, P3, A7 parents at 0.48). The studio plate's blurred soft-focus fill (1.34×) is unchanged from v1 and still needs your decision.
- **Post copy:** credits updated (Anu's family, the 2025 plane and the radar are illustrations). `check_copy`: INCOMPLETE, human review only.

## Weak spots, honestly
- The map is still a sparse drawn diagram. It's larger and clearer than v1, but it's the plainest scene.
- The 2025 card's window opening into the balcony is a quick 0.5 s resize; it reads, but isn't elegant.
- The Telugu counter label keeps "SILVER IODIDE" in English capitals. The narration says "silver iodide" in English too.
- No automated `qc_layout` run (this renderer draws text directly). Layout was checked on frames: section stills for both languages and the contact sheets every second.

**Score (before your review):** EN 8.8, TE 8.6.
