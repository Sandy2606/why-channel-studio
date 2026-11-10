"""GOLDEN SPARROW · 2/6 Short renderer (9:16). Env: LANGV=en|te, PLAT=yt|ig.
usage: render.py <t_start> <t_end> <out.mp4>   (frame range by seconds)"""
import os, sys, math, json, functools, subprocess
import numpy as np, cairo
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops
sys.path.insert(0, '/home/claude/why-channel-studio/pipeline/styles'); sys.path.insert(0, '/home/claude/why-channel-studio/pipeline/style_v2')
sys.path.insert(0, '/home/claude/gs/film3'); sys.path.insert(0, '/home/claude/gs/vis'); sys.path.insert(0, '/home/claude/gs2')
_argv = sys.argv; sys.argv = sys.argv[:1]
import flib as FL
sys.argv = _argv
from core import Stage, text, pill, font, pick, fit, wrap, radial_bg, glow, grain, clamp, prog, e_out, e_io, e_back, lerp, mix, INK, CREAM, AMBER, GREY
import cartoon_explainer as CE
import cta_card as CTA
from cues import *

W, H = 1080, 1920
ST = Stage('9x16')
LINES = json.load(open(ROOT + 'lines.json'))[LANGV]
GOLD = (255, 190, 80)

# ------------------------------------------------------------------ helpers
def cover(arr, u, c0, c1, z0, z1):
    """camera move on a still (graded RGB array) -> PIL RGB 1080x1920"""
    h, w = arr.shape[:2]; base = max(W / w, H / h); k = e_io(clamp(u)); z = lerp(z0, z1, k); sc = base * z
    fx, fy = lerp(c0[0], c1[0], k), lerp(c0[1], c1[1], k); hw, hh = W / 2 / sc, H / 2 / sc
    cx = min(max(fx * w, hw), w - hw); cy = min(max(fy * h, hh), h - hh)
    box = (cx - hw, cy - hh, cx + hw, cy + hh)
    return Image.fromarray(arr).resize((W, H), Image.BILINEAR, box=box)

@functools.lru_cache(8)
def IMG(key): return FL.img(key)

def darken(im, k=0.55, vign=True):
    a = np.asarray(im).astype(np.float32) * k
    if vign:
        yy, xx = np.mgrid[0:H, 0:W]; r = np.sqrt(((xx - W / 2) / (W * .75)) ** 2 + ((yy - H / 2) / (H * .62)) ** 2); a *= np.clip(1.15 - .55 * r, .35, 1)[..., None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))

@functools.lru_cache(1)
def VIG():
    yy, xx = np.mgrid[0:H, 0:W]; r = np.sqrt(((xx - W / 2) / (W * .75)) ** 2 + ((yy - H / 2) / (H * .62)) ** 2); return np.clip(1.15 - .55 * r, .35, 1)[..., None].astype(np.float32)

def grade(im, k=0.6):
    a = np.asarray(im).astype(np.float32) * k * VIG(); return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))

def tx(img, s, x, y, px, col=CREAM, anchor='mm', kind='head', a=1.0, maxw=None, shadow=(0, 0, 0)):
    text(img, s, x, y, px, col, anchor, kind, a, maxw, shadow if a >= 1 else None)

def chip(img, s, cx, cy, px=38, bg=AMBER, fg=INK, a=1.0, scale=1.0, kind='head', outline=None):
    pill(img, s, cx, cy, px, bg, fg, a, scale, kind, maxw=ST.sw, outline=outline)

def dark_panel(img, box, r=30, a=200, outline=None):
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); d.rounded_rectangle(box, r, fill=(12, 12, 14, a), outline=outline, width=4 if outline else 0)
    img.paste(lay, (0, 0), lay)

# ------------------------------------------------------------------ maps (gold undivided subcontinent / Republic of India)
import gsmap
@functools.lru_cache(4)
def map_layer(kind, wpx):
    if kind == 'undivided': polys = [list(q) for q in gsmap.india_polys() if len(q) > 2] + [q for n in ('Pakistan', 'Bangladesh') for q in gsmap.polys(n) if len(q) > 2]
    else: polys = [list(q) for q in gsmap.india_polys() if len(q) > 2]
    allp = [list(q) for q in gsmap.india_polys() if len(q) > 2] + [q for n in ('Pakistan', 'Bangladesh') for q in gsmap.polys(n) if len(q) > 2]
    xs = [x for q in allp for x, y in q]; ys = [y for q in allp for x, y in q]
    bx0, bx1, by0, by1 = min(xs), max(xs), min(ys), max(ys); sc = wpx / (bx1 - bx0); hp = int((by1 - by0) * sc) + 2
    SS = 2; m = Image.new('L', (wpx * SS, hp * SS), 0); d = ImageDraw.Draw(m)
    for q in polys: d.polygon([((x - bx0) * sc * SS, (y - by0) * sc * SS) for x, y in q], fill=255)
    ghost = Image.new('L', (wpx * SS, hp * SS), 0); dg = ImageDraw.Draw(ghost)
    for q in allp: dg.polygon([((x - bx0) * sc * SS, (y - by0) * sc * SS) for x, y in q], outline=255, width=3 * SS)
    m = m.resize((wpx, hp), Image.LANCZOS); ghost = ghost.resize((wpx, hp), Image.LANCZOS)
    pad = 60; out = Image.new('RGBA', (wpx + 2 * pad, hp + 2 * pad), (0, 0, 0, 0))
    big = Image.new('L', out.size, 0); big.paste(m, (pad, pad)); gl = big.filter(ImageFilter.GaussianBlur(22))
    g = Image.new('RGBA', out.size, GOLD + (0,)); g.putalpha(gl.point(lambda x: int(x * .7))); out.alpha_composite(g)
    if kind != 'undivided':
        gh = Image.new('RGBA', out.size, (150, 140, 120, 0)); gb = Image.new('L', out.size, 0); gb.paste(ghost, (pad, pad)); gh.putalpha(gb.point(lambda x: int(x * .55))); out.alpha_composite(gh)
    yy = np.linspace(0, 1, out.size[1])[:, None, None]; rgb = (np.array([255, 214, 120]) * (1 - yy) + np.array([196, 120, 30]) * yy) * np.ones((1, out.size[0], 1))
    fill = Image.fromarray(rgb.astype(np.uint8), 'RGB').convert('RGBA'); fill.putalpha(big); out.alpha_composite(fill)
    edge = ImageChops.subtract(big.filter(ImageFilter.MaxFilter(3)), big); e = Image.new('RGBA', out.size, (120, 70, 16, 0)); e.putalpha(edge); out.alpha_composite(e)
    return out

