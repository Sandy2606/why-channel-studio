"""GOLDEN SPARROW · 1/6 Short renderer (9:16). Env: LANGV=en|te, PLAT=yt|ig.
usage: render.py <t_start> <t_end> <out.mp4>   (frame range by seconds)"""
import os, sys, math, json, functools, subprocess
import numpy as np, cairo
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops
sys.path.insert(0, '/home/claude/why-channel-studio/pipeline/styles'); sys.path.insert(0, '/home/claude/why-channel-studio/pipeline/style_v2')
sys.path.insert(0, '/home/claude/gs/film3'); sys.path.insert(0, '/home/claude/gs/vis'); sys.path.insert(0, '/home/claude/gs1s')
_argv = sys.argv; sys.argv = sys.argv[:1]
import flib as FL
sys.argv = _argv
from core import Stage, text, pill, font, pick, fit, wrap, radial_bg, glow, grain, clamp, prog, e_out, e_io, e_back, lerp, mix, INK, CREAM, AMBER, GREY
import cartoon_explainer as CE, paper_cut as PC, chart3d_gs as CH
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
    return {'ANNA': gated(['1.5']), 'CHELLI': gated(['Q1', 'Q2', 'Q3'])}

def cartoon(t, s0, lines):
    v = t - s0; f0 = int(round(s0 * FPS)); env = {k: e[f0:] for k, e in ENV().items()}
    spec = dict(topic='', lines=[dict(who=w, t0=S(k) - s0, t1=E(k) - s0 + .05, text=LINES[k]) for w, k in lines], env=env, fps=FPS)
    return CE.draw(ST, v, spec)

# ------------------------------------------------------------------ overlays: series tag, progress chips, captions
TAG = L('GOLDEN SPARROW · 1/6', 'బంగారు పిచ్చుక · 1/6')
CHIPS = [('Q1', L('1/3 · THE NUMBER', '1/3 · అసలు లెక్క')), ('Q2', L('2/3 · THE CATCH', '2/3 · అసలు విషయం')), ('Q3', L('3/3 · WHAT INDIA MADE', '3/3 · మనం ఏం తయారుచేశాం'))]

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

# ------------------------------------------------------------------ scenes
def s_hook(t, s0, s1, frame0=False):
    """24% promise over the field + gold undivided subcontinent; 1.3 moves into the cotton."""
    u = (t - s0) / max(.1, (S('Q1') - 0.15) - s0)
    bg = cover(IMG('G01'), u, (.40, .62), (.30, .80), 1.05, 1.45)
    c13 = S('1.3'); k13 = e_io(prog(t, c13 - 0.3, c13 + 0.6))
    img = grade(bg, lerp(.42, .92, k13))
    a = 1 - k13
    if a > 0.01:
        m = map_layer('undivided', 560); paste_c(img, m, W / 2, 700 + 10 * math.sin(t * .6), a)
        pop = 1.0 if frame0 else e_back(prog(t, 0.0, 0.5)); pop = max(pop, 0.85) if t < 0.5 else pop
        f = font('head', 300); lay = Image.new('L', (W, H), 0); ImageDraw.Draw(lay).text((W / 2, 1080), '24%', font=f, fill=255, anchor='mm')
        sh = lay.filter(ImageFilter.GaussianBlur(14)); img.paste((0, 0, 0), (0, 10), sh.point(lambda p: int(p * .7 * a)))
        img.paste(AMBER, (0, 0), lay.point(lambda p: int(p * a)))
        sub = L("1700 · INDIA'S SHARE OF WORLD OUTPUT", '1700 · ప్రపంచ ఉత్పత్తిలో మన వాటా')
        tx(img, sub, W / 2, 1245, 44, CREAM, kind='head', a=a, maxw=ST.sw)
        tx(img, L('ESTIMATE · UNDIVIDED SUBCONTINENT', 'అంచనా · అవిభక్త ఉపఖండం'), W / 2, 1300, 32, GREY, kind='monob', a=a, maxw=ST.sw)
    if t >= c13:
        k = e_out(prog(t, c13 + 0.6, c13 + 1.1)) * (1 - prog(t, S('Q1') - 0.5, S('Q1') - 0.2))
        if k > 0.01: chip(img, L('COTTON · GROWN & WOVEN FOR MILLENNIA', 'పత్తి · వేల ఏళ్లుగా'), W / 2, 330, 36, AMBER, INK, a=k, scale=k)
    return img

