import sys; sys.path.insert(0, '/home/claude/gs')
from shorts import *

SPK = {'NAR': '', 'ANNA': '**ANNA** ', 'CHELLI': '**CHELLI** (Sowmya) '}
SPK_TE = {'NAR': '', 'ANNA': '**అన్న** ', 'CHELLI': '**చెల్లి** (Sowmya) '}
CH_NAMES = {'0': 'COLD OPEN', 'F1': 'THE TRUNK', '1': 'CHAPTER 1 · Was India really that rich?', '2': 'CHAPTER 2 · The cloth the world wanted',
            '3': 'CHAPTER 3 · Golconda & Machilipatnam', 'F2': 'THE COIN', '4': 'CHAPTER 4 · Who controlled the wealth?',
            '5': "CHAPTER 5 · Europe didn't discover India", '6': 'CHAPTER 6 · The company that came to trade', '7': 'FINAL 60 SECONDS'}

def sect(i):
    return i.split('.')[0]

def script(lang):
    tl, total = timeline(lang); d = {x['id']: x for x in tl}
    out = []; cur = None
    for r in L:
        if r['id'] not in d: continue
        s = sect(r['id'])
        if s != cur:
            cur = s; out.append(f"\n### {CH_NAMES[s]}  ·  starts {fmt(d[r['id']]['start'])}\n")
        x = d[r['id']]
        txt = r['en'] if lang == 'en' else r['te']
        mood = r['em'] if lang == 'en' else (r['tm'] or r['em'])
        spk = (SPK if lang == 'en' else SPK_TE)[r['spk']]
        lens = ' *(EN only)*' if r['only'] == 'en' else (' *(TE only)*' if r['only'] == 'te' else '')
        tags = []
        if r['src']: tags.append('src ' + r['src'])
        if r['sh']: tags.append('♻ ' + r['sh'])
        tag = ('  `' + ' · '.join(tags) + '`') if tags else ''
        out.append(f"**{r['id']}** `{fmt(x['start'])}–{fmt(x['end'])}` {spk}[{mood}] {txt}{lens}{tag}")
        if lang == 'en' and r['vis']: out.append(f"   → {r['vis']}")
    return '\n'.join(out), total

def shorts_md(lang):
    sp = short_plan(lang); i = 0 if lang == 'en' else 1
    rows = []
    for k, (segs, tot) in sp.items():
        parts = []
        for s in segs:
            if s[0] == 'reuse': parts.append(f"{s[1]} @{fmt(s[2])} ({s[3]:.1f}s)")
            else: parts.append(f"NEW {s[0][4:]} ({s[3]:.1f}s)")
        rows.append(f"| {k} | {tot:.0f} s | " + ' → '.join(parts) + ' |')
    return '| Short | Length | Cut list (film timecodes, %s) |\n|---|---|---|\n' % lang.upper() + '\n'.join(rows)

def pickups():
    lines = []
    for k, p in NEW.items():
        if not p['hook'][0].startswith('REUSE'):
            lines.append(f"- **{k} hook** EN: [HOOK · punchy] {p['hook'][0]}\n  TE: [HOOK] {p['hook'][1]}")
        for rid in p['reuse']:
            if rid in BRIDGE: lines.append(f"- **{k} bridge** EN: [PUNCH] {BRIDGE[rid][0]}\n  TE: [PUNCH] {BRIDGE[rid][1]}")
        lines.append(f"- **{k} tease** EN: [warm · quick] {p['tease'][0]}\n  TE: [ఆప్యాయంగా · వేగంగా] {p['tease'][1]}")
    return '\n'.join(lines)

en, ten = script('en')
te, tte = script('te')
tl_en, _ = timeline('en'); tl_te, _ = timeline('te')
den = {x['id']: x for x in tl_en}; dte = {x['id']: x for x in tl_te}
wc = sum(len(clean(r['en']).replace('⏸', '').split()) for r in L if r['only'] in (None, 'en') and r['en'])
npk = sum((0 if p['hook'][0].startswith('REUSE') else 1) + 1 + sum(1 for x in p['reuse'] if x in BRIDGE) for p in NEW.values())

