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

md = f"""# THE GOLDEN SPARROW · SEASON 1: FINAL RECORDING SCRIPTS (EN + TE) · v2 · for approval
*Do not record until approved. Built on the creatively approved Master Story v2 (`master_story.md`); claim sources are in `sources_verification.md` (C-numbers below).*

## Round-3 corrections (from your review)
1. **Cloth chronology:** the London sale is now beat **6.7** ("c.1680" chip), before 1686, 1717, the 1740s and 1756. The finale only calls back to it visually (7.1).
2. **1721 hook made precise:** enacted 1721, in force from 25 Dec 1722, covering *certain* printed, painted, stained or dyed calicoes, printed abroad **or in Britain**, with exceptions (spoken in 0.1–0.2 and 2.12; full terms in the on-screen chip). Telugu explains the **competition with wool and silk** (0.2, 2.14), not "banned because Indian".
3. **Buxar 1764** added before the **1765** diwani (7.5).
4. **1639 Madras grant:** the sources name different individuals (Damarla Venkatadri, Damarla Venkatappa and his brother Ayyappa), and the overlord is described as both the Vijayanagara king Venkata III and the "Raja of Chandragiri". The narration therefore says only what all sources agree on: "**the Damarla Nayakas**, local rulers of this coast under the Vijayanagara king" (6.5). Individual names stay off until checked in Foster, *English Factories in India 1637–41*, pp. 153–156.
5. **Spoken-word timing pass done** (method below), with a timestamp on every line.
6. **Shorts recalculated** from exact film timecodes; the new pick-up lines needed are counted below.
7. **Claims rechecked.** Changes:
   - The Zamorin "unimpressed" claim is corrected: the *Roteiro* says the **king's officials laughed** at the gifts.
   - The Tavernier blue is now "from Golconda's mines", not Kollur specifically.
   - Methwold's worker count is now "tens of thousands, early 1620s".
   - The Kollur district label is removed.
8. **Artwork:**
   - The Hayman/NPG Plassey painting is **dropped** (commercial licence); Plassey is now an AI reconstruction plus the map.
   - Bichitr's Jahangir (Freer) is **dropped** ("usage conditions apply"); a Met Open Access Mughal court image will replace it.
   - Met 1982.66 is **confirmed Public Domain** (18th c., captioned as such).
9. **One addition (+13 s, easy to drop):** the **Anglo-Mughal war of 1686–90** (6.8b). The Company tried force, lost, apologised and paid ₹1.5 lakh. It strengthens the turn toward politics: "Fighting the Mughals had failed. But choosing rulers… paid."

## Timing (measured, not guessed)
- **Method:** speaking rates are measured from **509 past ElevenLabs takes** in voice_lib (EN 2.63 words/s, TE 10.82 chars/s raw), with the long-form Pace Model tempo (×1.06) and its gaps applied: chapter 1.3 s, '?' 0.45 s, punch 0.5 s, ⏸ 0.25–0.45 s. Cinematic holds are added after chapter cards (+2 s) and big reveals (+1.5 s).

| | English | Telugu |
|---|---|---|
| **Film length** | **{fmt(ten)}** (~{wc} words) | **{fmt(tte)}** |
| First 30 s | hook ends {fmt(den['0.4']['end'])}; central question {fmt(den['0.5']['start'])}–{fmt(den['0.5']['end'])}; title card at {fmt(den['0.5']['end'])} | hook ends {fmt(dte['0.4']['end'])}; question {fmt(dte['0.5']['start'])}–{fmt(dte['0.5']['end'])}; title card at {fmt(dte['0.5']['end'])} |
| Final section (from 7.1 to the end card) | {fmt(den['7.1']['start'])} → {fmt(ten)} = {ten-den['7.1']['start']:.0f} s | {fmt(dte['7.1']['start'])} → {fmt(tte)} = {tte-dte['7.1']['start']:.0f} s |

- **Telugu** is longer and is **not rushed**: its first section runs ~38 s and its ending ~80 s, because of the extra regional beat (7.4) and longer word forms.
- **English runtime:** at our approved pace, English comes out ≈ **13.5 min**, not 16:45. I have not padded it.
- **If you want it longer,** the strongest real additions are:
  - (a) a Machilipatnam bazaar and everyday-life scene (+40 s);
  - (b) the 1695 *Ganj-i-Sawai* seizure by an English pirate and Aurangzeb's punishment of the Company (+35 s).
  - Both would be sourced first.
- Final timings will be re-measured from the actual recordings (Pace Model report).

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

**Notes on the Shorts:**
- S1, S3 and S5 (EN) land at 82–88 s, just under the 90 s start point; I'd keep them tight rather than pad.
- **TE S6 is 135 s:** the Plassey payoff needs it (it stays under 3:00).
- Lines that mention "our cloth" are kept out of the Shorts, so each one stands alone.

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
