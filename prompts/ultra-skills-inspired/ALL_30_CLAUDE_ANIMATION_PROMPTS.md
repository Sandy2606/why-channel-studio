# 30 Claude Code Animation Effects — Original, Repo-Ready Prompts

**Purpose:** A self-contained collection of newly written Claude Code prompts, inspired by the 30 *effect ideas* presented on [Ultra Skills](https://www.ultra-skills.com/resources/claude-code-animation-prompts-six-effects). This is **not** a verbatim copy or a purported official copy of the website's prompts. The text, implementation instructions and channel examples below are original.

**Target repository:** [https://github.com/Sandy2606/why-channel-studio](https://github.com/Sandy2606/why-channel-studio) — Why? and Why? Telugu. Reviewed its existing `playbook/why-channel-video-SKILL.md`, `README.md`, and `pipeline/styles/README.md` on 2026-11-08. This pack should be added **alongside** its nine existing animation styles.

**Suggested file layout**

```text
pipeline/remotion_effects/
  src/effects/             # new TS/TSX effect implementations
  examples/                # JSON specs, one per effect
  renders/                 # ignored MP4 and preview contact sheets
  README.md                # CLI, dependencies, usage and integration
prompts/ultra-skills-inspired/
  README.md
  effects/01-map-route.md ... 30-terminal-bloom.md
```

**Source groupings:** 14 three-dimensional scenes, seven ink/paper effects, three data/counting effects, six UI/typography effects. Source demonstrations generally use 60 or 90 frames at 30 fps. No external source text is reproduced here.

## Choose an effect

| # | Group | Prompt | Duration | Implementation |
|---:|---|---|---:|---|
| 01 | 3D Scenes | [Map Route](effects/01-map-route.md) | 3s | Three.js + React Three Fiber |
| 02 | 3D Scenes | [Teardown](effects/02-teardown.md) | 3s | Three.js + React Three Fiber |
| 03 | 3D Scenes | [Git City](effects/03-git-city.md) | 3s | Three.js instanced meshes |
| 04 | 3D Scenes | [Globe Arcs](effects/04-globe-arcs.md) | 2s | Three.js + d3-geo |
| 05 | 3D Scenes | [Hologram](effects/05-hologram.md) | 2s | React Three Fiber + Three.js shaders |
| 06 | 3D Scenes | [Deep Time](effects/06-deep-time.md) | 2s | Three.js shaders + React Three Fiber |
| 07 | 3D Scenes | [Contour Map](effects/07-contour-map.md) | 2s | Three.js + procedural height field |
| 08 | 3D Scenes | [Neon Silhouette](effects/08-neon-silhouette.md) | 2s | Three.js foreground + SVG/CSS background |
| 09 | 3D Scenes | [Laptop Reveal](effects/09-laptop-reveal.md) | 2s | Three.js + React Three Fiber |
| 10 | 3D Scenes | [Isometric Flow](effects/10-isometric-flow.md) | 2s | Three.js orthographic camera |
| 11 | 3D Scenes | [Turntable](effects/11-turntable.md) | 2s | Three.js + physically based materials |
| 12 | 3D Scenes | [Money Stack](effects/12-money-stack.md) | 2s | Three.js + React Three Fiber |
| 13 | 3D Scenes | [Receipt](effects/13-receipt.md) | 2s | Three.js + texture-generated typography |
| 14 | 3D Scenes | [Iceberg](effects/14-iceberg.md) | 2s | Three.js + volumetric-looking layers |
| 15 | Ink & Paper | [Headline](effects/15-headline.md) | 3s | Remotion DOM + CSS 3D |
| 16 | Ink & Paper | [Swiss Grid](effects/16-swiss-grid.md) | 2s | SVG + CSS |
| 17 | Ink & Paper | [Blueprint Draw](effects/17-blueprint-draw.md) | 2s | SVG path animation |
| 18 | Ink & Paper | [Paper Desk](effects/18-paper-desk.md) | 2s | SVG + CSS + optional handdrawn stroke package |
| 19 | Ink & Paper | [Ink Doodle](effects/19-ink-doodle.md) | 2s | SVG + RoughJS or p5 brush |
| 20 | Ink & Paper | [Ink Wash](effects/20-ink-wash.md) | 2s | SVG filter masks + procedural strokes |
| 21 | Ink & Paper | [Creator Life, Drawn Badly](effects/21-creator-life-doodle.md) | 2s | RoughJS + deterministic 2D motion |
| 22 | Data & Counters | [Stat Chart](effects/22-stat-chart.md) | 3s | SVG + @remotion/paths |
| 23 | Data & Counters | [Agent Swarm](effects/23-agent-swarm.md) | 2s | SVG + CSS |
| 24 | Data & Counters | [Day Counter](effects/24-day-counter.md) | 2s | CSS 3D + SVG |
| 25 | UI & Type | [Split-Flap](effects/25-split-flap.md) | 3s | CSS 3D |
| 26 | UI & Type | [Before & After](effects/26-before-after.md) | 2s | CSS clipped layers + SVG |
| 27 | UI & Type | [Lock-Screen Notifications](effects/27-lock-screen-notifications.md) | 2s | SVG + CSS |
| 28 | UI & Type | [Type Slam](effects/28-type-slam.md) | 2s | CSS + SVG typographic transforms |
| 29 | UI & Type | [Particle Word](effects/29-particle-word.md) | 2s | Three.js Points or 2D Canvas |
| 30 | UI & Type | [Terminal Bloom](effects/30-terminal-bloom.md) | 2s | DOM + CSS 3D |

## Full copy-paste prompts

Each effect below is standalone. You can paste one of them into Claude Code or upload this complete file.

---

# 01 — Map Route

**Group:** 3D Scenes  
**Recommended stack:** Three.js + React Three Fiber within Remotion + TypeScript  
**Default video:** 1080×1920 · 30 fps · 90 frames (3s)  
**Also required:** Responsive 1920×1080 landscape composition

## Paste this entire section into Claude Code

Create a reusable production animation named `map-route` for my Why? English/Telugu YouTube studio. The effect must be independently rendered and composable into a longer documentary or Short. Do not overwrite existing styles.

**Inputs the scene must accept:** [origin], [destination], [verified route points or illustrative demo], [distance], [travel label].

**Visual direction:** Build a miniature city out of simple blocks, street ribbons, trees and a curved water feature. Use an overhead-to-three-quarter camera move that helps the viewer understand the trip. A bright amber path follows the roads rather than flying through buildings.

**Frame choreography:** 0-14: establish the origin and reveal city depth; 15-50: animate a continuous route stroke with a luminous moving tip; 51-73: bring the destination into focus as a location marker descends and settles; 74-89: widen the camera to include both endpoints and display a small distance label.

**Technical construction:** Construct streets and route as separate scene geometry. Drive path reveal with shader draw range or tube segment progress; pin position must be derived from route end. Keep projected label coordinates bound to the camera. Use geographic verification for real-world routes; otherwise mark DEMO / schematic.

**Example creative brief:** Sample idea: show a schematic textile journey from a coastal weaving town to a port, without implying an exact historical street route.

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

This is an independently authored brief for the **Map Route** effect concept. Inspiration index: [Ultra Skills' public 30-effects article](https://www.ultra-skills.com/resources/claude-code-animation-prompts-six-effects). Do not copy its wording into this repository or imply that the original creators approved this pack.


---

# 02 — Teardown

**Group:** 3D Scenes  
**Recommended stack:** Three.js + React Three Fiber within Remotion + TypeScript  
**Default video:** 1080×1920 · 30 fps · 90 frames (3s)  
**Also required:** Responsive 1920×1080 landscape composition

## Paste this entire section into Claude Code

Create a reusable production animation named `teardown` for my Why? English/Telugu YouTube studio. The effect must be independently rendered and composable into a longer documentary or Short. Do not overwrite existing styles.

**Inputs the scene must accept:** [object], [ordered parts and labels], [purpose].

**Visual direction:** Show a highly readable object in a dark studio. After the silhouette is clear, its separate components drift apart along one stable axis; thin callout stems connect the individual components to labels.

**Frame choreography:** 0-18: build anticipation with a sparse materialization of the intact object; 19-32: complete assembly and let the object rotate slightly; 33-66: separate components in a deliberate stagger; 67-89: connect part callouts and hold a clean exploded view.

**Technical construction:** Make each component a distinct reusable mesh/group with its own transform and pivot. Attach annotation anchors to object-local positions and project them every frame. Ensure depth ordering avoids intersecting layers. If the subject needs engineering fidelity, require a real reference and label unverified anatomy as schematic.

**Example creative brief:** Sample idea: reveal the layers of a printing press or a clock mechanism in an invention explainer.

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

This is an independently authored brief for the **Teardown** effect concept. Inspiration index: [Ultra Skills' public 30-effects article](https://www.ultra-skills.com/resources/claude-code-animation-prompts-six-effects). Do not copy its wording into this repository or imply that the original creators approved this pack.


---

# 03 — Git City

**Group:** 3D Scenes  
**Recommended stack:** Three.js instanced meshes within Remotion + TypeScript  
**Default video:** 1080×1920 · 30 fps · 90 frames (3s)  
**Also required:** Responsive 1920×1080 landscape composition

## Paste this entire section into Claude Code

Create a reusable production animation named `git-city` for my Why? English/Telugu YouTube studio. The effect must be independently rendered and composable into a longer documentary or Short. Do not overwrite existing styles.

**Inputs the scene must accept:** [daily values data OR clearly labelled sample data], [metric and unit], [date range].

**Visual direction:** Start with a compact rectangular heatmap on a charcoal surface. Squares rise into towers of differing heights, transforming the flat matrix into a lit architectural skyline. The height and lighting encode the data rather than a random decorative pattern.

**Frame choreography:** 0-15: show a readable data grid; 16-38: a diagonal wave raises each cell into a prism based on value; 39-69: tilt and orbit to show the resulting city; 70-89: highlight peak towers and a compact legend.

**Technical construction:** Use InstancedMesh for performance and seeded placeholder values only when no input data exists. Normalize heights explicitly, support zeros, and label the measurement. Fit every tower within the camera frustum at its maximum height.

**Example creative brief:** Sample idea: build a visual of commits per day, views per month, or ship arrivals from supplied data.

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

This is an independently authored brief for the **Git City** effect concept. Inspiration index: [Ultra Skills' public 30-effects article](https://www.ultra-skills.com/resources/claude-code-animation-prompts-six-effects). Do not copy its wording into this repository or imply that the original creators approved this pack.


---

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


---

# 05 — Hologram

**Group:** 3D Scenes  
**Recommended stack:** React Three Fiber + Three.js shaders within Remotion + TypeScript  
**Default video:** 1080×1920 · 30 fps · 60 frames (2s)  
**Also required:** Responsive 1920×1080 landscape composition

## Paste this entire section into Claude Code

Create a reusable production animation named `hologram` for my Why? English/Telugu YouTube studio. The effect must be independently rendered and composable into a longer documentary or Short. Do not overwrite existing styles.

**Inputs the scene must accept:** [object geometry or approved 3D asset], [two highlighted components], [title].

**Visual direction:** A circular pedestal projects a translucent teal/amber wireframe model upward in a dim environment. A moving scanning plane uncovers its geometry, then two reticles track selected parts while the whole object rotates.

**Frame choreography:** 0-20: illuminate emitter and reveal model from base upward; 21-34: build the edge glow and begin turntable movement; 35-49: animate two target reticles to their anchored parts; 50-59: hold the model while a quiet secondary scan passes.

**Technical construction:** Implement geometry visibility with a clipping plane or shader uniform. Use edge outlines, fresnel-style rim lighting and restrained postprocessing. No browser-timed flicker, no laser flashes, and no geometry appearing before the scanning plane.

**Example creative brief:** Sample idea: explain a satellite instrument or historical engineering concept with clearly marked schematic parts.

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

This is an independently authored brief for the **Hologram** effect concept. Inspiration index: [Ultra Skills' public 30-effects article](https://www.ultra-skills.com/resources/claude-code-animation-prompts-six-effects). Do not copy its wording into this repository or imply that the original creators approved this pack.


---

# 06 — Deep Time

**Group:** 3D Scenes  
**Recommended stack:** Three.js shaders + React Three Fiber within Remotion + TypeScript  
**Default video:** 1080×1920 · 30 fps · 60 frames (2s)  
**Also required:** Responsive 1920×1080 landscape composition

## Paste this entire section into Claude Code

Create a reusable production animation named `deep-time` for my Why? English/Telugu YouTube studio. The effect must be independently rendered and composable into a longer documentary or Short. Do not overwrite existing styles.

**Inputs the scene must accept:** [cosmic event], [time scale], [caption], [scientific uncertainty note].

**Visual direction:** Produce a stylized astronomy diagram: a dark gravitational center surrounded by an orange rotating disc. A small luminous body traces an inward curve, loses a stream of particles and fades into the disc as a time scale changes pace.

**Frame choreography:** 0-16: establish the disk and incoming object; 17-34: tighten orbital motion while the time readout advances; 35-47: slow the motion for the decisive transition and arc the particles around the disk; 48-59: resolve with a stable frame and one explanatory line.

**Technical construction:** Use shader-based glow rather than image overlays; mathematical positions must be functions of frame only. Do not assert that the depiction is a physical simulation. Numeric timeline or sizes require cited data; otherwise add an ILLUSTRATION label.

**Example creative brief:** Sample idea: a visual metaphor for a star approaching a black hole in a science story.

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

This is an independently authored brief for the **Deep Time** effect concept. Inspiration index: [Ultra Skills' public 30-effects article](https://www.ultra-skills.com/resources/claude-code-animation-prompts-six-effects). Do not copy its wording into this repository or imply that the original creators approved this pack.


---

# 07 — Contour Map

**Group:** 3D Scenes  
**Recommended stack:** Three.js + procedural height field within Remotion + TypeScript  
**Default video:** 1080×1920 · 30 fps · 60 frames (2s)  
**Also required:** Responsive 1920×1080 landscape composition

## Paste this entire section into Claude Code

Create a reusable production animation named `contour-map` for my Why? English/Telugu YouTube studio. The effect must be independently rendered and composable into a longer documentary or Short. Do not overwrite existing styles.

**Inputs the scene must accept:** [terrain name], [elevation ranges], [label], [source or schematic marker].

**Visual direction:** Begin with a warm flat cartographic sheet carrying concentric elevation curves. The paper develops relief under those curves until a mountainous formation emerges, and the camera lowers to reveal its slopes.

**Frame choreography:** 0-12: draw isolines on the sheet; 13-37: lift a height field while the contour lines follow the raised surface; 38-52: move the camera from plan view to oblique view; 53-59: reveal a crest label and elevation key.

**Technical construction:** Sample heights from deterministic noise for fictional terrain or use verified topographic data for named mountains. Draw contours by quantizing height levels or marching squares; prevent z-fighting between surface and lines.

**Example creative brief:** Sample idea: explain how terrain height shapes roads, rainfall or historic travel.

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

This is an independently authored brief for the **Contour Map** effect concept. Inspiration index: [Ultra Skills' public 30-effects article](https://www.ultra-skills.com/resources/claude-code-animation-prompts-six-effects). Do not copy its wording into this repository or imply that the original creators approved this pack.


---

# 08 — Neon Silhouette

**Group:** 3D Scenes  
**Recommended stack:** Three.js foreground + SVG/CSS background within Remotion + TypeScript  
**Default video:** 1080×1920 · 30 fps · 60 frames (2s)  
**Also required:** Responsive 1920×1080 landscape composition

## Paste this entire section into Claude Code

Create a reusable production animation named `neon-silhouette` for my Why? English/Telugu YouTube studio. The effect must be independently rendered and composable into a longer documentary or Short. Do not overwrite existing styles.

**Inputs the scene must accept:** [short caption], [time], [character props].

**Visual direction:** Compose a moody desk scene in front of a layered evening skyline. The central person is only a near-black outline; a table lamp illuminates a mechanical clock and scattered tools. Very small movements make the scene feel alive.

**Frame choreography:** 0-14: parallax across three distant building layers; 15-31: illuminate the desk pool and reveal the clock; 32-48: flip several clock cards or numbers with convincing hinge timing; 49-59: settle on the time and caption as the silhouette subtly shifts.

**Technical construction:** Separate background planes for depth without over-modeling. Animate individual clock panels with local pivots. Keep bright neon accents below caption intensity and avoid photorealistic faces or user likeness unless assets are supplied.

**Example creative brief:** Sample idea: a visual transition for an overnight event, deadline or long research session.

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

This is an independently authored brief for the **Neon Silhouette** effect concept. Inspiration index: [Ultra Skills' public 30-effects article](https://www.ultra-skills.com/resources/claude-code-animation-prompts-six-effects). Do not copy its wording into this repository or imply that the original creators approved this pack.


---

# 09 — Laptop Reveal

**Group:** 3D Scenes  
**Recommended stack:** Three.js + React Three Fiber within Remotion + TypeScript  
**Default video:** 1080×1920 · 30 fps · 60 frames (2s)  
**Also required:** Responsive 1920×1080 landscape composition

## Paste this entire section into Claude Code

Create a reusable production animation named `laptop-reveal` for my Why? English/Telugu YouTube studio. The effect must be independently rendered and composable into a longer documentary or Short. Do not overwrite existing styles.

**Inputs the scene must accept:** [product or site title], [headline], [feature tags], [screen mockup].

**Visual direction:** A closed unbranded laptop sits in a bright neutral studio. Its lid opens on a visible hinge; the screen wakes gradually and a branded UI builds inside the display. Small supporting graphics appear beside the device.

**Frame choreography:** 0-16: camera approaches closed device; 17-39: open the screen with an inertial hinge and bring up display light; 40-52: lay out hero text and two interface components on the screen; 53-59: settle into a three-quarter product angle.

**Technical construction:** Model lid and base as separate hinge-linked groups with plausible thickness. The UI should be rendered to a texture or anchored plane aligned to the screen. No use of third-party logos or copyrighted product imagery by default.

**Example creative brief:** Sample idea: show a dashboard or evidence archive created for a Why? research video.

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

This is an independently authored brief for the **Laptop Reveal** effect concept. Inspiration index: [Ultra Skills' public 30-effects article](https://www.ultra-skills.com/resources/claude-code-animation-prompts-six-effects). Do not copy its wording into this repository or imply that the original creators approved this pack.


---

# 10 — Isometric Flow

**Group:** 3D Scenes  
**Recommended stack:** Three.js orthographic camera within Remotion + TypeScript  
**Default video:** 1080×1920 · 30 fps · 60 frames (2s)  
**Also required:** Responsive 1920×1080 landscape composition

## Paste this entire section into Claude Code

Create a reusable production animation named `isometric-flow` for my Why? English/Telugu YouTube studio. The effect must be independently rendered and composable into a longer documentary or Short. Do not overwrite existing styles.

**Inputs the scene must accept:** [stages], [short stage labels], [moving token], [travel direction].

**Visual direction:** Set a small isometric tabletop with several simplified locations connected by a single curving track. A tiny moving vehicle or token travels between the steps and makes each stage come alive as it arrives.

**Frame choreography:** 0-12: drop in the starting structure and stage one; 13-35: send the token along a path while showing stage two; 36-49: reveal stage three and connect the complete sequence; 50-59: pull back to show all locations.

**Technical construction:** Use an orthographic camera, path interpolation by normalized distance, and subtle shadow beneath moving objects. All stage text must be large enough at 9:16. Label each stop only after it becomes visible.

**Example creative brief:** Sample idea: cotton field → spinning → weaving → dyeing → port, as an explicitly simplified journey.

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

This is an independently authored brief for the **Isometric Flow** effect concept. Inspiration index: [Ultra Skills' public 30-effects article](https://www.ultra-skills.com/resources/claude-code-animation-prompts-six-effects). Do not copy its wording into this repository or imply that the original creators approved this pack.


---

# 11 — Turntable

**Group:** 3D Scenes  
**Recommended stack:** Three.js + physically based materials within Remotion + TypeScript  
**Default video:** 1080×1920 · 30 fps · 60 frames (2s)  
**Also required:** Responsive 1920×1080 landscape composition

## Paste this entire section into Claude Code

Create a reusable production animation named `turntable` for my Why? English/Telugu YouTube studio. The effect must be independently rendered and composable into a longer documentary or Short. Do not overwrite existing styles.

**Inputs the scene must accept:** [object], [three product or museum facts], [fact units], [asset provenance].

**Visual direction:** Stage one object on a slowly rotating base in a soft studio. As different surfaces face the camera, hairline annotation arms point to details and reveal short descriptions.

**Frame choreography:** 0-13: light the object and begin platform rotation; 14-30: call out the first detail; 31-46: animate two additional labels with linked anchors; 47-59: finish at a strong three-quarter view and display the product name.

**Technical construction:** Keep rotation smooth, annotations bound to projected mesh coordinates, and PBR shading readable without shiny clutter. Require cited specifications for real products or instruments; otherwise mark illustrative.

**Example creative brief:** Sample idea: museum-style rotating view of a coin, tool, or textile dye vessel.

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

This is an independently authored brief for the **Turntable** effect concept. Inspiration index: [Ultra Skills' public 30-effects article](https://www.ultra-skills.com/resources/claude-code-animation-prompts-six-effects). Do not copy its wording into this repository or imply that the original creators approved this pack.


---

# 12 — Money Stack

**Group:** 3D Scenes  
**Recommended stack:** Three.js + React Three Fiber within Remotion + TypeScript  
**Default video:** 1080×1920 · 30 fps · 60 frames (2s)  
**Also required:** Responsive 1920×1080 landscape composition

## Paste this entire section into Claude Code

Create a reusable production animation named `money-stack` for my Why? English/Telugu YouTube studio. The effect must be independently rendered and composable into a longer documentary or Short. Do not overwrite existing styles.

**Inputs the scene must accept:** [amounts list], [currency], [context and source], [display unit].

**Visual direction:** On a clean tabletop, equal-sized bundled blocks drop onto a platform. Each landing compresses the pile and moves a running total upward. The physical stack becomes a visual comparison of quantity.

**Frame choreography:** 0-12: establish empty platform and baseline value; 13-43: land blocks at increasingly close intervals; 44-53: count to the final verified total and highlight the top block; 54-59: hold a readable total and unit.

**Technical construction:** Generate one data-driven block per amount or bucket, scale counts consistently, and compute the sum from input values rather than typed labels. Include currency unit and time frame on-screen. If depicting estimates, state estimate.

**Example creative brief:** Sample idea: compare a series of documented revenue amounts or a historical trade value using normalized blocks.

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

This is an independently authored brief for the **Money Stack** effect concept. Inspiration index: [Ultra Skills' public 30-effects article](https://www.ultra-skills.com/resources/claude-code-animation-prompts-six-effects). Do not copy its wording into this repository or imply that the original creators approved this pack.


---

# 13 — Receipt

**Group:** 3D Scenes  
**Recommended stack:** Three.js + texture-generated typography within Remotion + TypeScript  
**Default video:** 1080×1920 · 30 fps · 60 frames (2s)  
**Also required:** Responsive 1920×1080 landscape composition

## Paste this entire section into Claude Code

Create a reusable production animation named `receipt` for my Why? English/Telugu YouTube studio. The effect must be independently rendered and composable into a longer documentary or Short. Do not overwrite existing styles.

**Inputs the scene must accept:** [business], [dated line items], [currency], [total], [illustrative flag].

**Visual direction:** A compact receipt printer sits at the upper edge of a dark wooden desk. A narrow strip of paper advances line by line, displaying items and a computed total before separating from the feed.

**Frame choreography:** 0-12: printer indicator activates and paper begins moving; 13-40: print rows synchronously with stepped paper advances; 41-51: emphasize the computed total; 52-59: separate the page and let it settle onto the desk.

**Technical construction:** Construct receipt content as a high-resolution texture on the paper strip. Keep all financial figures consistent and legible. Use deterministic step animations; no overlapping text when the strip curves.

**Example creative brief:** Sample idea: illustrate taxes or the costs of an everyday purchase without misrepresenting a real receipt.

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

This is an independently authored brief for the **Receipt** effect concept. Inspiration index: [Ultra Skills' public 30-effects article](https://www.ultra-skills.com/resources/claude-code-animation-prompts-six-effects). Do not copy its wording into this repository or imply that the original creators approved this pack.


---

# 14 — Iceberg

**Group:** 3D Scenes  
**Recommended stack:** Three.js + volumetric-looking layers within Remotion + TypeScript  
**Default video:** 1080×1920 · 30 fps · 60 frames (2s)  
**Also required:** Responsive 1920×1080 landscape composition

## Paste this entire section into Claude Code

Create a reusable production animation named `iceberg` for my Why? English/Telugu YouTube studio. The effect must be independently rendered and composable into a longer documentary or Short. Do not overwrite existing styles.

**Inputs the scene must accept:** [small visible fact], [three deeper factors], [topic].

**Visual direction:** Above calm water sits a small bright iceberg tip. The camera descends below the surface to reveal a much larger submerged structure. Explanatory flags attach to three distinct depths.

**Frame choreography:** 0-14: frame the small surface tip and title; 15-36: lower the camera through the waterline and uncover submerged geometry; 37-52: pull back to reveal its full scale; 53-59: hold the relative comparison and annotations.

**Technical construction:** Build one mesh with an authentic waterline intersection, clear water/fog colors and sufficient depth contrast. Treat relative sizes as illustration unless grounded in numerical ratios; do not suggest precise proportions without data.

**Example creative brief:** Sample idea: explain the visible versus hidden cost or a headline versus underlying causes.

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

This is an independently authored brief for the **Iceberg** effect concept. Inspiration index: [Ultra Skills' public 30-effects article](https://www.ultra-skills.com/resources/claude-code-animation-prompts-six-effects). Do not copy its wording into this repository or imply that the original creators approved this pack.


---

# 15 — Headline

**Group:** Ink & Paper  
**Recommended stack:** Remotion DOM + CSS 3D within Remotion + TypeScript  
**Default video:** 1080×1920 · 30 fps · 90 frames (3s)  
**Also required:** Responsive 1920×1080 landscape composition

## Paste this entire section into Claude Code

Create a reusable production animation named `headline` for my Why? English/Telugu YouTube studio. The effect must be independently rendered and composable into a longer documentary or Short. Do not overwrite existing styles.

**Inputs the scene must accept:** [source publication or fictional title], [headline], [subhead], [date], [citation].

**Visual direction:** A single editorial news page floats over a desk and assembles from its blank paper state: masthead, rules, headline, photo placeholder and a source line. A pen-like underline marks the key claim.

**Frame choreography:** 0-14: reveal paper and masthead; 15-39: set article content in deliberate column order; 40-68: spotlight a supplied quote or number with a moving underline; 69-89: stop with the proof card readable.

**Technical construction:** Use perspective CSS transforms, textured SVG paper, and frame-based text reveals. Prefer a real cited screenshot when depicting an actual publication; when generating a replica, mark it as an illustrative mock article. Do not invent sourced quotes.

**Example creative brief:** Sample idea: a source-backed documentary proof card with headline and publication date.

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

This is an independently authored brief for the **Headline** effect concept. Inspiration index: [Ultra Skills' public 30-effects article](https://www.ultra-skills.com/resources/claude-code-animation-prompts-six-effects). Do not copy its wording into this repository or imply that the original creators approved this pack.


---

# 16 — Swiss Grid

**Group:** Ink & Paper  
**Recommended stack:** SVG + CSS within Remotion + TypeScript  
**Default video:** 1080×1920 · 30 fps · 60 frames (2s)  
**Also required:** Responsive 1920×1080 landscape composition

## Paste this entire section into Claude Code

Create a reusable production animation named `swiss-grid` for my Why? English/Telugu YouTube studio. The effect must be independently rendered and composable into a longer documentary or Short. Do not overwrite existing styles.

**Inputs the scene must accept:** [three short words], [one message], [accent color].

**Visual direction:** Lay out bold words and geometric panels on an off-white poster grid. Alignment lines appear first, then rectangular tiles slide on precise axes. The composition intentionally snaps into a clean editorial arrangement.

**Frame choreography:** 0-9: reveal a fine layout grid; 10-25: bring in asymmetric blocks on rails; 26-40: shift two headline words between grid cells; 41-54: align the final poster lockup; 55-59: hold the typography.

**Technical construction:** Use strict grid coordinates and pixel snapping on final frames. Prefer a few strong elements over decorative noise. Use Archivo Black for English and Noto Sans Telugu for Telugu; reflow the grid after measuring actual glyph sizes.

**Example creative brief:** Sample idea: a bold two-word chapter announcement in a history or finance documentary.

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

This is an independently authored brief for the **Swiss Grid** effect concept. Inspiration index: [Ultra Skills' public 30-effects article](https://www.ultra-skills.com/resources/claude-code-animation-prompts-six-effects). Do not copy its wording into this repository or imply that the original creators approved this pack.


---

# 17 — Blueprint Draw

**Group:** Ink & Paper  
**Recommended stack:** SVG path animation within Remotion + TypeScript  
**Default video:** 1080×1920 · 30 fps · 60 frames (2s)  
**Also required:** Responsive 1920×1080 landscape composition

## Paste this entire section into Claude Code

Create a reusable production animation named `blueprint-draw` for my Why? English/Telugu YouTube studio. The effect must be independently rendered and composable into a longer documentary or Short. Do not overwrite existing styles.

**Inputs the scene must accept:** [diagram subject], [labels], [scale note].

**Visual direction:** On a dark blue technical page, a single luminous pen stroke traces an architectural or mechanical outline. Measurements, dimension guides and annotations appear only after the main contour is completed.

**Frame choreography:** 0-8: show blueprint frame and origin point; 9-38: draw the main outline through one continuous stroke; 39-51: reveal secondary lines and up to three callouts; 52-59: settle the final drawing with a schematic label.

**Technical construction:** Use SVG path-length interpolation or @remotion/paths; derive a moving nib location from the same path progress. Treat scale and dimensions as schematic unless supplied. Ensure no line abruptly teleports between disconnected path sections.

**Example creative brief:** Sample idea: explain a fort plan, port warehouse, machine outline or construction concept.

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

This is an independently authored brief for the **Blueprint Draw** effect concept. Inspiration index: [Ultra Skills' public 30-effects article](https://www.ultra-skills.com/resources/claude-code-animation-prompts-six-effects). Do not copy its wording into this repository or imply that the original creators approved this pack.


---

# 18 — Paper Desk

**Group:** Ink & Paper  
**Recommended stack:** SVG + CSS + optional handdrawn stroke package within Remotion + TypeScript  
**Default video:** 1080×1920 · 30 fps · 60 frames (2s)  
**Also required:** Responsive 1920×1080 landscape composition

## Paste this entire section into Claude Code

Create a reusable production animation named `paper-desk` for my Why? English/Telugu YouTube studio. The effect must be independently rendered and composable into a longer documentary or Short. Do not overwrite existing styles.

**Inputs the scene must accept:** [3 evidence cards], [highlight phrase], [closing takeaway].

**Visual direction:** A top-down research desk fills with three paper items, each sliding in with believable friction and a tightening shadow. A marker then circles one passage and draws an arrow to a concise conclusion.

**Frame choreography:** 0-18: lay down first and second documents at slight angles; 19-31: place final evidence slip; 32-48: annotate with a visible marker tip and textured stroke; 49-59: frame the completed evidence arrangement.

**Technical construction:** Make evidence cards data-driven. Real citations should display real titles, dates and source labels; do not simulate misleading news screenshots. Use existing approved real paper-slide, marker and knock SFX only when available.

**Example creative brief:** Sample idea: assemble three sources explaining a surprising historical claim.

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

This is an independently authored brief for the **Paper Desk** effect concept. Inspiration index: [Ultra Skills' public 30-effects article](https://www.ultra-skills.com/resources/claude-code-animation-prompts-six-effects). Do not copy its wording into this repository or imply that the original creators approved this pack.


---

# 19 — Ink Doodle

**Group:** Ink & Paper  
**Recommended stack:** SVG + RoughJS or p5 brush within Remotion + TypeScript  
**Default video:** 1080×1920 · 30 fps · 60 frames (2s)  
**Also required:** Responsive 1920×1080 landscape composition

## Paste this entire section into Claude Code

Create a reusable production animation named `ink-doodle` for my Why? English/Telugu YouTube studio. The effect must be independently rendered and composable into a longer documentary or Short. Do not overwrite existing styles.

**Inputs the scene must accept:** [short caption], [character action], [three props].

**Visual direction:** Draw a deliberately imperfect desk character in animated marker strokes. A small repeated action becomes comically faster, while discarded sheets or notes collect near the desk.

**Frame choreography:** 0-10: sketch character and desk into view; 11-31: perform three cycles of a simple action with slight pose variations; 32-45: pile up props as the action quickens; 46-59: reveal a short hand-lettered punchline.

**Technical construction:** Use seeded per-vertex jitter and 2-3 reusable pose states rather than unseeded noise. Maintain character continuity across frames. Keep dialogue out of the image when captions already provide it.

**Example creative brief:** Sample idea: humorous transition about researching hundreds of sources for one answer.

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

This is an independently authored brief for the **Ink Doodle** effect concept. Inspiration index: [Ultra Skills' public 30-effects article](https://www.ultra-skills.com/resources/claude-code-animation-prompts-six-effects). Do not copy its wording into this repository or imply that the original creators approved this pack.


---

# 20 — Ink Wash

**Group:** Ink & Paper  
**Recommended stack:** SVG filter masks + procedural strokes within Remotion + TypeScript  
**Default video:** 1080×1920 · 30 fps · 60 frames (2s)  
**Also required:** Responsive 1920×1080 landscape composition

## Paste this entire section into Claude Code

Create a reusable production animation named `ink-wash` for my Why? English/Telugu YouTube studio. The effect must be independently rendered and composable into a longer documentary or Short. Do not overwrite existing styles.

**Inputs the scene must accept:** [landscape layers], [sun position], [chapter title].

**Visual direction:** Start on warm unmarked paper. Soft pigment spreads to form distant hills, followed by a muted sun and nearer dark ridges. Sparse calligraphy or a plain chapter title appears after the painting settles.

**Frame choreography:** 0-14: spread a pale background wash; 15-28: reveal distant ridge and sun; 29-43: bring in nearer terrain with textured brush edges; 44-59: preserve blank paper for a calm title hold.

**Technical construction:** Animate masks and displacement amounts from frame, not wall time. Work in transparent layers so pigment overlap is plausible. No borrowed painting assets; implement procedural washes or use licensed references with proper credit.

**Example creative brief:** Sample idea: an atmospheric geography or historical chapter break.

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

This is an independently authored brief for the **Ink Wash** effect concept. Inspiration index: [Ultra Skills' public 30-effects article](https://www.ultra-skills.com/resources/claude-code-animation-prompts-six-effects). Do not copy its wording into this repository or imply that the original creators approved this pack.


---

# 21 — Creator Life, Drawn Badly

**Group:** Ink & Paper  
**Recommended stack:** RoughJS + deterministic 2D motion within Remotion + TypeScript  
**Default video:** 1080×1920 · 30 fps · 60 frames (2s)  
**Also required:** Responsive 1920×1080 landscape composition

## Paste this entire section into Claude Code

Create a reusable production animation named `creator-life-doodle` for my Why? English/Telugu YouTube studio. The effect must be independently rendered and composable into a longer documentary or Short. Do not overwrite existing styles.

**Inputs the scene must accept:** [daily task], [pile-up objects], [dry punchline].

**Visual direction:** A deliberately shaky marker drawing depicts a creator at a desk. Cups, notes and calendar pages accumulate until the workspace becomes absurdly cluttered; the central figure barely reacts.

**Frame choreography:** 0-11: draw desk and still-faced character; 12-34: add objects in stop-motion jumps; 35-46: stack and wobble the objects; 47-59: expose an understated final caption.

**Technical construction:** Keep the same imprecise stroke seed across frames to avoid unpleasant line crawl; apply jitter mainly between poses. No rapid strobe and no synthetic cartoon audio. Humor should come from timing and composition.

**Example creative brief:** Sample idea: quick comedic beat about editing versions, revisions or a late export.

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

This is an independently authored brief for the **Creator Life, Drawn Badly** effect concept. Inspiration index: [Ultra Skills' public 30-effects article](https://www.ultra-skills.com/resources/claude-code-animation-prompts-six-effects). Do not copy its wording into this repository or imply that the original creators approved this pack.


---

# 22 — Stat Chart

**Group:** Data & Counters  
**Recommended stack:** SVG + @remotion/paths within Remotion + TypeScript  
**Default video:** 1080×1920 · 30 fps · 90 frames (3s)  
**Also required:** Responsive 1920×1080 landscape composition

## Paste this entire section into Claude Code

Create a reusable production animation named `stat-chart` for my Why? English/Telugu YouTube studio. The effect must be independently rendered and composable into a longer documentary or Short. Do not overwrite existing styles.

**Inputs the scene must accept:** [ordered numeric series], [time labels], [units], [verified source].

**Visual direction:** Create a refined editorial data panel where a large live metric sits beside a thin chart. The line extends across the dates, then sharply changes trajectory around a highlighted event.

**Frame choreography:** 0-18: reveal title, axes and starting figure; 19-50: draw line through the data and advance numeric display; 51-69: emphasize the selected inflection point and rescale if needed; 70-89: hold a clean chart with end value and source.

**Technical construction:** Calculate interpolation from real points, do not invent extra readings between provided data. Scale the y-axis consistently with truthful ticks. A change of chart scale must be visibly indicated. Support negative values and units.

**Example creative brief:** Sample idea: historical gold prices, air pollution figures or population changes with verified data.

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

This is an independently authored brief for the **Stat Chart** effect concept. Inspiration index: [Ultra Skills' public 30-effects article](https://www.ultra-skills.com/resources/claude-code-animation-prompts-six-effects). Do not copy its wording into this repository or imply that the original creators approved this pack.


---

# 23 — Agent Swarm

**Group:** Data & Counters  
**Recommended stack:** SVG + CSS within Remotion + TypeScript  
**Default video:** 1080×1920 · 30 fps · 60 frames (2s)  
**Also required:** Responsive 1920×1080 landscape composition

## Paste this entire section into Claude Code

Create a reusable production animation named `agent-swarm` for my Why? English/Telugu YouTube studio. The effect must be independently rendered and composable into a longer documentary or Short. Do not overwrite existing styles.

**Inputs the scene must accept:** [task labels], [agent count], [statuses], [completion total].

**Visual direction:** One central light branches into a network of smaller nodes. Each node follows a smooth path to a work slot, displays a task tag, and switches to a completed state in sequence. The final image reads as coordinated parallel work.

**Frame choreography:** 0-12: pulse central node; 13-32: spread task paths outward and reveal workers; 33-49: complete tasks in staggered order; 50-59: show the network and a truthful completed-task tally.

**Technical construction:** Generate coordinates deterministically; give each edge a soft Bézier path and ensure captions do not collide. Do not imply that real agents completed anything unless their status input is real. Distinguish demo simulation from actual workflow data.

**Example creative brief:** Sample idea: explain an AI-assisted research or production workflow.

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

This is an independently authored brief for the **Agent Swarm** effect concept. Inspiration index: [Ultra Skills' public 30-effects article](https://www.ultra-skills.com/resources/claude-code-animation-prompts-six-effects). Do not copy its wording into this repository or imply that the original creators approved this pack.


---

# 24 — Day Counter

**Group:** Data & Counters  
**Recommended stack:** CSS 3D + SVG within Remotion + TypeScript  
**Default video:** 1080×1920 · 30 fps · 60 frames (2s)  
**Also required:** Responsive 1920×1080 landscape composition

## Paste this entire section into Claude Code

Create a reusable production animation named `day-counter` for my Why? English/Telugu YouTube studio. The effect must be independently rendered and composable into a longer documentary or Short. Do not overwrite existing styles.

**Inputs the scene must accept:** [start date], [end day or duration], [event description], [calendar basis].

**Visual direction:** A compact paper desk calendar occupies the middle of a warm frame. Sheets flip or turn while a giant day count changes above. A checkmark lands on selected milestone dates.

**Frame choreography:** 0-10: show day one and calendar thickness; 11-37: flip through evenly paced dates, then speed up; 38-50: slow onto final day and stamp one milestone; 51-59: hold result and date.

**Technical construction:** Derive all displayed dates and day indexes from one input calendar, respecting month lengths and leap years. For historical calendars, display the convention or use a neutral elapsed-days count. Never fake a count.

**Example creative brief:** Sample idea: explain a 30-day experiment, a policy deadline or a historically documented interval.

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

This is an independently authored brief for the **Day Counter** effect concept. Inspiration index: [Ultra Skills' public 30-effects article](https://www.ultra-skills.com/resources/claude-code-animation-prompts-six-effects). Do not copy its wording into this repository or imply that the original creators approved this pack.


---

# 25 — Split-Flap

**Group:** UI & Type  
**Recommended stack:** CSS 3D within Remotion + TypeScript  
**Default video:** 1080×1920 · 30 fps · 90 frames (3s)  
**Also required:** Responsive 1920×1080 landscape composition

## Paste this entire section into Claude Code

Create a reusable production animation named `split-flap` for my Why? English/Telugu YouTube studio. The effect must be independently rendered and composable into a longer documentary or Short. Do not overwrite existing styles.

**Inputs the scene must accept:** [2-4 message rows], [character width], [reveal order].

**Visual direction:** Make an old transport information board with physically hinged character cells. Cells cycle through a small set of glyphs and settle left to right until a short final message appears.

**Frame choreography:** 0-18: warm the board and begin random-looking but seeded flap rolls; 19-58: settle each row in cascading order; 59-76: the last row completes with a slightly delayed clack; 77-89: hold the finished message.

**Technical construction:** Use two faces per cell with transform-origin at the hinge and backface-visibility hidden. Derive the visible character at each frame from a deterministic sequence. Support Unicode only if the chosen font and glyph measurement are verified for Telugu.

**Example creative brief:** Sample idea: reveal the next chapter, year, destination or a documentary question.

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

This is an independently authored brief for the **Split-Flap** effect concept. Inspiration index: [Ultra Skills' public 30-effects article](https://www.ultra-skills.com/resources/claude-code-animation-prompts-six-effects). Do not copy its wording into this repository or imply that the original creators approved this pack.


---

# 26 — Before & After

**Group:** UI & Type  
**Recommended stack:** CSS clipped layers + SVG within Remotion + TypeScript  
**Default video:** 1080×1920 · 30 fps · 60 frames (2s)  
**Also required:** Responsive 1920×1080 landscape composition

## Paste this entire section into Claude Code

Create a reusable production animation named `before-after` for my Why? English/Telugu YouTube studio. The effect must be independently rendered and composable into a longer documentary or Short. Do not overwrite existing styles.

**Inputs the scene must accept:** [old state], [new state], [change description], [comparison disclaimer].

**Visual direction:** Place two coherent versions of the same screen inside a simple browser frame. A vertical handle begins near one edge and sweeps across to replace the old design with the updated design, then settles at the far side.

**Frame choreography:** 0-12: establish old appearance and hint at hidden new layer; 13-34: move handle to reveal most of the redesign; 35-47: pause briefly for comparison; 48-59: finish reveal and highlight one improved element.

**Technical construction:** Render both states at identical scale and layout before clipping. Compute new-side clip and handle from the same progress value to avoid seams. Use clear OLD/NEW labels and an illustrative disclaimer if the website is fictional.

**Example creative brief:** Sample idea: compare an old interface and a redesigned one, or historical versus modern presentation styles.

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

This is an independently authored brief for the **Before & After** effect concept. Inspiration index: [Ultra Skills' public 30-effects article](https://www.ultra-skills.com/resources/claude-code-animation-prompts-six-effects). Do not copy its wording into this repository or imply that the original creators approved this pack.


---

# 27 — Lock-Screen Notifications

**Group:** UI & Type  
**Recommended stack:** SVG + CSS within Remotion + TypeScript  
**Default video:** 1080×1920 · 30 fps · 60 frames (2s)  
**Also required:** Responsive 1920×1080 landscape composition

## Paste this entire section into Claude Code

Create a reusable production animation named `lock-screen-notifications` for my Why? English/Telugu YouTube studio. The effect must be independently rendered and composable into a longer documentary or Short. Do not overwrite existing styles.

**Inputs the scene must accept:** [notification list], [title], [optional total], [illustrative flag].

**Visual direction:** Show a clean fictional lock screen. Notification cards arrive upward in a rhythm that accelerates, pushing earlier cards away. A small floating tally rolls upward as each item lands.

**Frame choreography:** 0-11: establish lock-screen clock and first message; 12-37: add the next messages faster with subtle landing compression; 38-50: let the pile crowd the display and update count; 51-59: end on the count and one visible message.

**Technical construction:** Use card arrays with unique stable IDs, computed cumulative amounts, and deterministic arrival frames. No fake screenshots of real people or private messages. Respect safe-area clipping and avoid sending text beneath platform controls.

**Example creative brief:** Sample idea: visualize increasing orders, messages, or alerts from fictional demo data.

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

This is an independently authored brief for the **Lock-Screen Notifications** effect concept. Inspiration index: [Ultra Skills' public 30-effects article](https://www.ultra-skills.com/resources/claude-code-animation-prompts-six-effects). Do not copy its wording into this repository or imply that the original creators approved this pack.


---

# 28 — Type Slam

**Group:** UI & Type  
**Recommended stack:** CSS + SVG typographic transforms within Remotion + TypeScript  
**Default video:** 1080×1920 · 30 fps · 60 frames (2s)  
**Also required:** Responsive 1920×1080 landscape composition

## Paste this entire section into Claude Code

Create a reusable production animation named `type-slam` for my Why? English/Telugu YouTube studio. The effect must be independently rendered and composable into a longer documentary or Short. Do not overwrite existing styles.

**Inputs the scene must accept:** [word one], [word two], [key word], [final color].

**Visual direction:** On a deep charcoal background, short emphatic words land in the center at different scales. The last oversized word occupies most of the frame while an accent fill rises through its letterforms.

**Frame choreography:** 0-11: first word drops from a larger scale with tight motion blur; 12-25: second word lands beneath with a brief shake; 26-39: third word displaces the layout; 40-59: fill the final letters progressively and finish on a stable word.

**Technical construction:** Measure text width before animation; adjust font size to fit long English or Telugu phrases. Make impact changes high contrast but do not use full-frame white flashes or rapid inversion. Emphasize with spacing and weight.

**Example creative brief:** Sample idea: a dramatic one-word history reveal or scientific misconception correction.

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

This is an independently authored brief for the **Type Slam** effect concept. Inspiration index: [Ultra Skills' public 30-effects article](https://www.ultra-skills.com/resources/claude-code-animation-prompts-six-effects). Do not copy its wording into this repository or imply that the original creators approved this pack.


---

# 29 — Particle Word

**Group:** UI & Type  
**Recommended stack:** Three.js Points or 2D Canvas within Remotion + TypeScript  
**Default video:** 1080×1920 · 30 fps · 60 frames (2s)  
**Also required:** Responsive 1920×1080 landscape composition

## Paste this entire section into Claude Code

Create a reusable production animation named `particle-word` for my Why? English/Telugu YouTube studio. The effect must be independently rendered and composable into a longer documentary or Short. Do not overwrite existing styles.

**Inputs the scene must accept:** [word up to 8 characters], [particle density], [background].

**Visual direction:** Thousands of tiny motes orbit a center point in darkness, then move into the silhouette of a single bold word. A few residual motes continue around the edges after the word becomes readable.

**Frame choreography:** 0-15: show a loose rotating dust field; 16-34: compress the formation toward the target; 35-47: guide most points to sampled glyph pixels; 48-59: stabilize the word with a subtle shimmer and gently orbiting extras.

**Technical construction:** Rasterize a loaded font once to acquire deterministic per-particle targets; keep target assignment stable and avoid use of Math.random during frame rendering. Provide a lower-particle fallback for low-spec systems. Verify Telugu glyph clusters render correctly.

**Example creative brief:** Sample idea: form the film title WHY? or a short thematic word from particles.

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

This is an independently authored brief for the **Particle Word** effect concept. Inspiration index: [Ultra Skills' public 30-effects article](https://www.ultra-skills.com/resources/claude-code-animation-prompts-six-effects). Do not copy its wording into this repository or imply that the original creators approved this pack.


---

# 30 — Terminal Bloom

**Group:** UI & Type  
**Recommended stack:** DOM + CSS 3D within Remotion + TypeScript  
**Default video:** 1080×1920 · 30 fps · 60 frames (2s)  
**Also required:** Responsive 1920×1080 landscape composition

## Paste this entire section into Claude Code

Create a reusable production animation named `terminal-bloom` for my Why? English/Telugu YouTube studio. The effect must be independently rendered and composable into a longer documentary or Short. Do not overwrite existing styles.

**Inputs the scene must accept:** [command], [product title], [headline], [two buttons], [three cards].

**Visual direction:** A monospace command appears in a dark terminal. On execution, its characters break apart and turn into the scaffold of a small webpage: header, hero, buttons and cards. The assembled page settles into a quiet accent glow.

**Frame choreography:** 0-11: type command and register Enter; 12-30: scatter and redirect character fragments into a layout skeleton; 31-47: insert hero text and cards in purposeful stagger; 48-59: stabilize page with a slow final camera push.

**Technical construction:** Use frame-driven CSS transforms and character IDs derived from the input text. Support a fallback path where the typed line dissolves rather than morphs per character on low-performance devices. Never expose real tokens, commands with secrets or private repository URLs in the animation.

**Example creative brief:** Sample idea: explain how an AI workflow turns an idea into a production dashboard.

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

This is an independently authored brief for the **Terminal Bloom** effect concept. Inspiration index: [Ultra Skills' public 30-effects article](https://www.ultra-skills.com/resources/claude-code-animation-prompts-six-effects). Do not copy its wording into this repository or imply that the original creators approved this pack.

