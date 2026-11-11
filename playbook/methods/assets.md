# Methods: assets (pictures, clips, captures)

Method notes, not rules: they record how we currently do things and are updated by measuring and testing. Rules live in the owner files (see the master playbook). Copied from the pre-reorganisation playbook (tag `pre-pro-system`), with the original line numbers in brackets; superseded parts are left out and recorded in `history.md`.

## Finding and downloading [PB:205–213]
   - Pexels links and Wikimedia CC photos.
   - ChatGPT image prompts (9:16 for Shorts, 16:9 for long videos).
   - Search and download stock yourself when the user hasn't supplied it. WebFetch on Pexels search pages works; direct download URLs:
     - videos: pexels.com/download/video/ID/
     - photos: images.pexels.com/photos/ID/pexels-photo-ID.jpeg?w=2400
   - Wikimedia: use upload.wikimedia.org thumb URLs at standard sizes (960/1280/1920). Special:FilePath and the API are rate-limited (429).
   - Pre-extract clip frames at 1080p and 30 fps. Vertical clips go on a blurred fill.

## Captures [PB:330, 340, 354]
- Playwright element screenshots + Range.getClientRects() give real, exact highlights (a narrow viewport makes text bigger).
- When a capture tool can't screenshot, print-to-PDF is fine: build clippings from the PDF at 300 dpi; crops found by text (clipkit.py: pdftotext -bbox → crop + exact-phrase highlight).
- Evidence board: real screenshots as torn paper clippings with tape, source tag chip, highlighter sweeping the exact quoted line in sync with the voice.

## Space and science [PB:258]
- NASA SVS animations (public domain, credit Goddard/CI Lab) for space events; for 16:9 clips with moving subjects, use a wide feathered band over a starfield instead of a tight 9:16 crop (the subjects leave a tight crop).
- Unsplash MCP works for scene/object cover photos (images.unsplash.com downloads from the shell). [PB:362]


