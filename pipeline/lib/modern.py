# Modern explainer toolkit (WHY? brand: #0A0A0A, cream, amber; Archivo Black + Space Mono)
import math, json, functools
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops
from epic import font, clamp, prog, e_out, e_io, e_back, is_te, ASSETS, base_img, kb_frame

BG = (10, 10, 10); CREAM = (244, 241, 234); AMBER = (255, 178, 36); GREY = (140, 136, 128)
RED = (240, 72, 56); BLUE = (80, 170, 255); TEALC = (70, 200, 190); DARK2 = (22, 22, 24)

def F(kind, px):
    return font(kind, px)

def head_font(text, px):
    return font('tesans', int(px * 0.92)) if is_te(text) else font('archivo', px)
def mono_font(text, px):
    return font('tesansb', int(px * 1.05)) if is_te(text) else font('mono', px)

# ---------- background ----------
@functools.lru_cache(4)
def bg_base(W, H):
    im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im)
    step = 48
    for y in range(step // 2, H, step):
        for x in range(step // 2, W, step):
            d.point((x, y), fill=(34, 34, 34))
    # soft amber vignette glow top-left / bottom-right
    g = Image.new('L', (W, H), 0); dg = ImageDraw.Draw(g)
    dg.ellipse((-W * .3, -H * .6, W * .5, H * .5), fill=26); dg.ellipse((W * .55, H * .55, W * 1.3, H * 1.5), fill=18)
    g = g.filter(ImageFilter.GaussianBlur(160))
    am = Image.new('RGB', (W, H), AMBER)
    im = Image.composite(am, im, g)
    return im.convert('RGBA')

def bg(W, H): return bg_base(W, H).copy()

def alpha_paste(dst, spr, x, y, a=1.0):
    if a <= 0.004: return
    if a < 0.999:
        spr = spr.copy(); spr.putalpha(spr.getchannel('A').point(lambda v: int(v * a)))
    tmp = Image.new('RGBA', dst.size, (0, 0, 0, 0)); tmp.paste(spr, (int(x), int(y))); dst.alpha_composite(tmp)

def paste_c(dst, spr, cx, cy, a=1.0, s=1.0):
    if s != 1.0: spr = spr.resize((max(1, int(spr.width * s)), max(1, int(spr.height * s))), Image.BILINEAR)
    alpha_paste(dst, spr, cx - spr.width / 2, cy - spr.height / 2, a)

# ---------- kinetic headline ----------
@functools.lru_cache(1024)
def word_spr(word, px, color, hl):
    f = head_font(word, px)
    b = f.getbbox(word); pad = int(px * 0.18)
    asc, desc = f.getmetrics(); asc = int(px * 1.0); desc = int(px * 0.3) if not is_te(word) else int(px * 0.45)
    if is_te(word): asc = int(px * 1.1)
    w, h = b[2] - b[0] + 2 * pad, asc + desc + 2 * pad
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.text((pad - b[0], pad + asc), word, font=f, fill=(10, 10, 10) if hl else color, anchor='ls')
    return im

def layout_words(words, px, maxw):
    sp = px * 0.28; lines = [[]]; lw = 0
    for w in words:
        ww = word_spr(w, px, CREAM, False).width - px * 0.36
        if lines[-1] and lw + ww > maxw: lines.append([]); lw = 0
        lines[-1].append((w, ww)); lw += ww + sp
    return lines, sp

def headline(img, text, v, t0, cx, cy, px=96, maxw=1500, hl=(), color=CREAM, stagger=0.06, align='c', a_out=1.0, hl_col=AMBER):
    """word-by-word pop with marker highlight on words whose index in hl"""
    if v < t0: return
    words = text.split(' ')
    lines, sp = layout_words(words, px, maxw)
    lh = px * 1.28; y0 = cy - (len(lines) - 1) * lh / 2; idx = 0
    for li, ln in enumerate(lines):
        tw = sum(w for _, w in ln) + sp * (len(ln) - 1)
        x = cx - tw / 2 if align == 'c' else cx
        for (w, ww) in ln:
            ti = t0 + idx * stagger; k = e_out(prog(v, ti, ti + 0.35))
            if k > 0:
                is_h = idx in hl
                yy = y0 + li * lh + 26 * (1 - k)
                if is_h:
                    hk = e_io(prog(v, ti + 0.15, ti + 0.5))
                    if hk > 0:
                        d = ImageDraw.Draw(img); pad = px * 0.08
                        d.rounded_rectangle((x - pad, yy - px * 0.55, x - pad + (ww + 2 * pad) * hk, yy + px * 0.62), radius=int(px * 0.12), fill=hl_col + (int(255 * a_out),))
                spr = word_spr(w, px, color, is_h and prog(v, ti + 0.15, ti + 0.5) > 0.5)
                paste_c(img, spr, x + ww / 2, yy, k * a_out)
            x += ww + sp; idx += 1

def mono(img, text, x, y, px=30, color=AMBER, a=1.0, anchor='c', track=3):
    if a <= 0: return
    f = mono_font(text, px)
    w = sum(f.getlength(c) + track for c in text) - track if not is_te(text) else f.getlength(text)
    h = px * 1.4
    im = Image.new('RGBA', (int(w + 20), int(h + 20)), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if is_te(text): d.text((10, 10), text, font=f, fill=color)
    else:
        xx = 10
        for c in text: d.text((xx, 10), c, font=f, fill=color); xx += f.getlength(c) + track
    if anchor == 'c': alpha_paste(img, im, x - im.width / 2, y - im.height / 2, a)
    elif anchor == 'l': alpha_paste(img, im, x - 10, y - im.height / 2, a)
    else: alpha_paste(img, im, x - im.width + 10, y - im.height / 2, a)

def text_plain(img, text, x, y, px, color=CREAM, a=1.0, anchor='c'):
    f = head_font(text, px); b = f.getbbox(text)
    im = Image.new('RGBA', (b[2] - b[0] + 20, b[3] - b[1] + 20), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((10 - b[0], 10 - b[1]), text, font=f, fill=color)
    if anchor == 'c': alpha_paste(img, im, x - im.width / 2, y - im.height / 2, a)
    elif anchor == 'l': alpha_paste(img, im, x - 10, y - im.height / 2, a)
    else: alpha_paste(img, im, x - im.width + 10, y - im.height / 2, a)
    return im.width - 20

def pill(img, text, cx, cy, px=34, fill=AMBER, color=(10, 10, 10), a=1.0, s=1.0):
    f = head_font(text, px); b = f.getbbox(text); w = b[2] - b[0] + px * 1.2; h = px * 1.7
    im = Image.new('RGBA', (int(w), int(h)), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=int(h / 2), fill=fill)
    d.text(((w - (b[2] - b[0])) / 2 - b[0], (h - (b[3] - b[1])) / 2 - b[1]), text, font=f, fill=color)
    paste_c(img, im, cx, cy, a, s)
    return w

# ---------- photo card ----------
@functools.lru_cache(16)
def round_mask(w, h, r):
    m = Image.new('L', (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), radius=r, fill=255); return m

def photo_card(img, name, cx, cy, w, h, v, t0, t1, z=(1.0, 1.1), f=(0.5, 0.5), caption=None, enter='up', a_out=1.0):
    if v < t0: return
    k = e_out(prog(v, t0, t0 + 0.55))
    u = prog(v, t0, t1)
    ph = kb_frame(name, w, h, u, z[0], z[1], f[0], f[1]).convert('RGBA')
    ph.putalpha(round_mask(w, h, 22))
    # shadow
    sh = Image.new('RGBA', (w + 120, h + 120), (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle((60, 70, w + 60, h + 70), radius=26, fill=(0, 0, 0, 170))
    sh = sh.filter(ImageFilter.GaussianBlur(26))
    dy = 60 * (1 - k) if enter == 'up' else 0; sc = 0.94 + 0.06 * k
    a = k * a_out
    paste_c(img, sh, cx, cy + dy + 10, a, sc)
    paste_c(img, ph, cx, cy + dy, a, sc)
    d = Image.new('RGBA', (w, h), (0, 0, 0, 0)); ImageDraw.Draw(d).rounded_rectangle((0, 0, w - 1, h - 1), radius=22, outline=(244, 241, 234, 90), width=2)
    paste_c(img, d, cx, cy + dy, a, sc)
    if caption:
        mono(img, caption, cx - w * sc / 2 + 6, cy + dy + h * sc / 2 + 30, 22, GREY, a, anchor='l', track=2)

# ---------- counters / gauges / bars ----------
def counter(img, v, t0, dur, val, fmt, cx, cy, px=220, color=CREAM, prefix='', suffix=''):
    if v < t0: return
    k = e_out(prog(v, t0, t0 + dur))
    s = prefix + fmt.format(val * k) + suffix
    a = prog(v, t0, t0 + 0.2)
    text_plain(img, s, cx, cy, px, color, a)

def ring(img, v, t0, frac, cx, cy, r=170, w=28, color=AMBER, label=None, px=96):
    if v < t0: return
    k = e_out(prog(v, t0, t0 + 1.4)) * frac
    d = ImageDraw.Draw(img)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=(40, 40, 42, 255), width=w)
    if k > 0.002: d.arc((cx - r, cy - r, cx + r, cy + r), -90, -90 + 360 * k, fill=color + (255,), width=w)
    text_plain(img, f"{int(round(100 * k))}%", cx, cy, px, CREAM, prog(v, t0, t0 + .3))

def hbars(img, v, items, x0, y0, wmax, bh=74, gap=40, maxval=30, px=40):
    """items: (label, value, t_reveal, color)"""
    for i, (lab, val, tr, col) in enumerate(items):
        if v < tr: continue
        k = e_out(prog(v, tr, tr + 0.9)); y = y0 + i * (bh + gap)
        a = prog(v, tr, tr + .25)
        text_plain(img, lab, x0 - 30, y + bh / 2, px, CREAM, a, anchor='r')
        d = ImageDraw.Draw(img); w = wmax * abs(val) / maxval * k
        d.rounded_rectangle((x0, y, x0 + max(8, w), y + bh), radius=12, fill=col + (int(255 * a),))
        text_plain(img, f"{val * k:+.0f}%".replace('+', '+').replace('-', '−'), x0 + w + 28, y + bh / 2, px + 6, col, a, anchor='l')

def vbars(img, v, items, x0, base_y, gap, bw=110, hmax=420, px=36):
    for i, (lab, h, tr, col) in enumerate(items):
        if v < tr: continue
        k = e_out(prog(v, tr, tr + 0.8)); x = x0 + i * gap; hh = hmax * h * k
        d = ImageDraw.Draw(img)
        d.rounded_rectangle((x - bw / 2, base_y - hh, x + bw / 2, base_y), radius=12, fill=col + (255,))
        mono(img, lab, x, base_y + 34, 26, CREAM, prog(v, tr, tr + .3))
    d = ImageDraw.Draw(img); d.line((x0 - 100, base_y, x0 + gap * (len(items) - 1) + 100, base_y), fill=(80, 80, 80, 255), width=3)

def progress_bar(img, sections, cur, W, a=1.0):
    n = len(sections); m = 60; gap = 10; w = (W - 2 * m - gap * (n - 1)) / n; y = 34
    d = ImageDraw.Draw(img)
    for i, s in enumerate(sections):
        x = m + i * (w + gap)
        col = AMBER if i == cur else ((120, 110, 90) if i < cur else (50, 50, 50))
        d.rounded_rectangle((x, y, x + w, y + 6), radius=3, fill=col + (int(255 * a),))
        mono(img, s, x, y + 30, 18, AMBER if i == cur else GREY, a * (1.0 if i == cur else 0.7), anchor='l', track=2)

# ---------- icons ----------
def icon(img, kind, cx, cy, s=1.0, a=1.0, t=0.0, col=CREAM):
    S = int(240 * s); im = Image.new('RGBA', (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im); c = S / 2
    lw = max(3, int(12 * s)); cc = col + (255,)
    def cloud(cy0, colr):
        d.ellipse((c - S * .32, cy0 - S * .02, c - S * .02, cy0 + S * .2), fill=colr)
        d.ellipse((c - S * .18, cy0 - S * .16, c + S * .14, cy0 + S * .16), fill=colr)
        d.ellipse((c + S * .0, cy0 - S * .06, c + S * .3, cy0 + S * .2), fill=colr)
        d.rectangle((c - S * .2, cy0 + S * .06, c + S * .18, cy0 + S * .2), fill=colr)
    if kind == 'storm':
        cloud(S * .32, (190, 196, 205, 255))
        d.polygon([(c, S * .5), (c - S * .1, S * .7), (c + .0, S * .7), (c - S * .06, S * .9), (c + S * .12, S * .62), (c + .02 * S, S * .62), (c + S * .08, S * .5)], fill=AMBER + (255,))
    elif kind == 'cyclone':
        pts = []
        for i in range(260):
            th = i / 260 * 4.2 * math.pi + t * 3; r = S * .42 * (i / 260)
            pts.append((c + r * math.cos(th), c + r * math.sin(th)))
        d.line(pts, fill=(190, 196, 205, 255), width=lw)
    elif kind == 'sun':
        d.ellipse((c - S * .2, c - S * .2, c + S * .2, c + S * .2), fill=AMBER + (255,))
        for i in range(10):
            th = i / 10 * 2 * math.pi + t * .5
            d.line((c + S * .28 * math.cos(th), c + S * .28 * math.sin(th), c + S * .42 * math.cos(th), c + S * .42 * math.sin(th)), fill=AMBER + (255,), width=lw)
    elif kind == 'rain':
        cloud(S * .28, (200, 206, 214, 255))
        for i in range(5):
            x = c - S * .2 + i * S * .1; yy = S * .55 + ((t * 180 + i * 37) % (S * .3))
            d.line((x, yy, x - S * .03, yy + S * .08), fill=BLUE + (255,), width=lw)
    elif kind == 'thermo':
        d.rounded_rectangle((c - S * .07, S * .12, c + S * .07, S * .7), radius=int(S * .07), outline=cc, width=lw)
        d.ellipse((c - S * .14, S * .62, c + S * .14, S * .9), fill=RED + (255,))
        lvl = S * .65 - S * .45 * clamp(t)
        d.rectangle((c - S * .035, lvl, c + S * .035, S * .7), fill=RED + (255,))
    elif kind == 'fire':
        d.polygon([(c, S * .1), (c + S * .25, S * .55), (c + S * .18, S * .85), (c - S * .18, S * .85), (c - S * .25, S * .55)], fill=RED + (255,))
        d.polygon([(c, S * .4), (c + S * .12, S * .65), (c + S * .08, S * .82), (c - S * .08, S * .82), (c - S * .12, S * .65)], fill=AMBER + (255,))
    elif kind == 'flood':
        for j in range(3):
            pts = [(x, S * (.45 + j * .15) + S * .04 * math.sin(x / S * 12 + t * 3 + j)) for x in range(0, S, 4)]
            d.line(pts, fill=BLUE + (255,), width=lw)
    elif kind == 'drought':
        d.ellipse((c - S * .14, S * .1, c + S * .14, S * .38), fill=AMBER + (255,))
        for (x1, y1, x2, y2) in [(.2, .6, .45, .7), (.45, .7, .4, .9), (.45, .7, .7, .62), (.7, .62, .85, .8), (.25, .8, .45, .7)]:
            d.line((S * x1, S * y1, S * x2, S * y2), fill=cc, width=lw)
        d.line((S * .1, S * .55, S * .9, S * .55), fill=cc, width=lw)
    elif kind == 'x':
        d.line((S * .2, S * .2, S * .8, S * .8), fill=RED + (255,), width=lw * 2); d.line((S * .8, S * .2, S * .2, S * .8), fill=RED + (255,), width=lw * 2)
    elif kind == 'snow':
        cloud(S * .3, (200, 206, 214, 255))
        for i in range(4):
            x = c - S * .18 + i * S * .12; yy = S * .62 + (i % 2) * S * .1
            d.text((x, yy), '*', fill=cc, font=font('archivo', int(S * .18)))
    elif kind == 'rice':
        for i in range(7):
            th = -math.pi / 2 + (i - 3) * .28
            x = c + S * .3 * math.cos(th); y = S * .55 + S * .3 * math.sin(th)
            d.ellipse((x - S * .05, y - S * .09, x + S * .05, y + S * .09), fill=CREAM + (255,))
        d.line((c, S * .3, c, S * .92), fill=(160, 140, 80, 255), width=lw)
    paste_c(img, im, cx, cy, a)

# ---------- globe ----------
class Globe:
    def __init__(self, tex_w=2048):
        d = json.load(open('/home/claude/elnino/geo/countries.geojson'))
        tw, th = tex_w, tex_w // 2
        m = Image.new('L', (tw, th), 0); dr = ImageDraw.Draw(m)
        for ft in d['features']:
            g = ft['geometry']; polys = g['coordinates'] if g['type'] == 'MultiPolygon' else [g['coordinates']]
            for poly in polys:
                for ri, ring in enumerate(poly):
                    pts = [((lon + 180) / 360 * tw, (90 - lat) / 180 * th) for lon, lat in ring]
                    # skip polygons crossing dateline badly
                    xs = [p[0] for p in pts]
                    if max(xs) - min(xs) > tw * .6: continue
                    if len(pts) > 2: dr.polygon(pts, fill=255 if ri == 0 else 0)
        self.land = np.asarray(m, np.float32) / 255
        self.edge = np.asarray(m.filter(ImageFilter.FIND_EDGES).filter(ImageFilter.MaxFilter(3)), np.float32) / 255
        self.tw, self.th = tw, th

    def render(self, R, lon0, lat0, heat=None, ocean=(18, 34, 48), land=(58, 58, 60), coast=(150, 145, 135)):
        """returns RGBA disk image 2R x 2R, centred on lon0/lat0. heat: fn(lon,lat)->0..1 added amber/red"""
        n = 2 * R; yy, xx = np.mgrid[0:n, 0:n].astype(np.float32)
        x = (xx - R + .5) / R; y = -(yy - R + .5) / R; rr = x * x + y * y; inside = rr <= 1
        z = np.sqrt(np.clip(1 - rr, 0, 1))
        la0, lo0 = math.radians(lat0), math.radians(lon0)
        lat = np.arcsin(np.clip(y * math.cos(la0) + z * math.sin(la0), -1, 1))
        lon = lo0 + np.arctan2(x, z * math.cos(la0) - y * math.sin(la0))
        latd = np.degrees(lat); lond = (np.degrees(lon) + 180) % 360 - 180
        tx = ((lond + 180) / 360 * (self.tw - 1)).astype(np.int32); ty = ((90 - latd) / 180 * (self.th - 1)).astype(np.int32)
        L = self.land[ty, tx]; E = self.edge[ty, tx]
        col = np.zeros((n, n, 3), np.float32)
        for i in range(3): col[..., i] = ocean[i] * (1 - L) + land[i] * L
        if heat is not None:
            h = heat(lond, latd) * (1 - L)
            hot = np.array([255, 90, 40], np.float32); warm = np.array(AMBER, np.float32)
            hc = hot * h[..., None] + warm * (1 - h[..., None])
            col = col * (1 - np.clip(h * 1.1, 0, .85)[..., None]) + hc * np.clip(h * 1.1, 0, .85)[..., None]
        col = col * (1 - E[..., None]) + np.array(coast, np.float32) * E[..., None]
        shade = 0.55 + 0.45 * z
        col *= shade[..., None]
        a = np.clip((1 - rr) * R * 1.5, 0, 1) * inside
        out = np.dstack([col, a * 255]).clip(0, 255).astype(np.uint8)
        im = Image.fromarray(out, 'RGBA')
        # atmosphere rim
        rim = Image.new('RGBA', (n + 80, n + 80), (0, 0, 0, 0)); ImageDraw.Draw(rim).ellipse((40, 40, n + 40, n + 40), outline=(120, 180, 255, 120), width=10)
        rim = rim.filter(ImageFilter.GaussianBlur(12))
        rim.alpha_composite(im, (40, 40))
        return rim

    def project(self, R, lon0, lat0, lon, lat):
        la0, lo0 = math.radians(lat0), math.radians(lon0); la, lo = math.radians(lat), math.radians(lon)
        cosc = math.sin(la0) * math.sin(la) + math.cos(la0) * math.cos(la) * math.cos(lo - lo0)
        x = R * math.cos(la) * math.sin(lo - lo0)
        y = R * (math.cos(la0) * math.sin(la) - math.sin(la0) * math.cos(la) * math.cos(lo - lo0))
        return x, -y, cosc > 0

# ================= v3: real footage, real globe, proof cards =================
CLIPD = '/home/claude/elnino/clipf/'
_clip_n = {}
def clip_frame(cid, t, W=1920, H=1080, speed=1.0, zoom=(1.0, 1.06), u=0.0):
    """ping-pong playback of pre-extracted 30fps frames; returns RGBA WxH"""
    import os
    if cid not in _clip_n: _clip_n[cid] = len(os.listdir(CLIPD + cid))
    n = _clip_n[cid]; f = int(max(0, t) * 30 * speed); per = 2 * (n - 1)
    k = f % per; k = k if k < n else per - k
    im = Image.open(f"{CLIPD}{cid}/{k + 1:04d}.jpg")
    z = zoom[0] + (zoom[1] - zoom[0]) * u
    if W != 1920 or H != 1080 or z != 1.0:
        sw, sh = im.width, im.height
        s = max(W / sw, H / sh) * z; cw, ch = W / s, H / s
        x0, y0 = (sw - cw) / 2, (sh - ch) / 2
        im = im.resize((W, H), Image.BILINEAR, box=(x0, y0, x0 + cw, y0 + ch))
    return im.convert('RGBA')

def video_bg(img, cid, v, t0, t1, dim=0.45, grad=True, speed=1.0, zoom=(1.0, 1.08)):
    W, H = img.size
    fr = clip_frame(cid, v - t0, W, H, speed, zoom, prog(v, t0, t1))
    img.paste(fr, (0, 0))
    if dim: img.alpha_composite(Image.new('RGBA', (W, H), (0, 0, 0, int(255 * dim))))
    if grad: img.alpha_composite(_grad(W, H))

@functools.lru_cache(4)
def _grad(W, H):
    g = np.zeros((H, W, 4), np.uint8); a = np.clip((np.linspace(0, 1, H) - 0.45) / 0.55, 0, 1) ** 1.5 * 200
    g[..., 3] = a[:, None].astype(np.uint8); return Image.fromarray(g, 'RGBA')

def video_card(img, cid, cx, cy, w, h, v, t0, t1, caption=None, a_out=1.0):
    if v < t0: return
    k = e_out(prog(v, t0, t0 + 0.5)); a = k * a_out
    fr = clip_frame(cid, v - t0, w, h, 1.0, (1.0, 1.05), prog(v, t0, t1)); fr.putalpha(round_mask(w, h, 22))
    sh = Image.new('RGBA', (w + 120, h + 120), (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle((60, 70, w + 60, h + 70), radius=26, fill=(0, 0, 0, 170))
    sh = sh.filter(ImageFilter.GaussianBlur(26)); dy = 50 * (1 - k); sc = .95 + .05 * k
    paste_c(img, sh, cx, cy + dy + 10, a, sc); paste_c(img, fr, cx, cy + dy, a, sc)
    if caption: mono(img, caption, cx - w * sc / 2 + 6, cy + dy + h * sc / 2 + 30, 22, GREY, a, anchor='l', track=2)

@functools.lru_cache(8)
def _sci(name, crop=None):
    im = Image.open('/home/claude/elnino/sci/' + name).convert('RGB')
    if crop: im = im.crop(crop)
    return im

def image_card(img, name, cx, cy, w, v, t0, crop=None, credit=None, zoom=(1.0, 1.0), t1=None, focus=(.5, .5)):
    if v < t0: return
    src = _sci(name, crop); h = int(w * src.height / src.width)
    u = prog(v, t0, t1 or t0 + 6); z = zoom[0] + (zoom[1] - zoom[0]) * e_io(u)
    cw, ch = src.width / z, src.height / z; x0 = (src.width - cw) * focus[0]; y0 = (src.height - ch) * focus[1]
    im = src.resize((w, h), Image.LANCZOS, box=(x0, y0, x0 + cw, y0 + ch)).convert('RGBA')
    pad = 18; card = Image.new('RGBA', (w + 2 * pad, h + 2 * pad + (40 if credit else 0)), (0, 0, 0, 0))
    ImageDraw.Draw(card).rounded_rectangle((0, 0, card.width - 1, card.height - 1), radius=18, fill=(250, 250, 248, 255))
    card.alpha_composite(im, (pad, pad))
    if credit:
        f = font('mono', 18); ImageDraw.Draw(card).text((pad, h + pad + 12), credit, font=f, fill=(90, 90, 90))
    k = e_out(prog(v, t0, t0 + .5))
    paste_c(img, card, cx, cy + 40 * (1 - k), k, .96 + .04 * k)

def news_card(img, source, date, headline, cx, cy, v, t0, w=820, hl_words=(), tilt=-2.0, a_out=1.0):
    """clean proof card: source line, bold headline, highlighted key words"""
    if v < t0: return
    f_src = font('mono', 22); fh = font('archivo', 44) if not is_te(headline) else font('tesans', 42)
    # wrap
    words = headline.split(' '); lines = [[]]; maxw = w - 80
    for wd in words:
        test = ' '.join(lines[-1] + [wd])
        if lines[-1] and fh.getlength(test) > maxw: lines.append([])
        lines[-1].append(wd)
    lh = 60; H = 110 + lh * len(lines) + 20
    card = Image.new('RGBA', (w, H), (0, 0, 0, 0)); d = ImageDraw.Draw(card)
    d.rounded_rectangle((0, 0, w - 1, H - 1), radius=14, fill=(250, 249, 245, 255))
    d.rectangle((0, 0, 10, H), fill=AMBER + (255,))
    d.text((40, 34), source.upper(), font=f_src, fill=(150, 30, 30)); d.text((w - 40, 34), date.upper(), font=f_src, fill=(120, 120, 120), anchor='ra')
    d.line((40, 78, w - 40, 78), fill=(220, 218, 210), width=2)
    hk = e_io(prog(v, t0 + .5, t0 + 1.1)); idx = 0
    for li, ln in enumerate(lines):
        x = 40; y = 100 + li * lh
        for wd in ln:
            ww = fh.getlength(wd)
            if idx in hl_words and hk > 0:
                ext = fh.getlength(' ') if (idx + 1) in hl_words and wd != ln[-1] else 0
                d.rectangle((x - 4, y + 4, x - 4 + (ww + 8 + ext) * hk, y + 54), fill=AMBER + (255,))
            d.text((x, y), wd, font=fh, fill=(15, 15, 15)); x += ww + fh.getlength(' '); idx += 1
    card = card.rotate(tilt, resample=Image.BICUBIC, expand=True)
    sh = Image.new('RGBA', (card.width + 100, card.height + 100), (0, 0, 0, 0)); sh.alpha_composite(Image.new('RGBA', card.size, (0, 0, 0, 160)), (50, 62))
    sh.putalpha(ImageChops.multiply(sh.getchannel('A'), Image.new('L', sh.size, 255))); sh = sh.filter(ImageFilter.GaussianBlur(22))
    k = e_out(prog(v, t0, t0 + .45)); a = k * a_out
    paste_c(img, sh, cx, cy + 60 * (1 - k) + 10, a * .9); paste_c(img, card, cx, cy + 60 * (1 - k), a, .97 + .03 * k)

class RealGlobe(Globe):
    def __init__(self):
        super().__init__(1024)
        t = Image.open('/home/claude/elnino/sci/science_01_nasa_blue_marble_january_5400.jpg').convert('RGB').resize((4096, 2048), Image.LANCZOS)
        a = np.asarray(t, np.float32)
        a = (a - 0) * 1.08; self.tex = np.clip(a, 0, 255); self.TW, self.TH = 4096, 2048
    def render(self, R, lon0, lat0, heat=None, **kw):
        n = 2 * R; yy, xx = np.mgrid[0:n, 0:n].astype(np.float32)
        x = (xx - R + .5) / R; y = -(yy - R + .5) / R; rr = x * x + y * y; inside = rr <= 1
        z = np.sqrt(np.clip(1 - rr, 0, 1)); la0, lo0 = math.radians(lat0), math.radians(lon0)
        lat = np.arcsin(np.clip(y * math.cos(la0) + z * math.sin(la0), -1, 1))
        lon = lo0 + np.arctan2(x, z * math.cos(la0) - y * math.sin(la0))
        latd = np.degrees(lat); lond = (np.degrees(lon) + 180) % 360 - 180
        tx = ((lond + 180) / 360 * (self.TW - 1)).astype(np.int32); ty = ((90 - latd) / 180 * (self.TH - 1)).astype(np.int32)
        col = self.tex[ty, tx].copy()
        dark = np.clip(1 - col.sum(2) / 180, 0, 1)[..., None]
        col = col + dark * np.array([8, 30, 62], np.float32)
        if heat is not None:
            h = np.clip(heat(lond, latd), 0, 1)
            ocean = (dark[..., 0] > 0.15).astype(np.float32)   # dark pixels ~ ocean
            h = h * ocean
            hc = np.array([255, 70, 30], np.float32) * h[..., None] + np.array([255, 170, 40], np.float32) * (1 - h[..., None])
            m = np.clip(h * 1.2, 0, .85)[..., None]; col = col * (1 - m) + hc * m
        # lighting: soft terminator from upper-left
        L = np.array([-0.45, 0.35, 0.82]); L = L / np.linalg.norm(L)
        diff = np.clip(x * L[0] + y * L[1] + z * L[2], 0, 1)
        col = col * (0.42 + 0.78 * diff[..., None])
        a = np.clip((1 - rr) * R * 1.5, 0, 1) * inside
        im = Image.fromarray(np.dstack([col, a * 255]).clip(0, 255).astype(np.uint8), 'RGBA')
        rim = Image.new('RGBA', (n + 80, n + 80), (0, 0, 0, 0)); ImageDraw.Draw(rim).ellipse((40, 40, n + 40, n + 40), outline=(110, 170, 255, 150), width=12)
        rim = rim.filter(ImageFilter.GaussianBlur(14)); rim.alpha_composite(im, (40, 40))
        return rim
