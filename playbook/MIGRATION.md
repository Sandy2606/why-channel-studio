# MIGRATION: old playbook → reorganised system (Nov 10 2026)

Maps every line of `playbook/why-channel-video-SKILL.md` as it stood at tag `pre-pro-system` (commit fb25e59, 396 lines) to its new home. The full original is in git: `git show pre-pro-system:playbook/why-channel-video-SKILL.md`. This file is a record, not instructions.

## Rollback point (verified)
- The pre-reorganisation state is commit **fb25e5933dc52d27c7b7be6c05c1d19258a52616** (`fb25e59`, "Playbook: GS 4/6 KEEP + score 8.7, archival styling rule"). It is the tip of `main` on GitHub, verified with `git ls-remote origin refs/heads/main` on 2026-11-10.
- A local tag `pre-pro-system` points at the same commit. This session's GitHub connection refused to push tags (HTTP 403), so the tag isn't on GitHub yet. Before any merge, either add the tag on GitHub (Releases → "Draft a new release" → tag `pre-pro-system`, target commit fb25e59) or use the commit hash above. After a merge, restore by reverting the merge commit (`git revert -m 1 <merge-commit>`). The reorganisation only touched Markdown, so a revert never affects renders or assets.

Status: **CURRENT** (the content lives on in the named rule), **METHOD** (a technical note in `playbook/methods/`), **DATA** (in `platform_rules.md`, marked for re-check), **SUPERSEDED** (replaced; old text in `history.md`), **DROP** (failed approach; kept in `history.md`, enforced by the named rule), **EVIDENCE** (score history and lessons in `history.md`), **STRUCT** (heading, blank line or frontmatter).