def paste_c(img, lay, cx, cy, a=1.0, s=1.0):
    if a <= 0.01 or s <= 0.01: return
    if s != 1.0: lay = lay.resize((max(1, int(lay.width * s)), max(1, int(lay.height * s))), Image.BILINEAR)
    if a < 1: lay = lay.copy(); lay.putalpha(lay.getchannel('A').point(lambda p: int(p * a)))
    img.paste(lay, (int(cx - lay.width / 2), int(cy - lay.height / 2)), lay)

# ------------------------------------------------------------------ voice envelopes for the cartoons
@functools.lru_cache(1)
def ENV():
    full = CE.voice_envelope(ROOT + f'voice_{LANGV}.wav', FPS); lead = int(LEAD * FPS); full = [0.0] * lead + full
    def gated(keys):
        e = [0.0] * len(full)
        for k in keys:
            if k in M:
                for i in range(int(S(k) * FPS), min(len(full), int(E(k) * FPS) + 1)): e[i] = full[i]
        return e
    return {'ANNA': gated([]), 'CHELLI': gated(['Q1', 'Q2', 'Q3'])}

def cartoon(t, s0, lines):
    v = t - s0; f0 = int(round(s0 * FPS)); env = {k: e[f0:] for k, e in ENV().items()}
    spec = dict(topic='', lines=[dict(who=w, t0=S(k) - s0, t1=E(k) - s0 + .05, text=LINES[k]) for w, k in lines], env=env, fps=FPS)
    return CE.draw(ST, v, spec)

# ------------------------------------------------------------------ overlays: series tag, progress chips, captions
TAG = L('GOLDEN SPARROW · 2/6', 'బంగారు పిచ్చుక · 2/6')
CHIPS = [('Q1', L('1/3 · THE HANDS', '1/3 · చేతులు')), ('Q2', L('2/3 · THE SECRET', '2/3 · అసలు రహస్యం')), ('Q3', L('3/3 · THE BANS', '3/3 · నిషేధాలు'))]

def overlays(img, t, scn):
    if scn in ('slide',): return
    a = 1.0
    if scn == 'loop': a = 1.0
    # series tag (top-left, every scene)
    f = pick(TAG, 'monob', 30); w = int(f.getlength(TAG)) + 40
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); d.rounded_rectangle((70, 150, 70 + w, 150 + 56), 28, fill=(10, 10, 10, 200)); d.ellipse((86, 170, 102, 186), fill=AMBER + (255,))
    img.paste(lay, (0, 0), lay); text(img, TAG, 112, 178, 30, AMBER, 'lm', 'monob')
    # progress chip (current section), top-right under tag
    if scn not in ('hook', 'loop'):
        cur = None
        for k, s in CHIPS:
            if t >= S(k) - 0.15: cur = s
        if cur: chip(img, cur, W - 70 - pick(cur, 'head', 32).getlength(cur) / 2 - 26, 178, 32, CREAM, INK)

def captions(img, t, scn):
    if scn in ('cartoon1', 'cartoon2', 'cartoon3', 'slide'): return
    cur = [w for w in WORDS if w[0] - 0.05 <= t <= w[1] + 0.25]
    if not cur: return
    key = cur[-1][3]; ws = [w for w in WORDS if w[3] == key]; i = ws.index(cur[-1])
    # chunk of up to 4 words (EN) / 3 words (TE), break on sentence ends
    n = 3 if TE else 4; chunks = []; c = []
    for w in ws:
        c.append(w)
        if len(c) >= n or w[2][-1:] in '.?!…,:': chunks.append(c); c = []
    if c: chunks.append(c)
    ch = next(c for c in chunks if cur[-1] in c)
    if t > ch[-1][1] + 0.25: return
    if scn == 'loop' and t > DUR - 0.6: return
    px = 58 if not TE else 54; y = 1400
    s = ' '.join(w[2] for w in ch); f, px = fit(s, 'head', px, ST.sw - 40)
    widths = [pick(w[2], 'head', px).getlength(w[2]) for w in ch]; sp = f.getlength(' '); tot = sum(widths) + sp * (len(ch) - 1); x = W / 2 - tot / 2
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); d.rounded_rectangle((W / 2 - tot / 2 - 30, y - px * .85, W / 2 + tot / 2 + 30, y + px * .85), 26, fill=(8, 8, 8, 170)); img.paste(lay, (0, 0), lay)
    for w, wd in zip(ch, widths):
        on = w[0] - 0.05 <= t
        text(img, w[2], x, y, px, AMBER if (on and t <= w[1] + 0.12) else CREAM, 'lm', 'head', 1.0 if on else 0.55)
        x += wd + sp


