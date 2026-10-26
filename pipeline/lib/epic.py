# Epic cinematic renderer for WHY? bonus videos (El Nino)
import json, math, os, subprocess, sys, functools
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

FPS = 30
FD = "/home/claude/fonts/"
ASSETS = "/home/claude/elnino/assets/"
GOLD_HI = (255, 236, 170); GOLD_LO = (214, 128, 20); AMBER = (255, 178, 36)
WHITE = (244, 241, 234); RED = (255, 84, 48); TEAL = (60, 200, 210)

def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def prog(t, a, b): return clamp((t - a) / max(1e-6, b - a))
def e_out(x): return 1 - (1 - x) ** 3
def e_io(x): return 4 * x ** 3 if x < .5 else 1 - (-2 * x + 2) ** 3 / 2
def e_back(x, s=1.7): x -= 1; return 1 + (s + 1) * x ** 3 + s * x ** 2

# ---------------- fonts / text ----------------
@functools.lru_cache(None)
def font(kind, px):
    if kind == 'cinzel': return ImageFont.truetype(FD + "Cinzel-Black.woff", px)
    if kind == 'cinzelb': return ImageFont.truetype(FD + "Cinzel-Bold.woff", px)
    if kind == 'archivo': return ImageFont.truetype(FD + "ArchivoBlack-Regular.ttf", px)
    if kind == 'mono': return ImageFont.truetype(FD + "SpaceMono-Bold.ttf", px)
    if kind == 'teserif': return ImageFont.truetype(FD + "NotoSerifTelugu-Black.woff", px, layout_engine=ImageFont.Layout.RAQM)
    if kind == 'tesans':
        f = ImageFont.truetype(FD + "NotoSansTelugu.ttf", px, layout_engine=ImageFont.Layout.RAQM); f.set_variation_by_name(b"Black"); return f
    if kind == 'tesansb':
        f = ImageFont.truetype(FD + "NotoSansTelugu.ttf", px, layout_engine=ImageFont.Layout.RAQM); f.set_variation_by_name(b"Bold"); return f
    raise ValueError(kind)

def is_te(s): return any('ఀ' <= c <= '౿' for c in s)

def fit_font(kind, text, px, maxw):
    while px > 18:
        f = font(kind, px); b = f.getbbox(text)
        if b[2] - b[0] <= maxw: return f
        px = int(px * 0.92)
    return font(kind, px)

@functools.lru_cache(512)
def text_sprite(text, kind, px, maxw, style='gold', track=0):
    """returns RGBA sprite of styled text (gold gradient w/ glow), tight with margin"""
    if kind == 'teserif' and any(not ('\u0c00' <= c <= '\u0c7f' or c == ' ') for c in text): kind = 'tesans'
    f = fit_font(kind, text, px, maxw)
    b = f.getbbox(text)
    tw, th = b[2] - b[0] + track * max(0, len(text) - 1), b[3] - b[1]
    m = int(f.size * 0.5)
    W, H = tw + 2 * m, th + 2 * m
    mask = Image.new('L', (W, H), 0); d = ImageDraw.Draw(mask)
    if track and not is_te(text):
        x = m - b[0]
        for ch in text:
            d.text((x, m - b[1]), ch, font=f, fill=255); x += f.getlength(ch) + track
    else:
        d.text((m - b[0], m - b[1]), text, font=f, fill=255)
    out = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    if style == 'gold':
        glow = mask.filter(ImageFilter.GaussianBlur(f.size * 0.18))
        gl = Image.new('RGBA', (W, H), AMBER + (0,)); gl.putalpha(glow.point(lambda v: int(v * 0.85)))
        sh = mask.filter(ImageFilter.GaussianBlur(f.size * 0.06))
        shl = Image.new('RGBA', (W, H), (0, 0, 0, 0)); shl.putalpha(sh.point(lambda v: int(v * 0.9)))
        out = Image.alpha_composite(out, shl); out = Image.alpha_composite(out, gl)
        g = np.zeros((H, W, 3), np.float32); yy = np.linspace(0, 1, H)[:, None]
        y0 = (m) / H; y1 = (m + th) / H; tt = np.clip((yy - y0) / max(1e-3, y1 - y0), 0, 1)
        for i in range(3): g[..., i] = GOLD_HI[i] * (1 - tt) + GOLD_LO[i] * tt
        fill = Image.fromarray(g.astype(np.uint8), 'RGB').convert('RGBA'); fill.putalpha(mask)
        out = Image.alpha_composite(out, fill)
    else:
        col = {'white': WHITE, 'red': RED, 'amber': AMBER, 'teal': TEAL}[style]
        sh = mask.filter(ImageFilter.GaussianBlur(f.size * 0.12))
        shl = Image.new('RGBA', (W, H), (0, 0, 0, 0)); shl.putalpha(sh.point(lambda v: int(v * 0.95)))
        out = Image.alpha_composite(out, shl)
        if style in ('red', 'amber', 'teal'):
            gl = Image.new('RGBA', (W, H), col + (0,)); gl.putalpha(mask.filter(ImageFilter.GaussianBlur(f.size * 0.16)).point(lambda v: int(v * .7)))
            out = Image.alpha_composite(out, gl)
        fill = Image.new('RGBA', (W, H), col + (0,)); fill.putalpha(mask)
        out = Image.alpha_composite(out, fill)
    return out

