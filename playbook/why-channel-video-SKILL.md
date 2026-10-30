---
name: why-channel-video
description: Produce a Why? channel explainer (Short or long, English + Telugu): research, script, edit voice takes, visuals list, full-screen v3-style render.
---

# Why? channel video production

Channel: "Why?" (YouTube @WhyEveryQuestionHasaStory, Instagram @whyeveryquestion) plus "Why? Telugu". Faceless explainers that answer a "Why…?" question.

## 0. Quality system (READ FIRST, applies to every video)
- **Target: every video scores at least 8/10** on the scorecard. If the pre-render self-check predicts less than 8, fix it before rendering.
- **After EVERY delivery, give a full, honest review with scores.**
  - Sample frames (every 1.5 s, plus the first 3 s at 3 fps) and look at them.
  - Run the QA checks.
  - Score each area and state every mistake and the needed upgrade plainly. Never inflate.
  - Re-check the video against every rule here and the user's notes. Breaking a known rule is an automatic finding.
- **Living playbook.** After each review, update the KEEP / DROP log and propose the updated skill.
- When unsure what works, research current best practice (vidIQ, platform docs, data studies) and cite it.

### Scorecard (weights)
| Area | Weight | 8+/10 means |
|---|---|---|
| Hook (first 2 s) | 20% | Frame 1 is bright, full-screen and meaningful (no fade-in). Shocking fact first, then the question, then "Let me explain". |
| Pacing / editing | 15% | A visual change every 1.5–2.5 s (Shorts) or 2–4 s (long). No hold over 3 s (Shorts) or 4.5 s (long, unless it is an animation). No dead air over 0.15 s in Shorts; long videos follow the Pace Model. |
| Captions | 15% | Word-by-word, synced, active word in amber, safe zones, spelling exactly as the script. |
| Visual quality | 15% | Bright, full-screen, readable on a phone, the right footage for each named place, credits and sources present. |
| Audio | 10% | Pro voice chain, -14 LUFS, calm music bed, NO hissy or noise SFX. |
| Script / story | 10% | Conversational, one clear payoff, tight wording. Shorts are 45–60 s. |
| Research / trust | 10% | Claims sourced on screen with proof cards; legends worded as beliefs or tradition. |
| CTA / growth | 5% | Mid-video nudge plus an end button. Platform-correct wording (IG = FOLLOW, YT = SUBSCRIBE). Ending of 8 s or less. Shorts point to the long video. |

### Automatic QA checks (every render)
- Duration and integrated loudness (ffmpeg ebur128, -14 LUFS).
- Frame-1 brightness above 60/255.
- Longest hold.
- Voice pacing: Shorts have no silences over 0.16 s; long videos run the Pace Model report (wpm per role, deliberate pauses per minute).
- Caption coverage.
- Safe zones.
  - 9:16: key text between y = 250 and 1550; nothing in the bottom ~370 px or the right ~140 px.
  - 16:9: captions at about y = 950; nothing important in the bottom-right corner, where YouTube puts its controls and end-screen elements.

## Fixed brand
- Colours: black #0A0A0A, cream #F4F1EA, amber #FFB224 accent, red for strikes and the subscribe button.
- **Series tag (top-left stamp), user rule Oct 27:** week theme + video number / total that week, e.g. `GOLD · 2/6` (TE `గోల్డ్ · 2/6`). Not "GOLD WEEK", not bare "GOLD". The long video uses `GOLD · FULL STORY`.
- Fonts: Archivo Black for headlines and captions, Space Mono for labels. Telugu uses Noto Sans Telugu Black (RAQM). Archivo has no ▶ or ↓ glyphs, so never use them.
- **Script voice: conversational, talking TO the viewer.**
  - Open with the shocking fact, then the question, then "Let me explain."
  - Never open with "Hey" or "Do you know".
  - Friend telling a friend, NOT a teacher quizzing a class (user, Oct 26): "Okay, look at this…", "here's what blew my mind", "this is my favourite part", "right?". Avoid quiz-style "So why does X? Let me explain" chains. Telugu the same: "ఒక్కసారి చూడండి", "నాకు షాకింగ్ అనిపించింది", "కదా?".
