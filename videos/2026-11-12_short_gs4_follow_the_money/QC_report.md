# GOLDEN SPARROW · 4/6 · "Follow the money" · QC report (Nov 10)

Files: GoldenSparrow4_EN_YT / EN_IG (1:49.2) · TE_YT / TE_IG (2:15.7). 1080×1920, 30 fps, H.264 CRF 19, AAC 192k.
Voice: 15 new lines, 1,037 credits (EN 418 · TE 619), one take each, voice_lib tag gs_s4. No other paid assets.

## Technical QC (all four files)
| Check | EN_YT | EN_IG | TE_YT | TE_IG |
|---|---|---|---|---|
| Duration | 109.19 s | 109.19 s | 135.68 s | 135.68 s |
| Frames (parts a1+a2+tail) | complete | complete | complete | complete |
| Black frames | none | none | none | none |
| Freezes ≥ 2.5 s | none | none | none | none |
| Loudness (target −14) | −14.8 LUFS | −14.8 | −14.7 | −14.7 |
| True peak | −1.7 dB | −1.8 | −1.8 | −1.8 |
| Decode errors | 0 | 0 | 0 | 0 |
| Loop seam (first vs last frame, mean diff) | 0.61 | 0.61 | 0.55 | 0.55 |
| Frame 1 brightness | 142 | 142 | 143 | 143 |
| Sharpness | no source image enlarged beyond 1.0×; lowest Laplacian scores are flat vector maps/diagrams (kingdoms, rains split, Madanna map), not soft images |

## Professional visual QC (sign-off)
- [x] All text and labels aligned (shared badge component; one plate/card language; museum-label notes)
- [x] Borders and background fills contained (badge fill inset inside border, drawn at 3×)
- [x] Only approved colours and typography (ink #0A0A0A, cream #F4F1EA, amber #FFB224, parchment, antique gold #C4A05C; Archivo Black + Space Mono + Noto Sans Telugu)
- [x] No captions, chips or UI elements overlap (automated: 0 defects in every 0.25 s frame, EN and TE, plus 0.1 s on transitions)
- [x] English and Telugu layouts inspected separately (contact sheets, phone-size sheets, corner/caption crops for each)
- [x] No soft or over-zoomed source images (illustrations as native-pixel panels; archive full-screen only when ≥ 1920 px tall)
- [x] Transitions stylistically consistent (no stamps, no split-flap; archival date reveal; crossfades ≤ 0.5 s)
- [x] Reviewed at full 1080×1920 and at phone size (390 px), first 3 s frame by frame, corners and caption lane separately

Inspection files: qc/<VIDEO>/contact_sheet.jpg, first_3s.jpg, corners_captions.jpg, phone_size.jpg, key_*.png (every scene midpoint), entry_*.png (every scene entrance).

## Defect log
| # | Found in | Defect | Fix | Status |
|---|---|---|---|---|
| 1 | Preview | Red rubber stamps on the farman looked cheap | Museum-label notes with leader lines and soft highlighter | fixed |
| 2 | Preview | Split-flap / red 1498 too modern | Ink cartouche, antique-gold double rule, year rolls back while the thread winds in, on the 1502 map | fixed |
| 3 | Preview | Series badge text touched its right edge; Telugu sat high | Shared `layout.badge()` component | fixed |
| 4 | Preview | Captions in one fixed spot, over pictures and labels | Reserved caption lane above platform UI; no box, bottom fade; credits moved up; caption-vs-image check | fixed |
| 5 | Layout QC | "TRADING RIGHTS" overflowed its card mid-animation | Fixed card geometry, auto-wrap | fixed |
| 6 | Layout QC | Outgoing/incoming cards overlapping (Virji, Akbar) | Sequenced fades | fixed |
| 7 | Layout QC (TE) | Mughal-front label collided with Golconda/Deccan labels | Deccan labels fold away as the front passes (Golconda annexed 1687) | fixed |
| 8 | Layout QC | Farman slid up through the caption lane | Fades in place | fixed |
| 9 | Layout QC | Two credits overlapping at the engraving→globe cut | Credit hand-off | fixed |
| 10 | Frame QC | Static holds 2.7–3.9 s (TE chain, TE map, TE role cards, tease) | Gentle vector drift, pulse on Golconda, slow map pan, panel pan, wider map crop | fixed |
| 11 | Frame QC | First 3 s: grid lit at frame 1 then refilled (flicker); bottom fade popped in at frame 2 | Constant grid with a slow light sweep; constant bottom fade on frame 1 and the loop | fixed |
| 12 | Frame QC | Chain station label drifted into the caption lane; cut wedge sat on "KEEP A CUT" | Labels never drawn below 1300 px; wedge offset beside the building | fixed |
| 13 | Frame QC | Globe's own source line sat behind the captions | Masked; our credit above the lane | fixed |
| 14 | Frame QC | "Europe" globe label shrank to a sliver at the globe's edge | Kept the three Indian Ocean routes (Hormuz, Mocha, Malacca) | fixed |
| 15 | Frame QC | "Dramatized" chip touching the picture border (hook, Virji) | Moved 24 px inside | fixed |
| 16 | Frame QC | Disk allowance ran out during mux (TE_IG missing) | Cleared old intermediates, re-muxed, frame counts verified | fixed |

## Accuracy labels on screen
MADDISON ESTIMATE · ASSESSED DEMAND · VARIED · OFTEN PAID IN CASH · HISTORIANS' ESTIMATE · ILLUSTRATIVE · EXAMPLE OF THE DOCUMENT TYPE · ILLUSTRATION · NOT PORTRAITS (TE) · APPROXIMATE EXTENTS · HISTORICAL ESTIMATES · UNCERTAIN · DRAMATIZED on every AI illustration.

## Platform endings
YT: FULL FILM · RELATED VIDEO + Subscribe. IG: FULL FILM ON YOUTUBE · LINK IN BIO + Follow. Remember to assign the full film as the Related Video in YouTube Studio.