def paste_center(dst, spr, cx, cy, alpha=1.0, scale=1.0):
    if alpha <= 0.003: return
    if abs(scale - 1) > 0.003:
        spr = spr.resize((max(1, int(spr.width * scale)), max(1, int(spr.height * scale))), Image.BILINEAR)
    if alpha < 0.999:
        a = spr.getchannel('A').point(lambda v: int(v * alpha)); spr = spr.copy(); spr.putalpha(a)
    dst.alpha_composite(spr, (int(cx - spr.width / 2), int(cy - spr.height / 2))) if (0 <= int(cx - spr.width / 2) and 0 <= int(cy - spr.height / 2) and int(cx + spr.width / 2) <= dst.width and int(cy + spr.height / 2) <= dst.height) else _safe_paste(dst, spr, int(cx - spr.width / 2), int(cy - spr.height / 2))

def _safe_paste(dst, spr, x, y):
    tmp = Image.new('RGBA', dst.size, (0, 0, 0, 0)); tmp.paste(spr, (x, y)); dst.alpha_composite(tmp)

# ---------------- images ----------------
@functools.lru_cache(64)
def base_img(name, W, H, over=1.18, fx=0.5, fy=0.5):
    im = Image.open(ASSETS + name).convert('RGB')
    # crop watermark corner a bit
    im = im.crop((int(im.width * .012), int(im.height * .012), int(im.width * .988), int(im.height * .975)))
    s = max(W * over / im.width, H * over / im.height)
    im = im.resize((int(im.width * s + 1), int(im.height * s + 1)), Image.LANCZOS)
    return im

def kb_frame(name, W, H, u, z0=1.0, z1=1.12, fx=0.5, fy=0.5, px=0.0, py=0.0, over=1.18):
    """ken burns: u in 0..1. zoom from z0 to z1 relative to cover; focus fx,fy; pan px,py (fraction of slack)"""
    im = base_img(name, W, H, over)
    z = z0 + (z1 - z0) * u
    cw, ch = W / (over * z) * (im.width / (W * over)) * over, None
    # crop size in source px for given zoom relative to "cover"
    cover_s = max(W / im.width, H / im.height)
    cw = W / (cover_s * z); ch = H / (cover_s * z)
    cx = fx * im.width + px * u * (im.width - cw) * 0.5
    cy = fy * im.height + py * u * (im.height - ch) * 0.5
    x0 = clamp(cx - cw / 2, 0, im.width - cw); y0 = clamp(cy - ch / 2, 0, im.height - ch)
    return im.resize((W, H), Image.BILINEAR, box=(x0, y0, x0 + cw, y0 + ch))