# ------------------------------------------------------------------ GS 2/6 scenes
ACC = AMBER
NODES = [('B2', L('SPINNER', 'వడికేవారు')), ('2.3', L('WEAVER', 'నేతగాళ్లు')), ('2.4', L('DYER', 'రంగులు')), ('WEEKS', L('CHINTZ', 'అచ్చు గుడ్డ')),
         ('2.10', L('EUROPE', 'యూరప్')), ('2.11', L('BANS', 'నిషేధాలు')), ('T', L('PORT', 'రేవు'))]
def node_times():
    out = []
    for k, lab in NODES:
        out.append((AT('2.6', 'weeks', 'వారాల') if k == 'WEEKS' else S(k) - 0.1, lab))
    return out
NT = node_times()

def thread_chain(img, t, scn):
    """7-node cotton-thread chain under the tag; current node labelled."""
    if scn in ('hook', 'cartoon1', 'slide', 'loop', 'globe') or t < NT[0][0]: return
    n = sum(1 for c, _ in NT if t >= c); x0, x1, y = 110, 970, 262
    xs = [x0 + i * (x1 - x0) / 6 for i in range(7)]
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rounded_rectangle((x0 - 40, y - 26, x1 + 40, y + 70), 24, fill=(10, 10, 10, 150))
    pts = [(x, y + 5 * math.sin(x / 37 + t * 2)) for x in np.linspace(x0, x1, 120)]
    d.line(pts, fill=(120, 110, 96, 255), width=3)
    lit_end = xs[n - 1] if n >= 1 else x0
    c_last = NT[n - 1][0]; k = e_out(prog(t, c_last, c_last + 0.6)); lit_end = xs[max(0, n - 2)] + (xs[n - 1] - xs[max(0, n - 2)]) * k if n >= 2 else xs[0]
    d.line([p for p in pts if p[0] <= lit_end], fill=ACC + (255,), width=5)
    for i, x in enumerate(xs):
        on = i < n; r = 11 if on else 8
        if i == n - 1: r = 11 + 5 * (1 - k)
        d.ellipse((x - r, y - r, x + r, y + r), fill=(ACC + (255,)) if on else (70, 66, 60, 255), outline=(250, 240, 220, 255) if i == n - 1 else None, width=3)
    img.paste(lay, (0, 0), lay)
    lab = NT[n - 1][1]; text(img, lab, xs[n - 1], y + 44, 26, ACC, 'mm', 'monob')

def thread_sweep(img, t):
    """the thread draws across the cut at each node change"""
    for c, _ in NT[1:]:
        if c <= t < c + 0.75:
            u = e_io(prog(t, c, c + 0.55)); a = 1 - prog(t, c + 0.45, c + 0.75)
            lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
            xs = np.linspace(-40, W + 40, 160); xe = -40 + (W + 80) * u
            pts = [(x, 1150 - 0.55 * (x - 0) + 28 * math.sin(x / 70)) for x in xs if x <= xe]
            if len(pts) > 1:
                d.line(pts, fill=ACC + (int(255 * a),), width=7)
                glow_ = lay.filter(ImageFilter.GaussianBlur(10)); img.paste(glow_, (0, 0), glow_); img.paste(lay, (0, 0), lay)

def stamp(img, t1, t2, cx, cy, k, rot=-6, px=80):
    lay = Image.new('RGBA', (820, 240), (0, 0, 0, 0)); dl = ImageDraw.Draw(lay)
    dl.rounded_rectangle((8, 8, 812, 232), 24, fill=(14, 12, 10, 215), outline=ACC + (255,), width=12)
    f1, _ = fit(t1, 'head', px, 740); f2, _ = fit(t2, 'monob', 44, 740) if t2 else (None, 0)
    dl.text((410, 92 if t2 else 120), t1, font=f1, fill=ACC + (255,), anchor='mm')
    if t2: dl.text((410, 176), t2, font=f2, fill=ACC + (255,), anchor='mm')
    lay = lay.rotate(rot, expand=True, resample=Image.BICUBIC); paste_c(img, lay, cx, cy, clamp(k), 1.5 - .5 * min(1, k))

@functools.lru_cache(1)
def DRESS():
    im = Image.open(FL.A['PD04']).convert('RGB'); s = 1500 / im.height; return im.resize((int(im.width * s), 1500), Image.LANCZOS)
@functools.lru_cache(1)
def ACT():
    im = Image.open(FL.A['PD03']).convert('RGB'); w, h = im.size; return im.crop((int(w * .08), int(h * .05), int(w * .95), int(h * .36)))

def on_dark(im, cy=960, z=1.0):
    bg = Image.new('RGB', (W, H), (18, 16, 14)); dd = im.resize((int(im.width * z), int(im.height * z)), Image.BILINEAR)
    bg.paste(dd, (int(W / 2 - dd.width / 2), int(cy - dd.height / 2))); return grade(bg, .92)

def s_hook(t, s0, s1, frame0=False):
    img = on_dark(DRESS(), 980, 1.0 + .03 * t)
    stamp(img, L('LAW PASSED · 1721', 'చట్టం ఆమోదం · 1721'), None, W / 2, 640, 1.0 if frame0 or t < 0.01 else max(0.85, e_back(prog(t, 0, .35))), -6, 84)
    c2 = AT('0.1', 'wearing', 'కొన్ని') - 0.2
    if not frame0:
        k2 = e_back(prog(t, c2, c2 + .3))
        if k2 > .01: stamp(img, L('IN FORCE · 25 DEC 1722', 'అమలు · 25 డిసెంబర్ 1722'), None, W / 2, 900, k2, 4, 70)
        k3 = e_out(prog(t, c2 + .7, c2 + 1.1))
        if k3 > .01: chip(img, L('CERTAIN PRINTED CALICOES · SOME EXCEPTIONS', 'కొన్ని రకాల అచ్చు calico లు · కొన్ని మినహాయింపులు'), W / 2, 1150, 34, CREAM, INK, a=k3, scale=k3)
    text(img, 'Dress in chintz, c.1770–90 · Hugo Maertens · CC BY-SA 3.0', W / 2, 1690, 22, GREY, kind='mono')
    return img

