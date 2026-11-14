---
name: why-channel-video
description: Produce a Why? channel explainer (Short or long, English + Telugu): research, script, voice, scene sheet, render, QC and publishing. Master playbook: precedence, rule index, gated workflow, formats and credits.
---

# Why? production system: master playbook

Channel: "Why?" and "Why? Telugu" (handles → BR-07). Faceless explainers and story documentaries that answer a "Why…?" question.

## How rules work
- **Load for every video:** this file, `brand.md`, `platform_rules.md`, the role guides for the stage you are in (`roles/`), the series plan (`plans/<series>.md`) and the video's production brief. **Never load `history.md` as instructions**: it is a record. `MIGRATION.md` records the Nov 2026 reorganisation.
- **Precedence (highest first):** (1) the user's latest explicit instruction or approval for that topic and scope; (2) the video's approved plan (production brief + scene sheet); (3) the approved series plan; (4) the channel-wide rule in its owner file; (5) `history.md`, reference only. A video or series decision beats a channel rule only if it was approved after that rule or explicitly as an exception to it.
- **What counts as approval:** the user's explicit instruction or approval of a stated rule (dated) → a CURRENT rule in the scope given. Approval of a finished video → evidence for that video, not a channel rule. Claude's proposals, audit recommendations and ChatGPT review points → PROPOSED until the user approves. Measurements and methods → evidence or method notes, updated by measuring.
- **Replace, don't append:** (1) find the active rule by ID in the index below; (2) rewrite it in its owner file and raise its version; (3) move the old text to `history.md` as SUPERSEDED with date, replacement ID and version, reason, scope and the user's words; (4) update every reference (search the ID and the old wording); (5) confirm one current rule remains for that topic and scope.
- **No new channel-wide rule without the user's approval.** Lessons from a video enter `history.md` as TEST.
- **Exceptions** go in the brief's Exceptions table by rule ID, scope and date; they never edit the shared rule.
- **Rule format:** each rule is defined once, as `**[ID]**`, in its owner file and cited elsewhere as `→ ID`. Tags: **P** = production rule (pass/fail), **C** = creative guidance (professional judgment). Sources in brackets.
- The saved account skills `why-channel-video` and `why-channel-post-copy` are older copies. Where they disagree with these files, these files win.

## Rule index
| Topic | Rule IDs | Owner |
|---|---|---|
| Workflow, previews, release dates, after delivery, honest review, light workflow | WF-01 – WF-07 | this file |
| Shorts length, schedule, film vs Shorts, reminders, endings, exports | FMT-01 – FMT-11 | this file |
| Credits, voice generation, voice library | CR-01 – CR-03 | this file |
| Palette, fonts, series tag, components, look, Telugu text, handles, covers, CTA card | BR-01 – BR-09 | `brand.md` |
| Full frame, captions, safe zones, captions as main text, image scale | LAY-01 – LAY-05 | `brand.md` |
| Fact checking, sources, numbers, estimates, licences | RS-01 – RS-08 | `roles/research.md` |
| Screenwriting standard, hooks, voice, examples, characters, formats, voice direction | ST-01 – ST-11 | `roles/story.md` |
| Styles in the scene sheet, failing scenes, process shown, rhythm, film-not-slides, toolkit, long-film structure | DIR-01 – DIR-12 | `roles/director.md` |
| Right place, labels, real imagery, image sourcing, maps, image size, real captures, owned assets first, clip sources | ART-01 – ART-09 | `roles/art.md` |
| Moves within native resolution, animate information, historical look, libraries | MO-01 – MO-04 | `roles/motion.md` |
| Music source, calm under voice, cue sheet | MU-01 – MU-03 | `roles/music.md` |
| Real SFX only, on-screen events, variety, inventory, ambience | SD-01 – SD-05 | `roles/sound.md` |
| Audio edit, pacing, loudness, Telugu and caption checks, phrase timing | ED-01 – ED-05 | `roles/editor.md` |
| Delivery gate, severity, score, reporting, layout checks, technical checks | QC-01 – QC-06 | `roles/qc.md` |
| Post copy, counts, hashtags, after upload, disclosure, CTA text, claims | PUB-01 – PUB-07 | `roles/publishing.md` |
| Platform limits, disclosure policy and recommendations (dated, sourced) | PLT-01 – PLT-09 | `platform_rules.md` |
| Data before diagnosis, weekly review, post-launch watch | AN-01 – AN-03 | `roles/analytics.md` |
| Golden Sparrow series | GS-01 – GS-06 | `plans/golden_sparrow.md` |

Templates (`templates/`) hold structure and rule IDs only, never rule text.

