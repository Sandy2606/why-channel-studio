# Gold Short 2 "Why gold never rusts" (9:16, full-screen, explainer graphics)
# usage: PLAT=yt|ig python3 render_gold.py en|te OUTDIR [stills t,t | audio | part i n]
import sys, os, subprocess, functools, math
sys.path.insert(0, '/home/claude/elnino'); sys.path.insert(0, '/home/claude/gold2')
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from epic import load_wav, SR, FPS
from modern import *

LANG = sys.argv[1]; OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True)
TE = LANG == 'te'; W, H = 1080, 1920
PLAT = os.environ.get('PLAT', 'yt')
G = '/home/claude/gold2/'
voice = load_wav(G + f'voice_{LANG}_{PLAT}.wav'); VLEN = len(voice) / SR
LEAD = 0.15; TAIL = 0.7; TOTAL = LEAD + VLEN + TAIL
from cues_g2 import get_cues
SC, T = get_cues(LANG)
L = (lambda en, te: te if TE else en)
BRAND = 'WHY? తెలుగు' if TE else 'WHY?'
SERIES = L('GOLD', 'గోల్డ్')
BTN = ('FOLLOW', 'FOLLOWING') if PLAT == 'ig' else ('SUBSCRIBE', 'SUBSCRIBED')
from caps_g2 import words, chunks
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
    elif k == 'still': still_bg(img, b[1], v, t0, t1, b[2], b[3], b[4])
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

# ---------------- scene graphics (Short 2: why gold never rusts) ----------------
@functools.lru_cache(8)
def _still(name): return Image.open(G + 'media/' + name).convert('RGB')
def still_bg(img, name, v, t0, t1, dim, focus, zoom):
    s = _still(name); u = e_io(prog(v, t0, t1 + .5)); z = zoom[0] + (zoom[1] - zoom[0]) * u
    sc = max(W / s.width, H / s.height) * z; cw, ch = W / sc, H / sc
    x0 = (s.width - cw) * focus[0]; y0 = (s.height - ch) * focus[1]
    img.paste(s.resize((W, H), Image.BICUBIC, box=(x0, y0, x0 + cw, y0 + ch)), (0, 0))
    if dim: img.alpha_composite(Image.new('RGBA', (W, H), (0, 0, 0, int(255 * dim))))

def shine_sweep(img, v, t0, dur=.9, a=.55):
    q = prog(v, t0, t0 + dur)
    if q <= 0 or q >= 1: return
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); x = -400 + (W + 800) * e_io(q)
    d.polygon([(x - 90, 0), (x + 90, 0), (x - 330, H), (x - 510, H)], fill=(255, 245, 210, int(255 * a * math.sin(math.pi * q))))
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(40)))

def o2(img, x, y, ang=0.0, a=1.0, sep=0.0, s=1.0):
    r = int(24 * s); dx = (r * .8 + sep) * math.cos(ang); dy = (r * .8 + sep) * math.sin(ang)
    put(img, sphere(r, (230, 70, 60)), x - dx, y - dy, a); put(img, sphere(r, (230, 70, 60)), x + dx, y + dy, a)

def g_hook(img, v, t0, t1):
    ty = T['years']
    if v >= ty:
        k = e_out(prog(v, ty, ty + .8))
        big_text(img, f'{int(round(3300 * k)):,}', W / 2, 330, 170, AMBER, prog(v, ty, ty + .15), e_back(prog(v, ty, ty + .35)))
        mono(img, L('YEARS OLD · STILL SHINING', 'ఏళ్ళ వయసు · ఇంకా మెరుస్తోంది'), W / 2, 450, 30, CREAM, prog(v, ty + .3, ty + .6))
    shine_sweep(img, v, ty + 1.6, 1.0)

def g_rusty(img, v, t0, t1):
    mono(img, L('IRON · A FEW MONTHS OUTSIDE', 'ఐరన్ · కొన్ని నెలలు బయట'), W / 2, 330, 30, CREAM, prog(v, t0, t0 + .3))
    tr = T['rusty']
    if v >= tr: stamp_text(img, L('RUST', 'తుప్పు'), W / 2, 520, 130, (232, 110, 50), v, tr, rot=-6)

