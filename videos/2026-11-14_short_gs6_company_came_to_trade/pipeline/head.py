"""GOLDEN SPARROW · 6/6 Short renderer (9:16). Env: LANGV=en|te, PLAT=yt|ig.
usage: render.py <t_start> <t_end> <out.mp4>   (frame range by seconds)"""
import os, sys, math, json, functools, subprocess
import numpy as np, cairo
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops
sys.path.insert(0, '/home/claude/why-channel-studio/pipeline/styles'); sys.path.insert(0, '/home/claude/why-channel-studio/pipeline/style_v2')
sys.path.insert(0, '/home/claude/gs/film3'); sys.path.insert(0, '/home/claude/gs/vis'); sys.path.insert(0, '/home/claude/gs6')
_argv = sys.argv; sys.argv = sys.argv[:1]
import flib as FL
sys.argv = _argv
from core import Stage, text, pill, font, pick, fit, wrap, radial_bg, glow, grain, clamp, prog, e_out, e_io, e_back, lerp, mix, INK, CREAM, AMBER, GREY
import cartoon_explainer as CE
import cta_card as CTA
import layout as LY
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
TAG = L('GOLDEN SPARROW · 6/6', 'బంగారు పిచ్చుక · 6/6')
CHIPS = [('A', L('1/3 · PERMISSION', '1/3 · అనుమతి')), ('Q1', L('2/3 · THE WARS', '2/3 · యుద్ధాలు')), ('Q2', L('3/3 · PLASSEY', '3/3 · ప్లాసీ'))]

def overlays(img, t, scn):
    if scn in ('slide',): return
    a = 1.0
    if scn == 'loop': a = 1.0
    # no caption-lane fade (GS 4/6 lesson: full-screen pictures run to the bottom edge); captions carry their own outline
    LY.badge(img, TAG, 'left', 'tag')
    if scn not in ('hook', 'loop', 'tease'):
        cur = None
        for k, s_ in CHIPS:
            if t >= S(k) - 0.15: cur = s_
        if cur: LY.badge(img, cur, 'right', 'chip')

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
    # reserved caption lane: just above the platform UI, below every picture, card, label and credit
    px = 54 if not TE else 50; y = CAP_LANE
    s = ' '.join(w[2] for w in ch); f, px = fit(s, 'head', px, ST.sw - 40)
    widths = [pick(w[2], 'head', px).getlength(w[2]) for w in ch]; sp = f.getlength(' '); tot = sum(widths) + sp * (len(ch) - 1); x = W / 2 - tot / 2
    _ib = f.getbbox(s, anchor='lm'); LY.reg('caption', (x + _ib[0] - 12, y + _ib[1] - 10, x + tot + 12, y + _ib[3] + 10), (x + _ib[0], y + _ib[1], x + tot, y + _ib[3]), owner=s)
    for w, wd in zip(ch, widths):
        on = w[0] - 0.05 <= t
        cap_word(img, w[2], x, y, px, AMBER if (on and t <= w[1] + 0.12) else CREAM, 1.0 if on else 0.62)
        x += wd + sp

CAP_LANE = 1446
@functools.lru_cache(1)
def SCRIM():
    yy = np.arange(H, dtype=np.float32); prof = np.clip((yy - 1230) / 260, 0, 1) ** 1.4 * .74   # bottom fade, not a band
    a = np.repeat(prof[:, None], W, 1); lay = Image.new('RGBA', (W, H), (8, 8, 8, 0)); lay.putalpha(Image.fromarray((a * 255).astype(np.uint8))); return lay

def cap_word(img, s, x, y, px, col, a):
    """caption word with a soft dark outline + drop shadow (readable on any picture without a darkening band)"""
    f = pick(s, 'head', px); lay = Image.new('RGBA', (W, 140), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.text((x + 2, 74), s, font=f, fill=(0, 0, 0, int(150 * a)), anchor='lm', stroke_width=7, stroke_fill=(0, 0, 0, int(150 * a)))
    sh = lay.filter(ImageFilter.GaussianBlur(3)); d = ImageDraw.Draw(sh)
    d.text((x, 70), s, font=f, fill=col + (int(255 * a),), anchor='lm', stroke_width=3, stroke_fill=(8, 8, 8, int(235 * a)))
    img.paste(sh, (0, int(y - 70)), sh)
