import sys, json, re, collections
sys.path.insert(0, '/home/claude/gs'); sys.path.insert(0, '/home/claude/gs/plan')
from lines import L
from scenes import S
from assets import A
from shorts import NEW
OUT = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/why-channel-studio/videos/2026-11-08_long_golden_sparrow_s1/visual_production_plan.md'
T = {l: json.load(open(f'/home/claude/gs/out/timeline_{l}.json')) for l in ('en', 'te')}
SH = {l: json.load(open(f'/home/claude/gs/out/shorts_{l}.json')) for l in ('en', 'te')}
ROWS = {r['id']: r for r in L}; SC = {x['id']: x for x in S}
missing = [r['id'] for r in L if r['id'] not in SC]; assert not missing, missing
for x in S:
    for a in x['assets']: assert a in A, (x['id'], a)
def tc(s): m, s = divmod(s, 60); return f"{int(m):02d}:{s:04.1f}"
def mmss(s): m, s = divmod(round(s), 60); return f"{int(m)}:{int(s):02d}"
STY = {'CIN': 'Cinematic', 'MAP': 'Map', 'EVID': 'Evidence', 'DATA': 'Data', 'TITLE': 'Title', 'DLG': 'Frame story'}
CH = [('0', 'Cold open'), ('F1', 'Trunk scene'), ('1', 'Chapter 1 · Was India really that rich?'), ('2', 'Chapter 2 · The cloth the world wanted'),
      ('3', 'Chapter 3 · Golconda and Machilipatnam'), ('F2', 'Coin scene'), ('4', 'Chapter 4 · Who controlled the wealth?'), ('5', "Chapter 5 · Europe didn't discover India"),
      ('6', 'Chapter 6 · The company that came to trade'), ('7', 'Ending · Plassey → Season 2')]
def sec(i): return 'F1' if i.startswith('F1') else ('F2' if i.startswith('F2') else i.split('.')[0])
use = collections.defaultdict(list)
for x in S:
    for a in x['assets']: use[a].append(x['id'])
shorts_of = collections.defaultdict(list)
for k, p in NEW.items():
    for r in p['reuse']: shorts_of[r.split(':')[0]].append(k)
    if p['hook'][0].startswith('REUSE:'): shorts_of[p['hook'][0][6:]].append(k)

