"""Golden Sparrow S1 - full film renderer (16:9). python3 film.py en|te [t0 t1 out.mp4] | stills | full"""
import sys, os, json, math, re, subprocess, functools
LANG = sys.argv[1]
sys.argv_saved = list(sys.argv)
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, '/home/claude/gs'); sys.path.insert(0, '/home/claude/gs/film3'); sys.path.insert(0, '/home/claude/gs/plan'); sys.path.insert(0, '/home/claude/gs/poc')
import flib as FL
FL.set_lang(LANG)
from flib import W, H, FPS, put, text, chip, eo, win, shade, INK, PAPER, GOLD, MUTED, RUST, TEAL
from lines import L
from scenes import S as SCENES
from plan_shots import SHOTS, MAPS
TL = json.load(open(f'/home/claude/gs/out/timeline_{LANG}.json')); M = TL['lines']
ROWS = {r['id']: r for r in L}; SC = {x['id']: x for x in SCENES}
ORDER = [r['id'] for r in L if r['id'] in M]
TE = LANG == 'te'
# poc (approved Chapter 1 data block), same language, landscape
_argv = sys.argv; sys.argv = ['poc', LANG, 'land']; import poc; sys.argv = _argv

# ---------------------------------------------------------------- phrase starts per line (pauses in the take)
SR = 48000
PH_CACHE = f'/home/claude/gs/film/cache/phrases_{LANG}.json'
def _load_ph():
    for _ in range(20):
        try: return json.load(open(PH_CACHE)) if os.path.exists(PH_CACHE) else {}
        except Exception: import time; time.sleep(0.3)
    return {}
PH = _load_ph()
def phrases(i):
    if i in PH: return PH[i]
    x = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', f'/home/claude/gs/rec/take/{LANG}_{i}.mp3', '-ar', str(SR), '-ac', '1', '-f', 'f32le', '-'], capture_output=True).stdout, np.float32)
    hop = 480; n = len(x) // hop; db = 20 * np.log10(np.sqrt((x[:n * hop].reshape(n, hop) ** 2).mean(1)) + 1e-9); v = np.where(db > -50)[0]
    x = x[max(0, v[0] * hop - 960):]; n = len(x) // hop
    db = 20 * np.log10(np.sqrt((x[:n * hop].reshape(n, hop) ** 2).mean(1)) + 1e-9); vo = db > -42
    gaps = []; s = None
    for k, b in enumerate(vo):
        if not b and s is None: s = k
        if b and s is not None:
            if k - s >= 12: gaps.append((k - s, k * hop / SR))
            s = None
    txt = ROWS[i]['te' if TE else 'en']; nb = txt.count('⏸')
    sel = sorted(g[1] for g in sorted(gaps, reverse=True)[:nb])
    PH[i] = [round(M[i][0], 2)] + [round(M[i][0] + g, 2) for g in sel]
    return PH[i]

# ---------------------------------------------------------------- timeline of shots
LEAD = 0.25
POC_END = poc.T1
def build():
    shots = []   # (t0, t1, spec, line_id)
    starts = {i: (0.0 if k == 0 else M[i][0] - LEAD) for k, i in enumerate(ORDER)}
    ends = {i: (starts[ORDER[k + 1]] if k + 1 < len(ORDER) else TL['total']) for k, i in enumerate(ORDER)}
    for i in ORDER:
        a, b = starts[i], ends[i]
        if i in ('1.4e', '1.5', '1.6'): continue
        sp = list(SHOTS[i])
        if i == '1.4': shots.append((a, POC_END, ('poc',), i)); continue
        if i == '1.7':
            rest = sp[1:]; a2 = POC_END; n = len(rest)
            for k, s_ in enumerate(rest): shots.append((a2 + (b - a2) * k / n, a2 + (b - a2) * (k + 1) / n, s_, i))
            continue
        if i == '0.5': b_title = TL['title_hit'] - 0.15; shots.append((a, b_title, sp[0], i)); shots.append((b_title, b, ('title', 1), i)); continue
        if i == '7.9': b_title = TL['s2_hit'] - 0.15; shots.append((a, b_title, sp[0], i)); shots.append((b_title, b, ('title', 2), i)); continue
        sp = [(s_[1] if not TE else s_[2]) if s_[0] == 'lang' else s_ for s_ in sp]
        n = len(sp); ph = phrases(i)
        cuts = None
        if n > 1 and len(ph) >= n:
            cuts = [a] + [ph[k] - LEAD for k in range(1, n)] + [b]
            if min(cuts[k + 1] - cuts[k] for k in range(n)) < 2.2: cuts = None
        if cuts is None: cuts = [a + (b - a) * k / n for k in range(n + 1)]
        for k, s_ in enumerate(sp): shots.append((cuts[k], cuts[k + 1], s_, i))
    return shots
SHOTLIST = build()
_tmp = PH_CACHE + f'.{os.getpid()}'; json.dump(PH, open(_tmp, 'w')); os.replace(_tmp, PH_CACHE)

# ---------------------------------------------------------------- overlays (on-screen text per line)
def scene_text(i):
    s = SC[i]['te' if TE else 'en'] if i in SC else ''
    if i in ('0.2', '4.6', '4.10', '7.3', '6.8b', '6.10', '6.13', '7.5', '5.10', '6.3', '6.5'): return ''
    if i == '4.4': return "AKBAR'S COURT · AKBARNAMA"
    if i == '6.4': return ('A MUGHAL FARMAN · AURANGZEB (r. 1658–1707) · NATIONAL MUSEUM, NEW DELHI' if not TE else 'ఒక మొఘల్ ఫర్మానా · ఔరంగజేబు (1658–1707) · నేషనల్ మ్యూజియం, న్యూఢిల్లీ')
    if i == '2.12': return ('IN FORCE FROM 25 DEC 1722 · EXCEPTIONS: MUSLINS, NECKCLOTHS, FUSTIANS, ALL-BLUE CALICO' if not TE else '25 డిసెంబర్ 1722 నుంచి అమలు · మినహాయింపులు: మస్లిన్, మెడగుడ్డలు, ఫస్టియన్, పూర్తి నీలం calico')
    if i == '7.2': return '23 JUNE 1757 · ~3,000 vs ~50,000' if not TE else '23 జూన్ 1757 · ~3,000 vs ~50,000'
    if i in ('2.2', '2.3', '2.6', '2.11', '2.13', '3.3', '3.9'): return ''
    if i in ('0.1', '0.5', '7.9', '1.0', '2.0', '3.0', '4.0', '5.0', '6.0', '1.4', '1.4e', '1.5', '1.6', '1.7', '2.8', '3.8', '5.10', '3.12'): return ''
    if s.startswith('small caption'): return ''
    return s
