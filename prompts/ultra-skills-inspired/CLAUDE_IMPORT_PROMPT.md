# Copy this to Claude Code after attaching/extracting the animation prompt pack

I am maintaining https://github.com/Sandy2606/why-channel-studio on the `main` branch. I am supplying a local archive/folder of **30 self-contained, independently authored Remotion effect briefs**. Read `README.md`, `manifest.json`, and `ALL_30_CLAUDE_ANIMATION_PROMPTS.md` from the attached/extracted pack rather than visiting a web page.

Please integrate this pack into the repo **safely and incrementally**:

1. Read the repo's latest `playbook/why-channel-video-SKILL.md`, paying special attention to **current order of work** and the latest KEEP/DROP rules, plus `pipeline/styles/README.md`, `pipeline/styles/render_style.py`, both long/Shorts renderers and `brand/fonts/`. Explicitly identify any repo changes since this pack was created. Do not assume older weekly scheduling notes are current.
2. Preserve all nine existing Python-generated animations, pipeline APIs, voices and render outputs. Do not rename or delete them. Place these new prompts at `prompts/ultra-skills-inspired/` or a similarly clear folder.
3. Implement a reusable Remotion/TypeScript module in `pipeline/remotion_effects/` with a manifest, schemas, CLI, test previews, and options for **English/Telugu**, **9:16 / 16:9**, voice-aligned frame timing, safe-zone text, and existing brand defaults. Consume MP4 as an input to current Python/ffmpeg editing rather than rewriting the whole pipeline.
4. Start by implementing **01 Map Route**, **15 Headline**, and **22 Stat Chart**, as these are particularly useful for documentary maps, evidence cards and factual graphics. Run render smoke tests on both ratios and with actual Telugu text. Review stills before claiming success. Then implement the remaining effects in manageable batches, documenting any errors. Ask me before changes that would incur fees.
5. Include source validation: every metric and place must have a source field or be marked DEMO. Do not use modern political border lines for historical maps. Use real approved recorded SFX from `sfx/`, never generated cartoon sounds.
6. Commit the prompt documents first with a clear commit message. Create a feature branch and a PR for executable code if practical. Do not force-push or overwrite unrelated changes. Give me a list of exact files changed, tests run and any unimplemented effects.

This prompt pack is **newly written** and only draws on the idea-level effect list from [https://www.ultra-skills.com/resources/claude-code-animation-prompts-six-effects](https://www.ultra-skills.com/resources/claude-code-animation-prompts-six-effects). Do not copy the site's original instructions as part of your commits.
