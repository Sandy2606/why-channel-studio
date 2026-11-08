"""6) Maths Diagram: axes draw on, a curve traces itself, working appears line by line.
Best for: growth, percentages, compound interest, step-by-step calculations."""
import math
import numpy as np
from PIL import Image, ImageDraw
from core import *

DURATION = 7.0
DEFAULT = dict(title='WHY MONEY DOUBLES', xlabel='YEARS', f=lambda x: 100 * 1.10 ** x, x=(0, 10), y=(0, 280), xticks=[0, 5, 10], yticks=[100, 200],
               marks=[dict(x=7.27, label='DOUBLED IN 7.3 YEARS')], steps=['100 × 1.10^{n}', '100 × 1.10^{7} ≈ 195'], trace=(.5, 5.6))


def _math(img, s, x, y, px, col, a=1.0, anchor='l'):
    """Plain text with ^{...} superscripts."""
    parts = []; i = 0
    while i < len(s):
        j = s.find('^{', i)
        if j < 0: parts.append((s[i:], 0)); break
        parts.append((s[i:j], 0)); e = s.index('}', j); parts.append((s[j + 2:e], 1)); i = e + 1
    fa = font('monob', px); fb = font('monob', int(px * .62)); tot = sum((fb if u else fa).getlength(t) for t, u in parts)
    cx = x - tot / 2 if anchor == 'm' else x
    for t, u in parts:
        text(img, t, cx, y - (px * .34 if u else 0), int(px * .62) if u else px, col, 'lm', 'monob', a=a); cx += (fb if u else fa).getlength(t)


def draw(st, v, spec=None):
    s = merge(DEFAULT, spec); SS = 2; W, H = st.W, st.H; P = st.portrait
    base = radial_bg(W, H, (22, 24, 30), (8, 8, 10), cy=.5, reach=.8).copy(); im = base.resize((W * SS, H * SS), Image.BILINEAR); d = ImageDraw.Draw(im)
    for x in range(0, W * SS, 120 * SS // 2): d.line([(x, 0), (x, H * SS)], fill=(26, 28, 34), width=2)
    for y in range(0, H * SS, 120 * SS // 2): d.line([(0, y), (W * SS, y)], fill=(26, 28, 34), width=2)
    bx0, by0, bx1, by1 = (st.x0 + 100, st.y0 + 400, st.x1 - 26, st.y1 - 110) if P else (st.x0 + 110, st.y0 + 130, st.x0 + st.sw * .63, st.y1 - 90)
    X = lambda x: lerp(bx0, bx1, (x - s['x'][0]) / (s['x'][1] - s['x'][0])) * SS
    Y = lambda y: lerp(by1, by0, (y - s['y'][0]) / (s['y'][1] - s['y'][0])) * SS
    ka = e_io(prog(v, -.3, .35)); d.line([(bx0 * SS, by1 * SS), (lerp(bx0, bx1, ka) * SS, by1 * SS)], fill=CREAM, width=6); d.line([(bx0 * SS, by1 * SS), (bx0 * SS, lerp(by1, by0, ka) * SS)], fill=CREAM, width=6)
    k = e_io(prog(v, *s['trace'])) * .999 + .001; x1 = lerp(s['x'][0], s['x'][1], k); xs = np.linspace(s['x'][0], x1, 240); pts = [(X(float(x)), Y(float(s['f'](float(x))))) for x in xs]
    lay = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(lay).polygon(pts + [(pts[-1][0], by1 * SS), (pts[0][0], by1 * SS)], fill=AMBER + (46,)); im.paste(lay, (0, 0), lay); d = ImageDraw.Draw(im)
    for m in s['marks']:
        if x1 >= m['x']:
            mx, my = X(m['x']), Y(s['f'](m['x']))
            for yy in np.arange(my, by1 * SS, 34): d.line([(mx, yy), (mx, min(yy + 18, by1 * SS))], fill=CREAM, width=4)
            for xx in np.arange(bx0 * SS, mx, 34): d.line([(xx, my), (min(xx + 18, mx), my)], fill=CREAM, width=4)
    d.line(pts, fill=AMBER, width=12, joint='curve')
    out = im.resize((W, H), Image.LANCZOS); L = Image.new('RGB', (W, H), 0); dl = ImageDraw.Draw(L); dl.line([(a / SS, b / SS) for a, b in pts], fill=AMBER, width=10); out = glow(out, L, 26, .95)
    head = pts[-1]; hx, hy = head[0] / SS, head[1] / SS; L = Image.new('RGB', (W, H), 0); dl = ImageDraw.Draw(L); dl.ellipse((hx - 18, hy - 18, hx + 18, hy + 18), fill=AMBER); out = glow(out, L, 46, 1.0); d = ImageDraw.Draw(out); d.ellipse((hx - 11, hy - 11, hx + 11, hy + 11), fill=(255, 244, 214))
    a = prog(v, -.1, .3); fm = '{:,.0f}'
    for t in s['xticks']: text(out, str(t), X(t) / SS, by1 + 40, 38, CREAM, kind='mono', a=a)
    for t in s['yticks']: text(out, fm.format(t), bx0 - 18, Y(t) / SS, 38, CREAM, 'rm', 'mono', a=a)
    text(out, s['xlabel'], (bx0 + bx1) / 2, by1 + 86, st.label, GREY, kind='monob', a=a)
    text(out, s['title'], st.cx if P else st.x0, st.y0 + 44, 78 if P else 82, CREAM, 'mm' if P else 'lm', maxw=st.sw)
    n = len(s['steps']); tb = s['trace'][0]; dur = s['trace'][1] - tb
    for i, f_ in enumerate(s['steps']):
        t0 = tb + dur * i / n; a_ = prog(v, t0, t0 + .3); lit = i == sum(1 for j in range(n) if v >= tb + dur * j / n) - 1
        if P: _math(out, f_, st.cx, st.y0 + 170 + i * 92, 62, AMBER if lit else CREAM, a_, 'm')
        else: _math(out, f_, bx1 + 90, st.y0 + 280 + i * 118, 52, AMBER if lit else CREAM, a_)
    for m in s['marks']:
        if x1 >= m['x']:
            kk = e_back(prog(x1, m['x'], m['x'] + .55)); mx, my = X(m['x']) / SS, Y(s['f'](m['x'])) / SS
            pill(out, m['label'], clamp(mx - 40, st.x0 + 330, st.x1 - 330) if P else mx - 40, my - 86, 40, AMBER, INK, scale=kk, maxw=st.sw - 40)
    return out