def s_still(key, t, s0, s1, c0, c1, z0, z1, k=.92):
    return grade(cover(IMG(key), (t - s0) / max(.1, s1 - s0), c0, c1, z0, z1), k)

def s_boll(t, s0, s1):
    img = s_still('G04', t, s0, s1, (.5, .45), (.52, .42), 1.05, 1.25)
    u = e_io(prog(t, s0 + .3, s1 - .3)); lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    xs = np.linspace(540, W + 60, 140); xe = 540 + (W + 60 - 540) * u
    pts = [(x, 880 - .35 * (x - 540) + 22 * math.sin((x - 540) / 45 + t * 3)) for x in xs if x <= xe]
    if len(pts) > 1: d.line(pts, fill=(250, 244, 230, 255), width=6); g = lay.filter(ImageFilter.GaussianBlur(8)); img.paste(g, (0, 0), g); img.paste(lay, (0, 0), lay)
    return img

def grid_bg():
    img = radial_bg(W, H, (22, 24, 30), (8, 8, 10), cy=.5, reach=.8).copy(); d = ImageDraw.Draw(img)
    for x in range(0, W, 60): d.line([(x, 0), (x, H)], fill=(26, 28, 34), width=1)
    for y in range(0, H, 60): d.line([(0, y), (W, y)], fill=(26, 28, 34), width=1)
    return img

def s_spin(t, s0, s1):
    c = AT('2.2', 'many', 'ఎంతోమంది') - 0.15
    if t < c: return s_still('T5', t, s0, c, (.30, .55), (.25, .55), 1.0, 1.15)
    img = grid_bg(); d = ImageDraw.Draw(img); v = t - c
    lx, ly = W / 2, 1180
    for i in range(8):
        ka = e_out(prog(v, i * .12, i * .12 + .35))
        if ka <= 0: continue
        ang = math.pi * (0.1 + 0.8 * i / 7); x = W / 2 - 400 * math.cos(ang); y = 760 - 330 * math.sin(ang)
        r = 34 * ka; d.ellipse((x - r, y - r, x + r, y + r), outline=CREAM, width=5)
        for j in range(6):
            a = j * math.pi / 3 + t * 2; d.line([(x, y), (x + r * math.cos(a), y + r * math.sin(a))], fill=CREAM, width=2)
        kt = e_io(prog(v, .4 + i * .1, 1.2 + i * .1))
        if kt > 0:
            pts = [(lerp(x, lx, s_) + 30 * math.sin(s_ * 6 + i), lerp(y, ly - 90, s_)) for s_ in np.linspace(0, kt, 30)]
            d.line(pts, fill=ACC, width=3)
    kl = e_out(prog(v, 1.0, 1.5))
    if kl > 0:
        d.rounded_rectangle((lx - 170, ly - 90, lx + 170, ly + 90), 18, outline=ACC, width=7)
        for j in range(9): d.line([(lx - 140 + j * 35, ly - 70), (lx - 140 + j * 35, ly + 70)], fill=(200, 170, 110), width=2)
    tx(img, L('MANY SPINNERS', 'ఎంతోమంది వడికేవాళ్లు'), W / 2, 420, 58, CREAM)
    if kl > .01: chip(img, L('ONE LOOM', 'ఒక్క మగ్గం'), W / 2, 1330 - 20, 44, AMBER, INK, a=kl, scale=kl)
    return img

def s_loom(t, s0, s1):
    img = s_still('T6', t, s0, s1, (.45, .5), (.52, .5), 1.0, 1.12)
    c1 = AT('2.3', 'advance', 'ముందుగానే') - 0.1; c2 = AT('2.3', 'price.', 'ధర') - 0.1; c3 = AT('2.3', 'bargaining', 'బేరమాడే') - 0.2
    if t < c1:
        k = e_out(prog(t, s0 + .2, s0 + .6)); chip(img, L('WEAVER · PIT LOOM', 'నేతగాడు · గుంట మగ్గం'), W / 2, 420, 40, CREAM, INK, a=k, scale=k); return img
    if t < c2:
        k = e_back(prog(t, c1, c1 + .35)); dark_panel(img, (150, 360, 930, 560), 28, int(220 * min(1, k)), ACC + (255,))
        text(img, L('BROKER → WEAVER', 'దళారి → నేతగాడు'), W / 2, 410, 34, GREY, kind='monob', a=min(1, k))
        text(img, L('PAID IN ADVANCE', 'ముందుగానే డబ్బు'), W / 2, 490, 56, ACC, kind='head', a=min(1, k)); return img
    if t < c3:
        k = e_back(prog(t, c2, c2 + .35)); dark_panel(img, (150, 360, 930, 560), 28, int(220 * min(1, k)), ACC + (255,))
        text(img, L('PRICE', 'ధర'), W / 2, 410, 34, GREY, kind='monob', a=min(1, k))
        text(img, L('SET BY THE BROKER', 'దళారి నిర్ణయం'), W / 2, 490, 56, ACC, kind='head', a=min(1, k)); return img
    k = e_out(prog(t, c3, c3 + .3)); lv = lerp(.85, .15, e_io(prog(t, c3 + .2, c3 + 1.4)))
    dark_panel(img, (150, 340, 930, 600), 28, int(220 * k), ACC + (255,))
    text(img, L('BARGAINING POWER', 'బేరమాడే శక్తి'), W / 2, 400, 44, CREAM, kind='head', a=k)
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rounded_rectangle((210, 470, 870, 530), 30, fill=(60, 60, 66, int(255 * k))); d.rounded_rectangle((210, 470, 210 + 660 * lv, 530), 30, fill=ACC + (int(255 * k),))
    img.paste(lay, (0, 0), lay); return img