ORB = [(.0, -1), (.6, -1), (1.2, -1), (1.9, -1), (2.6, -1), (3.3, -1)]
def g_ironox(img, v, t0, t1):
    cx, cy, R = W / 2, 780, 210
    headline(img, L('RUST = OXYGEN EATING IRON', 'తుప్పు = ఆక్సిజన్ ఐరన్‌ని తినడం'), v, t0, W / 2, 360, 62 if not TE else 56, 1000)
    rk = e_io(prog(v, T['gives'] - .8, T['gives'] + .6))                       # rust spreading
    col = tuple(int(c0 * (1 - rk) + c1 * rk) for c0, c1 in zip((150, 152, 158), (178, 82, 36)))
    put(img, sphere(R, col), cx, cy); text_plain(img, 'Fe', cx, cy - 6, 96, WHITE, .9)
    mono(img, L('IRON', 'ఐరన్'), cx, cy + R + 40, 28, CREAM)
    rng = np.random.default_rng(5)
    for i in range(10):                                                         # O2 flies in and sticks
        st = t0 + .5 + i * .32; ang = rng.uniform(0, 2 * math.pi); q = e_out(prog(v, st, st + .45))
        if v < st: continue
        r0 = 700; r1 = R + 18; rr = r0 + (r1 - r0) * q; x, y = cx + rr * math.cos(ang), cy + rr * .9 * math.sin(ang)
        o2(img, x, y, ang + math.pi / 2, 1.0, s=.9)
    if v >= T['gives']:                                                         # flakes falling
        d = ImageDraw.Draw(img)
        for i in range(40):
            st = T['gives'] + rng.uniform(0, 1.2); q = prog(v, st, st + 1.4)
            if q <= 0 or q >= 1: continue
            x = cx + rng.uniform(-R * .8, R * .8); y = cy + R * .6 + 420 * q * q
            s = rng.uniform(5, 11); d.polygon([(x, y - s), (x + s, y), (x, y + s * .7), (x - s * .8, y)], fill=(176, 84, 40, int(255 * (1 - q))))
    if v >= t0 + .5: mono(img, L('O2 = OXYGEN', 'O2 = ఆక్సిజన్'), W / 2, 1080, 28, (240, 120, 110), prog(v, t0 + .5, t0 + .8))

def g_goldox(img, v, t0, t1):
    cx, cy, R = W / 2, 780, 170
    headline(img, L('GOLD HOLDS ITS ELECTRONS TIGHT', 'గోల్డ్ ఎలక్ట్రాన్స్‌ని గట్టిగా పట్టుకుంటుంది'), v, t0, W / 2, 360, 58 if not TE else 50, 1000)
    put(img, glow(320, (255, 190, 60), .6), cx, cy); put(img, sphere(R, GOLD), cx, cy); text_plain(img, 'Au', cx, cy - 6, 96, (40, 26, 6))
    d = ImageDraw.Draw(img); d.ellipse((cx - R - 40, cy - R - 40, cx + R + 40, cy + R + 40), outline=(255, 230, 160, 90), width=3)
    for j in range(4):                                                          # tight, fast electrons
        a = v * 5 + j * math.pi / 2; put(img, sphere(13, (150, 220, 255)), cx + (R + 40) * math.cos(a), cy + (R + 40) * math.sin(a))
    rng = np.random.default_rng(8)
    for i in range(9):                                                          # O2 bounces off
        st = t0 + .4 + i * .36; ang = rng.uniform(0, 2 * math.pi)
        if v < st: continue
        q = prog(v, st, st + 1.1); r1 = R + 70
        rr = 720 - (720 - r1) * e_out(q / .4) if q < .4 else r1 + 650 * e_io((q - .4) / .6)
        aa = ang if q < .4 else ang + .5
        if q < 1: o2(img, cx + rr * math.cos(aa), cy + rr * math.sin(aa), aa + math.pi / 2, min(1, (1 - q) * 3), s=.9)
    if v >= T['cant']:
        pill(img, L('NO GRIP', 'పట్టు దొరకదు'), W / 2, 1060, 40, AMBER, (10, 10, 10), prog(v, T['cant'], T['cant'] + .25), e_back(prog(v, T['cant'], T['cant'] + .3)))

