# Why? Remotion effects

30 reusable animation clips for Shorts and long videos. Each one renders to a **silent MP4** that the existing Python/ffmpeg editors use like any other clip. This collection is separate from the nine Python styles in `pipeline/styles/`, which are unchanged.

Previews of every final frame: `previews/`. Briefs: `prompts/ultra-skills-inspired/`. Status and suggested sounds for each effect: `manifest.json`.

## Cost
Everything runs locally for free: Remotion, three.js and the Chromium already on the machine. No generation services or paid assets are used.

Remotion's Free License covers individuals and for-profit organizations with up to 3 employees, including commercial videos. If the channel becomes a company with more than 3 employees, a Remotion Company License is needed.

## Set up and render
`bash setup.sh` at the repo root installs the dependencies. To do it by hand: `npm ci` in this folder.

```bash
node cli/render.mjs stat-chart --aspect 9x16 --lang te --out clip.mp4      # sample props
node cli/render.mjs headline --aspect 16x9 --props spec.json --out clip.mp4
node cli/render.mjs map-route --aspect 9x16 --lang en --sheet sheet.jpg    # four-frame contact sheet
node cli/render.mjs all --sheet-dir renders/sheets --aspect 16x9 --lang en # sheets for every effect
node cli/render.mjs videos --video-dir renders/videos --aspect 9x16 --lang te
npm run validate      # checks every sample, and that unsourced facts are refused
npm run typecheck
npm run studio        # live preview
```

From a Python render script:
```python
import sys; sys.path.insert(0, 'pipeline/remotion_effects')
from remotion_clip import render_clip, iter_frames, cue
mp4 = render_clip('stat-chart', props, aspect='9x16', lang='te', out='scene12.mp4')
```

## Props every effect accepts
| Prop | Meaning |
|---|---|
| `language` | `en` or `te`. Pass Telugu strings for every visible field |
| `captionSafe` | Default `true`: keeps text in the channel safe zones, the same numbers as `pipeline/styles/core.py` |
| `brandPalette` | Optional `ink`, `cream`, `amber` overrides |
| `durationFrames` | Longer clip. The extra time becomes a hold on the final frame |
| `cues` | Voice sync, for example `{"draw": 42}`. Later beats keep their spacing after the cued beat. Use `cue(seconds)` from word timestamps |
| `demo` | `true` prints DEMO / ILLUSTRATION on screen and waives the source check |

Beat names are in each effect's `beats` object. Effect-specific fields are in its `schema`, and `samples/<slug>.en.json` and `.te.json` are working examples.

## Rules built in
- **Sources:** with `demo` off, a render fails if any metric, place or claim has no source. Strings such as "DEMO" or "sample" do not count as sources.
- **Sample data is not research.** Everything in `samples/` is a demo. Verify real figures before use.
- **Stat Chart honesty:** the big number shows only supplied readings, and a change of scale is labelled on screen.
- **Maps:** Globe Arcs draws land as one mass with no borders. Map Route is a schematic city, not real geography.
- **Terminal Bloom** refuses commands containing secrets or repository URLs.
- All motion comes from the frame number and seeded randomness, so re-renders match.

## Using a clip in a video
- Name the effect in the scene sheet, like any other style, and get it agreed before rendering.
- Add sound in the Python mix using real recordings from `sfx/`. `manifest.json` suggests catalog sounds for each effect.
- Captions, series tags and CTA cards go on top in the Python pipeline.
- Several effects open on an empty or nearly empty frame, because they draw themselves in. If one opens a video, cut in a few frames late so frame 1 is meaningful and passes the brightness check.
- Clips are 2 to 3 seconds by default. Stretch with `cues` and `durationFrames` to match the line.

## Limits
- Map Route has no real-geography mode. For real journeys, use Globe Arcs or the existing map pipeline.
- Teardown, Hologram and Turntable use built-in models. Importing other 3D objects is not supported yet.
- Headline can show a real screenshot through `photo`. Otherwise it prints an ILLUSTRATIVE MOCK stamp.
- 3D effects use software WebGL here, at roughly 0.4 s per frame on 2 CPUs.
