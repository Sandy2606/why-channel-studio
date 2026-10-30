"""Diwali long: shared drawing helpers (16:9, 1920x1080)."""
import json, math, os, re
import numpy as np, cairo
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1920, 1080, 30
ROOT = '/home/claude/dl/'
ASSET = '/home/claude/why-channel-studio/videos/2026-11-01_long_diwali_explained/assets/'
CREAM = (0.957, 0.945, 0.918); AMBER = (1.0, 0.698, 0.141); AMBER2 = (1.0, 0.48, 0.10); INK = (0.04, 0.04, 0.04)
TEAL = (0.15, 0.55, 0.55); GREEN = (0.30, 0.78, 0.45); SKY = (0.45, 0.70, 0.98)
LANG = os.environ.get('LANGV', 'en')


def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def prog(t, a, b): return clamp((t - a) / max(1e-6, b - a))
def e_out(x): return 1 - (1 - x) ** 3
def e_io(x): return 4 * x ** 3 if x < .5 else 1 - (-2 * x + 2) ** 3 / 2
def e_back(x, s=1.7): x -= 1; return 1 + (s + 1) * x ** 3 + s * x ** 2
def lerp(a, b, u): return a + (b - a) * u


def surf_from_pil(im):
    im = im.convert('RGBA'); a = np.array(im); bgra = a[:, :, [2, 1, 0, 3]].copy()
    al = bgra[:, :, 3:4].astype(np.uint16)
    bgra[:, :, :3] = (bgra[:, :, :3].astype(np.uint16) * al // 255).astype(np.uint8)
    s = cairo.ImageSurface.create_for_data(memoryview(bgra), cairo.FORMAT_ARGB32, im.width, im.height)
    return (s, bgra)


def rrect(c, x, y, w, h, r):
    r = max(0.1, min(r, h / 2, w / 2))
    c.new_sub_path(); c.arc(x + w - r, y + r, r, -math.pi / 2, 0); c.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    c.arc(x + r, y + h - r, r, math.pi / 2, math.pi); c.arc(x + r, y + r, r, math.pi, 3 * math.pi / 2); c.close_path()


def agrad(x0, y0, x1, y1):
    g = cairo.LinearGradient(x0, y0, x1, y1); g.add_color_stop_rgb(0, *AMBER); g.add_color_stop_rgb(1, *AMBER2); return g


def glowdot(c, x, y, r=14, a=1.0):
    g = cairo.RadialGradient(x, y, 0, x, y, r * 3.2); g.add_color_stop_rgba(0, *AMBER, 0.55 * a); g.add_color_stop_rgba(1, *AMBER, 0)
    c.set_source(g); c.arc(x, y, r * 3.2, 0, 2 * math.pi); c.fill()
    c.set_source_rgba(1, 0.86, 0.55, a); c.arc(x, y, r, 0, 2 * math.pi); c.fill()


def glass(c, x, y, w, h, r=24, a=1.0, edge=True):
    c.set_source_rgba(0, 0, 0, 0.35 * a); rrect(c, x + 4, y + 10, w, h, r); c.fill()
    c.set_source_rgba(0.075, 0.07, 0.07, 0.92 * a); rrect(c, x, y, w, h, r); c.fill()
    c.set_source_rgba(1, 1, 1, 0.08 * a); c.set_line_width(2); rrect(c, x, y, w, h, r); c.stroke()
    if edge:
        c.save(); rrect(c, x, y, w, h, r); c.clip(); c.rectangle(x, y, 8, h); c.clip(); c.set_source(agrad(x, y, x, y + h)); c.paint_with_alpha(a); c.restore()


# ---------------- text ----------------
TE_RE = re.compile('[ఀ-౿]')
_TC = {}
TEFONT = '/home/claude/fonts/NotoSansTelugu.ttf'


def _tefont(px, weight='Black'):
    f = ImageFont.truetype(TEFONT, int(px), layout_engine=ImageFont.Layout.RAQM)
    try: f.set_variation_by_name(weight)
    except Exception: pass
    return f


def font(c, kind, px):
    c.select_font_face('Archivo Black' if kind == 'head' else 'Space Mono', cairo.FONT_SLANT_NORMAL,
                       cairo.FONT_WEIGHT_BOLD if kind == 'monob' else cairo.FONT_WEIGHT_NORMAL)
    c.set_font_size(px)


def text_w(c, s, px, kind='head'):
    if TE_RE.search(s):
        f = _tefont(px * 0.92, 'Black' if kind == 'head' else 'Bold'); return ImageDraw.Draw(Image.new('L', (4, 4))).textlength(s, font=f)
    font(c, kind, px); return c.text_extents(s).x_advance


def txt(c, s, x, y, px, col=CREAM, a=1.0, anchor='c', kind='head', grad=False, stroke=0.0, maxw=None):
    """draw text centred vertically on y. Telugu goes through PIL+RAQM."""
    if a <= 0.01 or not s: return 0
    m = c.get_matrix()
    if abs(m.xx * m.yy - m.xy * m.yx) < 1e-4: return 0
    if maxw:
        w0 = text_w(c, s, px, kind)
        if w0 > maxw: px *= maxw / w0
    if TE_RE.search(s):
        s = s.replace(' → ', ' - ').replace('→', '-')
        key = (s, int(px), col, kind, grad, stroke)
        if key not in _TC:
            f = _tefont(px * 0.92, 'Black' if kind == 'head' else 'Bold')
            d0 = ImageDraw.Draw(Image.new('L', (4, 4))); bb = d0.textbbox((0, 0), s, font=f, anchor='lm')
            pad = int(px * 0.3 + stroke); w, h = bb[2] - bb[0] + pad * 2, int(px * 1.8) + pad * 2
            im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
            fill = (255, 178, 36, 255) if grad else tuple(int(v * 255) for v in col) + (255,)
            d.text((pad - bb[0], h / 2), s, font=f, fill=fill, anchor='lm', stroke_width=int(stroke), stroke_fill=(0, 0, 0, 230))
            _TC[key] = (surf_from_pil(im), pad - bb[0], h)
        (sf, _), ox, h = _TC[key]; w = sf.get_width()
        xx = x - (w - 2 * ox) / 2 - ox if anchor == 'c' else (x - w + ox if anchor == 'r' else x - ox)
        c.set_source_surface(sf, xx, y - h / 2); c.paint_with_alpha(a); return w - 2 * ox
    font(c, kind, px); e = c.text_extents(s)
    xx = x - e.x_advance / 2 if anchor == 'c' else (x - e.x_advance if anchor == 'r' else x)
    yy = y + (px * 0.36 if kind == 'head' else px * 0.33)
    c.move_to(xx, yy); c.text_path(s)
    if stroke:
        c.set_line_join(cairo.LINE_JOIN_ROUND); c.set_source_rgba(0, 0, 0, 0.85 * a); c.set_line_width(stroke); c.stroke_preserve()
    if grad: c.set_source(agrad(xx, yy - px, xx + e.x_advance, yy))
    else: c.set_source_rgba(*col, a)
    if grad and a < 1:
        c.save(); c.clip(); c.paint_with_alpha(a); c.restore(); c.new_path()
    else: c.fill()
    return e.x_advance


def L(en, te): return te if LANG == 'te' else en


def pill(c, s, cx, cy, px=30, fill=AMBER, col=INK, a=1.0, sc=1.0, kind='head', outline=False):
    if sc <= 0.01 or a <= 0.01: return
    w = text_w(c, s, px, kind) + px * 1.4; h = px * 1.75
    c.save(); c.translate(cx, cy); c.scale(sc, sc)
    if outline:
        c.set_source_rgba(0, 0, 0, 0.6 * a); rrect(c, -w / 2, -h / 2, w, h, h / 2); c.fill()
        c.set_source_rgba(*AMBER, a); c.set_line_width(3); rrect(c, -w / 2, -h / 2, w, h, h / 2); c.stroke()
        txt(c, s, 0, 0, px, CREAM, a, kind=kind)
    else:
        c.set_source_rgba(*fill, a); rrect(c, -w / 2, -h / 2, w, h, h / 2); c.fill(); txt(c, s, 0, 0, px, col, a, kind=kind)
    c.restore()


def stamp(c, s, cx, cy, t, t0, px=110, rot=-8, col=AMBER):
    if t < t0: return
    u = prog(t, t0, t0 + 0.22); sc = 1.9 - 0.9 * e_out(u); a = clamp(u * 3)
    c.save(); c.translate(cx, cy); c.rotate(math.radians(rot)); c.scale(sc, sc)
    w = text_w(c, s, px) + px * 0.8; h = px * 1.45
    c.set_source_rgba(0, 0, 0, 0.45 * a); rrect(c, -w / 2 - 6, -h / 2 - 6, w + 12, h + 12, 18); c.fill()
    c.set_source_rgba(*col, a); c.set_line_width(9); rrect(c, -w / 2, -h / 2, w, h, 14); c.stroke()
    txt(c, s, 0, 0, px, col, a)
    c.restore()


def marker_circle(c, cx, cy, rx, ry, t, t0, dur=0.45):
    u = e_io(prog(t, t0, t0 + dur))
    if u <= 0: return
    c.save(); c.set_source_rgba(*AMBER, 0.95); c.set_line_width(8); c.set_line_cap(cairo.LINE_CAP_ROUND)
    a0 = -2.2; c.save(); c.translate(cx, cy); c.scale(rx, ry); c.arc(0, 0, 1, a0, a0 + u * 2 * math.pi * 1.06); c.restore(); c.stroke(); c.restore()


def marker_line(c, x0, y0, x1, y1, t, t0, dur=0.35, w=8, col=AMBER):
    u = e_io(prog(t, t0, t0 + dur))
    if u <= 0: return
    c.set_source_rgba(*col, 0.95); c.set_line_width(w); c.set_line_cap(cairo.LINE_CAP_ROUND)
    c.move_to(x0, y0); c.line_to(lerp(x0, x1, u), lerp(y0, y1, u)); c.stroke()


def arrow_head(c, x, y, ang, s=26, col=AMBER, a=1.0):
    c.save(); c.translate(x, y); c.rotate(ang); c.move_to(0, 0); c.line_to(-s, -s * 0.6); c.line_to(-s, s * 0.6); c.close_path()
    c.set_source_rgba(*col, a); c.fill(); c.restore()


def big_num(c, s, x, y, px, t, t0, anchor='c'):
    if t < t0: return
    u = e_back(prog(t, t0, t0 + 0.32)); c.save(); c.translate(x, y); c.scale(max(0.01, u), max(0.01, u))
    txt(c, s, 0, 0, px, grad=True, stroke=px * 0.09, anchor=anchor); c.restore()


def grain(c, t):
    pass


# ---------------- images ----------------
_IM = {}
def img(path, maxw=None):
    k = (path, maxw)
    if k not in _IM:
        im = Image.open(path).convert('RGB')
        if maxw and im.width > maxw: im = im.resize((maxw, int(im.height * maxw / im.width)), Image.LANCZOS)
        _IM[k] = surf_from_pil(im)
    return _IM[k][0]


def blur_fill(path):
    k = ('fill', path)
    if k not in _IM:
        im = Image.open(path).convert('RGB'); s = max(W / im.width, H / im.height) * 1.1
        im = im.resize((int(im.width * s), int(im.height * s))).filter(ImageFilter.GaussianBlur(40))
        im = Image.eval(im, lambda v: int(v * 0.45))
        _IM[k] = surf_from_pil(im)
    return _IM[k][0]


def photo_panel(c, path, cx, cy, w, t, t0, rot=0, caption=None, credit=None, a=1.0, zoom=(1.0, 1.0), dur=6.0):
    if t < t0: return
    sf = img(path, 2000); u = e_out(prog(t, t0, t0 + 0.45)); sc = w / sf.get_width(); h = sf.get_height() * sc
    zz = lerp(zoom[0], zoom[1], prog(t, t0, t0 + dur))
    c.save(); c.translate(cx, cy + (1 - u) * 120); c.rotate(math.radians(rot * u))
    c.set_source_rgba(0, 0, 0, 0.5 * u * a); rrect(c, -w / 2 + 8, -h / 2 + 16, w, h, 14); c.fill()
    c.save(); rrect(c, -w / 2, -h / 2, w, h, 14); c.clip()
    c.translate(0, 0); c.scale(sc * zz, sc * zz); c.set_source_surface(sf, -sf.get_width() / 2, -sf.get_height() / 2); c.paint_with_alpha(u * a); c.restore()
    c.set_source_rgba(1, 1, 1, 0.15 * u * a); c.set_line_width(2); rrect(c, -w / 2, -h / 2, w, h, 14); c.stroke()
    if caption: pill(c, caption, 0, -h / 2 - 2, 22, a=u * a, outline=True, kind='monob')
    if credit: txt(c, credit, w / 2 - 6, h / 2 + 22, 15, CREAM, 0.7 * u * a, anchor='r', kind='mono')
    c.restore()


# ---------------- clippings ----------------
CJ = json.load(open(ROOT + 'clips.json')); _CL = {}


def torn(im, seed=1, amp=7):
    pad = 26
    base = Image.new('RGB', (im.width + pad * 2, im.height + pad * 2), (250, 249, 245)); base.paste(im, (pad, pad))
    m = Image.new('L', base.size, 255); d = ImageDraw.Draw(m); rng = np.random.default_rng(seed); wdt = base.width
    for edge in ('top', 'bottom'):
        pts = [(x, rng.uniform(0, amp) if edge == 'top' else base.height - rng.uniform(0, amp)) for x in range(0, wdt + 8, 8)]
        poly = ([(0, 0)] + pts + [(wdt, 0)]) if edge == 'top' else ([(0, base.height)] + pts + [(wdt, base.height)])
        d.polygon(poly, fill=0)
    base.putalpha(m); return base, pad


def clip(name):
    if name not in _CL:
        im = Image.open(ROOT + f'clip_{name}.png').convert('RGB')
        paper, pad = torn(im, seed=len(name))
        _CL[name] = (surf_from_pil(paper), [(a + pad, b + pad, c_ + pad, d + pad) for a, b, c_, d in CJ[name]['hl']])
    return _CL[name]


def draw_clip(c, name, cx, cy, wpx, t, t0, rot=-1.5, hl_t0=None, hl_dur=0.9, a=1.0, src=None):
    if t < t0: return
    (sf, _), rects = clip(name)
    u = e_out(prog(t, t0, t0 + 0.4)); sc = wpx / sf.get_width(); w, h = sf.get_width(), sf.get_height()
    c.save(); c.translate(cx, cy + (1 - u) * 200); c.rotate(math.radians(rot + (1 - u) * 5)); c.scale(sc, sc)
    c.set_source_rgba(0, 0, 0, 0.45 * u * a); c.rectangle(-w / 2 + 10, -h / 2 + 18, w, h); c.fill()
    c.set_source_surface(sf, -w / 2, -h / 2); c.paint_with_alpha(u * a)
    tip = None
    if hl_t0 is not None and t >= hl_t0:
        tot = sum(r[2] - r[0] for r in rects); done = prog(t, hl_t0, hl_t0 + hl_dur) * tot
        for (x0, y0, x1, y1) in rects:
            wl = x1 - x0; f = clamp(done / wl); done -= wl
            if f <= 0: break
            xa, xb = -w / 2 + x0 - 3, -w / 2 + x0 + wl * f + 3
            c.set_source_rgba(1.0, 0.70, 0.14, 0.42 * a); c.rectangle(xa, -h / 2 + y0 - 2, xb - xa, y1 - y0 + 4); c.fill()
            tip = c.user_to_device(xb, -h / 2 + (y0 + y1) / 2)
    s2 = 1 / sc
    for tx in (-w / 2 + 70 * s2, w / 2 - 70 * s2):
        c.save(); c.translate(tx, -h / 2 + 4); c.rotate(math.radians(-30 if tx < 0 else 30))
        c.set_source_rgba(0.95, 0.89, 0.70, 0.75 * u * a); c.rectangle(-45 * s2, -12 * s2, 90 * s2, 24 * s2); c.fill(); c.restore()
    c.restore()
    if src:
        sw = text_w(c, src, 18, 'monob') + 40
        bx = cx - wpx / 2 + 10; by = cy + h * sc / 2 + 18 + (1 - u) * 200
        glass(c, bx, by, sw, 38, 19, u * a, edge=False); glowdot(c, bx + 18, by + 19, 5, u * a)
        txt(c, src, bx + 32, by + 19, 18, CREAM, u * a, anchor='l', kind='monob')
    if tip and prog(t, hl_t0, hl_t0 + hl_dur) < 1: glowdot(c, tip[0], tip[1], 9, a)


def board_bg(c, warm=0.08):
    c.set_source_rgb(0.05, 0.047, 0.05); c.paint()
    g = cairo.RadialGradient(W / 2, H * 0.45, 0, W / 2, H * 0.45, W * 0.7); g.add_color_stop_rgba(0, *AMBER, warm); g.add_color_stop_rgba(1, 0, 0, 0, 0)
    c.set_source(g); c.paint()
    c.set_source_rgba(1, 1, 1, 0.03); c.set_line_width(1)
    for x in range(0, W, 64): c.move_to(x, 0); c.line_to(x, H)
    for y in range(0, H, 64): c.move_to(0, y); c.line_to(W, y)
    c.stroke()


def thread(c, x0, y0, x1, y1, t, t0, dur=0.6, sag=60, a=1.0):
    u = e_io(prog(t, t0, t0 + dur))
    if u <= 0: return
    xm, ym = (x0 + x1) / 2, max(y0, y1) + sag
    pts = []
    for i in range(31):
        s = i / 30 * u
        pts.append(((1 - s) ** 2 * x0 + 2 * (1 - s) * s * xm + s * s * x1, (1 - s) ** 2 * y0 + 2 * (1 - s) * s * ym + s * s * y1))
    c.set_line_width(3); c.set_source_rgba(*AMBER, 0.8 * a); c.move_to(*pts[0]); [c.line_to(*p) for p in pts[1:]]; c.stroke()
    glowdot(c, pts[-1][0], pts[-1][1], 6, a)
