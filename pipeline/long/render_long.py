# Long video renderer (16:9, 1920x1080). usage: python3 render_long.py en|te OUTDIR [stills t,...] | [part i n] | [audio]
import sys, os, subprocess, functools, math
sys.path.insert(0, '/home/claude/elnino'); sys.path.insert(0, '/home/claude/long')
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from epic import load_wav, SR, FPS, boom
import modern
from modern import *
import anim_long as AN
from caps_long import en_words, te_words, chunks, Anchor
modern.CLIPD = '/home/claude/long/clipf/'

LANG = sys.argv[1]; OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True)
TE = LANG == 'te'; W, H = 1920, 1080
ROOT = '/home/claude/long/'
voice = load_wav(ROOT + f'voice_{LANG}.wav'); VLEN = len(voice) / SR
LEAD = 0.15; TAIL = 3.0; TOTAL = LEAD + VLEN + TAIL
IMG = ROOT + 'media/'
BTN = ('SUBSCRIBE', 'SUBSCRIBED')
BRAND = 'WHY? తెలుగు' if TE else 'WHY?'

if TE:
    from keep_te import TE_LINES
    WS = te_words(TE_LINES, ROOT + 'voice_te.wav', ROOT + 'voice_te.wav.map.json')
    from phr_te import PH
else:
    WS = en_words(); from phr_en import PH
A = Anchor(WS); A.p = {}
for k, ph in PH: A.p[k] = A(ph)
from cues_long import get_cues, CHAPTERS
SC, EV = get_cues(LANG, A)
CHAPS = CHAPTERS[LANG]
CH = chunks(WS, maxw=5 if not TE else 3, maxc=30 if not TE else 26)
DIMK = 0.6

# ---------- backgrounds ----------
@functools.lru_cache(16)
def _src(name): return Image.open(IMG + name).convert('RGB')

@functools.lru_cache(16)
def _blurfill(name):
    s = _src(name); sc = max(W / s.width, H / s.height)
    b = s.resize((int(s.width * sc) + 2, int(s.height * sc) + 2), Image.BILINEAR)
    x0 = (b.width - W) // 2; y0 = (b.height - H) // 2
    b = b.crop((x0, y0, x0 + W, y0 + H)).filter(ImageFilter.GaussianBlur(45))
    return Image.blend(b, Image.new('RGB', (W, H), (0, 0, 0)), .5).convert('RGBA')

