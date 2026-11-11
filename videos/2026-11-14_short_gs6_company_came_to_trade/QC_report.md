# Golden Sparrow 6/6 · QC report (final render, Nov 11)

Four files, 1080×1920, 30 fps, H.264 + AAC 192k:
`GoldenSparrow6_EN_YT.mp4`, `GoldenSparrow6_EN_IG.mp4`, `GoldenSparrow6_TE_YT.mp4`, `GoldenSparrow6_TE_IG.mp4`.
YT and IG differ only in the last 4 s (the Season 1 slide: YouTube "Subscribe / Related video" vs Instagram "Follow / Link in bio").

## 1. Technical QC (each file measured separately)

| File | Length | Loudness | True peak | Black frames | Frozen holds (>2.5 s) | Decode errors | Frame 1 brightness |
|---|---|---|---|---|---|---|---|
| EN · YouTube | 2:51.9 | −14.7 LUFS | −2.3 dBTP | 0 | 0 | 0 | 110 |
| EN · Instagram | 2:51.9 | −14.7 LUFS | −2.4 dBTP | 0 | 0 | 0 | 110 |
| TE · YouTube | 2:52.6 | −14.7 LUFS | −1.6 dBTP | 0 | 0 | 0 | 110 |
| TE · Instagram | 2:52.6 | −14.7 LUFS | −1.6 dBTP | 0 | 0 | 0 | 110 |

- **Under 3:00:** EN by 8 s, TE by 7 s. Narration is at its natural pace (no speed change).
- **True peak:** all four meet the −1 dBTP ceiling.
- **Mix:** the music is ducked about 20 dB under the voice and the SFX are sidechained to it.
- **Layout check** (`layout.check()` every 0.5 s across the whole video, both languages): 0 frames with defects in the final.
  - The first full pass found 46 EN frames and 5 TE frames with defects, and all were fixed:
    - labels within 40 px of the frame edge (AGRA, BUXAR);
    - the CARNATIC label under the "French did it first" card;
    - the Swally label crossing the 1613 card.
- **Sharpness:** every scene is drawn at output size or shown on native pixels (no picture is enlarged).
  - The lowest Laplacian scores are the map scenes: TE Buxar 204, EN hook counter 328. These are flat vector maps and a dimmed card, which is expected and not soft.
- **Frozen holds:** the first Telugu render had two 3 s holds, at the start of the southern wars (57 s) and "Calcutta seized" (98 s). Both now have motion:
  - in the wars: the decade written large, drifting, and an ink ring drawn round the Coromandel coast;
  - at Calcutta: a slow amber halo over the city.
  - The fixed windows were re-rendered and spliced frame-exactly, and all checks were run again.

## 2. Creative QC (watched as moving video: full contact sheets every 1–1.5 s, first 3 s frame by frame, phone size at 390 px)

**Composition: full-frame direction applied to every scene, varied per scene**

| Scene | How the frame is used |
|---|---|
| Hook | Jahangir's court fills the frame on native pixels → year counter 1608→1757 → Fort William on a soft backdrop of itself |
| 1608–1619 (EN) | Edge-to-edge west-India map: Surat and Agra pins, the road drawn, the Swally ships, the 1613 approval card low in the frame. Roe is shown on a close native crop of the darbar ("Roe is not shown") |
| 1608 → 1613 (TE) | The simplified intro: two big marks, **1608 · అనుమతి కోరారు → 1613 · ఆమోదం**, with Roe as a small secondary line |
| 1686 | India map: war lines, LOST, then the three terms on a separate card ("to trade again, the Company had to…"); 1690 Calcutta pin |
| 1717 | Tall native farman panel (labelled as an example) with the four terms stacked beside it, then a full-height river: the Company boat with its pass, then private boats with the same pass as the toll-post lamp dims |
| Wars | South-India map: Fort St George high, then sepoys marching up from the bottom edge in rows that skip the caption line; thrones with rival claimants |
| Lesson | A vertical split screen, FAILED vs PAID, with the right half filling amber from the bottom |
| 1756 | Fort William high, then the Bay of Bengal map: Calcutta taken, the army route from Madras with a ship |
| Plassey | The Company small and high; the Nawab's 100 dots march up from the bottom across a field to the bottom edge. Mir Jafar's cavalry turns grey, slides out left and down, and the rest closes right, leaving a clear gap. Then Hayman's painting at full height, panning from Clive to Mir Jafar |
| Buxar / diwani | India map, Buxar pin, Bengal–Bihar–Orissa hatched and labelled DIWANI · REVENUE-COLLECTION RIGHTS (not a conquest; area approximate); West's c. 1818 painting as an inset |
| Payoff | Top to bottom: bullion → chintz → Bengal's fields, which light up after 1765 while coins rise into the same cloth |
| Question | The completed season line runs down the frame and off the bottom edge |
| Tease | The same line runs into the EIC arms |
| Slide | Season 1 complete: six episodes ticked, the film card, then Subscribe or Follow |