- **Ending, 8 s or less:** full-video pointer (Shorts only), then a follow/subscribe line, then "comment your why".
  - EN: "Subscribe for a new why every day, and comment your why below. We'll do the research and get you the answer."
  - The user records both FOLLOW and SUBSCRIBE takes; IG versions use FOLLOW, YT versions use SUBSCRIBE.
- **Subscribe/follow prompts, ALWAYS:**
  - A mid-video nudge: in Shorts, a red pill around 25 s; in the long video, a full-screen ask with a tap animation timed to the voice.
  - A big button on the end card with the same tap animation.
  - Separate IG and YT exports for Shorts.

## Weekly model (long-first, from Oct 26 2026)
- **Sunday:** record the long video plus Monday's Short.
- **Monday:** post the long video plus Short part 1.
- **Monday to Saturday:** one Short a day, each recorded the evening before and scheduled.
- **The long video is a COMPLETE deep-dive,** not limited to the Shorts' content. If it is too big, split it into parts.
- **Shorts are the most interesting or trending hooks,** and they drive viewers to the long video.
  - YT Shorts: set "Related video" to the long video.
  - IG: "full video on YouTube, link in bio".

### Posting times
The user is in Texas, so IST times are converted to local time.

| Post | IST | CDT (until Oct 31) | CST (from Nov 1) |
|---|---|---|---|
| Long video | 5:00 PM | 6:30 AM | 5:30 AM |
| IG Reel | 7:00 PM | 8:30 AM | 7:30 AM |
| YT Short | 8:00 PM | 9:30 AM | 8:30 AM |

- Metricool brand "whytelugu" (id 7312248) has Telugu IG and one YT channel. The English accounts are not connected yet.
- Metricool's best-time data is generic until there are 2–3 weeks of history; re-check after that.

## Style (required)
- Modern explainer at the Think School / What If standard. Never epic or "Rajamouli" style.
- EVERYTHING FULL-SCREEN. Low-res or off-ratio photos sit on a blurred full-frame fill behind a large sharp crop.
- Look:
  - Bright footage with dims scaled to about 50–60%, and a soft dark band only behind the captions.
  - Captions are the main text, so don't add headlines that paraphrase the voice.
  - Keep place cards (name plus a state pill), big pop-in numbers, and proof cards.
  - Punch-in of about 7% (5% in 16:9) halfway through long shots.
  - "AI ILLUSTRATION" labels, and CC/Pexels credits.
- Never use footage from a different place for a named place.

### Long video (16:9, 1920x1080) additions
- **Chapter progress bar** across the top, about 12 chapters, matching the YouTube chapter timestamps in the description.
- **Chapter cards** ("STORY 1 · RAMA VS RAVANA") over a dimmed image.
- **2D motion-graphic explainers in the brand style** (anim_long.py):
  - an India map with pulsing pins;
  - word merges (DASHA + HARA → DUSSEHRA);
  - "three stories → DAY 10" lanes;
  - ✕/✓ loophole cards;
  - a timeline;
  - a town-as-stage map with a walking crowd;
  - world-map arcs;
  - a cycle diagram;
  - day-count badges;
  - a villain → power table.
  - Use them for the explaining parts. They can't do character animation; those beats stay on AI images with camera moves.
- **Maps:** draw land as ONE mass with NO political borders, so the Kashmir border can never be an issue.
- **Mid-video ask** (after roughly 45% of the video): a "WAIT." card, then a "HOW OLD?" style tease, then a full-screen SUBSCRIBE button tapped on "I'm hoping you did". The music dips to about 25% during the ask.
- **Music:** two calm tracks. Track 1 plays up to the ask; track 2 starts as the story resumes.
- **End card:** at least 5 s with WHY?, a subscribe tap and "COMMENT YOUR WHY BELOW", leaving room for YouTube end-screen elements.
- **Proof cards:** at least one per chapter (UNESCO pages, traveller accounts, news), not just one in the whole video.
- **AI images:** ask for the largest size (at least 1920 px wide) so they aren't upscaled and soft.
- **Thumbnail (1280x720):** three AI panels for the three subjects with amber name pills, at most 4–5 words of text (e.g. "DUSSEHRA IS NOT / ONE STORY"), plus a Telugu version.

