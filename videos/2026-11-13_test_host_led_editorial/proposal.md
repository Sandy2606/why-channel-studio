# WHY? Host-Led Editorial Documentary: test proposal v2

- Rules: main `b0c217fbcceb4211a141733e6fd7f13d5477a294` (Mode A, Nov 13, 2026).
- Status: **PROPOSED**. The design was approved in principle on Nov 13, with six corrections (applied below). This is a preview under WF-02, not a rule change. No playbook change, no host library, until the finished preview passes review (WF-05).
- Stage: equivalent of WF-01 steps 3 + 7. Render waits for the host artwork (WF-01.9).
- Reference studied: a 47 s Instagram explainer reel. We borrow **techniques only**. No shots, speech, characters, wording or sequence are copied.

## v1 → v2 corrections (user, Nov 13)
| # | Correction | Applied in |
|---|---|---|
| 1 | Keep the original approved voice lines. Show on screen that ≈18% is **relative to unseeded control clouds, under the Solapur experiment's conditions** | §1, shot 2 |
| 2 | No highlight over text that isn't on the page. Use an **original, source-cited evidence card**; a real results passage only if verified and its reuse rights are clear. Never assume a full copyrighted page is free | Shot 2, §3 T4, §6 |
| 3 | Minimal host: reuse the approved H_ref05 artwork; natural mouth movement, a head shake, a point. **No rig build, no pose library** | Shot 1, §3 T1, §5 |
| 4 | Protect the natural Telugu delivery; never rush it to hit 20 s | §1 timing |
| 5 | The amber portrait card is a **separate demo**, not part of the Solapur scene | §3 T2 |
| 6 | List the exact missing host files; confirm repo visibility before any likeness asset goes to GitHub | §7 |

---

## 1. The test sequence (9:16, EN and TE)

Topic: the Solapur turn in *Why Can't Delhi Make It Rain?* (Ch. 5): approved script, approved voice clips, used **unchanged** (→ CR-03 exact reuse). **0 ElevenLabs credits.**

| # | Line (approved script, unchanged) | EN clip (s) | TE clip (s) |
|---|---|---|---|
| L1 | EN: "So is cloud seeding just… fake? … Not at all. … In the right place, it's worked."<br>TE: "అంటే cloud seeding అంతా బూటకమా? … అస్సలు కాదు. … సరైన చోట అది పని చేసింది." | `en/920430065cbb` 6.35 | `te/bdf89bee036c` 6.11 |
| L2 | EN: "The result: about 18 percent more rain, over 100 square kilometres downwind, in the two hours after seeding."<br>TE: "ఫలితం: seeding తర్వాత రెండు గంటల్లో, గాలి వెళ్లే దిశలో 100 చదరపు కిలోమీటర్ల మేర, దాదాపు 18 శాతం ఎక్కువ వర్షం." | `en/43a3e74e4ef8` 7.71 | `te/2beb39b8b575` 9.33 |
| L3 | EN: "So why can't Delhi just copy Solapur?"<br>TE: "మరి ఢిల్లీ సోలాపూర్‌ను ఎందుకు copy చేయలేకపోతోంది?" | `en/737199a396cd` 3.00 | `te/954c70a18600` 3.87 |

**Timing (correction 4):**
- Raw: EN 17.1 s, TE 19.3 s.
- The ED-01 edit removes only noise and dead air between lines. No speed-up, no time-stretch, and no cuts inside the delivered pauses ("… Not at all. …").
- Each language keeps its own timeline. Telugu is longer and gets the time it needs.
- If the natural Telugu edit lands slightly over 20 s, it stays natural; I'll report the exact length rather than trim it.
- The film's in-between line "That's real. … Peer-reviewed, and published." is not voiced in this preview, and no approved line is altered. The peer-review fact is carried by the citation on the evidence card.

**Science (correction 1)**, from C15 in the Delhi Rain brief: Prabhakaran et al., *BAMS* 104(11), Nov 2023, doi:10.1175/BAMS-D-21-0291.1. Verified Nov 11 (→ RS-01).
- 18.42% ± 2.57% **relative** increase.
- Seeded vs unseeded clouds: randomised, 150 seeded / 122 unseeded samples.
- Hygroscopic seeding at the base of growing warm-based convective clouds.
- Solapur rain-shadow region, 2017–19.
- Over 100 km² downwind, 2 h after seeding.

## 2. Scene sheet (styles named per shot, → DIR-01)

EN timecodes, TE in brackets; final times come from the edited voice.
- Music: `the_last_threshold.m4a`, the approved Ch. 5 cue, low and calm (→ MU-02).
- SFX: real recordings from `sfx/catalog.json` only (→ SD-01). No whooshes.