def s_chart(t, s0, s1):
    v = t - s0
    bars = [dict(label=L('INDIA 1700', 'భారత్ 1700'), value=24.4, hero=True, t0=AT('1.4', '24', '24') - s0 - 0.2),
            dict(label=L('UK 1700', 'బ్రిటన్ 1700'), value=2.9, t0=AT('1.4', 'About', 'దాదాపు', n=L(2, 2)) - s0 - 0.1),
            dict(label=L('INDIA 1950', 'భారత్ 1950'), value=4.2, t0=AT('1.4', '1950', '1950') - s0 + 0.3)]
    img = CH.draw(ST, v, dict(title='', unit='%', decimals=1, bars=bars, gap=2.3, ht=2.7, source=L('MADDISON 2001 · TABLE B-20 · P.263 · EST.', 'Maddison 2001 · Table B-20 · p.263 · అంచనా'), ref=None)).convert('RGB')
    tx(img, L('SHARE OF WORLD OUTPUT', 'ప్రపంచ ఉత్పత్తిలో వాటా'), W / 2, 262, 54, CREAM, maxw=ST.sw - 330 if False else 700)
    # territory cards: left = 1700 undivided, right = 1950 Republic of India
    kL = e_out(prog(t, AT('1.4', '1700', '1700') - 0.2, AT('1.4', '1700', '1700') + 0.3)); kR = e_out(prog(t, AT('1.4', '1950', '1950') - 0.1, AT('1.4', '1950', '1950') + 0.4))
    for k, kind, cx, lab in ((kL, 'undivided', 300, L('1700 · UNDIVIDED SUBCONTINENT', '1700 · అవిభక్త ఉపఖండం')), (kR, 'republic', 780, L('1950 · REPUBLIC OF INDIA', '1950 · స్వతంత్ర భారత్'))):
        if k <= .01: continue
        dark_panel(img, (cx - 215, 315, cx + 215, 535), 26, int(190 * k), AMBER + (int(200 * k),) if kind == 'undivided' else CREAM + (int(160 * k),))
        paste_c(img, map_layer(kind, 120), cx, 405, k)
        lines_ = wrap(lab, 'monob', 28, 400)
        for i, ln in enumerate(lines_): text(img, ln, cx, 497 + i * 32 - (len(lines_) - 1) * 16, 28, CREAM, kind='monob', a=k)
    if kR > .01:
        chip(img, L('DIFFERENT BORDERS · NOT LIKE-FOR-LIKE', 'సరిహద్దులు వేరు · నేరుగా పోల్చలేం'), W / 2, 1268, 32, AMBER, INK, a=kR, scale=kR)
    # source flash (evidence card) on "Angus Maddison"
    c = AT('1.4', 'Maddison', 'Maddison'); k = e_out(prog(t, c - 0.1, c + 0.25)) * (1 - prog(t, c + 2.2, c + 2.5))
    if k > .01:
        dark_panel(img, (110, 1520, 970, 1700), 24, int(225 * k), AMBER + (int(255 * k),))
        text(img, 'ANGUS MADDISON', W / 2, 1572, 40, AMBER, kind='head', a=k)
        text(img, L('The World Economy: A Millennial Perspective · OECD 2001', 'The World Economy · OECD 2001'), W / 2, 1630, 28, CREAM, kind='mono', a=k, maxw=820)
    return img

