"""1) Isometric: a small world seen from above; blocks rise, goods flow along a road.
Best for: supply chains, how a system works, how money or goods move."""
import numpy as np
from PIL import Image, ImageDraw
from core import *

DURATION = 9.0
THEMES = {'light': dict(bg=(240, 236, 226), tile=(232, 227, 215), line=(218, 212, 198), road=(205, 197, 180), body=(84, 80, 74), text=INK, prop=(120, 150, 128)),
          'dark': dict(bg=(16, 16, 15), tile=(24, 23, 22), line=(38, 37, 34), road=(58, 54, 46), body=(112, 106, 96), text=CREAM, prop=(70, 110, 92))}
DEFAULT = dict(theme='light', title='COTTON TO CLOTH', sub='HOW ONE BALE TRAVELLED',
               items=[dict(label='FARM', h=.7, w=2.0), dict(label='MILL', h=2.3, w=1.8, hero=True), dict(label='PORT', h=1.2, w=2.2)], start=.0, stagger=.7, gap=1.7)


def _iso(st, U, ox, oy, x, y, z=0): return ox + (x - y) * U * .866, oy + (x + y) * U * .5 - z * U


def _box(d, p, x, y, w, h, col, win=False, dark=(50, 48, 44)):
    a = w / 2; L, R, B, F = p(x - a, y + a), p(x + a, y - a), p(x - a, y - a), p(x + a, y + a)
    up = lambda q: (q[0], q[1] - (L[1] - p(x - a, y + a, h)[1]))
    d.polygon([L, F, up(F), up(L)], fill=shade(col, .78)); d.polygon([F, R, up(R), up(F)], fill=shade(col, .58))
    d.polygon([up(L), up(F), up(R), up(B)], fill=shade(col, 1.12))
    if win and h > .35:
        for face, (A, Bb) in enumerate(((L, F), (F, R))):
            rows = max(1, int(h / .42)); cols = max(2, int(w / .42))
            for i in range(cols):
                for j in range(rows):
                    u0, u1 = (i + .25) / cols, (i + .75) / cols; v0, v1 = (j + .25) / rows, (j + .72) / rows
                    def q(u, v_):
                        return lerp(A[0], Bb[0], u), lerp(A[1], Bb[1], u) - v_ * (L[1] - up(L)[1])
                    d.polygon([q(u0, v0), q(u1, v0), q(u1, v1), q(u0, v1)], fill=dark if (i + j + face) % 3 else AMBER)


def draw(st, v, spec=None):
    s = merge(DEFAULT, spec); th = THEMES[s['theme']]; SS = 2; W, H = st.W * SS, st.H * SS
    img = Image.new('RGB', (W, H), th['bg']); d = ImageDraw.Draw(img)
    items = s['items']; n = len(items); span = (n - 1) * (s['gap'] * (1.85 if st.portrait else 1.25))
    U = (106 if st.portrait else 104) * SS * (1 + .045 * e_io(prog(v, 0, DURATION)))
    # the chain runs top-to-bottom on portrait and left-to-right on wide
    pos = [(i - (n - 1) / 2) * (s['gap'] * (1.85 if st.portrait else 1.25)) for i in range(n)]
    xy = [(q, q) if st.portrait else (q, -q) for q in pos]
    ox, oy = W / 2, (st.cy + (105 if st.portrait else 150)) * SS
    p = lambda x, y, z=0: _iso(st, U, ox, oy, x, y, z)
    # tiled floor bleeding off every edge (never a box inside the frame)
    R = 14
    for i in range(-R, R):
        for j in range(-R, R):
            if (i + j) % 2 == 0: d.polygon([p(i, j), p(i + 1, j), p(i + 1, j + 1), p(i, j + 1)], fill=th['tile'])
    for i in range(1, n):
        a, b = xy[i - 1], xy[i]; k = e_io(prog(v, s['start'] + .2 + i * s['stagger'], s['start'] + .9 + i * s['stagger']))
        e = (lerp(a[0], b[0], k), lerp(a[1], b[1], k)); hw = .2
        nx, ny = (hw, -hw) if st.portrait else (hw, hw)
        d.polygon([p(a[0] + nx, a[1] + ny), p(e[0] + nx, e[1] + ny), p(e[0] - nx, e[1] - ny), p(a[0] - nx, a[1] - ny)], fill=th['road'])
    # props pop in around the buildings
    rng = np.random.default_rng(5); props = []
    for i in range(16):
        q = (rng.uniform(-span / 2 - 1, span / 2 + 1), rng.uniform(.95, 2.2) * rng.choice((-1, 1)))
        x_, y_ = (q[0] + q[1] * .75, q[0] - q[1] * .75) if st.portrait else (q[0] + q[1] * .75, -q[0] + q[1] * .75)
        props.append((x_, y_, rng.uniform(.14, .26), rng.uniform(.2, .55), rng.uniform(.1, 2)))
    draws = [(x_ + y_, 'p', (x_, y_, w_, h_, t_)) for x_, y_, w_, h_, t_ in props]
    for i, it in enumerate(items): draws.append((xy[i][0] + xy[i][1], 'b', i))
    for i in range(1, n):            # goods moving along the finished road
        a, b = xy[i - 1], xy[i]; t0 = s['start'] + 1.0 + i * s['stagger']
        for m in range(3):
            u = (v - t0) * .42 + m / 3
            if v < t0: continue
            u %= 1.0; x_, y_ = lerp(a[0], b[0], u), lerp(a[1], b[1], u); draws.append((x_ + y_, 'g', (x_, y_)))
    for _, kind, o in sorted(draws, key=lambda q: q[0]):
        if kind == 'p':
            k = e_back(prog(v, o[4], o[4] + .4))
            if k > 0.01: _box(d, p, o[0], o[1], o[2], o[3] * k, th['prop'])
        elif kind == 'g':
            _box(d, p, o[0], o[1], .24, .24, AMBER)
        else:
            it = items[o]; t0 = s['start'] - .3 + o * s['stagger']; k = e_back(prog(v, t0, t0 + .55))
            if k <= 0.01: continue
            w = it.get('w', 1.6); x_, y_ = xy[o]; sh = [p(x_ - w / 2, y_ + w / 2), p(x_ + w / 2, y_ + w / 2), p(x_ + w / 2 + .7, y_ - w / 2 + .1), p(x_ - w / 2 + .9, y_ - w / 2 - .4)]
            d.polygon(sh, fill=shade(th['bg'], .84))
            _box(d, p, x_, y_, w, max(.02, it.get('h', 1.2) * k), AMBER if it.get('hero') else th['body'], win=True, dark=shade(th['body'], .55) if not it.get('hero') else (150, 96, 14))
    out = img.resize((st.W, st.H), Image.LANCZOS)
    text(out, s['title'], st.cx, st.y0 + 48, 76 if st.portrait else 84, th['text'], maxw=st.sw)
    text(out, s['sub'], st.cx, st.y0 + 118, st.label, shade(th['text'], .6) if s['theme'] == 'dark' else (112, 106, 96), kind='monob', maxw=st.sw)
    for i, it in enumerate(items):
        t0 = s['start'] + i * s['stagger'] + .05; k = e_back(prog(v, t0, t0 + .35)); x_, y_ = xy[i]; h = it.get('h', 1.2)
        px, py = p(x_, y_, h + .42 + .35); pill(out, it['label'], px / SS, py / SS, 42, AMBER if it.get('hero') else th['text'], INK if it.get('hero') else th['bg'], scale=k, maxw=360)
    return out
