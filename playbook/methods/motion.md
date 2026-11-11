# Methods: motion (long-video graphics and pipelines)

Method notes, not rules: they record how we currently do things and are updated by measuring and testing. Rules live in the owner files (see the master playbook). Copied from the pre-reorganisation playbook (tag `pre-pro-system`), with the original line numbers in brackets; superseded parts are left out and recorded in `history.md`.

## Long-video 2D explainers (anim_long.py) [PB:93–104]
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

## Story-cinema build notes [PB:235–239]
- **Characters = the long-video Anna & Chelli** (dl/chars2.py: anna(), chelli()), recast per story (e.g. Raju & Meera); side characters reuse anna() with recoloured clothes plus extras (Gurpreet: turban + beard). Don't use the old flat stick figures (user: 'feels like a drum').
- **Cartoons talk.** Mouths move with their own lines; drive them from the voice envelope (RMS per frame, gated by who owns the line). The narrator's third-person lines (hook and loop) don't move a character's mouth. Characters blink. In map or city shots, the asker appears as a round bust in the corner with a speech bubble that shows their line, and captions hide while the bubble is up.
- **Watching a film, not slides.** Use one continuous drawn world with a camera (map → city → home → street; log-zoom moves, no hard cuts). Use dark cinematic grades, vignette and bokeh dust for "invisible" scales. Keep it simple and clean: flat shapes, at most two labels on screen.
- **Body explanations use REAL-looking imagery, not cartoons** (user Nov 4: 'realistic so viewers are amazed'): stock 3D renders/photos (Unsplash MCP works; Pixabay/Pexels clips via user) with Ken Burns, dark grade and my overlays (particles, inflammation glow, labels). Size comparisons start at human scale (one hair on a table, actual size) then go under the microscope, drawn to TRUE ratio (hair 70 µm = 280 px → PM2.5 = 10 px).
- **Body explanations go inside the body.** Use a human example and follow the substance in: start with a macro lens (the particle next to a hair), then an x-ray band that sweeps through the clothes (torso first; keep the face visible), breathing in, particles travelling the airway into the lungs, inflamed red spots, a cough. Cut deeper (air sacs, immune cells, a capillary with blood cells), then pull back to the whole body to show the route to the heart and brain with HEART ATTACK / STROKE tags. Hold the camera steady during the serious health information. Put a source chip on screen (e.g. US EPA · WHO).

## Pipelines [PB:261, 380]
- Golden Sparrow Shorts reference build: `videos/2026-11-09_short_gs1_golden_sparrow/pipeline` (render.py, cues.py, mix.py, build_voice.py, words.py).
- **2D long-video pipeline (Diwali long, Oct 30):** `videos/2026-11-01_long_diwali_explained/pipeline/`: voice.py (per-line clips → Pace Model gaps: chapter 1.30 s, title 4.4 s, after '?' 0.45, punch 0.50, speaker change 0.28, same 0.20; internal pauses capped 0.40; atempo 1.06 except the Subscribe line), words.py (EN whisper per line + difflib snap; TE spread over voiced runs), clips.py (crop regions auto-found from first/last phrase), base/room/gfx1/gfx2/render.py (scene per script line, anchors by EN word, TE by number match or EN char fraction), mix.py (2 music tracks switching at chapter 4, duck 62%, chapter dips, real SFX by catalog hit points), thumb.py. Room shots: lip-sync from the voice envelope, listener looks at speaker, close-ups alternate with two-shots, REC + timer overlay after "Let me record this". ~0.07 s/frame.
- Static holds: a slow 4–5% push-in on graphic scenes is one way to avoid an unintended freeze (never on raster images beyond native size, → MO-01); the loop hold returns frame 0 to 1.0 so the last frame equals the first. [PB:266]
- Word-cue sequencing: one `seq` renderer per line with cuts on word cues (EN word timestamps; TE phrase + character position) and a cue-miss log. [PB:318]


