# pipeline/qc: reusable QC checks

Every checker works on any Why? project: 9:16 Shorts (1080×1920) and 16:9 films (1920×1080), EN and TE, YT and IG. None has a hardcoded project path, filename or runtime. Each writes `<tool>.json` and `<tool>.md` to `--out` and prints the table.

**Statuses:** PASS · FAIL · REVIEW (a person must look) · NOT PERFORMED (could not be checked automatically).
**Overall:** FAIL if anything failed; INCOMPLETE if anything was not performed; PASS WITH REVIEW; PASS only if every check was performed and passed. A partial check can never produce a complete pass.
**Exit codes:** 0 pass, 1 fail, 2 incomplete.

| Script | Reads | Can verify | Cannot verify (stays human, or NOT PERFORMED) |
|---|---|---|---|
| `qc_video.py VIDEO` | The rendered file (ffprobe, one ffmpeg decode pass, sampled frames) | Dimensions per format; Shorts under the limit in `platform_rules.md`; black frames (below 3% brightness, so the ink background is not "black"); freezes over 1.5 s (minus HOLDs from `--holds`); integrated loudness and true peak; audio dropouts (silence over 2 s); decode errors; frame-1 brightness; with `--loop`, the first frame vs the **actual final decoded frame**, plus any hard cut in the last 0.5 s; per-scene sharpness (`--scenes`, else fixed windows). Writes the contact sheet, first 3 s, corner and caption crops, and the phone-size sheet | Whether a freeze is intentional, when no HOLD list is given (reported as REVIEW). Sharpness on flat vector graphics (low scores are a known false positive; image scale is checked by `check_assets`). The whole visual checklist (QC-01) is always NOT PERFORMED: it needs a person, using the sheets |
| `qc_layout.py` | Boxes registered through `pipeline/style_v2/layout.py` `reg()`, from a `--dump` JSON or by calling a project's `render(t)` (`--render-script`) | Text inside its box with ≥ 8 px padding; ≥ 40 px from the frame edges (full-bleed images exempt); overlaps between captions, credits, cards, labels and badges; captions on pictures; corner badges on one centre line. Works at 1080×1920 or 1920×1080 | Anything not registered: Remotion clips, text baked into images, unregistered drawings. Declared `not_covered` intervals are NOT PERFORMED; frames with no registered text are REVIEW. Fonts and colours are NOT PERFORMED, because `reg()` records neither |
| `check_exports.py DIR --base NAME` | Every expected file (`{base}_{lang}_{platform}.mp4`) | Each platform version is present; dimensions; h264/aac; fps; Shorts under the limit; the same body across YT and IG at 8 points (`--points`) plus audio sync in 3 windows (lag ≤ 40 ms, r ≥ 0.9); the last `--ending-seconds` (default 10) are excluded because endings differ by design | Differences between the sampled points; the ending itself |
| `check_copy.py COPY.md` | The post-copy Markdown (`## ENGLISH · YouTube …`, with `**Title**`, `**Description**`, `**Tags**` and `**Caption**` blocks) and the limits block in `platform_rules.md` (no limits are kept in the script) | Title, tag, caption and hashtag limits as currently recorded; SOURCES and CREDITS present; brand hashtag (REVIEW if absent); disclosure decision recorded; a "Platform limits re-checked YYYY-MM-DD" line for this upload (FAIL if missing, REVIEW if older than 14 days); REVIEW when the central limits are older than 30 days or rest only on secondary sources | Accuracy, tone, readability, Telugu naturalness. Whether the disclosure decision is right |
| `check_assets.py REGISTER.md` | The asset register table (`templates/asset_register.md`) and `sfx/catalog.json` | Source and licence filled; scale ≤ 1.0 from native vs on-screen size; AI and composite rows labelled; named files exist (`--root`); sounds resolved by catalog key or catalogued path (nested `amb/` paths too), file present on disk, and not marked `approved_for_new_work: false` (unknown provenance); `--catalog-integrity` checks every entry | Whether a licence or credit is actually correct. Videos without a register are NOT PERFORMED |
| `check_sources.py SCRIPT.md --brief BRIEF.md` | `[C#]` markers in the script and the brief's source register (ID column) | Every marked claim has an entry with a source and a check date | Whether the source supports the claim; claims that are not marked. Scripts without markers are NOT PERFORMED |
| `check_rules.py` | The playbook Markdown | One owner per rule ID; index ranges complete; citations resolve; no retired wording (`retired_phrases.txt`, with benign hits in `retired_allow.txt`); `history.md` is never loaded; the migration record is complete | Whether a rule is wise. That is the user's approval |

## Human review and the final summary
`qc_summary.py QC_DIR --type short|long --signoff qc_signoff.md` combines every tool report with the human sign-off (`playbook/templates/qc_signoff.md`). It first checks that every **required** report exists (Short: `qc_video` for EN_YT, EN_IG, TE_YT and TE_IG; two `qc_layout`; `check_exports`, `check_copy`, `check_assets`, `check_sources`. Film: `qc_video` for EN and TE, plus the same others) and that rows H1–H13 are all present. Anything missing keeps the result INCOMPLETE, and a fully signed form never makes up for missing reports. Another production type needs `--manifest` with a written justification. A row may be N/A only with a reviewer, a date and a reason. An automated NOT PERFORMED item stays NOT PERFORMED unless the matching human row is signed PASS with a reviewer and a date. A row without both does not count. Overall: FAIL, INCOMPLETE, or PASS only when every automated check passed or is covered and every human row is signed. Contact sheets are aids, not inspections.

## Typical use (per video)
```
python3 pipeline/qc/check_exports.py out --base GoldenSparrow5
for f in out/*.mp4; do python3 pipeline/qc/qc_video.py "$f" --loop --holds holds.json --scenes scenes.json; done
python3 pipeline/qc/qc_layout.py --render-script pipeline/render.py --start 0 --end 110 --step 0.25 --out qc/layout_EN
python3 pipeline/qc/check_copy.py GS5_Short_Post_Copy.md
python3 pipeline/qc/check_assets.py asset_register.md --root .
python3 pipeline/qc/check_sources.py script_v3.md --brief production_brief.md
python3 pipeline/qc/qc_summary.py qc --type short --signoff qc_signoff.md --out QC_SUMMARY.md
```
Run `qc_layout.py` on previews or stills before the full render (WF-02): that is where it saves the most rework.

Self-test: `python3 pipeline/qc/tests/run_tests.py [--report pipeline/qc/tests/LAST_RUN.md]` (32 synthetic good and deliberately failing fixtures; temporary files are deleted afterwards).