def s_circle(t, s0, s1):
    """India 24.4 + China 22.3 = 46.7% of the world (Maths Diagram look)."""
    v = t - s0; img = radial_bg(W, H, (22, 24, 30), (8, 8, 10), cy=.5, reach=.8).copy(); d = ImageDraw.Draw(img)
    for x in range(0, W, 60): d.line([(x, 0), (x, H)], fill=(26, 28, 34), width=1)
    for y in range(0, H, 60): d.line([(0, y), (W, y)], fill=(26, 28, 34), width=1)
    tx(img, L('THE WORLD IN 1700', 'ప్రపంచం · 1700'), W / 2, 330, 64, CREAM)
    cx, cy, R = W / 2, 830, 330
    ki = e_io(prog(t, s0, s0 + 0.8)); kc = e_io(prog(t, AT('1.4e', '22', '22') - 0.2 if not TE else s0, AT('1.4e', '22', '22') + 0.7 if not TE else s0 + 1))
    SS = 2; lay = Image.new('RGBA', (W * SS, H * SS), (0, 0, 0, 0)); dl = ImageDraw.Draw(lay)
    bb = ((cx - R) * SS, (cy - R) * SS, (cx + R) * SS, (cy + R) * SS)
    dl.ellipse(bb, fill=(46, 46, 52, 255)); a0 = -90
    dl.pieslice(bb, a0, a0 + 360 * .244 * ki, fill=AMBER + (255,))
    if kc > 0: dl.pieslice(bb, a0 + 360 * .244, a0 + 360 * .244 + 360 * .223 * kc, fill=CREAM + (255,))
    dl.ellipse(((cx - R * .52) * SS, (cy - R * .52) * SS, (cx + R * .52) * SS, (cy + R * .52) * SS), fill=(14, 14, 18, 255))
    lay = lay.resize((W, H), Image.LANCZOS); img.paste(lay, (0, 0), lay)
    tot = 24.4 * ki + 22.3 * kc; tx(img, f'{tot:.1f}%', cx, cy, 92, AMBER if kc < 1 else CREAM)
    text(img, L('INDIA 24.4%', 'భారత్ 24.4%'), 250, 1240, 40, AMBER, kind='monob')
    text(img, L('CHINA 22.3%', 'చైనా 22.3%'), 830, 1240, 40, CREAM, kind='monob', a=clamp(kc * 2))
    kh = e_out(prog(t, AT('1.4e', 'half', 'half') - 0.2 if not TE else s1, AT('1.4e', 'half', 'half') + 0.3 if not TE else s1))
    if kh > .01:
        text(img, '24.4 + 22.3 = 46.7', W / 2, 1290, 46, CREAM, kind='monob', a=kh)
        chip(img, L('ALMOST HALF OF EVERYTHING ON EARTH', 'భూమిపై దాదాపు సగం'), W / 2, 1530, 36, AMBER, INK, a=kh, scale=kh)
    text(img, L('MADDISON (OECD 2001) · ESTIMATES', 'Maddison (OECD 2001) · అంచనాలు'), W / 2, 1640, 30, GREY, kind='mono')
    return img

def s_people(t, s0, s1):
    """1 in 4 people; then income per person (no exact numbers)."""
    c_inc = AT('1.6', 'Income', 'ఒక్కొక్కరి')
    if t >= c_inc - 0.1: return s_income(t, c_inc - 0.1, s1)
    img = radial_bg(W, H, (22, 24, 30), (8, 8, 10), cy=.5, reach=.8).copy(); d = ImageDraw.Draw(img)
    for x in range(0, W, 60): d.line([(x, 0), (x, H)], fill=(26, 28, 34), width=1)
    for y in range(0, H, 60): d.line([(0, y), (W, y)], fill=(26, 28, 34), width=1)
    tx(img, L("THE WORLD'S PEOPLE · 1700", 'ప్రపంచ జనాభా · 1700'), W / 2, 330, 58, CREAM, maxw=ST.sw)
    kq = e_out(prog(t, AT('1.6', 'quarter', 'నాలుగో') - 0.2, AT('1.6', 'quarter', 'నాలుగో') + 0.5))
    cols, rows, gx, gy = 10, 10, 72, 72; x0 = W / 2 - (cols - 1) * gx / 2; y0 = 470
    for r in range(rows):
        for c in range(cols):
            i = r * cols + c; ka = e_out(prog(t, s0 + i * .006, s0 + i * .006 + .3))
            if ka <= 0: continue
            lit = i < 25 and kq > (i / 25) * .8
            col = AMBER if lit else (90, 90, 96); x = x0 + c * gx; y = y0 + r * gy; rr = 15 * ka
            d.ellipse((x - rr * .7, y - rr * 1.55, x + rr * .7, y - rr * .15), fill=col); d.rounded_rectangle((x - rr, y - rr * .05, x + rr, y + rr * 1.3), int(rr * .6), fill=col)
    if kq > .01: chip(img, L('≈ 1 IN 4 LIVED HERE · EST.', 'దాదాపు 4లో 1 ఇక్కడే · అంచనా'), W / 2, 1225, 38, AMBER, INK, a=kq, scale=kq)
    kh = e_out(prog(t, AT('1.6', 'huge', 'పెద్దది') - 0.1, AT('1.6', 'huge', 'పెద్దది') + 0.4))
    if kh > .01: text(img, L('MANY PEOPLE + MAKING THINGS = BIG SHARE', 'ఎక్కువ జనం + తయారీ = పెద్ద వాటా'), W / 2, 1300, 36, CREAM, kind='monob', a=kh, maxw=ST.sw)
    return img

