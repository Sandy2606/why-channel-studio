# QC report: Delhi Rain 6/6 "Delhi is trying again. Has anything changed?" (Nov 20)

Files: `DelhiRain6_{EN,TE}_{YT,IG}.mp4`, 1080x1920, h264/aac, 30 fps. EN 121.07 s (2:01), TE 144.85 s (2:25).

| Check | Result |
|---|---|
| qc_video, all four files | 0 FAIL; 1 REVIEW each: sharpness on flat diagrams / soft smog plates (known false positive) |
| Freezes | All inside marked HOLDs (`qc/holds_*.json`, each with its reason) |
| Loudness | EN −14.0 (YT) / −14.5 (IG) LUFS, peak −2.0/−2.2 dBTP; TE −13.9 LUFS, −2.2 dBTP |
| check_exports | PASS: bodies identical across platforms, audio in sync, endings differ by design |
| check_copy | 0 FAIL; REVIEW: three limits rest on secondary sources only; platform limits last re-checked 2026-11-16 |
| New voice | 7 lines per language checked with Whisper (EN small.en; TE medium, phonetic): wording matches the script |
| Film 7.2 trim | middle phrase removed at its two delivered pauses; Whisper confirms both kept phrases |
| v2 corrections on screen | Nov 14 flight + OPERATOR'S OWN REPORT vs INDEPENDENT VERIFIED RESULT · NOT PUBLISHED; flight path APPROX. · ILLUSTRATIVE; western-disturbance band over the whole region with no causal arrow; CAN'T TELL WHICH CAUSED IT; AQI 373 → 367 → 290 → 221 strip; Nov 23–25 PLANNED; cost cards separate (ACTUAL TRIAL vs HYPOTHETICAL); IIT Delhi quote with PRELIMINARY label; answer card; Anu's balcony; Option A bridge with no date |
| Reminders | EN 29.0 / 58.7 / 85.2 / 105.4 s; TE 25.7 / 58.3 / 88.6 / 119.5 s; in pauses, clear of captions and key visuals |
| Telugu glyphs | ≈ spelled out (దాదాపు) in Telugu strings; ≠, → shown only in Latin-script chips; TE stills checked, no tofu |

Fixes made during QC: path bug that painted cards full-frame; map chips moved off Delhi; AQI strip label overlap; Telugu label overflow on the humidity gauge; Telugu translation line under the English quote; documentary pan across the balcony source (native pixels only) and a slow push-in on vector evidence boards; report lines read out progressively; cost card frame enters early; answer panels shown before their text.

Not performed: PUB-07 human review of claims, tone and Telugu naturalness (the user's final viewing). The HT article itself was blocked to our fetcher; its points are confirmed through the Inshorts summary (C21).
