# GOLDEN SPARROW · 4/6 · "Follow the money" · scene sheet v1 (actual voiced timings, Nov 10)
Runtime (voice + end slide + loop): EN 1:49.0 · TE 2:15.5. Both under 3:00.
Credits used: 1,037 (EN 418 · TE 619), 15 lines, one take each. All saved to voice_lib (tag gs_s4).
Script: v3 as approved (TE Madanna–Akkanna line replaced in full; no accurate existing recording).
Splices: all at sentence boundaries, checked by ASR (EN small.en, TE whisper-telugu-medium).

**Assets.** Approved GS film images and archive only. No new images or paid tools.
- Archive: FARMAN (Aurangzeb farman, National Museum), PD12 Company arms, PD18a Surat rupee, PD08 Akbarnama, PD09 Mundy famine page, PD06 Masulipatnam (Rijksmuseum), CC04 cracked earth, PD10 Cantino 1502, PD11 Roteiro.
- Illustrations: G16 empty bowl, G18 revenue office, G19 Surat counting-house, G20 empty loom, G21 bale.
- Tools: gsmap animated maps, the characters/cartoon styles, `sfx/`.

**Sharp-pictures plan.** The GS illustrations are only 1920×1080 or 1672×941, so they are never stretched to full 9:16 height. That would be a 1.8–2× upscale, the GS 3/6 mistake.
- Each illustration appears as a **native-pixel panel** (≤1.0 source px per output px), 1080 px wide, on a designed paper/ink background.
- Motion inside a panel is a pan across real pixels, never a zoom past 1.0.
- Full-screen use is limited to archive sources tall enough for 1920 px (PD08, PD09, PD06, PD10, PD11, CC04, CC01).
- Diagrams and maps are drawn at 1080×1920.
- QC: Laplacian sharpness per scene on the final files.

**Motifs.**
- (a) **One coin**: it drops at "Follow the money" and travels the whole chain.
- (b) **The cotton thread**: it runs from the empty loom out to the ports and the sea.

