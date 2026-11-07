"""Golden Sparrow S1 - full film renderer (16:9). python3 film.py en|te [t0 t1 out.mp4] | stills | full"""
import sys, os, json, math, re, subprocess, functools
LANG = sys.argv[1]
sys.argv_saved = list(sys.argv)
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, '/home/claude/gs'); sys.path.insert(0, '/home/claude/gs/film'); sys.path.insert(0, '/home/claude/gs/plan'); sys.path.insert(0, '/home/claude/gs/poc')
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
PH = json.load(open(PH_CACHE)) if os.path.exists(PH_CACHE) else {}
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
json.dump(PH, open(PH_CACHE, 'w'))

# ---------------------------------------------------------------- overlays (on-screen text per line)
def scene_text(i):
    s = SC[i]['te' if TE else 'en'] if i in SC else ''
    if i == '0.2': return 'Palampore · Coromandel Coast, 18th c. · The Met' if not TE else 'పలంపోర్ · కోరమాండల్ తీరం, 18వ శతాబ్దం · The Met'
    if i == '4.4': return "AKBAR'S COURT · AKBARNAMA"
    if i == '2.12': return ('IN FORCE FROM 25 DEC 1722 · EXCEPTIONS: MUSLINS, NECKCLOTHS, FUSTIANS, ALL-BLUE CALICO' if not TE else '25 డిసెంబర్ 1722 నుంచి అమలు · మినహాయింపులు: మస్లిన్, మెడగుడ్డలు, ఫస్టియన్, పూర్తి నీలం calico')
    if i == '7.2': return '23 JUNE 1757 · ~3,000 vs ~50,000' if not TE else '23 జూన్ 1757 · ~3,000 vs ~50,000'
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
OVER.append(('sub', M['3.12'][0] + 0.3, M['3.12'][1], 'SUBSCRIBE'))
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
    if k == 'card': return card(t, a, b, sp[1])
    if k == 'title': return title(t, a, b, sp[1])
    if k == 'text': return textcard(t, a, b, sp[1], sp[2])
    if k == 'flow': return flow(t, a, b)
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
