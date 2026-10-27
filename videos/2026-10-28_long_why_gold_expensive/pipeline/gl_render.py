# Gold long video "Why Is Gold So Expensive? (It Came From Space)" 16:9
# usage: python3 gl_render.py en|te OUTDIR [stills t,t | audio | part i n]
import sys, os, subprocess, functools, math, json, re
sys.path.insert(0, '/home/claude/elnino'); sys.path.insert(0, '/home/claude/goldL')
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from epic import load_wav, SR, FPS
from modern import *

LANG = sys.argv[1]; OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True)
TE = LANG == 'te'; W, H = 1920, 1080
G = '/home/claude/goldL/'
voice = load_wav(G + f'voice_{LANG}.wav'); VLEN = len(voice) / SR
LEAD = 0.15; TAIL = 6.0; TOTAL = LEAD + VLEN + TAIL
from gl_cues import get_cues
SC, _ = get_cues(LANG)
L = (lambda en, te: te if TE else en)
BRAND = 'WHY? తెలుగు' if TE else 'WHY?'
SERIES = L('GOLD · FULL STORY', 'గోల్డ్ · ఫుల్ స్టోరీ')
GOLD = (255, 196, 64); WHITE = (255, 255, 255)
COL = dict(red=RED, amber=AMBER, cream=CREAM, gold=GOLD)
CHAPS = [L(x, y) for x, y in [('INTRO', 'ఇంట్రో'), ('STARS', 'స్టార్స్'), ('FOREVER', 'ఎప్పటికీ'), ('MONEY', 'డబ్బు'), ('MINING', 'తవ్వకం'), ('PRICE', 'ధర'), ('INDIA', 'ఇండియా'), ('ANSWER', 'సమాధానం')]]

# ---------------- captions (piece text spread over whisper word onsets / voiced frames) ----------------
def build_words():
    keys = json.load(open(G + f'keys_{LANG}.json')); texts = json.load(open(G + f'pieces_{LANG}.json'))
    mp = json.load(open(G + f'voice_{LANG}.wav.map.json')); st = [m[0] for m in mp] + [VLEN]
    a = voice[:, 0]; hop = SR // 100; n = len(a) // hop
    db = 20 * np.log10(np.sqrt(np.mean(a[:n * hop].reshape(n, hop) ** 2, 1)) + 1e-9); vo = db > np.median(db) - 20
    ws = json.load(open(G + 'ven.words.json')) if not TE else []
    out = []
    for i, line in enumerate(texts):
        s, e = st[i], st[i + 1]; toks = line.split()
        on = [w[0] for w in ws if s - .1 <= w[0] < e - .05]
        if not TE and len(on) == len(toks):
            for j, t in enumerate(toks): out.append((on[j], (on[j + 1] if j + 1 < len(on) else e), t, j == len(toks) - 1))
            continue
        fr = np.where(vo[int(s * 100):int(e * 100)])[0] / 100 + s
        if len(fr) == 0: fr = np.array([s, e])
        Lw = np.array([max(2, len(w)) for w in toks], float); c = np.concatenate([[0], np.cumsum(Lw) / Lw.sum()])
        for j, w in enumerate(toks):
            t0 = fr[min(len(fr) - 1, int(c[j] * (len(fr) - 1)))]; t1 = fr[min(len(fr) - 1, int(c[j + 1] * (len(fr) - 1)))]
            out.append((float(t0), float(max(t1, t0 + .12)), w, j == len(toks) - 1))
    return out
def chunks(ws, maxw, maxc):
    C = []; cur = []
    for k, x in enumerate(ws):
        cur.append(x); txt = ' '.join(y[2] for y in cur); nxt = ws[k + 1] if k + 1 < len(ws) else None
        brk = x[3] or len(cur) >= maxw or len(txt) >= maxc or x[2][-1] in '.,?!' or (nxt and nxt[0] - x[1] > .35)
        if nxt and len(txt + ' ' + nxt[2]) > maxc + 4: brk = True
        if brk or not nxt: C.append(cur); cur = []
    return [(c[0][0], min(C[i + 1][0][0] if i + 1 < len(C) else c[-1][1] + .4, c[-1][1] + .6), c) for i, c in enumerate(C)]
