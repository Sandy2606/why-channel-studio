"""9) Glow Atom: dark science diagram, orbiting particles, one element lit up and called out.
Best for: physics, chemistry, anything tiny, or any 'this one piece is what matters' moment."""
import functools, math
import numpy as np
from PIL import Image, ImageChops, ImageDraw
from core import *

DURATION = 9.0
BLUE = (96, 128, 214); TEAL = (86, 200, 196); STEEL = (138, 150, 172); NUC = (232, 124, 58)
DEFAULT = dict(name='Sodium', sub='Na · 11 electrons', shells=[2, 8, 1], nucleus=23, hi=-1, callout='Valence electron', callout_sub='the only one in the outer shell', footer='ELECTRONS PER SHELL', park=2.6, focus=3.4)


@functools.lru_cache(16)
def _ball(r, col):
    D = int(r * 2 + 2); yy, xx = np.mgrid[0:D, 0:D]; nx, ny = (xx - r) / r, (yy - r) / r; q = nx ** 2 + ny ** 2; z = np.sqrt(np.maximum(1 - q, 0))
    L = np.array((-.45, -.55, .7)); dif = np.maximum(0, nx * L[0] + ny * L[1] + z * L[2]); spec = dif ** 26
    rgb = np.array(col)[None, None] * (.26 + .86 * dif)[..., None] + 255 * spec[..., None] * .55; a = np.clip((1 - q) * r, 0, 1) * 255
    return Image.fromarray(np.dstack([np.clip(rgb, 0, 255), a]).astype('uint8'), 'RGBA')