| Line | EN | TE | On screen (shown on the word) | Style | SFX |
|---|---|---|---|---|---|
| Hook | 0:00.0–0:06.5 | 0:00.0–0:08.4 | Frame 1 is bright: a grid of 100 squares, ~24 lit gold, "~1/4 OF WORLD OUTPUT · c.1700 · MADDISON ESTIMATE". On "made it" the squares fold into a woven cloth bale. On "stay poor" a hard cut to G16, the weaver's empty bowl (native panel), with a "?" | Maths Diagram → native panel | tick per lit square, sub_knock on "poor" |
| Q1 Chelli | 0:06.8–0:09.9 | 0:08.7–0:12.5 | Chelli asks; chip **1/3 THE MONEY · డబ్బు** | Cartoon Explainer | ui_pop (chip) |
| "Follow the money" | 0:10.3–0:11.3 | 0:12.9–0:14.1 | One coin drops from the top and lands in a field. The camera follows it, and this coin is the motif for the whole chain | Kinetic text + coin | coin_flutter → coins_clink |
| 4.6a money chain | 0:11.6–0:25.0 | 0:14.4–0:32.8 | **Connected vertical chain** built step by step on the words. FARMER (field tile) "pays land revenue" → COLLECTORS · LOCAL LORDS (a slice of the coin peels off: "keep a cut") → STATE TREASURY (chest opens) → ARMIES · COURTS (coins flow out) → BANKERS "lend to everyone" (arrows to every tile). At "a third to a half" a gauge fills 1/3→1/2 on the field. Labels: **ASSESSED REVENUE DEMAND · HISTORIANS' ESTIMATE · VARIED BY PLACE AND TIME · OFTEN PAID IN CASH** and **ILLUSTRATIVE**. The farmer hands over a coin, not a sack of grain | Isometric (Python styles) | coins_clink per step, marker on gauge |
| Farman | 0:25.3–0:31.8 | 0:33.1–0:39.5 | A COMPANY tile joins the chain (PD12 arms). The real Aurangzeb farman (archive, native size, as a card) slides in. A seal stamps on "farmans", then two tags write on: TRADING RIGHTS · PRIVILEGES. Caption: "A MUGHAL FARMAN · NATIONAL MUSEUM, NEW DELHI · EXAMPLE OF THE DOCUMENT" | Paper-Cut + archive evidence card | paper_slide, stamp, quill_writing |
| TE only: Madanna & Akkanna | none | 0:39.9–0:53.5 | Small Telangana map: pin HANUMAKONDA → line to GOLCONDA. Two cards appear in turn: (1) MADANNA · CHIEF MINISTER · REVENUE with G18 (revenue office, native panel), and the chain's coin passes through his ledger; (2) AKKANNA · COMMANDER-IN-CHIEF with a drawn banner and army icon, so the account books are not shown for him. Tag: ILLUSTRATION · NOT PORTRAITS · under ABUL HASAN QUTB SHAH | Animated map (gsmap) + Paper-Cut cards | map_unfold, pin_push, page_turn |
| 4.8a Virji Vora | 0:32.1–0:43.0 | 0:53.9–1:04.4 | G19 Surat counting-house as a native panel, panned slowly. The PD18a Surat rupee spins in. Tag SURAT · VIRJI VORA. On "lent money… again and again", loan arrows pulse VIRJI VORA → ENGLISH COMPANY, with the count rising 1, 2, 3. On "richest merchant": a quote card "THE COMPANY'S OWN RECORDS" | Native panel + Isometric flow arrows | coins_clink ×3, page_turn |
| Virji: "needed each other" | 0:43.3–0:45.9 | 1:04.7–1:09.1 | Two-way diagram, MERCHANTS ⇄ RULERS. → "credit · trade · customs revenue"; ← "protection · permissions". The arrows lock into a balanced loop | Maths Diagram | swoosh_slow |
| Q2 Chelli | 0:46.3–0:48.6 | 1:09.4–1:12.4 | Chip **2/3 THE POWER · అధికారం** | Cartoon Explainer | ui_pop |
| 4.2 kingdoms | 0:49.0–0:56.7 | 1:12.8–1:22.6 | **Animated historical map** drawn at 1080×1920. "Rose and fell": regional borders flicker on and off. "Deccan sultanates, like Golconda": the middle Deccan fills, pin GOLCONDA. "Mughal empire kept pushing south": a red Mughal front advances south in steps, with date ticks 1600s→1680s. Tag: APPROXIMATE EXTENTS | Animated map (gsmap) | map_unfold, woosh_deep per advance |
| 4.4 (EN only) | 0:57.0–1:05.7 | none | PD08 Akbarnama (full-screen, native), tag AKBAR'S COURT · AKBARNAMA. On "Todar Mal measured the land": a field from above, where a measuring rope and survey grid draw across it plot by plot, then a revenue figure appears in each plot. Tag ZABT · REVENUE SET BY SURVEY | Archive → Maths Diagram (process shown on the object) | scribble, tick per plot |
| "Kings come and go. The system lasted." | 1:06.0–1:09.0 | 1:22.9–1:27.2 | Crowns swap above, three times. Underneath, the same money chain keeps moving without stopping. Text: THE SYSTEM LASTED | Domino Reveal (crowns) over Isometric chain | sub_knock per crown, coins under |
| Q3 Chelli | 1:09.2–1:10.9 | 1:27.4–1:29.2 | Chip **3/3 THE FAMINE · కరువు**. Music drops away | Cartoon Explainer | none |
| 4.9 rains failed | 1:11.3–1:16.2 | 1:29.6–1:34.4 | Rain stops over the field and the field cracks (CC04, full-screen native, slow pan). Split: the treasury chest stays full and lit at the top; at the bottom the farmer's and weaver's tiles go grey. Tag FAILED RAINS · SCARCITY. No tax collector in this scene | Film cinema + split | wind_ambience (low), heartbeat_slow (very low) |
| 4.10 famine 1630–32 | 1:16.5–1:31.4 | 1:34.7–1:54.6 | Map: GUJARAT and DECCAN glow dark red, 1630–1632. PD09 Mundy page (real, full-screen, native), with the famine passage underlined as he is named: PETER MUNDY · TRAVELS · EYEWITNESS. "Estimates run into the millions": a sober number line with the label **HISTORICAL ESTIMATES · UNCERTAIN**. "Weavers died… or fled": G20 empty loom (native panel), dust in light. Restrained, no gore, no bodies drawn | Animated map + archive evidence + native panel | near silence, single low bell at the loom |
| TURN land / ports | 1:31.7–1:38.7 | 1:54.9–2:03.0 | The thread lifts from the empty loom. "Land brought rulers revenue": a quick recap of field → treasury. "India's ports": PD06 Masulipatnam (real 17th-c. painting, native, full-screen) with ports pinned SURAT · MACHILIPATNAM. "Trade across the seas": a globe of sea routes from those ports to Persia, Arabia, Southeast Asia and Europe, with the thread riding the arcs | Archive → Remotion **Globe Arcs** (demo:false, sourced routes) | harbour_waves, swoosh_slow |
| Tease | 1:39.0–1:43.6 | 2:03.2–2:08.8 | Large **EARLIER · 1498** stamp. A Split-Flap year board runs backwards 1632 → 1498. Then PD10 Cantino planisphere (1502) or PD11 Roteiro page with "WHO SHOWED VASCO DA GAMA THE WAY?" | Remotion **Split-Flap** + archive card | ticker_run, stamp |
| Series slide | 1:43.8–1:45.8 | 2:09.0–2:11.0 | ✓ 4/6 YOU'RE HERE · NEXT 5/6 · EARLIER: 1498. YT: FULL FILM · RELATED VIDEO + Subscribe. IG: FULL FILM ON YOUTUBE · LINK IN BIO + Follow | Series slide + cta_card | real click, bell (YT) |
| Loop | 1:45.8–1:48.7 | 2:11.0–2:15.2 | Cross-fade back to frame 1 (the 24% squares) | Loop | none |

**Collections.** Remotion effects (Globe Arcs, Split-Flap) are rendered as separate silent MP4s and composited in. The Python styles are Isometric, Paper-Cut, Maths Diagram, Domino Reveal and Cartoon Explainer, plus the film's gsmap.

**Accuracy labels on screen.**
- MADDISON ESTIMATE
- ASSESSED DEMAND · VARIED · OFTEN PAID IN CASH · ILLUSTRATIVE
- EXAMPLE OF THE DOCUMENT
- ILLUSTRATION · NOT PORTRAITS
- APPROXIMATE EXTENTS
- HISTORICAL ESTIMATES · UNCERTAIN
- DRAMATIZED tag on every AI illustration

**Famine sound.** Music ducks out at Q3 and returns softly at TURN.

**Process.** Two motion previews with sound in EN+TE before the full render: the money chain (4.6a→Farman) and the famine→ports turn (4.9→TURN).