OVER = []
for i in ORDER:
    s = scene_text(i)
    if s:
        a = M[i][0] + 0.5; b = max(M[i][1] - 0.1, a + 3.0)
        OVER.append(('chip', a, b, s))
p01 = phrases('0.1')
OVER.append(('chip', M['0.1'][0] + 0.6, p01[-1] - 0.1, '1721 · BRITAIN BANS PRINTED COTTON' if not TE else '1721 · అచ్చు గుడ్డలపై బ్రిటన్ నిషేధం'))
OVER.append(('why', p01[-1] - 0.05, M['0.2'][0] + 0.3, 'WHY?' if not TE else 'ఎందుకు?'))

# DRAMATIZED tag: first appearance of an own illustration in each section
seen = set()
for (a, b, sp, i) in SHOTLIST:
    if sp[0] == 'st' and sp[1] in FL.ILLUS:
        sec = i.split('.')[0]
        if sec not in seen:
            seen.add(sec); OVER.append(('dram', a + 0.4, min(b, a + 4.0), 'DRAMATIZED RECONSTRUCTION' if not TE else 'నాటకీయ పునఃసృష్టి'))

# ---------------------------------------------------------------- graphics shots
CH_NUM = {1: ('CHAPTER ONE', 'మొదటి అధ్యాయం'), 2: ('CHAPTER TWO', 'రెండో అధ్యాయం'), 3: ('CHAPTER THREE', 'మూడో అధ్యాయం'), 4: ('CHAPTER FOUR', 'నాలుగో అధ్యాయం'),
          5: ('CHAPTER FIVE', 'ఐదో అధ్యాయం'), 6: ('CHAPTER SIX', 'ఆరో అధ్యాయం')}
def paper():
    return Image.fromarray(np.ascontiguousarray(poc.BG)).convert('RGBA')
def card(t, a, b, n):
    fr = paper(); txt = SC[f'{n}.0']['te' if TE else 'en'].split(' · ')
    title = txt[1] if len(txt) > 1 else ''; chipy = txt[2] if len(txt) > 2 else ''
    k1 = eo((t - a) / 0.6); k2 = eo((t - a - 0.4) / 0.7)
    put(fr, text(CH_NUM[n][1 if TE else 0], 'label', 34, GOLD), W / 2, H / 2 - 110, k1, 'cb', (1 - k1) * 12)
    d = ImageDraw.Draw(fr); wl = int(140 * k1); d.rectangle((W / 2 - wl, H / 2 - 92, W / 2 + wl, H / 2 - 89), fill=GOLD + (255,))
    put(fr, text(title, 'disp', 82 if not TE else 76, PAPER, glow=True, maxw=1500), W / 2, H / 2 - 60, k2, 'ct', (1 - k2) * 18)
    if chipy: put(fr, text(chipy, 'label', 30, MUTED), W / 2, H / 2 + 130, eo((t - a - 0.9) / 0.6), 'ct')
    for j in range(6):   # progress dots
        x = W / 2 - 75 + j * 30; on = j < n
        d.ellipse((x - 6, H - 120 - 6, x + 6, H - 120 + 6), fill=(GOLD if on else (70, 66, 80)) + (int(255 * k1),))
    return fr
def title(t, a, b, n):
    fr = Image.new('RGBA', (W, H), INK + (255,))
    k1 = eo((t - a) / 0.6); k2 = eo((t - a - 0.5) / 0.6)
    if n == 1:
        put(fr, text('THE GOLDEN SPARROW' if not TE else 'బంగారు పిచ్చుక', 'disp', 118 if not TE else 108, GOLD, glow=True), W / 2, H / 2 - 10, k1, 'cb')
        put(fr, text('SEASON 1' if not TE else 'సీజన్ 1', 'disp', 54, PAPER), W / 2, H / 2 + 20, k2, 'ct')
    else:
        put(fr, text('THE GOLDEN SPARROW · SEASON 2' if not TE else 'బంగారు పిచ్చుక · సీజన్ 2', 'disp', 88 if not TE else 80, GOLD, glow=True), W / 2, H / 2 - 10, k1, 'cb')
        put(fr, text('HOW A COMPANY BECAME AN EMPIRE' if not TE else 'ఒక కంపెనీ సామ్రాజ్యం ఎలా అయింది', 'disp' if not TE else 'label', 46, PAPER), W / 2, H / 2 + 24, k2, 'ct')
        if t > a + 2.0: put(fr, text('Season 1: the full story · Subscribe for Season 2' if not TE else 'సీజన్ 2 కోసం subscribe చేయండి', 'ui', 30, MUTED), W / 2, H - 120, eo((t - a - 2.0) / 0.6), 'cb')
    return fr
def textcard(t, a, b, en, te, prev=None):
    fr = paper()
    if prev is not None:
        bg = Image.fromarray(prev).filter(ImageFilter.GaussianBlur(18)).convert('RGBA'); dk = Image.new('RGBA', (W, H), INK + (170,)); bg.alpha_composite(dk); fr = bg
    k = eo((t - a - 0.2) / 0.7)
    parts = (te if TE and te else en).split(' · ')
    put(fr, text(parts[0], 'disp', 76 if not TE else 70, GOLD, glow=True, maxw=1500), W / 2, H / 2 - 20, k, 'cb', (1 - k) * 16)
    if len(parts) > 1:
        put(fr, text(' · '.join(parts[1:]), 'label', 36, PAPER, maxw=1500), W / 2, H / 2 + 20, eo((t - a - 0.7) / 0.6), 'ct')
    return fr