def draw(st, v, spec=None):
    s = merge(DEFAULT, spec); W, H = st.W, st.H; P = st.portrait; img = radial_bg(W, H, (15, 30, 72), (2, 4, 14), cy=.5, reach=.68).copy()
    shells = s['shells']; n = len(shells); hi = (s['hi'] + n) % n; focus = e_io(prog(v, s['focus'], s['focus'] + 1)); zoom = 1 + .05 * e_io(prog(v, 0, DURATION))
    cx, cy = st.cx if P else W * .33, st.cy + 40 if P else st.cy + 20; Rmax = (st.sw * .5 * .97 if P else 390) * zoom; tilt = .62; roll = math.radians(-8 + 3 * math.sin(v * .35)); cr, sr = math.cos(roll), math.sin(roll)
    radii = [Rmax * (.36 + .64 * ((i + 1) / n) ** 1.05) for i in range(n)]
    def pos(i, th, R=None):
        R = radii[i] if R is None else R; x, y = R * math.cos(th), R * tilt * math.sin(th); return cx + x * cr - y * sr, cy + x * sr + y * cr, math.sin(th)
    SS = 2; orb = Image.new('RGB', (W * SS, H * SS), 0); d = ImageDraw.Draw(orb); g = Image.new('RGB', (W, H), 0); dg = ImageDraw.Draw(g)
    for i, R in enumerate(radii):
        pts = [pos(i, a / 240 * 2 * math.pi)[:2] for a in range(241)]; hot = i == hi; c = mix(mix(BLUE, (28, 40, 78), .58), mix(AMBER, BLUE, .75), focus * (not hot) * 0) if not hot else mix((46, 62, 120), AMBER, .35 + .65 * focus)
        d.line([(x * SS, y * SS) for x, y in pts], fill=c, width=int(2 * SS * (1 + hot * focus * 3.2)), joint='curve')
        if hot: dg.line(pts, fill=shade(AMBER, focus), width=10)
    img = ImageChops.screen(img, orb.resize((W, H), Image.LANCZOS)); img = glow(img, g, 28, .8)
    items = []
    for i, ne in enumerate(shells):
        sp = (1.15 / (i + 1)) * (.55 if focus > 0 else 1) * (1 - focus * .55)
        for e in range(ne):
            th = v * sp + e / ne * 2 * math.pi + i * 1.7; val = i == hi and e == 0; col = TEAL if i % 2 == 0 else BLUE
            if val:
                u = e_io(prog(v, 0, s['park'])); th = lerp(math.radians(150), math.radians(372), u)
            items.append((math.sin(th), i, th, val, col))
    t_n = v
    nr = Rmax * (.098 + .011 * s['nucleus'] ** .5); rng = np.random.default_rng(3); N = min(s['nucleus'], 30); parts = []
    for i in range(N):
        y_ = 1 - (i + .5) / N * 2; r_ = math.sqrt(max(0, 1 - y_ * y_)); a = i * 2.39996 + v * .32; rr = nr * (.72 + .28 * rng.random()); j = 1 + .02 * math.sin(v * 3 + i)
        parts.append((r_ * math.sin(a), cx + r_ * math.cos(a) * rr * j, cy + y_ * rr * j, NUC if i % 2 else STEEL))
    L = Image.new('RGB', (W, H), 0); ImageDraw.Draw(L).ellipse((cx - nr * 1.5, cy - nr * 1.5, cx + nr * 1.5, cy + nr * 1.5), fill=(120, 64, 30)); img = glow(img, L, 60, .75)
    def electron(it):
        _, i, th, val, col = it; x, y, zz = pos(i, th); b = _ball(9 if val else 12 - i, col if not val else (255, 244, 214)); nonlocal_img.paste(b, (int(x - b.width / 2), int(y - b.height / 2)), b)
    nonlocal_img = img
    for it in sorted(items, key=lambda q: q[0]):
        if it[0] < 0 and not it[3]: electron(it)
    pr = max(9, nr * .34)
    for z_, x, y, c in sorted(parts, key=lambda q: q[0]):
        b = _ball(pr, c); nonlocal_img.paste(b, (int(x - b.width / 2), int(y - b.height / 2)), b)
    vx = vy = None
    for it in sorted(items, key=lambda q: q[0]):
        if it[0] >= 0 and not it[3]: electron(it)
        if it[3]: vx, vy, _ = pos(it[1], it[2])
    L = Image.new('RGB', (W, H), 0); ld = ImageDraw.Draw(L); ld.ellipse((vx - 34, vy - 34, vx + 34, vy + 34), fill=AMBER); img = glow(nonlocal_img, L, 56, 1.05)
    d = ImageDraw.Draw(img); d.ellipse((vx - 15, vy - 15, vx + 15, vy + 15), fill=(255, 246, 222)); d.ellipse((vx - 37, vy - 37, vx + 37, vy + 37), outline=(255, 226, 170), width=4)
    text(img, s['name'], st.x0, st.y0 + 40, 96 if P else 82, CREAM, 'lm'); text(img, s['sub'], st.x0, st.y0 + (120 if P else 106), st.label + 4, (156, 172, 208), 'lm', 'mono')
    k = e_out(prog(v, s['focus'] - .2, s['focus'] + .4))
    if k > 0:
        if P:
            lx, ly = st.cx, cy + radii[hi] * tilt + 128; d = ImageDraw.Draw(img); d.line([(vx, vy + 34), (lerp(vx, min(vx, st.x1 - 80), k), lerp(vy + 34, ly - 92, k))], fill=(255, 226, 170), width=4)
            text(img, s['callout'], lx, ly - 38, 66, CREAM, a=k, maxw=st.sw); text(img, s['callout_sub'], lx, ly + 34, 38, (214, 212, 204), a=k, kind='mono', maxw=st.sw)
        else:
            lx, ly = W * .62, cy - 90; d = ImageDraw.Draw(img); d.line([(vx + 26, vy - 26), (lerp(vx + 26, lx - 20, k), lerp(vy - 26, ly + 6, k))], fill=(255, 226, 170), width=4)
            text(img, s['callout'], lx, ly - 22, 60, CREAM, 'lm', a=k, maxw=W - lx - 60); text(img, s['callout_sub'], lx, ly + 42, 34, (214, 212, 204), 'lm', 'mono', a=k, maxw=W - lx - 60)
    fy = st.y1 - 82 if P else st.y1 - 40; a = 1.0; text(img, s['footer'], st.cx if P else st.x0, fy, st.label - (0 if P else 0), (140, 156, 196), 'mm' if P else 'lm', 'monob', maxw=st.sw); nums = [str(x) for x in shells]
    f = font('head', 74); sep = '  ·  '; tot = sum(f.getlength(x) for x in nums) + f.getlength(sep) * (n - 1); x = st.cx - tot / 2 if P else st.x0 + 620
    if not P: x = st.x0 + 500
    yy = fy + 72 if P else fy
    for i, nm in enumerate(nums):
        c = mix((174, 186, 214), AMBER, focus) if i == hi else (174, 186, 214); text(img, nm, x, yy, 74, c, 'lm'); x += f.getlength(nm)
        if i < n - 1: text(img, sep, x, yy, 74, (98, 110, 148), 'lm'); x += f.getlength(sep)
    return img
