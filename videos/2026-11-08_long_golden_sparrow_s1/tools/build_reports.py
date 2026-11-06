"""Build the post-recording reports from the measured timelines: recording_report.md, shorts_cut_plans.md,
visual_asset_requirements.md (written into the video folder)."""
import sys, json, math, re
sys.path.insert(0, '/home/claude/gs')
from lines import L
from shorts import NEW
OUT = '/home/claude/gs/out'
V = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/why-channel-studio/videos/2026-11-08_long_golden_sparrow_s1'
T = {l: json.load(open(f'{OUT}/timeline_{l}.json')) for l in ('en', 'te')}
S = {l: json.load(open(f'{OUT}/shorts_{l}.json')) for l in ('en', 'te')}
ROWS = {r['id']: r for r in L}
JOBS = {(j['lang'], j['id']): j['text'] for j in json.load(open('/home/claude/gs/jobs.json'))}


def tc(s):
    m, s = divmod(max(0, s), 60); return f"{int(m):02d}:{s:04.1f}"


def mmss(s):
    m, s = divmod(round(s), 60); return f"{int(m)}:{int(s):02d}"


CHAP = {'0': 'Cold open', 'F1': 'Trunk scene', '1': 'Ch 1 · Was India really that rich?', '2': 'Ch 2 · The cloth the world wanted',
        '3': 'Ch 3 · Golconda and Machilipatnam', '4': 'Ch 4 · Who controlled the wealth?', '5': "Ch 5 · Europe didn't discover India",
        '6': 'Ch 6 · The company that came to trade', '7': 'Ending · Plassey → Season 2'}


def section(i):
    return 'F1' if i.startswith('F1') else ('3' if i.startswith('F2') else i.split('.')[0])


# ------------------------------------------------------------------ recording report
def rec_report():
    o = ['# Golden Sparrow S1: recording report (measured from the recorded audio)', '',
         'All lines are recorded in both languages at natural pace: **no tempo change and no pause squeezing**. '
         'Edge trims and Pace Model gaps are the only edits. The cold open and the final question use the approved test takes, and the cold-open gaps are kept exactly as in the test. '
         '0.2 was re-recorded with the new wording.', '',
         '## Film', '', '| | English | Telugu |', '|---|---|---|']
    e, t = T['en'], T['te']
    o.append(f"| **Total runtime** (incl. title card and 5 s Season 2 end card) | **{mmss(e['total'])}** ({e['total']:.1f} s) | **{mmss(t['total'])}** ({t['total']:.1f} s) |")
    o.append(f"| Cold open → title sting | {tc(e['title_hit'])} | {tc(t['title_hit'])} |")
    for c in '1234567':
        if c == '7':
            o.append(f"| Ending (7.1) starts | {tc(e['lines']['7.1'][0])} | {tc(t['lines']['7.1'][0])} |"); continue
        o.append(f"| {CHAP[c]} | {tc(e['chapters'][c])} | {tc(t['chapters'][c])} |")
    o.append(f"| Final question (7.9) | {tc(e['lines']['7.9'][0])}–{tc(e['lines']['7.9'][1])} ({e['lines']['7.9'][1]-e['lines']['7.9'][0]:.1f} s) | {tc(t['lines']['7.9'][0])}–{tc(t['lines']['7.9'][1])} ({t['lines']['7.9'][1]-t['lines']['7.9'][0]:.1f} s) |")
    o.append(f"| Season 2 card lands | {tc(e['s2_hit'])} | {tc(t['s2_hit'])} |")
    o.append(f"| Narration above music (speech regions) | {e['speech_to_music_db']} dB | {t['speech_to_music_db']} dB |")
    o += ['', 'Loudness for every master is −14 LUFS integrated, with true peak ≤ −0.9 dBTP.', '',
          '## Shorts', '', '| Short | English | Telugu |', '|---|---|---|']
    for k in NEW:
        a = next(x for x in S['en'] if x['short'] == k); b = next(x for x in S['te'] if x['short'] == k)
        o.append(f"| {k} | {mmss(a['total'])} ({a['total']:.1f} s) | {mmss(b['total'])} ({b['total']:.1f} s) |")
    o += ['', 'Every Short is under 3:00, and the story sets the length. The music tail after the last word is 1.1 s.', '',
          '## Mix', '- **Voice:** pro chain, on top. Music is ducked 65 % under speech, so narration sits about 22 dB above the music across both films and all Shorts.',
          '- **Music map:**',
          '  - Cold open: *Beneath the Rising Current*.',
          '  - Ch 1–3: *Where the River Bends*.',
          '  - Ch 4–5: *Before the World Wakes*.',
          '  - Ch 6: *Beneath the Rising Current*, from a later section.',
          '  - Ending: *The Quiet Meridian*.',
          '- **Season 2 ending, darker and more suspenseful:**',
          '  - *The Quiet Meridian* is pitched down 2 semitones, with the top end rolled off above 2.6 kHz, the mids scooped and the low end lifted.',
          '  - A distant boom and a slow heartbeat sit under the question.',
          '  - A synth riser runs into the impact on the card.',
          '- **Structural SFX (real library files only):**',
          '  - Chapter cards: air woosh, then a distant boom on the card.',
          '  - Big reveals: a low knock.',
          '  - Cold open: wind bed.',
          '  - Scene-level SFX follow once the picture is locked.',
          '- **QC:**',
          '  - All 89 EN film lines and 13 EN Short pickups were checked with Whisper; no missing or garbled words. "23 June 1757" is read as "June 23, 1757".',
          '  - TE take lengths were checked against the timing model; there are no truncations or long dead air (the longest internal pause is 0.7 s).', '',
          '## Files (out/)',
          '- `GS_S1_film_EN.mp3` / `_TE.mp3`: full mix.',
          '- `*_voice.wav`: narration stem.',
          '- `GS_S1_S1…S6_{EN,TE}.mp3`: Short mixes.',
          '- `timeline_{en,te}.json`: every line\'s start and end.',
          '- `shorts_{en,te}.json`: Short segment marks.']
    open(f'{V}/recording_report.md', 'w').write('\n'.join(o) + '\n')


