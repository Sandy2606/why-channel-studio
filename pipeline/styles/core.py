"""Shared toolkit for the Why? animation style library (PIL + numpy, no browser needed)."""
import functools, math, os, re
import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
FONTS = os.path.join(ROOT, 'brand', 'fonts')
INK = (10, 10, 10); CREAM = (244, 241, 234); AMBER = (255, 178, 36); GREY = (150, 146, 138)
SIZES = {'9x16': (1080, 1920), '16x9': (1920, 1080)}
TELUGU = re.compile('[ఀ-౿]')


def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def prog(v, t0, t1): return clamp((v - t0) / max(t1 - t0, 1e-6))
def e_out(p): return 1 - (1 - p) ** 3
def e_io(p): return 3 * p * p - 2 * p * p * p
def e_back(p, s=1.70158): p -= 1; return 1 + (s + 1) * p ** 3 + s * p ** 2
def lerp(a, b, k): return a + (b - a) * k
def mix(c0, c1, k): return tuple(int(round(lerp(a, b, k))) for a, b in zip(c0, c1))
def shade(c, k): return tuple(int(clamp(x * k, 0, 255)) for x in c)


class Stage:
    """Frame size plus the channel's safe areas (playbook QA rules)."""
    def __init__(self, aspect='9x16'):
        self.aspect = aspect; self.W, self.H = SIZES[aspect]; self.portrait = aspect == '9x16'
        self.safe = (70, 220, 900, 1500) if self.portrait else (90, 60, 1830, 900)
        self.x0, self.y0, self.x1, self.y1 = self.safe
        self.sw, self.sh = self.x1 - self.x0, self.y1 - self.y0
        self.cx, self.cy = (self.x0 + self.x1) // 2, (self.y0 + self.y1) // 2
        self.label = 36 if self.portrait else 34      # never go below the 34 px minimum


@functools.lru_cache(64)
def font(kind, px):
    name = {'head': 'ArchivoBlack-Regular.ttf', 'mono': 'SpaceMono-Regular.ttf', 'monob': 'SpaceMono-Bold.ttf', 'te': 'NotoSansTelugu.ttf'}[kind]
    f = ImageFont.truetype(os.path.join(FONTS, name), int(px))
    if kind == 'te':
        try: f.set_variation_by_axes([900, 100])
        except Exception: pass
    return f


def pick(txt, kind, px):
    return font('te', int(px * .86)) if TELUGU.search(txt) else font(kind, px)


def fit(txt, kind, px, maxw, minpx=34):
    while px > minpx and pick(txt, kind, px).getlength(txt) > maxw: px -= 2
    return pick(txt, kind, px), px


def wrap(txt, kind, px, maxw):
    f = pick(txt, kind, px); out = []; cur = ''
    for w in txt.split():
        t = (cur + ' ' + w).strip()
        if f.getlength(t) <= maxw or not cur: cur = t
        else: out.append(cur); cur = w
    if cur: out.append(cur)
    return out


def text(img, s, x, y, px, col=CREAM, anchor='mm', kind='head', a=1.0, maxw=None, shadow=None, track=0):
    if a <= 0 or not s: return img
    f, px = fit(s, kind, px, maxw) if maxw else (pick(s, kind, px), px)
    if a >= 1 and img.mode == 'RGB' and not track:
        d = ImageDraw.Draw(img)
        if shadow: d.text((x + 3, y + 4), s, font=f, fill=shadow, anchor=anchor)
        d.text((x, y), s, font=f, fill=col, anchor=anchor); return img
    W, H = img.size; layer = Image.new('L', (W, H), 0); d = ImageDraw.Draw(layer)
    if track:
        tw = sum(f.getlength(c) + track for c in s) - track
        cx = x - tw / 2 if anchor[0] == 'm' else (x - tw if anchor[0] == 'r' else x)
        for c in s: d.text((cx, y), c, font=f, fill=255, anchor='l' + anchor[1]); cx += f.getlength(c) + track
    else: d.text((x, y), s, font=f, fill=255, anchor=anchor)
    img.paste(col, (0, 0), layer.point(lambda p: int(p * a))); return img


def pill(img, s, cx, cy, px, bg=AMBER, fg=INK, a=1.0, scale=1.0, kind='head', maxw=None, pad=(26, 14), outline=None):
    if a <= 0 or scale <= 0.01: return
    f, px = fit(s, kind, px, maxw) if maxw else (pick(s, kind, px), px)
    tw = f.getlength(s); bb = f.getbbox('Hg'); th = bb[3] - bb[1]
    w, h = int(tw + pad[0] * 2), int(th + pad[1] * 2)
    spr = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(spr)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=h // 3, fill=tuple(bg) + (255,), outline=(tuple(outline) + (255,)) if outline else None, width=3)
    d.text((w / 2, h / 2), s, font=f, fill=tuple(fg) + (255,), anchor='mm')
    if scale != 1: spr = spr.resize((max(1, int(w * scale)), max(1, int(h * scale))), Image.BILINEAR)
    if a < 1: spr.putalpha(spr.getchannel('A').point(lambda p: int(p * a)))
    img.paste(spr, (int(cx - spr.width / 2), int(cy - spr.height / 2)), spr)