o = []; w = o.append
w('# The Golden Sparrow S1: visual production plan')
w('')
w('Approved motion-graphics system, applied to every line of the English and Telugu films and the six Shorts. Timecodes are measured from the final narration mixes.')
w('')
w('## 1. How the film moves (three visual languages)')
w('')
w('| Style | Used for | Motion | Count (scenes) |')
w('|---|---|---|---|')
cnt = collections.Counter(x['style'] for x in S)
w(f"| **Cinematic reconstruction** | People, workshops, ports, ships, battles | 2.5D depth parallax from a depth map, slow dolly, atmosphere (dust, mist, lamp flicker), wide → medium → close sequences | {cnt['CIN']} |")
w(f"| **Animated maps** | Kingdoms, trade routes, monsoon, the Company's advance, borders | One map system (Equal Earth world + regional maps, India's official outline), colour fields that change with the story, route lines that draw, camera that travels | {cnt['MAP']} |")
w(f"| **Evidence and data** | Documents, museum objects, dates, figures, flows | Document cards with a highlight sweep, the approved data kit (grid, counters, bars, people, flows), year rolls | {cnt['EVID'] + cnt['DATA']} |")
w(f"| Frame story and titles | Anna and Chelli, chapter cards, Season 2 card | Approved crops, parallax, title on the impact | {cnt['DLG'] + cnt['TITLE']} |")
w('')
w('**Each chapter has its own motion:**')
w('- **Ch 1:** Economic data, the approved proof-of-concept style.')
w('- **Ch 2:** Hands and processes: macro close-ups, step-by-step process strips, and document cards for the laws.')
w('- **Ch 3:** Port life: harbour parallax, ships and cargo, routes lighting up, and markets.')
w('- **Ch 4:** Systems: flow diagrams with moving coins. **The famine is restrained:** slow dissolves, no SFX hits and the music drops out.')
w('- **Ch 5:** The ocean: monsoon winds, routes, the 1498 landing, and journal quotes.')
w('- **Ch 6 and ending:** Documents, forts and the Company map growing step by step, then the battle in heavy, still air. No action-movie cutting.')
w('')
w('## 2. Rules carried from the approval')
w('- **Telugu graphics:** all labels are in natural Telugu, using the glossary in section 7. Numbers stay as international numerals. Only book titles (e.g. *The World Economy*) and the museum name stay in English.')
w('- **1700 vs 1950:** the two maps carry big labels in 9:16 (≥ 40 px), placed above the map:')
w('  - EN: "INDIAN SUBCONTINENT · c.1700" | "INDIA · 1950 (DIFFERENT TERRITORY)"')
w('  - TE: "భారత ఉపఖండం · సుమారు 1700" | "భారతదేశం · 1950 (వేరే భూభాగం)"')
w('- **Figures checked:** India 24.4 % of world GDP in 1700 and 4.2 % in 1950, population share 27.4 % in 1700, GDP per head $550 (1990 int. $). All are Maddison estimates.')
w('  - China 22.3 % and the UK 2.9 % (1700) come from the same tables. They are standard citations of Maddison 2001, Table B-20; I could not open the OECD PDF to re-read them this round, so a page check is noted in the source file.')
w('  - Geographic definitions: Maddison\'s 1700 "India" is the undivided subcontinent, and his 1950 figure is the Republic of India.')
w('- **Mobile safe areas (9:16, 1080×1920):**')
w('  - Keep key text inside x 70–900 and y 220–1500.')
w('  - Nothing important below y 1500 (Shorts title and description) or right of x 900 between y 900 and 1650 (like and share buttons).')
w('  - Minimum sizes: labels 34 px, source lines 28 px, territory labels 40 px. In 16:9: labels 26 px, sources 22 px.')
w('- **Sensitive scenes:**')
w('  - Caste (1.7): show the system, not ranked people.')
w('  - Child labour (3.7): keep it wide and distant.')
w('  - Famine (4.9–4.10): no bodies, slow fades, silence.')
w('  - Battle (7.2–7.3): no gore, labelled DRAMATIZED.')
w('  - Every reconstruction carries a "DRAMATIZED RECONSTRUCTION" tag the first time it appears in each chapter.')
w('- **Separate compositions:** 16:9 and 9:16 are laid out separately (maps, text, subject placement). The same art is reused, never just centre-cropped.')
w('')
# ---------------------------------------------------------------- scenes
w('## 3. Scene by scene')
w('')
w('Each scene lists:')
w('- **EN / TE timecodes:** from the final mixes.')
w('- **Picture and animation:** what is on screen and how it moves.')
w('- **Camera:** how the frame moves.')
w('- **Sync:** the narration cue that triggers each move.')
w('- **On-screen text:** in English and Telugu.')
w('- **Assets:** IDs from section 5.')
w('- **Licence:** where each asset comes from and its rights status.')
w('- **Reuse:** across languages, aspect ratios and Shorts.')
cur = None
for r in L:
    i = r['id']; x = SC[i]; c = sec(i)
    if c != cur:
        cur = c; w(''); w(f"### {dict(CH)[c]}"); w('')
    e = T['en']['lines'].get(i); t = T['te']['lines'].get(i)
    es = f"{tc(e[0])} ({e[1]-e[0]:.1f}s)" if e else '— (TE only)'; ts = f"{tc(t[0])} ({t[1]-t[0]:.1f}s)" if t else '— (EN only)'
    w(f"**{i}** · {STY[x['style']]} · EN {es} · TE {ts}")
    w(f"- **Picture:** {x['picture']}")
    if x['camera']: w(f"- **Camera:** {x['camera']}")
    if x['sync']: w(f"- **Sync:** {x['sync']}")
    if x['en'] or x['te']:
        w(f"- **On-screen text:**")
        if x['en']: w(f"  - EN: {x['en']}")
        if x['te']: w(f"  - TE: {x['te']}")
    lic = []
    for a in x['assets']:
        A_ = A[a]; lic.append(f"{a} ({ {'EXIST': 'have', 'GEN': 'generate free', 'PD': 'public domain/OA', 'CC': 'CC/free licence', 'BUILD': 'in-house'}[A_['kind']] })")
    w(f"- **Assets:** {', '.join(lic)}")
    reuse = ['the same art and motion in EN and TE (TE holds each shot longer, Telugu labels)' if not r['only'] else ('EN-only scene' if r['only'] == 'en' else 'TE-only scene')]
    reuse.append('9:16: ' + (re.sub(r'^9:16 ', '', x['vert']) or 'recomposed from the same layers'))
    if shorts_of.get(i): reuse.append('Shorts: ' + ', '.join(sorted(set(shorts_of[i]))))
    w(f"- **Reuse:**")
    for x_ in reuse: w(f"  - {x_}")
    if x['sens']: w(f"- **Care:** {x['sens']}")
    w('')