# ------------------------------------------------------------------ shorts cut plans
def text_of(lang, i):
    if i in ROWS: return ROWS[i][lang]
    return JOBS.get((lang, i), '')


def shorts_plan():
    o = ['# Golden Sparrow S1: the six Short cut plans (final, from the recorded audio)', '',
         'Each Short reuses the film\'s recorded lines, with new pickups recorded for its hook, bridge and tease.',
         '- **Picture:** reuse the film shot from "Film tc". For a new pickup, use the visual noted.',
         '- **Format:** 9:16 reframe.',
         '- **Link to the film:** links in a Short\'s description or comments are not clickable. Publish the full film first, then set each Short\'s **Related Video** in YouTube Studio to the film in the same language. That puts a clickable link under the channel handle, and it is what "The full film is linked" refers to.',
         '- **Subtitles:** the Text column is the complete approved line. Build captions from the recorded script text (`tools/jobs.json` / `script.md`), never from summaries.',
         '- **S4:** the tease starts at "Next: who showed Vasco da Gama the way?". Its first sentence repeated 4.11 and has been trimmed from the audio, with no re-recording.',
         '- **Ending:** the music tail ends 1.1 s after the last word, and there are no long music-only tails.', '']
    for k in NEW:
        for lang in ('en', 'te'):
            s = next(x for x in S[lang] if x['short'] == k)
            o += [f"## {k} · {'English' if lang == 'en' else 'Telugu'} · **{mmss(s['total'])}** ({s['total']:.1f} s)", '',
                  '| # | Short tc | Line | Source | Film tc | Text |', '|---|---|---|---|---|---|']
            for n, (i, a, b) in enumerate(s['segments'], 1):
                film = T[lang]['lines'].get(i)
                src = 'film reuse' if film else ('NEW pickup · bridge' if i.startswith('B') else ('NEW pickup · hook' if i.endswith('_hook') else 'NEW pickup · tease'))
                ftc = f"{tc(film[0])}–{tc(film[1])}" if film else '—'
                txt = re.sub(r'\*\*', '', text_of(lang, i)).replace('⏸', '·').replace('|', '/')
                o.append(f"| {n} | {tc(a)}–{tc(b)} | {i} | {src} | {ftc} | {txt} |")
            o.append('')
    o += ['### Visuals for the new pickups',
          '- **S1 tease:** a banned stamp on a chintz fashion plate, as in 2.10.',
          '- **S2 B2 bridge:** the hands montage from 2.1.',
          '- **S2 tease:** the Machilipatnam pin on the master map.',
          '- **S3 hook:** the Tavernier plate, then a cut to bales.',
          '- **S3 B3:** the 3.9 split screen, ending on the loom.',
          '- **S3 tease:** the clerk\'s ledger from 3.11.',
          '- **S4 hook:** the 1.4 bars, then the 4.1 empty bowl.',
          '- **S4 tease:** the 5.2 ship and a pilot "?".',
          '- **S5 hook:** the Cantino planisphere, then the busy-ocean route lines from 5.3.',
          '- **S5 tease:** the 5.10 cannon → bow.',
          '- **S6 hook:** the Company arms, then the Plassey throne cushion from 7.3.',
          '- **S6 B6:** silver chest (6.6) → revenue ledger → diwani scroll (7.5).',
          '- **S6 tease:** the Season 2 card.']
    open(f'{V}/shorts_cut_plans.md', 'w').write('\n'.join(o) + '\n')