def s_income(t, s0, s1):
    v = t - s0
    bars = [dict(label=L('INDIA', 'భారత్'), value=550, hero=True, t0=0.25), dict(label=L('WORLD AVG', 'ప్రపంచ సగటు'), value=615, t0=0.55), dict(label=L('W. EUROPE', 'ప. యూరప్'), value=1000, t0=AT('1.6', 'Western', 'పశ్చిమ') - s0 - 0.2)]
    img = CH.draw(ST, v, dict(title=L('INCOME PER PERSON · 1700', 'ఒక్కొక్కరి ఆదాయం · 1700'), unit='', decimals=0, bars=bars, novalues=True, gap=2.3, ht=4.2, source=L('ESTIMATES · MADDISON (OECD 2001)', 'అంచనాలు · Maddison (OECD 2001)'), ref=None)).convert('RGB')
    k = e_out(prog(t, AT('1.6', 'below', 'తక్కువగా') - 0.1, AT('1.6', 'below', 'తక్కువగా') + 0.4))
    if k > .01: chip(img, L('INDIA ≈ WORLD AVERAGE · BELOW W. EUROPE', 'భారత్ ≈ ప్రపంచ సగటు · యూరప్ కంటే తక్కువ'), W / 2, 1420, 34, AMBER, INK, a=k, scale=k)
    return img

# ---- paper-cut people, heaps, school
PAL = [(244, 226, 188), (240, 194, 120), (226, 150, 66), (168, 102, 52), (92, 70, 58), (38, 44, 48)]
def cut_shape(img, draw_fn, col, shadow=10):
    m = Image.new('L', (W, H), 0); draw_fn(ImageDraw.Draw(m))
    sh = m.filter(ImageFilter.GaussianBlur(shadow)); img.paste((40, 22, 12), (int(shadow * .5), int(shadow * .9)), sh.point(lambda p: int(p * .5)))
    img.paste(col, (0, 0), m)

def person(d, x, y, s, turban=False):
    d.ellipse((x - s * .22, y - s * 1.62, x + s * .22, y - s * 1.18), fill=255)
    if turban: d.ellipse((x - s * .26, y - s * 1.72, x + s * .26, y - s * 1.4), fill=255)
    d.polygon([(x - s * .34, y - s * 1.12), (x + s * .34, y - s * 1.12), (x + s * .42, y - s * .2), (x - s * .42, y - s * .2)], fill=255)
    d.rectangle((x - s * .3, y - s * .25, x - s * .08, y), fill=255); d.rectangle((x + s * .08, y - s * .25, x + s * .3, y), fill=255)

def heap(d, x, y, w, h):
    d.chord((x - w / 2, y - h, x + w / 2, y + h), 180, 360, fill=255)

