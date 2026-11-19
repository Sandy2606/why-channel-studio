# Delhi Rain 4/6 "Rain tonight, smog by…?" · QC report (Nov 18) · AWAITING THE USER'S FINAL VIEWING APPROVAL, NOT FOR PUBLISHING YET

Files (local only): `DelhiRain4_{EN,TE}_{YT,IG}.mp4`. EN 1:55.0, TE 2:14.6 (under 3:00).
- **New voice:** 4 lines per language, 635 credits. All 8 checked with Whisper.
- **Reused:** 12 film clips.
- **New illustration:** Anu at the puddle, 2 variations, 380 credits (see item 2).

## The user's adjustments (Nov 18)
1. **Film line 4.7 is cut at its delivered pause after the second "Every other day…"** (EN 7.66 s, TE 9.56 s). The spoken "all winter" / "చలికాలం మొత్తం" is gone, and Whisper confirms the line now ends on "Every other day". The rest of the take is untouched. On screen: VERY POOR → MODERATE · RAIN ALMOST EVERY OTHER DAY.
2. **Anu's heavy-rain morning:**
   - Labelled HYPOTHETICAL · THE MORNING AFTER A DOWNPOUR, then HYPOTHETICAL · ILLUSTRATIVE on the puddle picture.
   - A4 wasn't accessible, so a consistent new illustration was made (gpt-image, text prompt matched to A3: bob with bangs, round glasses, mustard cardigan, teal scarf, navy joggers, white sneakers). Her delighted reaction to the boat is kept; ripples show the boat floating.
   - The file stays local (`assets/A4n_anu_puddle.png`).
3. **IIT Kanpur:**
   - The reported small drop sits beside OTHER SCIENTISTS: DISPUTE IT, then NOT SHOWN THAT SEEDING CAUSED ANY DROP.
   - The Solapur beat shows MORE RAIN FROM SUITABLE CLOUDS · "rainfall enhancement, not proof of cleaner air in Delhi" (BAMS 2023).
   - The new tease says "Next: Solapur… where seeding added rain."
- **Two-lane recovery:**
  - Each lane traces out as it is named: GASES (NOx, SO₂) ~2–3 DAYS, PARTICLES (PM2.5, PM10) ~4–5 DAYS.
  - Labels: TYPICAL FINDINGS · NOT DEADLINES · VARIES WITH WEATHER, plus the PRELIMINARY · NOT PEER-REVIEWED tag and the source line.
- **Reminders:**
  - Subscribe (YT) / Follow (IG), 62% scale at the bottom, 1.9 s, one soft click.
  - EN: 29.9, 58.3, 92.5 s. TE: 27.5, 60.3, 93.4, 115.5 s.
  - Never inside the 80–95% or recovery-figure narration; the ending CTA is kept.

## Checks
| Check | EN YT | EN IG | TE YT | TE IG |
|---|---|---|---|---|
| qc_video | PASS (0 FAIL) | PASS | PASS | PASS |
| integrated loudness / true peak | −14.0 / −1.8 | −14.0 / −1.9 | −14.1 / −2.0 | −14.1 / −2.0 |
| freezes | PASS (marked reading holds) | PASS | PASS | PASS |
| check_exports | PASS (0 FAIL) | | | |
| check_copy | 0 FAIL; REVIEW: secondary-source limits | | | |

- **Purposeful motion added after the first pass:**
  - The hook rain is heavier.
  - The recovery curves trace day by day.
  - Ghude's calendar days appear before the rain fills every other day.
  - The plane picture pushes in behind Prabhakaran's source card.
- **Remaining holds:** evidence reads, listed in `qc/holds_*.json`.
- **Not done tonight:** platform limits were not re-fetched (the web request needed an approval that went unanswered); the Nov 16 check stands.
- **Frame review:** stills sheets for both languages checked. They stay local (host).
