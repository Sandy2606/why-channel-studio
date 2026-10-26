# Why? Channel Studio

Production kit for **Why?** (YouTube @WhyEveryQuestionHasaStory · Instagram @whyeveryquestion) and **Why? Telugu**.
Claude clones this repo at the start of every video session, runs `bash setup.sh`, and pushes improvements back.

## Layout
| Folder | What |
|---|---|
| `playbook/` | The production playbook (same as the `why-channel-video` skill): quality system, pacing model, sound design, script format, KEEP/DROP log |
| `pipeline/long/` | 16:9 long-video renderer: `render_long.py`, 2D animations `anim_long.py`, captions/anchors `caps_long.py`, Pace Model `pacing.py` + `make_voice_v2.py`, voice chain `proasm.py`, synth fallback SFX `sfx.py` |
| `pipeline/shorts/` | 9:16 Shorts renderer (Sunday Short version) |
| `pipeline/lib/` | Shared drawing helpers (`epic.py`, `modern.py`) + borderless world map data |
| `sfx/` | **Real** sound library + `catalog.json` (role, hit point). Add new sounds by drag & drop on GitHub |
| `music/` | Approved calm music beds |
| `brand/fonts/` | Archivo Black, Space Mono, Noto Sans Telugu |
| `videos/<date>_<slug>/` | Per-video files: cues, phrase anchors, take lists, script, post copy, thumbnails |

## Brand
Black `#0A0A0A` · cream `#F4F1EA` · amber `#FFB224` · Archivo Black + Space Mono · Telugu: Noto Sans Telugu Black.

## Adding sounds
Drop real recordings (Pixabay / YouTube Audio Library; never AI-generated) into `sfx/` with a descriptive name.
Wanted next: keyboard typing, key press, mouse click, camera shutter, polaroid, rubber stamp, marker scribble, highlighter, thumbtack, map unfold, sub drop.
