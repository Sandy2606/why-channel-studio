# PR #2 pre-merge report (pro-system → main), Nov 11 2026

A record for the user's decision. **PR #2 is not merged.** Nothing below is done without the user's explicit approval.

## 1. Commits
| | Commit | Note |
|---|---|---|
| `main` (GitHub) | `20fe4029f02355d4b611ba4b2df0c72ec1c0c8ac` (`20fe402`) | GS 6/6 final delivery; Season 1 complete |
| `pro-system` before this checklist | `0be61c1671f4c6cdbdc70f170c9fbdefea97772d` (`0be61c1`) | Phase 2B final safeguards |
| `pro-system` after the update | merge `feede4cc2091b185602a27eb21ac215561bcbbfb` (`feede4c`; parents `0be61c1` + `20fe402`), plus the commit that adds this report | `main` merged in, conflict resolved |
| Pre-reorganisation baseline | `fb25e5933dc52d27c7b7be6c05c1d19258a52616` (`fb25e59`) | historical only; never reset `main` to it |

`main` is now an ancestor of `pro-system`, so merging PR #2 into `main` has **no conflicts**. After the merge, `main`'s tree will equal `pro-system`'s tree exactly (verified with `git merge-tree`).

## 2. Bringing pro-system up to date
- `main` had 17 commits that were not on `pro-system` (GS 5/6 and GS 6/6). They were merged in with a merge commit (no rebase, no force-push), so every Golden Sparrow file and commit is kept.
- **One conflict:** `playbook/why-channel-video-SKILL.md`.
  - `main` had added the GS 5/6 and GS 6/6 lessons to the old single-file playbook; `pro-system` had replaced that file with the master playbook.
  - **Resolution:** keep the master playbook, and move each line `main` added to its new home, recorded in `MIGRATION.md` → "Merge addendum (2026-11-11)":
    - scores go to `history.md` as EVIDENCE;
    - lessons go to `history.md` as TEST (awaiting approval as rules);
    - the user's Nov 11 composition decision updates LAY-01 and LAY-02 (section 5).

## 3. Files changed (`main` → `pro-system`): 52
- **Modified (5):**
  - `CLAUDE.md` and `README.md` (load order for the new playbook);
  - `playbook/why-channel-video-SKILL.md` (now the master playbook: precedence, rule index, workflow, formats, credits);
  - `setup.sh` (one line: `.m4a` music is converted too);
  - `sfx/catalog.json` (paths fixed, provenance fields added, the owner-approval status from section 6).
- **Added (47):**
  - `pipeline/qc/`: 14 files (checkers, self-tests, retired-wording lists);
  - `plans/golden_sparrow.md`;
  - playbook docs: `brand.md`, `platform_rules.md`, `history.md`, `MIGRATION.md`, `roles/` ×11, `methods/` ×4, `templates/` ×6;
  - `playbook/reports/`: 7 Phase 2 records, plus this report.
- **Unchanged** (0 files differ from `main`):
  - `music/`, `brand/`, the voice files;
  - every audio file in `sfx/` (only `catalog.json` changes);
  - `pipeline/styles/`, `pipeline/remotion_effects/`, `pipeline/style_v2/`, the renderers and long-video pipeline;
  - every project in `videos/`.
- **No unexpected changes** were found: the file list matches the Phase 2A/2B scope plus this checklist's edits.