md = f"""# THE GOLDEN SPARROW · SEASON 1: RECORDING-READY SCRIPTS (EN + TE) · v3 · awaiting "approved"
*Nothing will be recorded until you say "approved". Built on the creatively approved Master Story v2 (`master_story.md`); claim sources are in `sources_verification.md` (C-numbers below).*

## Final changes (round 4, from your review)
1. **Short 6 payoff:**
   - Now includes the **1717 farman** (6.9) and a new Short-only line (B6) on the shift from **imported silver to revenue collected in India**, after the 1765 diwani.
   - Wording is "increasingly pay with revenue", not an absolute switch.
   - The film's Anna line (7.6) uses the same "increasingly".
2. **Tavernier (3.7):**
   - Now reads: "acquired a remarkable blue diamond in India, **possibly from the Golconda region**. It eventually became the Hope diamond."
   - On-screen chip: "EXACT MINE UNKNOWN".
3. **Anglo-Mughal war (6.8b):**
   - **No rupee figure in the voice.** The ₹1,50,000 figure traces to Keay, Kohli and Erikson via a secondary source, and I could not read it directly.
   - The narration now gives the documented outcome without oversimplifying: the envoys begged the emperor's pardon, paid a heavy fine and promised to behave. Only then could the Company trade again, and in 1690 it set up a new base in Bengal, Calcutta.
   - The amount can go on screen once it is checked in Keay, *India: A History*, p. 372.
4. **GDP (1.4):**
   - The voice now says "the **Republic of India's** share was about 4" for 1950.
   - Source note on screen: "MADDISON ESTIMATES · 1700 = UNDIVIDED SUBCONTINENT · 1950 = REPUBLIC OF INDIA ONLY (EXCL. PAKISTAN & BANGLADESH) · AREAS DIFFER".
5. **Short 2 bridge (B2)** after the 1721 hook: "The answer starts in India's weaving villages, with the hands that made the cloth."
6. **Pacing:**
   - **Every timecode below is a planning estimate.**
   - Edit timecodes will come from the recorded audio (the pipeline measures every line).
   - **Delivery is never sped up to match these numbers.** See the pacing check below.
7. **Shorts:**
   - No minimum or target length; each one runs as long as its story needs, up to 3:00.
   - Telugu S6 leaves out the Madras grant (it stays in the film) so it can keep the 1717 farman, the wars and the silver-to-revenue line.

*Earlier rounds, all kept: the cloth is sold c.1680 before the later history; precise 1721 hook; Buxar 1764; "the Damarla Nayakas"; the Roteiro says it was the king's officials who laughed; Hayman and Freer images dropped; Met 1982.66 public domain.*

## Timing (planning estimate, from measured voice rates)
- **Method:**
  - Rates measured from **509 past ElevenLabs takes** (EN 2.63 words/s, TE 10.82 chars/s raw).
  - Pace Model tempo ×1.06 and its gaps applied.
  - Holds added after chapter cards (+2 s) and big reveals (+1.5 s).

| | English | Telugu |
|---|---|---|
| **Film length** | **{fmt(ten)}** (~{wc} words) | **{fmt(tte)}** |
| First section | central question {fmt(den['0.5']['start'])}–{fmt(den['0.5']['end'])}; title card at {fmt(den['0.5']['end'])} | question {fmt(dte['0.5']['start'])}–{fmt(dte['0.5']['end'])}; title card at {fmt(dte['0.5']['end'])} |
| Final section (7.1 → end card) | {fmt(den['7.1']['start'])} → {fmt(ten)} = {ten-den['7.1']['start']:.0f} s | {fmt(dte['7.1']['start'])} → {fmt(tte)} = {tte-dte['7.1']['start']:.0f} s |

### Pacing check: the opening and the final question
At a slower documentary pace (EN ≈ 147 wpm, TE −8%):
- **EN cold open:** about **31 s → 35 s**. The central question (0.5) runs 7.1 → 8.1 s, and the final question (7.9) runs 5.7 → 6.5 s.
- **TE cold open:** about **39 s → 42 s**.

Both versions work at either pace: the title card simply lands later. **The rule is to let the line breathe.** If the hook feels long when we listen back, we cut words, not speed.

**First step after your approval** (only then): record **0.1–0.5 and 7.9** in both languages as a listening test (≈ 12 lines, small credit cost). Sign off the pace, then record the rest.

## Recording rules
- Format as per the playbook: **[MOOD · delivery]**, **bold** = stress, ⏸ = 1–2 s stop (a cut point).
- One chapter per session, and read each chapter once silently first.
- Voices: narrator and Anna = Sandeep; Chelli = Sowmya.
- **eleven_v4**, one take per line.
- Numbers and names a touch slower.
- Telugu numbers: say years naturally (e.g. "పదిహేడు వందల ఇరవై ఒకటి").
- Total recording = film lines + **{npk} pick-up lines per language** for the Shorts (listed below).

---

## ENGLISH: India-centric, world view
{en}

---

## TELUGU: regional-first, inside the wider story
*Visual directions are shared with English (see EN lines with the same number). TE-only lines use the visual noted in the EN section's master plan.*
{te}

---

## SIX SHORTS: exact reuse (9:16, standalone, no recap)
- Shorts **cut from the film recording**; only the NEW lines are recorded separately.
- Trims at ⏸ points are allowed.
- Lengths include 0.22 s joins.

{shorts_md('en')}

{shorts_md('te')}

**Runtime rule (updated Nov 6):** the story decides the runtime, up to 3:00 maximum.
- Long Shorts aim to finish by about 2:45–2:55, leaving a technical buffer.
- Simple ones stay short.
- English and Telugu may differ in length.

**Notes on the Shorts:**
- **S2, S4 and S6 keep their full context.** S2 has a bridge (B2) after the hook. S6 has the 1717 farman plus the silver-to-revenue payoff (B6).
- **S1, S3 and S5 run at their natural length.** There is no minimum or target length.
- **Telugu S6** leaves out the Surat permission steps and the Madras grant (both stay in the film) to keep the 1717 farman, the wars and the silver-to-revenue line.
- **Lines left out of the Shorts:** any line that mentions "our cloth", so each Short stands alone.
- **Content ID:** Shorts over 1:00 with an active Content ID claim can be blocked, so the music, SFX and art in the Shorts must be cleared (our own recordings, Public Domain or CC0 only).

### Pick-up lines to record ({npk} per language)
{pickups()}

---

## Open items before recording (nonessential; phrased cautiously or kept off screen)
- **Damarla grantor's personal name:** Foster, *EFI 1637–41*, pp. 153–156. The narration avoids it.
- **Kollur mine's present-day mandal/district:** kept off screen.
- **Palakollu (TE 2.5)** as a chintz/Dutch trading village: flagged 🔶. If it's unconfirmed by Saturday noon, it becomes "మచిలీపట్నం చుట్టుపక్కల ఊళ్లలో".
- **Roman coins in the Telugu lands (TE 5.4):** confirm one named find, or keep the general wording.
- **Met Open Access images:** pick the Mughal court and survey images, and the Rijksmuseum Masulipatnam view (licence must be CC0).
"""
open('/home/claude/why-channel-studio/videos/2026-11-08_long_golden_sparrow_s1/script.md', 'w').write(md)
print(fmt(ten), fmt(tte), npk, wc)