CH = chunks(build_words(), 5 if not TE else 3, 30 if not TE else 26)

# ---------------- clips & backgrounds ----------------
_N = {}
@functools.lru_cache(64)
def _cimg(cid, k): return Image.open(f'{G}cf/{cid}/{k + 1:04d}.jpg').convert('RGB')
def cframe(cid, t):
    if cid not in _N: _N[cid] = len(os.listdir(G + 'cf/' + cid))
    n = _N[cid]; f = int(max(0, t) * 30); per = 2 * (n - 1); k = f % per; k = k if k < n else per - k
    return _cimg(cid, k)
def zoomed(im, z):
    if z == 1.0: return im.convert('RGBA')
    cw, ch = W / z, H / z; x0 = (W - cw) / 2; y0 = (H - ch) / 2
    return im.resize((W, H), Image.BILINEAR, box=(x0, y0, x0 + cw, y0 + ch)).convert('RGBA')

@functools.lru_cache(1)
def starfield():
    rng = np.random.default_rng(3); a = np.zeros((H, W + 600, 3), np.float32) + np.array([6, 7, 12], np.float32)
    yy, xx = np.mgrid[0:H, 0:W + 600]
    for cx, cy, r, c in [(500, 400, 700, (30, 18, 50)), (1700, 800, 800, (10, 30, 50))]:
        d = ((xx - cx) ** 2 + (yy - cy) ** 2) / r ** 2; a += np.exp(-d * 2)[..., None] * np.array(c, np.float32)
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert('RGBA'); d = ImageDraw.Draw(im)
    for _ in range(900):
        x, y = rng.uniform(0, W + 600), rng.uniform(0, H); s = rng.choice([1, 1, 1, 2, 2, 3]); b = int(rng.uniform(120, 255))
        d.ellipse((x - s / 2, y - s / 2, x + s / 2, y + s / 2), fill=(b, b, min(255, b + 20), 255))
    return im
def stars_bg(img, v): off = int((v * 14) % 600); img.paste(starfield().crop((off, 0, off + W, H)), (0, 0))
@functools.lru_cache(1)
def warmglow():
    yy, xx = np.mgrid[0:H, 0:W]; d = np.sqrt((xx - W / 2) ** 2 + (yy - 470) ** 2) / 1100
    a = np.zeros((H, W, 3), np.float32) + 8; a += np.exp(-d * d * 3)[..., None] * np.array([90, 45, 10], np.float32)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert('RGBA')
CRASH_SRC = 12.7
def nasa_t(v, tc): return min(20.9, max(0, CRASH_SRC + (v - tc) * (1.5 if v < tc else 1.0)))
@functools.lru_cache(4)
def _still(name): return Image.open(G + 'media/' + name).convert('RGB')
@functools.lru_cache(4)
def _blurfill(name):
    s = _still(name); sc = max(W / s.width, H / s.height); b = s.resize((int(s.width * sc) + 2, int(s.height * sc) + 2))
    x0 = (b.width - W) // 2; y0 = (b.height - H) // 2; b = b.crop((x0, y0, x0 + W, y0 + H)).filter(ImageFilter.GaussianBlur(40))
    return Image.blend(b, Image.new('RGB', (W, H), (0, 0, 0)), .5).convert('RGBA')
def still_fit(img, name, v, t0, t1):
    img.paste(_blurfill(name), (0, 0)); s = _still(name); u = e_io(prog(v, t0, t1 + .5)); z = 1.0 + .08 * u
    h = int(H * z); w = int(s.width * h / s.height); im = s.resize((w, h), Image.BICUBIC).convert('RGBA')
    img.alpha_composite(im, (int(W / 2 - w / 2), int(H / 2 - h / 2 - 40 * u)))
