# pipeline/qc: reusable QC checks

Every checker works on any Why? project: 9:16 Shorts (1080×1920) and 16:9 films (1920×1080), EN and TE, YT and IG. None has a hardcoded project path, filename or runtime. Each writes `<tool>.json` and `<tool>.md` to `--out` and prints the table.

**Statuses:** PASS · FAIL · REVIEW (a person must look) · NOT PERFORMED (could not be checked automatically).
**Overall:** FAIL if anything failed; INCOMPLETE if anything was not performed; PASS WITH REVIEW; PASS only if every check was performed and passed. A partial check can never produce a complete pass.
**Exit codes:** 0 pass, 1 fail, 2 incomplete.

| Script | Reads | Can verify | Cannot verify (stays human, or NOT PERFORMED) |
|---|---|---|---|
| `qc_video.py VIDEO` | The rendered file (ffprobe, one ffmpeg decode pass, sampled frames) | Dimensions per format; Shorts under 3:00; black frames; freezes over 1.5 s (minus HOLDs from `--holds`); integrated loudness and true peak; audio dropouts (silence over 2 s); decode errors; frame-1 brightness; loop seam (`--loop`); per-scene sharpness (`--scenes`, else fixed windows). Writes the contact sheet, first 3 s, corner and caption crops, and the phone-size sheet | Whether a freeze is intentional, when no HOLD list is given (reported as REVIEW). Sharpness on flat vector graphics (low scores are a known false positive; image scale is checked by `check_assets`). The whole visual checklist (QC-01) is always NOT PERFORMED: it needs a person, using the sheets |
| `qc_layout.py` | Boxes registered through `pipeline/style_v2/layout.py` `reg()`, from a `--dump` JSON or by calling a project's `render(t)` (`--render-script`) | Text inside its box with ≥ 8 px padding; ≥ 40 px from the frame edges (full-bleed images exempt); overlaps between captions, credits, cards, labels and badges; captions on pictures; corner badges on one centre line. Works at 1080×1920 or 1920×1080 | Anything not registered: Remotion clips, text baked into images, unregistered drawings. Declared `not_covered` intervals are NOT PERFORMED; frames with no registered text are REVIEW. Fonts and colours are NOT PERFORMED, because `reg()` records neither |
| `check_exports.py DIR --base NAME` | Every expected file (`{base}_{lang}_{platform}.mp4`) | Each platform version is present; dimensions; h264/aac; fps; Shorts under 3:00; the same body across YT and IG (duration and mid-frame) | Platform-specific endings (they are meant to differ) |
| `check_copy.py COPY.md` | The post-copy Markdown (`## ENGLISH · YouTube …`, with `**Title**`, `**Description**`, `**Tags**` and `**Caption**` blocks) | Title ≤ 100; tags ≤ 500 (a ceiling, not a target); IG caption ≤ 2,200; ≤ 5 IG hashtags; SOURCES and CREDITS present; brand hashtag (REVIEW if absent); disclosure decision recorded; limits verification date recorded | Accuracy, tone, readability, Telugu naturalness. Whether the disclosure decision is right |
| `check_assets.py REGISTER.md` | The asset register table (`templates/asset_register.md`) | Source and licence filled; scale ≤ 1.0 from native vs on-screen size; AI and composite rows labelled; named files exist (`--root`); sounds in `sfx/catalog.json` | Whether a licence or credit is actually correct. Videos without a register are NOT PERFORMED |
| `check_sources.py SCRIPT.md --brief BRIEF.md` | `[C#]` markers in the script and the brief's source register (ID column) | Every marked claim has an entry with a source and a check date | Whether the source supports the claim; claims that are not marked. Scripts without markers are NOT PERFORMED |
| `check_rules.py` | The playbook Markdown | One owner per rule ID; index ranges complete; citations resolve; no retired wording (`retired_phrases.txt`, with benign hits in `retired_allow.txt`); `history.md` is never loaded; the migration record is complete | Whether a rule is wise. That is the user's approval |

## Typical use (per video)
```
python3 pipeline/qc/check_exports.py out --base GoldenSparrow5
for f in out/*.mp4; do python3 pipeline/qc/qc_video.py "$f" --loop --holds holds.json --scenes scenes.json; done
python3 pipeline/qc/qc_layout.py --render-script pipeline/render.py --start 0 --end 110 --step 0.25 --out qc/layout_EN
python3 pipeline/qc/check_copy.py GS5_Short_Post_Copy.md
python3 pipeline/qc/check_assets.py asset_register.md --root .
python3 pipeline/qc/check_sources.py script_v3.md --brief production_brief.md
```
Run `qc_layout.py` on previews or stills before the full render (WF-02): that is where it saves the most rework.

Self-test: `python3 pipeline/qc/tests/run_tests.py [--report pipeline/qc/tests/LAST_RUN.md]` (32 synthetic good and deliberately failing fixtures; temporary files are deleted afterwards).