# ---------------------------------------------------------------- shorts
w('## 4. The six Shorts (9:16, separately composed)')
w('')
w('**Every Short:**')
w('- Burned-in captions from the approved script text, in the safe area.')
w('- The same scenes as the film, recomposed for 9:16.')
w('- A 1.1 s music tail.')
w('- The Related Video in YouTube Studio set to the film in the same language.')
w('')
w('New pickup lines need these visuals (otherwise every segment reuses its film scene):')
NEWVIS = {'S1_tease': 'Fashion plate in chintz, "BANNED" stamp (from 2.10)', 'S2_tease': 'Machilipatnam pin lights on the coast map',
          'S3_hook': 'Tavernier plate (PD02) → cut to bales in the hold (G13)', 'S3_tease': 'The port clerk\'s ledger (G14)',
          'S4_hook': 'The 24 % squares (from 1.4) → the empty bowl (G16)', 'S4_tease': 'The pilot "?" from 5.6',
          'S5_hook': 'Cantino planisphere (PD10) → busy ocean routes (from 5.3)', 'S5_tease': 'Cannon → bow (from 5.10)',
          'S6_hook': 'Company coat of arms (PD12) → the throne cushion (from 7.3)', 'S6_tease': 'The Season 2 card',
          'B2': 'Hands montage (from 2.1)', 'B3': '3.9 split ending on the loom (T6)', 'B6': 'Silver chest (G25) → revenue ledger → diwani painting (PD17)'}
for k in NEW:
    for lang in ('en', 'te'):
        s_ = next(z for z in SH[lang] if z['short'] == k)
        w(f"**{k} · {'English' if lang == 'en' else 'Telugu'} · {mmss(s_['total'])}**")
        segs = []
        for i, a_, b_ in s_['segments']:
            segs.append(f"{i} [{tc(a_)}] " + (f"NEW: {NEWVIS[i]}" if i in NEWVIS else f"film scene {i} ({STY[SC[i]['style']]}), 9:16 layers"))
        w('')
        for x_ in segs: w(f"- {x_}")
        w('')