# ------------------------------------------------------------------ visual asset requirements
def klass(v):
    c = []
    if '[DRAM]' in v or '(DRAM)' in v or 'AI still' in v or 'AI reconstruction' in v: c.append('ILLUS')
    if re.search(r'[Mm]ap', v): c.append('MAP')
    if re.search(r'chip|card|[Tt]imeline|diagram|bars|Flow|tag|stamp "|word cards|Split', v): c.append('GFX')
    if re.search(r'\(PD|PD\)|PD,|Met |Met\)|OA|CC0|Rijksmuseum|Cantino|engraving|print \(PD', v): c.append('ARCHIVE')
    if re.search(r'licensed photo|licence-confirmed', v): c.append('LICENSED')
    if not c: c.append('BROLL')
    return c


LBL = {'ILLUS': 'Original illustration (in-house AI, our style bible)', 'MAP': 'Master map animation (in-house)',
       'GFX': 'Motion graphics / on-screen text', 'ARCHIVE': 'Public-domain / open-access archive image',
       'LICENSED': 'Licensed photo or image (rights must be confirmed before use)', 'BROLL': 'Atmos b-roll (Pexels or in-house AI)'}


def rights(v):
    r = []
    if 'Met 1982.66' in v: r.append('✅ Met OA, public domain')
    if 'to select' in v: r.append('⏳ select an OA object')
    if 'licence-confirmed' in v or 'licensed photo' in v: r.append('⏳ confirm licence')
    if 'date to confirm' in v: r.append('⏳ confirm date')
    if 'if located' in v: r.append('⏳ locate CC0 view, else illustrate')
    if 'NOT' in v: r.append('🚫 restricted image excluded')
    if re.search(r'\(PD', v) and not r: r.append('✅ PD, log the source URL')
    if 'only if verified' in v: r.append('⏳ fine amount stays off screen until Keay p.372 is checked')
    return '; '.join(r) or 'in-house'


