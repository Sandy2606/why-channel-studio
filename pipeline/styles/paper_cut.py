"""2) Paper-cut: layered cut-paper dioramas with real drop shadows, moving at 12 fps like stop-motion.
Best for: history, folk stories, festivals, 'long ago' sections."""
import functools, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from core import *

DURATION = 9.0
DEFAULT = dict(title='LONG BEFORE THE SHIPS', sub='INDIA · 1600', sun=True, scene='village', tags=[dict(t=2.6, text='A QUARTER OF THE WORLD ECONOMY')],
               palette=[(244, 226, 188), (240, 194, 120), (226, 150, 66), (168, 102, 52), (92, 70, 58), (38, 44, 48)])


def _ridge(W, H, y, amp, seed):
    rng = np.random.default_rng(seed); ph = rng.uniform(0, 6.3, 4); fq = rng.uniform(.7, 1.6, 4) * np.array([1, 2.1, 3.7, 6.3])
    xs = np.linspace(-.1, 1.1, 180); ys = y * H + amp * H * sum(np.sin(xs * 6.3 * f + p) / (1 + i) for i, (f, p) in enumerate(zip(fq, ph)))
    return [(float(x * W), float(q)) for x, q in zip(xs, ys)]


def _ground_at(ridge, x): return min(ridge, key=lambda p: abs(p[0] - x))[1]


def _tree(d, x, y, s):
    d.rectangle((x - s * .06, y - s * .4, x + s * .06, y + s * .1), fill=255)
    for i in range(3):
        k = 1 - i * .24; yy = y - s * (.25 + i * .34); d.polygon([(x - s * .46 * k, yy), (x + s * .46 * k, yy), (x, yy - s * .62 * k)], fill=255)


def _hut(d, x, y, s):
    d.rectangle((x - s * .5, y - s * .55, x + s * .5, y + s * .1), fill=255)
    d.polygon([(x - s * .72, y - s * .5), (x + s * .72, y - s * .5), (x, y - s * 1.15)], fill=255)


def _temple(d, x, y, s):
    for i in range(6):
        k = 1 - i * .15; d.rectangle((x - s * .75 * k, y - s * (i + 1) * .34, x + s * .75 * k, y - s * i * .34 + 2), fill=255)
    d.polygon([(x - s * .14, y - s * 2.0), (x + s * .14, y - s * 2.0), (x, y - s * 2.5)], fill=255); d.rectangle((x - s * .95, y - s * .2, x + s * .95, y + s * .12), fill=255)


@functools.lru_cache(12)
def _layer(W, H, idx, col, shadow, y_, amp, seed, deco):
    SS = 2; m = Image.new('L', (W * SS, H * SS), 0); d = ImageDraw.Draw(m); r = [(x * SS, q * SS) for x, q in _ridge(W, H, y_, amp, seed)]
    d.polygon(r + [(W * SS * 1.1, (H + 400) * SS), (-W * SS * .1, (H + 400) * SS)], fill=255)
    rng = np.random.default_rng(seed + 9)
    for kind, fx, s in deco:
        x = fx * W * SS; y = _ground_at(r, x) + 8 * SS; s *= H * SS
        {'tree': _tree, 'hut': _hut, 'temple': _temple}[kind](d, x, y, s)
    m = m.resize((W, H + 260), Image.LANCZOS); a = np.asarray(m, 'float32') / 255
    tex = np.asarray(col, 'float32')[None, None] * (1 + grain(W, H + 260, .018 + .004 * idx)[..., None]); rgb = np.clip(tex, 0, 255)
    sh = np.asarray(m.filter(ImageFilter.GaussianBlur(shadow)), 'float32') / 255
    o = int(shadow * .9); sh = np.roll(np.roll(sh, o, 0), int(shadow * .45), 1) * .52; sh[:o + 1] = 0
    alpha = a + sh * (1 - a); out_rgb = rgb * (a / np.maximum(alpha, 1e-3))[..., None] + np.asarray((30, 16, 8), 'float32')[None, None] * (1 - a / np.maximum(alpha, 1e-3))[..., None]
    return Image.fromarray(np.dstack([np.clip(out_rgb, 0, 255), alpha * 255]).astype('uint8'), 'RGBA')


def _cut_title(img, s, x, y, px, col, maxw, a=1.0):
    f, px = fit(s, 'head', px, maxw); W, H = img.size; m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).text((x, y), s, font=f, fill=255, anchor='mm')
    sh = m.filter(ImageFilter.GaussianBlur(7)); img.paste((40, 22, 12), (9, 12), sh.point(lambda p: int(p * .55 * a))); img.paste(col, (0, 0), m.point(lambda p: int(p * a)))


def draw(st, v, spec=None):
    s = merge(DEFAULT, spec); W, H = st.W, st.H; vs = stepped(v, 12); pal = s['palette']; img = Image.new('RGB', (W, H), pal[0])
    arr = np.clip(np.asarray(img, 'float32') * (1 + grain(W, H, .02)[..., None]), 0, 255); img = Image.fromarray(arr.astype('uint8'))
    if s['sun']:
        sy = lerp(H * .50, H * .40, e_out(prog(vs, 0, 2.2))); R = W * (.2 if st.portrait else .11); cx = W * .66
        for k, c in ((1.45, mix(pal[0], pal[1], .35)), (1.2, mix(pal[0], pal[1], .7)), (1, CREAM)):
            sh = Image.new('L', (W, H), 0); ImageDraw.Draw(sh).ellipse((cx - R * k, sy - R * k, cx + R * k, sy + R * k), fill=255); sf = sh.filter(ImageFilter.GaussianBlur(5))
            img.paste((120, 70, 20), (4, 6), sf.point(lambda p: int(p * .24))); img.paste(c, (0, 0), sh)
    P = st.portrait
    decos = [[], [('temple', .3, .09 if P else .13)], [('tree', .12, .05 if P else .075), ('tree', .78, .06 if P else .09), ('tree', .9, .05 if P else .07)],
             [('hut', .2, .055 if P else .07), ('hut', .42, .045 if P else .06), ('tree', .64, .085 if P else .11), ('hut', .86, .05 if P else .06)], [('tree', .05, .11 if P else .17), ('tree', .93, .13 if P else .2)]]
    ys = [.55, .63, .71, .80, .91] if P else [.50, .58, .68, .79, .93]
    for i in range(5):
        lay = _layer(W, H, i, pal[i + 1], 9 + i * 4, ys[i], .022 - i * .002, 40 + i * 7, tuple(decos[i]))
        t0 = .12 * i; k = e_back(prog(vs, t0, t0 + .7), 1.2)
        y = (1 - k) * (120 + i * 60); x = math.sin(vs * .55 + i) * (5 + i * 7) + (vs - DURATION / 2) * (i - 1) * 3.2
        img.paste(lay, (int(x), int(y)), lay)
    title_y = st.y0 + 110 if P else st.y0 + 95
    tx = st.cx + math.sin(vs * 1.3) * 3
    _cut_title(img, s['title'], tx, title_y, 104 if P else 118, INK, st.sw)
    text(img, s['sub'], st.cx, title_y + (92 if P else 92), st.label + 6, (84, 58, 34), kind='monob', maxw=st.sw)
    for tg in s['tags']:
        k = e_back(prog(vs, tg['t'], tg['t'] + .4))
        if k > .02:
            py = st.y1 - 110 if P else st.y1 - 150
            pill(img, tg['text'], st.cx + (1 - k) * 80, py + math.sin(vs * 2) * 3, 44, CREAM, INK, scale=k, maxw=st.sw - 60, pad=(32, 20))
    return img
