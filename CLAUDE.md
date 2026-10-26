# Why? Channel Studio: instructions for Claude

1. At the start of every video session run `bash setup.sh` (links the pipeline, fonts, sounds and music into /home/claude/...).
2. Follow `playbook/why-channel-video-SKILL.md` (quality system, Pace Model v2, sound design system, script format, KEEP/DROP log).
3. Per video, create `videos/<YYYY-MM-DD>_<slug>/` and keep cues, phrase anchors, take lists, script, post copy and thumbnails there.
4. Sounds: use only the real recordings in `sfx/` (see `sfx/catalog.json` for role and hit point). Ask the user for topic-specific extras in the visuals list; they upload them to `sfx/`.
5. After every delivery, update the playbook (KEEP/DROP + score history), commit, and push to `main`.