def s_paper(t, s0, s1):
    v = t - s0; img = PC.draw(ST, min(v, 2.0) + 2.0, dict(title='', sub='', tags=[], sun=False)).convert('RGB')
    c_split = AT('1.7', 'split.', 'సమానంగా'); c_caste = AT('1.7', 'Caste', 'చాలామంది'); c_school = AT('1.7', 'schooling', 'చదువు')
    if TE:
        c_kar = AT('1.7', 'ప్రతి', 'ప్రతి')
        if c_kar - 0.1 <= t < c_caste - 0.1:
            u = (t - c_kar) / max(.1, c_caste - c_kar); img = grade(cover(IMG('G03'), u, (.42, .5), (.40, .55), 1.0, 1.12), .9)
            chip(img, 'కరణం · ఊరి భూమి లెక్కలు', W / 2, 1220, 40, AMBER, INK)
            text(img, 'AI ఉదాహరణ చిత్రం', W - 80, 1500, 28, GREY, 'rm', 'mono')
            return img
    if t < c_caste - 0.1:
        # Ramayya + harvest split
        kR = e_out(prog(t, s0, s0 + 0.5)); gy = 1180
        cut_shape(img, lambda d: person(d, 210, gy, 170 * kR, turban=True), PAL[5])
        chip(img, L('RAMAYYA · ILLUSTRATIVE EXAMPLE', 'రామయ్య · ఉదాహరణ'), W / 2, 520, 34, INK, CREAM, a=kR, scale=kR)
        ks = e_io(prog(t, c_split - 0.1, c_split + 0.9))
        sizes = [(L('FARMER', 'రైతు'), 190, 90), (L('LANDLORD', 'భూస్వామి'), 250, 115), (L('STATE', 'రాజ్యం'), 320, 150)]
        xs = [lerp(640, 450, ks), 640, lerp(640, 860, ks)]; ys = [gy, lerp(gy, gy - 300, ks), gy]
        if ks < 0.05: cut_shape(img, lambda d: heap(d, 640, gy, 420, 190), PAL[2])
        else:
            for (lab, w_, h_), x, y in zip(sizes, xs, ys):
                cut_shape(img, lambda d, x=x, y=y, w_=w_, h_=h_: heap(d, x, y, w_ * lerp(1.6, 1, ks), h_ * lerp(1.5, 1, ks)), PAL[2])
                text(img, lab, x, y + 44, 38, INK, kind='monob', a=ks)
        kr = e_out(prog(t, AT('1.7', 'rarely', 'ఒక్కొక్కరూ') - 0.1, AT('1.7', 'rarely', 'ఒక్కొక్కరూ') + 0.4))
        if kr > .01: chip(img, L('RARELY AN EQUAL SHARE', 'సమాన వాటా కాదు'), W / 2, 420, 42, CREAM, INK, a=kr, scale=kr)
        return img
    if t < c_school - 0.1:
        k = e_out(prog(t, c_caste - 0.1, c_caste + 0.4)); gy = 1180
        for i, x in enumerate((200, 340, 480, 620, 760, 900)):
            cut_shape(img, lambda d, x=x: person(d, x, gy, 130), PAL[5 - (i % 2)])
        chip(img, L('WORK OFTEN DECIDED BY BIRTH', 'పని పుట్టుకతోనే నిర్ణయం'), W / 2, 420, 42, CREAM, INK, a=k, scale=k)
        return img
    k = e_out(prog(t, c_school - 0.1, c_school + 0.4)); gy = 1190
    def school(d):
        d.rectangle((330, gy - 330, 750, gy), fill=255); d.polygon([(290, gy - 320), (790, gy - 320), (540, gy - 520)], fill=255)
    cut_shape(img, school, PAL[3])
    win = Image.new('L', (W, H), 0); ImageDraw.Draw(win).rectangle((380, gy - 270, 700, gy - 60), fill=255); img.paste((255, 214, 140), (0, 0), win)
    for x in (450, 540, 630): cut_shape(img, lambda d, x=x: person(d, x, gy - 70, 85), PAL[5], 4)
    for i, x in enumerate((110, 200, 860, 950, 160, 900)):
        cut_shape(img, lambda d, x=x, i=i: person(d, x, gy + (60 if i >= 4 else 0), 110), PAL[4])
    chip(img, L('SCHOOLING · ONLY A FEW', 'చదువు · కొంతమందికే'), W / 2, 420, 42, CREAM, INK, a=k, scale=k)
    return img