def g_proof(img, v, t0, t1):
    mono(img, L('HERE IS WHAT BLEW MY MIND', 'నాకు షాకింగ్ అనిపించింది'), W / 2, 330, 30, AMBER, prog(v, t0, t0 + .3))
    ty = T['year']
    if v >= ty - .1:
        big_text(img, '2026', W / 2, 560, 220, CREAM, prog(v, ty - .1, ty + .05), e_back(prog(v, ty - .1, ty + .25)))
    if v >= ty + .5:
        news_card(img, 'SCIENCEALERT', 'MAY 22, 2026', 'Scientists Found The Atomic Reason That Gold Refuses to Rust', W / 2, 900, v, ty + .5, w=940, hl_words=(6, 7, 8))
        mono(img, 'TULANE UNIVERSITY · PHYSICAL REVIEW LETTERS', W / 2, 1065, 22, GREY, prog(v, ty + .9, ty + 1.2))

HEX = None
def _hexpts():
    pts = []; r = 46; dx = 2 * r * .98; dy = dx * math.sqrt(3) / 2
    for row in range(-5, 6):
        for col in range(-6, 7):
            x = W / 2 + col * dx + (row % 2) * dx / 2; y = 760 + row * dy
            if 60 < x < W - 60 and 450 < y < 1090: pts.append((x, y))
    return pts, r
def g_hexa(img, v, t0, t1):
    headline(img, L("GOLD'S SURFACE: A TIGHT HEXAGON", 'గోల్డ్ ఉపరితలం: టైట్ హెక్సాగన్'), v, t0, W / 2, 340, 58 if not TE else 50, 1000)
    pts, r = _hexpts(); cx, cy = W / 2, 760
    for (x, y) in pts:
        dd = math.hypot(x - cx, y - cy); st = t0 + .2 + dd / 900
        if v < st: continue
        put(img, sphere(r, GOLD, .8), x, y, 1, e_back(prog(v, st, st + .3)))
    if v >= t0 + 1.2:                                                           # highlight one hexagon
        a = prog(v, t0 + 1.2, t0 + 1.5); d = ImageDraw.Draw(img); R = 2 * r * .98
        hx = [(cx + R * math.cos(math.radians(60 * k)), cy + R * math.sin(math.radians(60 * k))) for k in range(7)]
        d.line(hx, fill=AMBER + (int(255 * a),), width=7, joint='curve')
    ts = T['split']
    if v >= ts:                                                                 # O2 lands, tries to split, fails, leaves
        q = v - ts
        if q < .5: y = 200 + (cy - 70 - 200) * e_out(q / .5); sep = 0
        elif q < 2.0: y = cy - 70; sep = 22 * abs(math.sin((q - .5) * 7)) * (1 - (q - .5) / 1.5)
        else: y = cy - 70 - 700 * e_io(min(1, (q - 2.0) / .8)); sep = 0
        if q < 2.8: o2(img, cx, y, 0, 1.0, sep=sep, s=1.2)
        if q > .6: pill(img, L("O2 CAN'T SPLIT", 'O2 విడిపోలేదు'), W / 2, 1100, 38, (230, 70, 60), WHITE, prog(v, ts + .6, ts + .85))

def g_aqua(img, v, t0, t1):
    ta, tr, tc = T['aqua'], T['royal'], T['acids']
    if v >= ta: pill(img, 'AQUA REGIA', W / 2, 380, 52, AMBER, (10, 10, 10), prog(v, ta, ta + .25), e_back(prog(v, ta, ta + .3)))
    if v >= tr: mono(img, L('= "ROYAL WATER"', '= "రాజ ద్రవం"'), W / 2, 470, 34, CREAM, prog(v, tr, tr + .3))
    if v >= tc:
        for i, (txt, ti) in enumerate([('NITRIC ACID', tc), ('HYDROCHLORIC ACID', tc + .45)]):
            if v < ti: continue
            k = e_back(prog(v, ti, ti + .3)); y = 680 + i * 170
            pill(img, txt, W / 2 + 60 * (1 - k), y, 40, (14, 14, 14, 230), CREAM, prog(v, ti, ti + .2))
            if i == 1: text_plain(img, '+', W / 2, 765, 70, AMBER, prog(v, ti, ti + .2))

def g_fav(img, v, t0, t1):
    sc = 1 + .05 * prog(v, t0, t1)
    big_text(img, L('MY FAVOURITE\nPART', 'నాకు బాగా నచ్చిన\nస్టోరీ'), W / 2, 820, int(120 * sc) if not TE else int(130 * sc), CREAM, prog(v, t0, t0 + .3))