FLOW_N = [('FARMER', 'రైతు', 230, 420), ('COLLECTORS · LOCAL LORDS', 'వసూలుదారులు · స్థానిక పెద్దలు', 700, 420), ('STATE TREASURY', 'రాజ్య ఖజానా', 1200, 420),
          ('ARMIES · COURTS', 'సైన్యాలు · దర్బార్లు', 1650, 420), ('BANKERS', 'వడ్డీ వ్యాపారులు', 950, 760), ('FOREIGN MERCHANT → FARMAN', 'విదేశీ వ్యాపారి → ఫర్మానా', 1500, 760)]
def flow(t, a, b):
    fr = paper(); ph = phrases('4.6') + [b]
    show = [ph[0], ph[0] + 1.6, ph[1], ph[2], ph[3], ph[4] if len(ph) > 4 else ph[-2]]
    d = ImageDraw.Draw(fr)
    put(fr, text('FOLLOW THE MONEY' if not TE else 'డబ్బు వెనకే', 'label', 34, GOLD), 70, 90, eo((t - a) / 0.5))
    for k, (en, te, x, y) in enumerate(FLOW_N):
        kk = eo((t - show[k]) / 0.5)
        if kk <= 0: continue
        im = text(te if TE else en, 'label', 30, PAPER, maxw=360)
        bw, bh = im.width + 50, im.height + 34
        d.rounded_rectangle((x - bw / 2, y - bh / 2, x + bw / 2, y + bh / 2), 10, fill=(34, 32, 44, int(235 * kk)), outline=GOLD + (int(255 * kk),), width=3)
        put(fr, im, x, y, kk, 'cc')
        if 0 < k < 4:   # arrow from previous node + coins flowing
            x0 = FLOW_N[k - 1][2] + 150; x1 = x - 160
            d.line((x0, y, x1, y), fill=GOLD + (int(220 * kk),), width=4); d.polygon([(x1, y - 10), (x1 + 18, y), (x1, y + 10)], fill=GOLD + (int(220 * kk),))
            for c in range(4):
                f = ((t - show[k]) * 0.45 + c / 4) % 1
                cx = x0 + (x1 - x0) * f; d.ellipse((cx - 9, y - 30 - 9, cx + 9, y - 30 + 9), fill=(232, 190, 90, int(230 * kk)), outline=(140, 100, 30, int(230 * kk)))
        if k == 4:
            for tx in (230, 700, 1200, 1650):
                d.line((950, 760 - 40, tx, 420 + 40), fill=(120, 140, 178, int(160 * kk)), width=2)
    if t > ph[0] + 1.0 and len(ph) > 1:
        put(fr, text('OFTEN 1/3 TO 1/2 OF THE CROP · HISTORIANS\' ESTIMATE' if not TE else 'తరచుగా పంటలో 1/3 నుంచి 1/2 · చరిత్రకారుల అంచనా', 'label', 28, MUTED), 110, 520, eo((t - ph[0] - 1.0) / 0.5), 'lt')
    return fr


# ---------------------------------------------------------------- cue times (EN: word timestamps; TE: phrase + character position)
WORDS = json.load(open('/home/claude/gs/film/words_en_all.json')) if not TE else {}
CUE_MISS = set()
def cue(i, en, te=None, nth=0):
    if i not in M: return None
    if not TE:
        hits = [a for w, a, b in WORDS.get(i, []) if w.lower().strip('.,?!;:\'"').startswith(en.lower())]
        if len(hits) > nth: return hits[nth]
        CUE_MISS.add((i, en)); return M[i][0]
    txt = re.sub(r'\*\*', '', ROWS[i]['te']); parts = txt.split('⏸'); ph = phrases(i) + [M[i][1]]
    tok = te or en; pos = 0
    for k, p in enumerate(parts):
        j = p.find(tok)
        if j >= 0:
            a = ph[k]; b = ph[k + 1] - 0.35 if k + 1 < len(ph) else M[i][1]
            return a + (b - a) * j / max(1, len(p.strip()))
    CUE_MISS.add((i, tok)); return M[i][0]

# --- dyeing steps (2.6)
DYE = [('MORDANT', 'మోర్డెంట్', (70, 64, 60), 'mordants', 'పదార్థాలతో'), ('RED · CHAY ROOT', 'ఎరుపు · చిరివేరు', (170, 50, 40), 'reds', 'ఎరుపు'),
       ('BLUE · INDIGO', 'నీలం · నీలిమందు', (40, 60, 140), 'blue', 'నీలం'), ('WAX RESIST', 'మైనం', (232, 222, 190), 'wax', 'మైనం')]
def dye_overlay(fr, t, a, b):
    xs = 120; y = H - 150; k_all = min(1.0, (b - t) / 0.4)
    shade(fr, (60, y - 70, W - 60, y + 70), int(140 * k_all), 30)
    cues = [cue('2.6', d[3], d[4]) for d in DYE]
    w_ = (W - 240) / 4
    d = ImageDraw.Draw(fr)
    for n, (en, te, col, *_r) in enumerate(DYE):
        k = eo((t - cues[n] + 0.1) / 0.5) * k_all
        if k <= 0: continue
        x = xs + n * w_
        d.rounded_rectangle((x, y - 30, x + 60, y + 30), 8, fill=col + (int(255 * k),), outline=GOLD + (int(255 * k),), width=2)
        put(fr, text(f'{n + 1}', 'num', 30, PAPER if n < 3 else (40, 30, 20)), x + 30, y, k, 'cc')
        put(fr, text(te if TE else en, 'label', 32, PAPER, maxw=int(w_ - 90)), x + 78, y, k, 'lc')
        if n < 3:
            d.line((x + w_ - 40, y, x + w_ - 14, y), fill=GOLD + (int(200 * k),), width=3)

