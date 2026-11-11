# GS 5/6 · "Europe didn't discover India" · QC report (Nov 11)

| Check | EN (YT / IG) | TE (YT / IG) |
|---|---|---|
| Duration (under 3:00) | 2:17.3 ✅ | 2:46.1 ✅ (13.9 s margin; narration not sped up) |
| Resolution / fps | 1080×1920 / 30 | 1080×1920 / 30 |
| Loudness / true peak | −14.7 LUFS / −1.9 dBTP | −14.7 LUFS / −1.5 dBTP |
| Black frames | none | none |
| Freezes (≥ 2.5 s with no motion) | none | none (two Telugu holds fixed: the IBN MAJID name greys as doubt grows; the Calicut smoke drifts for 4.5 s) |
| Decode errors | 0 | 0 |
| Frame 1 brightness (mean) | 145 | 145 |
| Loop seam (first vs last frame, mean abs diff) | 2.05 | 1.99 |
| Automated layout check (every 0.5 s: padding, edges, overlaps, badge, caption lane) | 0 defects | 0 defects (the coin-card overlap found on the first Telugu render was fixed) |
| Sharp-picture rule | every source image ≤ 1.0 source px per output px (asserted in code) | same |

**Sharpness, per scene (Laplacian variance):**
- Documents, archive pictures and cards score 940–1,810.
- Flat vector maps score 98–830, which is expected for flat colour, not softness.

**Human checks done on frames (contact sheets and phone-size sheets in `qc/`):**
- Key terms are readable at phone size.
- There is one exhibit at a time, with no ghosting between documents.
- Telugu exhibits land on the Telugu words.
- Captions stay in their lane on a calm part of the picture.
- Badge and chip sit inside their borders.
- Labels:
  - The Phanigiri coin is labelled "illustrative example, not the Phanigiri coin".
  - The Roteiro is shown alone and labelled as a surviving manuscript copy.
  - Translation quotes are labelled "Ravenstein 1898".

**Still yours to do:** a full listening pass for naturalness and pronunciation (e.g. "Canaqua", "crew's") and the ambience balance.

**Sound:**
- Voice and music are unchanged and approved; the music bed is *where_the_river_bends*.
- Real SFX are taken from `sfx/` only.
- `cannon_distant` is used once, low, under the Calicut bombardment pin. It was owner-cleared on Nov 10; its provenance is unverified and no licence is claimed.