def g_1940(img, v, t0, t1):
    stamp_text(img, '1940', W / 2, 520, 200, AMBER, v, t0 + .1, rot=-5)
    tn = t0 + .9
    if v >= tn:
        pill(img, L('NAZIS INVADE DENMARK', 'నాజీలు డెన్మార్క్‌పై దాడి'), W / 2, 760, 44, (230, 70, 60), WHITE, prog(v, tn, tn + .25), e_back(prog(v, tn, tn + .3)))
        mono(img, L('APRIL 9, 1940', 'ఏప్రిల్ 9, 1940'), W / 2, 845, 30, CREAM, prog(v, tn + .2, tn + .5))

@functools.lru_cache(8)
def medal(r, sh=1.0):
    im = sphere(r, GOLD, .7).copy(); d = ImageDraw.Draw(im); c = im.width / 2
    d.ellipse((c - r * .82, c - r * .82, c + r * .82, c + r * .82), outline=(150, 100, 20, 255), width=max(2, r // 18))
    f = font('archivo', max(10, int(r * .32))); d.text((c, c), 'NOBEL', font=f, fill=(110, 70, 10), anchor='mm'); return im
def g_medals(img, v, t0, t1):
    pill(img, L('NIELS BOHR INSTITUTE · COPENHAGEN', 'నీల్స్ బోర్ ఇన్‌స్టిట్యూట్ · కోపెన్‌హాగెన్'), W / 2, 330, 32, AMBER, (10, 10, 10), prog(v, t0, t0 + .3))
    for i, (x, nm) in enumerate([(320, 'MAX VON LAUE · 1914'), (760, 'JAMES FRANCK · 1925')]):
        ti = t0 + 1.4 + i * .45
        if v < ti: continue
        k = e_back(prog(v, ti, ti + .35)); put(img, glow(240, (255, 190, 60), .5), x, 760, prog(v, ti, ti + .3))
        put(img, medal(150), x, 760, 1, k); mono(img, nm, x, 960, 22, CREAM, prog(v, ti + .2, ti + .5))
    if v >= t0 + 2.4: mono(img, L('2 GOLD NOBEL MEDALS · HIDE THEM', '2 గోల్డ్ నోబెల్ మెడల్స్ · దాచాలి'), W / 2, 1060, 28, AMBER, prog(v, t0 + 2.4, t0 + 2.7))

JAR = (360, 470)
def draw_jar(img, cx, cy, s, tint, a=1.0):
    w, h = JAR[0] * s, JAR[1] * s; lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    lvl = cy - h * .5 + h * .22
    d.rounded_rectangle((cx - w / 2 + 10, lvl, cx + w / 2 - 10, cy + h / 2 - 10), radius=int(40 * s), fill=tint + (int(150 * a),))
    d.rounded_rectangle((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), radius=int(46 * s), outline=(220, 235, 240, int(220 * a)), width=max(3, int(7 * s)))
    d.rounded_rectangle((cx - w * .38, cy - h / 2 - 40 * s, cx + w * .38, cy - h / 2 + 6 * s), radius=int(10 * s), fill=(80, 80, 86, int(255 * a)))
    d.rounded_rectangle((cx - w * .34, cy + h * .02, cx + w * .34, cy + h * .2), radius=8, fill=(244, 241, 234, int(235 * a)))
    img.alpha_composite(lay); mono(img, 'AQUA REGIA', cx, cy + h * .11, max(12, int(26 * s)), (30, 30, 30), a)
    return lvl

def g_jar(img, v, t0, t1):
    td, tl, tw = T['dropin'], T['leave'], T['war']
    dk = prog(v, td + .9, td + 2.3)                                             # dissolve progress
    tint = tuple(int(c0 * (1 - dk) + c1 * dk) for c0, c1 in zip((200, 225, 150), (235, 150, 30)))
    mv = e_io(prog(v, tl + .3, tl + 1.1)); s = 1 - .3 * mv; cx = W / 2 - 150 * mv; cy = 760 + 170 * mv
    if mv > 0:                                                                  # the shelf + other bottles
        d = ImageDraw.Draw(img); a = int(255 * mv); sy = cy + JAR[1] * s / 2
        d.rectangle((60, sy, W - 60, sy + 22), fill=(120, 84, 50, a))
        for bx, bh in [(700, 260), (860, 190)]:
            d.rounded_rectangle((bx - 55, sy - bh, bx + 55, sy), radius=18, outline=(170, 170, 176, a), width=5, fill=(60, 70, 80, int(a * .6)))
    lvl = draw_jar(img, cx, cy, s, tint, prog(v, t0, t0 + .3))
    rng = np.random.default_rng(3)
    for i, ox in enumerate((-60, 60)):                                          # medals drop in, then dissolve
        st = td + .15 + i * .2
        if v < st: continue
        q = e_out(prog(v, st, st + .6)); y = cy - 700 * s * (1 - q) + 120 * s * q
        r = int(70 * s * (1 - dk) ** .8)
        if r > 4: put(img, medal(max(5, r)), cx + ox * s, y)
    if td + .8 <= v < td + 3.0:                                                 # fizz bubbles
        d = ImageDraw.Draw(img)
        for i in range(40):
            st = td + .8 + rng.uniform(0, 1.8); q = prog(v, st, st + .8)
            if 0 < q < 1:
                x = cx + rng.uniform(-120, 120) * s; y = cy + 150 * s - (cy + 150 * s - lvl) * q; rr = rng.uniform(4, 10) * s
                d.ellipse((x - rr, y - rr, x + rr, y + rr), outline=(255, 255, 255, int(200 * (1 - q))), width=2)
    if v >= tw:                                                                 # the whole war: years roll by
        k = prog(v, tw, tw + 1.6); yr = 1940 + int(round(5 * k))
        big_text(img, str(yr), W / 2, 360, 150, CREAM, prog(v, tw, tw + .2)); mono(img, L('UNTOUCHED', 'ఎవరూ ముట్టుకోలేదు'), W / 2, 460, 30, AMBER, prog(v, tw + .3, tw + .6))
    elif v >= td: mono(img, L('MEDALS → DISSOLVED', 'మెడల్స్ కరిగిపోయాయి'), W / 2, 360, 32, AMBER, prog(v, td + 1.2, td + 1.6))

def g_recast(img, v, t0, t1):
    cx, cy = W / 2 - 150, 930; s = .7
    k1 = prog(v, t0 + .2, t0 + 1.4)                                             # gold settles out of the liquid
    tint = tuple(int(c0 * (1 - k1) + c1 * k1) for c0, c1 in zip((235, 150, 30), (200, 225, 150)))
    jar_a = 1 - prog(v, t0 + 2.0, t0 + 2.5)
    d = ImageDraw.Draw(img); sy = cy + JAR[1] * s / 2; d.rectangle((60, sy, W - 60, sy + 22), fill=(120, 84, 50, int(255 * jar_a)))
    if jar_a > 0:
        draw_jar(img, cx, cy, s, tint, jar_a); rng = np.random.default_rng(12)
        for i in range(70):
            x = cx + rng.uniform(-100, 100); y0 = cy - 60 + rng.uniform(-40, 60); q = e_io(prog(v, t0 + .2 + rng.uniform(0, .6), t0 + 1.4))
            y = y0 + (sy - 30 - y0) * q; d.ellipse((x - 5, y - 5, x + 5, y + 5), fill=GOLD + (int(255 * jar_a),))
    for i, x in enumerate((360, 720)):                                         # medals reborn
        ti = t0 + 2.2 + i * .3
        if v < ti: continue
        k = e_back(prog(v, ti, ti + .4)); put(img, glow(260, (255, 200, 80), .6), x, 760, prog(v, ti, ti + .3)); put(img, medal(140), x, 760, 1, k)
    if v >= t0 + 2.6:
        pill(img, L('RECAST · 1952', 'మళ్ళీ తయారు · 1952'), W / 2, 380, 44, AMBER, (10, 10, 10), prog(v, t0 + 2.6, t0 + 2.85), e_back(prog(v, t0 + 2.6, t0 + 2.9)))
    if v >= T['came']: shine_sweep(img, v, T['came'], .9, .45)

def g_chips(img, v, t0, t1):
    items = [(L('NO RUST', 'తుప్పు పట్టదు'), T['rust2']), (L('NO FADE', 'రంగు పోదు'), T['fade']), (L('ALWAYS COMES BACK', 'తిరిగి వస్తుంది'), T['comes'])]
    for i, (txt, ti) in enumerate(items):
        if v < ti: continue
        k = e_back(prog(v, ti, ti + .3)); y = 440 + i * 150
        pill(img, txt, W / 2 - 70 * (1 - k), y, 50, (14, 12, 8, 235), GOLD, prog(v, ti, ti + .15))
    tc = T['costly']
    if v >= tc:
        big_text(img, L('= SO EXPENSIVE', '= అందుకే కాస్ట్లీ'), W / 2, 960, 110 if not TE else 120, AMBER, prog(v, tc, tc + .15), e_back(prog(v, tc, tc + .35)))

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
SUB_T = T['invinc'] + .2
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

GFX = dict(hook=g_hook, rusty=g_rusty, ironox=g_ironox, goldox=g_goldox, proof=g_proof, hexa=g_hexa, aqua=g_aqua, fav=g_fav,
           y1940=g_1940, medals=g_medals, jar=g_jar, recast=g_recast, chips=g_chips)

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
    m = load_wav('/home/claude/gold1/music.wav')
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
    d0 = int((LEAD + T['fav'] - .05) * SR); d1 = int((LEAD + T['y1940'] + .1) * SR); g[d0:d1] *= .15
    r = int(.3 * SR); g[d1:d1 + r] *= np.linspace(.15, 1, r) / np.maximum(1e-3, np.linspace(1, 1, r))
    out += m * g[:, None]
    # hook
    add(sfx('boom_distant'), 0.0, .3); add(sfx('ticker_run'), T['years'], .35); add(sfx('woosh_air'), T['years'] + 1.55, .18, dur=1.0)
    for q, s in enumerate(SC):
        k = s['kind']; t0 = s['t']
        if q > 0 and s.get('sfx', True) and k not in ('fav',): add(sfx('woosh_air'), t0 - .25, .2, dur=1.0)
        if k == 'big':
            if s.get('stamp'): add(sfx('stamp'), t0 + s['bd'], .5)
            else: add(sfx('sub_knock'), t0 + s['bd'], .55)
    add(sfx('stamp'), T['rusty'], .45)
    for i in range(10): add(sfx('tick'), T['oxy'] + .5 + i * .32 + .45, .35)
    add(sfx('paper_drop'), T['gives'], .3)
    for i in range(9): add(sfx('tick'), T['grip'] + .4 + i * .36 + .44, .3)
    add(sfx('sub_knock'), T['cant'], .5)
    add(sfx('shutter'), T['year'] - .1, .4); add(sfx('paper_slide'), T['year'] + .5, .35)
    add(sfx('ticker_run'), T['hexa'] + .2, .3); add(sfx('marker'), T['hexa'] + 1.2, .25, dur=.6)
    for j in range(4): add(sfx('sub_knock'), T['split'] + .5 + j * .45, .28)
    add(sfx('woosh_air'), T['split'] + 2.0, .25, dur=1.0)
    amb('water_bubbles', T['liquid'], T['fav'] - .1, .3)
    for t in (T['aqua'], T['acids'], T['acids'] + .45): add(sfx('sub_knock'), t, .45)
    # music drop into the 1940 story
    d0 = int((LEAD + T['fav'] - .05) * SR); d1 = int((LEAD + T['y1940'] + .1) * SR)
    add(sfx('riser'), T['y1940'] + .1 - 2.53, .45); add(sfx('boom_impact'), T['y1940'] + .1, .55)
    add(sfx('stamp'), T['y1940'] + .1, .4)
    for i in range(2): add(sfx('coin_flutter'), T['medals'] + 1.4 + i * .45 - .6, .45)
    for i in range(2): add(sfx('coin_flutter'), T['dropin'] + .15 + i * .2 + .6 - .6, .35)
    amb('water_bubbles', T['dropin'] + .7, T['dropin'] + 3.0, .5, fin=.2)
    add(sfx('jar_set_down'), T['leave'] + 1.1, .7)
    add(sfx('ticker_run'), T['war'], .35)
    add(sfx('metal_transform'), T['back'] + 2.2, .25, dur=.9); add(sfx('coins_clink'), T['came'], .35)
    for t in (T['rust2'], T['fade'], T['comes']): add(sfx('sub_knock'), t, .45)
    add(sfx('coins_clink'), T['costly'], .35)
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
