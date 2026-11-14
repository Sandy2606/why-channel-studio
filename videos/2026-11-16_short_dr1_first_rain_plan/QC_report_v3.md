# Delhi Rain 1/6 · v3 (round 2 of the v2 rebuild) · QC report (Nov 14) · AWAITING THE USER'S FINAL REVIEW, NOT FOR PUBLISHING YET

Files (local only): `DelhiRain1_v3_{EN,TE}_{YT,IG}.mp4`. EN runs 1:55.8 and TE 2:19.8. Same approved voice tracks; no new credits.

## Changes from v2 (user review, Nov 14)
1. **Opening:** no zoom out of the board.
   - After the lift, the timeline starts at TODAY · 2026 and rewinds fast through the years.
   - The big year counter rolls, slows and stops exactly on the spoken "1957".
   - The 1957 painting develops from sepia to colour in the narration pause, then opens with soft edges into the full-screen lawn.
   - The 2025 balcony opens the same way.
2. **Subtitles move:**
   - Each subtitle chunk takes the first free position (1515 / 1445 / 1585 / 470 / 560) that overlaps no drawn label or reserved key area: the board, faces, chips, the boat.
   - Numbers are amber and underlined.
3. **Spacing:**
   - The 1957 header lines are spread out.
   - The results labels are respaced, and the verdict pill no longer touches them.
   - The 1971–72 ground scene was raised (horizon at y 1380) so subtitles sit on open ground.
   - The illustration label moved under the source card.
4. **Map:**
   - India first, with Delhi marked by an India Gate silhouette.
   - A zoom to the Delhi region, with state lines and an India inset in the corner.
   - Meerut to Delhi; flare rings over Burari, Karol Bagh and Mayur Vihar; a 20 km scale bar.
   - Boundaries: India as per the Survey of India (DataMeet `india-composite`, CC0) and state boundaries (DataMeet, CC BY 4.0). Credited on screen and in the post copy.
5. **Delhi landmark:** India Gate on the map and next to "2025 · DELHI".
6. **Small subscribe/follow reminders** (user request, Nov 14):
   - The BR-09 card at 62% at the bottom of the frame, about every 30 s, with quiet click/bell sounds at 30% of the slide level.
   - EN at 29.0, 65.2 and 86.0 s; TE at 31.0, 64.0, 92.6 and 120.4 s.
   - None in the first 15 s, none over key visuals, YouTube "Subscribe" / Instagram "Follow".
   - **This conflicts with FMT-04** ("Shorts have no mid-video subscribe card"). Your latest instruction was followed for this Short; the rule changes only if you approve (WF-05).

## Technical QC (`qc_video.py`, each file)
| File | Loudness | True peak | Unmarked freezes | Loop seam |
|---|---|---|---|---|
| EN YT | −14.0 LUFS | −1.1 dBTP (limit −1.0) | 0 | PASS |
| EN IG | −14.0 LUFS | −1.5 dBTP | 0 | PASS |
| TE YT / IG | −14.0 LUFS | −1.6 dBTP | 0 | PASS |

`check_exports`: PASS. The body is identical at 8 points; audio stays in sync across platforms. The Telugu holds are the same as in v2, and the pause after "1957" is now filled by the painting developing.