# --- textile-ban timeline (2.11-2.13)
BAN = [(1680, 'c.1680 · OUR CLOTH', 'సుమారు 1680 · మన గుడ్డ', ('2.11', None, None)),
       (1686, '1686 · FRANCE BANS PRINTED CALICOES', '1686 · ఫ్రాన్స్ నిషేధం', ('2.11', 'France', '1686')),
       (1700, '1700 · ENGLAND: NOT FOR HOME USE · RE-EXPORT ALLOWED', '1700 · ఇంగ్లాండ్: దేశంలో వాడకూడదు · మళ్లీ ఎగుమతి సరే', ('2.11', '1700', '1700')),
       (1721, '1721 ACT · IN FORCE 25 DEC 1722', '1721 చట్టం · 25 డిసెంబర్ 1722 నుంచి', ('2.12', '1721', '1721')),
       (1774, '1774 · REPEALED', '1774 · రద్దు', ('2.13', '1774', '1774'))]
def ban_cue(c):
    i, en, te = c
    if i not in M: return 1e9
    return M[i][0] - 0.3 if en is None else cue(i, en, te)
def ban_timeline(fr, t, y, x0, x1, mini=False, alpha=1.0):
    d = ImageDraw.Draw(fr); X = lambda yr: x0 + (yr - 1670) / (1785 - 1670) * (x1 - x0)
    d.line((x0, y, x1, y), fill=(120, 116, 130, int(255 * alpha)), width=3 if not mini else 2)
    for yr in range(1680, 1781, 20):
        d.line((X(yr), y - 6, X(yr), y + 6), fill=(120, 116, 130, int(255 * alpha)), width=2)
        if not mini: put(fr, text(str(yr), 'small', 22, MUTED), X(yr), y + 14, alpha, 'ct')
    c1721 = ban_cue(BAN[3][3]); c1774 = ban_cue(BAN[4][3])
    if t > c1721 + 0.6:     # in-force bar 1722 -> 1774
        k = eo((t - c1721 - 0.6) / 1.2); xe = X(1722) + (X(min(1774, 1722 + 52 * (1 if t > c1774 else 0.75))) - X(1722)) * k
        d.rectangle((X(1722), y - 7, xe, y + 7), fill=RUST + (int(220 * alpha),))
    for n, (yr, en, te, c) in enumerate(BAN):
        tc = ban_cue(c); k = eo((t - tc) / 0.5) * alpha
        if k <= 0: continue
        x = X(yr); r = 9 if not mini else 6
        d.ellipse((x - r, y - r, x + r, y + r), fill=(GOLD if n else PAPER) + (int(255 * k),))
        if not mini:
            up, yy = [(True, y - 40), (False, y + 50), (True, y - 150), (False, y + 160), (True, y - 40)][n]
            d.line((x, y - (r if up else -r), x, yy + (8 if up else -8)), fill=GOLD + (int(160 * k),), width=2)
            put(fr, text(te if TE else en, 'label', 32, PAPER, maxw=520), min(max(x, 330), W - 330), yy, k, 'cb' if up else 'ct', (1 - k) * (10 if up else -10))
def bantl_card(t, a, b):
    fr = paper()
    put(fr, text('BANNING A CLOTH' if not TE else 'ఒక గుడ్డపై నిషేధం', 'label', 34, GOLD), 120, 150, eo((t - a) / 0.5))
    ban_timeline(fr, t, H / 2 + 20, 140, W - 140)
    return fr

# --- Company chronology bar (Chapter 6 -> 7.5)
CHRONO = [(1600, '1600 · CHARTER', '1600 · charter', ('6.2', '1600', '1600')), (1612, '1612 · SWALLY', '1612 · స్వాలీ', ('6.3', '1612', '1612')),
          (1639, '1639 · MADRAS', '1639 · మద్రాసు', ('6.5', '1639', '1639')), (1680, 'c.1680 · OUR CLOTH SOLD', 'సుమారు 1680 · మన గుడ్డ అమ్మకం', ('6.7', '1680', '1680')),
          (1686, '1686–90 · WAR WITH THE MUGHALS, LOST', '1686–90 · మొఘలులతో యుద్ధం, ఓటమి', ('6.8b', '1686', '1686')), (1717, '1717 · FARMAN', '1717 · ఫర్మానా', ('6.9', '1717', '1717')),
          (1745, '1740s–50s · CARNATIC WARS', '1740–50లు · యుద్ధాలు', ('6.10', '1740s', '1740')), (1753, '1753 · CIRCARS TO FRANCE', '1753 · సర్కారులు ఫ్రెంచ్ చేతికి', ('6.11', None, '1753')),
          (1756, '1756 · CALCUTTA SEIZED', '1756 · కలకత్తా స్వాధీనం', ('6.13', '1756', '1756')), (1757, '1757 · PLASSEY', '1757 · ప్లాసీ', ('7.2', '1757', '1757')),
          (1759, '1759 · MACHILIPATNAM', '1759 · మచిలీపట్నం', ('7.4', None, '1759')), (1764, '1764 · BUXAR', '1764 · బక్సర్', ('7.5', '1764', '1764')),
          (1765, '1765 · DIWANI', '1765 · దివానీ', ('7.5', '1765', '1765'))]
CHRONO = [c for c in CHRONO if c[3][0] in M and (c[3][1] is not None or TE)]
def chrono_cue(c):
    i, en, te = c; return cue(i, en or te, te)
import seqs
from plan_shots import P as PL_P
seqs.init(cue, TE, M, PL_P)
def mapshot(name):
    def f(t, a, b):
        spec = dict(MAPS[name]); d_ = b - a; res = lambda c: a + c * d_
        spec['pins'] = [(p[0], p[1], p[2], res(p[3])) + tuple(p[4:]) for p in spec.get('pins', [])]
        spec['routes'] = [(r[0], res(r[1])) + tuple(r[2:]) for r in spec.get('routes', [])]
        spec['glows'] = [g[:5] + (res(g[5]),) for g in spec.get('glows', [])]
        return FL.render_map(None, t, spec, a, b)
    return f
