# Why? animation style library

Nine reusable animation styles, drawn entirely in code. No footage, image credits or ElevenLabs credits needed, and safe for monetization because every frame is generated here.

The style names come from a reel by matt_penny_applied_ai. The code is our own build of those styles, in the channel's colours and safe areas. His repos and prompts were not used (they are only sent to people who comment on the reel).

Previews: `previews/sheet_9x16.jpg`, `previews/sheet_16x9.jpg`.

## Pick a style
| Style (`name`) | Use it for | Main spec fields | Timing fields (sync to voice) | Sounds (one job each, `sfx/`) |
|---|---|---|---|---|
| Isometric (`isometric`) | Supply chains, how a system works | `title`, `sub`, `theme`, `items[label,h,w,hero]` | `start`, `stagger` | card lands as each block rises |
| Paper-Cut (`paper_cut`) | History, folk stories, festivals | `title`, `sub`, `palette`, `sun` | `tags[t,text]` | paper slide, page turn |
| 3D Data Chart (`chart_3d`) | Comparisons, prices over time, rankings | `title`, `bars[label,value,hero]`, `unit`, `decimals`, `ref`, `source` | `start`, `stagger` | ticker while bars grow, knock on the hero |
| Synthwave (`synthwave`) | Tech, 80s/90s history, "the future" (short bursts) | `events[big,small]` | `events[t]` | deep woosh on each event |
| 3D Explainer (`explainer_3d`) | What is inside something, layers | `title`, `layers[label,sub,col,r]` | `split`, `beat` | sub knock as layers part |
| Maths Diagram (`maths_diagram`) | Growth, percentages, step-by-step sums | `title`, `xlabel`, `f`, `x`, `y`, `xticks`, `yticks`, `marks[x,label]`, `steps` | `trace` | marker on the curve, typing on the working |
| Cartoon Explainer (`cartoon_explainer`) | Anna and Chelli question-and-answer beats | `topic`, `lines[who,text]`, `env` | `lines[t0,t1]` | follow the voice, light room tone only |
| Domino Reveal (`domino_reveal`) | Chain reactions, the payoff of a story | `steps`, `reveal`, `reveal_sub`, `per_step` | `hits` (one per step + reveal), `speed` | tick per domino, impact on the reveal |
| Glow Atom (`glow_atom`) | Science, anything tiny, "this one piece matters" | `name`, `sub`, `shells`, `nucleus`, `hi`, `callout`, `callout_sub`, `footer` | `park`, `focus` | riser into the focus, knock on the callout |

Each style has working example values in its `DEFAULT`. Those examples are demos: research and verify every real number before it goes in a video.

## Use it
```bash
pip install --break-system-packages pycairo     # setup.sh already does this
python3 pipeline/styles/render_style.py glow_atom --aspect 9x16 --t 5 --out still.png
python3 pipeline/styles/render_style.py domino_reveal --spec spec.json --aspect 16x9 --video clip.mp4 --dur 9
python3 pipeline/styles/render_style.py all --sheet sheet.jpg --aspect 9x16
```
Inside a video's scene script:
```python
import sys; sys.path.insert(0, 'pipeline/styles')
from render_style import frame
from cartoon_explainer import voice_envelope
img = frame('maths_diagram', seconds_since_scene_start, '9x16', spec)   # returns a PIL image
spec = {'env': {'ANNA': voice_envelope('anna.wav'), 'CHELLI': voice_envelope('chelli.wav')}, 'lines': [...]}
```
`frame()` returns a full-screen RGB image, so captions, the series tag and CTA cards layer on top as usual.

## Rules
- Telugu works in every text field. Pass Telugu strings for the Telugu version; graphics must never stay in English there.
- Sync with voice: set the timing fields from word timestamps, the same way as other cue-driven scenes.
- Cartoon Explainer: always pass `env` from the real voice for delivery. Without it the mouth uses a preview rhythm only.
- Domino Reveal, 3D Data Chart and Maths Diagram begin nearly empty. If one opens a video, start rendering from a later `v` so frame 1 is meaningful and passes the brightness check.
- Maths Diagram and Domino Reveal hold still once finished, so cut to the next visual as soon as the animation lands.
- Switch style every 20–30 s at most (retention rule). Use Synthwave sparingly; it is the loudest look and magenta sits outside the brand.
- Check a stills sheet before any full render. Do not render a full video only to test a style.
- Safe areas and the 34 px label minimum live in `core.Stage`. Add new styles through `core.py` and list them in `render_style.STYLES`.
