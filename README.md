# Why? Channel Studio

Production kit for **Why?** and **Why? Telugu**. Accounts: see `playbook/brand.md` (BR-07).
Claude clones this repo at the start of every video session, runs `bash setup.sh`, and pushes improvements back.

## Layout
| Folder | What |
|---|---|
| `playbook/` | Master playbook (precedence, rule index, workflow), `brand.md`, `platform_rules.md`, `roles/` (11 role guides), `methods/` (technical notes), `templates/`, `history.md` (record only, not instructions), `MIGRATION.md` |
| `plans/` | Series plans (e.g. `golden_sparrow.md`) and topic ideas |
| `pipeline/long/` | 16:9 long-video renderer: `render_long.py`, 2D animations `anim_long.py`, captions/anchors `caps_long.py`, Pace Model `pacing.py` + `make_voice_v2.py`, voice chain `proasm.py`, synth fallback SFX `sfx.py` |
| `pipeline/shorts/` | 9:16 Shorts renderer (Sunday Short version) |
| `pipeline/styles/` | Library of 9 code-drawn animation styles for 9:16 and 16:9 (see its README) |
| `pipeline/remotion_effects/` | 30 Remotion effect clips rendered to silent MP4s (see its README); briefs in `prompts/ultra-skills-inspired/` |
| `pipeline/lib/` | Shared drawing helpers (`epic.py`, `modern.py`) + borderless world map data |
| `sfx/` | **Real** sound library + `catalog.json` (role, hit point). Add new sounds by drag & drop on GitHub |
| `music/` | Approved calm music beds |
| `brand/fonts/` | Archivo Black, Space Mono, Noto Sans Telugu |
| `videos/<date>_<slug>/` | Per-video files: cues, phrase anchors, take lists, script, post copy, thumbnails |

## Brand
See `playbook/brand.md` (BR-01, BR-02).

## Adding sounds
Drop real recordings (Pixabay / YouTube Audio Library; never AI-generated) into `sfx/` with a descriptive name.
The wanted list is in `playbook/roles/sound.md`.