def shipsmap(i):
    base = MAPS['port_routes']; cs = [cue(i, 'Persia', 'Persia'), cue(i, 'Arabia', 'అరేబియా'), cue(i, 'Burma', 'బర్మా'), cue(i, 'Southeast', 'ఆగ్నేయాసియా')]
    spec = dict(box0=base['box0'], box1=base['box1'], pins=[('Machilipatnam',) + PL_P['Machilipatnam'] + (M[i][0] - 0.3,)],
                glows=[g[:5] + (cs[k] - 0.1,) for k, g in enumerate(base['glows'])],
                routes=[(r[0], cs[k] - 0.2, (120, 112, 96)) for k, r in enumerate(base['routes'])],
                ships=[(list(reversed(r[0])), cs[k], 3.4) for k, r in enumerate(base['routes'])], autoships=False)
    return lambda t, a, b: FL.render_map(None, t, spec, a, b)
VILLAGES = [(80.55, 16.05), (80.8, 16.2), (81.0, 16.42), (80.85, 16.65), (81.3, 16.62), (81.55, 16.72), (81.8, 16.8), (82.0, 16.98)]
def netmap(i):
    cw = cue(i, 'buyers', 'కొనుగోలుదారులను') + 0.3
    spec = dict(box0=(79.3, 83.4, 14.7, 18.3), box1=(79.6, 83.1, 15.0, 18.0), pins=[('Machilipatnam',) + PL_P['Machilipatnam'] + (cw - 0.6, 'd')],
                net=(PL_P['Machilipatnam'], VILLAGES, cw, 'WEAVING VILLAGES' if not TE else 'నేత గ్రామాలు'))
    return lambda t, a, b: FL.render_map(None, t, spec, a, b)
import fx2
_L = lambda en, te: te if TE else en
WORLD_ROUTES = [[(-8, 45), (-20, 15), (0, -5), (18, -35), (45, -28), (58, 0), (72, 10), (75.8, 11.25)], [(43, 13), (55, 13), (68, 17), (72.8, 21.2)],
                [(56.3, 27), (62, 23), (72.8, 21.2)], [(39.7, -3.2), (55, 2), (75.8, 11.25)], [(101, 3), (92, 8), (85, 13), (81.14, 16.17)],
                [(114, 22), (106, 10), (95, 6), (85, 12), (81.14, 16.17)]]
def worldships(i):
    c0 = cue(i, 'sailed', 'ప్రపంచం') - 0.6
    spec = dict(box0=(-25, 150, -40, 60), box1=(20, 130, -22, 44), routes=[(r, c0 + k * 0.15, (110, 104, 92)) for k, r in enumerate(WORLD_ROUTES)],
                ships=[(r, c0 + k * 0.15, 3.0) for k, r in enumerate(WORLD_ROUTES)],
                glows=[('', 79, 21, 9, (220, 170, 60), c0)], autoships=False)
    return lambda t, a, b: FL.render_map(None, t, spec, a, b)
def diwani_map():
    return mapshot('diwani')
OVER.append(('chip', M['0.2'][0] + 0.4, cue('0.2', 'Indian', 'పత్తి') - 0.3, 'Palampore · Coromandel Coast, 18th c. · The Met' if not TE else 'పలంపోర్ · కోరమాండల్ తీరం, 18వ శతాబ్దం · The Met'))
SUB_T = cue('3.12', 'subscribe', 'subscribe') if '3.12' in M else 0
import fx3
fx3.init(cue=cue, TE=TE, P=PL_P)
def mapshot2(name, draw_factory, extra=None):
    def f(t, a, b):
        spec = dict(MAPS[name]); d_ = b - a; res = lambda c: a + c * d_
        spec['pins'] = [(p[0], p[1], p[2], res(p[3])) + tuple(p[4:]) for p in spec.get('pins', [])]
        spec['routes'] = [(r[0], res(r[1])) + tuple(r[2:]) for r in spec.get('routes', [])]
        spec['glows'] = [g[:5] + (res(g[5]),) for g in spec.get('glows', [])]
        spec['arrows'] = [r[:4] + (res(r[4]), res(r[5])) for r in spec.get('arrows', [])]
        if extra: spec.update(extra)
        if draw_factory: spec['draw'] = draw_factory(spec)
        return FL.render_map(None, t, spec, a, b)
    return f
def london_draw(lab_cue=None, lab_txt=''):
    def fac(spec):
        def draw(out, d, V, tt):
            x, y = V(*PL_P['London']); fx3.glow(out, x, y, 80, (210, 210, 230), 1.0)
            if lab_cue and tt > lab_cue: fx3.lab(out, lab_txt, x, y - 70, eo((tt - lab_cue) / 0.4), 26, PAPER, 'cb')
        return draw
    return fac
def cutseq(parts):
    return lambda t, a, b: seqs.cuts(t, [(p(a, b) if callable(p) else p, fn) for p, fn in parts])
PR2 = dict(MAPS['port_routes']); PR2 = dict(PR2, box0=(-22, 125, -40, 40), box1=(-22, 125, -40, 40),
           routes=PR2['routes'] + [([PL_P['Machilipatnam'], (80, 5), (73, -8), (40, -36), (18, -36), (8, -20), (5, -2), (2, 5)], .7)],
           glows=PR2['glows'] + [('West Africa' if not TE else 'పశ్చిమ ఆఫ్రికా', 2, 9, 5, (120, 140, 178), .7)])
MAPS['port_routes_wa'] = PR2
def _sub_end(fr, t):
    if '7.9' not in M: return fr
    t0 = M['7.9'][1] + 0.3
    if t < t0: return fr
    import cairo, sys as _s; _s.path.insert(0, '/home/claude/why-channel-studio/pipeline/style_v2'); import cta_card
    sf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(sf); c.translate((W - 1080 * 1.25) / 2, 0); c.scale(1.25, 1.25)
    cta_card.draw(c, t, t0, 'yt', 'te' if TE else 'en', y=H * 0.72 / 1.25)
    buf = np.ndarray((H, W, 4), np.uint8, sf.get_data()); fr.alpha_composite(Image.fromarray(buf[..., [2, 1, 0, 3]].copy(), 'RGBA')); return fr
