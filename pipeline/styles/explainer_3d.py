"""5) 3D Explainer: a solid object pulls apart into labelled layers while the camera moves round it.
Best for: what is inside something, stacked systems, layers of the Earth or air, how a device is built."""
import math
import numpy as np
from PIL import Image, ImageDraw
from core import *

DURATION = 10.0
DEFAULT = dict(title='WHAT IS UNDER YOUR FEET?', layers=[dict(label='CRUST', sub='ABOUT 35 KM', col=(112, 138, 112), r=2.1), dict(label='MANTLE', sub='ABOUT 2,900 KM', col=(186, 104, 52), r=2.0),
               dict(label='OUTER CORE', sub='ABOUT 2,200 KM', col=(232, 148, 48), r=1.85), dict(label='INNER CORE', sub='ABOUT 1,220 KM', col=(250, 214, 130), r=1.65)], split=(.5, 2.0), beat=1.75)


def _disc(d, cam, y, r, h, col, spin, dim):
    N = 96; col = shade(col, dim); strips = []
    for i in range(N):
        a0, a1 = i / N * 2 * math.pi, (i + 1) / N * 2 * math.pi; mid = (a0 + a1) / 2; n = np.array((math.cos(mid), 0, math.sin(mid))); P = np.array((n[0] * r, y, n[2] * r))
        if n @ (cam.eye - P) <= 0: continue
        k = .42 + .78 * max(0, float(n @ np.array((-.62, 0, -.78))))
        q = [cam.pt((math.cos(a) * r, yy, math.sin(a) * r)) for a, yy in ((a0, y + h), (a1 + .006, y + h), (a1 + .006, y), (a0, y))]; d.polygon(q, fill=shade(col, k))
    top = [cam.pt((math.cos(i / 120 * 2 * math.pi) * r, y + h, math.sin(i / 120 * 2 * math.pi) * r)) for i in range(120)]; d.polygon(top, fill=shade(col, 1.14)); d.line(top + [top[0]], fill=shade(col, 1.5), width=4)
    for j in range(24):
        a = spin + j / 24 * 2 * math.pi; d.line([cam.pt((math.cos(a) * r * .86, y + h + .002, math.sin(a) * r * .86)), cam.pt((math.cos(a) * r * .95, y + h + .002, math.sin(a) * r * .95))], fill=shade(col, .86), width=4)


def draw(st, v, spec=None):
    s = merge(DEFAULT, spec); SS = 2; W, H = st.W * SS, st.H * SS; L = s['layers']; n = len(L)
    bg = radial_bg(st.W, st.H, (34, 32, 30), (8, 8, 9), cy=.5, reach=.75).resize((W, H), Image.BILINEAR); d = ImageDraw.Draw(bg)
    ks = e_io(prog(v, *s['split'])); gap = lerp(.0, 1.0 if st.portrait else .62, ks); th = .72 if st.portrait else .58; total = n * th + (n - 1) * gap
    a = math.radians(-38 + 30 * e_io(prog(v, 0, DURATION))); elev = 7.0 if st.portrait else 5.0; R = 15.0 if st.portrait else 10.8
    tx = 0 if st.portrait else -2.3; cam = Cam((math.sin(a) * R + tx, total / 2 + elev, -math.cos(a) * R), (tx, total / 2 + (.55 if st.portrait else 0), 0), 38 if st.portrait else 34, W, H)
    t_first = s['split'][1] - .1; act = int(clamp((v - t_first) // s['beat'], 0, n - 1)) if v >= t_first else -1
    placed = []
    for i in range(n - 1, -1, -1):     # first layer sits on top
        y = (n - 1 - i) * (th + gap); lift = e_back(prog(v - t_first - i * s['beat'], 0, .35)) * .1 if act == i else 0; dim = 1.0 if act in (-1, i) else .5
        _disc(d, cam, y + lift, L[i]['r'] * (1 + .03 * (act == i)), th, L[i]['col'], v * .45, dim); placed.append((i, y + lift))
    out = bg.resize((st.W, st.H), Image.LANCZOS)
    for i, y in placed:
        dr = np.array((cam.eye[0], cam.eye[2])); dr /= np.linalg.norm(dr); fx, fy = cam.pt((dr[0] * L[i]['r'], y + th / 2, dr[1] * L[i]['r'])); fx /= SS; fy /= SS
        c = L[i]['col']; dark = sum(c) / 3 > 140; col = INK if dark else CREAM
        if act in (-1, i): text(out, L[i]['label'], fx, fy, 44 if st.portrait else 36, col, maxw=560)
    text(out, s['title'], st.cx, st.y0 + 44, 74 if st.portrait else 76, CREAM, maxw=st.sw)
    if act >= 0:
        k = e_back(prog((v - t_first) % s['beat'], 0, .3)) if act < n - 1 or v - t_first < n * s['beat'] else 1
        px, py = (st.cx, st.y1 - 10) if st.portrait else (int(st.x0 + st.sw * .22), st.cy + 40)
        pill(out, L[act]['label'] + ' · ' + L[act]['sub'] if st.portrait else L[act]['sub'], px, py, 54 if st.portrait else 56, AMBER, INK, scale=k, maxw=st.sw - 40 if st.portrait else 640, pad=(32, 20))
        if not st.portrait: text(out, L[act]['label'], px, py - 90, 62, CREAM, maxw=660)
    return out