# ---------------- global FX ----------------
class FX:
    def __init__(self, W, H, seed=7):
        self.W, self.H = W, H
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        r = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
        self.vig = np.clip(1.0 - 0.42 * np.clip(r - 0.45, 0, None) ** 1.6, 0.35, 1.0)[..., None].astype(np.float32)
        rng = np.random.default_rng(seed)
        self.grain = [rng.normal(0, 3.5, (H // 2, W // 2)).astype(np.float32) for _ in range(6)]
        n = 70
        self.px = rng.uniform(0, W, n); self.py = rng.uniform(0, H, n)
        self.pv = rng.uniform(18, 70, n); self.ps = rng.uniform(1.2, 3.6, n); self.ph = rng.uniform(0, 6.28, n)
        self.pa = rng.uniform(.25, .9, n)
        sp = 24; yy2, xx2 = np.mgrid[-sp:sp + 1, -sp:sp + 1]
        self.spr = np.exp(-(xx2 ** 2 + yy2 ** 2) / (2 * (sp / 4.5) ** 2)).astype(np.float32)

    def embers(self, arr, t, amount=1.0, col=(255, 170, 60)):
        if amount <= 0: return arr
        W, H = self.W, self.H; sp = self.spr.shape[0] // 2
        add = np.zeros((H, W), np.float32)
        for i in range(len(self.px)):
            y = (self.py[i] - self.pv[i] * t) % (H + 80) - 40
            x = (self.px[i] + 30 * math.sin(t * 0.6 + self.ph[i])) % W
            s = self.ps[i]; r = int(sp * s / 3.6)
            if r < 2: continue
            k = self.spr[::max(1, int(3.6 / s)), ::max(1, int(3.6 / s))]
            kh, kw = k.shape; x0, y0 = int(x - kw / 2), int(y - kh / 2)
            xa, ya = max(0, x0), max(0, y0); xb, yb = min(W, x0 + kw), min(H, y0 + kh)
            if xa >= xb or ya >= yb: continue
            flick = 0.6 + 0.4 * math.sin(t * 3 + self.ph[i] * 3)
            add[ya:yb, xa:xb] += k[ya - y0:yb - y0, xa - x0:xb - x0] * self.pa[i] * flick
        add *= amount
        return arr + add[..., None] * np.array(col, np.float32)[None, None] * 0.9

    def finish(self, img, t, embers=0.6, grade=1.0, vig=1.0, shake=(0, 0), flash=0.0, flash_col=(255, 220, 160), fade=1.0):
        arr = np.asarray(img.convert('RGB'), np.float32)
        if shake != (0, 0):
            arr = np.roll(arr, (int(shake[1]), int(shake[0])), axis=(0, 1))
        if grade:
            # teal shadows / warm highlights + contrast
            lum = arr.mean(2, keepdims=True) / 255.0
            warm = np.array([1.06, 1.0, 0.9], np.float32); cool = np.array([0.9, 1.0, 1.06], np.float32)
            w = np.clip((lum - 0.35) * 2, 0, 1)
            arr = arr * (cool * (1 - w) + warm * w) * grade + arr * (1 - grade)
            arr = (arr - 128) * 1.06 + 128
        arr = self.embers(arr, t, embers)
        if vig: arr = arr * (self.vig * vig + (1 - vig))
        g = self.grain[int(t * FPS) % len(self.grain)]
        g = np.repeat(np.repeat(g, 2, 0), 2, 1)[:self.H, :self.W]
        arr = arr + g[..., None]
        if flash > 0: arr = arr * (1 - flash) + np.array(flash_col, np.float32) * flash
        if fade < 1: arr = arr * fade
        return np.clip(arr, 0, 255).astype(np.uint8)

def shockwave(img, cx, cy, u, col=AMBER, maxr=900):
    if u <= 0 or u >= 1: return
    ov = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    r = maxr * e_out(u); w = int(26 * (1 - u) + 3); a = int(200 * (1 - u) ** 1.5)
    d.ellipse((cx - r, cy - r * 0.62, cx + r, cy + r * 0.62), outline=col + (a,), width=w)
    ov = ov.filter(ImageFilter.GaussianBlur(4)); img.alpha_composite(ov)

def darken(img, a):
    if a <= 0: return img
    ov = Image.new('RGBA', img.size, (0, 0, 0, int(255 * clamp(a))))
    img.alpha_composite(ov); return img

# ---------------- audio synth ----------------
SR = 48000
def boom(dur=2.2, f0=70, f1=34, amp=0.9):
    t = np.arange(int(dur * SR)) / SR
    f = f1 + (f0 - f1) * np.exp(-t * 6); ph = 2 * np.pi * np.cumsum(f) / SR
    body = np.sin(ph) * np.exp(-t * 2.4)
    rng = np.random.default_rng(1); n = rng.normal(0, 1, len(t))
    # lowpass noise
    from scipy.signal import butter, lfilter
    b, a = butter(2, 900 / (SR / 2)); nl = lfilter(b, a, n) * np.exp(-t * 9) * 0.6
    click = np.exp(-t * 90) * rng.normal(0, 1, len(t)) * 0.25
    y = (body + nl + click) * amp
    return np.tanh(y * 1.4) * 0.8

def riser(dur=2.0, amp=0.35):
    from scipy.signal import butter, sosfilt
    t = np.arange(int(dur * SR)) / SR; rng = np.random.default_rng(3); n = rng.normal(0, 1, len(t))
    out = np.zeros_like(n); seg = int(0.05 * SR)
    for i in range(0, len(n), seg):
        fc = 300 + 5000 * (i / len(n)) ** 2
        sos = butter(2, [fc * 0.7 / (SR / 2), min(0.99, fc * 1.3 / (SR / 2))], 'band', output='sos')
        out[i:i + seg] = sosfilt(sos, n[i:i + seg])
    env = (t / dur) ** 2
    return out * env * amp / (np.abs(out).max() + 1e-6)

def thunder(dur=3.0, amp=0.6):
    from scipy.signal import butter, lfilter
    t = np.arange(int(dur * SR)) / SR; rng = np.random.default_rng(5); n = rng.normal(0, 1, len(t))
    b, a = butter(3, 400 / (SR / 2)); y = lfilter(b, a, n)
    env = np.exp(-t * 1.4) * (0.6 + 0.4 * np.sin(t * 23) ** 2)
    y = y / (np.abs(y).max() + 1e-6) * env * amp
    return y

def whoosh(dur=0.8, amp=0.12):
    from scipy.signal import butter, lfilter
    t = np.arange(int(dur * SR)) / SR; rng = np.random.default_rng(9); n = rng.normal(0, 1, len(t))
    b, a = butter(2, 1400 / (SR / 2)); y = lfilter(b, a, n)
    env = np.sin(np.pi * t / dur) ** 2
    return y / (np.abs(y).max() + 1e-6) * env * amp

def load_wav(path):
    import scipy.io.wavfile as wf
    sr, a = wf.read(path); a = a.astype(np.float32) / 32768
    if a.ndim == 1: a = np.stack([a, a], 1)
    if sr != SR: raise ValueError(sr)
    return a