def still_bg(img, name, v, t0, t1, dim=.3, focus=(.5, .5), fit=False, zoom=(1.0, 1.08)):
    s = _src(name); u = e_io(prog(v, t0, t1 + .5)); z = zoom[0] + (zoom[1] - zoom[0]) * u
    if fit and s.width / s.height < 1.5:
        img.paste(_blurfill(name), (0, 0))
        bh = H; bw = int(min(W, s.width / s.height * H * z)); sc = H / s.height * z
        cw, ch = min(s.width, bw / sc), bh / sc
        x0 = (s.width - cw) * focus[0]; y0 = (s.height - ch) * focus[1]
        im = s.resize((bw, bh), Image.BICUBIC, box=(x0, y0, x0 + cw, y0 + ch)).convert('RGBA')
        sh = Image.new('RGBA', (bw + 80, bh), (0, 0, 0, 0)); ImageDraw.Draw(sh).rectangle((40, 0, bw + 40, bh), fill=(0, 0, 0, 150))
        img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(20)), ((W - bw) // 2 - 40, 0))
        img.alpha_composite(im, ((W - bw) // 2, 0))
    else:
        sc = max(W / s.width, H / s.height) * z; cw, ch = W / sc, H / sc
        x0 = (s.width - cw) * focus[0]; y0 = (s.height - ch) * focus[1]
        img.alpha_composite(s.resize((W, H), Image.BICUBIC, box=(x0, y0, x0 + cw, y0 + ch)).convert('RGBA'))
    if dim: img.alpha_composite(Image.new('RGBA', (W, H), (0, 0, 0, int(255 * dim))))

@functools.lru_cache(2)
def _vign():
    g = np.zeros((H, W, 4), np.uint8); y = np.linspace(0, 1, H)[:, None]; x = np.linspace(-1, 1, W)[None, :]
    a = np.clip((y - .55) / .45, 0, 1) ** 1.5 * 190 + np.clip((.12 - y) / .12, 0, 1) ** 2 * 120 + (np.abs(x) ** 3) * 60
    g[..., 3] = np.clip(a, 0, 255).astype(np.uint8); return Image.fromarray(g, 'RGBA')

def background(img, b, v, t0, t1):
    k = b[0]
    if k == 'clip': video_bg(img, b[1], v, t0, t1, dim=b[2] * DIMK, grad=False, zoom=(1.0, 1.06))
    elif k == 'img': still_bg(img, b[1], v, t0, t1, dim=b[2] * DIMK, focus=b[3], fit=b[4], zoom=b[5])
    if k in ('clip', 'img'): img.alpha_composite(_vign())

# ---------- overlays ----------
def tag(img, text, x, y, a=1.0, px=20, fill=(10, 10, 10, 190), col=CREAM, anchor='l'):
    if a <= 0: return
    f = mono_font(text, px); w = f.getlength(text) + (len(text) * 2 if not is_te(text) else 0) + 32; h = px * 1.9
    if anchor == 'r': x = x - w
    im = Image.new('RGBA', (int(w), int(h)), (0, 0, 0, 0)); ImageDraw.Draw(im).rounded_rectangle((0, 0, w - 1, h - 1), radius=9, fill=fill)
    alpha_paste(img, im, x, y, a); mono(img, text, x + 16, y + h / 2, px, col, a, anchor='l', track=2)

def place_header(img, v, t0, name, state):
    k = e_out(prog(v, t0, t0 + .45))
    if k <= 0: return
    x = 110; y = 640
    text_plain(img, name, x - 40 * (1 - k), y, 130 if not is_te(name) else 104, CREAM, k, anchor='l')
    sk = prog(v, t0 + .25, t0 + .6)
    if sk > 0:
        f = head_font(state, 38); w = f.getlength(state) + 56
        pill(img, state, x + w / 2 - 10, y + 105, 38, AMBER, (10, 10, 10), sk)

def chapter_card(img, v, t0, num, title):
    k = e_out(prog(v, t0, t0 + .5))
    mono(img, num, W / 2, 400, 34, AMBER, k, track=6)
    text_plain(img, title, W / 2, 500 + 30 * (1 - k), 120 if not is_te(title) else 92, CREAM, k)
    d = ImageDraw.Draw(img); lw = 300 * e_io(prog(v, t0 + .2, t0 + .8))
    d.rounded_rectangle((W / 2 - lw, 590, W / 2 + lw, 596), radius=3, fill=AMBER)

def chips(img, v, items, title, t0):
    text_plain(img, title, W / 2, 300, 64 if not is_te(title) else 54, AMBER, prog(v, t0, t0 + .3))
    n = len(items); gap = 560; x0 = W / 2 - gap * (n - 1) / 2
    for i, (txt, ti) in enumerate(items):
        if v < ti: continue
        k = e_back(prog(v, ti, ti + .4)); px = 60 if not is_te(txt) else 50
        f = head_font(txt, px); b = f.getbbox(txt); w = b[2] - b[0] + 100; h = px * 2.2
        im = Image.new('RGBA', (int(w), int(h)), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.rounded_rectangle((0, 0, w - 1, h - 1), radius=26, fill=(12, 12, 12, 230), outline=AMBER + (255,), width=4)
        d.text((50 - b[0], (h - (b[3] - b[1])) / 2 - b[1]), txt, font=f, fill=CREAM)
        paste_c(img, im, x0 + i * gap, 520, prog(v, ti, ti + .15), .8 + .2 * k)

def stack_words(img, v, items, y0=330, gap=150):
    for i, (txt, ti, col) in enumerate(items):
        if v < ti: continue
        k = e_out(prog(v, ti, ti + .3))
        text_plain(img, txt, W / 2, y0 + i * gap + 30 * (1 - k), 110 if not is_te(txt) else 88, col, k)

def bell(d, cx, cy, r, col):
    pts = []
    for t in range(0, 181, 10):
        ang = math.radians(180 + t); pts.append((cx + r * .62 * math.cos(ang), cy - r * .15 + r * .7 * math.sin(ang)))
    pts += [(cx + r * .75, cy + r * .55), (cx - r * .75, cy + r * .55)]
    d.polygon(pts, fill=col); d.ellipse((cx - r * .18, cy + r * .55, cx + r * .18, cy + r * .85), fill=col)

def sub_button(img, v, t_in, cx, cy, s=1.0, t_tap=None):
    if v < t_in: return
    k = e_back(prog(v, t_in, t_in + .4)); a = prog(v, t_in, t_in + .2)
    pressed = t_tap is not None and v >= t_tap
    dip = .9 if t_tap is not None and t_tap <= v < t_tap + .12 else 1.0
    txt = BTN[1] if pressed else BTN[0]
    f = font('archivo', int(46 * s)); tw = f.getlength(txt); h = int(104 * s); w = int(tw + 150 * s)
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=h // 2, fill=(70, 70, 72, 255) if pressed else (230, 30, 30, 255))
    bell(d, 62 * s, h / 2, 30 * s, CREAM + (255,))
    d.text((110 * s, h / 2), txt, font=f, fill=CREAM, anchor='lm')
    paste_c(img, im, cx, cy, a, k * dip)
    if t_tap is not None:
        rp = prog(v, t_tap - .05, t_tap + .45)
        if 0 < rp < 1:
            g = Image.new('RGBA', img.size, (0, 0, 0, 0)); gd = ImageDraw.Draw(g); R = 30 + 90 * rp
            tx, ty = cx + w * .25, cy + 10
            gd.ellipse((tx - R, ty - R, tx + R, ty + R), outline=(255, 255, 255, int(220 * (1 - rp))), width=6)
            gd.ellipse((tx - 22, ty - 22, tx + 22, ty + 22), fill=(255, 255, 255, int(200 * (1 - rp))))
            img.alpha_composite(g)

# ---------- captions ----------
CAP_Y = 948
@functools.lru_cache(2)
def _capband():
    g = np.zeros((H, W, 4), np.uint8); y = np.arange(H)[:, None]
    g[..., 3] = (np.exp(-((y - CAP_Y) / 120.0) ** 2) * 130).astype(np.uint8); return Image.fromarray(g, 'RGBA')

def caption(img, v):
    cur = None
    for c in CH:
        if c[0] - .05 <= v < c[1]: cur = c
    img.alpha_composite(_capband())
    if not cur: return
    s0, e0, ws = cur; px = 60 if not TE else 56
    f = font('archivo', px) if not TE else font('tesans', px)
    toks = [x[2].upper() if not TE else x[2] for x in ws]
    sp = f.getlength(' '); wid = [f.getlength(t) for t in toks]; tot = sum(wid) + sp * (len(toks) - 1)
    x = W / 2 - tot / 2; k = e_back(prog(v, s0 - .05, s0 + .12))
    for i in range(len(toks)):
        active = ws[i][0] - .03 <= v < (ws[i + 1][0] if i + 1 < len(ws) else e0)
        said = v >= ws[i][0] - .03
        col = AMBER if active else (CREAM if said else (200, 196, 188))
        sc = (1.06 if active else 1.0) * (.88 + .12 * k)
        im = Image.new('RGBA', (int(wid[i] + 40), int(px * 1.9)), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.text((20, px * .95), toks[i], font=f, fill=col, anchor='lm', stroke_width=6, stroke_fill=(0, 0, 0))
        paste_c(img, im, x + wid[i] / 2, CAP_Y, 1.0, sc); x += wid[i] + sp

# ---------- frame ----------
def scene_at(v):
    idx = 0
    for i, s in enumerate(SC):
        if v >= s['t'] - 1e-6: idx = i
    s = SC[idx]; t1 = SC[idx + 1]['t'] if idx + 1 < len(SC) else VLEN + TAIL
    return idx, s, t1

def chap_at(idx):
    c = 0
    for s in SC[:idx + 1]:
        if 'chap' in s: c = s['chap']
    return c

def frame_at(T):
    v = T - LEAD
    idx, s, t1 = scene_at(v); t0 = s['t']
    img = Image.new('RGBA', (W, H), (10, 10, 10, 255))
    background(img, s['bg'], v, t0, t1)
    k = s['kind']
    if t1 - t0 > 3.0 and s['bg'][0] in ('img', 'clip') and k in ('head', 'place', 'big', 'chapter'):
        dd = t1 - t0
        if dd > 5.2:   # two punch-ins on long shots so nothing sits still for more than ~2 s
            pk = .55 * e_out(prog(v, t0 + dd * .36, t0 + dd * .36 + .12)) + .45 * e_out(prog(v, t0 + dd * .68, t0 + dd * .68 + .12))
        else:
            pk = e_out(prog(v, t0 + dd * .5, t0 + dd * .5 + .12))
        if pk > 0:
            z = 1 + .06 * pk; cw, ch = W / z, H / z
            img = img.resize((W, H), Image.BILINEAR, box=((W - cw) / 2, (H - ch) / 2, (W + cw) / 2, (H + ch) / 2))
    if k == 'anim':
        args = dict(s['args']); fn = getattr(AN, s['fn'])
        if s['fn'] == 'india_hook': args['title'] = s.get('title')
        fn(img, v, t0, lang=LANG, **args)
    elif k == 'why':
        sc_ = e_back(prog(v, t0, t0 + .35))
        text_plain(img, 'WHY?' if not TE else 'ఎందుకు?', W / 2, 470, int((300 if not TE else 240) * max(.3, sc_)), AMBER, prog(v, t0, t0 + .15))
    elif k == 'place': place_header(img, v, t0, s['name'], s['state'])
    elif k == 'chapter': chapter_card(img, v, t0, s['num'], s['title'])
    elif k == 'chips': chips(img, v, s['items'], s['title'], t0)
    elif k == 'stack': stack_words(img, v, s['items'])
    elif k == 'big':
        bd = s.get('bd', .1); sc_ = e_back(prog(v, t0 + bd, t0 + bd + .35)); by = s.get('by', 470); bpx = s.get('bpx', 200)
        if is_te(s['big']): bpx = int(bpx * .8)
        if sc_ > 0: text_plain(img, s['big'], W / 2, by, int(bpx * max(.2, sc_)), s.get('bcol', AMBER), prog(v, t0 + bd, t0 + bd + .15))
        if 'lab' in s: mono(img, s['lab'], W / 2, by - bpx * .62 - 34, 30, CREAM, prog(v, t0, t0 + .3), track=4)
    elif k == 'subask':
        tap = s['tap']
        mono(img, 'IF YOU\'RE ENJOYING THIS' if not TE else 'ఈ వీడియో నచ్చితే', W / 2, 330, 34, AMBER, prog(v, t0, t0 + .3), track=5)
        sub_button(img, v, t0 + .4, W / 2, 500, 1.6, t_tap=tap)
        text_plain(img, 'IT REALLY HELPS US GROW' if not TE else 'మాకు చాలా హెల్ప్ అవుతుంది', W / 2, 680, 54 if not TE else 46, CREAM, prog(v, t0 + 1.2, t0 + 1.6))
    elif k == 'cta':
        text_plain(img, 'WHY?' if not TE else 'WHY? తెలుగు', W / 2, 250, 200 if not TE else 150, CREAM, prog(v, t0, t0 + .25))
        sub_button(img, v, t0 + .6, W / 2, 470, 1.3, t_tap=t0 + 2.0)
        mono(img, 'A NEW WHY EVERY DAY' if not TE else 'రోజూ ఒక కొత్త "ఎందుకు"', W / 2, 590, 30, AMBER, prog(v, t0 + .8, t0 + 1.2), track=4)
        text_plain(img, 'COMMENT YOUR WHY BELOW' if not TE else 'మీ "ఎందుకు" కామెంట్ చేయండి', W / 2, 720, 64 if not TE else 50, CREAM, prog(v, t0 + 2.6, t0 + 3.0))
        mono(img, s['src'], W / 2, 1030, 20, GREY, prog(v, t0 + 1.2, t0 + 1.6), track=2)
    if s.get('ai'): tag(img, 'AI ILLUSTRATION', W - 40, 80, prog(v, t0, t0 + .3), anchor='r')
    if s.get('credit'): tag(img, s['credit'], W - 30, H - 44, prog(v, t0, t0 + .3) * .95, px=15, col=(200, 196, 188), anchor='r')
    if s.get('src') and k != 'cta': tag(img, ('SOURCE · ' if not TE else 'ఆధారం · ') + s['src'], 60, 820, prog(v, t0 + .3, t0 + .6), px=20, fill=(10, 10, 10, 210), col=AMBER)
    for e in EV:
        if e['t'] <= v < e['t1']:
            news_card(img, e['source'], e['date'], e['head'], W / 2, 720, v, e['t'], w=900, hl_words=e.get('hl', ()), tilt=-2, a_out=1 - prog(v, e['t1'] - .3, e['t1']))
    if k != 'cta': caption(img, v)
    if k not in ('cta',):
        progress_bar(img, CHAPS, chap_at(idx), W, .85)
        mono(img, BRAND, 60, H - 30, 20, AMBER, .8, anchor='l')
    arr = np.asarray(img.convert('RGB'), np.float32)
    fade = min(1.0, (T / .25) if T < .25 else 1.0) if False else 1.0
    fade *= 1 - prog(T, TOTAL - .4, TOTAL)
    return np.clip(arr * fade, 0, 255).astype(np.uint8)

def build_audio(path):
    from scipy.ndimage import uniform_filter1d
    from pedalboard import Pedalboard, PeakFilter, HighShelfFilter, LowpassFilter, HighpassFilter
    n = int(TOTAL * SR) + SR; out = np.zeros((n, 2), np.float32)
    i0 = int(LEAD * SR); out[i0:i0 + len(voice)] += voice
    bed = Pedalboard([HighpassFilter(60), PeakFilter(cutoff_frequency_hz=2200, gain_db=-5, q=0.7), HighShelfFilter(cutoff_frequency_hz=6000, gain_db=-5), LowpassFilter(10000)])
    def track(name, start, end, fin=.3, fout=1.5):
        m = load_wav(ROOT + 'music/' + name + '.wav'); m = bed(m.T.copy(), SR).T.astype(np.float32)
        L = int((end - start) * SR)
        if L > len(m):   # crossfaded loop: re-enter at 20 s with a 4 s crossfade, skip the track's fade-out tail
            body = m[:max(int(25 * SR), len(m) - int(8 * SR))]; x = int(4 * SR); seg = body[int(20 * SR):]; outm = body.copy()
            while len(outm) < L:
                r_ = np.linspace(0, 1, x)[:, None]; outm = np.concatenate([outm[:-x], outm[-x:] * (1 - r_) + seg[:x] * r_, seg[x:]])
            m = outm
        m = m[:L]
        g = np.ones(L, np.float32); a = int(fin * SR); b = int(fout * SR)
        g[:a] *= np.linspace(0, 1, a); g[-b:] *= np.linspace(1, 0, b)
        o = np.zeros((n, 2), np.float32); j = int(start * SR); o[j:j + L] = m * g[:, None]; return o
    sw = [s for s in SC if s.get('music_switch')]; tsw = LEAD + sw[0]['t'] if sw else TOTAL / 2
    ask0 = LEAD + min(s['t'] for s in SC if s.get('ask'))
    mus = track('river', 0, ask0 + .4, .3, 1.2) + track('wakes', tsw - .3, TOTAL, 1.5, 3.0)
    env = uniform_filter1d(np.abs(out[:, 0]), int(.12 * SR)); sc = np.clip(env / .04, 0, 1)
    g = float(os.environ.get('MGAIN', .22)) * (1 - .62 * sc)
    # the ask: music almost silent
    a0 = int(ask0 * SR); a1 = int(tsw * SR); g[a0:a1] *= .25
    for s in SC:
        if s['kind'] == 'chapter':
            c1 = int((LEAD + s['t']) * SR); c0 = c1 - int(1.0 * SR)
            if c0 > 0: g[c0:c1] *= np.linspace(1, .3, c1 - c0); g[c1:c1 + int(.6 * SR)] *= np.linspace(.3, 1, int(.6 * SR))
    out += mus * g[:, None]
    def add(x, t, k=1.0):
        j = int(t * SR)
        if j < 0: x = x[-j:]; j = 0
        x = x[:max(0, n - j)]; out[j:j + len(x)] += (x[:, None] if x.ndim == 1 else x) * k
    def hit(a=.55):
        b = boom(1.2, f0=90, f1=40, amp=a); b = b if b.ndim == 1 else b[:, 0]; return b
    def soft_tr():
        t = np.arange(int(.35 * SR)) / SR; f = 140 * np.exp(-t * 6) + 55
        return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9) * .18
    def pop():
        tp = np.arange(int(.09 * SR)) / SR; return np.sin(2 * np.pi * (220 + 900 * np.exp(-tp * 40)) * tp) * np.exp(-tp * 35) * .28
    def click():
        t = np.arange(int(.06 * SR)) / SR; return (np.sin(2 * np.pi * 1800 * t) * np.exp(-t * 90) * .35 + np.random.default_rng(7).normal(0, 1, len(t)) * np.exp(-t * 200) * .15)
    # ---------------- sound design (sfx.py): every cut and animation beat gets a tonal sound ----------------
    import sfx as FX
    for _nm, _fn in [('boom', 'sub_boom'), ('riser', 'low_swell'), ('click', 'mouse_click'), ('shutter', 'shutter'), ('whoosh', None), ('paper', None)]:
        _p = ROOT + 'sounds/sfx_' + _nm + '.wav'
        if os.path.exists(_p) and _fn:
            _w = load_wav(_p); _w = _w / max(1e-6, float(np.abs(_w).max())) * .6; setattr(FX, _fn, (lambda w: (lambda *a, **k: w * (k.get('g', a[-1] if a else .5) / .5)))(_w))
    from scipy.ndimage import uniform_filter1d as _uf
    venv = _uf(np.abs(voice[:, 0] if voice.ndim > 1 else voice), int(.08 * SR))
    def addfx(x, t, k=1.0):
        j = int((LEAD + t) * SR)
        if j < 0 or j >= n: return
        x = x[:n - j]
        # gentle duck under the voice so effects never mask words
        vi = np.clip(np.arange(j, j + len(x)) - i0, 0, len(venv) - 1); duck = 1 - .45 * np.clip(venv[vi] / .05, 0, 1)
        out[j:j + len(x)] += x * (k * duck)[:, None]
    addfx(FX.sub_boom(.5), -.02)
    for q, s in enumerate(SC):
        t = s['t']; k_ = s['kind']; args = s.get('args', {})
        if q > 0:
            if k_ == 'chapter': addfx(FX.low_swell(.9, .22), t - .9); addfx(FX.sub_boom(.55), t)
            elif k_ == 'place': addfx(FX.swish(.35, 300, 1200, .10), t - .2); addfx(FX.thud(.22), t + .05)
            elif k_ == 'why': addfx(FX.low_swell(.6, .18), t - .6); addfx(FX.sub_boom(.5), t)
        if s.get('boom'): addfx(FX.sub_boom(.42), t)
        if k_ == 'big':
            bd = s.get('bd', .1); addfx(FX.swish(.3, 300, 1300, .09), t + bd - .22); addfx(FX.thud(.24), t + bd)
            if s.get('bcol') == RED: addfx(FX.sub_boom(.35), t + bd)
        if k_ == 'chips':
            for j, (_, ti) in enumerate(s['items']): addfx(FX.drop(.2), ti)
        if k_ == 'stack':
            for j, it in enumerate(s['items']): addfx(FX.stamp(.26), it[1])
        if k_ == 'subask': addfx(FX.mouse_click(.4), s['tap'])
        if k_ == 'cta': addfx(FX.mouse_click(.4), t + 2.0)
        if s.get('card'): addfx(FX.swish(.35, 300, 1200, .1), s['card_t'] - .15); addfx(FX.shutter(.3), s['card_t'] + .1)
        fn = s.get('fn')
        if fn in ('india_hook', 'india_days'):
            for j, p in enumerate(args.get('pins', [])):
                if p[3] < 90: addfx(FX.drop(.2), p[3])
                if fn == 'india_days' and p[4]: addfx(FX.drop(.14), p[3] + .35)
        elif fn == 'word_merge':
            for p in args['parts']: addfx(FX.swish(.3, 250, 1100, .1), p[2] - .15); addfx(FX.drop(.18), p[2] + .1)
            rt = args['result'][1]; addfx(FX.swish(.45, 300, 1500, .12), rt - .25); addfx(FX.lock(.28), rt + .15); addfx(FX.sub_boom(.22), rt + .15)
        elif fn == 'three_lines':
            addfx(FX.drop(.18), args['t_day'])
            ends = []
            for j, ln in enumerate(args['lanes']):
                addfx(FX.swish(1.6, 200 + 40 * j, 900 + 150 * j, .07), ln[2] + .2); addfx(FX.lock(.22), ln[2] + 1.8); ends.append(ln[2] + 1.8)
            addfx(FX.sub_boom(.3), max(ends) + .02)
        elif fn == 'loophole':
            for sl in args['slots']:
                if sl[1]: addfx(FX.low_swell(.5, .16), sl[2] - .15); addfx(FX.sub_boom(.42), sl[2] + .35); addfx(FX.lock(.24), sl[2] + .35)
                else: addfx(FX.drop(.16), sl[2]); addfx(FX.stamp(.32), sl[2] + .35)
        elif fn == 'timeline':
            for j, nd in enumerate(args['nodes']):
                if j: addfx(FX.swish(.6, 250, 1000, .09), nd[2] - .6)
                addfx(FX.drop(.22), nd[2])
        elif fn == 'town_stage':
            addfx(FX.swish(1.0, 200, 700, .07), t)
            for sp in args['spots']: addfx(FX.drop(.2), sp[2])
        elif fn == 'diaspora':
            addfx(FX.drop(.2), t)
            for d in args['dests']: addfx(FX.swish(1.1, 220, 1200, .09), d[3]); addfx(FX.drop(.18), d[3] + 1.1)
        elif fn == 'clay_cycle':
            for nd in args['nodes']: addfx(FX.swish(.8, 220, 900, .07), nd[1]); addfx(FX.drop(.18), nd[1])
            if args.get('center'): addfx(FX.lock(.26), args['center'][1]); addfx(FX.sub_boom(.25), args['center'][1])
        elif fn == 'power_table':
            for rw in args['rows']: addfx(FX.stamp(.28), rw[2]); addfx(FX.drop(.14), rw[2] + .3)
    # ---------------- ambience: real recordings under matching footage (sounds/<key>.wav, optional) ----------------
    AMB = {  # background (image/clip/anim) -> ambience key, level
        'E2': ('fire', .16), 'E3': ('fire', .16), 'E4': ('fire', .14), 'E5': ('fire', .16), 'P_effigy': ('fire', .14), 'P_effigy2': ('fire', .12),
        'L_inner_ravana': ('fire', .13), 'bonfire': ('fire', .14),
        'crowd': ('crowd', .12), 'P10a': ('crowd', .07), 'P10b': ('crowd', .07), 'W_kullu': ('crowd', .10), 'RV_P1': ('crowd', .05),
        'mysore': ('crowd', .11), 'P3': ('crowd', .11), 'P_mysorepalace': ('crowd', .06),
        'durgaproc': ('drums', .12), 'durgaidol': ('drums', .10), 'garba': ('drums', .11), 'BAS': ('drums', .11), 'W_bathukamma1': ('crowd', .07), 'W_bathukamma2': ('crowd', .07),
        'howrah': ('river', .12), 'P_howrahnight': ('river', .07), 'clay_cycle': ('river', .07), 'monsoon': ('river', .08),
        'L_setu': ('waves', .13),
        'L_shami': ('forest', .12), 'P6': ('forest', .10), 'paddy': ('forest', .08), 'harvest': ('forest', .08), 'P_hampi': ('forest', .07), 'W_dibba1': ('forest', .06), 'W_dibba2': ('forest', .06),
        'P_aarti': ('bells', .09), 'L_mysore_banni': ('bells', .08), 'P_kumartuli': ('bells', .05), 'P_dashain_tika': ('bells', .05),
        'L_durga_fight': ('war', .13), 'L_villains': ('war', .09), 'L_durga_birth': ('war', .06), 'L_paes': ('crowd', .08),
    }
    KEEP_AMB = {'E2', 'E3', 'E4', 'E5', 'P_effigy', 'P_effigy2', 'bonfire', 'crowd', 'mysore', 'durgaproc', 'garba', 'BAS', 'W_kullu'}
    AMB = {k: (v[0], v[1] * .7) for k, v in AMB.items() if k in KEEP_AMB}   # user: literal ambience felt artificial
    ONESHOT = {}
    _ac = {}
    def amb_load(key):
        if key not in _ac:
            p = ROOT + 'sounds/' + key + '.wav'
            _ac[key] = load_wav(p) if os.path.exists(p) else None
        return _ac[key]
    from scipy.ndimage import uniform_filter1d as _uf2
    venv2 = _uf2(np.abs(out[:, 0]), int(.15 * SR))
    used = set()
    for q, s in enumerate(SC):
        bg = s['bg']; key = bg[1].split('.')[0] if bg[0] in ('img', 'clip') else s.get('fn')
        if key not in AMB: continue
        kind, lvl = AMB[key]; a = amb_load(kind)
        if a is None: continue
        t0 = LEAD + s['t']; t1 = LEAD + (SC[q + 1]['t'] if q + 1 < len(SC) else VLEN)
        L = int((t1 - t0 + .6) * SR); off = (hash(kind + str(q)) % max(1, len(a) - L)) if len(a) > L else 0
        seg = np.concatenate([a] * (1 + L // len(a)))[off:off + L] if len(a) > 0 else None
        if seg is None or len(seg) < L: continue
        f = int(.35 * SR); env = np.ones(L, np.float32); env[:f] = np.linspace(0, 1, f); env[-f:] = np.linspace(1, 0, f)
        j = int((t0 - .15) * SR); j = max(0, j); seg = seg[:max(0, min(L, n - j))]; env = env[:len(seg)]
        duck = 1 - .55 * np.clip(venv2[j:j + len(seg)] / .05, 0, 1)
        out[j:j + len(seg)] += seg * (1.8 * lvl * env * duck)[:, None]; used.add(kind)
        if key in ONESHOT and ONESHOT[key] not in used:
            o = amb_load(ONESHOT[key])
            if o is not None: k2 = int((t0 + .3) * SR); o = o[:min(len(o), int(4 * SR), n - k2)]; out[k2:k2 + len(o)] += o * .18; used.add(ONESHOT[key])
    print('ambience used:', sorted(used))
    import scipy.io.wavfile as wf
    wf.write(path + '.pre.wav', SR, (np.clip(out, -1, 1) * 32767).astype(np.int16))
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', path + '.pre.wav', '-af', 'loudnorm=I=-14:TP=-1:LRA=7', '-ar', '48000', path], check=True)

if __name__ == '__main__':
    mode = sys.argv[3] if len(sys.argv) > 3 else 'full'
    if mode == 'stills':
        for t in sys.argv[4].split(','): Image.fromarray(frame_at(float(t) + LEAD)).save(f"{OUT}/still_{float(t):06.2f}.jpg", quality=85)
        sys.exit()
    if mode == 'audio': build_audio(f"{OUT}/audio.wav"); sys.exit()
    if mode == 'scenes':
        for s in SC: print(round(s['t'], 2), s['kind'], s['bg'][:2], s.get('big', s.get('name', s.get('fn', ''))))
        sys.exit()
    if mode == 'part':
        i, nparts = int(sys.argv[4]), int(sys.argv[5]); N = int(TOTAL * FPS); a, b = N * i // nparts, N * (i + 1) // nparts
        p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                              '-c:v', 'libx264', '-preset', 'medium', '-crf', '19', '-pix_fmt', 'yuv420p', f"{OUT}/part{i}.mp4"], stdin=subprocess.PIPE)
        for f in range(a, b): p.stdin.write(frame_at(f / FPS).tobytes())
        p.stdin.close(); p.wait(); print('part done', i)