| Line | Status | New home | Note | Original (start) |
|---|---|---|---|---|
| 1 | STRUCT | master | frontmatter, title | --- |
| 2 | STRUCT | master | ″ | name: why-channel-video |
| 3 | STRUCT | master | ″ | description: Produce a Why? channel explainer (Short or long, English … |
| 4 | STRUCT | master | ″ | --- |
| 5 | STRUCT | master | ″ |  |
| 6 | STRUCT | master | ″ | # Why? channel video production |
| 7 | STRUCT | master | ″ |  |
| 8 | SUPERSEDED | BR-07 | handle "@whyeveryquestion" wrong; description moved to master | Channel: "Why?" (YouTube @WhyEveryQuestionHasaStory, Instagram @whyeve… |
| 9 | STRUCT |  |  |  |
| 10 | STRUCT |  | ″ | ## 0. Quality system (READ FIRST, applies to every video) |
| 11 | SUPERSEDED | QC-03 | 8/10 target raised to 8.5 (user Oct 28), now a target beside the QC-02 gate (user Nov 10) | - **Target: every video scores at least 8/10** on the scorecard. If th… |
| 12 | CURRENT | WF-06 |  | - **After EVERY delivery, give a full, honest review with scores.** |
| 13 | CURRENT | QC-01 | frame sampling, QA | - Sample frames (every 1.5 s, plus the first 3 s at 3 fps) and look at… |
| 14 | CURRENT | QC-01 | ″ | - Run the QA checks. |
| 15 | CURRENT | WF-06 |  | - Score each area and state every mistake and the needed upgrade plain… |
| 16 | CURRENT | QC-01 |  | - Re-check the video against every rule here and the user's notes. Bre… |
| 17 | SUPERSEDED | WF-05 | after-delivery update now goes to history; rules change only by approval (Phase 2A, Nov 10) | - **Living playbook.** After each review, update the KEEP / DROP log a… |
| 18 | CURRENT | RS-08 |  | - When unsure what works, research current best practice (vidIQ, platf… |
| 19 | STRUCT |  |  |  |
| 20 | STRUCT |  | ″ | ### Scorecard (weights) |
| 21 | CURRENT | QC-03 | scorecard table header | \| Area \| Weight \| 8+/10 means \| |
| 22 | CURRENT | QC-03 | ″ | \|---\|---\|---\| |
| 23 | SUPERSEDED | ST-02 | hook formula retired as mandatory (user Nov 10, decision 6) | \| Hook (first 2 s) \| 20% \| Frame 1 is bright, full-screen and meani… |
| 24 | SUPERSEDED | DIR-04 | fixed cut cadence and hold caps replaced (user Nov 10: don't force cuts; intentional stillness allowed); dead-air part kept in ED-01 | \| Pacing / editing \| 15% \| A visual change every 1.5–2.5 s (Shorts)… |
| 25 | CURRENT | LAY-02 |  | \| Captions \| 15% \| Word-by-word, synced, active word in amber, safe… |
| 26 | CURRENT | QC-03 |  | \| Visual quality \| 15% \| Bright, full-screen, readable on a phone, … |
| 27 | CURRENT | QC-03 | ″ | \| Audio \| 10% \| Pro voice chain, -14 LUFS, calm music bed, NO hissy… |
| 28 | SUPERSEDED | FMT-01 | "Shorts are 45–60 s" replaced (user Oct 28, Oct 31, Nov 10) | \| Script / story \| 10% \| Conversational, one clear payoff, tight wo… |
| 29 | CURRENT | QC-03 |  | \| Research / trust \| 10% \| Claims sourced on screen with proof card… |
| 30 | SUPERSEDED | FMT-04 | mid-video nudge in Shorts removed (user Nov 1); endings now FMT-06/07 | \| CTA / growth \| 5% \| Mid-video nudge plus an end button. Platform-… |
| 31 | STRUCT |  |  |  |
| 32 | STRUCT |  | ″ | ### Automatic QA checks (every render) |
| 33 | CURRENT | QC-06 |  | - Duration and integrated loudness (ffmpeg ebur128, -14 LUFS). |
| 34 | CURRENT | QC-06 | ″ | - Frame-1 brightness above 60/255. |
| 35 | CURRENT | QC-06 | ″ | - Longest hold. |
| 36 | CURRENT | QC-06 | ″ | - Voice pacing: Shorts have no silences over 0.16 s; long videos run t… |
| 37 | CURRENT | QC-06 | ″ | - Caption coverage. |
| 38 | CURRENT | LAY-03 |  | - Safe zones. |
| 39 | CURRENT | LAY-03 | ″ | - 9:16: key text between y = 250 and 1550; nothing in the bottom ~370 … |
| 40 | CURRENT | LAY-03 | ″ | - 16:9: captions at about y = 950; nothing important in the bottom-rig… |
| 41 | STRUCT |  |  |  |
| 42 | STRUCT |  | ″ | ## Fixed brand |
| 43 | SUPERSEDED | BR-01 | red accents dropped (user Oct 27, Nov 10) | - Colours: black #0A0A0A, cream #F4F1EA, amber #FFB224 accent, red for… |
| 44 | CURRENT | BR-03 |  | - **Series tag (top-left stamp), user rule Oct 27:** week theme + vide… |
| 45 | CURRENT | BR-02 |  | - Fonts: Archivo Black for headlines and captions, Space Mono for labe… |
| 46 | CURRENT | ST-03 |  | - **Script voice: conversational, talking TO the viewer.** |
| 47 | SUPERSEDED | ST-02 | hook formula retired as mandatory (user Nov 10, decision 6) | - Open with the shocking fact, then the question, then "Let me explain… |
| 48 | CURRENT | ST-03 |  | - Never open with "Hey" or "Do you know". |
| 49 | CURRENT | ST-03 | ″ | - Friend telling a friend, NOT a teacher quizzing a class (user, Oct 2… |
| 50 | SUPERSEDED | FMT-06 | spoken subscribe ending replaced by the v3 ending (user Nov 1); voice is generated, not recorded (user Oct 28) | - **Ending, 8 s or less:** full-video pointer (Shorts only), then a fo… |
| 51 | SUPERSEDED | FMT-06 | ″ | - EN: "Subscribe for a new why every day, and comment your why below. … |
| 52 | SUPERSEDED | FMT-06 | ″ | - The user records both FOLLOW and SUBSCRIBE takes; IG versions use FO… |
| 53 | SUPERSEDED | FMT-04 | red pill / mid-video nudges replaced (user Nov 1, Nov 10; long films FMT-05) | - **Subscribe/follow prompts, ALWAYS:** |
| 54 | SUPERSEDED | FMT-04 | ″ | - A mid-video nudge: in Shorts, a red pill around 25 s; in the long vi… |
| 55 | CURRENT | BR-09 |  | - A big button on the end card with the same tap animation. |
| 56 | CURRENT | FMT-09 |  | - Separate IG and YT exports for Shorts. |
| 57 | STRUCT |  |  |  |
| 58 | STRUCT |  | ″ | ## Weekly model (long-first, from Oct 26 2026) |
| 59 | SUPERSEDED | FMT-02 | Monday long-video model replaced (user Oct 29) | - **Sunday:** record the long video plus Monday's Short. |
| 60 | SUPERSEDED | FMT-02 | ″ | - **Monday:** post the long video plus Short part 1. |
| 61 | SUPERSEDED | FMT-02 | ″ | - **Monday to Saturday:** one Short a day, each recorded the evening b… |
| 62 | CURRENT | FMT-03 |  | - **The long video is a COMPLETE deep-dive,** not limited to the Short… |
| 63 | CURRENT | FMT-03 | ″ | - **Shorts are the most interesting or trending hooks,** and they driv… |
| 64 | CURRENT | PUB-04 |  | - YT Shorts: set "Related video" to the long video. |
| 65 | CURRENT | PUB-04 | ″ | - IG: "full video on YouTube, link in bio". |
| 66 | STRUCT |  |  |  |
| 67 | DATA | PLT-07 | posting times and Metricool status, marked NEEDS RE-CHECK | ### Posting times |
| 68 | DATA | PLT-07 | ″ | The user is in Texas, so IST times are converted to local time. |
| 69 | DATA | PLT-07 | ″ |  |
| 70 | DATA | PLT-07 | ″ | \| Post \| IST \| CDT (until Oct 31) \| CST (from Nov 1) \| |
| 71 | DATA | PLT-07 | ″ | \|---\|---\|---\|---\| |
| 72 | DATA | PLT-07 | ″ | \| Long video \| 5:00 PM \| 6:30 AM \| 5:30 AM \| |
| 73 | DATA | PLT-07 | ″ | \| IG Reel \| 7:00 PM \| 8:30 AM \| 7:30 AM \| |
| 74 | DATA | PLT-07 | ″ | \| YT Short \| 8:00 PM \| 9:30 AM \| 8:30 AM \| |
| 75 | DATA | PLT-07 | ″ |  |
| 76 | DATA | PLT-07 | ″ | - Metricool brand "whytelugu" (id 7312248) has Telugu IG and one YT ch… |
| 77 | DATA | PLT-07 | ″ | - Metricool's best-time data is generic until there are 2–3 weeks of h… |
| 78 | STRUCT |  |  |  |
| 79 | STRUCT |  | ″ | ## Style (required) |
| 80 | CURRENT | BR-05 |  | - Modern explainer at the Think School / What If standard. Never epic … |
| 81 | CURRENT | LAY-01 | blurred fill kept as an allowed background in LAY-05 | - EVERYTHING FULL-SCREEN. Low-res or off-ratio photos sit on a blurred… |
| 82 | STRUCT |  |  | - Look: |
| 83 | SUPERSEDED | LAY-01 | dark band behind captions replaced (user Nov 10: whole screen, no masked bottom) | - Bright footage with dims scaled to about 50–60%, and a soft dark ban… |
| 84 | CURRENT | LAY-04 |  | - Captions are the main text, so don't add headlines that paraphrase t… |
| 85 | CURRENT | DIR-09 |  | - Keep place cards (name plus a state pill), big pop-in numbers, and p… |
| 86 | SUPERSEDED | MO-01 | fixed punch-in replaced (user Nov 10: native resolution; rhythm follows information) | - Punch-in of about 7% (5% in 16:9) halfway through long shots. |
| 87 | CURRENT | ART-02 |  | - "AI ILLUSTRATION" labels, and CC/Pexels credits. |
| 88 | CURRENT | ART-01 |  | - Never use footage from a different place for a named place. |
| 89 | STRUCT |  |  |  |
| 90 | STRUCT |  | ″ | ### Long video (16:9, 1920x1080) additions |
| 91 | CURRENT | DIR-11 | now series-specific (DIR-11 v2, user Nov 10); fixed elements are options in series plans | - **Chapter progress bar** across the top, about 12 chapters, matching… |
| 92 | CURRENT | DIR-11 | now series-specific (DIR-11 v2, user Nov 10); fixed elements are options in series plans | - **Chapter cards** ("STORY 1 · RAMA VS RAVANA") over a dimmed image. |
| 93 | METHOD | methods/motion.md |  | - **2D motion-graphic explainers in the brand style** (anim_long.py): |
| 94 | METHOD | methods/motion.md | ″ | - an India map with pulsing pins; |
| 95 | METHOD | methods/motion.md | ″ | - word merges (DASHA + HARA → DUSSEHRA); |
| 96 | METHOD | methods/motion.md | ″ | - "three stories → DAY 10" lanes; |
| 97 | METHOD | methods/motion.md | ″ | - ✕/✓ loophole cards; |
| 98 | METHOD | methods/motion.md | ″ | - a timeline; |
| 99 | METHOD | methods/motion.md | ″ | - a town-as-stage map with a walking crowd; |
| 100 | METHOD | methods/motion.md | ″ | - world-map arcs; |
| 101 | METHOD | methods/motion.md | ″ | - a cycle diagram; |
| 102 | METHOD | methods/motion.md | ″ | - day-count badges; |
| 103 | METHOD | methods/motion.md | ″ | - a villain → power table. |
| 104 | METHOD | methods/motion.md | ″ | - Use them for the explaining parts. They can't do character animation… |
| 105 | CURRENT | MO-04 |  | - **Animation style library (Nov 8 2026):** `pipeline/styles/` has Iso… |
| 106 | CURRENT | MO-04 | ″ | - **Remotion effect clips (Nov 8 2026):** `pipeline/remotion_effects/`… |
| 107 | SUPERSEDED | ART-05 | one land mass with no borders replaced (user Nov 10, decision 4) | - **Maps:** draw land as ONE mass with NO political borders, so the Ka… |
| 108 | SUPERSEDED | FMT-05 | fixed mid-video ask replaced (user Nov 10: story breaks) | - **Mid-video ask** (after roughly 45% of the video): a "WAIT." card, … |
| 109 | SUPERSEDED | MU-03 | two-track bed was one video's choice; cue sheet per video (Phase 2A) | - **Music:** two calm tracks. Track 1 plays up to the ask; track 2 sta… |
| 110 | CURRENT | DIR-11 | now series-specific (DIR-11 v2, user Nov 10); fixed elements are options in series plans | - **End card:** at least 5 s with WHY?, a subscribe tap and "COMMENT Y… |
| 111 | CURRENT | DIR-11 | now series-specific (DIR-11 v2, user Nov 10); fixed elements are options in series plans | - **Proof cards:** at least one per chapter (UNESCO pages, traveller a… |
| 112 | CURRENT | ART-06 |  | - **AI images:** ask for the largest size (at least 1920 px wide) so t… |
| 113 | SUPERSEDED | BR-08 | three-panel thumbnail replaced by cover rules + series layouts (user Oct 28–29) | - **Thumbnail (1280x720):** three AI panels for the three subjects wit… |
| 114 | STRUCT |  |  |  |
| 115 | STRUCT |  | ″ | ## Sound design system (user: "sound effects make a normal video extra… |
| 116 | CURRENT | SD-02 |  | - **Purpose:** sound follows what MOVES ON SCREEN (graphics, cards, ma… |
| 117 | SUPERSEDED | SD-04 | pack attached per session / sfxlib path / old lists replaced by sfx/ + catalog (CLAUDE.md) | - **Real recorded library only.** Generated SFX (code or AI) sounded "… |
| 118 | SUPERSEDED | SD-04 | ″ | - Have: impact_big (hit at 2.17 s), impact_trailer (0.93 s, use once p… |
| 119 | SUPERSEDED | SD-04 | ″ | - Still needed: keyboard typing, key press, mouse click, camera shutte… |
| 120 | METHOD | methods/audio.md |  | - **One sound, one job ("physical desk-object" world, Vox / Johnny Har… |
| 121 | METHOD | methods/audio.md | ″ | - typing → text typing on letter by letter; |
| 122 | METHOD | methods/audio.md | ″ | - mouse click → button tap; |
| 123 | METHOD | methods/audio.md | ″ | - shutter → photo appears; |
| 124 | METHOD | methods/audio.md | ″ | - paper slide + sub_knock → card lands; |
| 125 | METHOD | methods/audio.md | ″ | - stamp → ✕/✓ verdicts; |
| 126 | METHOD | methods/audio.md | ″ | - marker → circles, arrows, lines drawing; |
| 127 | METHOD | methods/audio.md | ″ | - highlighter → word highlight; |
| 128 | METHOD | methods/audio.md | ″ | - pin/map unfold → maps; |
| 129 | METHOD | methods/audio.md | ″ | - tick/ticker_run → timeline years; |
| 130 | METHOD | methods/audio.md | ″ | - page_turn + impact_big → new chapter; |
| 131 | METHOD | methods/audio.md | ″ | - heartbeat/riser + music drop + impact → the big reveal. |
| 132 | SUPERSEDED | BR-01 | "red marker" conflicts with no-red rule (user Nov 10); rest kept in methods/audio.md | - **Design new animations for these sounds:** typewriter text for quot… |
| 133 | CURRENT | SD-03 |  | - **Don't sound every movement.** Key actions and transitions only; va… |
| 134 | SUPERSEDED | SD-05 | v2 (user Nov 10): ambience allowed under explanations and reconstructions where it supports the scene | - **Ambience:** only faint real ambience under real event footage (fir… |
| 135 | METHOD | methods/audio.md |  | - **Mix:** voice on top (-14 LUFS); SFX clearly audible but under the … |
| 136 | METHOD | methods/audio.md | ″ | - **Script carries SFX cues** next to the mood and pause marks, e.g. `… |
| 137 | STRUCT |  |  |  |
| 138 | STRUCT |  | ″ | ## Script format for long recordings (user request, from next video) |
| 139 | CURRENT | ST-07 |  | - Every line starts with **[MOOD · delivery]** (hook/amazed/curious/st… |
| 140 | CURRENT | ST-07 | ″ | - ⏸ = stop 1–2 s, ⏸⏸ = 2–3 s (before reveals and chapters). These give… |
| 141 | SUPERSEDED | CR-02 | recording tips obsolete: voice is generated in ElevenLabs (user Oct 27–28) | - Recording tips: |
| 142 | SUPERSEDED | CR-02 | ″ | - record one chapter at a time; |
| 143 | SUPERSEDED | CR-02 | ″ | - on a stumble, pause and redo the whole line (keep recording); |
| 144 | SUPERSEDED | CR-02 | ″ | - smile on hook and ask lines; |
| 145 | SUPERSEDED | CR-02 | ″ | - talk to one friend; |
| 146 | SUPERSEDED | CR-02 | ″ | - questions go up at the end, names and numbers a touch slower; |
| 147 | SUPERSEDED | CR-02 | ″ | - same room and mic distance every session; |
| 148 | SUPERSEDED | CR-02 | ″ | - read each chapter once silently first. |
| 149 | STRUCT |  |  |  |
| 150 | STRUCT |  | ″ | ## Current order of work (user-confirmed Nov 8 2026; overrides older w… |
| 151 | CURRENT | WF-01 |  | 1. Agree the topic. |
| 152 | CURRENT | WF-01 | ″ | 2. Research and verify every fact against current sources. |
| 153 | CURRENT | WF-01 | ″ | 3. Write the full English and Telugu scripts with sources, a visual be… |
| 154 | CURRENT | WF-01 | ″ | 4. **Script versions:** the user asks for changes to humanize it and w… |
| 155 | CURRENT | WF-01 | ″ | 5. Generate both voices in ElevenLabs, one take each, reusing saved li… |
| 156 | CURRENT | WF-01 | ″ | 6. Edit the voice: silences, pacing, mix. |
| 157 | CURRENT | WF-01 | ″ | 7. Send one message with the scene sheet (what is on screen for each l… |
| 158 | CURRENT | WF-01 | ″ | 8. The user gives changes until the scene sheet and its animation styl… |
| 159 | CURRENT | WF-01 | ″ | 9. The user sends the assets. Never render before they arrive. |
| 160 | CURRENT | WF-01 | ″ | 10. Send stills only if the style is changing; otherwise go straight t… |
| 161 | CURRENT | WF-01 | ″ | 11. Render the final videos: English and Telugu, with separate YouTube… |
| 162 | CURRENT | WF-01 | ″ | 12. Run the QA checks. |
| 163 | CURRENT | WF-01 | ″ | 13. Deliver the videos, thumbnail or cover and post copy. |
| 164 | SUPERSEDED | QC-03 | "8.5 minimum" as a stand-alone pass mark replaced (user Nov 10) | 14. Give one short honest report: score (8.5 minimum), mistakes, credi… |
| 165 | CURRENT | WF-05 |  | 15. Update the playbook, commit and push. |
| 166 | STRUCT |  |  |  |
| 167 | SUPERSEDED | WF-01 | phased workflow replaced by the Nov 8 order (user Nov 8) | ## Workflow (phased; do not skip ahead) |
| 168 | CURRENT | RS-02 |  | 1. **Research.** Verify every claim and record the outlet, date and UR… |
| 169 | SUPERSEDED | ST-01 | "use the hook formula" replaced (user Nov 10) | 2. **Script.** Write English and natural spoken Telugu. |
| 170 | SUPERSEDED | ST-01 | ″ | - Use the conversational voice and the hook formula. |
| 171 | CURRENT | ST-10 | fixed 30–45 s re-hook SUPERSEDED (ST-10 v2, user Nov 10) | - One idea per line, with re-hooks every 30–45 s in the long video. |
| 172 | CURRENT | RS-08 | external review: the user reviews with ChatGPT; facts it flags are re-checked | - Get an external review (e.g. ChatGPT) and fix the facts it flags. |
| 173 | METHOD | methods/editing.md | Pace Model v2 is ED-01 | 3. **Voice edit (pro Reels style).** |
| 174 | METHOD | methods/editing.md | ″ | - **English:** transcribe with faster-whisper small.en at 16 kHz. |
| 175 | METHOD | methods/editing.md | ″ | - **Telugu:** transcribe per phrase with the CT2 te_med model. For ret… |
| 176 | METHOD | methods/editing.md | ″ | - Run whisper jobs sequentially; the machine has only 2 CPUs. |
| 177 | METHOD | methods/editing.md | ″ | - Pick the best take of each line. When pieces overlap, clamp each end… |
| 178 | METHOD | methods/editing.md | ″ | - **Denoise, join and tighten:** |
| 179 | METHOD | methods/editing.md | ″ | - Denoise first. |
| 180 | METHOD | methods/editing.md | ″ | - **Shorts:** join pieces with 70 ms gaps, then compress pauses over 0… |
| 181 | METHOD | methods/editing.md | ″ | - **Long videos:** NEVER use the Shorts squeeze; it made the first lon… |
| 182 | METHOD | methods/editing.md | ″ | - **Why? Pace Model v2 (long-form; user-approved Oct 25 2026). v1 at 1… |
| 183 | METHOD | methods/editing.md | ″ | - Every piece gets a role, and the role sets the pause after it and ho… |
| 184 | METHOD | methods/editing.md | ″ | - Fast roles: HOOK (whole intro up to "Let me explain"), TEASE (quick … |
| 185 | METHOD | methods/editing.md | ″ | - ASK (the mid-video subscribe ask) is warm and quick: about 0.2 s gap… |
| 186 | METHOD | methods/editing.md | ″ | - EXPLAIN: 0.18 s after '.', 0.10 s after ',', 0.45 s after '?', and i… |
| 187 | METHOD | methods/editing.md | ″ | - QUESTION gets a 0.45–0.50 s beat before the answer, including questi… |
| 188 | METHOD | methods/editing.md | ″ | - PUNCH or reveal ("Power wasn't their problem", "A new beginning") ge… |
| 189 | METHOD | methods/editing.md | ″ | - Every chapter start gets a 1.30 s pause before it, filled with a mus… |
| 190 | METHOD | methods/editing.md | ″ | - Classify short lines by spoken duration, not word count (Telugu word… |
| 191 | METHOD | methods/editing.md | ″ | - **Targets:** EN overall about 172–176 wpm; EXPLAIN parts about 170; … |
| 192 | METHOD | methods/editing.md | ″ | - **Evidence:** |
| 193 | METHOD | methods/editing.md | ″ | - Popular YouTube speech is about 171 wpm median; top TED talks about … |
| 194 | METHOD | methods/editing.md | ″ | - Explainer and documentary narration is advised at about 135–160 wpm. |
| 195 | METHOD | methods/editing.md | ″ | - Deliberate pauses run 0.6–1.5 s; speakers speed up for interest and … |
| 196 | METHOD | methods/editing.md | ″ | - Calibrated to the narrator's raw pauses: '.' 0.6 s, ',' 0.4 s, '?' 0… |
| 197 | SUPERSEDED | WF-02 | sample clips replaced by motion previews (user Nov 10) | - Send 3 sample clips (hook → explaining, ask → next chapter, ending) … |
| 198 | METHOD | methods/editing.md |  | - **Chain:** de-esser, then pedalboard EQ, two compressors and a limit… |
| 199 | METHOD | methods/editing.md | ″ | - **Re-records:** denoise them with their own noise profile and match … |
| 200 | METHOD | methods/editing.md | ″ | - **Verify:** re-transcribe the final track and check every splice in … |
| 201 | METHOD | methods/editing.md | ″ | - **Captions:** |
| 202 | METHOD | methods/editing.md | ″ | - English: align the exact SCRIPT text to the whisper word times (diff… |
| 203 | METHOD | methods/editing.md | ″ | - Telugu: the script line per piece, with word times spread over that … |
| 204 | METHOD | methods/editing.md | ″ | - **Scene timing:** anchor scenes to spoken phrases, not fixed times, … |
| 205 | METHOD | methods/assets.md |  | 4. **Visuals list.** |
| 206 | METHOD | methods/assets.md | ″ | - Pexels links and Wikimedia CC photos. |
| 207 | METHOD | methods/assets.md | ″ | - ChatGPT image prompts (9:16 for Shorts, 16:9 for long videos). |
| 208 | METHOD | methods/assets.md | ″ | - A CALM Gemini music prompt: minimal bed, soft piano or pads, no busy… |
| 209 | METHOD | methods/assets.md | ″ | - Search and download stock yourself when the user hasn't supplied it.… |
| 210 | METHOD | methods/assets.md | ″ | - videos: pexels.com/download/video/ID/ |
| 211 | METHOD | methods/assets.md | ″ | - photos: images.pexels.com/photos/ID/pexels-photo-ID.jpeg?w=2400 |
| 212 | METHOD | methods/assets.md | ″ | - Wikimedia: use upload.wikimedia.org thumb URLs at standard sizes (96… |
| 213 | METHOD | methods/assets.md | ″ | - Pre-extract clip frames at 1080p and 30 fps. Vertical clips go on a … |
| 214 | METHOD | methods/editing.md |  | 5. **Render.** |
| 215 | METHOD | methods/editing.md | ″ | - PIL frames piped to ffmpeg: libx264, CRF 19–20, 30 fps. |
| 216 | METHOD | methods/editing.md | ″ | - Lead 0.15 s. Tail 0.7 s (Shorts) or 3 s (long). |
| 217 | METHOD | methods/editing.md | ″ | - Render in 2 parallel parts. Long video speed is about 0.17 s per fra… |
| 218 | METHOD | methods/audio.md |  | - Music: pick the least busy track. EQ-carve it (-5 dB at 2.2k, -5 dB … |
| 219 | METHOD | methods/audio.md | ″ | - SFX: follow the Sound design system above. Events come from the scen… |
| 220 | CURRENT | QC-06 |  | - Render a stills sheet and fix overlaps before the full render. Then … |
| 221 | CURRENT | WF-01 |  | 6. **Deliver.** Platform versions, covers or thumbnails, post copy (wh… |
| 222 | STRUCT |  |  |  |
| 223 | STRUCT |  | ″ | ## Copyright |
| 224 | CURRENT | RS-07 |  | - Monetization-safe only: Pexels, CC BY/BY-SA with attribution, own AI… |
| 225 | SUPERSEDED | PUB-05 | v2 (user Nov 10): follow the official YouTube policy (PLT-09) | - Flag YouTube "Altered or synthetic content" only when AI images look… |
| 226 | CURRENT | BR-08 |  | - Avoid graphic blood in thumbnails. |
| 227 | STRUCT |  |  |  |
| 228 | STRUCT |  | ″ | ## Environment gotchas |
| 229 | METHOD | methods/editing.md |  | - Never `pkill -f` / `pgrep -f` with a pattern that also matches the s… |
| 230 | METHOD | methods/editing.md | ″ | - Don't run heavy whisper jobs alongside renders unless you have to. B… |
| 231 | STRUCT |  |  |  |
| 232 | STRUCT |  | ″ | ## Story-cinema style (standing rule from Nov 4 2026, every Short from… |
| 233 | CURRENT | ST-05 |  | The user asked for this to be the channel's continuing look so viewers… |
| 234 | CURRENT | ST-05 | ″ | - **Tell it as a story with characters.** A family or person lives the… |
| 235 | CURRENT | DIR-05 | split: DIR-05 (P) talking mouths, DIR-12 (C) continuous world and rig reuse | - **Characters = the long-video Anna & Chelli** (dl/chars2.py: anna(),… |
| 236 | CURRENT | DIR-05 | ″ | - **Cartoons talk.** Mouths move with their own lines; drive them from… |
| 237 | CURRENT | DIR-05 | ″ | - **Watching a film, not slides.** Use one continuous drawn world with… |
| 238 | CURRENT | ART-03 |  | - **Body explanations use REAL-looking imagery, not cartoons** (user N… |
| 239 | CURRENT | DIR-10 | steady camera + source chip; inside-the-body in DIR-05 | - **Body explanations go inside the body.** Use a human example and fo… |
| 240 | CURRENT | FMT-04 |  | - **Channel schedule** goes on the series slide subtitle ("SUN · FULL … |
| 241 | CURRENT | BR-02 |  | - **Telugu text:** the Telugu font has no µ ³ ≈ ≤ glyphs. te_text.surf… |
| 242 | STRUCT |  |  |  |
| 243 | STRUCT |  | ″ | ## KEEP / DROP log (update after every review) |
| 244 | STRUCT |  |  | **KEEP (working):** |
| 245 | CURRENT | RS-02 |  | - Real sources and proof cards. |
| 246 | CURRENT | ED-01 |  | - Pro voice edit with tight pauses. |
| 247 | CURRENT | LAY-02 |  | - Word-by-word captions aligned to the script. |
| 248 | CURRENT | LAY-01 |  | - Bright full-screen footage. |
| 249 | CURRENT | DIR-09 |  | - Place cards and big pop numbers. |
| 250 | EVIDENCE | history | AI art for mythology (labelled → ART-02) | - AI art for mythology. |
| 251 | CURRENT | MU-02 |  | - Calm, EQ-carved music, e.g. "the quiet meridian", "where the river b… |
| 252 | CURRENT | FMT-09 | nudge part superseded by FMT-04 | - Subscribe/follow nudges, and separate IG/YT exports. |
| 253 | EVIDENCE | history |  | - Real effigy and event photos at climaxes. |
| 254 | METHOD | methods/motion.md |  | - 2D brand animations for the explaining parts (long video). |
| 255 | CURRENT | ED-05 |  | - Phrase-anchored scene timing. |
| 256 | CURRENT | ED-01 |  | - Why? Pace Model for long videos: fast hooks, lists and asks; explain… |
| 257 | CURRENT | DIR-07 |  | - One explainer graphic per idea in Shorts too (user asked "add graphi… |
| 258 | METHOD | methods/assets.md |  | - NASA SVS animations (public domain, credit Goddard/CI Lab) for space… |
| 259 | CURRENT | ART-09 |  | - Clips sent as original MP4s straight from Pexels/NASA (never through… |
| 260 | STRUCT |  |  |  |
| 261 | CURRENT | GS-03 |  | - **Golden Sparrow 1/6 build (Nov 8 2026, approved): reuse the week's … |
| 262 | CURRENT | RS-05 |  | - **Two-territory numbers (Nov 8):** when comparing figures across dif… |
| 263 | CURRENT | ST-09 |  | - **Legal teasers (Nov 8):** narration stays short ("banned wearing ce… |
| 264 | CURRENT | FMT-06 | slide content (P); hold timing → FMT-11 (C) | - **Phone-readable end slide (Nov 8):** only 3 items (YOU'RE HERE n/6,… |
| 265 | CURRENT | ED-04 |  | - **Telugu checks (Nov 8):** verify every generated or reused Telugu l… |
| 266 | CURRENT | QC-06 | freezedetect kept; the 4–5% push is a method (methods/motion.md), HOLDs exempt | - **Static-hold QA (Nov 8):** run freezedetect (n=0.003, d=1.5) on eve… |
| 267 | METHOD | methods/editing.md |  | - **Render speed (Nov 8):** render the shared body once per language a… |
| 268 | CURRENT | PUB-02 | limits in PLT-02/03/04 | - **Post copy limits, check before sending (user, Nov 10):** Instagram… |
| 269 | STRUCT |  |  |  |
| 270 | CURRENT | DIR-03 |  | - **Process steps must be shown happening, as precisely as in the film… |
| 271 | EVIDENCE | history | GS 2/6 score | - **Golden Sparrow 2/6 "The cloth the world wanted" (Nov 10): EN 2:27 … |
| 272 | STRUCT |  |  |  |
| 273 | CURRENT | DIR-06 |  | - **Match cut + one recurring object (GS 3/6, Nov 10, approved):** for… |
| 274 | CURRENT | WF-02 |  | - **Motion previews before a full render (Nov 10):** for an upgraded e… |
| 275 | EVIDENCE | history | GS 3/6, 4/6 scores | - **Golden Sparrow 3/6 "Diamonds made the legends, cloth filled the sh… |
| 276 | EVIDENCE | history | ″ | - **Golden Sparrow 4/6 "Follow the money" (Nov 10): EN 1:49 / TE 2:16,… |
| 277 | CURRENT | GS-02 |  | - **Archival styling for historical series (GS 4/6, approved):** annot… |
| 278 | STRUCT |  |  |  |
| 279 | CURRENT | QC-01 |  | - **Professional visual QC is a delivery gate (user, Nov 10, GS 4/6 pr… |
| 280 | CURRENT | BR-01 | reworded by decision 3 (user Nov 10) | - **Palette:** ink #0A0A0A, cream #F4F1EA, amber #FFB224, plus restrai… |
| 281 | CURRENT | BR-04 |  | - **One component per UI element.** Corner badges come only from `pipe… |
| 282 | CURRENT | QC-01 |  | - **Checklist (record each item per video in QC_report.md, with every … |
| 283 | CURRENT | QC-01 | ″ | - **Frame-level inspection:** full contact sheet of the whole video; k… |
| 284 | CURRENT | LAY-02 | its "soft bottom fade" is SUPERSEDED by LAY-01 (user Nov 10) | - **Captions get their own lane (user, Nov 10, GS 4/6):** captions mus… |
| 285 | CURRENT | LAY-01 |  | - **Use the whole screen; no masked bottom (user, Nov 10, after GS 4/6… |
| 286 | CURRENT | QC-05 |  | - **Automated layout checks:** components register their boxes with `l… |
| 287 | CURRENT | LAY-05 |  | - **Sharp pictures only (user, Nov 10, after GS 3/6):** blurry frames … |
| 288 | STRUCT |  |  |  |
| 289 | STRUCT |  | ″ | **DROP (failed; never repeat):** |
| 290 | DROP | BR-05 |  | - Epic/cinematic style. |
| 291 | DROP | LAY-01 |  | - Visuals in bands or boxes. |
| 292 | DROP | ED-01 |  | - Basic take-picking with natural pauses. |
| 293 | DROP | MU-02 |  | - Busy music (e.g. "under the marigold arch"). |
| 294 | DROP | SD-01 |  | - Hissy noise whooshes and risers. |
| 295 | DROP | LAY-01 |  | - Heavy dims. |
| 296 | DROP | DIR-08 |  | - Fade-in or a black first frame. |
| 297 | DROP | FMT-06 |  | - Long static or black end screens (Shorts). |
| 298 | DROP | LAY-04 |  | - Headlines that paraphrase the voice. |
| 299 | DROP | FMT-09 |  | - "SUBSCRIBE" on Instagram. |
| 300 | SUPERSEDED | DIR-02 | "holds over 4 s" as a fail rule replaced: intentional stillness allowed, marked HOLD (user Nov 10) | - Holds over 4 s. |
| 301 | DROP | ART-01 |  | - Wrong-place footage. |
| 302 | DROP | ST-03 |  | - "Hey / Do you know" openers. |
| 303 | DROP | FMT-06 |  | - Endings over 8 s. |
| 304 | DROP | ED-04 |  | - Patching whisper spellings word by word. |
| 305 | SUPERSEDED | ART-05 | "political borders on maps" replaced by the map convention (user Nov 10, decision 4) | - Political borders on maps. |
| 306 | DROP | SD-01 |  | - Generated or synthetic SFX: pings, bells, sparkles, pops ("kids' vid… |
| 307 | DROP | SD-02 |  | - Literal ambience matched to spoken words (trees for "Jammi", elephan… |
| 308 | DROP | ED-01 |  | - Even 0.5 s pauses after every sentence ("sounds slow, can't hold int… |
| 309 | DROP | ED-01 | ″ | - Shorts-style pause squeezing on long videos (204 wpm, "sounds like r… |
| 310 | STRUCT |  |  |  |
| 311 | CURRENT | CR-01 |  | - **Credits rule (user, Nov 6):** before ANY paid generation that is n… |
| 312 | CURRENT | MU-01 |  | - **Music source (user, Nov 6):** all music tracks are the user's own … |
| 313 | CURRENT | ART-04 |  | - **Images (user, Nov 6):** ElevenLabs credits can't cover a film's im… |
| 314 | METHOD | methods/editing.md |  | - **Film grain cost (Nov 6):** per-frame random grain at σ≈5.5 drove x… |
| 315 | CURRENT | GS-01 |  | - **Golden Sparrow visual system (user-approved Nov 6, after rejecting… |
| 316 | STRUCT |  |  | **Score history:** |
| 317 | EVIDENCE | history | GS film; thumbnail → GS-06 | - Golden Sparrow S1 v5 APPROVED (Nov 7): editorial thread cards (vary … |
| 318 | EVIDENCE | history | GS film v3; DROP depth parallax on people → MO-02 | - Golden Sparrow S1 full films v3 (Nov 7): EN 13:51, TE 16:54, 1920×10… |
| 319 | EVIDENCE | history | score history; extracted: 325 → RS-04, 327 KEEP outline → ART-05, 328 → RS-06 | - Golden Sparrow S1 film + 6 Shorts, narration recorded (Nov 6, pictur… |
| 320 | EVIDENCE | history | ″ | - Ravana Short (Oct 23): not scored. |
| 321 | EVIDENCE | history | ″ | - Saturday Short (Oct 24): v2 6.5, v3 about 7.5. The gaps were in the … |
| 322 | EVIDENCE | history | ″ | - Sunday Short "Why burn Ravana" (Oct 25): v1 8.0, v2 8.4. Remaining: … |
| 323 | EVIDENCE | history | ″ | - Gold Short 1 "Your gold came from dead stars" (Oct 26): EN 8.3, TE 8… |
| 324 | EVIDENCE | history | ″ | - Gold Short 2 "Why gold never rusts" (Oct 27): EN 8.2, TE 8.0. Strong… |
| 325 | EVIDENCE | history | ″ | - Diwali Short 5/6 "₹7 lakh crore of festive trade: where does it all … |
| 326 | EVIDENCE | history | ″ | - Diwali Short 6/6 v6 (finale, story version, Nov 7): EN 2:26, TE 2:46… |
| 327 | EVIDENCE | history | ″ | - Diwali Short 6/6 (finale) "Why does Delhi's air get so bad around Di… |
| 328 | EVIDENCE | history | ″ | - Diwali Short 4/6 "Why India's stock market opens on Diwali, for 70 m… |
| 329 | EVIDENCE | history | ″ | - Diwali Short 3/6 "Why every home gets deep-cleaned before Diwali" (N… |
| 330 | EVIDENCE | history | ″ | - Diwali Short 2/6 "That India-from-space photo? Not Diwali." (Nov 3):… |
| 331 | EVIDENCE | history | ″ | - Diwali Short 1/6 "Is your Diwali bonus a gift… or the law?" (Nov 2):… |
| 332 | EVIDENCE | history | ″ | - Gold long "Why Is Gold So Expensive?" (Oct 28): EN 8.4, TE 8.2. Stro… |
| 333 | EVIDENCE | history | ″ | - Long video "Dussehra Is NOT One Story. It's Three." (Oct 26): v1 8.3… |
| 334 | STRUCT |  |  |  |
| 335 | STRUCT |  | ″ | ## Update Oct 28 2026: new style, new workflow, voice via ElevenLabs |
| 336 | SUPERSEDED | WF-01 | Oct 28 workflow replaced by the Nov 8 order | - **Workflow (replaces record-first):** topic → Claude script (EN+TE, … |
| 337 | SUPERSEDED | CR-02 | 0.46 credits/char estimate replaced by measurement; reuse → CR-03 | - **Credits:** ~0.46 credits/char (eleven_v4). Telugu ≈ 1,200/Short, E… |
| 338 | SUPERSEDED | QC-03 | score target restated as a target beside the gate (user Nov 10) | - **Target score: 8.5/10.** |
| 339 | CURRENT | BR-05 |  | - **Style v2 (approved):** dark glass cards with amber edge bar, amber… |
| 340 | CURRENT | ART-07 | evidence board in DIR-09 | - **Evidence board (Johnny Harris verification):** real screenshots → … |
| 341 | METHOD | methods/editing.md |  | - **Telugu captions:** PIL + RAQM (cairo toy fonts can't shape Telugu)… |
| 342 | METHOD | methods/editing.md | ″ | - **Gotcha:** pill/scale(0) → cairo singular matrix → "out of memory" … |
| 343 | STRUCT |  |  |  |
| 344 | EVIDENCE | history | KEEP (Gold 3) | **KEEP:** evidence clippings + highlighter sync (Gold 3), relativity O… |
| 345 | DROP | BR-01 | red accents; mascot (BR-05); recreated screenshots (ART-07); two-take TTS (CR-02) | **DROP:** red accents; "?" mascot with eye; recreated screenshots; two… |
| 346 | STRUCT |  |  |  |
| 347 | STRUCT |  | ″ | **Score history:** |
| 348 | EVIDENCE | history |  | - Ravana new-style test (Oct 27): v1 ~8.0 (red + mascot rejected), v2 … |
| 349 | EVIDENCE | history | ″ | - **Golden Sparrow 1/6 "Was India really the golden sparrow?" (Nov 8):… |
| 350 | EVIDENCE | history | ″ | - Gold Short 3 "Why is gold yellow?" (Oct 28): EN/TE ~8.0. Holding bac… |
| 351 | CURRENT | BR-08 | layout now per series plan | - **Covers (Oct 28):** hero image from ChatGPT (Claude gives the promp… |
| 352 | CURRENT | CR-03 |  | - **Voice line library (Oct 28):** `voice_lib/` (see its README). Chec… |
| 353 | EVIDENCE | history | measured rate → methods/editing.md | - Gold Short 4 "Why is India bringing its gold back home?" (Oct 28): E… |
| 354 | CURRENT | ART-07 |  | - Asset rule: when a capture tool can't screenshot, print-to-PDF is fi… |
| 355 | CURRENT | ST-08 |  | - **Voice direction (user, Oct 28):** expressive but LIGHT. Use mild t… |
| 356 | SUPERSEDED | FMT-01 | merged into FMT-01 (user Nov 10) | - **Length (user, Oct 28):** Shorts may run up to 3 min if interesting… |
| 357 | EVIDENCE | history |  | - Gold Short 5 "Why do Indians trust gold more than banks?" (Oct 29): … |
| 358 | CURRENT | BR-02 |  | - **₹ glyph (Oct 29):** Archivo Black / Space Mono have no ₹; `brand/f… |
| 359 | METHOD | methods/editing.md |  | - **Caption fix (Oct 29):** whisper drops/duplicates words at chunk ed… |
| 360 | CURRENT | RS-03 |  | - **Number check (Oct 29):** every on-screen formula must match the sc… |
| 361 | EVIDENCE | history | KEEP kinetic data → DIR-09 | **KEEP:** kinetic-data template for money topics; source footnote on s… |
| 362 | CURRENT | BR-08 |  | - **Cover rule (user, Oct 29):** no recognizable person's face on cove… |
| 363 | CURRENT | BR-09 |  | - **CTA upgrade (user, Oct 29, from Gold 6 on; built: pipeline/style_v… |
| 364 | CURRENT | BR-07 |  | - **Accounts (for the CTA card):** YT EN "Why?" @WhyEveryQuestionHasAS… |
| 365 | SUPERSEDED | FMT-05 | twice-per-Short and every-2-minutes replaced (user Nov 1, Nov 10); card details kept in FMT-05 | - **CTA placement (user, Oct 29, all videos):** Shorts: the animated c… |
| 366 | CURRENT | FMT-02 |  | - **Weekly schedule (user, Oct 29):** full (long) video every **Sunday… |
| 367 | SUPERSEDED | FMT-06 | spoken schedule line replaced by the v3 ending (user Nov 1) | - **New ending (from Gold 6):** series slide (week name, full-video th… |
| 368 | SUPERSEDED | FMT-06 | ″ | EN: "If you like learning things like this, we post a full video every… |
| 369 | SUPERSEDED | FMT-06 | ″ | TE: "ఇలాంటి కొత్త విషయాలు నేర్చుకోవడం నచ్చితే, ప్రతి ఆదివారం ఒక full v… |
| 370 | CURRENT | FMT-10 | click-on-spoken-word part superseded with 367–369 | The animated subscribe/follow card clicks exactly on the spoken "Subsc… |
| 371 | CURRENT | FMT-08 | 6/6 open-questions part SUPERSEDED by FMT-07 (user Nov 10) | - **Teasers & open questions (user, Oct 29):** Shorts 1/6–5/6 end with… |
| 372 | EVIDENCE | history |  | - Gold Short 6 "Why is gold falling right now?" (Oct 30): EN/TE ~8.5. … |
| 373 | CURRENT | ED-02 |  | - **Pacing (user, Oct 30):** information lines faster, branding/reques… |
| 374 | METHOD | methods/editing.md |  | - **Whisper on generated voice:** use overlapping ~22 s windows (keep … |
| 375 | EVIDENCE | history | KEEP → FMT-06, ED-02, BR-09 | **KEEP:** series slide, open questions with real-image cards, per-segm… |
| 376 | CURRENT | ST-06 | split: ST-06 (P, only where approved) cast and voices; ST-11 (C) film pattern | - **Long video format (user, Oct 30):** 2D two-character story — ANNA … |
| 377 | CURRENT | FMT-03 |  | - **Shorts vs long:** each Short adds facts not in the long video; the… |
| 378 | CURRENT | ST-11 |  | - **"Let me record this" framing (user, Oct 30):** in the cold open An… |
| 379 | SUPERSEDED | PUB-03 | "2 niche + 2 searchable + #whyeveryquestion" replaced (user Nov 10, decision 5); limit → PLT-02; advice → PLT-08; no short IG cuts → FMT-09 | - **Instagram rules (Oct 30 audit):** max **5 hashtags** per post/Reel… |
| 380 | METHOD | methods/motion.md |  | - **2D long-video pipeline (Diwali long, Oct 30):** `videos/2026-11-01… |
| 381 | EVIDENCE | history |  | - Diwali long "DIWALI, EXPLAINED" (Nov 1, first 2D two-character video… |
| 382 | METHOD | methods/editing.md |  | - **Gotchas (Oct 30):** cairo `paint_with_alpha` ignores a rectangle p… |
| 383 | EVIDENCE | history | KEEP → ST-06, ED-05 | **KEEP:** two-character 2D format; per-line voice clips (re-timing, re… |
| 384 | CURRENT | RS-01 | recency now applies to time-sensitive facts only (v2, user Nov 10) | - **Research rule (user, Oct 31 — after the Diwali bonus miss):** befo… |
| 385 | CURRENT | WF-01 |  | - **Scene sheet before render (user, Oct 31):** after the script is lo… |
| 386 | CURRENT | DIR-01 |  | - **Animation style in the scene sheet (user, Nov 8 2026):** the scene… |
| 387 | CURRENT | BR-06 |  | - **Telugu on-screen text (user, Oct 31):** the TE version must show T… |
| 388 | METHOD | methods/editing.md |  | - **Runtime check method:** always measure runtime AFTER the standard … |
| 389 | CURRENT | DIR-09 | v3 toolkit; reset every 8–12 s → DIR-04 | - **SHORTS STYLE v3 = DEFAULT from Nov 1 2026 (user: "let's try this f… |
| 390 | CURRENT | DIR-09 | ″ | - Script: explain through 2–3 named people with concrete numbers; show… |
| 391 | CURRENT | DIR-09 | ″ | - Visuals: moving avatars against a threshold line; clippings as evide… |
| 392 | CURRENT | FMT-04 | and FMT-06 | - Ending: NO mid-video subscribe card in Shorts; no spoken "full video… |
| 393 | SUPERSEDED | FMT-01 | 2:45/2:50 runtime targets removed (user Nov 10, decision 1) | - Process: scene sheet approved before render; runtime ≤ 2:45 EN / ≤ 2… |
| 394 | CURRENT | AN-03 |  | - Watch after posting: replay rate (loop) and any dip at the correctio… |
| 395 | SUPERSEDED | FMT-01 | hard limit kept; 2:45/2:50 targets removed (user Nov 10, decision 1); budgeting → methods/editing.md | - **Shorts HARD LIMIT (user, Oct 31): every Short/Reel must be under 3… |
| 396 | CURRENT | DIR-09 | its "every-2-min card for long videos" part SUPERSEDED by FMT-05 | - **Shorts visual rules (from ChatGPT storyboard review, Oct 31, agree… |