**Readability at phone size**
- Secondary labels are now 26 px or more and kickers 31 px; Telugu labels are about 1.2× larger.
- The coin label reads "COIN: ILLUSTRATIVE RUPEE / MINTED IN SURAT, INDIA" at 26 px.
- Telugu fonts have no ≈ or → glyphs, so those labels spell out దాదాపు or use a dash. No empty-box glyphs remain.

**Caption collisions**
- Captions carry a soft local shadow.
- Moving dots and coins are softened inside the caption line.
- The sepoy rows were moved off the caption line after the first full render (they crossed it).
- No caption sits on an archive picture panel. The full-height Hayman painting has captions over it with the shadow, which reads clearly.

**Transitions:** clean cuts between exhibits (no cross-dissolves between documents); map scenes open with the map and season line already in place.

**Historical labels** (as approved in scene sheet v2):
- 1608 ASKED vs 1613 APPROVED.
- Jahangir's court c. 1620 (not the 1608 meeting).
- Plassey figures from the National Army Museum; 1 dot ≈ 500 men.
- Hayman c. 1760; West c. 1818, a later idealised image.
- Diwani shown as revenue-collection rights.
- Spices → textiles by the late 1600s.
- Silver shown as bullion; the Surat rupee labelled illustrative.

## 3. Changes from scene sheet v2 (flagged for your review)
1. **The Aurangzeb farman moved from the 1686 scene to the 1717 scene.** The pardon/fine/promise terms are now on their own card in the 1686 scene with no document near them. The farman appears only when the narration says "a farman", labelled **EXAMPLE: A FARMAN OF AURANGZEB · NOT THE 1717 GRANT**.
2. **Archive pictures that can't fill the frame sharply** (Fort William, the farman) sit on a heavily blurred, darkened copy of themselves as background texture. The picture itself is always on native pixels.
3. **The cloth panel is the Met's CC0 chintz** (the earlier candidate was CC BY-SA, not the Met).
4. **Two motion elements added** to remove Telugu holds: the drifting decade text with a coast ring in the wars scene, and the halo over Calcutta. Both appear in English too.

## 4. Sound
- Real recordings from `sfx/` only:
  - court ambience;
  - harbour waves and ship creak at Swally and on the Madras route;
  - soft footsteps and very low drums under the sepoy drill;
  - low distant drums and battlefield rumble under Plassey;
  - pins, paper, quill, page turns, coins at 1765;
  - the real click and bell on the slide.
- `cannon_distant` is used once, very low, at Swally (EN only). Its provenance is unverified, so no licence is claimed (owner-cleared Nov 10).
- Music: *where_the_river_bends*, ducked, with a small lift under the payoff.

## 5. Delivered with this report
- Four videos.
- Covers `cover_GS6_{EN,TE}_{YT,IG}.jpg` (Jahangir darbar, full-bleed on native pixels; "FROM PERMISSION / TO TAXES").
- `GS6_Short_Post_Copy.md` (counted limits inside).
- Contact sheets and phone-size sheets in `qc/`.