def s_dyer(t, s0, s1): return s_still('G06', t, s0, s1, (.5, .5), (.45, .55), 1.0, 1.15)

@functools.lru_cache(1)
def SWATCH():
    im = Image.open(FL.A['PD20c']).convert('RGB'); w, h = im.size; return im.crop((int(w * .22), int(h * .25), int(w * .50), int(h * .53))).resize((560, 560), Image.LANCZOS)

def s_wash(t, s0, s1):
    img = grid_bg(); v = t - s0; d = ImageDraw.Draw(img)
    wy = 1060; dip = e_io(prog(v, .6, 1.6)) * (1 - e_io(prog(v, 2.4, 3.4)))
    sy = 760 + 330 * dip; sw = SWATCH()
    img.paste(sw, (int(W / 2 - 280), int(sy - 280)))
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dl = ImageDraw.Draw(lay)
    dl.rectangle((0, wy, W, 1330), fill=(40, 90, 130, 200))
    for i in range(6):
        yy = wy + 4 * math.sin(t * 3 + i); dl.arc((80 + i * 160, yy - 14, 220 + i * 160, yy + 14), 0, 180, fill=(170, 210, 235, 220), width=3)
    img.paste(lay, (0, 0), lay)
    kd = e_out(prog(v, 0.1, 0.5)); chip(img, L('ILLUSTRATIVE DEMONSTRATION', 'ఉదాహరణ ప్రదర్శన'), W / 2, 380, 30, CREAM, INK, a=kd, scale=kd)
    ka = e_out(prog(v, 3.3, 3.7))
    if ka > .01: tx(img, L('AFTER WASHING: COLOURS STAY', 'ఉతికిన తర్వాతా రంగులు అలాగే'), W / 2, 450, 46, ACC, a=ka, maxw=ST.sw)
    if TE:
        kp = e_out(prog(t, AT('2.5', 'మచిలీపట్నం,', 'మచిలీపట్నం,') - .1, AT('2.5', 'మచిలీపట్నం,', 'మచిలీపట్నం,') + .3)) * (1 - ka)
        if kp > .01: chip(img, 'మచిలీపట్నం · పాలకొల్లు', W / 2, 450, 40, ACC, INK, a=kp, scale=kp)
    text(img, L('Chintz detail, India, 18th c. · Science Museum · CC BY-SA 4.0', 'చింట్జ్, భారత్, 18వ శతాబ్దం · Science Museum · CC BY-SA 4.0'), W / 2, 1690, 22, GREY, kind='mono')
    return img

def s_kalam(t, s0, s1):
    cw = AT('2.6', 'weeks', 'వారాల') - 0.1
    if t >= cw:
        im = Image.open(FL.A['MET1']).convert('RGB'); s_ = 1350 / im.height; im = im.resize((int(im.width * s_), 1350), Image.LANCZOS)
        img = on_dark(im, 960, 1 + .03 * (t - cw)); k = e_out(prog(t, cw + .1, cw + .5))
        chip(img, L('FINISHED CHINTZ', 'అచ్చు గుడ్డ సిద్ధం'), W / 2, 380, 42, ACC, INK, a=k, scale=k)
        text(img, L('Palampore, Coromandel Coast · The Met (CC0)', 'పలంపోర్, కోరమాండల్ తీరం · The Met (CC0)'), W / 2, 1690, 22, GREY, kind='mono'); return img
    img = s_still('G05', t, s0, cw, (.62, .42), (.58, .45), 1.1, 1.3)
    steps = [(AT('2.6', 'mordants,', 'పదార్థాలతో'), L('1 · MORDANT', '1 · రంగు పట్టించే పదార్థం')), (AT('2.6', 'reds', 'ఎరుపు'), L('2 · RED · CHAY ROOT', '2 · ఎరుపు · చిరివేరు')),
             (AT('2.6', 'blue', 'నీలం'), L('3 · BLUE · INDIGO', '3 · నీలం · నీలిమందు')), (AT('2.6', 'wax', 'మైనం'), L('4 · WAX', '4 · మైనం'))]
    for i, (c, lab) in enumerate(steps):
        k = e_back(prog(t, c - .1, c + .25))
        if k > .01: chip(img, lab, W / 2, 400 + i * 90, 38, ACC if i == sum(1 for cc, _ in steps if t >= cc - .1) - 1 else CREAM, INK, a=min(1, k), scale=min(1, k))
    text(img, L('ILLUSTRATIVE RECONSTRUCTION', 'పద్ధతికి ఉదాహరణ పునఃసృష్టి'), W / 2, 1690, 24, GREY, kind='monob')
    return img

def s_kalamkari(t, s0, s1):
    img = s_still('CC06', t, s0, s1, (.5, .5), (.45, .5), 1.0, 1.15, .85)
    c1 = AT('2.7', 'శ్రీకాళహస్తిలో', 'శ్రీకాళహస్తిలో') - .1; c2 = AT('2.7', 'మచిలీపట్నం,', 'మచిలీపట్నం,') - .1
    k1 = e_back(prog(t, c1, c1 + .3)); k2 = e_back(prog(t, c2, c2 + .3))
    if k1 > .01: chip(img, 'శ్రీకాళహస్తి · కలంతో', W / 2, 520, 46, ACC, INK, a=min(1, k1), scale=min(1, k1))
    if k2 > .01: chip(img, 'మచిలీపట్నం, పెడన · అచ్చులతో', W / 2, 640, 46, CREAM, INK, a=min(1, k2), scale=min(1, k2))
    text(img, 'Kalamkari · Ravitheja Kumar Reddy C · CC BY-SA 4.0', W / 2, 1690, 22, GREY, kind='mono'); return img