def s_reveal(t, s0, s1):
    c_hum = AT('1.8b', 'humbler', 'సాధారణమైన') - 0.1
    if t < c_hum:
        u = (t - s0) / max(.1, c_hum - s0); img = grade(cover(IMG('G01'), u, (.5, .55), (.5, .6), 1.0, 1.1), .75)
        # gold coins rise then dissolve
        kin = e_out(prog(t, s0, s0 + 0.6)); kout = prog(t, c_hum - 1.0, c_hum)
        for i in range(9):
            x = 160 + (i % 5) * 190 + (i // 5) * 95; y = 700 + (i // 5) * 260 - 40 * math.sin(t * 1.5 + i) - 120 * kout
            a = kin * (1 - kout); r = 62
            if a <= .01: continue
            lay = Image.new('RGBA', (2 * r + 20, 2 * r + 20), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
            d.ellipse((10, 10, 10 + 2 * r, 10 + 2 * r), fill=(214, 160, 48, 255)); d.ellipse((22, 22, 2 * r - 2, 2 * r - 2), outline=(255, 214, 120, 255), width=6)
            paste_c(img, lay, x, y, a)
        k = e_out(prog(t, AT('1.8b', 'gold.', 'బంగారం') - 0.1, AT('1.8b', 'gold.', 'బంగారం') + 0.3)) * (1 - kout)
        if k > .01: chip(img, L('NOT GOLD', 'బంగారం కాదు'), W / 2, 420, 46, CREAM, INK, a=k, scale=k)
        return img
    u = (t - c_hum) / max(.1, s1 - c_hum); img = grade(cover(IMG('G04'), u, (.50, .45), (.48, .40), 1.05, 1.35), .95)
    k = e_out(prog(t, AT('1.8b', 'field.', 'పొలంలోనే') - 0.2, AT('1.8b', 'field.', 'పొలంలోనే') + 0.3))
    if k > .01: chip(img, L('COTTON', 'పత్తి'), W / 2, 420, 60, AMBER, INK, a=k, scale=k)
    return img

@functools.lru_cache(1)
def DRESS():
    im = Image.open(FL.A['PD04']).convert('RGB'); s = 1500 / im.height; return im.resize((int(im.width * s), 1500), Image.LANCZOS)

@functools.lru_cache(1)
def ACT():
    im = Image.open(FL.A['PD03']).convert('RGB'); w, h = im.size; return im.crop((int(w * .08), int(h * .05), int(w * .95), int(h * .36)))

def s_tease(t, s0, s1):
    v = t - s0; c_stamp = AT('T', 'Britain', 'బ్రిటన్'); c_flash = E('T') - 0.9
    if t >= c_flash:
        # evidence flash: the 1721 Act page, everything dimmed but the title
        a = ACT(); s_ = W * 1.25 / a.width; k = e_out(prog(t, c_flash, c_flash + 0.25))
        im = a.resize((int(a.width * s_), int(a.height * s_)), Image.LANCZOS); bg = Image.new('RGB', (W, H), (14, 13, 12))
        z = 1 + .05 * (t - c_flash); im2 = im.resize((int(im.width * z), int(im.height * z)), Image.BILINEAR)
        bg.paste(im2, (int(W / 2 - im2.width / 2), int(H / 2 - im2.height / 2 - 60)))
        arr = np.asarray(bg).astype(np.float32); band = np.zeros((H, W, 1), np.float32); y0 = int(H / 2 - im2.height / 2 - 60 + im2.height * .14); band[y0:y0 + int(im2.height * .30)] = 1
        arr = arr * (.35 + .65 * band); bg = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
        chip(bg, L('CALICO ACT · 1721', 'Calico Act · 1721'), W / 2, 420, 42, AMBER, INK, a=k, scale=k)
        text(bg, 'Statutes at Large · 7 Geo. I c.7', W / 2, 1560, 30, GREY, kind='mono')
        return bg
    bg = Image.new('RGB', (W, H), (18, 16, 14)); d = DRESS(); z = 1.0 + .04 * v
    dd = d.resize((int(d.width * z), int(d.height * z)), Image.BILINEAR); bg.paste(dd, (int(W / 2 - dd.width / 2), int(980 - dd.height / 2)))
    img = grade(bg, .9)
    k1 = e_out(prog(t, s0 + 0.3, s0 + 0.8))
    chip(img, L('INDIAN PRINTED COTTON', 'మన అచ్చు cotton'), W / 2, 330, 40, CREAM, INK, a=k1, scale=k1)
    ks = e_back(prog(t, c_stamp - 0.05, c_stamp + 0.25))
    if ks > .01:
        lay = Image.new('RGBA', (760, 230), (0, 0, 0, 0)); dl = ImageDraw.Draw(lay); dl.rounded_rectangle((8, 8, 752, 222), 24, fill=(14, 12, 10, 215), outline=AMBER + (255,), width=12)
        t1 = L('NOT TO BE WORN', 'వేసుకోవడం నిషేధం'); t2 = L('FROM 25 DEC 1722', '25 డిసెంబర్ 1722 నుంచి')
        f1, _ = fit(t1, 'head', 74, 680); f2, _ = fit(t2, 'monob', 40, 680)
        dl.text((380, 92), t1, font=f1, fill=AMBER + (255,), anchor='mm'); dl.text((380, 172), t2, font=f2, fill=AMBER + (255,), anchor='mm')
        lay = lay.rotate(-8, expand=True, resample=Image.BICUBIC); paste_c(img, lay, W / 2, 900, clamp(ks), 1.6 - .6 * min(1, ks))
        k2 = e_out(prog(t, c_stamp + 0.3, c_stamp + 0.7))
        dark_panel(img, (110, 1500, 970, 1640), 22, int(220 * k2))
        text(img, L('1721 ACT · CERTAIN PRINTED CALICOES', '1721 చట్టం · కొన్ని రకాల అచ్చు calico లు'), W / 2, 1545, 34, CREAM, kind='head', a=k2, maxw=820)
        text(img, L('SOME EXCEPTIONS · IN FORCE UNTIL 1774', 'కొన్ని మినహాయింపులు · 1774 వరకు'), W / 2, 1600, 30, AMBER, kind='monob', a=k2, maxw=820)
    text(img, 'Dress in chintz, c.1770–90 · Hugo Maertens · CC BY-SA 3.0', W / 2, 1680, 22, GREY, kind='mono')
    return img

# ---- series slide (platform specific, phone-readable: 3 items + button)
@functools.lru_cache(1)
def FILM_THUMB():
    return Image.open(f'/home/claude/why-channel-studio/videos/2026-11-08_long_golden_sparrow_s1/thumb_golden_sparrow_film_{LANGV.upper()}.jpg').convert('RGB')

def s_slide(t, s0, s1, plat=None):
    plat = plat or PLAT; v = t - s0
    img = radial_bg(W, H, (34, 28, 18), (8, 8, 9), cy=.4, reach=.8).copy()
    tx(img, L('THE GOLDEN SPARROW · SEASON 1', 'బంగారు పిచ్చుక · సీజన్ 1'), W / 2, 250, 40, AMBER, kind='head', maxw=ST.sw)
    rows = [(L('1/6', '1/6'), L('Was India really rich?', 'మనం నిజంగా ధనికులమా?'), L("YOU'RE HERE", 'మీరు ఇక్కడ'), True),
            (L('NEXT · 2/6', 'తర్వాత · 2/6'), L('The cloth the world wanted', 'ప్రపంచం కోరుకున్న గుడ్డ'), L('TOMORROW', 'రేపు'), False)]
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
def render(t):
    scn, s0, s1 = scene_at(t)
    if scn == 'hook': img = s_hook(t, s0, s1)
    elif scn == 'cartoon1': img = cartoon(t, s0, [('CHELLI', 'Q1')])
    elif scn == 'chart': img = s_chart(t, s0, s1)
    elif scn == 'circle': img = s_circle(t, s0, s1)
    elif scn == 'cartoon2': img = cartoon(t, s0, [('CHELLI', 'Q2'), ('ANNA', '1.5')])
    elif scn == 'people': img = s_people(t, s0, s1)
    elif scn == 'paper': img = s_paper(t, s0, s1)
    elif scn == 'cartoon3': img = cartoon(t, s0, [('CHELLI', 'Q3')])
    elif scn == 'reveal': img = s_reveal(t, s0, s1)
    elif scn == 'tease': img = s_tease(t, s0, s1)
    elif scn == 'slide': img = s_slide(t, s0, s1)
    else:
        img = s_loop(t, s0, s1); captions(img, t, 'loop'); return img
    img = img.convert('RGB')
    if scn in ('chart', 'circle', 'people', 'paper', 'cartoon1', 'cartoon2', 'cartoon3'): img = zoom(img, 1 + 0.045 * e_io(prog(t, s0, s1)))
    overlays(img, t, scn); captions(img, t, scn); return img

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
