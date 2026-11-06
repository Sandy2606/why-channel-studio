"""Golden Sparrow S1: assemble film + Shorts voice tracks from the recorded takes, at natural pace (no tempo change),
then mix with music (narration clearly on top) and structural SFX. Writes out/<lang>/... and out/timeline_<lang>.json.
python3 assemble.py [en|te] [film|shorts|all]"""
import sys, os, json, subprocess, numpy as np, soundfile as sf
sys.path.insert(0, '/home/claude/gs'); sys.path.insert(0, '/home/claude/why-channel-studio/pipeline/shorts')
from timing import L, gap_after, HOLD
from shorts import NEW
import proasm
SR = 48000
ST = '/home/claude/why-channel-studio'
CAT = json.load(open(f'{ST}/sfx/catalog.json'))
TAKE = '/home/claude/gs/rec/take'
OUT = '/home/claude/gs/out'
ROWS = {r['id']: r for r in L}


def load(p, ch=1, af=None):
    cmd = ['ffmpeg', '-v', 'error', '-i', p] + (['-af', af] if af else []) + ['-ar', str(SR), '-ac', str(ch), '-f', 'f32le', '-']
    a = np.frombuffer(subprocess.run(cmd, capture_output=True).stdout, np.float32).copy()
    return a if ch == 1 else a.reshape(-1, 2)


def trim(x, thr=-50):
    hop = 480; n = len(x) // hop
    db = 20 * np.log10(np.sqrt((x[:n * hop].reshape(n, hop) ** 2).mean(1)) + 1e-9); v = np.where(db > thr)[0]
    return x[max(0, v[0] * hop - 960):min(len(x), (v[-1] + 1) * hop + 2400)]


def fade(x, a=0.01, b=0.03):
    x = x.copy(); fa = int(a * SR); fb = int(b * SR); x[:fa] *= np.linspace(0, 1, fa); x[-fb:] *= np.linspace(1, 0, fb); return x


# S4 tease: drop its first sentence ("And the richest trade of all came by sea"), which repeats film line 4.11 right before it
TRIM_START = {('en', 'S4_tease'): 3.01, ('te', 'S4_tease'): 3.29}


def take(lang, i):
    x = load(f'{TAKE}/{lang}_{i}.mp3')
    if (lang, i) in TRIM_START: x = x[int(TRIM_START[(lang, i)] * SR):]
    return fade(trim(x))


def db(g): return 10 ** (g / 20)


def sfx(name, af=None):
    c = CAT[name]; return load(f'{ST}/sfx/{c["file"]}', 2, af), (c.get('hit_at') or 0.0)


def place(buf, x, t, g=1.0):
    i = int(t * SR)
    if i < 0: x = x[-i:]; i = 0
    n = min(len(x), len(buf) - i)
    if n > 0: buf[i:i + n] += x[:n] * g


EQ = 'equalizer=f=2200:t=q:w=1:g=-5,highshelf=f=6000:g=-5,lowpass=f=10000'
# music map: (track, start offset s, extra filter)
TRACK = {
    'open': ('beneath_the_rising_current', 8, ''),
    'A': ('where_the_river_bends', 0, ''),          # ch1-3: villages, cloth, port
    'B': ('before_the_world_wakes', 0, ''),         # ch4-5: wealth, ocean
    'C': ('beneath_the_rising_current', 40, ''),    # ch6: the Company
    # Season 2 ending: darker + more suspenseful, less melodic: down 2 semitones, top end rolled off
    'end': ('the_quiet_meridian', 20, ',asetrate=48000*0.8909,aresample=48000,lowpass=f=2600,equalizer=f=900:t=q:w=1.2:g=-4,bass=g=3:f=90'),
}


def music_src(key):
    tr, off, extra = TRACK[key]
    return load(f'{ST}/music/{tr}.mp3', 2, f'atrim=start={off},asetpts=PTS-STARTPTS,' + EQ + extra)


