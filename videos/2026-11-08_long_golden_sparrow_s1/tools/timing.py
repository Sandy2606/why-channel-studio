import re, json, sys
sys.path.insert(0, '/home/claude/gs')
from lines import L

# Speaking rates measured from 509 past ElevenLabs takes in voice_lib (raw): EN 2.63 words/s, TE 10.82 chars/s.
# Long-form Pace Model tempo 1.06 applied.
TEMPO = 1.06
EN_WPS = 2.63 * TEMPO
TE_CPS = 10.82 * TEMPO

def clean(t):
    return re.sub(r'\*\*', '', t)

def en_words(t):
    t = clean(t).replace('⏸', ' ')
    n = 0
    for w in t.split():
        core = re.sub(r'[^\w,]', '', w)
        if re.fullmatch(r'1[0-9]{3}s?', core): n += 3          # years
        elif re.fullmatch(r'[0-9]{1,3}(,[0-9]{3})+', core): n += 2   # 3,000
        elif re.fullmatch(r'[0-9]+', core): n += 1.6
        else: n += 1
    return n

def te_chars(t):
    t = clean(t).replace('⏸', '')
    extra = 0
    for m in re.findall(r'[0-9][0-9,]*', t):
        d = m.replace(',', '')
        extra += 16 if len(d) == 4 else (8 if d.endswith('000') else 6 * len(d) / 2 + 2)
    t = re.sub(r'[0-9,]+', '', t)
    # Latin words inside Telugu (Angus Maddison, cotton) read at the EN rate: convert to char-equivalents
    lat = re.findall(r'[A-Za-z]+', t)
    lat_s = len(lat) / EN_WPS
    t = re.sub(r'[A-Za-z]+', '', t)
    chars = len(re.sub(r"[\s\.,:;!?'…\-–—‘’“”()]", '', t)) + extra
    return chars / TE_CPS + lat_s

def internal(t, role):
    beat = 0.45 if role in ('Q', 'PUNCH') else 0.35
    if role in ('HOOK', 'LIST'): beat = 0.25
    return t.count('⏸') * beat + t.count('…') * 0.30 + clean(t).count(',') * 0.06 + clean(t).count(':') * 0.12

def spoken(t, lang, role):
    if not t: return 0
    s = en_words(t) / EN_WPS if lang == 'en' else te_chars(t)
    return s + internal(t, role)

def gap_after(cur, nxt):
    if nxt is None: return 0
    g = 0.18
    if cur['id'] == '0.5': return 2.6          # title card after the cold open
    if cur['role'] == 'HOOK': g = 0.12
    if cur['en'].rstrip().endswith('?') or cur['en'].rstrip().endswith('?**'): g = 0.45
    if nxt['role'] == 'PUNCH': g = max(g, 0.50)
    if nxt['spk'] != cur['spk']: g = max(g, 0.28)
    if nxt['role'] == 'CHAP': g = 1.30
    if cur['role'] == 'CHAP': g = 0.60
    if nxt['id'].startswith('F'): g = max(g, 0.8)
    return g

# cinematic holds (music/visual only, seconds): after chapter cards and after big reveals
HOLD = {k: 2.0 for k in ('1.0','2.0','3.0','4.0','5.0','6.0')}
HOLD.update({k: 1.5 for k in ('1.5','2.14','3.9','4.10','5.8','6.12','7.3')})

def timeline(lang):
    rows = [x for x in L if (x['only'] in (None, lang)) and (x['en'] if lang == 'en' else x['te'])]
    t = 0; out = []
    for i, r in enumerate(rows):
        txt = r['en'] if lang == 'en' else r['te']
        d = spoken(txt, lang, r['role'])
        out.append(dict(id=r['id'], start=t, dur=d, end=t + d))
        t += d + gap_after(r, rows[i + 1] if i + 1 < len(rows) else None) + HOLD.get(r['id'], 0)
    return out, t + 4.0   # +end card hold

def fmt(s):
    m, s = divmod(s, 60); return f"{int(m):02d}:{s:04.1f}"

if __name__ == '__main__':
    for lang in ('en', 'te'):
        tl, total = timeline(lang)
        d = {x['id']: x for x in tl}
        co = d['0.5']['end']
        fin_start = d['7.1']['start']
        words = sum(en_words(r['en']) for r in L if r['only'] in (None, 'en') and r['en']) if lang == 'en' else None
        print(lang.upper(), 'total', fmt(total), '| cold open to title', fmt(co), '| final from', fmt(fin_start), 'len', round(total - fin_start, 1), 's', '| words', words)
        chap = [x for x in tl if x['id'].endswith('.0')]
        for c in chap: print('   ', c['id'], fmt(c['start']))
