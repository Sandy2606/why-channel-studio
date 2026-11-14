# WHY? Host-Led Editorial Documentary: test proposal v1

- Rules: main `b0c217fbcceb4211a141733e6fd7f13d5477a294` (Mode A, Nov 13, 2026).
- Status: **PROPOSED**. This is a test, not a rule change (WF-02 preview). Nothing in the playbook changes until the user approves the preview (WF-05).
- Stage: equivalent of WF-01 steps 3 + 7 (script and scene sheet for the 10–20 s preview). No render before the user approves and the assets arrive (WF-01.9).
- Reference studied: a 47 s Instagram explainer reel (presenter + archival footage + portrait cards + "WHY?" card, ~23 cuts). We borrow **techniques only**. No shots, speech, characters, wording or sequence are copied.

---

## 1. The test sequence (EN ≈ 17 s · TE ≈ 19 s, 9:16)

Topic: the Solapur turn in *Why Can't Delhi Make It Rain?* (Ch. 5). It is already researched, approved and voiced, so the test costs **0 ElevenLabs credits** (→ CR-03 exact reuse).

| # | Line | EN clip (s) | TE clip (s) |
|---|---|---|---|
| L1 | EN: "So is cloud seeding just… fake? … Not at all. … In the right place, it's worked."<br>TE: "అంటే cloud seeding అంతా బూటకమా? … అస్సలు కాదు. … సరైన చోట అది పని చేసింది." | `en/920430065cbb` 6.35 | `te/bdf89bee036c` 6.11 |
| L2 | EN: "The result: about 18 percent more rain, over 100 square kilometres downwind, in the two hours after seeding."<br>TE: "ఫలితం: seeding తర్వాత రెండు గంటల్లో, గాలి వెళ్లే దిశలో 100 చదరపు కిలోమీటర్ల మేర, దాదాపు 18 శాతం ఎక్కువ వర్షం." | `en/43a3e74e4ef8` 7.71 | `te/2beb39b8b575` 9.33 |
| L3 | EN: "So why can't Delhi just copy Solapur?"<br>TE: "మరి ఢిల్లీ సోలాపూర్‌ను ఎందుకు copy చేయలేకపోతోంది?" | `en/737199a396cd` 3.00 | `te/954c70a18600` 3.87 |

- Raw total: EN 17.1 s, TE 19.3 s. After the ED-01 edit (silence and breath trims), both land inside 10–20 s.
- Not reused: "That's real. Peer-reviewed, and published." (EN 3.8 s / TE 4.3 s). It would push TE past 20 s. Its job is done on screen by the PEER-REVIEWED stamp in T4 (an editorial label that adds credibility, → LAY-04).
- Facts: C15 in the Delhi Rain brief (Prabhakaran et al., *BAMS* Nov 2023, doi:10.1175/BAMS-D-21-0291.1): 18.42% ± 2.57% relative increase, 100 km² downwind, 2 h after seeding, randomised. Already verified Nov 11 (→ RS-01).

## 2. Scene sheet (styles named per shot, → DIR-01)

EN timecodes; TE in brackets. Music: `the_last_threshold.m4a` (the approved Ch. 5 cue), low and calm under the voice (→ MU-02). All SFX are real recordings from `sfx/catalog.json` (→ SD-01). No whooshes.

