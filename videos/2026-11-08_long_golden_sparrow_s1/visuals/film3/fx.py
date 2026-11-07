"""Golden Sparrow S1 - visual pass v3: living stills and animated explanations built from the existing artwork.
All coordinates are in the graded image space returned by flib.img(key) (2688x1512 for the illustrations)."""
import math, functools
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFilter
import flib as FL
from flib import W, H, put, text, eo, GOLD, PAPER, INK, MUTED, RUST

def sm(x): x = min(max(x, 0.0), 1.0); return x * x * (3 - 2 * x)
def lerp(a, b, k): return a + (b - a) * k

# ------------------------------------------------------------------ camera on an arbitrary source array
def view(a, cx, cy, s):
    M = np.float32([[s, 0, W / 2 - cx * s], [0, s, H / 2 - cy * s]])
    return cv2.warpAffine(a, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
def cam(a, u, c0, c1, z0, z1, ease=True):
    """c = (fx, fy) as fractions of the source; z relative to 'cover'."""
    h, w = a.shape[:2]; base = max(W / w, H / h); e = (sm(u) * .8 + u * .2) if ease else u
    s = base * lerp(z0, z1, e); fx = lerp(c0[0], c1[0], e); fy = lerp(c0[1], c1[1], e)
    hw, hh = W / 2 / s, H / 2 / s
    cx = min(max(fx * w, hw), w - hw); cy = min(max(fy * h, hh), h - hh)
    return view(a, cx, cy, s)
def to_rgba(a): return Image.fromarray(a).convert('RGBA')

# ------------------------------------------------------------------ living-still effects
@functools.lru_cache(maxsize=4)
def wheel_mask():
    a = FL.img('T5'); h, w = a.shape[:2]; m = np.zeros((h, w), np.float32)
    cv2.circle(m, (470, 890), 352, 1.0, -1)
    cv2.rectangle(m, (405, 800), (548, 1400), 0.0, -1)          # front post + axle stay still
    cv2.ellipse(m, (590, 520), (130, 95), 0, 0, 360, 0.0, -1)  # her hand on the rim stays still
    cv2.rectangle(m, (0, 1240), (w, h), 0.0, -1)
    return cv2.GaussianBlur(m, (0, 0), 5)[..., None]
def wheel(t, speed=6.5):
    """T5 with the charkha wheel turning (motion-blurred) and the oil lamp flickering."""
    a = FL.img('T5').astype(np.float32); c = (470, 890); th = math.degrees(speed * t)
    acc = np.zeros_like(a)
    for k in range(4):
        R = cv2.getRotationMatrix2D(c, th + k * math.degrees(speed / 30) * 0.25, 1.0)
        acc += cv2.warpAffine(a, R, (a.shape[1], a.shape[0]), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    m = wheel_mask(); out = a * (1 - m) + (acc / 4) * m
    fl = 1 + 0.07 * math.sin(t * 23) * math.sin(t * 7.3 + 1) + 0.03 * math.sin(t * 41)
    out *= lamp_field() * (fl - 1) + 1
    return np.clip(out, 0, 255).astype(np.uint8)
@functools.lru_cache(maxsize=2)
def lamp_field():
    h, w = FL.img('T5').shape[:2]; Y, X = np.mgrid[0:h, 0:w]
    return np.exp(-(((X - 940) ** 2 + (Y - 1300) ** 2) / (2 * 520 ** 2))).astype(np.float32)[..., None]

@functools.lru_cache(maxsize=6)
def water_mask(key):
    a = FL.img(key).astype(np.int16); h, w = a.shape[:2]; m = np.zeros((h, w), np.float32)
    if key == 'G09':
        r, g, b = a[..., 0], a[..., 1], a[..., 2]
        reg = np.zeros((h, w), bool); reg[590:1130, 820:] = True
        m[reg & (b + 12 >= r) & (a.sum(2) > 250)] = 1
    elif key == 'G21':
        r, g, b = a[..., 0], a[..., 1], a[..., 2]
        reg = np.zeros((h, w), bool); reg[700:1250, 0:1500] = True
        m[reg & (b + 8 >= r)] = 1
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    return cv2.GaussianBlur(m, (0, 0), 6)
@functools.lru_cache(maxsize=4)
def grids(h, w):
    Y, X = np.mgrid[0:h, 0:w].astype(np.float32); return X, Y
def water(a, key, t, amp=3.0):
    h, w = a.shape[:2]; X, Y = grids(h, w); m = water_mask(key)
    dx = (amp * np.sin(0.045 * Y + 2.3 * t) + 1.2 * np.sin(0.11 * Y - 0.02 * X + 3.7 * t)) * m
    dy = (0.8 * amp * np.sin(0.035 * X + 0.05 * Y + 1.9 * t)) * m
    out = cv2.remap(a, X + dx, Y + dy, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT).astype(np.float32)
    glint = (np.sin(0.09 * X + 0.21 * Y + 4.1 * t) * np.sin(0.13 * X - 0.17 * Y - 2.9 * t)).clip(0.82, 1) - 0.82
    out += (glint * 140 * m)[..., None]
    return np.clip(out, 0, 255).astype(np.uint8)

def swing(a, t, pivot, poly, amp=0.9, period=3.2, feather=9):
    """rotate a masked region (bale + ropes) about a pivot - a pendulum sway."""
    h, w = a.shape[:2]; m = np.zeros((h, w), np.float32); cv2.fillPoly(m, [np.int32(poly)], 1.0)
    m = cv2.GaussianBlur(m, (0, 0), feather)[..., None]
    ang = amp * math.sin(2 * math.pi * t / period)
    R = cv2.getRotationMatrix2D(pivot, ang, 1.0)
    rot = cv2.warpAffine(a, R, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    mr = cv2.warpAffine(m[..., 0], R, (w, h))[..., None]
    return (a * (1 - mr) + rot * mr).astype(np.uint8)
G21_BALE = [(1060, 40), (1240, 40), (1580, 420), (1600, 900), (1480, 1130), (880, 1150), (560, 1010), (560, 560), (900, 420)]

def ripple(a, t, c, ax, amp=4.0):
    h, w = a.shape[:2]; X, Y = grids(h, w)
    nx, ny = (X - c[0]) / ax[0], (Y - c[1]) / ax[1]; r = np.sqrt(nx ** 2 + ny ** 2)
    m = np.clip(1 - r, 0, 1) ** 0.5
    d = amp * np.sin(r * 38 - 5.5 * t) * m
    return cv2.remap(a, X + d * nx, Y + d * ny * 0.6, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)

# ------------------------------------------------------------------ backgrounds
def dark():
    a = np.zeros((H, W, 3), np.float32) + np.array(INK, np.float32)
    Y, X = np.mgrid[0:H, 0:W]; v = 1 - 0.35 * (((X - W / 2) / W) ** 2 + ((Y - H / 2) / H) ** 2) * 2
    return Image.fromarray(np.clip(a * v[..., None] + 8, 0, 255).astype(np.uint8)).convert('RGBA')
@functools.lru_cache(maxsize=6)
def blurred(key, dim=0.32, z=1.08, fx=.5, fy=.5):
    a = cam(FL.img(key), 0, (fx, fy), (fx, fy), z, z)
    a = cv2.GaussianBlur(a, (0, 0), 14).astype(np.float32) * dim
    return a.astype(np.uint8)

# ------------------------------------------------------------------ weaving close-up (procedural, cloth forming pick by pick)
WARP = 24; PICK = 22
@functools.lru_cache(maxsize=2)
def cloth_tex():
    """plain-weave cloth texture W x 2H with a red border band, plus open warp texture."""
    rng = np.random.default_rng(7); hh = H * 2
    base = np.array([232, 220, 196], np.float32)
    X, Y = np.mgrid[0:hh, 0:W][1].astype(np.float32), np.mgrid[0:hh, 0:W][0].astype(np.float32)
    jit = cv2.resize(rng.normal(0, 1, (hh // 40 + 2, W // 40 + 2)).astype(np.float32), (W, hh), interpolation=cv2.INTER_CUBIC)
    X0 = X.copy(); X = X + jit * 0.8; Y = Y + np.roll(jit, 7, 1) * 0.8
    col = (X // WARP).astype(int).clip(0, W // WARP + 1); row = (Y // PICK).astype(int).clip(0, hh // PICK + 1)
    over = ((col + row) % 2 == 0)
    fx = (X % WARP) / WARP; fy = (Y % PICK) / PICK
    shade_w = 0.78 + 0.32 * np.sin(np.pi * fx)       # warp thread round
    shade_p = 0.78 + 0.32 * np.sin(np.pi * fy)       # weft thread round
    sh = np.where(over, shade_w * (0.92 + 0.08 * np.sin(np.pi * fy)), shade_p * (0.92 + 0.08 * np.sin(np.pi * fx)))
    var_c = rng.normal(1, 0.035, W // WARP + 2)[col]; var_r = rng.normal(1, 0.045, hh // PICK + 2)[row]
    weft_col = np.where(((row % 40) >= 30) & ((row % 40) < 34), 1, 0)   # red border band
    c = np.where(weft_col[..., None] & ~over[..., None], np.array([168, 52, 40], np.float32), base)
    fuzz = rng.normal(0, 7, (hh, W)).astype(np.float32); fuzz = cv2.GaussianBlur(fuzz, (0, 0), 0.8)
    woven = np.clip(c * (sh * var_c * var_r)[..., None] + fuzz[..., None], 0, 255)
    woven = cv2.GaussianBlur(woven.astype(np.float32), (0, 0), 0.9)
    c0 = (X0 // WARP).astype(int).clip(0, W // WARP + 1); fx = (X0 % WARP) / WARP; var_c = rng.normal(1, 0.035, W // WARP + 2)[c0]
    warp_only = np.clip(base * (0.6 + 0.45 * np.sin(np.pi * fx))[..., None] * var_c[..., None], 0, 255)
    warp_only = np.where((fx > 0.12)[..., None] & (fx < 0.88)[..., None], warp_only, 40)
    return woven.astype(np.uint8), warp_only.astype(np.uint8)
def shuttle_img():
    s = Image.new('RGBA', (300, 70), (0, 0, 0, 0)); d = ImageDraw.Draw(s)
    d.polygon([(0, 35), (60, 8), (240, 8), (300, 35), (240, 62), (60, 62)], fill=(122, 78, 42, 255), outline=(60, 36, 18, 255))
    d.rounded_rectangle((95, 22, 205, 48), 10, fill=(236, 226, 204, 255))       # bobbin of weft
    for x in range(100, 205, 7): d.line((x, 23, x, 47), fill=(200, 188, 160, 255))
    d.line((10, 35, 290, 35), fill=(150, 100, 60, 120), width=2)
    return s
SHUTTLE = None
def weave(t, a, b, t_first, pass_dur=0.62, period=0.86, push=(1.0, 1.08)):
    """cloth forming: the shuttle crosses the open shed, the reed beats the new pick into the fell."""
    global SHUTTLE
    if SHUTTLE is None: SHUTTLE = shuttle_img()
    woven, warp = cloth_tex()
    n_done = max(0, int((t - t_first) // period) + (1 if t >= t_first else 0))
    ph = (t - t_first) % period if t >= t_first else -1
    fell = int(H * 0.50) - n_done * PICK * 2 + (0 if ph < 0 or ph < pass_dur else int(PICK * 2 * sm((ph - pass_dur) / (period - pass_dur))))
    off = (n_done * PICK * 2) % (PICK * 40)
    fr = np.empty((H, W, 3), np.uint8)
    fy = max(0, min(H, fell))
    fr[fy:] = woven[off:off + H - fy] if H - fy > 0 else fr[fy:]
    # open shed above the fell: alternate warps lifted (slight vertical offset + shading)
    fr[:fy] = warp[:fy]
    fr[:fy, :] = (fr[:fy, :].astype(np.float32) * np.where(((np.arange(W) // WARP) % 2 == (n_done % 2)), 1.0, 0.72)[None, :, None]).astype(np.uint8)
    im = Image.fromarray(fr).convert('RGBA'); d = ImageDraw.Draw(im)
    # reed / beater bar
    ry = fell - 70 if (ph < 0 or ph < pass_dur) else fell - 70 + int(60 * math.sin(math.pi * (ph - pass_dur) / (period - pass_dur)))
    d.rectangle((0, ry - 34, W, ry - 10), fill=(96, 62, 34, 255)); d.rectangle((0, ry - 34, W, ry - 30), fill=(140, 96, 58, 255))
    for x in range(0, W, WARP): d.line((x + WARP // 2, ry - 10, x + WARP // 2, ry + 8), fill=(70, 46, 26, 255), width=2)
    # shuttle crossing + trailing weft
    if 0 <= ph < pass_dur:
        k = sm(ph / pass_dur); left = (n_done % 2 == 0)
        x = lerp(-320, W + 20, k) if left else lerp(W + 20, -320, k)
        y = fell - 40
        d.line((0 if left else W, y + 6, x + 150, y + 6), fill=(236, 226, 204, 255), width=6)
        im.alpha_composite(SHUTTLE if left else SHUTTLE.transpose(Image.FLIP_LEFT_RIGHT), (int(x), int(y - 35)))
    u = (t - a) / max(0.1, b - a)
    arr = np.asarray(im.convert('RGB'))
    arr = cam(arr, u, (.5, .5), (.5, .5), push[0], push[1])
    # warm light + depth of field at frame edges
    top = cv2.GaussianBlur(arr, (0, 0), 7); wy = np.clip((0.42 - np.linspace(0, 1, H)) / 0.32, 0, 1)[:, None, None]   # shallow depth of field
    arr = arr * (1 - wy) + top * wy
    arr = arr.astype(np.float32); Yv = np.linspace(-1, 1, H)[:, None, None]; Xv = np.linspace(-1, 1, W)[None, :, None]
    arr *= (1.08 - 0.22 * ((Xv + 0.5) ** 2 * 0.4 + (Yv + 0.3) ** 2 * 0.6))          # warm key light from the upper left
    arr *= np.array([1.06, 0.98, 0.86]); arr += np.random.default_rng(int(t * 30)).normal(0, 3.0, (H, W, 1))
    return to_rgba(np.clip(arr, 0, 255).astype(np.uint8))
def weave_hits(t_first, t_end, pass_dur=0.62, period=0.86):
    out = []; tt = t_first
    while tt + pass_dur < t_end: out.append(tt + pass_dur); tt += period
    return out

# ------------------------------------------------------------------ many spinners -> one loom
def wheel_icon(d, cx, cy, r, ang, col, w=3):
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=col, width=w)
    for k in range(6):
        a = ang + k * math.pi / 3; d.line((cx, cy, cx + r * math.cos(a), cy + r * math.sin(a)), fill=col, width=2)
    d.ellipse((cx - 4, cy - 4, cx + 4, cy + 4), fill=col)
def loom_icon(d, cx, cy, s, col, k=1.0):
    d.rectangle((cx - 1.4 * s, cy - s, cx + 1.4 * s, cy + s), outline=col, width=4)
    for i in range(15):
        x = cx - 1.2 * s + i * 2.4 * s / 14; d.line((x, cy - s + 10, x, cy + s - 10), fill=col, width=2)
    d.rectangle((cx - 1.4 * s, cy + 0.15 * s, cx + 1.4 * s, cy + 0.15 * s + 10), fill=col)
def spinners(t, a, b, c_many, c_loom, lab_many, lab_loom, te=False):
    fr = dark(); d = ImageDraw.Draw(fr); cx, cy = W / 2, H / 2 + 120
    N = 9; pts = []
    for i in range(N):
        ang = math.pi * (1.08 + 0.84 * i / (N - 1)); R = 640
        pts.append((cx + R * math.cos(ang) * 1.15, cy + R * math.sin(ang) * 0.95))
    kL = eo((t - a + 0.1) / 0.6)
    loom_icon(d, cx, cy, 70, GOLD + (int(255 * kL),))
    for i, (x, y) in enumerate(pts):
        k = eo((t - (c_many - 0.6 + i * 0.09)) / 0.4)
        if k <= 0: continue
        wheel_icon(d, x, y, 38, t * 6 + i, PAPER + (int(255 * k),))
        kt = eo((t - (c_many - 0.3 + i * 0.09)) / 0.9)
        if kt > 0:
            mx, my = (x + cx) / 2, min(y, cy) - 120
            seg = [(lerp(lerp(x, mx, s), lerp(mx, cx, s), s), lerp(lerp(y, my, s), lerp(my, cy - 70, s), s)) for s in np.linspace(0, kt, 40)]
            d.line(seg, fill=(236, 226, 204, 150), width=2)
            ph = (t * 0.9 + i * 0.13) % 1.0                                       # thread pulse travelling to the loom
            if kt >= 1:
                s = ph; px, py = lerp(lerp(x, mx, s), lerp(mx, cx, s), s), lerp(lerp(y, my, s), lerp(my, cy - 70, s), s)
                d.ellipse((px - 5, py - 5, px + 5, py + 5), fill=GOLD + (230,))
    put(fr, text(lab_many, 'label', 40, PAPER), cx, 120, eo((t - c_many) / 0.5), 'ct')
    put(fr, text(lab_loom, 'label', 40, GOLD), cx, cy + 110, eo((t - c_loom) / 0.5), 'ct')
    return fr

# ------------------------------------------------------------------ broker / weaver: advance, price, bargaining power
@functools.lru_cache(maxsize=4)
def medallion(key, cx, cy, r, size):
    a = FL.img(key); crop = a[cy - r:cy + r, cx - r:cx + r]
    im = Image.fromarray(crop).resize((size, size), Image.LANCZOS).convert('RGBA')
    m = Image.new('L', (size, size), 0); ImageDraw.Draw(m).ellipse((4, 4, size - 4, size - 4), fill=255); im.putalpha(m)
    ring = Image.new('RGBA', (size + 16, size + 16), (0, 0, 0, 0)); ImageDraw.Draw(ring).ellipse((2, 2, size + 13, size + 13), outline=GOLD + (255,), width=5)
    ring.alpha_composite(im, (8, 8)); return ring
def broker(t, a, b, cues, labels):
    """cues: weaver, broker, advance, price, power. labels: dict of strings."""
    fr = to_rgba(blurred('T6', 0.30)); d = ImageDraw.Draw(fr)
    bx, wx, y0 = 560, 1360, 470
    tilt = 0.0
    if t > cues['power']: tilt = -11 * eo((t - cues['power']) / 0.9)        # broker side goes down
    kb = eo((t - cues['beam']) / 0.6)
    ang = math.radians(tilt); pcx = (bx + wx) / 2
    ex = (wx - bx) / 2; lx, ly = pcx - ex * math.cos(ang), y0 - ex * math.sin(ang) * -1
    lx, ly = pcx - ex * math.cos(ang), y0 + ex * math.sin(-ang); rx, ry = pcx + ex * math.cos(ang), y0 - ex * math.sin(-ang)
    if kb > 0:
        d.line((lx, ly, rx, ry), fill=GOLD + (int(220 * kb),), width=6)
        d.polygon([(pcx, y0 + 4), (pcx - 30, y0 + 70), (pcx + 30, y0 + 70)], fill=GOLD + (int(220 * kb),))
        d.line((pcx, y0 + 70, pcx, H - 250), fill=GOLD + (int(160 * kb),), width=4)
    mb = medallion('T6', 930, 260, 230, 300); mw = medallion('T6', 1640, 370, 230, 300)
    kw, kbk = eo((t - cues['weaver']) / 0.5), eo((t - cues['broker']) / 0.5)
    put(fr, mw, rx, ry + 40, kw, 'ct'); put(fr, mb, lx, ly + 40, kbk, 'ct')
    put(fr, text(labels['weaver'], 'label', 34, PAPER), rx, ry + 370, kw, 'ct')
    put(fr, text(labels['broker'], 'label', 34, PAPER), lx, ly + 370, kbk, 'ct')
    # advance: coins arc broker -> weaver
    for i in range(6):
        tc = cues['advance'] + i * 0.13; k = (t - tc) / 0.7
        if 0 <= k <= 1.4:
            kk = min(k, 1); x = lerp(lx + 80, rx - 80, sm(kk)); y = lerp(ly + 180, ry + 180, sm(kk)) - 160 * math.sin(math.pi * kk)
            al = 1.0 if k < 1 else max(0, 1 - (k - 1) / 0.4)
            d.ellipse((x - 16, y - 16, x + 16, y + 16), fill=(222, 188, 92, int(255 * al)), outline=(140, 104, 40, int(255 * al)), width=3)
    if t > cues['advance']:
        put(fr, text(labels['advance'], 'label', 30, GOLD), pcx, ly + 250, eo((t - cues['advance'] - 0.3) / 0.5) * (1 - eo((t - cues['price'] + 0.3) / 0.4)), 'ct')
    # price tag stamped by the broker
    kp = eo((t - cues['price']) / 0.25)
    if kp > 0:
        sc = 1 + 0.6 * (1 - kp); tag = text(labels['price'], 'label', 36, (40, 26, 16))
        pad = Image.new('RGBA', (tag.width + 50, tag.height + 30), (0, 0, 0, 0)); pd = ImageDraw.Draw(pad)
        pd.rounded_rectangle((0, 0, pad.width - 1, pad.height - 1), 10, fill=(228, 214, 182, 255), outline=RUST + (255,), width=4); pad.alpha_composite(tag, (25, 15))
        pad = pad.rotate(-6, expand=True, resample=Image.BICUBIC).resize((int(pad.width * sc), int(pad.height * sc)))
        put(fr, pad, pcx, H - 230, kp, 'cc')
    if t > cues['power']:
        put(fr, text(labels['power'], 'label', 36, GOLD), pcx, 120, eo((t - cues['power']) / 0.5), 'ct')
    return fr

# ------------------------------------------------------------------ the palampore being made (MET1, real object)
KAL = (1072, 820, 1200, 675)          # crop in graded MET1 space (x, y, w, h)
@functools.lru_cache(maxsize=1)
def kal_layers():
    a = FL.img('MET1'); x, y, w, h = KAL
    crop = cv2.resize(a[y:y + h, x:x + w], (int(W * 1.12), int(H * 1.12)), interpolation=cv2.INTER_CUBIC).astype(np.float32)
    hsv = cv2.cvtColor(crop.astype(np.uint8), cv2.COLOR_RGB2HSV).astype(np.float32)
    hh, ss, vv = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    lum = crop.mean(2)
    outline = np.clip((95 - lum) / 45, 0, 1)                                       # dark drawn lines
    red = (((hh < 12) | (hh > 165)) & (ss > 60) & (vv > 70)).astype(np.float32)
    blue = ((hh > 60) & (hh < 130) & (ss > 35) & (lum > 50)).astype(np.float32)
    red = cv2.GaussianBlur(red, (0, 0), 2); blue = cv2.GaussianBlur(blue, (0, 0), 2)
    cloth = np.array([238, 228, 204], np.float32)
    detail = (lum - cv2.GaussianBlur(lum, (0, 0), 3))[..., None] * 0.5
    base = np.clip(cloth + detail, 0, 255)
    ink = np.array([52, 36, 26], np.float32)
    hgt, wid = lum.shape
    rng = np.random.default_rng(5); noise = cv2.resize(rng.random((24, 42)).astype(np.float32), (wid, hgt), interpolation=cv2.INTER_CUBIC)
    X = np.linspace(0, 1, wid)[None, :]; Y = np.linspace(0, 1, hgt)[:, None]
    order_draw = np.clip(0.75 * (0.6 * X + 0.4 * Y) + 0.25 * noise, 0, 1)        # pen sweep order
    order_soak = np.clip(noise, 0, 1)                                              # dye soaking order
    return dict(final=crop, base=base, ink=ink, outline=outline, red=red, blue=blue, od=order_draw, os=order_soak)
def kalam(t, a, b, c_draw, c_red, c_blue, c_wax, c_out, label=''):
    L = kal_layers(); f = L['final']
    p_draw = sm((t - c_draw) / 4.2); p_red = sm((t - c_red) / 1.4); p_blue = sm((t - c_blue) / 1.3); p_wax = sm((t - c_wax) / 0.8)
    p_rest = sm((t - c_wax - 0.9) / 1.3)
    img = L['base'].copy()
    # dyes soak in (red, then blue), everything else after the wax step
    mr = (L['os'] < p_red * 1.15).astype(np.float32) * L['red']
    mb = (L['os'] < p_blue * 1.15).astype(np.float32) * L['blue']
    rest = p_rest * (1 - np.clip(L['red'] + L['blue'], 0, 1))
    m = np.clip(mr + mb + rest, 0, 1)[..., None]
    img = img * (1 - m) + f * m
    # mordant lines drawn with the kalam
    md = np.clip((p_draw * 1.08 - L['od']) / 0.04, 0, 1) * L['outline']
    ink_now = L['ink'] * (1 - p_rest) + f * p_rest
    img = img * (1 - md[..., None]) + ink_now * md[..., None]
    # wax: a glossy pale layer that shines then cures
    wx = p_wax * (1 - sm((t - c_wax - 1.2) / 1.0))
    if wx > 0:
        Xs = np.linspace(0, 1, img.shape[1])[None, :]; sheen = np.exp(-((Xs - ((t - c_wax) * 0.6 % 1.4 - 0.2)) ** 2) / 0.004)
        wm = np.clip(L['red'] * 0.9, 0, 1)[..., None]
        img = img * (1 - 0.45 * wx * wm) + 250 * 0.45 * wx * wm + (sheen[..., None] * 60 * wx * wm)
    # nib tip glint on the frontier while drawing
    img = np.clip(img, 0, 255).astype(np.uint8)
    u = (t - a) / max(0.1, b - a)
    # camera: slow push on the detail; after c_out pull back to the whole palampore
    if t < c_out:
        out = cam(img, u * 0.5, (.5, .5), (.52, .5), 1.0, 1.06)
        return to_rgba(out)
    k = sm((t - c_out) / 2.6)
    full = FL.img('MET1'); fh, fw = full.shape[:2]
    x, y, w, h = KAL
    s0 = W / w * 1.0; s1 = min(W / fw, H / fh) * 0.96
    s = math.exp(lerp(math.log(s0), math.log(s1), k))
    cx = lerp(x + w / 2, fw / 2, k); cy = lerp(y + h / 2, fh / 2, k)
    bg = np.full((H, W, 3), INK, np.uint8)
    M = np.float32([[s, 0, W / 2 - cx * s], [0, s, H / 2 - cy * s]])
    out = cv2.warpAffine(full, M, (W, H), dst=bg.copy(), flags=cv2.INTER_AREA if s < 1 else cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=INK)
    fr = to_rgba(out)
    if label: put(fr, text(label, 'label', 30, PAPER), W / 2, H - 70, eo((t - c_out - 1.8) / 0.6), 'cb')
    return fr
