# Gold Short 1 "Your gold came from dead stars" (9:16, full-screen, explainer graphics)
# usage: PLAT=yt|ig python3 render_gold.py en|te OUTDIR [stills t,t | audio | part i n]
import sys, os, subprocess, functools, math
sys.path.insert(0, '/home/claude/elnino'); sys.path.insert(0, '/home/claude/gold1')
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from epic import load_wav, SR, FPS
from modern import *

LANG = sys.argv[1]; OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True)
TE = LANG == 'te'; W, H = 1080, 1920
PLAT = os.environ.get('PLAT', 'yt')
G = '/home/claude/gold1/'
voice = load_wav(G + f'voice_{LANG}_{PLAT}.wav'); VLEN = len(voice) / SR
LEAD = 0.15; TAIL = 0.7; TOTAL = LEAD + VLEN + TAIL
from cues_gold import get_cues
SC, T = get_cues(LANG)
L = (lambda en, te: te if TE else en)
BRAND = 'WHY? తెలుగు' if TE else 'WHY?'
SERIES = L('GOLD WEEK · 1/6', 'గోల్డ్ వీక్ · 1/6')
BTN = ('FOLLOW', 'FOLLOWING') if PLAT == 'ig' else ('SUBSCRIBE', 'SUBSCRIBED')
from caps_gold import words, chunks
CH = chunks(words(LANG), maxw=3 if not TE else 2, maxc=18 if not TE else 22)
CH[0] = (0.0,) + tuple(CH[0][1:])
GOLD = (255, 196, 64); WHITE = (255, 255, 255)
COL = dict(red=RED, amber=AMBER, cream=CREAM)
CRASH_SRC = 12.7

# ---------------- clips ----------------
_N = {}
@functools.lru_cache(96)
def _cimg(cid, k): return Image.open(f'{G}cf/{cid}/{k + 1:04d}.jpg').convert('RGB')
def cframe(cid, t):
    if cid not in _N: _N[cid] = len(os.listdir(G + 'cf/' + cid))
    n = _N[cid]; f = int(max(0, t) * 30); per = 2 * (n - 1); k = f % per; k = k if k < n else per - k
    return _cimg(cid, k)
def zoomed(im, z, cx=.5, cy=.5):
    if z == 1.0: return im.convert('RGBA')
    cw, ch = W / z, H / z; x0 = (W - cw) * cx; y0 = (H - ch) * cy
    return im.resize((W, H), Image.BILINEAR, box=(x0, y0, x0 + cw, y0 + ch)).convert('RGBA')

@functools.lru_cache(1)
def starfield():
    rng = np.random.default_rng(3); a = np.zeros((H + 400, W, 3), np.float32)
    a[:] = np.array([6, 7, 12], np.float32)
    yy, xx = np.mgrid[0:H + 400, 0:W]
    for cx, cy, r, c in [(300, 700, 700, (30, 18, 50)), (800, 1500, 800, (10, 30, 50))]:
        d = ((xx - cx) ** 2 + (yy - cy) ** 2) / r ** 2; a += np.exp(-d * 2)[..., None] * np.array(c, np.float32)
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert('RGBA'); d = ImageDraw.Draw(im)
    for _ in range(700):
        x, y = rng.uniform(0, W), rng.uniform(0, H + 400); s = rng.choice([1, 1, 1, 2, 2, 3]); b = int(rng.uniform(120, 255))
        d.ellipse((x - s / 2, y - s / 2, x + s / 2, y + s / 2), fill=(b, b, min(255, b + 20), 255))
    return im
def stars_bg(img, v):
    off = int((v * 12) % 400); img.paste(starfield().crop((0, off, W, off + H)), (0, 0))

@functools.lru_cache(1)
def warmglow():
    yy, xx = np.mgrid[0:H, 0:W]; d = np.sqrt((xx - 540) ** 2 + (yy - 820) ** 2) / 900
    a = np.zeros((H, W, 3), np.float32) + 8
    a += np.exp(-d * d * 3)[..., None] * np.array([90, 45, 10], np.float32)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert('RGBA')

@functools.lru_cache(1)
def nasa_mask():
    y = np.arange(H); m = np.clip((y - 330) / 140, 0, 1) * np.clip((1320 - y) / 140, 0, 1)
    return Image.fromarray((np.repeat(m[:, None], W, 1) * 255).astype(np.uint8), 'L')

def nasa_t(v):
    c = T['crash']; return min(20.9, max(0, CRASH_SRC + (v - c) * (1.5 if v < c else 1.0)))

@functools.lru_cache(2)
def _vign():
    g = np.zeros((H, W, 4), np.uint8); y = np.linspace(0, 1, H)
    a = np.clip((y - .5) / .5, 0, 1) ** 1.4 * 215 + np.clip((.2 - y) / .2, 0, 1) ** 2 * 150
    g[..., 3] = a[:, None].astype(np.uint8); return Image.fromarray(g, 'RGBA')

