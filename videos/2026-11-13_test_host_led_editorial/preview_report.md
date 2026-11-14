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

---

# Polish pass v2 (Nov 13, 2026, after the user's review)
The concept was approved in principle (user: 8.5/10 concept, 7.8/10 execution). One focused polish pass was requested: Telugu chart timing, phone readability, frame composition. Host, voice, WHY? reveal and Telugu length are unchanged.

| Request | Change |
|---|---|
| Telugu chart timing | Both bars now rise together as the card lands, so the 100 vs 118 comparison is complete in about 1.5 s in both languages. On the spoken "18", a dashed reference at the unseeded level and an amber **+18%** bracket draw the difference, and the headline lands. |
| Phone readability | The numbers are labelled **RAINFALL INDEX · UNSEEDED CLOUDS = 100** (TE: వర్షపాత సూచిక · సీడ్ చేయని మేఘాలు = 100). The values read 100 and 118, with no "%", so they can't be read as cloud counts. The conditions are on two larger lines (36/34 px; TE 38). Chips are 38–40 px. The citation moved below the captions, still inside the safe zone, with the DOI kept as secondary text. |
| Composition | A larger chart that fills y≈410–1180. One restrained push-in across the card (still a downscale), so no stretch freezes. The WHY? lockup is larger and centred in the safe area. |

Automated QC (v2): PASS on dimensions, duration (EN 18.7 s, TE 20.87 s), black frames, **freezes (now none in either language)**, −14.3 LUFS, −1.5 dBTP, dropouts, decode and frame 1. EN sharpness at 0 s stays REVIEW: the intentional soft-focus studio background. Visual QC (QC-01) is a human review.

Honest score, v2 execution: **8.2 / 10**.

Still open:
- prototype mouth shapes;
- one gesture;
- the soft background (no native 9:16 plate);
- the Telugu headline arrives late by design, because it follows the spoken "18";
- the lower ~350 px under the citation is the platform overlay zone.
