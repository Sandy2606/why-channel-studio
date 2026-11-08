# 04 — Globe Arcs

**Group:** 3D Scenes  
**Recommended stack:** Three.js + d3-geo within Remotion + TypeScript  
**Default video:** 1080×1920 · 30 fps · 60 frames (2s)  
**Also required:** Responsive 1920×1080 landscape composition

## Paste this entire section into Claude Code

Create a reusable production animation named `globe-arcs` for my Why? English/Telugu YouTube studio. The effect must be independently rendered and composable into a longer documentary or Short. Do not overwrite existing styles.

**Inputs the scene must accept:** [origin coordinate], [destination coordinates], [names], [metric], [data source].

**Visual direction:** Place a clean low-detail globe in a dark room. A source marker glows; curved paths appear progressively to distant points. Each endpoint receives a small halo on arrival, while a counter reports the number of connections.

**Frame choreography:** 0-10: locate the source on a gently turning Earth; 11-39: launch paths with staggered starts and reveal them tip-first; 40-52: land destination nodes and synchronize the connection count; 53-59: drift the camera closer to the network.

**Technical construction:** Build routes with great-circle interpolation on a sphere, add a small altitude arc, and hide connections behind the planet by depth testing. Use supplied or verified geography. Do not draw modern political borders in the Why? videos; use one landmass-style texture.

**Example creative brief:** Sample idea: illustrate documented maritime connections or a modern global supply network; avoid unsupported historical trade routes.

**Output requirements:** A deterministic TypeScript component, schema/default spec, short demo clip, vertical/landscape variants, preview stills at at least four time points, and a README that shows render commands. Include optional `language`, `captionSafe`, `brandPalette` and `durationFrames` options. If dependencies are unavailable, explain the exact dependency blocker rather than claiming to have rendered.

### Global execution contract

- Build this as a **reusable effect**, not just a one-off demo. Start by inspecting this repository's latest `playbook/why-channel-video-SKILL.md`, `pipeline/styles/README.md`, and actual render entry points. Preserve the nine existing Python effects; place Remotion components in `pipeline/remotion_effects/` (or an equivalent isolated folder already chosen by the repo maintainer) with a thin MP4 export interface. Do not assume the Python renderer directly imports React code.
- Use **Remotion with TypeScript**. Control all motion from `useCurrentFrame()`, `interpolate()` and `spring()` or deterministic functions of the frame. Seed every procedural layout; do not use `Math.random()`, `Date.now()`, real-time timers or browser transition timing for the rendered motion.
- The default export is a silent **1080×1920, 30 fps** vertical effect with the scene-specific frame length. Also support **1920×1080** by recomposing camera, sizes and captions, not by letterboxing or stretching. For a longer scene, add hold and voice-timing parameters instead of slowing everything arbitrarily.
- Channel default palette: black `#0A0A0A`, cream `#F4F1EA`, amber `#FFB224`; allow local accent overrides. Prefer `Archivo Black` and `Space Mono` from `brand/fonts/`, and `Noto Sans Telugu` for Telugu. Check real glyph metrics. No third-party paid services, paid asset models or watermarked stock.
- Only use claims, figures, dates and places from verified scene data; if mock data is used, label it **DEMO / ILLUSTRATION**. Preserve sources and any permitted asset attribution. Do not fabricate numbers for a documentary.
- In vertical exports, keep essential text inside the existing channel-safe region and leave the bottom controls area clear. Protect YouTube 16:9 caption space too. Never replace real spoken subtitles with decorative text. Avoid rapid flashes, strobing and busy screen shake.
- Use existing **real recorded** SFX from `sfx/` if an effect needs sound in the final film; do not synthesize cartoon noises. The individual animation MP4 can remain silent for editing.
- Include typed input schema/default example, reusable effect component, sample JSON data, a CLI command to render an MP4, and a contact sheet covering opening, midpoint and final frames. Validate the render, inspect label legibility, and document any assumptions. Do not say a render passed unless it was actually produced and checked.

## Attribution / boundaries

This is an independently authored brief for the **Globe Arcs** effect concept. Inspiration index: [Ultra Skills' public 30-effects article](https://www.ultra-skills.com/resources/claude-code-animation-prompts-six-effects). Do not copy its wording into this repository or imply that the original creators approved this pack.
