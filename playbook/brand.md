# Brand and layout (owner file)

Channel-wide look. Role guides link here and never restate these values. Rule format and precedence: see the master playbook.

## Brand
- **[BR-01]** (P, user Oct 27, Nov 10; decision Nov 10) **Palette.** Core brand colours, unchanged: ink #0A0A0A, cream #F4F1EA, amber #FFB224. Historical maps and visual reconstructions may also use muted natural tones where appropriate: parchment, sandstone, muted olive, antique gold (#C4A05C) and related tones. No bright red graphics, neon, excessive glow or modern-looking effects that clash with the documentary. Historical paintings and archival photographs keep their original colours.
- **[BR-02]** (P, user Oct 2026) **Typography.** Archivo Black for headlines and captions, Space Mono for labels; Telugu uses Noto Sans Telugu Black, shaped with RAQM. Copies with ₹ merged in are in `brand/fonts/`. Glyph limits: Archivo has no ▶ or ↓; the Telugu font has no →, µ, ³, ≈ or ≤, so substitute them (`te_text` does: → becomes "-", µg/m³ becomes మైక్రోగ్రాములు, ≈ becomes దాదాపు). Check Telugu stills for missing-glyph boxes before every render.
- **[BR-03]** (P, user Oct 27) **Series tag:** theme + number / total, e.g. `GOLD · 2/6` (TE `గోల్డ్ · 2/6`); never "GOLD WEEK" or bare "GOLD". The film uses the theme with `FULL STORY` or the series' own film label.
- **[BR-04]** (P, user Nov 10) **One component per UI element.** Corner badges come only from `pipeline/style_v2/layout.py` `badge()`: fill inset inside its border, drawn at 3x, text centred on its real ink box (Telugu-safe), fixed 60 px height, 26 px padding, full-round radius, 64 px from the frame edge, both corner badges on one centre line. The section chip hides in hook, tease and loop.
- **[BR-05]** (P, user Oct 27–28, Nov 10) **Look.** Premium editorial documentary at the Think School / What If standard; never epic or "Rajamouli" style; no mascot face; the "?"→"!" logo only at the why, payoff and ending. Every effect looks designed by the same editor in the same design system; an effect that looks out of place is replaced even if it works. The presentation style may change per video or per part (the user's Oct 28 freedom) within these rules. Style v2 (dark glass cards, amber edge bar, amber gradient on key words, glowing amber guide dot, highlighter) remains one available treatment; helpers in `pipeline/style_v2`.
- **[BR-06]** (P, user Oct 31) **Telugu versions** show Telugu on-screen text (titles, labels, cards), never the English graphics text. Law names, months and numbers follow the voice. Telugu layouts are inspected on their own.
- **[BR-07]** (P, user Oct 28) **Accounts.** YouTube EN "Why?" @WhyEveryQuestionHasAStory · YouTube TE "why?telugu" @WhyTeluguStories · Instagram EN "Why?" why_everyquestionhasastory · Instagram TE "Why? Telugu" whytelugu. Profile pictures are in `brand/avatars/*_2160.png`.
- **[BR-08]** (P, user Oct 28–29) **Covers and thumbnails** are delivered with every video in EN and TE. They carry the WHY? logo and the series tag; match the topic exactly; look human-made, stylish and modern (no red-box text); show no recognisable person's face; and avoid graphic blood. The layout is set in the series plan.
- **[BR-09]** (P, user Oct 29) **CTA card:** a realistic animated subscribe/follow card (`pipeline/style_v2/cta_card.py`). YT: profile picture, channel name and handle, Subscribe → "Subscribed", then the bell → "All". IG: profile picture, handle, Follow → "Following" with a check mark. Real click, bell and tick sounds.

## Layout
- **[LAY-01]** (P, v2 user Nov 11; earlier Oct 2026 and Nov 10) **Use the whole frame as the storytelling canvas.**
  - Use the full frame whenever the story benefits; never a fixed working area that leaves the lower part of the frame unused, and no large, permanently dark or empty regions just because captions appear near the bottom.
  - Distribute information across the top, centre and lower parts of the frame, and vary the composition from scene to scene instead of repeating one arrangement.
  - Let animation move through the frame: maps, connecting lines, ships, arrows, formations and flows may extend into the lower screen and behind the platform overlays when they are not essential text.
  - Full-screen pictures, maps and graphics fill the frame to every edge: no dark band, bottom fade, masked area or heavy dim, and no visuals shrunk into bands or boxes.
  - Intentional negative space is allowed when it serves the story; unused space must be a directorial choice, not a layout limitation. The goal is not to make objects bigger or fill every pixel. No decorative clutter or unnecessary effects (→ BR-05).
- **[LAY-02]** (P, v3 user Nov 11; earlier Nov 10) **Captions are always readable and never hide essential information.**
  - 9:16: captions sit at y≈1446 by default, above the YouTube/Instagram overlay.
  - Captions may sit over maps, diagrams, moving graphics and full-frame pictures, with an outline, a shadow or a subtle local gradient behind the words (never a full-width band or box). They must never become unreadable.
  - Captions never cover essential information: an inset picture or document panel, a card, a label, a count or a credit. Moving elements (coins, formations, map lines, figures) are softened or routed around the caption line so they don't compete with it.
  - Captions are word by word, synced, with the active word in amber, spelled exactly as the script.
- **[LAY-03]** (P, playbook) **Safe zones.**
  - 9:16: key text between y = 250 and 1550; nothing important in the bottom ~370 px or the right ~140 px.
  - 16:9: captions at about y = 950; nothing important in the bottom-right corner (player controls and end-screen elements).
- **[LAY-04]** (C, v2 user Nov 10) **Captions are the main text.** Editorial labels and headlines are welcome where they add meaning (archival labels, kickers, data titles). Avoid on-screen text that merely duplicates the narration.
- **[LAY-05]** (P, user Nov 10) **Sharp pictures only.** Never show a source image beyond its native resolution: the crop shown keeps at least ~1 source pixel per output pixel.
  - A low-resolution image appears at native size on a designed full-frame background; a blurred fill of the same picture is one allowed background.
  - For close-ups, use a sharper or larger source, or show the image smaller.
  - Draw maps and graphics at the final output size; never zoom a rendered map.
  - Sharpness is measured in QC (→ QC-06).