SUB_CORNERS = [M[i][0] + 0.4 for i in ('1.2', '2.9', '3.6', '4.4', '5.3', '6.6') if i in M]
import fx4
fx4.init(TE=TE, paper=paper)
SEQ = {'0.1': lambda t, a, b: fx2.s01(t, a, b, cue, _L), '0.2': lambda t, a, b: fx2.s02(t, a, b, cue, _L),
       '0.3': lambda t, a, b: fx2.s03(t, a, b, cue, _L, worldships('0.3')), '0.5': seqs.s05,
       '3.12': lambda t, a, b: fx2.subscribe(t, a, b, SUB_T, 'te' if TE else 'en'),
       '4.6': lambda t, a, b: fx2.flow2(t, a, b, cue, _L), '4.9': lambda t, a, b: fx2.s49(t, a, b, cue, _L), '4.10': lambda t, a, b: fx2.s410(t, a, b, cue, _L),
       '7.1': seqs.s71, '7.2': fx3.s72, '7.3': fx3.s73,
       '7.5': fx3.s75, '7.6': fx3.s76,
       '6.8b': fx3.s68b, '6.10': fx3.s610, '6.12': fx3.s612, '6.13': fx3.s613, '7.4': fx3.s74,
       '4.2': mapshot2('deccan', lambda sp: fx3.deccan_draw(cue('4.2', 'Thalikota', 'తళ్లికోట'), cue('4.2', 'Aravidu', 'ఆరవీడు'), cue('4.2', 'Deccan', 'గోల్కొండ'), cue('4.2', 'Mughal', 'మొఘల్'))),
       '6.3': lambda t, a, b: seqs.cuts(t, [(a, mapshot2('surat', lambda sp: fx3.surat_draw(cue('6.3', '1608', '1608'), cue('6.3', 'Jahangir', 'జహంగీర్'), cue('6.3', '1612', '1612'), cue('6.3', '1613', '1613'), 0), dict(autoships=False, box0=(62, 86, 16, 33), box1=(63, 85, 16.5, 32.5)))),
                                              ((cue('6.3', '1615', 'ఆమోదించాడు') - 0.3) if not TE else b - 2.4, seqs.still('PD13', (.5, .4), (.5, .42), 1.0, 1.12))]),
       '6.5': lambda t, a, b: seqs.cuts(t, [(a, mapshot2('madras', lambda sp: fx3.madras_draw(cue('6.5', '1611', '1611'), cue('6.5', '1639', '1639'), cue('6.5', 'Madras', 'మద్రాసు')))),
                                              (min(b - 1.6, cue('6.5', 'Madras', 'మద్రాసు') + 1.6), seqs.still('PD14', (.5, .5), (.5, .5), 1.0, 1.1))]),
       '6.7': lambda t, a, b: seqs.cuts(t, [(a, seqs.still('G26', (.45, .55), (.47, .55), 1.0, 1.08)),
                                              (cue('6.7', 'carried', 'లండన్‌కి') - 0.6, mapshot2('london_route', london_draw(cue('6.7', 'Thames', 'థేమ్స్'), _L('LONDON · THAMES WAREHOUSE', 'లండన్ · థేమ్స్ గోదాము')), dict(cargo='bale', shipflag=(200, 56, 48)))),
                                              (cue('6.7', 'open', 'విప్పారు') + 0.3, seqs.still('PD15', (.5, .5), (.5, .5), 1.0, 1.1))]),
       'F1.2': lambda t, a, b: seqs.cuts(t, [(a, seqs.still('T4', (.46, .5), (.46, .5), 1.0, 1.12)),
                                               (cue('F1.2', 'More', 'మూడు') - 0.2, mapshot2('london_route', london_draw(cue('F1.2', 'London', 'లండన్'), _L('LONDON', 'లండన్')), dict(cargo='bale')))]),
       '2.15': mapshot2('port_routes_wa', None, dict(cargo='bale')),
       '5.5': lambda t, a, b: seqs.cuts(t, [(a, mapshot2('monsoon', lambda sp: fx3.monsoon_draw(sp['arrows']))), (a + (b - a) * 0.72, seqs.still('CC05', (.5, .5), (.5, .5), 1.0, 1.08))]),
       '5.6': mapshot2('malindi', lambda sp: fx3.malindi_draw(cue('5.6', 'pilot', 'దారిచూపే'), cue('5.6', 'debate', 'చర్చిస్తున్నారు'))),
       '5.7': lambda t, a, b: seqs.cuts(t, [(a, seqs.still('PD11', (.5, .3), (.5, .4), 1.1, 1.25)),
                                              (cue('5.7', 'Two', 'ట్యూనిస్') - 0.2, lambda tt, s_, e_: fx3.encounter(tt, s_, e_, cue('5.7', 'What', 'ఎందుకొచ్చారు') - 0.3, cue('5.7', 'Christians', 'క్రైస్తవుల') - 0.3))]),
       '5.8': lambda t, a, b: seqs.cuts(t, [(a, seqs.still('G23', (.45, .5), (.47, .5), 1.0, 1.1)),
                                              (cue('5.8', 'Hats', 'టోపీలు') - 0.3, lambda tt, s_, e_: fx3.gifts(tt, s_, e_, [cue('5.8', w, tw) for w, tw in (('Hats', 'టోపీలు'), ('coral', 'పగడాలు'), ('sugar', 'చక్కెర'), ('honey', 'తేనె'))], cue('5.8', 'laughed', 'నవ్వారు')))]),
       '5.10': lambda t, a, b: fx3.cannons_vs_permission(t, a, b, cue('5.10', 'cannons', 'ఫిరంగులతో'), cue('5.10', 'politely', 'మర్యాదగా')),
       '7.9': lambda t, a, b: fx4.payoff(t, a, b, cue('7.9', 'permission', 'అనుమతి'), cue('7.9', 'taxes', 'పన్నులే')),
       '2.1': seqs.s21, '2.2': seqs.s22, '2.3': seqs.s23, '2.4': seqs.s24, '2.6': seqs.s26,
       '3.2': lambda t, a, b: seqs.s32(t, a, b, mapshot('golconda')),
       '3.3': lambda t, a, b: seqs.s33(t, a, b, shipsmap('3.3'), netmap('3.3'))}
