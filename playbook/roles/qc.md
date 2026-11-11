# Role: Quality control

**Inputs:** the four exports, the scene sheet (with HOLD marks), the asset register and the post copy.
**Responsibilities:** technical, layout, visual and accuracy checks; the defect log; the score.
**Outputs:** `QC_report.md` (→ templates/qc_report.md).

## Rules
- **[QC-01]** (P, user Nov 10) **Delivery gate.** A video isn't approved until it passes both technical and professional visual QC. Check EN and TE, and YT and IG, independently.
  - **Checklist:**
    1. Every text box, label, badge and card is aligned.
    2. Fills sit inside their borders.
    3. Margins, padding and radii are consistent.
    4. Arrows and leader lines land on their targets.
    5. One font family per role, with a consistent size hierarchy.
    6. Only palette colours are used (→ BR-01).
    7. No text goes beyond or touches a box edge.
    8. Captions, labels, credits and animations never overlap.
    9. The hierarchy is clear and uncluttered.
    10. No modern-looking graphic appears in a historical scene.
    11. No image is enlarged beyond its source resolution.
    12. Telugu layouts are inspected on their own.
  - **Frame-level inspection:**
    - a contact sheet of the whole video;
    - keyframes at full 1080×1920;
    - every text entrance, exit and transition;
    - the first 3 s frame by frame;
    - the corners, caption lane and edges cropped at 2x;
    - a phone-size review (~390 px wide).
- **[QC-02]** (P, Phase 2A approval Nov 10) **Severity.**
  - BLOCKERs must be zero at delivery: a factual or numeric error; a missing or false label on an image; an unsourced claim; an export defect; unreadable text; an overlap.
  - IMPORTANT items are fixed, or explicitly accepted by the user.
  - POLISH items are logged.
- **[QC-03]** (P, user Oct 28, Nov 10) **Score.** The target is 8.5/10, and it never substitutes for QC-02. A factual error fails whatever the score; a deliberate quiet archival shot never fails for having little motion. Score honestly (→ WF-06) with the scorecard below.
- **[QC-04]** (P, Phase 2A approval) Report every check as **Performed?** (yes, no or not applicable) and **Method** (script, frame review or listening). A check that wasn't performed is never reported as passed. Composition, story, historical interpretation, music fit, SFX fit, Telugu naturalness and real listening are human reviews; say who did them and how.
- **[QC-05]** (P, user Nov 10) **Automated layout checks.** Components register their boxes with `layout.reg()`; `qc_layout.py` renders frames every 0.1–0.5 s, and `layout.check()` flags:
  - text outside its box or with less than 8 px padding;
  - boxes nearer than 40 px to a frame edge (full-bleed images excepted);
  - overlaps between captions, credits, cards, labels and badges;
  - corner badges off their shared centre line.
  - Automation never replaces human inspection.
- **[QC-06]** (P, playbook Oct–Nov) **Technical checks:**
  - duration (→ FMT-01);
  - integrated loudness and true peak (→ ED-03);
  - frame-1 brightness above 60/255;
  - black frames;
  - freezes (freezedetect n=0.003, d=1.5; marked HOLDs are exempt);
  - decode errors;
  - loop seam;
  - sharpness per scene (Laplacian; flat vector scenes score low by nature);
  - caption coverage;
  - safe zones (→ LAY-03).
  - Make a stills sheet and fix overlaps before the full render.

## Scorecard (weights)
| Area | Weight | 8+/10 means |
|---|---|---|
| Hook (first 2 s) | 20% | Curiosity from the first frame (→ ST-01, DIR-08) |
| Pacing / editing | 15% | Rhythm follows information (→ DIR-04, ED-01) |
| Captions | 15% | → LAY-02 |
| Visual quality | 15% | → QC-01, LAY-05, ART-01 |
| Audio | 10% | → ED-03, MU-02, SD-01 |
| Script / story | 10% | → ST-01 |
| Research / trust | 10% | → RS-01 – RS-06 |
| CTA / growth | 5% | → FMT-04 – FMT-09 |

**Failure conditions:** any open BLOCKER; an unperformed check reported as passed.
**Handoff:** the QC report goes with the delivery; defects and lessons go to `history.md` (→ WF-05).
