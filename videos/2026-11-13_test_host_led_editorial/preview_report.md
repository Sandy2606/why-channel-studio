# Host-led editorial preview v1: report (Nov 13, 2026)

- Built to proposal v2, rules main `b0c217f`. **PREVIEW ONLY.** No playbook change and no host library.
- **Likeness assets are not in this repository** (it is public). The host files, the rendered previews and the host rig code stay in private storage only.

## Delivered (sent in chat, not committed)
| File | Length | Loudness |
|---|---|---|
| WHY_HostPreview_EN.mp4 | 18.7 s | −14.3 LUFS, −1.5 dBTP |
| WHY_HostPreview_TE.mp4 | 20.9 s | −14.3 LUFS, −1.5 dBTP |

Both are 9:16, 1080×1920, 30 fps.
- The Telugu delivery is natural, with no speed change. It runs 0.9 s past 20 s because of the 1.2 s question hold.
- ElevenLabs credits used: **0** (three approved voice_lib clips per language).

## What was built
- **Shot 1, host.** The approved H_ref05 rig art in one framing, at native size.
  - Natural mouth movement (Rhubarb cues), blinks, and a brow raise on the question.
  - Stillness on "Not at all": no head-shake art exists.
  - A point toward the board on "right place", an eye glance to the board, and a small nod on "worked".
  - "FAKE?" / "బూటకమా?" struck through with an amber marker line.
- **Shot 2, original evidence card** in the Python 3D Data Chart style.
  - UNSEEDED 100% vs SEEDED ≈118%, labelled RELATIVE TO UNSEEDED CLOUDS.
  - Condition chips in each language's spoken order.
  - SOLAPUR · 2017–19 · GROWING MONSOON CLOUDS · RANDOMISED, plus the citation and DOI. No document image.
- **Shot 3, WHY? reveal.** The amber dot lands, the brand "?" draws, the WHY wordmark locks, with the kicker DELHI vs SOLAPUR. A slow halftone drift keeps the hold alive.
- **Sound.** Music is the_last_threshold, EQ-carved and ducked 62%. SFX: marker, paper_slide, tick ×2, sub_knock ×2. Voice over the bed: EN +22.8 dB, TE +24.3 dB.

## Automated QC (`pipeline/qc/qc_video.py`)
- PASS: dimensions, duration, black frames, freezes, loudness, true peak, dropouts, decode errors, frame-1 brightness.
- EN sharpness at 0 s is REVIEW. That's the intentionally soft-focus studio background: the plate is 1438 px tall, under the frame height, so it's blurred as an allowed fill (→ LAY-05). The host is sharp, at native size.
- The visual checklist (QC-01) is a human review.

## Honest review: 7.5 / 10 (target 8.5)
| Area | Score | Notes |
|---|---|---|
| Host performance | 7.5 | Mouth and blinks read naturally at this size. Prototype mouth shapes. No head shake, so the answer beat relies on stillness and the strike. The point lands just before "right place" (natural), but it's the only gesture. |
| Evidence card | 7.5 | Clear, honest baseline. A static stretch of about 2 s between chips (EN 9–11 s). The Telugu condition line is small (≈27 px), so phone readability is borderline. |
| WHY? reveal | 8.5 | On brand, clean build. The kicker could land a beat earlier. |
| Sound | 8 | Clear voice; light, purposeful SFX. |
| Layout | 7.5 | The lower ~400 px of shots 2–3 are empty (overlay zone, but it reads as unused). The badge's Telugu text is small (fixed component size). |

## Upgrades if the treatment goes ahead (PROPOSED, not rules)
1. A painted phoneme set and one head-shake pose (free Gemini prompts; likeness checked by the user).
2. A second framing (MCU) for questions.
3. Evidence card: a third beat in the static stretch, or a shorter card. Telugu condition line on two larger lines.
4. A native 9:16 studio plate (≥1920 px tall), so the background can be sharp when wanted.
