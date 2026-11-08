# Why? Channel Studio: instructions for Claude

1. At the start of every video session run `bash setup.sh` (links the pipeline, fonts, sounds and music into /home/claude/...).
2. Follow `playbook/why-channel-video-SKILL.md` (quality system, Pace Model v2, sound design system, script format, KEEP/DROP log).
3. Per video, create `videos/<YYYY-MM-DD>_<slug>/` and keep cues, phrase anchors, take lists, script, post copy and thumbnails there.
4. Sounds: use only the real recordings in `sfx/` (see `sfx/catalog.json` for role and hit point). Ask the user for topic-specific extras in the visuals list; they upload them to `sfx/`.
5. After every delivery, update the playbook (KEEP/DROP + score history), commit, and push to `main`.
6. Animation styles: `pipeline/styles/README.md` lists nine ready styles (Isometric, Paper-Cut, 3D Data Chart, Synthwave, 3D Explainer, Maths Diagram, Cartoon Explainer, Domino Reveal, Glow Atom). Consider them whenever writing a scene sheet and use whichever fits the explanation.
7. Order of work: follow "Current order of work" in the playbook. Scripts go through versions until the user approves the final script. Every scene sheet names the animation style for every line or chapter, and rendering waits until the user has agreed those styles.
8. Remotion effects: `pipeline/remotion_effects/README.md` lists 30 more clip effects (silent MP4s for the Python editors), in English and Telugu, for 9:16 and 16:9. Offer them in scene sheets alongside the nine Python styles. Their factual fields need sources unless shown as DEMO. Keep the two collections separate.