## Sound design system (user: "sound effects make a normal video extraordinary")
- **Purpose:** sound follows what MOVES ON SCREEN (graphics, cards, maps, stamps), not the words. Never illustrate spoken words literally (no tree sounds for "Jammi", no elephant for "Mysuru"); the user said that feels artificial.
- **Real recorded library only.** Generated SFX (code or AI) sounded "kiddy" (pings/bells/pops) or hissy. The user keeps the pack and attaches it each session; the catalog lives at sfxlib/catalog.json (role, hit point).
  - Have: impact_big (hit at 2.17 s), impact_trailer (0.93 s, use once per video), sub_knock, heartbeat, riser (ends at 2.53 s), woosh_deep, swoosh_slow, page_turn, paper_slide, tick, ticker_run.
  - Still needed: keyboard typing, key press, mouse click, camera shutter, polaroid, rubber stamp, marker scribble, highlighter, thumbtack/pin, map unfold, sub drop.
- **One sound, one job ("physical desk-object" world, Vox / Johnny Harris style):**
  - typing → text typing on letter by letter;
  - mouse click → button tap;
  - shutter → photo appears;
  - paper slide + sub_knock → card lands;
  - stamp → ✕/✓ verdicts;
  - marker → circles, arrows, lines drawing;
  - highlighter → word highlight;
  - pin/map unfold → maps;
  - tick/ticker_run → timeline years;
  - page_turn + impact_big → new chapter;
  - heartbeat/riser + music drop + impact → the big reveal.
- **Design new animations for these sounds:** typewriter text for quotes and dates, a red marker circling the key word, a highlighter sweep, stamped verdicts, polaroid photo drops, page-turn chapters.
- **Don't sound every movement.** Key actions and transitions only; vary the family (not one "thud" everywhere).
- **Ambience:** only faint real ambience under real event footage (fire under burnings, crowd/drums under processions), and never in the explaining parts.
- **Mix:** voice on top (-14 LUFS); SFX clearly audible but under the voice (duck about 45% while speaking); music lowest; silence before reveals; chapter = voice pause about 1.3 s + music dip + swell + boom, with the card landing on the boom.
- **Script carries SFX cues** next to the mood and pause marks, e.g. `[⌨️ TYPE "1520"]`, `[✍️ CIRCLE "three"]`, `[⏸⏸ + BOOM]`.

## Script format for long recordings (user request, from next video)
- Every line starts with **[MOOD · delivery]** (hook/amazed/curious/storytelling/serious/dramatic/playful/proud/urgent/reflective). **Bold** marks the stress word.
- ⏸ = stop 1–2 s, ⏸⏸ = 2–3 s (before reveals and chapters). These give clean cut points; the Pace Model sets the final rhythm.
- Recording tips:
  - record one chapter at a time;
  - on a stumble, pause and redo the whole line (keep recording);
  - smile on hook and ask lines;
  - talk to one friend;
  - questions go up at the end, names and numbers a touch slower;
  - same room and mic distance every session;
  - read each chapter once silently first.

## Workflow (phased; do not skip ahead)
1. **Research.** Verify every claim and record the outlet, date and URL. Word legends as "tradition says". Re-check numbers, and cut factual slips from the audio.
2. **Script.** Write English and natural spoken Telugu.
   - Use the conversational voice and the hook formula.
   - One idea per line, with re-hooks every 30–45 s in the long video.
   - Get an external review (e.g. ChatGPT) and fix the facts it flags.