| Shot | Time | Line | On screen | Treatment / style | SFX |
|---|---|---|---|---|---|
| 1a | 0.0–2.4 (0.0–2.3) | L1 "So is cloud seeding just… fake?" | **Host, medium close-up (MCU)**, studio storyboard wall soft behind him. He leans in slightly, eyebrows up on "fake". "FAKE?" (TE "బూటకమా?") pops to his left in Archivo Black, cream, amber "?" | **T1 Host Story-Turn** · framing A (MCU) | none (voice alone opens) |
| 1b | 2.4–6.3 (2.3–6.1) | "…Not at all. … In the right place, it's worked." | **Cut to medium shot (MS)**: small head shake + open palm on "Not at all". A marker stroke crosses out "FAKE?". On "it's worked" he turns toward the wall and points; the wall's Solapur card catches light (motivates the cut) | T1 · framing B (MS) + **keyword strike** | `marker.wav` on the strike |
| 2 | 6.3–14.0 (6.1–15.4) | L2 | **The real BAMS first page** slides onto the dark desk, full frame. Restrained push-in (≤4 %, within native resolution, → LAY-05). Amber highlighter sweeps the exact result sentence as it is spoken. Callouts land on their words: **≈18% MORE RAIN** → **RELATIVE** → **100 KM²** → **2 H AFTER SEEDING** (TE: ≈18% ఎక్కువ వర్షం → సాపేక్షంగా → 100 చ.కి.మీ. → 2 గంటల్లో). Source strip bottom-left, always readable: "PRABHAKARAN ET AL. · BAMS · NOV 2023 · © AMS". At the end: **PEER-REVIEWED** stamp (TE: PEER REVIEW అయిన పరిశోధన) | **T4 Evidence Reveal** | `paper_slide.wav` in, `scribble.wav` on the highlight, `sub_knock.wav` on 18%, `stamp.wav` on the stamp |
| 3 | 14.0–17.0 (15.4–19.3) | L3 | **Hard cut to ink #0A0A0A** with a faint amber halftone field (the brand dot repeated, ~6 % opacity). On "So/మరి" the amber dot lands; the round-stroke "?" draws up from it; WHY locks beside it as the wordmark. Space Mono kicker under it: **DELHI vs SOLAPUR** (TE: ఢిల్లీ vs సోలాపూర్). Holds as a question: no "?"→"!" here, because the answer comes later (→ BR-05) | **T3 WHY? Question Reveal** | `sub_knock.wav` on the dot (felt, not heard) · `marker.wav` softly on the "?" stroke |

- Captions: word by word, amber active word, y≈1446 (→ LAY-02). They yield while the host's face or gesture is in their path, and never cover the source strip or the stamp.
- Series tag: "DELHI RAIN · TEST", marked as a preview, not a real episode number (→ BR-03).
- Telugu is laid out on its own (→ BR-06): longer callouts get a two-line stack; the evidence shot runs 1.3 s longer, so the TE highlight also takes in "Solapur, 2017–19" before the result. Glyph check on every Telugu still (→ BR-02).

## 3. The six treatments (designs)

### T1 Host Story-Turn System
- **Identity:** the locked H_ref05 host (olive overshirt, cream tee, dark jeans, cream sneakers, painterly). No new look.
- **When he appears:** only on a question, a twist, an emotional beat or an explanation that needs a face. Never on a timer. Typical: 3–4 appearances in a Short, more in a film at genuine turns.
- **Framings:** A = MCU (questions, emotion) · B = MS with hands (answers, gestures) · C = wide at the storyboard wall (connections, conclusions). Cuts between framings happen on the beat change inside a line, which reads as a real two-camera shoot.
- **Performance:** lip-sync from word timestamps + phoneme groups (6–8 mouth shapes), not RMS flapping (→ DIR-05); blink every 3–6 s with jitter; 3 eyebrow states (neutral / raised / concerned); 4 gestures (open palm, point-to-wall, head shake, lean-in). Each gesture is a 2–4-pose sequence with natural easing; no bouncing, warping or zooms (Delhi Rain Nov 11 note).
- **Keyword beside the host:** at most one per appearance, and only when it adds something the voice doesn't (here: the strike-through answers the question visually).

### T2 Amber Portrait Card (not in this test; design only)
- Framed real portrait (public-domain or licensed), 10 px amber #FFB224 border with a 1 px cream inner line, on ink with the halftone dot field.
- Name in Archivo Black (cream), role and date in Space Mono (amber date). Source/licence chip in the corner.
- Enters with `paper_drop.wav`; the date ticks in with `tick.wav`. Low-res portraits follow LAY-05 (native size, designed background).

### T3 WHY? Question Reveal
- Built only from existing brand parts: the amber dot, the round-stroke "?" and the WHY wordmark from the logo work. Total 1.5–3 s.
- Used only for a central question or the chapter's real turn: at most 1 per Short, 2–3 per film. The "?"→"!" turn stays reserved for the why, the payoff and the ending (→ BR-05).

### T4 Evidence Reveal System
- **Sources:** genuine documents only (papers, government pages, archival photos, quotes). Built from the real PDF or screenshot with `clipkit.py` (pdftotext bbox crops at 300 dpi, `methods/assets.md`).
- **Highlight:** the exact sentence spoken, swept in sync with the word timestamps. Callouts sit on the page next to their line.
- **Camera:** one slow move per document (push ≤4 % or a short lateral drift), always within native resolution.
- **Source strip:** author/outlet · date · licence, readable for the whole shot.
- **Licence:** checked per item and logged in the asset register (→ RS-07, ART-08).

