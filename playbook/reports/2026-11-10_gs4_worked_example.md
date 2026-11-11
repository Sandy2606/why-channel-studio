# Worked example: the new checks applied to GS 4/6 "Follow the money"

A record, not instructions. It applies the Phase 2A research, story, director and visual-QC checks to GS 4/6's script v1 and scene sheet v1, and compares them with what actually happened: three script versions, four visual revision rounds after the previews, and 16 logged defects.

**How it is judged.** "Advance-detectable" means a check that existed *before* GS 4/6 began, run through the new structured checklists, would have flagged the problem before the full render. A problem only counts as advance-detectable if the rule behind it predates GS 4/6. Rules that were created *because of* GS 4/6 (the caption lane, archival styling, the shared badge, whole screen) count as hindsight for this video, even though they will now protect future videos. These are estimates; the real test is the pilot on a new video.

## Script stage (v1 → v3)
| Issue | How it was found | New check | Verdict |
|---|---|---|---|
| Famine figures not labelled as estimates (v1 line 12) | Script review (v1 → v2) | RS-04, which has required estimate labels since Nov 6 | **Advance-detectable**: a rule that already existed was missed |
| "A foreign merchant needed a farman just to trade" overstated what farmans did | Script review | The researcher's source register: each claim must quote its supporting source (RS-02); Chaudhuri and Pearson describe trading rights and privileges | **Likely** detectable. It needs a careful reading of the source, so it is judgment, not automation |
| "Even [Virji Vora] lived by the ruler's permission" was one-sided | Script review | Research checklist item 4 (frame disputed or two-sided relationships as such); Pearson's merchant–ruler interdependence | **Likely** detectable |
| "Every ruler wanted one thing: trade" overgeneralised | Script review | The same register check | **Likely** detectable |
| Telugu Madanna–Akkanna line reused from the film with a disputed origin and imprecise roles (v2 → v3) | Your review | Research checklist item 1 (every claim, including reused audio, has a register entry); the film's own lesson, now in `history.md` (DROP "Telugu brothers") | **Advance-detectable**: the lesson already existed, but reused lines weren't re-checked |

**A new story-check finding** (not in the original log, offered for future scripts, not as a defect): ST-01 asks for a payoff that answers the hook ("why did so many of the people who made it stay poor?"). The approved script answers it implicitly, through the chain and the famine; it never says the answer in one line before the turn to the ports. A beat-map pass would have suggested one sentence there, such as "most of what they made flowed up the chain". The "who was in charge?" section is the weakest link to the central question.

## Scene sheet v1 and preview stage (the four revision rounds)
| Round | What happened | New check | Verdict |
|---|---|---|---|
| 1. Red seal stamp on the farman looked cheap | You, at preview | A palette check on the preview (no red since Oct 27, PB:339/345) | **Partly**: the red was catchable by an existing rule; "looks cheap" was your taste, which is hindsight |
| 2. Split-flap board and "EARLIER · 1498" stamp looked too modern | The scene sheet named "Remotion Split-Flap" and a stamp; you asked for a fallback, then rejected it at preview | A series-consistency check against the GS visual system (Nov 6), which doesn't include split-flap boards | **Partly**: it would have been *raised as a question* before the preview; the rule that now fails it (MO-03, GS-02) came from this video |
| 3. Badge text touching its edge, Telugu sitting high | You, at preview | Measuring text bounds on the stills sheet before render (PB:220 already required "fix overlaps before the full render") | **Advance-detectable**: measurable geometry |
| 4. Captions sitting over pictures and labels in a fixed spot | You, at preview | QC checklist item 8 (no caption overlapping a label or document), measurable from the registered boxes | **Partly**: the overlaps were detectable; "looks automatic" was taste, which is hindsight. The caption-lane rule came from this video |

The scene sheet also showed the famine map as "GUJARAT and DECCAN glow dark red". A palette check would have raised it for a decision (now under BR-01, decision 3).

## The 16 logged defects
| # | Defect | Stage found | Could the new system catch it earlier? |
|---|---|---|---|
| 1 | Red stamps (round 1) | Preview | Partly (see above) |
| 2 | Split-flap / red 1498 (round 2) | Preview | Partly (see above) |
| 3 | Badge edge / Telugu high (round 3) | Preview | Yes: measurable on stills |
| 4 | Captions over content (round 4) | Preview | Partly |
| 5 | "TRADING RIGHTS" overflowed its card | Layout QC after render | Yes: `qc_layout` run on the previews or stills (the chain was in the preview set) |
| 6 | Outgoing and incoming cards overlapping | Layout QC after render | Yes, same |
| 7 | TE Mughal-front label collided with the Deccan labels | Layout QC after render (TE) | Yes, if the TE map was previewed or stilled: measurable |
| 8 | The farman slid through the caption lane | Layout QC after render | Yes: measurable (it was in the previewed chain) |
| 9 | Two credits overlapping at the globe cut | Layout QC after render | Yes: measurable on a stills pass of transitions |
| 10 | TE static holds of 2.7–3.9 s | Frame QC after render | Yes: the scene sheet already showed TE lines 30–40% longer on the same shots. A director check ("are TE holds deliberate HOLDs?") plus freezedetect on the previews would flag them |
| 11 | First 3 s: grid flicker and fade popping | Frame QC after render | No: only visible frame by frame, and the hook wasn't in the preview set. Same stage as before |
| 12 | A chain label drifted into the caption lane | Frame QC after render | Yes: measurable, and it was in the previewed chain |
| 13 | The globe's own source line sat behind the captions | Frame QC after render | No: the text is baked into the Remotion clip, so automation can't see it. Human frame review, same stage |
| 14 | The "Europe" globe label shrank to a sliver | Frame QC after render | Only with a manual still review of the Remotion clip before compositing; otherwise the same stage |
| 15 | "Dramatized" chip touching the picture border | Frame QC after render | Yes: measurable if registered |
| 16 | Disk allowance ran out during the mux | Technical | Not applicable: these checks don't cover it |

## Result
- **Script stage:** 2 of the 5 corrections were advance-detectable under rules that already existed; 3 more were likely detectable through the source register. All five depend on the research and story passes being done *before* you see the script.
- **Previews (4 rounds):** 1 advance-detectable (the badge); 3 partly (each one's measurable part is detectable, but its taste part isn't); 0 fully avoidable without hindsight.
- **16 defects:** 9 could have been caught before the full render by running the existing layout and freeze checks on previews and stills (3, 5, 6, 7, 8, 9, 10, 12, 15); 3 partly (1, 2, 4); 3 not earlier (11, 13, 14); 1 not applicable (16).
- **What it would not have changed:** your taste judgments at preview (the cheap-looking stamp, the modern-looking split-flap, the automatic-looking captions, the bottom fade reading as a mask). Those created the rules that now protect future videos, which is the system learning, not the system predicting.
- **Cost:** a source register and a beat map in the brief (about 15–20 minutes of my work on a Short); running `qc_layout` on the previews (a few minutes). No new approval steps for you.

The largest realistic gain is moving the existing layout checks from after the full render to the preview and stills stage. Running them on previews uses the existing GS 4/6 checker today. Making that standard is Phase 2B work (the general QC scripts).