def s_letter(t, s0, s1):
    img = s_still('G06', t, s0, s1, (.6, .5), (.65, .5), 1.1, 1.2, .45); v = t - s0
    dark_panel(img, (110, 560, 970, 980), 30, 225, ACC + (255,))
    t1 = 'COEURDOUX' if not TE else 'కర్డూ (Coeurdoux)'; t2 = L('LETTERS FROM PONDICHERRY · 1740s', 'పాండిచ్చేరి నుంచి ఉత్తరాలు · 1740లు')
    n1 = int(len(t1) * clamp(v / .8)); n2 = int(len(t2) * clamp((v - .8) / 1.4))
    text(img, t1[:n1], W / 2, 700, 72, ACC, kind='head')
    if n2: text(img, t2[:n2], W / 2, 830, 34, CREAM, kind='monob', maxw=800)
    return img

def s_muslin(t, s0, s1):
    img = s_still('G07', t, s0, s1, (.30, .5), (.36, .5), 1.0, 1.08, .95)
    c = AT('2.9', 'woven', 'woven') - .1; k = e_back(prog(t, c, c + .3))
    if k > .01: chip(img, 'WOVEN AIR', W / 2, 420, 60, ACC, INK, a=min(1, k), scale=min(1, k))
    return img

def s_europe(t, s0, s1):
    img = s_still('PD20a', t, s0, s1, (.5, .5), (.5, .45), 1.0, 1.12, .8)
    for i, (en, te) in enumerate((('bright,', 'రంగురంగుల,'), ('light,', 'తేలికైన,'), ('washable', 'ఉతకగలిగే'))):
        c = AT('2.10', en, te) - .05; k = e_back(prog(t, c, c + .3))
        if k > .01: chip(img, L(['BRIGHT', 'LIGHT', 'WASHABLE'][i], ['రంగురంగుల', 'తేలికైన', 'ఉతకగలిగే'][i]), W / 2, 500 + i * 110, 52, ACC, INK, a=min(1, k), scale=min(1, k))
    text(img, 'Chintz wall panel · The Met (CC0)', W / 2, 1690, 22, GREY, kind='mono')
    return img

TL = [(('2.11', 'France', 'ఫ్రాన్స్'), '1686', L('FRANCE BANS PRINTED CALICOES', 'ఫ్రాన్స్: అచ్చు calico లపై నిషేధం'), None, None),
      (('2.11', '1700', '1700'), '1700', L('ENGLAND: ASIAN PRINTED CALICOES NOT FOR HOME USE', 'ఇంగ్లాండ్: ఆసియా అచ్చు calico లు దేశంలో వాడకూడదు'), ('2.11', 're-exported.', 'మళ్లీ'), L('RE-EXPORT ALLOWED', 'మళ్లీ ఎగుమతి చేయొచ్చు')),
      (('2.12', '1721', '1721'), '1721', L('ACT PASSED', 'చట్టం ఆమోదం'), None, None),
      (('2.12', 'Christmas', 'క్రిస్మస్'), '1722', L('IN FORCE · 25 DEC 1722', 'అమలు · 25 డిసెంబర్ 1722'), ('2.12', 'exceptions.', 'మినహాయింపులు'), L('PRINTED, PAINTED, STAINED OR DYED · SOME EXCEPTIONS', 'అచ్చు, రంగుల calico లు · కొన్ని మినహాయింపులు')),
      (('2.13', '1774.', '1774'), '1774', L('REPEALED', 'రద్దు'), None, None)]

def s_timeline(t, s0, s1):
    cf = AT('2.12', 'further.', 'ముందుకెళ్లింది.', end=True)
    if cf <= t < cf + 1.5:
        a = ACT(); s_ = W * 1.25 / a.width; k = e_out(prog(t, cf, cf + .25))
        im = a.resize((int(a.width * s_), int(a.height * s_)), Image.LANCZOS); bg = Image.new('RGB', (W, H), (14, 13, 12))
        z = 1 + .05 * (t - cf); im2 = im.resize((int(im.width * z), int(im.height * z)), Image.BILINEAR)
        bg.paste(im2, (int(W / 2 - im2.width / 2), int(H / 2 - im2.height / 2 - 60)))
        arr = np.asarray(bg).astype(np.float32); band = np.zeros((H, W, 1), np.float32); y0 = int(H / 2 - im2.height / 2 - 60 + im2.height * .14); band[y0:y0 + int(im2.height * .30)] = 1
        bg = Image.fromarray(np.clip(arr * (.35 + .65 * band), 0, 255).astype(np.uint8))
        chip(bg, L('CALICO ACT · 1721', 'Calico Act · 1721'), W / 2, 420, 42, ACC, INK, a=k, scale=k)
        text(bg, 'Statutes at Large · 7 Geo. I c.7', W / 2, 1560, 30, GREY, kind='mono'); return bg
    img = grid_bg(); d = ImageDraw.Draw(img); x = 190; y0, y1 = 380, 1290
    pts = [(x + 8 * math.sin(y / 40 + t), y) for y in np.linspace(y0, y1, 120)]; d.line(pts, fill=(110, 100, 86), width=4)
    tx(img, L('THE BANS', 'నిషేధాలు'), W / 2 + 60, 330, 44, CREAM) if False else None
    for i, ((key, en, te), yr, desc, sub, subt) in enumerate(TL):
        c = AT(key, en, te) - .15; k = e_back(prog(t, c, c + .35))
        if k <= .01: continue
        y = 400 + i * 218; kk = min(1, k)
        lit = [(x + 8 * math.sin(yy / 40 + t), yy) for yy in np.linspace(y0, y, 60)]; d.line(lit, fill=ACC, width=6)
        r = 16 * kk; d.ellipse((x - r, y - r, x + r, y + r), fill=ACC)
        text(img, yr, x + 50, y - 26, 56, ACC, 'lm', 'monob', a=kk)
        lines_ = wrap(desc, 'head', 40, 760)
        for j, ln in enumerate(lines_[:2]): text(img, ln, x + 50, y + 32 + j * 46, 40, CREAM, 'lm', 'head', a=kk)
        if sub:
            cs = AT(*sub[:1], sub[1], sub[2]) - .1; ks = e_out(prog(t, cs, cs + .3))
            if ks > .01:
                for j2, sl in enumerate(wrap(subt, 'monob', 30, 740)[:2]): text(img, sl, x + 50, y + 32 + len(lines_[:2]) * 46 + j2 * 36, 30, ACC, 'lm', 'monob', a=ks)
    return img

