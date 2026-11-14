# Delhi Rain 1/6 "Delhi's first rain plan wasn't in 2025" · QC report (final render, Nov 14)

Four files, 1080×1920, 30 fps, H.264 + AAC 192k:
`DelhiRain1_EN_YT.mp4`, `DelhiRain1_EN_IG.mp4`, `DelhiRain1_TE_YT.mp4`, `DelhiRain1_TE_IG.mp4`.
YT and IG differ only in the series slide's CTA card (Subscribe vs Follow). The videos, the host renders and every host likeness file stay local; this public repo holds text, the asset register and the covers (no host, no recognizable face).

## 1. Technical QC (each file measured separately with `qc_video.py`)

| File | Length | Loudness | True peak | Black frames | Unmarked freezes | Decode errors | Frame 1 | Loop seam |
|---|---|---|---|---|---|---|---|---|
| EN · YouTube | 1:55.8 | −14.0 LUFS | −1.7 dBTP | 0 | 0 (4 inside HOLDs) | 0 | 126.5 | PASS (0.57) |
| EN · Instagram | 1:55.8 | −14.0 LUFS | −1.7 dBTP | 0 | 0 (3 inside HOLDs) | 0 | 126.5 | PASS (0.58) |
| TE · YouTube | 2:19.8 | −14.0 LUFS | −1.6 dBTP | 0 | 0 (5 inside HOLDs) | 0 | 127.0 | PASS (0.50) |
| TE · Instagram | 2:19.8 | −14.0 LUFS | −1.6 dBTP | 0 | 0 (5 inside HOLDs) | 0 | 127.0 | PASS (0.50) |

- **Exports** (`check_exports.py`): PASS. The body is identical across YT and IG at 8 points per language; endings differ by design.
- **HOLDs** (`qc/holds_en.json`, `qc/holds_te.json`, local): the empty 18-dot grid on "Eighteen trial runs", the verdict beat, the series slide, and the loop tail. The Telugu map window is marked as a detector false positive: the plane is moving and the flare rings are opening on the spoken words, but the sprite is small on a dark map.
- **Sharpness:** low scores only on the flat drawn map (EN 85 s, TE 100 s) and the Telugu lawn mist at 25 s. These are known false positives.
- **Image scale** (`check_assets.py`): **FAIL, 1 row.** ST1, the studio plate (2576×1438), is enlarged 1.34× to fill 1920 px. It is blurred as the approved soft-focus fill from the host pilot (Nov 13), so it shows no visible softness, but it is still an enlargement under LAY-05. This needs a decision: approve it as an exception, or have a 3:4 studio plate made for the next host Short. Every other picture is shown at scale 1.0 or below.
- **Sources** (`check_sources.py`): PASS. Markers C1, C2, C3, C14 and C17 all have entries with check dates, and C17 is now from the full paper.
- **Post copy** (`check_copy.py`): INCOMPLETE. The only open items are human review and three platform limits that rest on secondary sources (provisional, as in the central file).
- **Automated layout** (`qc_layout.py`): **NOT PERFORMED.** `dr1.py` draws its text directly and does not register boxes through `layout.py reg()`. Layout was checked by frame review instead (below).

## 2. Creative QC (Claude, frame review: contact sheets every 1 s, the first 3 s, phone size, and seam frames)
- **Hook:** the 1957 card is visible behind the 2025 card from frame 1 and is lifted on "underneath". The host speaks with varied mouth shapes (spot-checked at 5 fps on line 2: open on "Wait", rest in the pause).
- **1957 lawn:** G1 is shown on native pixels with a pan, the host is composited in the scene, and the salt spray is labelled.
- **Match cut:** boy → grandfather on "Today", with ILLUSTRATIVE chips.
- **Evidence:** 18 dots fill 12/2/4 on the spoken numbers, with TENDENCIES, NOT PROOF and a verdict pill. The citation ROY ET AL. · MAUSAM 12(3) · 1961 stays on screen.
- **Studio board:** 1957 / 1971–72 / 2025 timeline with the MORE RAIN vs CLEAN AIR chips.
- **2025 map:** the flight now spans the spoken line in both languages.
- **Ending:** Anu and her grandfather → the dry gauge with IMD figures → WHY? reveal → series slide → loop.
- **Telugu:** on-screen text is native Telugu, and the cues were checked on frames at the dots, map and sill.
- **Weak spots, honestly:**
  - The studio-board stretch is long (EN about 28 s, TE about 34 s of host at the board). It holds attention with gestures, board drops and chips, but it is the likeliest retention dip.
  - The loop tail is about 3 s of a nearly still host.
  - TE runs 2:20 (natural Telugu pace, not sped up).

## Defect log (→ QC-02)
| # | Found at | Severity | Defect | Fix | Status |
|---|---|---|---|---|---|
| 1 | render | High | `card()` crash on float box coordinates at about 45 s | Integer box; resumed render | Fixed |
| 2 | preview | Medium | Word-anchor indices off by one or two in places | Re-indexed against the word list | Fixed |
| 3 | render QC | High | EN line 13 word timings collapsed ("And" lasted 4.4 s), so the captions and the "NO RAIN" chip were late | Re-aligned with an unprompted Whisper pass; SFX re-mixed | Fixed |
| 4 | render QC | Medium | Sill shot static for about 10 s; source line inside the caption lane | 340 px native pan (boat rides with it); source line moved to y 525 with a stroke | Fixed |
| 5 | render QC | Medium | TE map: flight finished about 6 s before the voice did | Flight keyed to the spoken line (T0+1.6 → T1−0.6), EN and TE | Fixed |
| 6 | render QC | Low | Dot chart static during read beats (TE three holds) | Slow ripple on the dots | Fixed |
| 7 | environment | — | Session restart killed the TE render | Re-rendered in 16 s chunks; frame-exact splice (seams checked against sources, difference < 1/255) | Fixed |
| 8 | asset check | Review | Studio plate enlarged 1.34× (blurred fill) | Needs the user's decision | Open |

## Human review still needed (H-rows in `qc_signoff.md` style; none are signed)
Listening on headphones and a phone speaker; Telugu naturalness; licences (the C17 CC BY-NC page is not reproduced); the PUB-05 disclosure decision for the illustrated host; the final watch.

## Score (→ QC-03)
EN **8.3**, TE **8.1** (honest, before your review). This is the strongest hook and evidence beat in the host format so far. Holding back: the long board stretch, the static loop tail, the studio-plate enlargement, and no automated layout coverage.