3. **Voice edit (pro Reels style).**
   - **English:** transcribe with faster-whisper small.en at 16 kHz.
   - **Telugu:** transcribe per phrase with the CT2 te_med model. For retake-heavy passages, do a fine pass: energy segments with a 0.12 s merge, then whisper per segment, to find exact boundaries.
   - Run whisper jobs sequentially; the machine has only 2 CPUs.
   - Pick the best take of each line. When pieces overlap, clamp each end to the next start. Mark hand-tuned boundaries 'raw'.
   - **Denoise, join and tighten:**
     - Denoise first.
     - **Shorts:** join pieces with 70 ms gaps, then compress pauses over 0.16 s to 0.10 s with crossfades.
     - **Long videos:** NEVER use the Shorts squeeze; it made the first long cut 204 wpm and the user said it sounded like reading. Use the **Why? Pace Model** (pacing.py + make_voice_v2.py, build_long) instead.
   - **Why? Pace Model v2 (long-form; user-approved Oct 25 2026). v1 at 159 wpm with 0.5 s sentence gaps felt slow ("can't watch it"); v2 uses a fast baseline with beats only where they work:**
     - Every piece gets a role, and the role sets the pause after it and how much internal pause is kept.
     - Fast roles: HOOK (whole intro up to "Let me explain"), TEASE (quick recaps), LIST (rapid-fire names and items, from story structure, never auto-detected), CTA. They get about 0.10–0.16 s gaps and internal pauses capped 0.16 → 0.10.
     - ASK (the mid-video subscribe ask) is warm and quick: about 0.2 s gaps.
     - EXPLAIN: 0.18 s after '.', 0.10 s after ',', 0.45 s after '?', and internal pauses capped 0.20 → 0.12.
     - QUESTION gets a 0.45–0.50 s beat before the answer, including questions in the middle of a line, where the internal pause is kept at ≥ 0.35 s.
     - PUNCH or reveal ("Power wasn't their problem", "A new beginning") gets a 0.50 s breath before it.
     - Every chapter start gets a 1.30 s pause before it, filled with a music dip, swell and boom.
     - Classify short lines by spoken duration, not word count (Telugu words are longer).
     - **Targets:** EN overall about 172–176 wpm; EXPLAIN parts about 170; fast parts about 180+; about 2 deliberate beats per minute. Telugu: the same roles, and about 1.3× the Shorts-cut length.
     - **Evidence:**
       - Popular YouTube speech is about 171 wpm median; top TED talks about 175.
       - Explainer and documentary narration is advised at about 135–160 wpm.
       - Deliberate pauses run 0.6–1.5 s; speakers speed up for interest and slow down for weight.
       - Calibrated to the narrator's raw pauses: '.' 0.6 s, ',' 0.4 s, '?' 0.66 s.
     - Send 3 sample clips (hook → explaining, ask → next chapter, ending) for approval before the full render.
   - **Chain:** de-esser, then pedalboard EQ, two compressors and a limiter. Finish with loudnorm -14.
   - **Re-records:** denoise them with their own noise profile and match the tone (e.g. +2 dB high shelf at 3 kHz). Append them to the source with a 1 s gap and splice them in. Use 'raw' bounds so plosives such as the "P" in "Power" aren't trimmed.
   - **Verify:** re-transcribe the final track and check every splice in isolation. Whisper blends neighbouring words in context.
   - **Captions:**
     - English: align the exact SCRIPT text to the whisper word times (difflib, interpolating unmatched words). Never patch whisper's spelling word by word, because whisper output varies between runs.
     - Telugu: the script line per piece, with word times spread over that piece's voiced frames.
   - **Scene timing:** anchor scenes to spoken phrases, not fixed times, so re-records re-time everything automatically.
4. **Visuals list.**
   - Pexels links and Wikimedia CC photos.
   - ChatGPT image prompts (9:16 for Shorts, 16:9 for long videos).
   - A CALM Gemini music prompt: minimal bed, soft piano or pads, no busy hi-hats, no vocals.
   - Search and download stock yourself when the user hasn't supplied it. WebFetch on Pexels search pages works; direct download URLs:
     - videos: pexels.com/download/video/ID/
     - photos: images.pexels.com/photos/ID/pexels-photo-ID.jpeg?w=2400
   - Wikimedia: use upload.wikimedia.org thumb URLs at standard sizes (960/1280/1920). Special:FilePath and the API are rate-limited (429).
   - Pre-extract clip frames at 1080p and 30 fps. Vertical clips go on a blurred fill.