def lay_loop(buf, m, a, b, fin=1.5, fout=2.0):
    a, b = int(a * SR), min(len(buf), int(b * SR)); n = b - a
    if n <= 0: return
    reps = np.concatenate([m] * (n // len(m) + 1))[:n].copy()
    g = np.ones(n, np.float32); fi, fo = min(n, int(fin * SR)), min(n, int(fout * SR))
    g[:fi] = np.linspace(0, 1, fi); g[-fo:] = np.minimum(g[-fo:], np.linspace(1, 0, fo))
    buf[a:b] += reps * g[:, None]


def activity(voice):
    mono = np.abs(voice); hop = 480; n = len(mono) // hop
    env = mono[:n * hop].reshape(-1, hop).max(1); act = (env > 0.02).astype(np.float32)
    act = np.clip(np.convolve(act, np.ones(31) / 31, 'same') * 1.6, 0, 1)
    act = np.repeat(act, hop); return np.pad(act, (0, len(voice) - len(act)))[:len(voice)]


def finish(voice, music, fx, name, lufs=-14):
    voice = proasm.CHAIN(voice[None, :], SR)[0]
    act = activity(voice)
    music = music * (1 - 0.65 * act)[:, None]          # duck music 65 % while speaking
    fx = fx * (1 - 0.45 * act)[:, None]
    y = voice[:, None] + music + fx
    os.makedirs(os.path.dirname(name), exist_ok=True)
    sf.write('/tmp/claude-0/pre.wav', np.clip(y, -1, 1), SR)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', '/tmp/claude-0/pre.wav', '-af', f'loudnorm=I={lufs}:TP=-1.0:LRA=11', '-ar', '48000', name + '.wav'], check=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', name + '.wav', '-b:a', '192k', name + '.mp3'], check=True)
    sf.write(name + '_voice.wav', voice, SR)
    # narration-over-music margin, measured in speech regions
    sp = act > 0.9
    vr = 20 * np.log10(np.sqrt((voice[sp] ** 2).mean()) + 1e-9); mr = 20 * np.log10(np.sqrt((music[sp] ** 2).mean()) + 1e-9)
    return round(vr - mr, 1)