# ---------------------------------------------------------------- assets
w('## 5. Asset register')
w('')
w('| Kind | What it means | Count |')
w('|---|---|---|')
kc = collections.Counter(a['kind'] for a in A.values())
w(f"| EXIST | Already made and approved | {kc['EXIST'] + 1} |")
w(f"| GEN | New illustration, generated free by you in ChatGPT from the prompt pack (no ElevenLabs credits) | {kc['GEN']} |")
w(f"| PD | Public-domain / open-access museum or archive image; I download it and log the URL | {kc['PD'] - 1} |")
w(f"| CC | Creative Commons or Pexels photo; credited at the end | {kc['CC']} |")
w(f"| BUILD | Made in the motion-graphics pipeline; no outside rights | {kc['BUILD']} |")
w('')
for kind, title in (('EXIST', 'Have'), ('GEN', 'To generate (free, ChatGPT; ★ = attach the character sheet)'), ('PD', 'Public domain / open access'), ('CC', 'Creative Commons / Pexels'), ('BUILD', 'In-house builds')):
    w(f"### {title}")
    w('')
    w('| ID | Asset | Source | Status | Used in |')
    w('|---|---|---|---|---|')
    for a in A.values():
        if a['kind'] != kind: continue
        star = ' ★' if a['ref'] else ''
        w(f"| {a['id']}{star} | {a['desc']} | {a['source']} | {a['status']} | {', '.join(use.get(a['id'], [])) or '—'} |")
    w('')
w('**Credits:** none. Every new picture is generated free in ChatGPT. Everything else is public domain, Creative Commons, or built in-house.')
w('')
# ---------------------------------------------------------------- production order
w('## 6. Production order')
w('1. Telugu localisation and the 9:16 size and safe-area rules go into the shared graphics kit. This is done once and applies everywhere.')
w(f"2. The prompt pack v2 page for the {kc['GEN']} new illustrations: same phone workflow, with ★ shots using the character sheet.")
w('3. In parallel, I collect the public-domain, open-access and CC images and log each URL and licence in `credits.md`.')
w('4. I build the remaining maps: Coromandel coast, Indian Ocean, Deccan, and the Company map.')
w('5. Assemble chapter by chapter, render 16:9 and 9:16 in both languages, and run the QA stills sheet per chapter.')
w('6. Cut the six Shorts from the 9:16 film layers, adding burned-in captions.')
w('')
# ---------------------------------------------------------------- glossary
w('## 7. Telugu on-screen glossary (used by every graphic)')
w('')
GL = [('India (1700, undivided)', 'భారత ఉపఖండం'), ('India (1950)', 'భారతదేశం'), ('Britain', 'బ్రిటన్'), ('China', 'చైనా'), ('Pakistan', 'పాకిస్తాన్'), ('Bangladesh', 'బంగ్లాదేశ్'),
      ('Share of world output', 'ప్రపంచ ఉత్పత్తిలో వాటా'), ('Estimate(s)', 'అంచనా(లు)'), ('World average', 'ప్రపంచ సగటు'), ('Western Europe', 'పశ్చిమ యూరప్'),
      ('Income per person', 'ఒక్కొక్కరి సగటు ఆదాయం'), ('Different territory', 'వేరే భూభాగం'), ('Dramatized reconstruction', 'నాటకీయ పునఃసృష్టి'), ('Illustrative', 'ఉదాహరణ మాత్రమే'),
      ('Debated', 'చర్చనీయాంశం'), ('Chapter', 'అధ్యాయం'), ('c. (circa)', 'సుమారు'), ('Banned', 'నిషేధం'), ('Broker', 'దళారి'), ('Weaver', 'నేతగాడు'), ('Spinner', 'వడికేవాళ్లు'),
      ('Farmer / Landlord / State', 'రైతు / భూస్వామి / రాజ్యం'), ('Monsoon', 'రుతుపవనాలు'), ('Company', 'కంపెనీ'), ('Revenue', 'పన్నుల ఆదాయం'), ('Farman', 'ఫర్మానా')]
w('| English | Telugu |'); w('|---|---|')
for a_, b_ in GL: w(f"| {a_} | {b_} |")
w('')
w(f"*{len(S)} scenes · film EN {mmss(T['en']['total'])} / TE {mmss(T['te']['total'])}*")
open(OUT, 'w').write('\n'.join(o) + '\n')
print('ok', len(S), kc)