5. **Render.**
   - PIL frames piped to ffmpeg: libx264, CRF 19–20, 30 fps.
   - Lead 0.15 s. Tail 0.7 s (Shorts) or 3 s (long).
   - Render in 2 parallel parts. Long video speed is about 0.17 s per frame, so about 25 min for 5 min of video.
   - Music: pick the least busy track. EQ-carve it (-5 dB at 2.2k, -5 dB high shelf at 6k, lowpass 10k), gain about 0.22–0.24, sidechain duck about 62%.
   - SFX: follow the Sound design system above. Events come from the scene list and the animation args (pin, part, lane, slot, node and row times). Use real library files aligned on their hit points.
   - Render a stills sheet and fix overlaps before the full render. Then run the QA checks.
6. **Deliver.** Platform versions, covers or thumbnails, post copy (why-channel-post-copy, including chapters for long videos), then the honest review and scorecard.

## Copyright
- Monetization-safe only: Pexels, CC BY/BY-SA with attribution, own AI images, licensed music.
- Flag YouTube "Altered or synthetic content" only when AI images look photoreal.
- Avoid graphic blood in thumbnails.

## Environment gotchas
- Never `pkill -f` / `pgrep -f` with a pattern that also matches the shell's own command line; it kills the shell (exit 144). Kill by PID from `ps` filtered with `grep -v grep`.
- Don't run heavy whisper jobs alongside renders unless you have to. Both slow to a crawl on 2 CPUs.

## KEEP / DROP log (update after every review)
**KEEP (working):**
- Real sources and proof cards.
- Pro voice edit with tight pauses.
- Word-by-word captions aligned to the script.
- Bright full-screen footage.
- Place cards and big pop numbers.
- AI art for mythology.
- Calm, EQ-carved music, e.g. "the quiet meridian", "where the river bends", "before the world wakes".
- Subscribe/follow nudges, and separate IG/YT exports.
- Real effigy and event photos at climaxes.
- 2D brand animations for the explaining parts (long video).
- Phrase-anchored scene timing.
- Why? Pace Model for long videos: fast hooks, lists and asks; explaining pace with natural pauses; beats after questions and before reveals (user: "it's good").
- One explainer graphic per idea in Shorts too (user asked "add graphics for explanation"): element chain stopping at iron, balance scale, collapse, sugar-cube counter, spectrum, element tiles, Earth cutaway, timeline (Gold Short 1).
- NASA SVS animations (public domain, credit Goddard/CI Lab) for space events; for 16:9 clips with moving subjects, use a wide feathered band over a starfield instead of a tight 9:16 crop (the subjects leave a tight crop).
- Clips sent as original MP4s straight from Pexels/NASA (never through Descript: free-plan watermark).

**DROP (failed; never repeat):**
- Epic/cinematic style.
- Visuals in bands or boxes.
- Basic take-picking with natural pauses.
- Busy music (e.g. "under the marigold arch").
- Hissy noise whooshes and risers.
- Heavy dims.
- Fade-in or a black first frame.
- Long static or black end screens (Shorts).
- Headlines that paraphrase the voice.
- "SUBSCRIBE" on Instagram.
- Holds over 4 s.
- Wrong-place footage.
- "Hey / Do you know" openers.
- Endings over 8 s.
- Patching whisper spellings word by word.
- Political borders on maps.
- Generated or synthetic SFX: pings, bells, sparkles, pops ("kids' video"); AI-generated SFX packs (hiss).
- Literal ambience matched to spoken words (trees for "Jammi", elephant for "Mysuru").
- Even 0.5 s pauses after every sentence ("sounds slow, can't hold interest").
- Shorts-style pause squeezing on long videos (204 wpm, "sounds like reading").

