"""3) 3D Data Chart: bars grow in real perspective while the camera orbits, one hero bar glows.
Best for: comparisons, prices over time, rankings, old-vs-new scoreboards."""
import math
import numpy as np
from PIL import Image, ImageDraw
from core import *

DURATION = 8.0
DEFAULT = dict(title="INDIA'S SHARE OF WORLD GDP", unit='%', decimals=0, source='SOURCE: MADDISON PROJECT',
               start=.35, stagger=.28, bars=[dict(label='1700', value=24, hero=True), dict(label='1820', value=16), dict(label='1913', value=8), dict(label='1950', value=4)], ref=None)


def draw(st, v, spec=None):
    s = merge(DEFAULT, spec); SS = 2; W, H = st.W * SS, st.H * SS; bars = s['bars']; n = len(bars)
    bg = radial_bg(st.W, st.H, (40, 34, 24), (9, 9, 9), cy=.52, reach=.72).resize((W, H), Image.BILINEAR); d = ImageDraw.Draw(bg)
    gap = 1.55; span = (n - 1) * gap; vmax = max(b['value'] for b in bars); HT = 5.3 if st.portrait else 3.25
    a = math.radians(-24 + 15 * e_io(prog(v, 0, DURATION))); R = (span * 2.2 + 9) if st.portrait else (span * .95 + 6)
    eye = (math.sin(a) * R, 5.5 if st.portrait else 3.3, -math.cos(a) * R); cam = Cam(eye, (0, (HT * .5 - .66) if st.portrait else HT * .5, 0), 40 if st.portrait else 34, W, H)
    ext = span / 2 + 6
    for i in range(-24, 25):                 # floor grid runs off-frame
        for A, B in (((i, 0, -24), (i, 0, 24)), ((-24, 0, i), (24, 0, i))):
            pa, pb = cam.pt(A), cam.pt(B); d.line([pa, pb], fill=(40, 38, 34), width=2)
    faces = []; hero_faces = []; tops = []; bases = []
    for i, b in enumerate(bars):
        x = i * gap - span / 2; t0 = s['start'] + i * s['stagger']; k = e_out(prog(v, t0, t0 + 1.25)); h = max(.03, b['value'] / vmax * HT * k)
        col = AMBER if b.get('hero') else (112, 108, 100); f = box_faces(cam, (x, h / 2, 0), (1.05, h, 1.05), col, top=shade(col, 1.15))
        sh = [cam.pt((x - .5, 0.005, -.5)), cam.pt((x + 1.0, 0.005, -.5 + .1)), cam.pt((x + 1.2, 0.005, .9)), cam.pt((x - .3, .005, .85))]
        d.polygon(sh, fill=(14, 13, 12)); faces += f
        if b.get('hero'): hero_faces += f
        tops.append((cam.pt((x, h + .08, 0)), b['value'] * k, prog(v, t0, t0 + .2))); bases.append(cam.pt((x, 0, -.95)))
    paint(d, faces, 2)
    if s.get('ref'):
        y = s['ref']['value'] / vmax * HT; k = e_io(prog(v, 1.8, 2.5))
        d.line([cam.pt((-span / 2 - 1.0, y, 0)), cam.pt((lerp(-span / 2 - 1.0, span / 2 + 1.2, k), y, 0))], fill=CREAM, width=6)
    out = bg.resize((st.W, st.H), Image.LANCZOS)
    if hero_faces:
        L = Image.new('RGB', (W, H), 0); paint(ImageDraw.Draw(L), hero_faces, 1); out = glow(out, L.resize((st.W, st.H), Image.BILINEAR), 70, .62)
    fm = '{:,.%df}' % s['decimals']
    for (p, val, a_), b in zip(tops, bars):
        text(out, fm.format(val) + s['unit'], p[0] / SS, p[1] / SS - 42, 62 if st.portrait else 58, AMBER if b.get('hero') else CREAM, a=a_)
    for p, b in zip(bases, bars): text(out, b['label'], p[0] / SS, p[1] / SS + 30, 42 if st.portrait else 38, CREAM, kind='monob')
    lines = wrap(s['title'], 'head', 78 if st.portrait else 70, st.sw) if st.portrait else [s['title']]
    for i, l in enumerate(lines): text(out, l, st.cx, st.y0 + 44 + i * 90, 78 if st.portrait else 70, CREAM, maxw=st.sw)
    if s.get('ref'): text(out, s['ref']['label'], st.x1, st.y0 + 44 + len(lines) * 84, st.label, CREAM, 'rm', 'monob', a=prog(v, 2.3, 2.7))
    if s['source']: text(out, s['source'], st.cx, st.y1 - 18 if st.portrait else st.y0 + 104, 34, GREY, kind='mono', maxw=st.sw)
    return out