def glow(img, layer, radius=24, strength=1.0):
    """Add a soft bloom of an RGB layer on top of img (fast: blurs at quarter size)."""
    w, h = img.size; sm = layer.resize((w // 4, h // 4), Image.BILINEAR).filter(ImageFilter.GaussianBlur(radius / 4)).resize((w, h), Image.BILINEAR)
    if strength != 1: sm = sm.point(lambda p: min(255, int(p * strength)))
    return ImageChops.screen(img, sm)


def vgradient(w, h, stops):
    ys = np.linspace(0, 1, h); ps = [s[0] for s in stops]
    arr = np.stack([np.interp(ys, ps, [s[1][c] for s in stops]) for c in range(3)], 1)
    return Image.fromarray(np.repeat(arr[:, None, :], w, 1).astype('uint8'), 'RGB')


@functools.lru_cache(8)
def radial_bg(W, H, inner, outer, cx=.5, cy=.42, reach=.8):
    yy, xx = np.mgrid[0:H, 0:W]; d = np.hypot((xx - cx * W) / max(W, H), (yy - cy * H) / max(W, H)) / reach
    k = np.clip(d, 0, 1)[..., None] ** 1.4
    arr = np.array(inner) * (1 - k) + np.array(outer) * k
    arr += np.random.default_rng(7).normal(0, 1.2, arr.shape)      # dither stops banding on YouTube
    return Image.fromarray(np.clip(arr, 0, 255).astype('uint8'), 'RGB')


@functools.lru_cache(4)
def grain(W, H, amount):
    rng = np.random.default_rng(11); n = rng.normal(0, amount, (H // 2, W // 2))
    return np.asarray(Image.fromarray(n.astype('float32'), 'F').resize((W, H), Image.BILINEAR))


class Cam:
    """Y-up perspective camera. fov is vertical, in degrees."""
    def __init__(self, eye, target, fov, W, H):
        self.eye = np.array(eye, float); self.W, self.H = W, H
        f = np.array(target, float) - self.eye; f /= np.linalg.norm(f)
        r = np.cross((0, 1, 0), f); r /= np.linalg.norm(r); u = np.cross(f, r)   # +x is screen-right when looking along +z
        self.R = np.stack([r, u, f]); self.f = .5 * H / math.tan(math.radians(fov) / 2)

    def project(self, P):
        P = np.atleast_2d(np.array(P, float)); q = (P - self.eye) @ self.R.T
        z = np.maximum(q[:, 2], 1e-3)
        return np.stack([self.W / 2 + q[:, 0] * self.f / z, self.H / 2 - q[:, 1] * self.f / z], 1), z

    def pt(self, p):
        xy, _ = self.project(p); return float(xy[0, 0]), float(xy[0, 1])


LIGHT = np.array([-.45, .8, -.4]); LIGHT = LIGHT / np.linalg.norm(LIGHT)
_FACES = [((0, 1, 3, 2), (-1, 0, 0)), ((4, 6, 7, 5), (1, 0, 0)), ((0, 4, 5, 1), (0, -1, 0)),
          ((2, 3, 7, 6), (0, 1, 0)), ((0, 2, 6, 4), (0, 0, -1)), ((1, 5, 7, 3), (0, 0, 1))]


def box_faces(cam, c, size, col, R=None, pivot=None, top=None, edge=True):
    """Visible faces of a box as (depth, polygon, fill, outline) ready for paint()."""
    c = np.array(c, float); h = np.array(size, float) / 2
    V = np.array([[sx, sy, sz] for sx in (-1, 1) for sy in (-1, 1) for sz in (-1, 1)], float) * h + c
    pv = np.array(pivot, float) if pivot is not None else c
    if R is not None: V = (V - pv) @ R.T + pv
    out = []
    for idx, n in _FACES:
        n = np.array(n, float)
        if R is not None: n = R @ n
        mid = V[list(idx)].mean(0)
        if n @ (cam.eye - mid) <= 0: continue
        k = .52 + .58 * max(0, float(n @ LIGHT))
        fill = shade(top if (top is not None and n[1] > .9) else col, k)
        xy, _ = cam.project(V[list(idx)])
        out.append((float(np.linalg.norm(mid - cam.eye)), [tuple(p) for p in xy], fill, shade(fill, 1.22) if edge else None))
    return out


def paint(draw, faces, width=2):
    for _, poly, fill, line in sorted(faces, key=lambda f: -f[0]):
        draw.polygon(poly, fill=fill)
        if line: draw.line(poly + [poly[0]], fill=line, width=width, joint='curve')


def rot_axis(axis, a):
    c, s = math.cos(a), math.sin(a)
    return {'x': np.array([[1, 0, 0], [0, c, -s], [0, s, c]]), 'y': np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]]), 'z': np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])}[axis]


def stepped(v, fps=12): return math.floor(v * fps) / fps


def merge(default, spec):
    out = dict(default); out.update(spec or {}); return out