**Score history:**
- Ravana Short (Oct 23): not scored.
- Saturday Short (Oct 24): v2 6.5, v3 about 7.5. The gaps were in the script: a question-first hook, and 75 s long.
- Sunday Short "Why burn Ravana" (Oct 25): v1 8.0, v2 8.4. Remaining: an 8 s static end grid, estimated Telugu caption timing, and a 6 s AI image hold.
- Gold Short 1 "Your gold came from dead stars" (Oct 26): EN 8.3, TE 8.0. Strong graphics and proof card. Holding it back: no on-screen hook text for the first 1.7 s, the iron-vs-gold scale is on screen only 1.5 s, Telugu caption timing is estimated, the meteor/panning clips are 1080p upscales, and the subscribe pop crowds the panning shot.
- Gold Short 2 "Why gold never rusts" (Oct 27): EN 8.2, TE 8.0. Strong: friend-to-friend script, 2026 study proof card, iron-vs-gold O2 graphics, hexagon lattice, jar/medal story graphics. Holding it back: 79-83 s long, the voice says "rusty is" (caption fixed), the 1940 scene is a magazine page rather than one photo, Telugu caption timing estimated. User-sent 'acid fizz / jar / medal' WAVs were synthetic and rejected; Mixkit real ones used.
- Gold long "Why Is Gold So Expensive?" (Oct 28): EN 8.4, TE 8.2. Strong: 8-chapter structure with progress bar, Johnny-Harris-style paper/clippings title sequence after "Let's go", periodic-table elimination, central-bank and price charts, NASA kilonova footage, Pace Model v2 with 6.6 s title gap. Holding it back: some chapter middles are graphic-on-dark for long stretches, Telugu captions estimated (no word timestamps), TE fusion/price anchors set by fractions. KEEP: TE take list keyed by EN piece prefixes so one cue file drives both languages.
- Long video "Dussehra Is NOT One Story. It's Three." (Oct 26): v1 8.3 on visuals, but the pacing was too fast (204 wpm). v3 final: Pace Model v2 (172 wpm), chapter pause plus boom, motion-graphics SFX, faint real fire/crowd/drums. The user felt the SFX were still one-note; the next video uses the real-SFX system.