def s_protect(t, s0, s1):
    cg = AT('2.14', 'good', 'గొప్పదో') - .3
    if t >= cg:
        im = Image.open(FL.A['MET1']).convert('RGB'); s_ = 1350 / im.height; im = im.resize((int(im.width * s_), 1350), Image.LANCZOS)
        return on_dark(im, 960, 1.05 + .03 * (t - cg))
    img = s_still('G08', t, s0, cg, (.5, .5), (.55, .5), 1.0, 1.1, .85)
    c = AT('2.14', 'wool', 'ఉన్ని,') - .1; k = e_back(prog(t, c, c + .3))
    if k > .01: chip(img, L('PROTECTING WOOL & SILK WEAVERS', 'ఉన్ని, పట్టు నేతగాళ్లకు రక్షణ'), W / 2, 420, 40, ACC, INK, a=min(1, k), scale=min(1, k))
    return img

def s_globe(t, s0, s1):
    ce = AT('2.15', 'Even', 'Even') - .1
    if t < ce:
        i = min(150, max(1, int((t - s0) / max(.1, ce - s0) * 150) + 1))
        return Image.open(f'/home/claude/gs2/rem/gframes/{i:04d}.jpg').convert('RGB')
    img = grid_bg(); v = t - ce
    for j, (a_, b_) in enumerate((('CALICO', '← CALICUT'), ('CHINTZ', '← HINDI chhīṇṭ'))):
        k = e_back(prog(v, .1 + j * 1.2, .45 + j * 1.2))
        if k <= .01: continue
        y = 640 + j * 300; dark_panel(img, (140, y - 110, 940, y + 110), 30, 230, ACC + (255,))
        text(img, a_, W / 2, y - 30, 80, ACC, kind='head', a=min(1, k)); text(img, b_, W / 2, y + 55, 38, CREAM, kind='monob', a=min(1, k))
    text(img, 'Oxford English Dictionary · Riello, Cotton (2013)', W / 2, 1690, 22, GREY, kind='mono')
    return img

def s_tease(t, s0, s1):
    img = s_still('G09', t, s0, s1, (.62, .5), (.70, .45), 1.0, 1.15, .9)
    px, py = 640, 880; u = e_io(prog(t, s0 + .2, s0 + 1.6))
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    xs = np.linspace(-40, px, 120); xe = -40 + (px + 40) * u
    pts = [(x, 1300 - (1300 - py) * (x + 40) / (px + 40) + 20 * math.sin(x / 50)) for x in xs if x <= xe]
    if len(pts) > 1: d.line(pts, fill=ACC + (255,), width=7)
    img.paste(lay, (0, 0), lay)
    if u >= 1:
        d2 = ImageDraw.Draw(img); r = 22; d2.ellipse((px - r, py - r, px + r, py + r), fill=ACC, outline=CREAM, width=4)
        if TE:
            c = AT('T', 'మచిలీపట్నం.', 'మచిలీపట్నం.') - .1; k = e_back(prog(t, c, c + .3))
            if k > .01: chip(img, 'మచిలీపట్నం', px, py - 80, 50, ACC, INK, a=min(1, k), scale=min(1, k))
        else:
            c = AT('T', 'port', 'port') - .1; k = e_back(prog(t, c, c + .3))
            if k > .01: chip(img, "?  A PORT ON INDIA'S EAST COAST", px - 60, py - 80, 36, ACC, INK, a=min(1, k), scale=min(1, k))
    return img

def overlays2(img, t, scn):
    overlays(img, t, scn)
    if scn in ('slide',): return
    thread_chain(img, t, scn)
    if scn not in ('hook', 'cartoon1', 'cartoon2', 'cartoon3', 'loop'): thread_sweep(img, t)

ZOOM = ('spin', 'wash', 'timeline', 'cartoon1', 'cartoon2', 'cartoon3', 'globe')
def render(t):
    scn, s0, s1 = scene_at(t)
    if scn == 'loop':
        img = s_loop(t, s0, s1); captions(img, t, 'loop'); return img
    if scn.startswith('cartoon'):
        q = {'cartoon1': 'Q1', 'cartoon2': 'Q2', 'cartoon3': 'Q3'}[scn]; img = cartoon(t, s0, [('CHELLI', q)])
    elif scn == 'slide': img = s_slide(t, s0, s1)
    else: img = globals()['s_' + scn](t, s0, s1)
    img = img.convert('RGB')
    if scn in ZOOM and not (scn == 'globe' and t < AT('2.15', 'Even', 'Even') - .1): img = zoom(img, 1 + 0.04 * e_io(prog(t, s0, s1)))
    if scn == 'spin' and t < AT('2.2', 'many', 'ఎంతోమంది') - 0.15: pass
    overlays2(img, t, scn); captions(img, t, scn); return img