def background(img, b, v, t0, t1):
    k = b[0]
    if k == 'clip':
        dim = b[2]; z0, z1 = b[3]; off = b[4] if len(b) > 4 else 0.0
        z = z0 + (z1 - z0) * e_io(prog(v, t0, t1 + .3))
        img.paste(zoomed(cframe(b[1], v - t0 + off), z), (0, 0))
        if dim: img.alpha_composite(Image.new('RGBA', (W, H), (0, 0, 0, int(255 * dim))))
    elif k == 'nasa':
        stars_bg(img, v); fr = cframe('N', nasa_t(v)).convert('RGBA'); fr.putalpha(nasa_mask()); img.alpha_composite(fr)
    elif k == 'stars': stars_bg(img, v)
    elif k == 'glow': img.paste(warmglow(), (0, 0))
    elif k == 'black': img.paste((8, 8, 8, 255), (0, 0, W, H))
    elif k == 'grid':
        for q, cid in enumerate(b[1]):
            fr = cframe(cid, v - t0 + q * .4) if cid != 'N' else cframe('N', 14 + (v - t0))
            fr = fr.resize((W // 2, H // 2), Image.BILINEAR).convert('RGBA')
            img.alpha_composite(fr, ((q % 2) * W // 2, (q // 2) * H // 2))
        img.alpha_composite(Image.new('RGBA', (W, H), (0, 0, 0, int(255 * b[2]))))
        d = ImageDraw.Draw(img); d.line((W // 2, 0, W // 2, H), fill=(10, 10, 10, 255), width=8); d.line((0, H // 2, W, H // 2), fill=(10, 10, 10, 255), width=8)
    img.alpha_composite(_vign())

# ---------------- drawing helpers ----------------
@functools.lru_cache(64)
def sphere(r, col, hl=1.0):
    s = int(r * 2 + 4); yy, xx = np.mgrid[0:s, 0:s].astype(np.float32); c = s / 2
    d = np.sqrt((xx - c) ** 2 + (yy - c) ** 2) / r
    h = np.sqrt((xx - c + r * .35) ** 2 + (yy - c + r * .38) ** 2) / r
    base = np.array(col, np.float32)[None, None, :]
    sh = (1 - .55 * np.clip(d, 0, 1) ** 2)[..., None]
    rgb = base * sh + 255 * hl * .55 * np.exp(-h * h * 9)[..., None]
    a = np.clip((1 - d) * r / 1.5, 0, 1) * 255
    return Image.fromarray(np.dstack([np.clip(rgb, 0, 255), a]).astype(np.uint8), 'RGBA')

@functools.lru_cache(32)
def glow(r, col, strength=1.0):
    s = int(r * 2); yy, xx = np.mgrid[0:s, 0:s].astype(np.float32); d = np.sqrt((xx - r) ** 2 + (yy - r) ** 2) / r
    a = np.exp(-d * d * 4) * 255 * strength
    return Image.fromarray(np.dstack([np.full((s, s), col[0]), np.full((s, s), col[1]), np.full((s, s), col[2]), np.clip(a, 0, 255)]).astype(np.uint8), 'RGBA')

def put(img, spr, cx, cy, a=1.0, s=1.0):
    if a <= 0 or s <= 0: return
    paste_c(img, spr, cx, cy, a, s)

def stamp_text(img, text, cx, cy, px, col, v, t0, rot=-7):
    if v < t0: return
    k = prog(v, t0, t0 + .18); s = 1.7 - .7 * e_out(k)
    f = head_font(text, px); b = f.getbbox(text); w = b[2] - b[0] + px * .9; h = b[3] - b[1] + px * .7
    im = Image.new('RGBA', (int(w + 20), int(h + 20)), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((10, 10, w + 10, h + 10), radius=14, outline=col + (255,), width=max(6, px // 12), fill=(10, 10, 10, 150))
    d.text((10 + (w - (b[2] - b[0])) / 2 - b[0], 10 + (h - (b[3] - b[1])) / 2 - b[1]), text, font=f, fill=col)
    im = im.rotate(rot, Image.BICUBIC, expand=True); put(img, im, cx, cy, min(1, k * 3), s)

def big_text(img, text, cx, cy, px, col, a=1.0, sc=1.0):
    lines = text.split('\n')
    for i, ln in enumerate(lines):
        y = cy + (i - (len(lines) - 1) / 2) * px * 1.12
        p = px if not is_te(ln) else int(px * .82)
        f = head_font(ln, int(p * max(.3, sc))); b = f.getbbox(ln)
        im = Image.new('RGBA', (b[2] - b[0] + 40, b[3] - b[1] + 40), (0, 0, 0, 0))
        ImageDraw.Draw(im).text((20 - b[0], 20 - b[1]), ln, font=f, fill=col, stroke_width=max(3, p // 22), stroke_fill=(0, 0, 0))
        alpha_paste(img, im, cx - im.width / 2, y - im.height / 2, a)

def counter_txt(img, v, t0, t1, val, fmt, cx, cy, px, col):
    if v < t0: return
    k = e_out(prog(v, t0, t1)); n = val * k
    big_text(img, fmt(n), cx, cy, px, col, prog(v, t0, t0 + .15))

def fmt_int(n): return f'{int(round(n)):,}'

# ---------------- scene graphics ----------------
ELS = [('H', 1, (120, 190, 255)), ('He', 2, (150, 225, 235)), ('C', 6, (120, 120, 125)), ('O', 8, (235, 95, 80)),
       ('Ne', 10, (240, 130, 200)), ('Mg', 12, (180, 200, 160)), ('Si', 14, (170, 150, 120)), ('Fe', 26, (185, 95, 60))]
def g_fusion(img, v, t0, t1):
    a = prog(v, t0, t0 + .3)
    mono(img, L('INSIDE EVERY STAR', 'ప్రతి స్టార్ లోపల'), W / 2, 300, 30, AMBER, a)
    if v >= T['stars']:
        headline(img, L('STARS FUSE ATOMS', 'స్టార్స్ ఆటమ్స్‌ని కలుపుతాయి'), v, T['stars'], W / 2, 390, 74 if not TE else 64, 1000)
    if v < T['squeeze']:                               # a glowing star core, breathing
        r = 210 + 10 * math.sin(v * 5)
        put(img, glow(420, (255, 150, 40), .9), W / 2, 820); put(img, sphere(int(r), (255, 170, 50)), W / 2, 820, prog(v, t0, t0 + .3))
    elif v < T['H']:                                   # two atoms squeezed together, looping
        ph = ((v - T['squeeze']) % 1.0); cx, cy = W / 2, 820
        if ph < .55:
            dx = 300 * (1 - e_io(ph / .55)); put(img, sphere(70, (120, 190, 255)), cx - dx - 20, cy); put(img, sphere(70, (120, 190, 255)), cx + dx + 20, cy)
        else:
            q = (ph - .55) / .45; put(img, glow(260, (255, 240, 200), 1 - q), cx, cy); put(img, sphere(95, (150, 225, 235)), cx, cy, 1, .7 + .3 * e_back(min(1, q * 2)))
        mono(img, L('SQUEEZE → NEW ELEMENT', 'నొక్కితే - కొత్త ఎలిమెంట్'), W / 2, 1050, 28, CREAM, prog(v, T['squeeze'], T['squeeze'] + .3))
    else:                                              # the ladder of elements, up to iron
        ts = [T['H'], T['He'], T['C']] + list(np.linspace(T['C'], T['Fe'], 6)[1:-1]) + [T['Fe']]
        for i, (sym, z, col) in enumerate(ELS):
            if v < ts[i]: continue
            x = 165 + (i % 4) * 250; y = 640 + (i // 4) * 260; r = 78 + i * 3
            k = e_back(prog(v, ts[i], ts[i] + .3))
            stopped = v >= T['stop'] and sym == 'Fe'
            if stopped: put(img, glow(170, (240, 60, 50), .8), x, y)
            put(img, sphere(r, col), x, y, 1, k)
            text_plain(img, sym, x, y - 4, 64, WHITE, prog(v, ts[i], ts[i] + .2))
            mono(img, str(z), x, y + r + 26, 26, AMBER if sym == 'Fe' else GREY, prog(v, ts[i], ts[i] + .2))
            if i < 7 and i != 3 and v >= ts[i + 1]:
                mono(img, '›', x + 125, y, 44, AMBER, prog(v, ts[i + 1] - .1, ts[i + 1] + .1))
        if v >= T['stop']:
            x, y = 165 + 3 * 250, 640 + 260
            stamp_text(img, 'STOP', x, y, 52, RED, v, T['stop'], rot=-12)
            text_plain(img, L('IRON = THE LIMIT', 'ఐరన్ దగ్గర ఆగిపోతుంది'), W / 2, 1100, 58 if not TE else 50, AMBER, prog(v, T['stop'] + .2, T['stop'] + .45))

def g_scale(img, v, t0, t1):
    a = prog(v, t0, t0 + .2)
    headline(img, L('GOLD ATOM: 3.5× HEAVIER', 'గోల్డ్ ఆటమ్: 3.5 రెట్లు బరువు'), v, t0, W / 2, 380, 66 if not TE else 58, 1000, hl=(2,) if not TE else ())
    cx, cy = W / 2, 640; ar = math.radians(14 * e_out(prog(v, t0 + .25, t0 + .8)))
    d = ImageDraw.Draw(img); half = 330
    xl, yl = cx - half * math.cos(ar), cy - half * math.sin(ar)
    xr, yr = cx + half * math.cos(ar), cy + half * math.sin(ar)
    d.polygon([(cx - 40, cy + 260), (cx + 40, cy + 260), (cx, cy)], fill=(70, 70, 74, int(255 * a)))
    d.line((xl, yl, xr, yr), fill=CREAM + (int(255 * a),), width=12)
    for x, y, sym, m, r, col in [(xl, yl, 'Fe', '56', 62, (185, 95, 60)), (xr, yr, 'Au', '197', 108, GOLD)]:
        d.line((x, y, x, y + 70), fill=(160, 156, 150, int(255 * a)), width=4)
        put(img, sphere(r, col), x, y + 70 + r, a); text_plain(img, sym, x, y + 66 + r, 56 if r < 80 else 80, (20, 16, 8) if sym == 'Au' else WHITE, a)
        mono(img, L(('IRON' if sym == 'Fe' else 'GOLD'), ('ఐరన్' if sym == 'Fe' else 'గోల్డ్')) + ' · ' + m, x, y + 2 * r + 120, 28, AMBER if sym == 'Au' else CREAM, prog(v, t0 + .3, t0 + .5))

def g_collapse(img, v, t0, t1):
    tc, tn = T['collapse'], T['neutron']; cx, cy = W / 2, 800
    if v < tc + .45:
        k = e_io(prog(v, tc, tc + .45)); r = int(max(30, (300 + 12 * math.sin(v * 3)) * (1 - k) + 30 * k))
        put(img, glow(int(r * 1.9), (255, 90, 40), .8), cx, cy); put(img, sphere(r, (235, 80, 45)), cx, cy, prog(v, t0, t0 + .3))
        mono(img, L('A GIANT STAR DIES', 'ఒక పెద్ద స్టార్ చనిపోతుంది'), W / 2, 330, 32, AMBER, prog(v, t0, t0 + .3) * (1 - prog(v, tc, tc + .2)))
    else:
        q = prog(v, tc + .45, tc + 1.4)
        if q < 1:
            R = 40 + 900 * e_out(q); g = Image.new('RGBA', (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
            gd.ellipse((cx - R, cy - R, cx + R, cy + R), outline=(255, 240, 220, int(230 * (1 - q))), width=int(30 * (1 - q)) + 4); img.alpha_composite(g)
        put(img, glow(260, (120, 200, 255), .9 + .1 * math.sin(v * 9)), cx, cy); put(img, sphere(34, (210, 235, 255)), cx, cy)
        for s in (1, -1):                                  # pulsar beams
            ang = v * 2.2 + (0 if s > 0 else math.pi); bx, by = cx + 700 * math.cos(ang), cy + 700 * math.sin(ang)
            g = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(g).line((cx, cy, bx, by), fill=(150, 210, 255, 60), width=26)
            img.alpha_composite(g.filter(ImageFilter.GaussianBlur(10)))
    fl = 1 - prog(v, tc + .42, tc + .65)
    if tc + .42 <= v and fl > 0: img.alpha_composite(Image.new('RGBA', (W, H), (255, 255, 255, int(200 * fl))))
    if v >= tn:
        pill(img, L('NEUTRON STAR', 'న్యూట్రాన్ స్టార్'), W / 2, 380, 44, AMBER, (10, 10, 10), prog(v, tn, tn + .25), e_back(prog(v, tn, tn + .3)))
        mono(img, L('≈ 20 KM WIDE · AS HEAVY AS THE SUN', '~20 KM వెడల్పు · సూర్యుడంత బరువు'), W / 2, 460, 26, CREAM, prog(v, tn + .2, tn + .5))

def cube_spr(s, glow_k):
    im = Image.new('RGBA', (int(s * 2.2), int(s * 2.4)), (0, 0, 0, 0)); d = ImageDraw.Draw(im); cx, cy = im.width / 2, im.height / 2
    top = [(cx, cy - s), (cx + s * .95, cy - s * .5), (cx, cy), (cx - s * .95, cy - s * .5)]
    left = [(cx - s * .95, cy - s * .5), (cx, cy), (cx, cy + s * 1.05), (cx - s * .95, cy + s * .55)]
    right = [(cx + s * .95, cy - s * .5), (cx, cy), (cx, cy + s * 1.05), (cx + s * .95, cy + s * .55)]
    mix = lambda c1, c2: tuple(int(c1[i] * (1 - glow_k) + c2[i] * glow_k) for i in range(3))
    d.polygon(top, fill=mix((250, 250, 246), (210, 240, 255))); d.polygon(left, fill=mix((214, 212, 206), (110, 180, 255)))
    d.polygon(right, fill=mix((188, 186, 180), (80, 150, 240)))
    rng = np.random.default_rng(4)
    for _ in range(140):
        x, y = rng.uniform(cx - s * .9, cx + s * .9), rng.uniform(cy - s, cy + s); d.point((x, y), fill=(255, 255, 255, 120))
    return im

def g_sugar(img, v, t0, t1):
    put(img, glow(140, (120, 200, 255), .8), W / 2, 330); put(img, sphere(20, (210, 235, 255)), W / 2, 330)
    mono(img, L('ONE SUGAR CUBE OF IT', 'దాని ఒక్క చక్కెర ముక్క'), W / 2, 430, 30, AMBER, prog(v, T['cube'] - .3, T['cube']))
    if v >= T['cube']:
        k = e_back(prog(v, T['cube'], T['cube'] + .35)); gk = e_io(prog(v, T['weigh'], T['weigh'] + .5))
        if gk > 0: put(img, glow(330, (110, 180, 255), gk * .8), W / 2, 720)
        put(img, cube_spr(150, gk), W / 2, 720 - 120 * (1 - k), prog(v, T['cube'], T['cube'] + .15))
    if v >= T['weigh']:
        if not TE: counter_txt(img, v, T['weigh'], T['billion'] + .3, 1e9, fmt_int, W / 2, 1000, 104, AMBER)
        else: counter_txt(img, v, T['weigh'], T['billion'] + .3, 100, lambda n: f'{int(round(n))} కోట్ల', W / 2, 1000, 110, AMBER)
        mono(img, L('TONS', 'టన్నులు'), W / 2, 1090, 34, CREAM, prog(v, T['weigh'] + .2, T['weigh'] + .4))

def g_nasa1(img, v, t0, t1):
    pill(img, L('TWO DEAD STARS', 'రెండు చనిపోయిన స్టార్స్'), W / 2, 270, 38, AMBER, (10, 10, 10), prog(v, t0, t0 + .3) * (1 - prog(v, T['crash'] - .1, T['crash'])))
    c = T['crash']; fl = 1 - prog(v, c, c + .35)
    if v >= c and fl > 0: img.alpha_composite(Image.new('RGBA', (W, H), (255, 255, 255, int(220 * fl))))

def g_2017(img, v, t0, t1):
    mono(img, L('FIRST ONE EVER SEEN', 'మొదటిసారి కనిపించింది'), W / 2, 260, 30, AMBER, prog(v, t0, t0 + .3))
    sc = e_back(prog(v, t0 + .05, t0 + .4)); big_text(img, '2017', W / 2, 460, 200, CREAM, prog(v, t0, t0 + .15), sc)
    if v >= T['away']:
        if not TE: counter_txt(img, v, T['away'], T['away'] + .8, 130, lambda n: f'{int(round(n))} MILLION', W / 2, 650, 86, AMBER)
        else: counter_txt(img, v, T['away'], T['away'] + .8, 13, lambda n: f'{int(round(n))} కోట్ల', W / 2, 650, 96, AMBER)
        mono(img, L('LIGHT-YEARS AWAY', 'లైట్ ఇయర్స్ దూరం'), W / 2, 730, 28, CREAM, prog(v, T['away'] + .3, T['away'] + .6))
    tc = t0 + .9
    if v >= tc:
        news_card(img, 'NASA', 'OCT 16, 2017', 'NASA Missions Catch First Light from a Gravitational-Wave Event', W / 2, 1520, v, tc, w=940, hl_words=(3, 4))

def g_spectrum(img, v, t0, t1):
    mono(img, L('ITS LIGHT = A FINGERPRINT', 'ఆ వెలుగే ఒక వేలిముద్ర'), W / 2, 270, 30, AMBER, prog(v, t0, t0 + .3))
    k = e_out(prog(v, t0 + .1, t0 + .6)); x0, y0, w, h = 80, 1390, 920, 120
    if k <= 0: return
    arr = np.zeros((h, w, 4), np.uint8); xs = np.linspace(0, 1, w)
    hue = np.clip(xs, 0, 1)
    import colorsys
    cols = np.array([colorsys.hsv_to_rgb(.78 * (1 - u), .85, 1) for u in hue]) * 255
    arr[..., :3] = cols[None, :, :].astype(np.uint8); arr[..., 3] = 235
    lines = [.12, .21, .33, .38, .52, .61, .67, .74, .86, .91]
    for i, lx in enumerate(lines):
        if v >= t0 + .7 + i * .12: c = int(lx * w); arr[:, max(0, c - 3):c + 3, :3] = 10
    sp = Image.fromarray(arr, 'RGBA')
    sp = sp.crop((0, 0, int(w * k) or 1, h)); img.alpha_composite(sp, (x0, y0))
    if v >= t0 + 1.9:
        pill(img, L('HEAVY METALS INSIDE', 'లోపల హెవీ మెటల్స్'), W / 2, 1580, 38, AMBER, (10, 10, 10), prog(v, t0 + 1.9, t0 + 2.2), e_back(prog(v, t0 + 1.9, t0 + 2.25)))

def tile(img, cx, cy, z, sym, name, v, ti, col):
    if v < ti: return
    k = e_back(prog(v, ti, ti + .35)); w, h = 300, 340
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=26, fill=(14, 12, 8, 235), outline=col + (255,), width=6)
    d.text((24, 18), str(z), font=font('mono', 40), fill=col)
    f = font('archivo', 150); b = f.getbbox(sym); d.text(((w - (b[2] - b[0])) / 2 - b[0], 90 - b[1]), sym, font=f, fill=col)
    f2 = head_font(name, 40); b2 = f2.getbbox(name); d.text(((w - (b2[2] - b2[0])) / 2 - b2[0], 270 - b2[1]), name, font=f2, fill=CREAM)
    put(img, im, cx, cy + 40 * (1 - k), prog(v, ti, ti + .15), .9 + .1 * k)

def g_metals(img, v, t0, t1):
    tg = T['goldw']; tile(img, 360, 720, 79, 'Au', L('GOLD', 'గోల్డ్'), v, min(tg, t0 + .25), GOLD)
    tile(img, 720, 720, 78, 'Pt', L('PLATINUM', 'ప్లాటినం'), v, min(tg, t0 + .25) + .45, (220, 222, 230))
    pill(img, L('MADE IN THE BLAST', 'ఆ పేలుడులో పుట్టాయి'), W / 2, 470, 36, AMBER, (10, 10, 10), prog(v, t0, t0 + .3))

def g_twist(img, v, t0, t1):
    stamp_text(img, L('THE TWIST', 'ట్విస్ట్'), W / 2, 760, 150 if not TE else 130, AMBER, v, t0 + .05, rot=-4)

def g_cutaway(img, v, t0, t1):
    cx, cy, R = W / 2, 760, 380
    a = prog(v, t0, t0 + .3); ts = T['sank']
    mono(img, L('YOUNG EARTH · MOLTEN', 'కొత్త భూమి · కరిగిన లావా'), W / 2, 300, 30, AMBER, a * (1 - prog(v, ts, ts + .2)))
    if v >= ts: pill(img, L('GOLD SANK TO THE CORE', 'గోల్డ్ కోర్‌లోకి మునిగింది'), W / 2, 300, 40, AMBER, (10, 10, 10), prog(v, ts, ts + .25), e_back(prog(v, ts, ts + .3)))
    put(img, glow(int(R * 1.5), (255, 90, 20), .55 * a), cx, cy)
    # molten mantle with a slow bubbling shimmer
    s = 2 * R; yy, xx = np.mgrid[0:s, 0:s].astype(np.float32); d = np.sqrt((xx - R) ** 2 + (yy - R) ** 2) / R
    n = (np.sin(xx / 23 + v * 2.1) + np.sin(yy / 19 - v * 1.7) + np.sin((xx + yy) / 31 + v * 1.3)) / 3
    base = np.array([200, 55, 15], np.float32) + (np.array([255, 150, 40], np.float32) - [200, 55, 15]) * (.5 + .5 * n)[..., None] * (1 - d * .5)[..., None]
    crust = (d > .93)[..., None]; base = np.where(crust, np.array([70, 30, 20], np.float32), base)
    al = np.clip((1 - d) * R / 2, 0, 1) * 255 * a
    img.alpha_composite(Image.fromarray(np.dstack([np.clip(base, 0, 255), al]).astype(np.uint8), 'RGBA'), (int(cx - R), int(cy - R)))
    gk = e_io(prog(v, t0 + 1.2, ts + .6)); rc = 130
    put(img, sphere(rc, (int(90 + 165 * gk), int(60 + 136 * gk), int(40 + 24 * gk)), .6 + .4 * gk), cx, cy, a)
    if gk > .5: mono(img, L('CORE', 'కోర్'), cx, cy, 30, (40, 26, 6), (gk - .5) * 2)
    rng = np.random.default_rng(9); d2 = ImageDraw.Draw(img)
    for i in range(110):
        ang = rng.uniform(0, 2 * math.pi); r0 = rng.uniform(170, 340); st = t0 + .3 + rng.uniform(0, ts - t0 - .6); du = rng.uniform(1.0, 1.8)
        if v < st: continue
        q = e_io(prog(v, st, st + du)); rr = r0 + (rc * .6 - r0) * q
        if q >= 1: continue
        x, y = cx + rr * math.cos(ang), cy + rr * math.sin(ang); sz = 6
        d2.ellipse((x - sz, y - sz, x + sz, y + sz), fill=GOLD + (int(255 * min(1, (1 - q) * 3)),))

def g_meteor(img, v, t0, t1):
    pill(img, L('METEORITES', 'మీటియోరైట్స్'), W / 2, 520, 42, AMBER, (10, 10, 10), prog(v, t0, t0 + .25), e_back(prog(v, t0, t0 + .3)))
    mono(img, L('~4 BILLION YEARS AGO', '~400 కోట్ల ఏళ్ల క్రితం'), W / 2, 600, 28, CREAM, prog(v, t0 + .2, t0 + .5))
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for (st, x0, y0, x1, y1, w0) in [(t0 + .15, 1100, 380, 300, 1180, 26), (t0 + .85, 1000, 250, 560, 900, 16), (t0 + 1.45, 1140, 600, 160, 1500, 22)]:
        q = prog(v, st, st + .75)
        if q <= 0 or q >= 1.0 and v > st + 1.1: continue
        hx, hy = x0 + (x1 - x0) * e_io(min(1, q)), y0 + (y1 - y0) * e_io(min(1, q)); fade = 1 - prog(v, st + .75, st + 1.1)
        for j in range(28):
            u = j / 28; tx, ty = hx - (x1 - x0) * .32 * u, hy - (y1 - y0) * .32 * u
            c = (255, int(240 - 150 * u), int(200 - 190 * u)); a = int(255 * (1 - u) ** 1.5 * fade); wd = w0 * (1 - u) + 2
            d.ellipse((tx - wd / 2, ty - wd / 2, tx + wd / 2, ty + wd / 2), fill=c + (a,))
        d.ellipse((hx - w0 * .7, hy - w0 * .7, hx + w0 * .7, hy + w0 * .7), fill=(255, 255, 240, int(255 * fade)))
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(9))); img.alpha_composite(lay)

def g_timeline(img, v, t0, t1):
    to = T['older']; mono(img, L('OLDER THAN EARTH', 'భూమి కంటే పాతది'), W / 2, 300, 34, AMBER, prog(v, to, to + .3))
    x = 150; ya, yb = 470, 1060; k = e_io(prog(v, t0 + .1, t0 + 1.8))
    d = ImageDraw.Draw(img); d.line((x, ya, x, ya + (yb - ya) * k), fill=CREAM + (220,), width=6)
    nodes = [(ya, L('STARS COLLIDE', 'స్టార్స్ ఢీ'), L('GOLD IS MADE', 'గోల్డ్ పుట్టింది'), GOLD, t0 + .1),
             (765, L('EARTH FORMS', 'భూమి పుట్టింది'), L('4.5 BILLION YEARS AGO', '450 కోట్ల ఏళ్ల క్రితం'), CREAM, max(t0 + .6, to - .3)),
             (yb, L('TODAY', 'ఈరోజు'), L('YOUR RING', 'మీ ఉంగరం'), GOLD, max(t0 + 1.2, to + .4))]
    for y, t, s, col, ti in nodes:
        if v < ti: continue
        kk = e_back(prog(v, ti, ti + .3)); put(img, sphere(26, col), x, y, 1, kk)
        text_plain(img, t, x + 70, y - 22, 56 if not TE else 48, col, prog(v, ti, ti + .2), anchor='l')
        mono(img, s, x + 72, y + 36, 26, CREAM, prog(v, ti + .1, ti + .3), anchor='l')

def g_stardust(img, v, t0, t1):
    rng = np.random.default_rng(21); lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    cx, cy = W / 2, 770
    for i in range(240):
        ang = rng.uniform(0, 2 * math.pi); r0 = rng.uniform(450, 1100); sp = rng.uniform(.8, 1.6); st = t0 + rng.uniform(0, .8)
        q = e_out(prog(v, st, st + sp)); rr = r0 * (1 - q) + rng.uniform(40, 260) * q; aa = ang + 2.2 * q
        x, y = cx + rr * math.cos(aa), cy + rr * .55 * math.sin(aa); s = rng.uniform(2, 6)
        tw = .6 + .4 * math.sin(v * 9 + i)
        d.ellipse((x - s, y - s, x + s, y + s), fill=(255, 210, 110, int(255 * prog(v, st, st + .2) * tw)))
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(3))); img.alpha_composite(lay)
    sc = e_back(prog(v, t0 + .2, t0 + .55)); big_text(img, L('STARDUST', 'స్టార్ ధూళి'), W / 2, 380, 150, GOLD, prog(v, t0 + .2, t0 + .35), sc)

# ---------------- subscribe button ----------------
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
        gd.ellipse((tx - R, ty - R, tx + R, ty + R), outline=(255, 255, 255, int(220 * (1 - rp))), width=6)
        gd.ellipse((tx - 22, ty - 22, tx + 22, ty + 22), fill=(255, 255, 255, int(200 * (1 - rp)))); img.alpha_composite(g)
SUB_T = T['today']
def sub_pop(img, v, t0, dur=3.0):
    if not (t0 <= v < t0 + dur): return
    a = prog(v, t0, t0 + .25) * (1 - prog(v, t0 + dur - .3, t0 + dur)); k = e_out(prog(v, t0, t0 + .35)); y = 150 + 110 * k
    sub_button(img, v, t0, W / 2, y, .8, tap=1.4)
    mono(img, L('A NEW WHY EVERY DAY', 'రోజూ ఒక కొత్త "ఎందుకు"'), W / 2, y + 80, 26 if not TE else 28, CREAM, a)

# ---------------- captions ----------------
CAP_Y = 1250
@functools.lru_cache(2)
def _capband():
    g = np.zeros((H, W, 4), np.uint8); y = np.arange(H)[:, None]
    g[..., 3] = (np.exp(-((y - CAP_Y) / 230.0) ** 2) * 150).astype(np.uint8); return Image.fromarray(g, 'RGBA')
def caption(img, v):
    cur = None
    for c in CH:
        if c[0] - .05 <= v < c[1]: cur = c
    img.alpha_composite(_capband())
    if not cur: return
    s0, e0, ws = cur; px = 82 if not TE else 76
    f = font('archivo', px) if not TE else font('tesans', px)
    toks = [x[2].upper() if not TE else x[2] for x in ws]
    sp = f.getlength(' '); wid = [f.getlength(t) for t in toks]; tot = sum(wid) + sp * (len(toks) - 1)
    lines = [list(range(len(toks)))]
    if tot > 960: cut = len(toks) // 2 + (len(toks) % 2); lines = [list(range(cut)), list(range(cut, len(toks)))]
    k = e_back(prog(v, s0 - .05, s0 + .12))
    for li, ln in enumerate(lines):
        lw = sum(wid[i] for i in ln) + sp * (len(ln) - 1); x = W / 2 - lw / 2; y = CAP_Y + (li - (len(lines) - 1) / 2) * px * 1.25
        for i in ln:
            active = ws[i][0] - .03 <= v < (ws[i + 1][0] if i + 1 < len(ws) else e0); said = v >= ws[i][0] - .03
            col = AMBER if active else (CREAM if said else (200, 196, 188)); sc = (1.08 if active else 1.0) * (.85 + .15 * k)
            im = Image.new('RGBA', (int(wid[i] + 40), int(px * 1.8)), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
            d.text((20, px * .9), toks[i], font=f, fill=col, anchor='lm', stroke_width=7, stroke_fill=(0, 0, 0))
            paste_c(img, im, x + wid[i] / 2, y, 1.0, sc); x += wid[i] + sp

def tag(img, text, x, y, a=1.0, px=24, fill=(10, 10, 10, 190), col=CREAM):
    if a <= 0: return
    f = mono_font(text, px); w = f.getlength(text) + (len(text) * 2 if not is_te(text) else 0) + 36; h = px * 1.9
    im = Image.new('RGBA', (int(w), int(h)), (0, 0, 0, 0)); ImageDraw.Draw(im).rounded_rectangle((0, 0, w - 1, h - 1), radius=10, fill=fill)
    alpha_paste(img, im, x, y, a); mono(img, text, x + 18, y + h / 2, px, col, a, anchor='l', track=2)
def credit(img, text, a=1.0):
    f = mono_font(text, 19); w = f.getlength(text) + len(text) * 1 + 28; tag(img, text, (W - w) / 2, H - 92, a * .95, px=19, col=(200, 196, 188))

# ---------------- frame ----------------
def scene_at(v):
    idx = 0
    for i, s in enumerate(SC):
        if v >= s['t'] - 1e-6: idx = i
    s = SC[idx]; t1 = SC[idx + 1]['t'] if idx + 1 < len(SC) else VLEN + TAIL
    return idx, s, t1

GFX = dict(fusion=g_fusion, scale=g_scale, collapse=g_collapse, sugar=g_sugar, nasa1=g_nasa1, y2017=g_2017, spectrum=g_spectrum,
           metals=g_metals, twist=g_twist, cutaway=g_cutaway, meteor=g_meteor, timeline=g_timeline, stardust=g_stardust)

def frame_at(Tt):
    v = Tt - LEAD; idx, s, t1 = scene_at(v); t0 = s['t']
    img = Image.new('RGBA', (W, H), (8, 8, 8, 255))
    background(img, s['bg'], v, t0, t1)
    k = s['kind']
    if k in GFX: GFX[k](img, v, t0, t1)
    elif k == 'why':
        sc = e_back(prog(v, t0, t0 + .35)); big_text(img, s['word'], W / 2, 820, 200 if not TE else 170, AMBER, prog(v, t0, t0 + .15), sc)
    elif k == 'big':
        bd = s.get('bd', .1); col = COL[s.get('bcol', 'amber')]
        if 'lab' in s: mono(img, s['lab'], W / 2, s['by'] - (130 if s.get('stamp') else s['bpx'] * (.75 if '\n' not in s['big'] else 1.3)), 30 if not TE else 32, CREAM, prog(v, t0, t0 + .3))
        if s.get('stamp'): stamp_text(img, s['big'], W / 2, s['by'], s['bpx'], col, v, t0 + bd)
        else:
            sc = e_back(prog(v, t0 + bd, t0 + bd + .35))
            if v >= t0 + bd: big_text(img, s['big'], W / 2, s['by'], s['bpx'], col, prog(v, t0 + bd, t0 + bd + .15), sc)
    elif k == 'plain' and s.get('pill'):
        pill(img, s['pill'], W / 2, 540, 38, AMBER, (10, 10, 10), prog(v, t0 + .1, t0 + .35), e_back(prog(v, t0 + .1, t0 + .45)))
    elif k == 'cta':
        text_plain(img, 'WHY?', W / 2, 600, 230, CREAM, prog(v, t0, t0 + .25))
        sub_button(img, v, t0 + 1.0, W / 2, 900, 1.2, tap=1.3)
        mono(img, s['src'], W / 2, 1640, 22 if not TE else 24, GREY, prog(v, t0 + 1.2, t0 + 1.6))
    if s.get('credit'): credit(img, s['credit'], prog(v, t0, t0 + .3))
    caption(img, v)
    mono(img, BRAND, W / 2, 120, 28, AMBER)
    if k != 'cta': tag(img, SERIES, 40, 175, 1.0, px=20, fill=(10, 10, 10, 170), col=AMBER)
    sub_pop(img, v, SUB_T)
    arr = np.asarray(img.convert('RGB'), np.float32)
    if k == 'nasa1' and T['crash'] <= v < T['crash'] + .35:          # impact shake
        sh = int(18 * (1 - prog(v, T['crash'], T['crash'] + .35)) * math.sin(v * 90)); arr = np.roll(arr, sh, axis=1)
    fade = 1 - prog(Tt, TOTAL - .35, TOTAL)
    return np.clip(arr * fade, 0, 255).astype(np.uint8)

# ---------------- audio ----------------
SFXD = '/home/claude/why-channel-studio/sfx/'
@functools.lru_cache(32)
def sfx(name, peak=.6):
    a = load_wav(SFXD + name + '.wav'); m = np.abs(a).max() + 1e-9; return a * (peak / m)

def build_audio(path):
    from scipy.ndimage import uniform_filter1d
    from pedalboard import Pedalboard, PeakFilter, HighShelfFilter, LowpassFilter, HighpassFilter
    n = int(TOTAL * SR) + SR; out = np.zeros((n, 2), np.float32)
    i0 = int(LEAD * SR); out[i0:i0 + len(voice)] += voice
    m = load_wav(G + 'music.wav')
    bed = Pedalboard([HighpassFilter(60), PeakFilter(cutoff_frequency_hz=2200, gain_db=-5, q=0.7), HighShelfFilter(cutoff_frequency_hz=6000, gain_db=-5), LowpassFilter(10000)])
    m = bed(m.T.copy(), SR).T.astype(np.float32)
    m = m[:n] if len(m) >= n else np.concatenate([m, np.zeros((n - len(m), 2), np.float32)])
    env = uniform_filter1d(np.abs(out[:, 0]), int(.12 * SR)); sc = np.clip(env / .04, 0, 1)
    g = float(os.environ.get('MGAIN', .24)) * (1 - .6 * sc)
    fi = int(.3 * SR); g[:fi] *= np.linspace(0, 1, fi)
    e = int((TOTAL - .05) * SR); fo = int(1.6 * SR); g[e - fo:e] *= np.linspace(1, 0, fo); g[e:] = 0
    def add(x, t, k=1.0, dur=None, fade=.05):
        x = x.copy()
        if dur: x = x[:int(dur * SR)]
        f = int(fade * SR)
        if len(x) > 2 * f: x[-f:] *= np.linspace(1, 0, f)[:, None]
        j = int((LEAD + t) * SR)
        if j < 0: x = x[-j:]; j = 0
        x = x[:max(0, n - j)]; out[j:j + len(x)] += x * k
    def amb(name, t0, t1, k, fin=.6, fout=.8):
        a = sfx(name); d = t1 - t0
        while len(a) < int(d * SR) + SR: a = np.concatenate([a, a])
        a = a[:int(d * SR)].copy(); fi_ = int(fin * SR); fo_ = int(fout * SR)
        a[:fi_] *= np.linspace(0, 1, fi_)[:, None]; a[-fo_:] *= np.linspace(1, 0, fo_)[:, None]
        add(a, t0, k, fade=.01)
    st = {s['kind'] + str(i): s['t'] for i, s in enumerate(SC)}
    nxt = lambda i: SC[i + 1]['t'] if i + 1 < len(SC) else VLEN
    # music drop for the twist
    for q, s in enumerate(SC):
        if s.get('drop'):
            d0 = int((LEAD + s['t'] - .05) * SR); d1 = int((LEAD + nxt(q) - .02) * SR); g[d0:d1] *= .0
            r = int(.3 * SR); g[d1:d1 + r] *= np.linspace(0, 1, r)
            add(sfx('riser'), s['t'] - 2.53, .55); add(sfx('boom_impact'), s['t'] + .05, .6)
    out += m * g[:, None]
    # hook
    add(sfx('boom_distant'), 0.0, .35); add(sfx('coins_clink'), .25, .18)
    for q, s in enumerate(SC):
        k = s['kind']; t0 = s['t']
        if q > 0 and s.get('sfx', True) and k not in ('twist',): add(sfx('woosh_air'), t0 - .25, .22, dur=1.0)
        if k == 'big':
            if s.get('stamp'): add(sfx('stamp'), t0 + s['bd'], .5)
            else: add(sfx('sub_knock'), t0 + s['bd'], .55)
        if k == 'why': add(sfx('woosh_deep'), t0 - .2, .3, dur=1.6)
    # fusion
    ts = [T['H'], T['He'], T['C']] + list(np.linspace(T['C'], T['Fe'], 6)[1:-1]) + [T['Fe']]
    for t in ts: add(sfx('tick'), t, .55)
    add(sfx('sub_knock'), T['Fe'], .5); add(sfx('stamp'), T['stop'], .55)
    tq = T['squeeze']
    while tq + .55 < T['H']: add(sfx('sub_knock'), tq + .55, .3); tq += 1.0
    # scale
    add(sfx('metal_transform'), T['heavy'] + .25, .25, dur=.9)
    # space: drone under collapse -> nasa
    amb('space_drone', T['giant'] - .2, T['glow'] + 1.0, .32)
    add(sfx('boom_distant'), T['collapse'] + .4, .6); add(sfx('woosh_tunnel'), T['collapse'] - .2, .2, dur=1.2)
    add(sfx('sub_knock'), T['cube'] + .3, .5); add(sfx('ticker_run'), T['weigh'], .35); add(sfx('sub_knock'), T['billion'] + .3, .55)
    add(sfx('riser'), T['crash'] - 2.53, .45); add(sfx('impact_trailer'), T['crash'] - 0.0, .75)
    add(sfx('shutter'), T['y2017'] + .05, .45); add(sfx('ticker_run'), T['away'], .3); add(sfx('paper_slide'), T['y2017'] + .9, .35)
    for i in range(10): add(sfx('tick'), T['glow'] + .7 + i * .12, .3)
    add(sfx('coins_clink'), min(T['goldw'], T['heavym'] + .25), .4); add(sfx('coin_prize'), min(T['goldw'], T['heavym'] + .25) + .45, .25, dur=.35)
    # young earth
    amb('lava_bubble', T['young'] - .1, T['today'] + .2, .45); add(sfx('sub_knock'), T['sank'], .5)
    amb('waterfall', T['today'] - .1, T['falling'] + .3, .22)
    add(sfx('meteor_fall'), T['falling'] + .15 + .75 - 2.54, .45); add(sfx('meteor_fall'), T['falling'] + 1.45 + .75 - 2.54, .3)
    add(sfx('swoosh_slow'), T['ring'], .2, dur=2.0)
    for t in [T['ring'] + .1, max(T['ring'] + .6, T['older'] - .3), max(T['ring'] + 1.2, T['older'] + .4)]: add(sfx('tick'), t, .55)
    add(sfx('sparkle_soft'), T['stardust'] + .1, .18)
    add(sfx('mouse_click'), SUB_T + 1.4, .45); add(sfx('mouse_click'), T['cta'] + 1.0 + 1.3, .5)
    import scipy.io.wavfile as wf
    wf.write(path + '.pre.wav', SR, (np.clip(out, -1, 1) * 32767).astype(np.int16))
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', path + '.pre.wav', '-af', 'loudnorm=I=-14:TP=-1:LRA=7', '-ar', '48000', path], check=True)

if __name__ == '__main__':
    mode = sys.argv[3] if len(sys.argv) > 3 else 'full'
    if mode == 'stills':
        for t in sys.argv[4].split(','): Image.fromarray(frame_at(float(t) + LEAD)).save(f"{OUT}/still_{float(t):06.2f}.jpg", quality=85)
        sys.exit()
    if mode == 'audio': build_audio(f"{OUT}/audio.wav"); sys.exit()
    if mode == 'part':
        i, nparts = int(sys.argv[4]), int(sys.argv[5]); N = int(TOTAL * FPS); a, b = N * i // nparts, N * (i + 1) // nparts
        p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                              '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p', f"{OUT}/part{i}.mp4"], stdin=subprocess.PIPE)
        for f in range(a, b): p.stdin.write(frame_at(f / FPS).tobytes())
        p.stdin.close(); p.wait(); print('part done', i)
