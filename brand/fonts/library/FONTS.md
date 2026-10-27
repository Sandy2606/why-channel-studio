# Font library (all SIL Open Font License 1.1, from google/fonts)
Free for monetized videos, thumbnails, titles and captions; no credit required. Don't sell the font files themselves.
See `SPECIMEN.png` for a side-by-side preview. Brand defaults stay Archivo Black + Space Mono + Noto Sans Telugu (in `brand/fonts/`).

| Font | Lang | Best for |
|---|---|---|
| Bebas Neue | EN | tall condensed thumbnail headlines, big numbers |
| Oswald (variable) | EN | condensed bold titles, chapter cards |
| Montserrat (variable) | EN | bold modern titles, covers |
| Poppins (Regular→ExtraBold) | EN | clean modern labels and titles |
| Inter (variable) | EN | UI-style labels, data cards, small text |
| Lato (Regular/Bold/Black) | EN | readable body text, subtitles |
| Nunito (variable) | EN | friendly rounded titles |
| Raleway (variable) | EN | elegant headings |
| Noto Sans Telugu (variable) | TE | default captions / body (current brand) |
| Noto Serif Telugu (variable) | TE | formal / story titles |
| Hind Guntur (Regular/Medium/Bold) | TE | modern, real Bold, clean labels |
| Baloo Tammudu 2 (variable) | TE | rounded, friendly, punchy cover titles |
| Ramabhadra | TE | heavy headline look |
| Timmana | TE | bold display titles |
| Mandali / Mallanna | TE | readable small text |
| Ramaraja / Peddana / Dhurjati / Tenali Ramakrishna | TE | traditional display |
| Suravaram / Lakki Reddy / Gurajada | TE | handwritten / brush, headings only |

Loading in PIL: `ImageFont.truetype(path, px, layout_engine=ImageFont.Layout.RAQM)` (RAQM is required for correct Telugu shaping); for variable fonts call `f.set_variation_by_name(b"Bold")` (or "Black"/"ExtraBold" when available).