@functools.lru_cache(2)
def _vign():
    g = np.zeros((H, W, 4), np.uint8); y = np.linspace(0, 1, H)
    g[..., 3] = (np.clip((y - .55) / .45, 0, 1) ** 1.4 * 200 + np.clip((.15 - y) / .15, 0, 1) ** 2 * 110)[:, None].astype(np.uint8)
    return Image.fromarray(g, 'RGBA')
def background(img, s, v, t0, t1):
    b = s['bg']; k = b[0]
    if k == 'clip':
        dim = b[2]; z0, z1 = b[3]; off = b[4] if len(b) > 4 else 0.0; z = z0 + (z1 - z0) * e_io(prog(v, t0, t1 + .3))
        img.paste(zoomed(cframe(b[1], v - t0 + off), z), (0, 0))
        if dim: img.alpha_composite(Image.new('RGBA', (W, H), (0, 0, 0, int(255 * dim))))
    elif k == 'nasa':
        tc = s.get('t_crash') or NASA_TC
        img.paste(cframe('N', nasa_t(v, tc)).convert('RGBA'), (0, 0)); img.alpha_composite(Image.new('RGBA', (W, H), (0, 0, 0, 40)))
    elif k == 'still': still_fit(img, b[1], v, t0, t1)
    elif k == 'stars': stars_bg(img, v)
    elif k == 'glow': img.paste(warmglow(), (0, 0))
    elif k == 'black': img.paste((10, 10, 10, 255), (0, 0, W, H))
    elif k == 'grid':
        for q, cid in enumerate(b[1]):
            fr = cframe(cid, v - t0 + q * .4).resize((W // 2, H // 2), Image.BILINEAR).convert('RGBA')
            img.alpha_composite(fr, ((q % 2) * W // 2, (q // 2) * H // 2))
        img.alpha_composite(Image.new('RGBA', (W, H), (0, 0, 0, int(255 * b[2]))))
    img.alpha_composite(_vign())
NASA_TC = next(s['t_crash'] for s in SC if s['kind'] == 'nasa')

# ---------------- helpers ----------------
@functools.lru_cache(96)
def sphere(r, col, hl=1.0):
    s = int(r * 2 + 4); yy, xx = np.mgrid[0:s, 0:s].astype(np.float32); c = s / 2
    d = np.sqrt((xx - c) ** 2 + (yy - c) ** 2) / r; h = np.sqrt((xx - c + r * .35) ** 2 + (yy - c + r * .38) ** 2) / r
    rgb = np.array(col, np.float32)[None, None, :] * (1 - .55 * np.clip(d, 0, 1) ** 2)[..., None] + 255 * hl * .55 * np.exp(-h * h * 9)[..., None]
    return Image.fromarray(np.dstack([np.clip(rgb, 0, 255), np.clip((1 - d) * r / 1.5, 0, 1) * 255]).astype(np.uint8), 'RGBA')
@functools.lru_cache(32)
def glow(r, col, strength=1.0):
    s = int(r * 2); yy, xx = np.mgrid[0:s, 0:s].astype(np.float32); d = np.sqrt((xx - r) ** 2 + (yy - r) ** 2) / r
    a = np.exp(-d * d * 4) * 255 * strength
    return Image.fromarray(np.dstack([np.full((s, s), col[0]), np.full((s, s), col[1]), np.full((s, s), col[2]), np.clip(a, 0, 255)]).astype(np.uint8), 'RGBA')
def put(img, spr, cx, cy, a=1.0, s=1.0):
    if a > 0 and s > 0: paste_c(img, spr, cx, cy, a, s)
def stamp_text(img, text, cx, cy, px, col, v, t0, rot=-6):
    if v < t0: return
    k = prog(v, t0, t0 + .18); s = 1.7 - .7 * e_out(k)
    f = head_font(text, px); b = f.getbbox(text); w = b[2] - b[0] + px * .9; h = b[3] - b[1] + px * .7
    im = Image.new('RGBA', (int(w + 20), int(h + 20)), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((10, 10, w + 10, h + 10), radius=14, outline=col + (255,), width=max(6, px // 12), fill=(10, 10, 10, 150))
    d.text((10 + (w - (b[2] - b[0])) / 2 - b[0], 10 + (h - (b[3] - b[1])) / 2 - b[1]), text, font=f, fill=col)
    put(img, im.rotate(rot, Image.BICUBIC, expand=True), cx, cy, min(1, k * 3), s)
def big_text(img, text, cx, cy, px, col, a=1.0, sc=1.0):
    lines = text.split('\n')
    for i, ln in enumerate(lines):
        y = cy + (i - (len(lines) - 1) / 2) * px * 1.12; p = px if not is_te(ln) else int(px * .82)
        f = head_font(ln, max(8, int(p * max(.3, sc)))); b = f.getbbox(ln)
        im = Image.new('RGBA', (b[2] - b[0] + 40, b[3] - b[1] + 40), (0, 0, 0, 0))
        ImageDraw.Draw(im).text((20 - b[0], 20 - b[1]), ln, font=f, fill=col, stroke_width=max(3, p // 22), stroke_fill=(0, 0, 0))
        alpha_paste(img, im, cx - im.width / 2, y - im.height / 2, a)
def pop_big(img, v, t, text, cx, cy, px, col):
    if v >= t: big_text(img, text, cx, cy, px, col, prog(v, t, t + .15), e_back(prog(v, t, t + .35)))
def shine_sweep(img, v, t0, dur=.9, a=.5):
    q = prog(v, t0, t0 + dur)
    if q <= 0 or q >= 1: return
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); x = -500 + (W + 1000) * e_io(q)
    d.polygon([(x - 120, 0), (x + 120, 0), (x - 380, H), (x - 620, H)], fill=(255, 245, 210, int(255 * a * math.sin(math.pi * q))))
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(50)))
def chip(img, text, cx, cy, px, fill, col, a=1.0, s=1.0): pill(img, text, cx, cy, px, fill, col, a, s)
def o2(img, x, y, ang=0.0, a=1.0, sep=0.0, s=1.0):
    r = int(24 * s); dx = (r * .8 + sep) * math.cos(ang); dy = (r * .8 + sep) * math.sin(ang)
    put(img, sphere(r, (230, 70, 60)), x - dx, y - dy, a); put(img, sphere(r, (230, 70, 60)), x + dx, y + dy, a)
def tag(img, text, x, y, a=1.0, px=20, fill=(10, 10, 10, 190), col=CREAM, anchor='l'):
    if a <= 0: return
    f = mono_font(text, px); w = f.getlength(text) + (len(text) * 2 if not is_te(text) else 0) + 36; h = px * 1.9
    im = Image.new('RGBA', (int(w), int(h)), (0, 0, 0, 0)); ImageDraw.Draw(im).rounded_rectangle((0, 0, w - 1, h - 1), radius=10, fill=fill)
    if anchor == 'r': x = x - w
    alpha_paste(img, im, x, y - h / 2, a); mono(img, text, x + 18, y, px, col, a, anchor='l', track=2)

exec(open(G + 'gl_scenes.py').read())

# ---------------- subscribe ----------------
BTN = ('SUBSCRIBE', 'SUBSCRIBED')
def bellicon(d, cx, cy, r, col):
    pts = [(cx + r * .62 * math.cos(math.radians(180 + t)), cy - r * .15 + r * .7 * math.sin(math.radians(180 + t))) for t in range(0, 181, 10)]
    pts += [(cx + r * .75, cy + r * .55), (cx - r * .75, cy + r * .55)]
    d.polygon(pts, fill=col); d.ellipse((cx - r * .18, cy + r * .55, cx + r * .18, cy + r * .85), fill=col)
def sub_button(img, v, t_in, cx, cy, s=1.0, tap=0.9):
    if v < t_in: return
    k = e_back(prog(v, t_in, t_in + .4)); a = prog(v, t_in, t_in + .2); pressed = v >= t_in + tap
    dip = .9 if t_in + tap <= v < t_in + tap + .12 else 1.0; txt = BTN[1] if pressed else BTN[0]
    f = font('archivo', int(46 * s)); tw = f.getlength(txt); h = int(104 * s); w = int(tw + 150 * s)
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=h // 2, fill=(70, 70, 72, 255) if pressed else (230, 30, 30, 255))
    bellicon(d, 62 * s, h / 2, 30 * s, CREAM + (255,)); d.text((110 * s, h / 2), txt, font=f, fill=CREAM, anchor='lm')
    paste_c(img, im, cx, cy, a, k * dip)
    rp = prog(v, t_in + tap - .05, t_in + tap + .45)
    if 0 < rp < 1:
        g = Image.new('RGBA', img.size, (0, 0, 0, 0)); gd = ImageDraw.Draw(g); R = 30 + 90 * rp; tx, ty = cx + w * .25, cy + 10
        gd.ellipse((tx - R, ty - R, tx + R, ty + R), outline=(255, 255, 255, int(220 * (1 - rp))), width=6); img.alpha_composite(g)
SUB_T = next(s['t'] for s in SC if s.get('subpop')) + 2.6
def sub_pop(img, v, t0, dur=3.4):
    if not (t0 <= v < t0 + dur): return
    a = prog(v, t0, t0 + .25) * (1 - prog(v, t0 + dur - .3, t0 + dur)); k = e_out(prog(v, t0, t0 + .35))
    sub_button(img, v, t0, W - 260, 70 + 40 * k, .75, tap=1.4)
    mono(img, L('ENJOYING THIS?', 'ఈ వీడియో నచ్చితే'), W - 260, 150 + 40 * k, 22, CREAM, a)

# ---------------- captions ----------------
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
        active = ws[i][0] - .03 <= v < (ws[i + 1][0] if i + 1 < len(ws) else e0); said = v >= ws[i][0] - .03
        col = AMBER if active else (CREAM if said else (200, 196, 188)); sc = (1.06 if active else 1.0) * (.88 + .12 * k)
        im = Image.new('RGBA', (int(wid[i] + 40), int(px * 1.9)), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.text((20, px * .95), toks[i], font=f, fill=col, anchor='lm', stroke_width=6, stroke_fill=(0, 0, 0))
        paste_c(img, im, x + wid[i] / 2, CAP_Y, 1.0, sc); x += wid[i] + sp

def progress(img, cur):
    n = len(CHAPS); x0, x1, y = 60, W - 60, 40; seg = (x1 - x0) / n; d = ImageDraw.Draw(img)
    for i, nm in enumerate(CHAPS):
        a, b = x0 + i * seg + 4, x0 + (i + 1) * seg - 4; col = AMBER if i == cur else ((150, 146, 138) if i < cur else (70, 70, 72))
        d.rounded_rectangle((a, y - 3, b, y + 3), radius=3, fill=col + (230,))
        if i == cur: mono(img, nm, (a + b) / 2, y + 22, 15, AMBER, .9, track=3)

# ---------------- frame ----------------
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

def frame_at(Tt):
    v = Tt - LEAD; idx, s, t1 = scene_at(v); t0 = s['t']
    img = Image.new('RGBA', (W, H), (10, 10, 10, 255))
    background(img, s, v, t0, t1)
    k = s['kind']
    if k in GFX: GFX[k](img, v, t0, t1, s)
    elif k == 'chapter': chapter_card(img, v, t0, s['num'], s['title'])
    elif k == 'big':
        bd = s.get('bd', .1); col = COL[s.get('bcol', 'amber')]
        if s.get('stamp'): stamp_text(img, s['big'], W / 2, 430, s['bpx'], col, v, t0 + bd)
        else: pop_big(img, v, t0 + bd, s['big'], W / 2, 430, s['bpx'], col)
    elif k == 'plain':
        if s.get('pill') and v >= s['pill_t']: chip(img, s['pill'], W / 2, 200, 40, AMBER, (10, 10, 10), prog(v, s['pill_t'], s['pill_t'] + .25), e_back(prog(v, s['pill_t'], s['pill_t'] + .3)))
        if s.get('bigq'): pop_big(img, v, s['bigq_t'], s['bigq'], W / 2, 430, 170, AMBER)
    elif k == 'cta': cta(img, v, t0, s)
    if s.get('shine'): shine_sweep(img, v, s['shine'])
    if s.get('credit'): tag(img, s['credit'], W - 30, H - 26, prog(v, t0, t0 + .3) * .95, px=15, col=(200, 196, 188), anchor='r')
    if k not in ('cta', 'jhintro'):
        caption(img, v); progress(img, chap_at(idx))
        mono(img, BRAND, 60, H - 30, 20, AMBER, .8, anchor='l'); mono(img, SERIES, 60, 92, 18, AMBER, .75, anchor='l')
    sub_pop(img, v, SUB_T)
    arr = np.asarray(img.convert('RGB'), np.float32)
    if k == 'nasa':
        tc = s['t_crash']
        if tc <= v < tc + .35:
            sh = int(18 * (1 - prog(v, tc, tc + .35)) * math.sin(v * 90)); arr = np.roll(arr, sh, axis=1)
        fl = 1 - prog(v, tc, tc + .35)
        if v >= tc and fl > 0: arr = arr * (1 - .8 * fl) + 255 * .8 * fl
    fade = 1 - prog(Tt, TOTAL - .4, TOTAL)
    return np.clip(arr * fade, 0, 255).astype(np.uint8)

# ---------------- audio ----------------
SFXD = '/home/claude/why-channel-studio/sfx/'
@functools.lru_cache(48)
def sfx(name, peak=.6):
    a = load_wav(SFXD + name + '.wav'); m = np.abs(a).max() + 1e-9; return a * (peak / m)
def build_audio(path):
    from scipy.ndimage import uniform_filter1d
    from pedalboard import Pedalboard, PeakFilter, HighShelfFilter, LowpassFilter, HighpassFilter
    n = int(TOTAL * SR) + SR; out = np.zeros((n, 2), np.float32)
    i0 = int(LEAD * SR); out[i0:i0 + len(voice)] += voice
    bed = Pedalboard([HighpassFilter(60), PeakFilter(cutoff_frequency_hz=2200, gain_db=-5, q=0.7), HighShelfFilter(cutoff_frequency_hz=6000, gain_db=-5), LowpassFilter(10000)])
    m = bed(load_wav('/home/claude/gold1/music.wav').T.copy(), SR).T.astype(np.float32)
    body = m[:len(m) - int(6 * SR)]; x = int(4 * SR); seg = body[int(20 * SR):]; mm = body.copy()
    while len(mm) < n:
        r_ = np.linspace(0, 1, x)[:, None]; mm = np.concatenate([mm[:-x], mm[-x:] * (1 - r_) + seg[:x] * r_, seg[x:]])
    mm = mm[:n]
    env = uniform_filter1d(np.abs(out[:, 0]), int(.12 * SR)); sc = np.clip(env / .04, 0, 1)
    g = float(os.environ.get('MGAIN', .2)) * (1 - .62 * sc)
    fi = int(.4 * SR); g[:fi] *= np.linspace(0, 1, fi)
    e = int((TOTAL - .1) * SR); fo = int(3.0 * SR); g[e - fo:e] *= np.linspace(1, 0, fo); g[e:] = 0
    for s in SC:
        if s['kind'] == 'chapter':
            c1 = int((LEAD + s['t']) * SR); c0 = c1 - int(1.0 * SR)
            if c0 > 0: g[c0:c1] *= np.linspace(1, .3, c1 - c0); g[c1:c1 + int(.6 * SR)] *= np.linspace(.3, 1, int(.6 * SR))
    for q, s_ in enumerate(SC):                                               # music swells under the title sequence
        if s_['kind'] == 'jhintro':
            a0 = int((LEAD + s_['t'] - .3) * SR); a1 = int((LEAD + SC[q + 1]['t']) * SR); r = np.clip(np.linspace(-1, 1, a1 - a0) * 3, -1, 1)
            g[a0:a1] = np.maximum(g[a0:a1], .45 * (1 - np.abs(np.minimum(r, 0)) * 0) * np.minimum(1, np.linspace(0, 6, a1 - a0)))
    out += mm * g[:, None]
    venv = uniform_filter1d(np.abs(voice[:, 0]), int(.08 * SR))
    def add(name, t, k=1.0, dur=None, duck=True):
        xx = sfx(name).copy()
        if dur: xx = xx[:int(dur * SR)]; f = int(.05 * SR); xx[-f:] *= np.linspace(1, 0, f)[:, None]
        j = int((LEAD + t) * SR)
        if j < 0: xx = xx[-j:]; j = 0
        xx = xx[:max(0, n - j)]
        if duck:
            vi = np.clip(np.arange(j, j + len(xx)) - i0, 0, len(venv) - 1); dk = 1 - .45 * np.clip(venv[vi] / .05, 0, 1); xx = xx * dk[:, None]
        out[j:j + len(xx)] += xx * k
    def amb(name, t0, t1, k, fin=.5, fout=.8):
        a = sfx(name); d = t1 - t0
        while len(a) < int(d * SR) + SR: a = np.concatenate([a, a])
        a = a[:int(d * SR)].copy(); f1 = int(fin * SR); f2 = int(fout * SR)
        a[:f1] *= np.linspace(0, 1, f1)[:, None]; a[-f2:] *= np.linspace(1, 0, f2)[:, None]
        j = int((LEAD + t0) * SR); out[j:j + len(a)] += a[:max(0, n - j)] * k
    add('boom_distant', 0.0, .35, duck=False)
    for q, s in enumerate(SC):
        t0 = s['t']; k = s['kind']; t1 = SC[q + 1]['t'] if q + 1 < len(SC) else VLEN
        if k == 'chapter': add('riser', t0 - 2.53, .3, duck=False); add('boom_impact', t0, .5, duck=False)
        elif q > 0 and s.get('sfx', True): add('woosh_air', t0 - .25, .18, dur=1.0)
        if k == 'big': add('stamp' if s.get('stamp') else 'sub_knock', t0 + s.get('bd', .1), .45)
        if k == 'plain' and s.get('pill'): add('sub_knock', s['pill_t'], .4)
        if k == 'plain' and s.get('bigq'): add('sub_knock', s['bigq_t'], .5)
        if s.get('shine'): add('woosh_air', s['shine'] - .1, .15, dur=1.0)
        for name, tt, kk in SFX_EVENTS(s, t0, t1): add(name, tt, kk)
        for name, a0, a1, kk in AMB_EVENTS(s, t0, t1): amb(name, a0, a1, kk)
    add('mouse_click', SUB_T + 1.4, .45)
    import scipy.io.wavfile as wf
    wf.write(path + '.pre.wav', SR, (np.clip(out, -1, 1) * 32767).astype(np.int16))
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', path + '.pre.wav', '-af', 'loudnorm=I=-14:TP=-1.5:LRA=8', '-ar', '48000', path], check=True)
    os.remove(path + '.pre.wav')

if __name__ == '__main__':
    mode = sys.argv[3] if len(sys.argv) > 3 else 'full'
    if mode == 'stills':
        for t in sys.argv[4].split(','): Image.fromarray(frame_at(float(t) + LEAD)).save(f"{OUT}/still_{float(t):06.2f}.jpg", quality=80)
        sys.exit()
    if mode == 'audio': build_audio(f"{OUT}/audio.wav"); sys.exit()
    if mode == 'part':
        i, nparts = int(sys.argv[4]), int(sys.argv[5]); N = int(TOTAL * FPS); a, b = N * i // nparts, N * (i + 1) // nparts
        p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                              '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p', f"{OUT}/part{i}.mp4"], stdin=subprocess.PIPE)
        for f in range(a, b): p.stdin.write(frame_at(f / FPS).tobytes())
        p.stdin.close(); p.wait(); print('part done', i)