# ---- series slide (platform specific, phone-readable: 3 items + button)
@functools.lru_cache(1)
def FILM_THUMB():
    return Image.open(f'/home/claude/why-channel-studio/videos/2026-11-08_long_golden_sparrow_s1/thumb_golden_sparrow_film_{LANGV.upper()}.jpg').convert('RGB')

def s_slide(t, s0, s1, plat=None):
    plat = plat or PLAT; v = t - s0
    img = radial_bg(W, H, (34, 28, 18), (8, 8, 9), cy=.4, reach=.8).copy()
    tx(img, L('THE GOLDEN SPARROW · SEASON 1', 'బంగారు పిచ్చుక · సీజన్ 1'), W / 2, 250, 40, AMBER, kind='head', maxw=ST.sw)
    rows = [(L('2/6', '2/6'), L('The cloth the world wanted', 'ప్రపంచం కోరుకున్న గుడ్డ'), L("YOU'RE HERE", 'మీరు ఇక్కడ'), True),
            (L('NEXT · 3/6', 'తర్వాత · 3/6'), L('Golconda & Machilipatnam', 'గోల్కొండ, మచిలీపట్నం'), L('TOMORROW', 'రేపు'), False)]
    for i, (num, title, tag, here) in enumerate(rows):
        k = e_back(prog(v, .05 + .12 * i, .45 + .12 * i)); y = 350 + i * 180
        if k <= .01: continue
        x0 = 90 + (1 - min(1, k)) * 60
        dark_panel(img, (x0, y, x0 + 900, y + 160), 30, 230, AMBER + (255,) if here else (90, 90, 96, 255))
        text(img, num, x0 + 40, y + 50, 38, AMBER if here else CREAM, 'lm', 'monob')
        text(img, title, x0 + 40, y + 112, 46, CREAM, 'lm', 'head', maxw=560)
        chip(img, tag, x0 + 900 - 40 - pick(tag, 'head', 30).getlength(tag) / 2 - 22, y + 50, 30, AMBER if here else CREAM, INK)
    # full film pointer with the film thumbnail
    k = e_out(prog(v, .35, .75)); y = 735
    if k > .01:
        th = FILM_THUMB(); tw = 760; thh = int(tw * th.height / th.width); thi = th.resize((tw, thh), Image.LANCZOS)
        m = Image.new('L', thi.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, tw - 1, thh - 1), 26, fill=int(255 * k)); img.paste(thi, (160, y), m)
        lab = L('FULL FILM · RELATED VIDEO', 'పూర్తి సినిమా · RELATED VIDEO') if plat == 'yt' else L('FULL FILM ON YOUTUBE · LINK IN BIO', 'పూర్తి సినిమా YouTube లో · LINK IN BIO')
        chip(img, lab, W / 2, y + thh + 45, 38, AMBER, INK, a=k, scale=k)
    # subscribe / follow card
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(surf)
    CTA.draw(c, t, s0 + 0.9, plat, LANGV, y=1360, t_out=None); surf.flush()
    a = np.frombuffer(surf.get_data(), np.uint8).reshape(H, W, 4); rgba = Image.fromarray(a[..., [2, 1, 0, 3]].copy(), 'RGBA')
    img.paste(rgba, (0, 0), rgba)
    return img

@functools.lru_cache(1)
def frame0():
    img = s_hook(0.0, 0.0, 1.0, frame0=True); overlays(img, 0.0, 'hook'); return img

def s_loop(t, s0, s1):
    """slide fades out into frame 0 so the last frame matches the first"""
    k = e_io(prog(t, s0, s0 + 0.4)); b = zoom(frame0(), 1 + 0.06 * (1 - e_io(prog(t, s0, DUR - 1 / FPS))))
    if k >= 1: return b
    a = s_slide(t, SC_START['slide'], s0); return Image.blend(a, b, k)

SC_START = {n: s for n, s in SC}
def zoom(img, z):
    if z <= 1.0005: return img.copy()
    w, h = W / z, H / z; return img.resize((W, H), Image.BICUBIC, box=((W - w) / 2, (H - h) / 2, (W + w) / 2, (H + h) / 2))

if __name__ == '__main__':
    if sys.argv[1] == 'stills':
        ts = [float(x) for x in sys.argv[2].split(',')]; ims = [render(x).resize((270, 480), Image.LANCZOS) for x in ts]
        cols = 6; sh = Image.new('RGB', (cols * 276, ((len(ims) + cols - 1) // cols) * 506), (40, 40, 40)); d = ImageDraw.Draw(sh)
        for i, (x, im) in enumerate(zip(ts, ims)): sh.paste(im, ((i % cols) * 276 + 3, (i // cols) * 506 + 3)); d.text(((i % cols) * 276 + 8, (i // cols) * 506 + 486), f'{x:.1f}', fill='white')
        sh.save(sys.argv[3]); sys.exit()
    if sys.argv[1] == 'one':
        render(float(sys.argv[2])).save(sys.argv[3]); sys.exit()
    a, b, out = float(sys.argv[1]), float(sys.argv[2]), sys.argv[3]
    f0, f1 = int(round(a * FPS)), int(round(b * FPS))
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '19', '-pix_fmt', 'yuv420p', '-g', '60', out + '.tmp.mp4'], stdin=subprocess.PIPE)
    for f in range(f0, f1): p.stdin.write(render(f / FPS).tobytes())
    p.stdin.close(); p.wait(); os.replace(out + '.tmp.mp4', out); print('ok', out, f1 - f0)