**Shot 1 · 0.0–6.3 (0.0–6.1) · L1 · T1 Host Story-Turn, minimal**
- On screen: the host from the approved H_ref05 artwork, in **one framing**: a medium shot in the existing approved setting.
- Mouth: moves naturally with L1 only (→ DIR-05).
- On "Not at all / అస్సలు కాదు": a small **head shake**.
- On "In the right place / సరైన చోట": he **points** off-frame toward where the evidence will appear, which motivates the cut.
- One keyword beside him: "FAKE?" (TE "బూటకమా?"). A marker line strikes it out on "Not at all" (→ LAY-04: it answers the question visually).
- SFX: `marker.wav` on the strike.

**Shot 2 · 6.3–14.0 (6.1–15.4) · L2 · T4 Evidence Reveal, as an original evidence card in the Python 3D Data Chart style** (the style already agreed for the Delhi Rain result, scene 37)
- Full-frame ink background with a subtle paper grain.
- Two bars side by side: **UNSEEDED CLOUDS** set at an index of 100, and **SEEDED CLOUDS** rising to ≈118 on "18 percent".
- Bar labels (TE): సీడ్ చేయని మేఘాలు / సీడ్ చేసిన మేఘాలు.
- Headline label: **≈18% MORE RAIN · RELATIVE TO UNSEEDED CLOUDS** (TE: సీడ్ చేయని మేఘాలతో పోలిస్తే ≈18% ఎక్కువ వర్షం).
- Condition chips land on their spoken words:
  - **100 KM² DOWNWIND** · **2 H AFTER SEEDING**
  - TE: గాలి వెళ్లే దిశలో 100 చ.కి.మీ. · 2 గంటల్లో
- One more line underneath: **SOLAPUR · 2017–19 · GROWING MONSOON CLOUDS · RANDOMISED** (TE: సోలాపూర్ · 2017–19 · పెరుగుతున్న monsoon మేఘాలు · random ఎంపిక).
- Citation strip, readable for the whole shot: **PRABHAKARAN ET AL. · BAMS · NOV 2023 · PEER-REVIEWED · DOI 10.1175/BAMS-D-21-0291.1**.
- No document image and no highlighter.
- SFX: `paper_slide.wav` as the card enters, `sub_knock.wav` as the seeded bar lands, `tick.wav` per chip.

**Shot 3 · 14.0–17.0 (15.4–19.3) · L3 · T3 WHY? Question Reveal**
- Hard cut to ink #0A0A0A with a faint amber halftone field (the brand dot repeated, ~6 %).
- On "So / మరి" the amber dot lands, the round-stroke "?" draws up from it, and WHY locks beside it.
- Space Mono kicker: **DELHI vs SOLAPUR** (TE ఢిల్లీ vs సోలాపూర్).
- Holds as a question: no "?"→"!" here (→ BR-05).
- SFX: `sub_knock.wav` on the dot (felt, not heard); `marker.wav`, soft, on the "?" stroke.

Around all three shots:
- Captions: word by word, active word in amber, y≈1446 (→ LAY-02). They yield while the host's face, mouth or gesture is in their path, and never cover the chart, chips or citation.
- Series tag: "DELHI RAIN · TEST", marked as a preview (→ BR-03).
- Telugu is laid out on its own (→ BR-06, BR-02): longer labels stack on two lines, chips get their own timing, and the glyph check runs on every Telugu still.

## 3. The treatments

### T1 Host Story-Turn: minimal for the first test
- **In this test:** the existing approved H_ref05 artwork, one framing, natural mouth movement, one head shake, one point. Nothing else.
- **Not in this test:** extra framings, blink and eyebrow systems, gesture sets, a rig or a pose library. Those are decided only after the preview passes.
- If an existing frame lacks the head shake or the point:
  - I'll name the one or two missing poses and send exact Gemini prompts (free) first.
  - No paid generation (→ CR-01).
  - The likeness check stays with you.
- Principle carried forward: the host appears only on a question, a twist, an emotional beat or an explanation, never on a timer.

### T2 Amber Portrait Card: separate demonstration (not in the Solapur scene)
- A stand-alone 4–5 s demo card, after the preview, on a subject you choose. It must be a public-domain or licensed portrait, with its licence logged.
- Design: framed portrait, 10 px amber #FFB224 border with a 1 px cream inner line, on ink with the halftone field.
- Name in Archivo Black (cream); role and date in Space Mono (amber date); source/licence chip in the corner.
- `paper_drop.wav` as it enters, `tick.wav` on the date. Low-resolution portraits follow LAY-05.

### T3 WHY? Question Reveal
- Built only from existing brand parts: the amber dot, the round-stroke "?" and the WHY wordmark. 1.5–3 s.
- Use: at most one per Short, two or three per film, only for a real central question.
- The "?"→"!" turn stays reserved for the why, the payoff and the ending (→ BR-05).

### T4 Evidence Reveal
- **Default: an original, source-cited evidence card.** We redraw the verified numbers and conditions in our own design, with a full citation strip. No reproduced page.
- **A real document or passage, only when all three hold:**
  1. the exact passage is verified in the source;
  2. its reuse rights are confirmed and logged (→ RS-07, ART-08);
  3. any highlight sits only on text that is actually there.
