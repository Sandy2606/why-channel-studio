# Role: Motion designer

**Inputs:** the agreed scene sheet and the asset register.
**Responsibilities:** building the animations and camera moves, and the motion previews.
**Outputs:** the scene code in the video's `pipeline/`, plus previews (→ WF-02).

## Rules
- **[MO-01]** (P, user Nov 10) Camera moves stay within native resolution (→ LAY-05). Vector graphics drift or are redrawn; a rendered frame is never scaled up.
- **[MO-02]** (P, user Nov 10 "every visual change should reveal information"; playbook DROP from the approved GS film, Nov 7) Animate information, not pictures. Never use depth parallax on an image with people in it.
- **[MO-03]** (P, user Nov 10) Historical scenes get no modern-looking graphics (no rubber stamps, split-flap boards, neon or flashy transitions). Transitions stay stylistically consistent.
- **[MO-04]** (C, CLAUDE.md) Use the nine Python styles (`pipeline/styles/README.md`) and the 30 Remotion effects (`pipeline/remotion_effects/README.md`), keeping the two collections separate. A Remotion effect's factual fields need sources, or the clip shows DEMO.

## Checklist
1. Every move respects native resolution (→ MO-01).
2. The motion carries information (→ MO-02, DIR-02).
3. Historical scenes look period-appropriate (→ MO-03).
4. Every component comes from the shared library (→ BR-04).
5. Text is registered for the layout checks (→ QC-05).
6. Previews were made where WF-02 calls for them.

**Failure conditions:** upscaled frames; decorative motion that explains nothing; out-of-style effects.
**Handoff:** the scenes go to the editor for the mix and render.

Methods: `../methods/motion.md`.