## 4. Tests performed and results
| Test | Result |
|---|---|
| `pipeline/qc/tests/run_tests.py` (self-tests) | **64 / 64 as expected**. The 63 existing cases pass, plus 1 new case: an owner-approved sound with an unrecorded source resolves as REVIEW. One existing case was updated, because the four sounds are now owner-approved: they now resolve as REVIEW instead of FAIL. Report: `pipeline/qc/tests/LAST_RUN.md` |
| `check_rules.py` (production-rule validation) | **PASS** on every check: **123 rules**, each defined once and indexed; 249 citations resolve in 30 files; no retired wording in 70 files (30 phrases, including the two superseded LAY-02 phrases); `history.md` never loaded; migration record 396/396; platform limits parse |
| `check_assets.py --catalog-integrity` (sound catalog) | **PASS**: 74 entries, every file present |
| Real GS 6/6 files, `check_exports.py` | **PASS**: 4 exports at 1080×1920 h264/aac 30 fps; body identical YT vs IG (max difference 0.00); audio in sync (lag 0 ms, r = 1.00) in both languages |
| Real GS 6/6 Telugu, `qc_video.py` | PASS on dimensions, duration, black frames, loudness (−14.7), true peak (−1.6), decode, frame 1 and sharpness. **REVIEW:** 29 still stretches of 1.5–2.5 s (the new system's threshold is 1.5 s; GS 6/6 was produced under the old 2.5 s check). See section 8 |
| Real GS film (16:9), `qc_video.py` | PASS on dimensions, duration (13:51), loudness (−14.0), true peak (−1.3), decode, frame 1. REVIEW: unmarked holds and low sharpness on flat maps (a known false positive) |
| Real GS 6/6 post copy, `check_copy.py` | Limits PASS. **FAIL:** no "Platform limits re-checked YYYY-MM-DD" line (a new PUB-02 requirement); REVIEW: brand hashtag missing on the YouTube descriptions |
| Merge and rollback rehearsal (in git objects, no checkout) | Merging gives `main` the exact `pro-system` tree. Reverting that merge with `-m 1` gives back `main`'s exact tree (`0e66f57`). GS 6/6 files: 61 before and 61 after |

## 5. Latest-approved-decision check
- **Updated to match the user's latest decision:** the Nov 11 GS 6/6 composition instruction conflicted with two active rules.
  - **LAY-01 → v2:** "use the whole frame as the storytelling canvas", with no fixed working area and varied compositions.
  - **LAY-02 → v3:** captions may sit over moving visuals with an outline, a shadow or a subtle local gradient; they must never be unreadable and must never cover essential information. This replaces "content stays above ~1360" and "captions never sit on a picture".
  - The old versions are in `history.md` as SUPERSEDED, with the user's words.
  - Two references were updated: the director checklist and the editor checklist.
  - The old wording was added to `retired_phrases.txt` so it can't return.
- **Scope:** recorded as channel-wide because the instruction is worded generally. If the user meant Golden Sparrow only, it moves to a GS rule instead.
- **No other conflicts found** among the 123 rules. The four sounds are no longer described as "not cleared" anywhere outside the record files.

## 6. Sound catalog status
| Entry | File | Status now | Licence field | Third-party rights |
|---|---|---|---|---|
| `amb_fire` | `amb_fire.mp3` | APPROVED BY OWNER, SOURCE NOT RECORDED | UNKNOWN (unchanged) | UNVERIFIED |
| `amb_crowd` | `amb_crowd.mp3` | APPROVED BY OWNER, SOURCE NOT RECORDED | UNKNOWN (unchanged) | UNVERIFIED |
| `amb_drums` (festival drums) | `amb_drums.mp3` | APPROVED BY OWNER, SOURCE NOT RECORDED | UNKNOWN (unchanged) | UNVERIFIED |
| `sfx_cannon_distant` | `cannon_distant.wav` | APPROVED BY OWNER, PROVENANCE UNVERIFIED | "CC0 (as listed by Freesound)" (unchanged; CC0 needs no credit) | UNVERIFIED: not yet matched to Freesound 675613; the Freesound page could not be fetched on Nov 11 |

- Each entry records the owner's approval: the date (2026-11-10), "by Sandeep", the user's words and the scope.
- No source or licence was invented.
- QC treats these sounds as usable but always reports them as REVIEW, so a person sees the unverified provenance every time.
- `sfx_war_drums` (Pixabay 463214) is a different, verified file and is unchanged.

## 7. Languages, platforms and formats
The system covers:
- English and Telugu: BR-06, ED-04, the separate Telugu layout checks.
- YouTube and Instagram: FMT-09, PUB, PLT; `check_exports` compares the platform versions.
- Shorts and long films: FMT-01–FMT-11, DIR-12; `qc_video` handles 9:16 and 16:9.

This was confirmed on real files: the GS 6/6 Shorts (4 versions) and the Season 1 film (16:9).

## 8. Unresolved issues and risks (none blocks the merge)
1. **Freeze threshold:** the new `qc_video` flags still stretches over 1.5 s (the old check used 2.5 s). Future scene sheets need a HOLD list for intentional holds, or the scenes need more motion. Expect REVIEW items until then.
2. **Post-copy checks:** `check_copy` now requires a dated "Platform limits re-checked" line and prefers the brand hashtag on YouTube. GS 6/6's copy predates this; it can be updated before upload if wanted.
3. **Cannon provenance:** still not matched to the Freesound original (needs a Freesound login). Owner-approved and in use; flagged REVIEW.
4. **Account skills:** the saved `why-channel-video` and `why-channel-post-copy` skills are older. The repo files win (master playbook precedence). They are to be reviewed after the merge, with separate approval.
5. **`pre-pro-system` tag:** exists locally only (pushing tags was refused on Nov 10). Use commit `fb25e59` if it's ever needed.
6. **New `main` commits:** any new commit on `main` before the merge means repeating step 2 and the tests.

## 9. Proposed merge procedure (after the user's explicit approval only)
1. Confirm `main` is still `20fe402` (`git ls-remote origin refs/heads/main`). If it moved, merge `main` into `pro-system` again and re-run the tests.
2. On GitHub, PR #2 → **"Create a merge commit"** (not squash, not rebase).
3. Record the merge SHA in this report and in `2026-11-10_merge_and_rollback.md` (`MERGE_SHA`).
4. After the merge: run `bash setup.sh`, `check_rules.py` and the self-tests on `main`.
5. Afterwards, with separate approval: review the saved account skills.

## 10. Rollback
- `git revert -m 1 <MERGE_SHA>`, then push to `main`.
  - This removes only what PR #2 brought in. All Golden Sparrow commits are kept, including any made after the merge.
  - Rehearsed today: after the revert, the tree equals `main` at `20fe402` exactly.
- **Never** reset `main` to `fb25e59` or `20fe402`; that would discard later work.
- A rollback can't affect any video build: PR #2 changes only Markdown, `pipeline/qc/`, `sfx/catalog.json` metadata and one `setup.sh` line.