- Comparisons are always labelled with their baseline (relative vs absolute) and their conditions.
- Camera: one restrained move at most, within native resolution (→ LAY-05).

### T5 Topic-Based Visual Loop: design only, not in this test
- The opening and closing frames share one meaningful object (for Delhi Rain, Anu's paper boat).
- Fits FMT-06 unchanged.

### T6 Expressive Voice Editing
- Library first: this test is 100% reuse.
- ED-01 trims only noise and dead air. Each language keeps its natural delivery and its own timeline.
- New lines only when no exact match exists, priced first (→ CR-01, CR-02).

## 4. Current approach vs proposed

| | Current (Shorts v3 / Delhi Rain film) | Proposed host-led editorial |
|---|---|---|
| Who tells the story | Narrator voice over scenes; the host appears in the Delhi Rain film | Host on camera at turns; scenes and evidence carry the facts |
| Proof on screen | Clipping flashes, chips such as "BAMS 2023" | An original evidence card: comparison with its baseline, conditions and full citation |
| Question moments | Spoken; the logo at why/payoff/ending | A full-frame WHY? reveal at the one central question |
| Rhythm | Visual change on information | Same rule; the host's gesture motivates the cut to evidence |
| Risk | Proven, lower cost | Lip-sync and gestures must look natural or they hurt trust, so the first test stays minimal |

## 5. Implementation and library fit (local, free)

| Component | For this test | Built from |
|---|---|---|
| Host shot | A test-only script in this folder; nothing added to `pipeline/` yet | The existing approved H_ref05 frames and the existing host animation code (§7); faster-whisper word timestamps |
| Keyword strike | A test-only helper | style_v2 `layout.py` fonts and colours; `marker.wav` |
| Evidence card | The existing Python **3D Data Chart** style (`pipeline/styles/chart_3d.py`) | C15 facts; style_v2 chips |
| WHY? reveal | A test-only script | The approved logo geometry |

- The nine Python styles and the 30 Remotion effects stay separate and unchanged (→ MO-04).
- New shared modules (`pipeline/host/`, `pipeline/editorial/`) are proposed only after the preview passes.

## 6. Licences (each item on its own)

| Item | Status |
|---|---|
| Evidence | **No third-party page or passage is reproduced.** An original card with a citation. The facts aren't copyrightable; the citation gives credit |
| Voice | Your own clones, from the existing library |
| Music | Your Gemini track (AI music, → PUB-05 disclosure check per upload) |
| SFX | Catalog entries (Mixkit Free / CC0, already logged) |
| Host | Your AI-generated likeness of yourself; disclosure assessed per upload (→ PUB-05) |

## 7. Host assets: what's missing, and where they may go

**Checked Nov 13:**
- The studio repo on `main`, `pro-system` and `feature/remotion-effects`.
- This workspace.

None of them contains any host image, pose or host animation code.

What the test needs, by role. File names are as found in session records; the exact list must be confirmed from the source workspace:

| Needed | Purpose | Where it was last seen |
|---|---|---|
| **H_ref05**: the approved host master image | Likeness and look | The Delhi Rain host work, in another chat's workspace (not in the repo) |
| The host's existing mouth frames or mouth-movement setup | Natural mouth movement | Same |
| An existing head-shake pose or sequence | Shot 1 | Same; may not exist yet |
| An existing pointing pose | Shot 1 | Same ("pointing at the last card" appears in the Delhi Rain host shots) |
| The approved host setting/background plate | Shot 1 | Same |
| Host animation code (seen as `host_poc/final.py` and its modules) | Compositing, lip-sync | `/home/claude/delhirain/host_poc/` in that chat's workspace; it disappears when that session ends |

**Repository visibility, checked Nov 13 via the GitHub API: `Sandy2606/why-channel-studio` is PUBLIC.** Anyone can see and download its files.
- **No likeness asset (H_ref05, poses, mouth frames) goes to this repo while it is public.**
- Collaborator access couldn't be listed from here; GitHub blocks that API through this proxy.
- Options, your choice:
  1. **Upload the host files directly into this chat** for the test. They stay in this workspace only. Simplest for the preview.
  2. Make `why-channel-studio` private (GitHub → Settings → Danger Zone → Change visibility). Then push the host files there.
  3. A separate **private** repo for likeness assets only, linked from the studio repo.
- The non-likeness host animation code can go to the public repo after review, if you want it there.

## 8. Next steps (normal workflow)
1. You choose how the host files get here (§7) and send them.
2. I confirm which poses exist. If the head shake or the point is missing, I send one or two free Gemini prompts, and you check the likeness.
3. Stills only where the style is new, then the 10–20 s EN and TE previews with sound (→ WF-02), then QC and an honest report.
4. The portrait-card demo is a separate item after the preview.
5. No host library and no playbook change until the finished preview passes review.
