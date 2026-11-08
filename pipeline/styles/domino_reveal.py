"""8) Domino Reveal: one small cause knocks over the next until the big answer lands.
Best for: chain reactions, 'and that is why...', cause-and-effect stories, the payoff of a video."""
import math
import numpy as np
from PIL import Image, ImageDraw
from core import *

DURATION = 9.0
DEFAULT = dict(title=None, steps=['RAINS FAIL', 'CROPS DIE', 'PRICES JUMP', 'WAGES CRASH'], reveal='THE LOOMS WENT SILENT', reveal_sub='BENGAL · 1770', per_step=3, speed=2.4, start=.25, hits=None)   # hits: voice-cue seconds, one per step, then one for the reveal
DT, DD, DH, GAP = .2, 1.15, 1.9, .95


def _lean(u):
    return math.radians(74) * (1 - (1 - clamp(u)) ** 2.2)


def draw(st, v, spec=None):
    s = merge(DEFAULT, spec); SS = 2; W, H = st.W * SS, st.H * SS; P = st.portrait; steps = s['steps']; ps = s['per_step']; total = len(steps) * ps + 1
    bg = radial_bg(st.W, st.H, (44, 37, 25), (8, 8, 9), cy=.62, reach=.72).resize((W, H), Image.BILINEAR); d = ImageDraw.Draw(bg)
    wend = total + .8
    if s['hits']:
        ks = list(s['hits']); t_end = ks[-1]; wv = float(np.interp(v, [s['start']] + ks, [0] + [(j + 1) * ps for j in range(len(steps))] + [wend]))
    else: t_end = s['start'] + wend / s['speed']; wv = clamp((v - s['start']) * s['speed'], 0, wend); tx = (min(wv, total - 1) - .2) * GAP
    pull = e_io(prog(v, t_end - .15, t_end + .75))
    # camera rides behind the wave and looks down the line, so the row recedes (works on 9:16 and 16:9)
    far = (8.0, 6.2, -7.4) if P else (6.8, 5.2, -9.0)
    eye = (tx - lerp(far[0], 7.0 if P else 7.5, pull), lerp(far[1], 11.5 if P else 9.5, pull), lerp(far[2], -9.5 if P else -12.0, pull))
    tg = (tx + lerp(2.4, -2.6 if P else -2.4, pull), lerp(3.0 if P else 2.05, 3.9 if P else 2.9, pull), 0); fov = 40 if P else 32
    cam = Cam(eye, tg, fov, W, H)
    for i in range(-30, 46): d.line([cam.pt((tx + i, 0, -24)), cam.pt((tx + i, 0, 24))], fill=(36, 33, 29), width=2)
    for z in range(-24, 25): d.line([cam.pt((tx - 30, 0, z)), cam.pt((tx + 46, 0, z))], fill=(36, 33, 29), width=2)
    rng = np.random.default_rng(2); order = []
    for i in range(total):
        step = i % ps == ps - 1 and i < total - 1; order.append((i, (((i + 1) // ps) if step else int(rng.integers(0, 5)))))
    px_unit = np.linalg.norm(np.array(cam.pt((tx, 1, 0))) - np.array(cam.pt((tx, 0, 0))))
    for i, pips in sorted(order, key=lambda q: -np.linalg.norm(np.array((q[0] * GAP, 1, 0)) - cam.eye)):
        x = i * GAP; u = (wv - i) / 1.1; R = rot_axis('z', -_lean(u) if u > 0 else 0.0); pv = np.array((x + DT / 2, 0, 0)); step = i % ps == ps - 1 and i < total - 1; hero = i == total - 1
        col = AMBER if hero or step else (232, 226, 212); sc = 1.5 if hero else 1.0; hh = DH * sc; dd = DD * sc
        paint(d, box_faces(cam, (x, hh / 2, 0), (DT, hh, dd), col, R=R, pivot=pv, edge=False), 1)
        fp = lambda py, pz: cam.pt(((np.array((x - DT / 2 - .004, py, pz)) - pv) @ R.T + pv))
        ink = (34, 28, 20)
        if eye[0] < x - DT / 2 or u > .35:
            d.line([fp(hh * .5, -dd * .42), fp(hh * .5, dd * .42)], fill=ink, width=5 * SS)
            grid = [(.5, .5), (.25, .25), (.75, .75), (.25, .75), (.75, .25), (.25, .5), (.75, .5)]
            for gy, gz in grid[:pips] if pips % 2 else grid[1:1 + pips]:
                cxp, cyp = fp(hh * (.56 + .4 * gy), dd * (gz - .5) * .8); r = .075 * px_unit * sc * (9.0 / max(np.linalg.norm(cam.eye - np.array((x, 1, 0))), 1))
                d.ellipse((cxp - r, cyp - r, cxp + r, cyp + r), fill=ink)
    out = bg.resize((st.W, st.H), Image.LANCZOS)
    done = int(min(len(steps), wv // ps)) if wv >= ps * .7 else 0; cur = int(clamp(math.floor((wv + .3) / ps), 0, len(steps))); yc = st.y0 + 140 if P else st.y0 + 90
    for j in range(len(steps)):
        hit = (s['hits'][j] if s['hits'] else s['start'] + (j + 1) * ps / s['speed']) - .32; k = e_back(prog(v, hit, hit + .25)); out_k = 1 - e_io(prog(v, t_end - .1, t_end + .22))
        if k <= .01 or out_k <= .01: continue
        if P: x_, y_ = st.cx, yc + j * 104
        else: x_, y_ = st.x0 + 40 + (j % 2) * 0, yc + j * 86
        lab = '%d  %s' % (j + 1, steps[j]); hot = j == cur - 1
        if P: pill(out, lab, x_, y_, 56, AMBER if hot else (40, 38, 34), INK if hot else CREAM, a=out_k, scale=k, maxw=st.sw - 60, pad=(30, 16))
        else: f = pick(lab, 'head', 52); w = f.getlength(lab) + 64; pill(out, lab, st.x0 + w / 2, y_, 52, AMBER if hot else (40, 38, 34), INK if hot else CREAM, a=out_k, scale=k, pad=(30, 16))
    if v > t_end - .05:
        k = e_back(prog(v, t_end, t_end + .35), 1.3); L = wrap(s['reveal'], 'head', 124 if P else 132, st.sw); yy = st.y0 + (250 if P else 170)
        if k > .02:
            lay = Image.new('RGB', (st.W, st.H), 0)
            for i, l in enumerate(L): text(lay, l, st.cx, yy + i * (136 if P else 142), 124 if P else 132, AMBER, maxw=st.sw)
            out = glow(out, lay, 60, .55 * clamp(k))
            for i, l in enumerate(L): text(out, l, st.cx, yy + i * (136 if P else 142), 124 if P else 132, CREAM, a=clamp(k), maxw=st.sw)
            text(out, s['reveal_sub'], st.cx, yy + len(L) * (136 if P else 142) - 10, 46, AMBER, kind='monob', a=prog(v, t_end + .2, t_end + .45))
    return out