# ---------------------------------------------------------------- film
OPEN_GAPS = {'0.1': 0.55, '0.2': 0.40, '0.3': 0.45, '0.4': 0.60}
def film(lang):
    rows = [x for x in L if (x['only'] in (None, lang)) and (x['en'] if lang == 'en' else x['te'])]
    lead = 1.2; t = lead; segs = []; marks = {}
    for k, r in enumerate(rows):
        v = take(lang, r['id'])
        marks[r['id']] = [round(t, 2), round(t + len(v) / SR, 2)]
        segs.append((t, v))
        nxt = rows[k + 1] if k + 1 < len(rows) else None
        g = gap_after(r, nxt) + HOLD.get(r['id'], 0)
        if r['id'] in OPEN_GAPS: g = OPEN_GAPS[r['id']]   # the approved listening-test timing
        if r['id'] == '0.5': g = 0.9 + 3.0          # title sting + title card (approved test: sting 0.9 s after the question)
        t += len(v) / SR + g
    vend = marks['7.9'][1]
    hit = vend + 0.9                                   # Season 2 card lands on the impact
    total = hit + 5.0                                  # end card: 5 s, music fades under it
    N = int(total * SR)
    voice = np.zeros(N, np.float32)
    for st, v in segs: place(voice, v, st)
    chap = {r['id'][0]: marks[r['id']][0] for r in rows if r['role'] == 'CHAP'}
    music = np.zeros((N, 2), np.float32); fx = np.zeros((N, 2), np.float32)
    title = marks['0.5'][1] + 0.9
    # music sections
    lay_loop(music, music_src('open'), 0, title + 3.0, fin=0.6, fout=1.2)
    lay_loop(music, music_src('A'), chap['1'] - 1.0, chap['4'] + 0.4, fin=2.0, fout=1.6)
    lay_loop(music, music_src('B'), chap['4'] - 0.2, chap['6'] + 0.4, fin=1.5, fout=1.6)
    lay_loop(music, music_src('C'), chap['6'] - 0.2, marks['7.1'][0] + 0.3, fin=1.5, fout=1.8)
    lay_loop(music, music_src('end'), marks['7.1'][0] - 0.8, total, fin=2.0, fout=3.2)
    mg = np.full(N, 0.20, np.float32)
    # cold open sits lower, swells into the title; ending swells into the Season 2 card
    for a_, b_, g0, g1 in ((title - 0.4, title, 0.20, 0.42), (title, title + 3.0, 0.42, 0.42), (hit - 0.4, hit, 0.20, 0.40), (hit, total, 0.40, 0.40)):
        a, b = int(a_ * SR), int(b_ * SR); mg[a:b] = np.linspace(g0, g1, b - a)
    for c, s in chap.items():                         # chapter dip then swell; card lands on the boom
        a, b = int((s - 1.2) * SR), int((s + 1.8) * SR)
        mg[a:b] *= np.concatenate([np.linspace(1, 0.4, (b - a) // 2), np.linspace(0.4, 1.2, b - a - (b - a) // 2)])
    music *= mg[:, None]
    # structural SFX (scene-level SFX are added once the visual cut is locked)
    w, _ = sfx('wind_ambience'); w = w[int(6 * SR):int(6 * SR) + int(title * SR)]
    place(fx, w * np.linspace(0, 1, len(w))[:, None] ** 0.5, 0, db(-30))
    hb, h = sfx('heartbeat_slow'); place(fx, hb, marks['0.5'][0] - h - 0.15, db(-16))
    r_, h = sfx('riser'); place(fx, r_, title - h, db(-14))
    b_, h = sfx('boom_impact'); place(fx, b_, title - h, db(-6))
    for c, s in chap.items():
        wa, h = sfx('woosh_air'); place(fx, wa, s - 0.15 - h, db(-16))
        bd, h = sfx('boom_distant'); place(fx, bd, s - h, db(-12))
    for rid in ('1.5', '2.14', '3.9', '4.10', '5.8', '6.12', '7.3'):   # big reveals: low knock on the last word
        if rid in marks:
            k_, h = sfx('sub_knock'); place(fx, k_, marks[rid][1] - 0.05, db(-14))
    # ending: distant boom under the question, slow heartbeat, synth riser into the impact
    bd, h = sfx('boom_distant'); place(fx, bd, marks['7.9'][0] + 0.3 - h, db(-20))
    hb, h = sfx('heartbeat_slow'); place(fx, hb, marks['7.9'][0] - h - 0.2, db(-18))
    rs, h = sfx('riser_synth'); place(fx, rs, hit - h, db(-16))
    it, h = sfx('impact_trailer'); place(fx, it, hit - h, db(-7))
    name = f'{OUT}/{lang}/GS_S1_film_{lang.upper()}'
    margin = finish(voice[:N], music, fx, name)
    tl = dict(lang=lang, total=round(total, 2), lead=lead, title_hit=round(title, 2), s2_hit=round(hit, 2), chapters=chap, lines=marks,
              speech_to_music_db=margin)
    json.dump(tl, open(f'{OUT}/timeline_{lang}.json', 'w'), indent=1)
    return tl


# ---------------------------------------------------------------- shorts
SHORT_MUSIC = {'S1': 'A', 'S2': 'A', 'S3': 'A', 'S4': 'B', 'S5': 'B', 'S6': 'end'}


def short(lang, k):
    p = NEW[k]; ids = []
    h = p['hook'][0]
    ids.append(h[6:] if h.startswith('REUSE:') else f'{k}_hook')
    for rid in p['reuse']:
        if ':' in rid:
            rid, only = rid.split(':')
            if only != lang: continue
        if rid.startswith('B') or (rid in ROWS and ROWS[rid]['only'] in (None, lang) and (ROWS[rid]['en'] if lang == 'en' else ROWS[rid]['te'])):
            ids.append(rid)
    ids.append(f'{k}_tease')
    lead = 0.15; t = lead; segs = []; marks = []
    for n, i in enumerate(ids):
        v = take(lang, i)
        marks.append([i, round(t, 2), round(t + len(v) / SR, 2)]); segs.append((t, v))
        if n + 1 == len(ids): break
        r = ROWS.get(i, dict(id=i, role='EXP', en='', spk='NAR'))
        nx = ROWS.get(ids[n + 1], dict(id=ids[n + 1], role='EXP', en='', spk='NAR'))
        g = 0.22
        if i in ROWS and ids[n + 1] in ROWS: g = min(gap_after(r, nx), 0.6)
        if n == 0: g = 0.35                             # beat after the hook
        if ids[n + 1].endswith('_tease'): g = 0.45
        t += len(v) / SR + g
    vend = marks[-1][2]
    total = vend + 1.1                                  # no long music-only tail
    N = int(total * SR)
    voice = np.zeros(N, np.float32)
    for st, v in segs: place(voice, v, st)
    music = np.zeros((N, 2), np.float32); fx = np.zeros((N, 2), np.float32)
    lay_loop(music, music_src(SHORT_MUSIC[k]), 0, total, fin=0.3, fout=1.0)
    music *= 0.20
    bd, h = sfx('boom_distant'); place(fx, bd, lead + 0.05 - h + 0.44, db(-18))     # soft low hit under the hook
    if k == 'S6':
        m79 = next(m for m in marks if m[0] == '7.9')
        hb, h = sfx('heartbeat_slow'); place(fx, hb, m79[1] - h - 0.2, db(-18))
        it, h = sfx('impact_trailer'); place(fx, it, m79[2] + 0.35 - h, db(-10))
    name = f'{OUT}/{lang}/GS_S1_{k}_{lang.upper()}'
    margin = finish(voice[:N], music, fx, name)
    return dict(short=k, lang=lang, total=round(total, 2), segments=marks, speech_to_music_db=margin)


if __name__ == '__main__':
    langs = [sys.argv[1]] if len(sys.argv) > 1 and sys.argv[1] in ('en', 'te') else ['en', 'te']
    what = sys.argv[2] if len(sys.argv) > 2 else 'all'
    for lang in langs:
        if what in ('film', 'all'):
            tl = film(lang); print(lang, 'film', tl['total'], 'margin', tl['speech_to_music_db'])
        if what in ('shorts', 'all'):
            res = [short(lang, k) for k in NEW]
            json.dump(res, open(f'{OUT}/shorts_{lang}.json', 'w'), indent=1)
            for r in res: print(lang, r['short'], r['total'], 'margin', r['speech_to_music_db'])