CH_A = M['6.2'][0] - 0.2 if '6.2' in M else 1e9
CH_B = M['7.6'][0] - 0.4 if '7.6' in M else 0
def chrono_overlay(fr, t):
    if not (CH_A <= t <= CH_B): return
    al = min(1.0, (t - CH_A) / 0.6, (CH_B - t) / 0.5)
    x0, x1, y = 520, 1400, 52; X = lambda yr: x0 + (yr - 1595) / (1770 - 1595) * (x1 - x0)
    shade(fr, (x0 - 60, 10, x1 + 60, y + 70), int(110 * al), 25)
    d = ImageDraw.Draw(fr); d.line((x0, y, x1, y), fill=(140, 136, 150, int(220 * al)), width=2)
    for yr in (1600, 1650, 1700, 1750):
        put(fr, text(str(yr), 'small', 20, MUTED), X(yr), y - 10, al * 0.9, 'cb')
    cur = None
    for c in CHRONO:
        tc = chrono_cue(c[3])
        if t >= tc - 0.1: cur = c
        k = eo((t - tc + 0.1) / 0.5) * al
        if k <= 0: continue
        x = X(c[0]); d.ellipse((x - 5, y - 5, x + 5, y + 5), fill=GOLD + (int(255 * k),))
    if cur:
        tc = chrono_cue(cur[3]); k = eo((t - tc + 0.1) / 0.5) * al; x = X(cur[0])
        d.ellipse((x - 9, y - 9, x + 9, y + 9), outline=GOLD + (int(255 * k),), width=2)
        put(fr, text(cur[2] if TE else cur[1], 'label', 28, PAPER), min(max(x, x0 + 120), x1 - 120), y + 16, k, 'ct')