def visual_plan():
    e, t = T['en']['lines'], T['te']['lines']
    o = ['# Golden Sparrow S1: scene-by-scene visual asset requirements', '',
         'Timecodes are measured from the recorded narration.',
         '- **Shots:** at least one new shot every ~5 s ("Shots" = minimum shots for the longer of the two languages).',
         '- **One shared visual master:** EN and TE use the same shots. TE simply holds each shot longer, with Telugu labels on the maps and cards.',
         '- **Asset classes:**']
    o += [f'  - **{k}** = {v}' for k, v in LBL.items()]
    o += ['', '## Two edits of one visual system',
          'Characters, style, map assets and master illustrations are shared. EN and TE are **separate timelines**, so each picture matches its own narration:',
          '- **EN only:** 1.4e (China bar, "≈ half"), 2.15 (route lines plus the calico/chintz word cards), 4.4 (land-survey miniature), 5.9 (spice route dims, Cape route lights), and the Madras/Bombay footholds in 7.5.',
          '- **TE only:** 2.7 (Kalamkari map: Srikalahasti, Machilipatnam, Pedana), 3.4 (Malkibharama, the Qutb Shahi tombs and a Telugu manuscript), 3.10 (Mughal colour floods Golconda), 4.3 (Hampi and the "దేశ భాషలందు తెలుగు లెస్స" verse), 4.7 (Madanna and Akkanna), 5.4 (Roman coin, Telugu-region pin), 6.11 (coastal Andhra French blue, 1753) and 7.4 (Machilipatnam 1759).',
          '- **Different prop:** F2.1/F2.2 shows a Mughal silver rupee in EN and a Golconda gold pagoda (hun) in TE, so the coin macro is two separate assets.',
          '- **Map labels:** all on-screen text is Telugu in the TE edit.',
          '', '## Style bible (applies to every in-house illustration)',
          '- **Look:** painterly, warm, documentary realism. Late-17th-century Coromandel coast.',
          '- **Light and palette:** lamp-light interiors; madder-red, indigo and turmeric accents on black-soil earth tones.',
          '- **Recurring cast:** Anna (about 12, kurta) and Chelli (about 8, langa voni). Keep the same faces every time; generate a character sheet first.',
          '- **Recurring props:** Ammamma\'s trunk, the kalamkari cloth (Rama, Sita, Lakshmana), the coin, and the folded map.',
          '- **Tagging:** every dramatized shot is tagged "DRAMATIZED RECONSTRUCTION" the first time it appears in each chapter.', '']
    cur = None; tot = {k: 0 for k in LBL}; todo = []
    for r in L:
        i = r['id']; sec = section(i)
        if sec != cur:
            cur = sec; o += ['', f'## {CHAP.get(sec, sec)}', '', '| ID | EN tc (dur) | TE tc (dur) | Shots | Visual | Class | Rights / status | Short |', '|---|---|---|---|---|---|---|---|']
        de = (e[i][1] - e[i][0]) if i in e else 0; dt = (t[i][1] - t[i][0]) if i in t else 0
        en_s = f"{tc(e[i][0])} ({de:.1f}s)" if i in e else '— (TE only)'
        te_s = f"{tc(t[i][0])} ({dt:.1f}s)" if i in t else '— (EN only)'
        shots = max(1, math.ceil(max(de, dt) / 5.5))
        cl = klass(r['vis'])
        for c in cl: tot[c] += shots if c in ('ILLUS', 'BROLL') else 1
        rt = rights(r['vis'])
        if '⏳' in rt: todo.append(f"- **{i}:** {rt.replace('⏳ ', '')}. ({r['vis'][:90]}…)")
        sh = ', '.join(k for k, p in NEW.items() if any(x.split(':')[0] == i for x in p['reuse']) or p['hook'][0] == f'REUSE:{i}')
        o.append(f"| {i} | {en_s} | {te_s} | {shots} | {r['vis'].replace('|', '/')} | {' + '.join(cl)} | {rt} | {sh} |")
    o += ['', '## Totals (approximate)', '']
    o += [f"- **{LBL[k]}:** about {v} {'shots' if k in ('ILLUS', 'BROLL') else 'scenes'}" for k, v in tot.items()]
    o += ['', '## Still to clear before the render', ''] + todo
    o += ['', '## Release blockers (not visual)',
          '- **Music Content ID:** every Short is over 1:00, and a Short of 1–3 min with an active Content ID claim can be blocked worldwide. Before release:',
          '  - Have proof of permission on file for all four tracks.',
          '  - Upload private test renders and check YouTube Studio\'s copyright check.',
          '  - Swap any claimed track.',
          '- **Listening QA:** a native-speaker listening pass on the TE film and Shorts, plus an EN pass, before publishing.',
          '- **Rights:** none of the ⏳ items above enter the final edit until the permission is documented; otherwise replace them with a PD alternative or an original illustration.']
    o += ['', '## Sounds to add (please upload to `sfx/` if you have them)',
          '- **Loom shuttle / pit-loom clack (PRIORITY):** the season\'s signature motif, for the cold open (0.1), 2.3 and the end card. A real recording is needed.',
          '- **Harbour ambience** (gulls, rigging, surf): 3.3 and 4.11.',
          '- **Ship creak and sail flap:** 5.2 and 5.5.',
          '- **Quill on paper:** 2.8, 3.11 and 4.8. Until then, the library `scribble` stands in.',
          '- **Distant musket or cannon volley:** 7.2 and 7.4. Keep it subtle.',
          'Everything else uses the existing library: woosh, boom, riser, knock, coins, paper, map_unfold, stamp, heartbeat and wind.']
    open(f'{V}/visual_asset_requirements.md', 'w').write('\n'.join(o) + '\n')


rec_report(); shorts_plan(); visual_plan()
print('ok')