## Update Oct 28 2026: new style, new workflow, voice via ElevenLabs
- **Workflow (replaces record-first):** topic → Claude script (EN+TE, visual beat under each line, sources + exact lines to screenshot, credit estimate) → user humanizes & approves → Claude generates both voices in ElevenLabs (cloned "Sandeep English" / "Sandeep Telugu", eleven_v4, ONE take each, generations_count=1) → visuals/music/SFX/screenshot list → user sends assets → render 4 versions (EN/TE × YT/IG) → one-block report (score, issues, credits used, credits left).
- **Credits:** ~0.46 credits/char (eleven_v4). Telugu ≈ 1,200/Short, English ≈ 450/Short. Budget 121k/month: ~30 Shorts + 4 long (~10 min). Reuse the saved CTA lines (voice_lib/te_gold3_take2_source.wav, 75.30–86.64 s: subscribe/follow/comment) instead of regenerating. ElevenLabs is for voice ONLY.
- **Target score: 8.5/10.**
- **Style v2 (approved):** dark glass cards with amber edge bar, amber→orange gradient on key numbers/words, glowing amber dot as the guide (travels to what matters; rides the highlighter tip), highlighter swipe (from "paper" style), NO red anywhere, no mascot face; plain logo "?"→"!" only at Why/payoff/ending. Helpers: pipeline/style_v2.
- **Evidence board (Johnny Harris verification):** real screenshots → torn paper clippings with tape, source tag chip, amber highlighter sweeping the exact quoted line in sync with the voice; taped real photos; amber threads connect pieces; ending zooms out to the full board. Never use recreated/AI "screenshots" — verify the URL in the image (Gemini-made pack had a 404 URL).
- **Telugu captions:** PIL + RAQM (cairo toy fonts can't shape Telugu). Timing: sentence boundaries from the TTS pause map, words spread by length.
- **Gotcha:** pill/scale(0) → cairo singular matrix → "out of memory" crash mid-render; guard s<=0.01.

**KEEP:** evidence clippings + highlighter sync (Gold 3), relativity ON/OFF switch payoff, drawn objects (metals, gold bar, spectrum, atom) when stock is missing, real Pexels clips for hook/key beats.
**DROP:** red accents; "?" mascot with eye; recreated screenshots; two-take TTS generations.

**Score history:**
- Ravana new-style test (Oct 27): v1 ~8.0 (red + mascot rejected), v2 approved style.
- Gold Short 3 "Why is gold yellow?" (Oct 28): EN/TE ~8.0. Holding back: soft BBC screenshot text, music not the gold-week bed, TE 69 s, TE captions sentence-level timing, no cover delivered.
- **Covers (Oct 28):** hero image from ChatGPT (Claude gives the prompt; user generates) + Claude's layer: large taped real photo, real clipping with highlight, amber thread + glow dot linking them (user: "organic, stylish"), headline in the dark lower third (cream + amber gradient word), WHY? logo top-left, amber-outlined series pill "GOLD · 3/6" under the headline (TE: "గోల్డ్ · 3/6").
- **Voice line library (Oct 28):** `voice_lib/` (see its README). Check every script line against `index.json` before generating; reuse exact sentence/phrase matches only (no single-word splicing); generate the rest per line, one take; save each new line + index entry. Write a week's Shorts lines word-for-word from the long-video script where possible to maximise reuse.
- Gold Short 4 "Why is India bringing its gold back home?" (Oct 28): EN/TE ~8.3. First fully generated-voice video (both clones, eleven_v4, one take, mood tags work in Telugu too). Real print-to-PDF captures → crops found by text (clipkit.py: pdftotext -bbox → crop + exact-phrase highlight). Credits 2,167 (EN 1,164 incl. one-time EN CTA; TE 1,003). Real rate ≈1 credit/char. Holding back: TE runs 62 s; the board ending is busy; wide map makes cities small; EN "RBI" may sound slurred (check).
- Asset rule: when a capture tool can't screenshot, print-to-PDF is fine — build clippings from the PDF at 300 dpi (sharper than phone screenshots). Verify every quoted line against the PDF text and the article date; label syndicated copies honestly (e.g. "REUTERS FACTBOX (VIA ENERGIESNET)").
- **Voice direction (user, Oct 28):** expressive but LIGHT. Use mild tags only ([calm], [warm], [curious], [slightly serious], [conversational]); no strong ones ([excited], [amazed], [fast-paced], [intrigued]); at most one tag per line, many lines untagged. Consider higher stability for the clone.
- **Length (user, Oct 28):** Shorts may run up to 3 min if interesting — don't trim content just to hit 60 s; don't count length as an issue in reviews.
- Gold Short 5 "Why do Indians trust gold more than banks?" (Oct 29): EN/TE ~8.4. Template: kinetic data + evidence (flag race of the top-10 central banks with a running total → combined bar vs Indian homes; ₹ counter + price line; gold vs FD bars; $1 = ₹45 → ₹95 flip; rupee-vs-gold log chart; stopwatch loan; Mint clippings; taped family photos → "saving it for the future"). Credits 2,388 (EN 1,182, TE 1,206), ending lines reused from voice_lib. Holding back: ABC table clipping text is small, USD/INR yearly path is approximate (endpoints sourced), the ICMAI clipping lists Turkey as 10th while the voice says Netherlands (footnote "10th place varies by date"), TE captions sentence-level timing.
- **₹ glyph (Oct 29):** Archivo Black / Space Mono have no ₹; `brand/fonts/` now hold copies with ₹ merged in (Poppins Bold / DejaVu Sans Mono), see `videos/2026-10-30_short_gold_dhanteras/pipeline/addrupee.py`. Install to ~/.fonts and run fc-cache.
- **Caption fix (Oct 29):** whisper drops/duplicates words at chunk edges on generated voice. Transcribe in ~25 s windows, then snap to the exact script text with difflib (fixw.py) and interpolate missing words. TE captions: map spelled-out numbers to digits (CAPMAP in tealign5.py).
- **Number check (Oct 29):** every on-screen formula must match the script math (caught "1.07^19" for a 20-year FD before delivery).
**KEEP:** kinetic-data template for money topics; source footnote on screen when a ranking changes by date; reuse ending lines from voice_lib.
- **Cover rule (user, Oct 29):** no recognizable person's face on covers; a face grabs the eye before the headline. Use a scene/object photo that matches the topic (e.g. dense Indian homes rooftops for Gold 5). Unsplash MCP works for these (images.unsplash.com downloads from the shell).
- **CTA upgrade (user, Oct 29, from Gold 6 on; built: pipeline/style_v2/cta_card.py, sfx ui_click/ui_bell/ui_pop):** replace the plain SUBSCRIBE/FOLLOW pill with a realistic animated card. YT: profile picture + channel name/handle + Subscribe button; cursor glides in, clicks → "Subscribed", then clicks the bell → bell rings, "All". IG: profile picture + handle + Follow button; click → "Following" + check mark. Real SFX on each click/bell/tick. Synced to the CTA voice line. Needs: profile pictures for all 4 accounts, exact names/handles, real click/bell/tick sounds.
- **Accounts (for the CTA card):** YT EN "Why?" @WhyEveryQuestionHasAStory · YT TE "why?telugu" @WhyTeluguStories · IG EN "Why?" why_everyquestionhasastory · IG TE "Why? Telugu" whytelugu. Profile pictures: brand/avatars/*_2160.png.
- **CTA placement (user, Oct 29, all videos):** Shorts: the animated card at least twice — once mid-video, once at the end — plus a third time if the length allows. Long videos: once every 2–3 minutes. Mid-video cards keep the click/bell/pop SFX at low volume (~50% of the end card) with no extra narration, are smaller and placed where they don't cover the key visual; drop them right after a payoff beat, never in the first 15 s. The end card stays synced to the spoken CTA line.
- **Weekly schedule (user, Oct 29):** full (long) video every **Sunday**; one Short every day **Monday–Saturday**. Each video is made at least one day before it posts (Sunday's on Saturday, Monday's on Sunday…), earlier when there's time.
- **New ending (from Gold 6):** series slide (week name, full-video thumbnail "▶ FULL VIDEO · on the channel", all Shorts 1/6–6/6 with covers + short titles, current one "YOU'RE HERE", next ones blurred "TOMORROW") + schedule CTA line, reused from voice_lib:
  EN: "If you like learning things like this, we post a full video every Sunday and a new Short the other six days. So there's always something new. Subscribe (IG: Follow), and we'll make it worth it."
  TE: "ఇలాంటి కొత్త విషయాలు నేర్చుకోవడం నచ్చితే, ప్రతి ఆదివారం ఒక full video, మిగతా ఆరు రోజులు రోజుకో Short పెడతాం. ఎప్పుడూ ఏదో ఒక కొత్తది ఉంటుంది. Subscribe చేయండి (IG: Follow అవ్వండి), మీకు నచ్చేలా చేస్తాం."
  The animated subscribe/follow card clicks exactly on the spoken "Subscribe/Follow". "GOT A WHY? COMMENT IT" stays as on-screen text only (no voice).
- **Teasers & open questions (user, Oct 29):** Shorts 1/6–5/6 end with a one-line hook for the next Short ("Tomorrow: why …?"), also shown on the series slide's "TOMORROW" card, so the whole week's topics are planned up front. The 6th Short and the Sunday full video instead end with 2–3 open questions on the same topic: "…that's a why for another day. If you want it, comment below." (TE: "అది ఇంకో రోజు చెప్పుకునే why. కావాలంటే, comment చేయండి.") No likes targets (Instagram demotes engagement bait).
- Gold Short 6 "Why is gold falling right now?" (Oct 30): EN/TE ~8.5. First video with: variable pacing (info 1.12×, questions/wrap/schedule 1.10×, the Subscribe/Follow line at regular pace), animated subscribe/follow card mid (quieter SFX) + end (click lands on the spoken word), open-question ending ("a why for another day"), animated series slide (week + full video + 6 covers, YOU'RE HERE, NEXT · NEW SERIES THIS SUNDAY). Credits 4,020 (EN 1,942, TE 2,078; estimate was 3,100 — count TTS chars, numbers spelled out in Telugu add a lot). Holding back: captions hidden during the series slide; the 1st chart is two sourced points only; CERN capture is the home.cern substitute (original ALICE link dead).
- **Pacing (user, Oct 30):** information lines faster, branding/request lines also a bit faster, the Subscribe/Follow line itself at regular pace. Implemented per segment in voice6.py (squeeze + atempo per segment).
- **Whisper on generated voice:** use overlapping ~22 s windows (keep words that end before window−0.6 s) and snap to the script with difflib; a single pass drops 10 s chunks.
**KEEP:** series slide, open questions with real-image cards, per-segment pacing, CTA card in-frame (no overlay pass needed).