## Workflow
- **[WF-01]** (P, user Nov 8; additions Nov 10; step 3 v2 Nov 13) Order of work:
  1. Agree the topic.
  2. Research and verify every fact (→ RS-01).
  3. Write the full English and Telugu scripts (→ ST-07) in the production brief as an **audiovisual script** (v2, user Nov 13): the story and the viewing plan are written together, before any voice. Each beat names
     - **who** carries it: the host on camera, the narrator voice-over, or a story character;
     - **the line** in English and in natural Telugu;
     - **what is on screen** and its treatment (host framing and gesture, human scene, evidence card, WHY? reveal, a named style or effect);
     - **why it is there**: the question it raises, the point it proves or the feeling it creates.
     Before approval the script is read twice: as a viewer (curious? clear? want the next beat?) and as a director (can every line be shown? does each host appearance earn its place? can we make it with our tools and budget?). A line that can't be shown is rewritten at script stage. The host, the WHY? reveal and evidence cards are optional per story, never forced. Sources and the estimated credits are included. The scene sheet (step 7) later adds exact timing, styles and assets.
  4. Script versions: the user asks for changes until he approves the final script. Nothing below starts before that.
  5. Generate both voices, one take each, reusing the voice library (→ CR-02, CR-03).
  6. Edit the voice (→ ED-01).
  7. Send one message with the scene sheet (what is on screen for each line and the animation style for every line or chapter, → DIR-01) and the resource list (pictures, stock clips, screenshots with source links, music, SFX, image prompts).
  8. The user gives changes until the scene sheet and its styles are agreed.
  9. The user sends the assets. Never render before they arrive.
  10. Send stills only if the style is changing; motion previews per WF-02.
  11. Render English and Telugu, with separate YouTube and Instagram versions (→ FMT-09).
  12. Run QC (→ QC-01).
  13. Deliver the videos, cover and post copy.
  14. One short honest report: score (→ QC-03), defects, credits used and credits left.
  15. Update the system (→ WF-05), commit and push.
- **[WF-02]** (P, user Nov 10) For an upgraded edit or a new or risky sequence, render 10–20 s previews of the key sequences in both languages with sound. Approval of the previews covers the full render.
- **[WF-03]** (P, user Oct 27) Never render a full video only to test a style.
- **[WF-04]** (P, user Nov 6) Release dates are fixed. Never propose moving them; flag critical blockers early.
- **[WF-05]** (P, user Nov 10; Phase 2A approval Nov 10) After delivery: the score, defects and lessons go to `history.md` (EVIDENCE or TEST); a rule changes only when the user approves it, by the replace procedure above; commit and push every time.
- **[WF-06]** (P, user Oct 24) After every delivery give a full, honest review: score each area, name every mistake and the upgrade needed. Never inflate.
- **[WF-07]** (P, user Nov 10) Keep the workflow light. For straightforward Shorts, the role outputs are combined into three documents: one research-and-story brief (the production brief), one director's scene sheet with assets, music and sound cues, and one QC report. The roles are professional passes, not eleven separate reports.

## Formats
- **[FMT-01]** (P, user Nov 10, replaces the Oct 31 targets) Every Short and Reel is under 3:00 including the ending, in both languages. The story sets the length. Plan with an internal safety margin from measured speech (method in `roles/editor.md`). Never pad to reach a duration or rush narration to meet a target. If a script is over budget, cut at script stage, not after voicing (user Oct 31).
- **[FMT-02]** (P, user Oct 29, Nov 6) The film posts on Sunday and Shorts Monday–Saturday; each video is made at least a day before it posts. Each week is a connected season: the Sunday film plus six connected Shorts.
- **[FMT-03]** (C, user Oct 26) The film is a complete deep-dive, not a stitch of the Shorts; split it into parts if it is too big. Shorts carry the most interesting angles, add facts the film doesn't have, and drive viewers to it.
- **[FMT-04]** (P, user Nov 1) Shorts have no mid-video subscribe card and no spoken schedule or subscribe lines. The schedule appears only on the series slide.
- **[FMT-05]** (P, user Nov 10; card details user Oct 29) In long films, the brief sets the number of subscribe reminders and places them at story breaks, never at fixed intervals and never interrupting a scene. Mid-video cards are smaller than the end card, with click/bell SFX at about half volume and no extra narration, placed off the key visual, never in the first 15 s.
- **[FMT-06]** (P, v2 user Nov 1, Nov 8 and Nov 10) Shorts other than a season's last end with the phone-readable series slide: YOU'RE HERE n/6, NEXT n+1/6 with tomorrow's tease, and the full-film pointer (YT "FULL FILM · RELATED VIDEO", IG "FULL FILM ON YOUTUBE · LINK IN BIO"). It carries the platform-correct on-screen Subscribe/Follow button, and its text stays readable on a phone. Then a loop line runs into the opening, and the last frame equals the first.
- **[FMT-11]** (C, v2 user Nov 10) End-slide timing is an editing judgment: hold the slide long enough to read (about 5 s is typical) and keep the ending short (around 8 s or less). Never a long static end screen.
- **[FMT-07]** (P, user Nov 10) The last Short of a season answers its own central question with a satisfying conclusion. It may then build anticipation for the next season with a question or teaser. A loop is optional.
- **[FMT-08]** (C, user Oct 29) Each Short's tease names the next Short, so the week's topics are planned up front. No likes targets (engagement bait).
- **[FMT-09]** (P, user Oct 28–30) Each Short has four exports: EN and TE, each in a YouTube (SUBSCRIBE) and an Instagram (FOLLOW) version. Instagram gets the same full video; no shortened IG cuts.
- **[FMT-10]** (C, user Oct 29) "GOT A WHY? COMMENT IT" appears as on-screen text only, without voice.

## Credits
- **[CR-01]** (P, user Nov 6) Before any paid generation that isn't in the approved plan (images, video, extra takes), price it and ask first. Default: one generation.
- **[CR-02]** (P, user Oct 27–28) ElevenLabs is for voice (anything else only under CR-01). Generate one take per line. Budget about 2,000–2,400 credits per Short for both languages. Report credits used and credits left after every video. Measured rates are kept in `roles/editor.md` (method).
- **[CR-03]** (P, user Oct 28) Check every script line against `voice_lib/index.json`. Reuse exact sentence or phrase matches only, never single words. Save every new line with an index entry.