# --- split comparisons (2.5 faded/bright, 3.9 diamond/cloth)
def split(t, a, b, left, right, lab_l, lab_r, c_l, c_r, faded=False):
    u = min(max((t - a) / max(0.01, b - a), 0), 1)
    L_ = FL.still(left, u, 1.15, 1.25, .5, .5, .5, .5, 0.0, False); R_ = FL.still(right, u, 1.15, 1.25, .5, .5, .5, .5, 0.0, False)
    if faded:
        g = L_.astype(np.float32); l = g.mean(2, keepdims=True); g = l + (g - l) * 0.25; g = 70 + g * 0.65; L_ = np.clip(g, 0, 255).astype(np.uint8)
    out = np.zeros((H, W, 3), np.uint8); hw = W // 2
    kL = eo((t - c_l) / 0.6); kR = eo((t - c_r) / 0.6)
    out[:, :hw] = (L_[:, W // 4:W // 4 + hw] * (0.35 + 0.65 * kL)).astype(np.uint8)
    out[:, hw:] = (R_[:, W // 4:W // 4 + hw] * (0.25 + 0.75 * kR)).astype(np.uint8)
    fr = Image.fromarray(out).convert('RGBA'); d = ImageDraw.Draw(fr); d.rectangle((hw - 2, 0, hw + 2, H), fill=GOLD + (255,))
    put(fr, text(lab_l, 'label', 34, PAPER), hw / 2, 110, kL, 'ct'); put(fr, text(lab_r, 'label', 34, PAPER), hw + hw / 2, 110, kR, 'ct')
    return fr

# ---------------------------------------------------------------- frame
def render_shot(sh, t):
    a, b, sp, i = sh; u = min(max((t - a) / max(0.01, b - a), 0), 1)
    k = sp[0]
    if k == 'st':
        _, key, z0, z1, fx0, fy0, fx1, fy1, par, fit = sp
        return Image.fromarray(FL.still(key, u, z0, z1, fx0, fy0, fx1, fy1, par, fit)).convert('RGBA')
    if k == 'map':
        spec = dict(MAPS[sp[1]]); d_ = b - a
        res = lambda c: a + c * d_
        spec['pins'] = [(p[0], p[1], p[2], res(p[3])) + tuple(p[4:]) for p in spec.get('pins', [])]
        spec['routes'] = [(r[0], res(r[1])) + tuple(r[2:]) for r in spec.get('routes', [])]
        spec['glows'] = [g[:5] + (res(g[5]),) for g in spec.get('glows', [])]
        spec['arrows'] = [r[:4] + (res(r[4]), res(r[5])) for r in spec.get('arrows', [])]
        return FL.render_map(None, t, spec, a, b)
    if k == 'card': return fx4.chapter_card(t, a, b, sp[1], card)
    if k == 'title': return title(t, a, b, sp[1])
    if k == 'text': return textcard(t, a, b, sp[1], sp[2])
    if k == 'flow': return flow(t, a, b)
    if k == 'seq': return SEQ[sp[1]](t, a, b)
    if k == 'bantl': return bantl_card(t, a, b)
    if k == 'split25':
        return split(t, a, b, 'PD20a', 'PD20a', 'FADES IN THE WASH' if not TE else 'ఉతికితే పోయే రంగు', 'STAYS BRIGHT' if not TE else 'ఉతికినా పోని రంగు',
                     a + 0.3, (cue('2.5', "didn't", 'ఉతికినా') or a + 1.5) - 0.3, faded=True)
    if k == 'split39':
        return split(t, a, b, 'G11', 'G13', 'DIAMONDS · THE LEGENDS' if not TE else 'వజ్రాలు · కథలు', 'CLOTH · THE CARGO' if not TE else 'గుడ్డ · ఓడల సరుకు',
                     cue('3.9', 'Diamonds', 'వజ్రాలు') - 0.2, cue('3.9', 'Cloth', 'ఓడలు') - 0.2)
    if k == 'poc':
        fr = poc.base()
        for a_, b_, fn in poc.SC:
            if a_ <= t < b_: fn(fr, t)
        return fr
    raise ValueError(k)
XF = 0.45
def frame(t):
    idx = next((k for k, s in enumerate(SHOTLIST) if s[0] <= t < s[1]), len(SHOTLIST) - 1)
    sh = SHOTLIST[idx]; fr = render_shot(sh, t)
    if idx + 1 < len(SHOTLIST) and t > sh[1] - XF:
        nx = SHOTLIST[idx + 1]
        if nx[2][0] == 'title' or sh[2][0] == 'title':
            pass
        else:
            fr = Image.blend(fr, render_shot(nx, t), (t - (sh[1] - XF)) / XF)
    if idx + 1 < len(SHOTLIST) and SHOTLIST[idx + 1][2][0] == 'title':   # fade to black into a title
        k = eo((t - (sh[1] - 1.0)) / 1.0); fr = Image.blend(fr, Image.new('RGBA', (W, H), INK + (255,)), k) if k > 0 else fr
    if '2.6' in M and M['2.6'][0] <= t <= M['2.6'][1] + 0.6: dye_overlay(fr, t, M['2.6'][0], M['2.6'][1] + 0.6)
    if '2.12' in M and M['2.12'][0] - 0.25 <= t <= M['2.13'][0] - 0.25:
        shade(fr, (60, 30, W - 60, 140), 150, 25); ban_timeline(fr, t, 80, 160, W - 160, mini=True)
    if '0.4' in M and M['0.4'][0] <= t <= M['0.4'][1] + 0.4:
        fx2.ring_overlay(fr, t, cue('0.4', 'quarter', 'నాలుగో'), 0.24, 1560, 470, 150, '~1/4', _L('OF WORLD OUTPUT, 1700 · ONE ESTIMATE', 'ప్రపంచ ఉత్పత్తిలో, 1700 · ఒక అంచనా'))
    if '0.2' in M and M['0.2'][0] + 0.3 <= t <= cue('0.2', 'Indian', 'పత్తి') - 0.2:
        fx4.opening_lines(fr, t, M['0.2'][0] + 0.4, [_L('TODAY · MASS-PRODUCED FABRIC', 'ఈరోజు · యంత్రాలతో భారీగా తయారయ్యే గుడ్డ'), _L('1700 · WEEKS OF SKILLED HANDWORK', '1700 · వారాల తరబడి నైపుణ్యమైన చేతిపని')])
    if '0.3' in M and cue('0.3', 'cloth', 'గుడ్డ') <= t <= M['0.4'][0] + 3.2:
        fx4.opening_lines(fr, t, cue('0.3', 'cloth', 'గుడ్డ'), [_L('SPICES BROUGHT THEM EAST.', 'సుగంధ ద్రవ్యాలు వాళ్లను తూర్పుకు తెచ్చాయి.'), _L('INDIAN CLOTH BECAME THE BIG PRIZE.', 'భారత గుడ్డే పెద్ద బహుమతి అయింది.')], x=90, y=150)
    if '0.5' in M and cue('0.5', 'company', 'కంపెనీ') + 0.4 <= t <= M['0.5'][1]:
        fx4.typed(fr, _L('HOW DID TRADE TURN INTO RULE?', 'వ్యాపారం పాలనగా ఎలా మారింది?'), W / 2, H - 150, t, cue('0.5', 'company', 'కంపెనీ') + 0.4, cps=34, size=48, col=GOLD, maxw=1600, anchor='ct', bg=True)
    for t0_ in SUB_CORNERS: fr = fx3.sub_corner(fr, t, t0_, 'te' if TE else 'en')
    fr = _sub_end(fr, t)
    chrono_overlay(fr, t)
    for o in OVER:
        kind, a, b, s = o
        if not (a <= t <= b): continue
        if kind == 'chip': chip(fr, t, a, b, s, size=34 if not TE else 34, maxw=1300)
        elif kind == 'why':
            k = win(t, a, b, 0.25, 0.4); fr = Image.blend(fr, Image.new('RGBA', (W, H), INK + (255,)), 0.45 * k)
            put(fr, text(s, 'disp', 190, GOLD, glow=True), W / 2, H / 2, k, 'cc')
        elif kind == 'sub':
            k = win(t, a, b); im = text(s, 'label', 32, (255, 255, 255))
            d = ImageDraw.Draw(fr); x, y = W - 120, 110
            d.rounded_rectangle((x - im.width - 60, y - 34, x, y + 34), 34, fill=(200, 30, 30, int(235 * k))); put(fr, im, x - 30, y, k, 'rc')
        elif kind == 'dram':
            put(fr, text(s, 'small', 24, (225, 215, 200)), 60, 50, win(t, a, b) * 0.9)
    return FL.finish(np.asarray(fr.convert('RGB')), t)

def render(t0, t1, out):
    ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                           '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '21', '-maxrate', '14M', '-bufsize', '28M', '-pix_fmt', 'yuv420p', '-g', '60', out], stdin=subprocess.PIPE)
    f0, f1 = int(round(t0 * FPS)), int(round(t1 * FPS))
    for f in range(f0, f1):
        ff.stdin.write(frame(f / FPS).tobytes())
        if (f - f0) % 300 == 0: print(out.split('/')[-1], f - f0, '/', f1 - f0, flush=True)
    ff.stdin.close(); ff.wait()

if __name__ == '__main__':
    mode = sys.argv[2] if len(sys.argv) > 2 else 'stills'
    if mode == 'stills':
        ts = [float(x) for x in sys.argv[3].split(',')] if len(sys.argv) > 3 else [(s[0] + s[1]) / 2 for s in SHOTLIST[::max(1, len(SHOTLIST) // 24)]]
        ims = [Image.fromarray(frame(t)).resize((480, 270)) for t in ts]
        Sh = Image.new('RGB', (480 * 4, 270 * ((len(ims) + 3) // 4)))
        for k, im in enumerate(ims): Sh.paste(im, ((k % 4) * 480, (k // 4) * 270))
        Sh.save(f'/tmp/claude-0/film_{LANG}_stills.jpg', quality=85); print('stills', len(ims))
    elif mode == 'seg':
        render(float(sys.argv[3]), float(sys.argv[4]), sys.argv[5])
    elif mode == 'shots':
        for s in SHOTLIST: print(round(s[0], 2), round(s[1], 2), s[3], s[2][:2])