### T5 Topic-Based Visual Loop (not in this test; design only)
- The opening and closing frames share one meaningful object. For Delhi Rain that's Anu's paper boat: dry on the sill in the hook, dry again on the final loop frame.
- Fits FMT-06 unchanged: series slide → loop line → last frame equals the first.

### T6 Expressive Voice Editing
- Library first (this test is 100 % reuse).
- The ED-01 edit; pacing per the approved model (questions and hooks quicker, explanations natural).
- Host lines get 0.15–0.25 s breath room before a cut, so a framing change never clips a word.
- New lines only when a script line has no exact match, priced first (→ CR-01, CR-02).

## 4. Current approach vs proposed

| | Current (Shorts v3 / Delhi Rain film) | Proposed host-led editorial |
|---|---|---|
| Who tells the story | Narrator voice over scenes; the host appears in the Delhi Rain film | Host on camera at turns; scenes and evidence carry the facts |
| Proof on screen | Clipping flashes, chips such as "BAMS 2023" | The actual page, highlighted line by line, with a stamp and source strip |
| Question moments | Spoken; the logo at why/payoff/ending | A full-frame WHY? reveal at the one central question |
| Rhythm | Visual change on information | Same rule, plus framing changes inside host lines |
| People in history | Painted scenes or photos | Amber portrait cards for named real people |
| Risk | Proven, lower cost | More craft per Short; lip-sync must look natural or it hurts trust |

## 5. Implementation and library fit (all local, free)

| Component | Where it goes | Built from |
|---|---|---|
| Host rig (framings, visemes, blinks, gestures) | `pipeline/host/` (new) | The host rig built for Delhi Rain (see blocker 1); faster-whisper word timestamps; cairo/PIL compositing |
| Keyword pop + strike | `pipeline/style_v2/` helper | `layout.py` fonts and colours; `marker.wav` |
| Evidence Reveal | `pipeline/editorial/evidence.py` (new) | `clipkit.py` crops; style_v2 highlighter; Remotion `paper-desk` / `headline` (with `photo`) as optional alternatives |
| WHY? reveal | `pipeline/editorial/why_reveal.py` (new) | The approved logo geometry from the intro animation |
| Portrait card, loop | `pipeline/editorial/` (later, after the test) | style_v2 + `sfx/` |
| Voice | `voice_lib/` reuse | ED-01 chain |

- The nine Python styles and the 30 Remotion effects stay separate and unchanged (→ MO-04).
- No new channel-wide rule. If the preview is approved, a proposal for the treatment's rules goes to the user first (WF-05).

## 6. Licences (each item checked on its own)

| Item | Status |
|---|---|
| BAMS article page | The AMS copyright notice grants permission to use figures, tables and brief excerpts in scientific and educational works, provided the source is acknowledged. A monetised channel is a grey zone for "educational works", so we show one page, briefly, with full credit. Confirm the notice on the PDF's first page before use; if the article is CC BY, record that instead. |
| Voice | Your own clones, from the existing library |
| Music | Your Gemini track (AI music, → PUB-05 disclosure check per upload) |
| SFX | Catalog entries (Mixkit Free / CC0, already logged) |
| Host | Your AI-generated likeness of yourself → disclosure assessed per upload (→ PUB-05) |

## 7. Costs
- ElevenLabs: **0 credits** (all lines reused).
- Images: possibly 4–8 extra host poses/mouth shapes if the existing set lacks them. Free in Gemini on your phone; I'll send exact prompts.
- Rendering: local, free.

## 8. Blockers and what's needed
1. **The H_ref05 host files are not on GitHub.** Main, `pro-system` and `feature/remotion-effects` have no host images or rig. They live in the other chat's workspace (where the Delhi Rain host film is rendering), which is wiped when that session ends. Needed: H_ref05 plus its pose/mouth set and rig code. Either ask that session to push them to the repo, or upload them here.
2. **The BAMS paper.** Send the PDF (IISc eprints link in C15) or a full-page screenshot. My fetch of the PDF needs your approval.
3. **Approval** of this script + scene sheet, or changes.
