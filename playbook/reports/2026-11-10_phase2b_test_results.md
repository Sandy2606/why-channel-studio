# Phase 2B test results (Nov 10)

A record, not instructions. All runs used the `pro-system` branch in this workspace; nothing was merged.

## 1. Self-test: synthetic good and deliberately failing fixtures
`python3 pipeline/qc/tests/run_tests.py` covers 32 cases, all behaving as expected; the full table is in `pipeline/qc/tests/LAST_RUN.md`. The fixtures are deterministic: an earlier version with random pink-noise audio gave 2 of 32 inconsistent loudness results, so it was replaced with a calibrated sine (−14.1 LUFS).
| Known problem | Case | Result |
|---|---|---|
| Clipped caption text | `layout: clipped caption text` | FAIL detected |
| Overlapping caption and label | `layout: caption overlaps a label` | FAIL detected |
| Caption sitting on a picture | `layout: caption on a picture` | FAIL detected |
| Misaligned corner badges | `layout: misaligned corner badges` | FAIL detected |
| Element too close to the frame edge | `layout: card too close to the edge` | FAIL detected |
| Partial layout coverage (Remotion, baked-in text) | `layout: partial coverage never passes` | INCOMPLETE, never PASS |
| Missing source or licence | `assets: missing licence…` | FAIL detected |
| Excessive image scaling (1.8×) | same case | FAIL detected |
| Unlabelled AI image | same case | REVIEW |
| Claim without a register entry | `sources: claim C2 missing` | FAIL detected |
| Wrong export dimensions | `video: wrong dimensions`; `exports: wrong dimensions in one version` | FAIL detected |
| Missing platform version | `exports: missing platform version` | FAIL detected |
| Short over 3:00 | `video: Short over 3:00` | FAIL detected |
| Clipping, loud audio | `video: clipping, too loud` | FAIL detected |
| Audio dropout | `video: audio dropout` | REVIEW |
| Black first second | `video: black first second` | FAIL detected |
| Unmarked still vs the same still marked HOLD | two cases | REVIEW vs PASS |
| Post copy: 11 hashtags, 120-character title, no disclosure | `copy: long title…` | FAIL detected |
| Real known defect: GS 1/6's original copy with 30 hashtags (commit 0b65210) | `copy: GS 1/6 original` | FAIL detected |
| Duplicate rule ID; retired wording reintroduced | two `rules:` cases | FAIL detected |
| Good 9:16 and good 16:9 files, a complete register, compliant copy, all four exports | positive cases | No false FAIL; checks that need a person stay NOT PERFORMED |

## 2. Against completed videos (reproducing the delivered QC)
| Video | Check | Delivered QC_report | New checker |
|---|---|---|---|
| GS 4/6 EN_YT / EN_IG | Duration, loudness, true peak, loop seam, frame 1 | 109.19 s, −14.8, −1.7 / −1.8, 0.61, 142 | 109.19 s, −14.8, −1.7 / −1.8, 0.61, 142.2: **identical** |
| GS 4/6 TE_YT / TE_IG | same | 135.68 s, −14.7, −1.8, 0.55, 143 | 135.68 s, −14.7, −1.8, 0.55, 143.4: **identical** |
| GS 4/6 | Black frames, decode errors | none, 0 | none, 0 |
| GS 4/6 EN and TE | Layout (render script, 1 s steps) | 0 defects | 0 defects in 109 frames each. Globe clip and in-image text reported NOT PERFORMED; 2 EN frames (104–105 s) had no registered text: REVIEW |
| GS 2/6, 3/6, 4/6 | All four exports | delivered | PASS (all present, 1080×1920, h264/aac, 30 fps, same body) |
| GS 2/6, 3/6, 4/6 | Post copy | delivered | FAIL only on the new PUB-02 "verification date" line, and REVIEW for #WhyTelugu (PUB-03). Both rules post-date these copies (Nov 10), so these are expected findings, not checker errors |
| GS 4/6 | Assets, sources | no register, no claim markers | NOT PERFORMED (never shown as a pass) |
| GS Season 1 film, EN 16:9 (13:51) | Full technical pass | approved | 1920×1080 long format; −14.0 LUFS; −1.3 dBTP; 0 decode errors; frame 1 at 160.8/255 |

## 3. False positives recorded
- **Black frames on dark brand backgrounds (fixed).** The first film run flagged 5 "black" intervals; they were ink (#0A0A0A) design backgrounds while graphics build. The threshold went from pixel brightness 0.06 to 0.03; a re-run of the film found 0, and pure black is still caught (fixture passes).
- **Freezes (QC-06 threshold d = 1.5 s, stricter than the 2.5 s the GS 4/6 script used).**
  - GS 4/6: 7 EN and 8 TE unmarked holds. They include the TE hook grid (0–4.3 s, whose slow light sweep is below the motion threshold) and the end-slide hold.
  - Film: 44 holds (document and evidence holds).
  - All are REVIEW, never FAIL. Once scene sheets mark HOLDs (DIR-02), marked holds pass automatically.
- **Sharpness.** The film had 6 low windows (dark or flat graphics, median 280); GS 4/6 had none. Always REVIEW; image enlargement is judged by `check_assets`, not by this metric.
- **The film sample clip** starts dark (frame 1 at 17/255), so it FAILs frame-1 brightness. That is correct for a clip that isn't a real opening; it was used only to test the 16:9 path.

## 4. Compatibility
- **Fresh `setup.sh` run from the branch:** completed. All six music beds were converted (including the two `.m4a` tracks), 60 sounds were linked, the fonts were linked, and the Remotion `npm ci` gave no error. The first attempt hit the workspace disk limit because of my test fixtures; after the fixture fix it ran cleanly.
- **No hardcoded project paths, names, runtimes or dimensions** in `pipeline/qc/`. Formats are detected from the file (1080×1920 or 1920×1080); EN/TE and YT/IG come from file names or arguments.
- **16:9 layout checking** is verified on synthetic dumps only: the film renderer doesn't register its boxes, so on real films that check reports NOT PERFORMED.
- **Unchanged:** music files (checksums unchanged), sound files, the catalog, renderers, styles, Remotion effects, voices and every `videos/` folder. GS 5/6 and 6/6 are untouched.

## 5. Remaining blockers before a merge
1. The user approves the SFX catalog proposal (`2026-11-10_sfx_catalog_proposal.md`); then the entries are added to `sfx/catalog.json`.
2. The rollback tag on GitHub, or acceptance of the verified commit hash (see `2026-11-10_merge_and_rollback.md`).
3. A pull request. This session can push branches but its GitHub API write access is blocked (see the delivery note); the compare link is given instead.
4. Fonts and colours remain human checks until `layout.reg()` records them. A proposed future change to `layout.py` is not part of this phase.
5. The account-skill pointers: after the merge, with separate approval.
