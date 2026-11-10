
# ------------------------------------------------------------------ GS 3/6 scenes (previews: hook, payoff, ships, port)
import cv2, fx as FX, sprites as SP
ACC = AMBER; DBLUE = (60, 110, 190)
def sm_(x): x = clamp(x); return x * x * (3 - 2 * x)

# ---- aged map (real geography via gsmap, Mercator)
class AMap:
    def __init__(self, lon0, lon1, latc, mult=1):
        self.m = mult; self.s = W * mult / ((lon1 - lon0) * gsmap.AX); self.x0 = gsmap.to_svg(lon0, 0)[0]; self.yc = gsmap.to_svg(0, latc)[1]
        self.base = self._render()
    def P(self, lon, lat):
        x, y = gsmap.to_svg(lon, lat); return ((x - self.x0) * self.s, H * self.m / 2 + (y - self.yc) * self.s)
    def _tr(self, q): return [((x - self.x0) * self.s, H * self.m / 2 + (y - self.yc) * self.s) for x, y in q]
    def _render(self):
        Wm, Hm = W * self.m, H * self.m; im = Image.new('RGB', (Wm, Hm), (176, 186, 178)); d = ImageDraw.Draw(im)
        for f in gsmap.GEO['features']:
            n = f['properties']['name']
            if n == 'India': continue
            for q in gsmap.polys(n):
                if len(q) > 2:
                    p = self._tr(q)
                    if max(x for x, y in p) < 0 or min(x for x, y in p) > Wm: continue
                    d.polygon(p, fill=(206, 190, 152), outline=(150, 128, 92))
        for q in gsmap.india_polys():
            if len(q) > 2: d.polygon(self._tr([tuple(z) for z in q]), fill=(222, 200, 150))
        for n in ('Pakistan', 'Bangladesh'):
            for q in gsmap.polys(n):
                if len(q) > 2: d.polygon(self._tr(q), fill=(222, 200, 150))
        im = im.filter(ImageFilter.GaussianBlur(0.8)); a = np.asarray(im).astype(np.float32)
        rng = np.random.default_rng(3); n = cv2.GaussianBlur(cv2.resize(rng.random((12, 7)).astype(np.float32), (Wm, Hm), interpolation=cv2.INTER_CUBIC), (0, 0), 60)[..., None]
        a = a * (0.95 + 0.08 * n) * np.array([1.0, .96, .86])
        if self.m == 1: a = a * VIG() * 1.02
        return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    def cam(self, cx, cy, z):
        """view of the big map centred on (cx, cy) in big coords, z = magnification relative to the full view"""
        w, h = W * self.m / z, H * self.m / z; cx = min(max(cx, w / 2), W * self.m - w / 2); cy = min(max(cy, h / 2), H * self.m - h / 2)
        im = self.base.resize((W, H), Image.BILINEAR, box=(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2))
        sc = W / w; return grade(im, 1.02), (lambda p: ((p[0] - (cx - w / 2)) * sc, (p[1] - (cy - h / 2)) * sc))

@functools.lru_cache(6)
def amap(lon0, lon1, latc, mult=1): return AMap(lon0, lon1, latc, mult)
KRISHNA = [(73.7, 17.9), (74.6, 16.85), (75.6, 16.4), (76.5, 16.2), (77.4, 16.2), (78.3, 16.0), (78.87, 16.08), (79.3, 16.57), (80.05, 16.75), (80.62, 16.51), (80.95, 15.85)]
GOLC = (78.40, 17.38); KOLLUR = (80.03, 16.72); MTM = (81.14, 16.19)

def map_label(img, s, x, y, px=30, col=INK, a=1.0, anchor='mm'):
    f = pick(s, 'monob', px); w = f.getlength(s) + 26; x0 = x - w / 2 if anchor == 'mm' else x
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(lay).rounded_rectangle((x0, y - px * .8, x0 + w, y + px * .8), 12, fill=(244, 236, 214, int(225 * a)))
    img.paste(lay, (0, 0), lay); text(img, s, x0 + w / 2, y, px, col, 'mm', 'monob', a, None, None)

# ---- cutouts
@functools.lru_cache(1)
def DIAMOND():
    """the approved diamond (G11), whole stone visible, on its own dark cloth extended to 9:16"""
    a = IMG('G11'); h, w = a.shape[:2]; x0, x1 = int(w * .30), int(w * .86); c = a[:, x0:x1]
    sc = W / c.shape[1]; c = cv2.resize(c, (W, int(h * sc)), interpolation=cv2.INTER_AREA); ch = c.shape[0]
    bg = cv2.resize(cv2.GaussianBlur(c, (0, 0), 40), (W, H), interpolation=cv2.INTER_LINEAR).astype(np.float32) * 0.45
    y0 = int(H * .47 - ch * .47); out = bg.copy(); m = np.ones((ch, 1, 1), np.float32); f = 160
    m[:f, 0, 0] = np.linspace(0, 1, f); m[-f:, 0, 0] = np.linspace(1, 0, f)
    out[y0:y0 + ch] = out[y0:y0 + ch] * (1 - m) + c.astype(np.float32) * m
    return np.clip(out, 0, 255).astype(np.uint8)
@functools.lru_cache(1)
def DIA_CUT():
    a = DIAMOND(); cy, cx, r = int(H * .46), int(W * .50), 520
    c = a[cy - r:cy + r, cx - r:cx + r]; yy, xx = np.mgrid[-r:r, -r:r]; m = np.clip(1.25 - np.sqrt(xx ** 2 + yy ** 2) / r * 1.3, 0, 1) ** 1.5
    return Image.fromarray(np.dstack([c, (m * 255).astype(np.uint8)]), 'RGBA')
def diamond_lit(t, k=1.0, z=1.0):
    """restrained moving light: a narrow diagonal band lifts only the bright facets; local gain on the stone only"""
    a = DIAMOND().astype(np.float32); Y, X = np.mgrid[0:H, 0:W].astype(np.float32)
    pos = ((t * 0.42 + 0.42) % 1.6 - 0.3) * (W + H); band = np.exp(-((X + Y * .6 - pos) ** 2) / (2 * 120.0 ** 2))
    lum = a.mean(2) / 255.0; loc = np.exp(-(((X - W * .5) / 520) ** 2 + ((Y - H * .46) / 520) ** 2))
    a = a * (0.85 + 0.75 * loc[..., None] + 0.6 * band[..., None] * (lum[..., None] ** 1.5) * 2.2) * k
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    return zoom(im, 1.22 * z, cy=.46)

@functools.lru_cache(1)
def BALE():
    """our fish-and-7 bale cut from the approved hoist painting (G21)"""
    a = IMG('G21'); m = np.zeros(a.shape[:2], np.float32); poly = np.int32([(880, 430), (1500, 430), (1600, 900), (1480, 1130), (880, 1150), (560, 1010), (560, 560)])
    cv2.fillPoly(m, [poly], 1.0); m = cv2.GaussianBlur(m, (0, 0), 5)
    x0, y0, x1, y1 = 540, 410, 1620, 1170
    return Image.fromarray(np.dstack([a[y0:y1, x0:x1], (m[y0:y1, x0:x1] * 255).astype(np.uint8)]), 'RGBA')
def bale_at(img, cx, cy, wpx, a=1.0, dark=1.0, rot=0.0):
    b = BALE(); s = wpx / b.width; b = b.resize((int(b.width * s), int(b.height * s)), Image.LANCZOS)
    if dark < 1: arr = np.asarray(b).astype(np.float32); arr[..., :3] *= dark; b = Image.fromarray(arr.astype(np.uint8), 'RGBA')
    if rot: b = b.rotate(rot, expand=True, resample=Image.BICUBIC)
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).ellipse((cx - b.width * .42, cy + b.height * .40, cx + b.width * .42, cy + b.height * .52), fill=(0, 0, 0, int(120 * a)))
    sh = sh.filter(ImageFilter.GaussianBlur(14)); img.paste(sh, (0, 0), sh); paste_c(img, b, cx, cy, a)

def cov(key, t, s0, s1, c0, c1, z0, z1, k=.95, alive=None):
    arr = IMG(key)
    if alive: arr = alive(arr, t)
    return grade(cover(arr, (t - s0) / max(.1, s1 - s0), c0, c1, z0, z1), k)

# ------------------------------------------------------------------ 0:00 hook: diamond -> historical geography -> the covered bale
def s_hook(t, s0, s1, frame0=False):
    c_pull = AT('S3_hook', 'many', 'ఎన్నో') - 0.1; c_but = AT('S3_hook', 'But', 'కానీ') - 0.15; c_else = AT('S3_hook', 'something', 'వేరే') - 0.1
    if frame0 or t < c_pull:
        return diamond_lit(0.0 if frame0 else t, 1.0, 1.0 + 0.03 * (0 if frame0 else t))
    M = amap(72.0, 86.0, 16.6); gx, gy = M.P(*GOLC)
    if t < c_but:
        u = sm_((t - c_pull) / 1.1); img = Image.blend(diamond_lit(t, 1.0, 1.0 + 0.04 * t), M.base, sm_((t - c_pull) / 0.7))
        d = ImageDraw.Draw(img); kr = sm_((t - c_pull - 0.5) / 1.4)
        pts = [M.P(*p) for p in KRISHNA]; n = max(2, int(len(pts) * kr) + 1)
        if kr > 0: d.line(pts[:n], fill=(70, 110, 150), width=6, joint='curve')
        dc = DIA_CUT(); sz = lerp(1.22, 0.15, u); paste_c(img, dc, lerp(W / 2, gx, u), lerp(H * .46, gy, u), 1.0, sz)
        if u > .8:
            a = sm_((u - .8) / .2); glow(img, gx, gy, 90, AMBER, .35 * a) if False else None
            map_label(img, L('GOLCONDA', 'గోల్కొండ'), gx, gy - 125, 48, INK, a)
            map_label(img, L('KRISHNA RIVER', 'కృష్ణా నది'), M.P(76.3, 16.2)[0], M.P(76.3, 16.2)[1] + 70, 32, (50, 80, 110), a * kr)
        return img
    # the mystery: the map falls into shadow; a covered bale waits; the diamond stays small above it
    k = sm_((t - c_but) / 0.6); base = Image.blend(M.base, Image.new('RGB', (W, H), (10, 9, 8)), 0.86 * k)
    img = base; dc = DIA_CUT(); paste_c(img, dc, lerp(gx, 250, k), lerp(gy, 520, k), 1.0, lerp(0.16, 0.30, k))
    kb = sm_((t - c_but - 0.2) / 0.8); bale_at(img, W / 2 + 40, lerp(1400, 1130, kb), 720, kb, dark=lerp(0.10, 0.22, sm_((t - c_else) / 0.8)))
    kq = e_back(prog(t, c_else, c_else + 0.35))
    if kq > .01: text(img, '?', W / 2 + 40, 1110, int(260 * min(1.15, kq)), AMBER, 'mm', 'head', min(1, kq))
    return img

# ------------------------------------------------------------------ 0:46 payoff: diamond -> one bale -> the hold -> the fleet
def s_payoff(t, s0, s1):
    c_dia = AT('3.9', 'Diamonds', 'వజ్రాలు') - 0.1; c_cloth = AT('3.9', 'Cloth', 'ఓడలు') - 0.12
    c_fist = AT('3.9', 'A', 'ఒక') - 0.1; c_fleet = AT('3.9', 'Cloth', 'గుడ్డ', n=2 if not TE else 1) - 0.12
    MX, MY = .46, .50          # the fish-and-7 mark on our bale in G21 (fraction of the image)
    if t < c_cloth:
        k = lerp(0.55, 1.0, sm_((t - c_dia) / 0.4)); img = diamond_lit(t, k, 1.0 + 0.06 * sm_((t - s0) / max(.1, c_cloth - s0)))
        ka = e_back(prog(t, c_dia + .15, c_dia + .5))
        if ka > .01: chip(img, L('DIAMONDS · THE LEGENDS', 'వజ్రాలు · కథలు'), W / 2, 1210, 46, CREAM, INK, a=min(1, ka), scale=min(1, ka))
        # match-cut: in the last 0.22 s the diamond collapses toward the centre where the bale's mark will be
        kc = sm_((t - (c_cloth - 0.22)) / 0.22)
        if kc > 0: img = Image.blend(zoom(img, 1 + 1.6 * kc), Image.new('RGB', (W, H), (236, 214, 170)), 0.55 * kc)
        return img
    d1 = min(1.15, (c_fist - c_cloth) * 0.42)
    if t < c_cloth + d1:        # ONE bale: start on its mark (same screen position/size as the diamond), ease back
        u = (t - c_cloth) / d1; img = cov('G21', t, c_cloth, c_cloth + d1, (MX, MY), (MX + .02, MY + .01), 3.2, 1.25, 1.0, alive=lambda a_, tt: FX.swing(a_, tt, (1140, 80), FX.G21_BALE))
        kf = 1 - sm_(u / 0.25)
        if kf > 0: img = Image.blend(img, Image.new('RGB', (W, H), (236, 214, 170)), 0.55 * kf)
        chip(img, L('ONE BALE OF CLOTH', 'ఒక్క గుడ్డ మూట'), W / 2, 1210, 46, AMBER, INK, a=sm_(u / .3))
        return img
    if t < c_fist:              # the hold: pull back from a marked bale to the whole stacked hold
        img = cov('G13', t, c_cloth + d1, c_fist, (.47, .44), (.52, .50), 2.4, 1.0, .98)
        chip(img, L("A SHIP'S HOLD", 'ఓడ గిడ్డంగి'), W / 2, 1210, 46, AMBER, INK, a=sm_((t - c_cloth - d1) / .3))
        return img
    if t < c_fleet:             # a diamond fits in your fist: the same diamond, small, alone
        k = sm_((t - c_fist) / 0.5); img = Image.new('RGB', (W, H), (10, 9, 8)); dc = DIA_CUT()
        paste_c(img, dc, W / 2, 860, 1.0, lerp(0.70, 0.28, k))
        r = lerp(330, 150, k); lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(lay).ellipse((W / 2 - r, 860 - r, W / 2 + r, 860 + r), outline=CREAM + (int(170 * k),), width=4); img.paste(lay, (0, 0), lay)
        chip(img, L('ONE DIAMOND · FITS IN A FIST', 'ఒక వజ్రం · గుప్పిట్లో పడుతుంది'), W / 2, 1210, 42, CREAM, INK, a=k)
        return img
    # whole fleets: the harbour pulls back while more trading ships appear one by one (illustrative)
    def fleet(a_, tt):
        a_ = FX.water(a_, 'G09', tt).astype(np.float32); sx0, sy0, sx1, sy1 = 1690, 215, 2010, 560; ship_ = IMG('G09')[sy0:sy1, sx0:sx1].astype(np.float32)
        for i, (px_, sc_) in enumerate(((1330, .62), (2190, .70), (1520, .46), (1235, .40), (2330, .50))):
            ka = sm_((tt - c_fleet - 0.25 - i * 0.42) / 0.45)
            if ka <= 0: continue
            w_, h_ = int((sx1 - sx0) * sc_), int((sy1 - sy0) * sc_); sp = cv2.resize(ship_, (w_, h_), interpolation=cv2.INTER_AREA)
            yy, xx = np.mgrid[0:h_, 0:w_].astype(np.float32); m = np.clip(1.15 - np.sqrt(((xx - w_ / 2) / (w_ / 2)) ** 2 + ((yy - h_ * .52) / (h_ / 2)) ** 2), 0, 1); m = np.clip(m * 3.2, 0, 1)[..., None] * ka
            x_ = int(px_ - w_ / 2 + (1 - ka) * 60); y_ = int(545 - h_ * .93 + 2 * math.sin(tt * 2 + i))
            if x_ < 0 or x_ + w_ > a_.shape[1]: continue
            a_[y_:y_ + h_, x_:x_ + w_] = a_[y_:y_ + h_, x_:x_ + w_] * (1 - m) + sp * m
        return a_.astype(np.uint8)
    img = cov('G09', t, c_fleet, s1 + 0.4, (.74, .40), (.62, .44), 1.5, 1.0, 1.0, alive=fleet)
    kd = sm_((t - c_fleet) / 0.5); paste_c(img, DIA_CUT(), 170, 470, kd, 0.17)
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(lay).ellipse((170 - 100, 470 - 100, 170 + 100, 470 + 100), outline=CREAM + (int(190 * kd),), width=4); img.paste(lay, (0, 0), lay)
    kl = e_back(prog(t, c_fleet + 0.9, c_fleet + 1.25))
    if kl > .01: chip(img, L('TEXTILES · A MAJOR EXPORT TRADE', 'గుడ్డ · ఒక ప్రధాన ఎగుమతి వ్యాపారం'), W / 2, 1210, 40, AMBER, INK, a=min(1, kl), scale=min(1, kl))
    text(img, L('SCALE SHOWN IS ILLUSTRATIVE', 'ఇది ఉదాహరణ దృశ్యం'), W / 2, 1690, 24, CREAM, kind='monob', a=kd)
    return img

# ------------------------------------------------------------------ 1:10 ships arrive (real geography)
ROUTES = [(('Persia,', 'Persia,'), L('PERSIA', 'పర్షియా'), [(56.3, 26.6), (58.5, 24.2), (64, 19), (72, 11), (77.6, 6.6), (81.3, 8.2), (82.4, 12.5), (81.5, 15.6), MTM], (55.5, 28.4)),
          (('Arabia,', 'అరేబియా,'), L('ARABIA', 'అరేబియా'), [(45.6, 12.3), (52, 12.3), (62, 10.5), (72, 7.6), (77.6, 5.8), (81.6, 7.4), (82.9, 12), (81.7, 15.4), MTM], (46.5, 16.2)),
          (('Burma', 'బర్మా,'), L('BURMA', 'బర్మా'), [(96.2, 16.2), (93.5, 15.2), (89, 15.6), (85, 16.0), MTM], (96.6, 19.4)),
          (('Southeast', 'ఆగ్నేయాసియా'), L('SOUTHEAST ASIA', 'ఆగ్నేయాసియా'), [(101.5, 2.4), (98.5, 5.2), (94.5, 6.6), (89, 10.5), (84.5, 14.2), MTM], (101.5, -1.2))]
def pathpt(pts, f):
    f = clamp(f); seg = [math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]; tot = sum(seg); d = f * tot
    for i, s_ in enumerate(seg):
        if d <= s_ or i == len(seg) - 1:
            u = d / s_ if s_ else 0; return (lerp(pts[i][0], pts[i + 1][0], u), lerp(pts[i][1], pts[i + 1][1], u))
        d -= s_
def s_ships(t, s0, s1):
    M = amap(41.0, 107.0, 9.0); img = M.base.copy(); z = 1.0
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); mx, my = M.P(*MTM)
    for (en, te), lab, route, lp in ROUTES:
        c = AT('3.3', en, te) - 0.35; f = sm_((t - c) / max(1.6, (s1 - c) * 0.95)); pts = [M.P(*p) for p in route]
        if t < c: continue
        n = 40; tr = [pathpt(pts, f * i / n) for i in range(n + 1)]
        for i in range(0, n, 2): d.line([tr[i], tr[i + 1]], fill=(120, 70, 30, 220), width=4)
        x, y = tr[-1]; SP.ship(d, x, y + 20 + 3 * math.sin(t * 3 + x), 95, a=1.0)
    img.paste(lay, (0, 0), lay)
    for (en, te), lab, route, lp in ROUTES:
        c = AT('3.3', en, te) - 0.35; k = e_back(prog(t, c, c + .3))
        if k > .01: hw_ = pick(lab, 'monob', 40).getlength(lab) / 2 + 30; map_label(img, lab, min(max(M.P(*lp)[0], hw_), W - hw_), M.P(*lp)[1], 40, INK, min(1, k))
    r = 16 + 5 * math.sin(t * 5); ImageDraw.Draw(img).ellipse((mx - r, my - r, mx + r, my + r), fill=AMBER, outline=INK, width=3)
    map_label(img, L('MACHILIPATNAM', 'మచిలీపట్నం'), mx - 40, my - 90, 44, INK, 1.0)
    return zoom(img, 1 + 0.05 * sm_((t - s0) / max(.1, s1 - s0)))

# ------------------------------------------------------------------ 1:15 the port: traders -> brokers -> our bale goes aboard
def s_port(t, s0, s1):
    c_du = AT('3.3', 'Dutch', 'డచ్') - 0.1; c_en = AT('3.3', 'English', 'ఇంగ్లీష్') - 0.1
    c_loc = AT('3.3', 'Local', 'మన') - 0.15; c_weave = AT('3.3', 'weaving', 'నేత') - 0.9
    if t < c_loc:
        img = cov('G09', t, s0, c_loc, (.30, .50), (.52, .46), 1.25, 1.05, 1.0, alive=lambda a_, tt: FX.water(a_, 'G09', tt))
        k0 = sm_((t - s0) / .4); chip(img, L('MACHILIPATNAM · THE PORT', 'మచిలీపట్నం · రేవు'), W / 2, 400, 40, CREAM, INK, a=k0)
        for i, (c, lab) in enumerate(((c_du, L('DUTCH TRADE · EARLY 1600s', 'డచ్ వ్యాపారం · 1600ల మొదట్లో')), (c_en, L('ENGLISH TRADE · 1611', 'ఇంగ్లీష్ వ్యాపారం · 1611')))):
            k = e_back(prog(t, c, c + .3))
            if k > .01: chip(img, lab, W / 2, 1130 + i * 96, 40, AMBER, INK, a=min(1, k), scale=min(1, k))
        return img
    c_thr = max(c_loc + 1.3, c_weave - 2.0); c_hoist = c_weave + 0.35
    if t < c_thr:
        img = cov('G10', t, c_loc, c_thr, (.42, .52), (.50, .50), 1.0, 1.22, 1.0)
        k = e_back(prog(t, c_loc + .2, c_loc + .5))
        if k > .01: chip(img, L('BROKERS & INTERPRETERS', 'దళారులు · దుబాసీలు'), W / 2, 400, 42, AMBER, INK, a=min(1, k), scale=min(1, k))
        return img
    if t < c_hoist:
        return thread_map(t, c_thr, c_hoist)
    img = cov('G21', t, c_hoist, s1, (.44, .55), (.46, .45), 1.0, 1.12, 1.0, alive=lambda a_, tt: FX.water(FX.swing(a_, tt, (1140, 80), FX.G21_BALE, amp=1.3, period=2.6), 'G21', tt))
    k = e_back(prog(t, c_hoist + .15, c_hoist + .45))
    if k > .01: chip(img, L('OUR BALE · ABOARD', 'మన మూట · ఓడలోకి'), W / 2, 400, 42, AMBER, INK, a=min(1, k), scale=min(1, k))
    return img

VILLAGES = [(81.73, 16.52), (81.15, 16.47), (80.75, 16.05), (81.5, 16.95), (80.45, 15.75), (82.05, 16.9)]
def thread_line(img, pts, k, col=AMBER, w=7):
    if k <= 0 or len(pts) < 2: return pts[0]
    seg = [math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]; tot = sum(seg); d_ = k * tot; out = [pts[0]]
    for i, s_ in enumerate(seg):
        if d_ >= s_: out.append(pts[i + 1]); d_ -= s_
        else: u = d_ / s_; out.append((lerp(pts[i][0], pts[i + 1][0], u), lerp(pts[i][1], pts[i + 1][1], u))); break
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(lay).line(out, fill=col + (255,), width=w, joint='curve')
    g = lay.filter(ImageFilter.GaussianBlur(8)); img.paste(g, (0, 0), g); img.paste(lay, (0, 0), lay); return out[-1]
def thread_map(t, s0, s1):
    """our cotton thread: WEAVING VILLAGES -> BROKERS -> MACHILIPATNAM -> SHIP (real coast; village dots illustrative)"""
    M = amap(78.6, 83.6, 16.25); img = M.base.copy(); d = ImageDraw.Draw(img); u = (t - s0) / max(.1, s1 - s0)
    hub = M.P(81.02, 16.36); port = M.P(*MTM); ship = M.P(82.25, 15.55)
    for i, v in enumerate(VILLAGES):
        x, y = M.P(*v); ka = sm_((u - i * .03) / .12)
        if ka > 0:
            r = 13 * ka; d.ellipse((x - r, y - r, x + r, y + r), fill=(120, 70, 30), outline=(244, 236, 214), width=3)
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dl = ImageDraw.Draw(lay); SP.ship(dl, ship[0], ship[1] + 30 + 3 * math.sin(t * 3), 150, a=1.0); img.paste(lay, (0, 0), lay)
    kv = sm_((u - .12) / .30)
    for i, v in enumerate(VILLAGES):
        x, y = M.P(*v); thread_line(img, [(x, y), ((x + hub[0]) / 2 + 20 * math.sin(i), (y + hub[1]) / 2 - 18), hub], kv, AMBER, 5)
    kp = sm_((u - .42) / .5); head = thread_line(img, [hub, ((hub[0] + port[0]) / 2, hub[1] + 26), port, ((port[0] + ship[0]) / 2, port[1] + 70), (ship[0], ship[1] - 10)], kp, AMBER, 8)
    bx, by = head if kp > 0 else hub; b = BALE(); bw = 120; bi = b.resize((bw, int(b.height * bw / b.width)), Image.LANCZOS)
    if kv > .9: paste_c(img, bi, bx, by - 34, sm_((kv - .9) / .1))
    d = ImageDraw.Draw(img); r = 16; d.ellipse((port[0] - r, port[1] - r, port[0] + r, port[1] + r), fill=AMBER, outline=INK, width=3)
    map_label(img, L('WEAVING VILLAGES', 'నేత గ్రామాలు'), M.P(81.6, 17.35)[0], M.P(81.6, 17.35)[1], 38, INK, sm_(u / .15))
    map_label(img, L('BROKERS', 'దళారులు'), hub[0] - 150, hub[1] - 10, 38, INK, sm_((u - .3) / .12))
    map_label(img, L('MACHILIPATNAM', 'మచిలీపట్నం'), port[0] - 170, port[1] + 70, 38, INK, sm_((u - .5) / .12))
    map_label(img, L('SHIP', 'ఓడ'), ship[0] - 150, ship[1] + 20, 38, INK, sm_((u - .75) / .12))
    img = zoom(img, 1.5 + .05 * u, cy=.50)
    text(img, L('VILLAGE POSITIONS ARE ILLUSTRATIVE', 'గ్రామాల స్థానాలు ఉదాహరణకు మాత్రమే'), W / 2, 1690, 26, INK, kind='monob', shadow=None)
    return img

def dust(img, t, n=46, a=0.5):
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); rng = np.random.default_rng(11)
    for i in range(n):
        x0, y0, sp, r = rng.random() * W, rng.random() * H, 20 + rng.random() * 50, 2 + rng.random() * 5
        x = (x0 + t * sp) % W; y = (y0 - t * sp * .35 + 30 * math.sin(t + i)) % H
        d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 230, 180, int(255 * a * (0.25 + 0.5 * rng.random()))))
    lay = lay.filter(ImageFilter.GaussianBlur(2.2)); img.paste(lay, (0, 0), lay)

def s_kollur(t, s0, s1):
    """journey down the Krishna to Kollur, then where the world's diamonds came from"""
    c_k = AT('3.6', 'Kollur', 'కొల్లూరు'); c_world = AT('3.6', 'Until', '1720లలో') - 0.25
    if t < c_world:
        M = amap(72.5, 83.5, 16.6, 3); pts = [M.P(*p) for p in KRISHNA[:9]]; u = sm_((t - s0 - 0.2) / max(.5, c_k - s0 + 0.2))
        hx, hy = pathpt(pts, u); z = lerp(1.9, 3.1, u); img, S_ = M.cam(hx + 80, hy, z); d = ImageDraw.Draw(img)
        allp = [S_(M.P(*p)) for p in KRISHNA]; d.line(allp, fill=(120, 150, 170), width=5, joint='curve')
        n = 60; tr = [S_(pathpt(pts, u * i / n)) for i in range(n + 1)]; d.line(tr, fill=(50, 96, 150), width=12, joint='curve')
        hd = S_((hx, hy)); r = 12; d.ellipse((hd[0] - r, hd[1] - r, hd[0] + r, hd[1] + r), fill=(244, 236, 214), outline=(50, 96, 150), width=4)
        map_label(img, L('KRISHNA RIVER', 'కృష్ణా నది'), W / 2, 420, 40, (40, 76, 120), sm_((t - s0) / .4))
        kk = e_back(prog(t, c_k - .1, c_k + .25))
        if kk > .01:
            kx, ky = S_(M.P(*KOLLUR)); r = 20 * min(1, kk); d = ImageDraw.Draw(img); d.ellipse((kx - r, ky - r, kx + r, ky + r), fill=AMBER, outline=INK, width=4)
            map_label(img, L('KOLLUR MINES', 'కొల్లూరు గనులు'), kx - 40, ky - 80, 48, INK, min(1, kk))
            map_label(img, L("near today's Pulichintala", 'ఇప్పటి పులిచింతల దగ్గర'), kx - 40, ky + 76, 30, INK, min(1, kk))
        return img
    M = amap(-88.0, 128.0, 6.0); img = M.base.copy(); d = ImageDraw.Draw(img)
    ix, iy = M.P(79, 20); bx, by = M.P(-43.6, -18.2); ox, oy = M.P(114, 0.5)
    c_br = AT('3.6', "Brazil's", 'బ్రెజిల్‌లో') - .1; c_in = AT('3.6', 'India', 'ప్రపంచానికి') - .1; c_bo = AT('3.6', 'Borneo', 'బోర్నియో') - .1
    ki = e_back(prog(t, min(c_in, c_world + .2), min(c_in, c_world + .2) + .4)) if TE else e_back(prog(t, c_world + .15, c_world + .5))
    r = 34 + 8 * math.sin(t * 4); lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dl = ImageDraw.Draw(lay)
    dl.ellipse((ix - r * 2.2, iy - r * 2.2, ix + r * 2.2, iy + r * 2.2), fill=AMBER + (70,)); dl.ellipse((ix - r, iy - r, ix + r, iy + r), fill=AMBER + (255,), outline=INK + (255,), width=4); img.paste(lay, (0, 0), lay)
    map_label(img, L('INDIA · THE MAJOR SOURCE', 'భారత్ · ప్రధాన వనరు'), W / 2 + 120, iy - 110, 40, INK, min(1, ki))
    kb = e_back(prog(t, c_br, c_br + .3))
    if kb > .01:
        r = 22 * min(1, kb); d.ellipse((bx - r, by - r, bx + r, by + r), fill=(90, 120, 90), outline=INK, width=4)
        map_label(img, L('BRAZIL · FROM THE 1720s', 'బ్రెజిల్ · 1720ల నుంచి'), bx + 150, by + 70, 36, INK, min(1, kb))
    ko = e_back(prog(t, c_bo, c_bo + .3))
    if ko > .01:
        r = 12 * min(1, ko); d.ellipse((ox - r, oy - r, ox + r, oy + r), fill=(120, 70, 30), outline=INK, width=3)
        map_label(img, L('BORNEO · A FEW', 'బోర్నియో · కొన్ని'), ox - 120, oy + 60, 32, INK, min(1, ko))
    chip(img, L("THE WORLD'S DIAMONDS · BEFORE THE 1720s", 'ప్రపంచ వజ్రాలు · 1720లకు ముందు'), W / 2, 400, 36, CREAM, INK, a=sm_((t - c_world) / .4))
    return zoom(img, 1 + .04 * sm_((t - c_world) / max(.1, s1 - c_world)))

def s_mine(t, s0, s1):
    img = cov('G12', t, s0, s1, (.42, .58), (.55, .55), 1.02, 1.22, 1.0); dust(img, t)
    kf = 1 - sm_((t - s0) / .5)
    if kf > 0: img = Image.blend(img, Image.new('RGB', (W, H), (214, 196, 150)), .8 * kf)
    c = AT('3.7', 'tens', 'పదుల') - .1; k = e_back(prog(t, c, c + .3))
    if k > .01:
        dark_panel(img, (110, 360, 970, 590), 26, int(215 * min(1, k)), AMBER + (255,))
        text(img, L('TENS OF THOUSANDS OF WORKERS', 'పదుల వేల మంది కూలీలు'), W / 2, 430, 44, AMBER, kind='head', a=min(1, k), maxw=800)
        text(img, L("CONTEMPORARY TRAVELLERS' ESTIMATE · 1620s", 'ఆనాటి యాత్రికుల అంచనా · 1620లు'), W / 2, 520, 30, CREAM, kind='monob', a=min(1, k), maxw=800)
    text(img, L('AI illustration · reconstruction', 'AI చిత్రం · పునఃసృష్టి'), W / 2, 1690, 22, CREAM, kind='mono')
    return img

@functools.lru_cache(1)
def PLATE():
    im = Image.open(FL.A['PD02']).convert('RGB'); s_ = (W - 80) / im.width; return im.resize((W - 80, int(im.height * s_)), Image.LANCZOS)
def s_tavernier(t, s0, s1):
    img = Image.new('RGB', (W, H), (16, 14, 12)); p = PLATE(); z = 1 + .05 * sm_((t - s0) / max(.1, s1 - s0)); pz = p.resize((int(p.width * z), int(p.height * z)), Image.BILINEAR)
    py = 700; img.paste(pz, (int(W / 2 - pz.width / 2), int(py - pz.height / 2))); img = grade(img, 1.0)
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); k0 = sm_((t - s0) / .5)
    d.rectangle((W / 2 - pz.width / 2 - 6, py - pz.height / 2 - 6, W / 2 + pz.width / 2 + 6, py + pz.height / 2 + 6), outline=AMBER + (int(255 * k0),), width=5); img.paste(lay, (0, 0), lay)
    chip(img, L("TAVERNIER'S PLATE OF INDIAN DIAMONDS · 1703 ED.", 'Tavernier గీయించిన భారత వజ్రాలు · 1703'), W / 2, 330, 32, CREAM, INK, a=k0)
    c_b = AT('3.7', 'blue', 'నీలి') - .1; c_p = AT('3.7', 'possibly', 'బహుశా') - .1; c_h = AT('3.7', 'Hope', 'Hope') - .1
    kb = sm_((t - c_b) / .6)
    if kb > 0:
        thread_line(img, [(W / 2, py + pz.height / 2 + 6), (W / 2 - 60, 1120), (W / 2, 1200)], kb, DBLUE, 6)
        dark_panel(img, (130, 1200, 950, 1330), 24, int(225 * kb), DBLUE + (255,))
        text(img, L('A BLUE DIAMOND · BOUGHT IN INDIA', 'ఒక నీలి వజ్రం · భారత్‌లో కొన్నది'), W / 2, 1265, 38, CREAM, kind='head', a=kb, maxw=780)
    kh = e_back(prog(t, c_h, c_h + .3))
    if kh > .01: chip(img, L('→ LATER, THE HOPE DIAMOND', '→ తర్వాత Hope diamond'), W / 2, 1150, 38, DBLUE, CREAM, a=min(1, kh), scale=min(1, kh))
    kp = e_back(prog(t, c_p, c_p + .3))
    if kp > .01: chip(img, L('EXACT MINE UNCERTAIN', 'ఏ గనో ఖచ్చితంగా తెలియదు'), W / 2, 1570, 36, AMBER, INK, a=min(1, kp), scale=min(1, kp))
    text(img, 'J.-B. Tavernier, Les Six Voyages (1703 ed.) · public domain', W / 2, 1690, 22, GREY, kind='mono')
    return img

def s_kohinoor(t, s0, s1):
    M = amap(72.0, 86.0, 16.6); img = Image.blend(M.base, Image.new('RGB', (W, H), (10, 9, 8)), .72); v = t - s0
    for i, (lo, la) in enumerate(((80.0, 16.7), (77.2, 15.2), (79.4, 18.6))):
        x, y = M.P(lo, la); k = sm_((v - .2 - i * .35) / .4); text(img, '?', x + 14 * math.sin(t * 1.3 + i), y + 10 * math.cos(t + i), 110, AMBER, 'mm', 'head', .85 * k)
    dark_panel(img, (110, 1010, 970, 1250), 28, 225, AMBER + (255,))
    t1 = 'KOH-I-NOOR' if not TE else 'కోహినూర్'; t2 = L('MINE OF ORIGIN · DEBATED', 'ఏ గని? · ఇప్పటికీ చర్చే')
    text(img, t1[:max(1, int(len(t1) * clamp(v / .6)))], W / 2, 1090, 70, AMBER, kind='head')
    n2 = int(len(t2) * clamp((v - .6) / 1.0))
    if n2: text(img, t2[:n2], W / 2, 1185, 36, CREAM, kind='monob', maxw=800)
    return img

EXTENT = [(77.3, 19.5), (80.5, 19.3), (83.5, 18.3), (82.3, 16.6), (81.2, 16.0), (80.2, 15.0), (80.1, 13.8), (78.6, 14.0), (77.3, 15.5), (77.0, 17.5)]
def s_golconda(t, s0, s1):
    c_map = AT('3.2', 'Their', 'వాళ్ల') - 0.9
    if t < c_map:
        img = cov('CC01', t, s0, c_map, (.55, .5), (.62, .48), 1.0, 1.18, .95)
        c = AT('3.2', 'Qutb', 'కుతుబ్‌షాహీ') - .1; k = e_back(prog(t, c, c + .3))
        chip(img, L('GOLCONDA · c. 1680', 'గోల్కొండ · సుమారు 1680'), W / 2, 400, 42, CREAM, INK, a=sm_((t - s0) / .4))
        if k > .01: chip(img, L('QUTB SHAHI KINGS', 'కుతుబ్‌షాహీ రాజులు'), W / 2, 500, 42, AMBER, INK, a=min(1, k), scale=min(1, k))
        text(img, 'Golconda Fort · Amit Kumar Sahoo · CC BY-SA 4.0', W / 2, 1690, 22, CREAM, kind='mono')
        return img
    M = amap(72.0, 86.0, 16.6); img = M.base.copy(); v = t - c_map
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ke = sm_(v / .7); ImageDraw.Draw(lay).polygon([M.P(*p) for p in EXTENT], fill=AMBER + (int(95 * ke),), outline=(150, 96, 20, int(230 * ke)))
    lay = lay.filter(ImageFilter.GaussianBlur(6)); img.paste(lay, (0, 0), lay)
    map_label(img, L('GOLCONDA KINGDOM · APPROXIMATE EXTENT', 'గోల్కొండ రాజ్యం · సుమారు విస్తీర్ణం'), W / 2, M.P(80, 20.6)[1], 32, INK, ke)
    gx, gy = M.P(*GOLC); d = ImageDraw.Draw(img); d.ellipse((gx - 12, gy - 12, gx + 12, gy + 12), fill=INK)
    map_label(img, L('GOLCONDA', 'గోల్కొండ'), gx - 30, gy - 60, 40, INK, 1.0)
    c_g = AT('3.2', 'Their', 'వాళ్ల'); kt = sm_((t - c_g + .2) / max(1.2, s1 - c_g - .4))
    route = [M.P(*GOLC), M.P(79.3, 16.57), M.P(80.05, 16.75), M.P(80.62, 16.51), M.P(*MTM)]; head = thread_line(img, route, kt, AMBER, 8)
    b = BALE(); bi = b.resize((130, int(b.height * 130 / b.width)), Image.LANCZOS)
    if kt > 0: paste_c(img, bi, head[0], head[1] - 36, 1.0)
    c_m = AT('3.2', 'Machilipatnam', 'మచిలీపట్నం') - .1; km = e_back(prog(t, c_m, c_m + .3))
    if km > .01:
        mx, my = M.P(*MTM); d = ImageDraw.Draw(img); r = 18 * min(1, km); d.ellipse((mx - r, my - r, mx + r, my + r), fill=AMBER, outline=INK, width=4)
        map_label(img, L('MACHILIPATNAM · THE SEA GATE', 'మచిలీపట్నం · సముద్ర ద్వారం'), W / 2 + 40, my + 90, 40, INK, min(1, km))
    return zoom(img, 1 + .06 * sm_(v / max(.1, s1 - c_map)), cy=.42)

def s_b3(t, s0, s1):
    c_w = AT('B3', 'woven', 'అది') - .15
    if t < c_w:
        img = cov('G12', t, s0, c_w, (.5, .55), (.52, .55), 1.1, 1.2, lerp(.95, .45, sm_((t - s0) / max(.1, c_w - s0)))); dust(img, t, 30, .35)
        chip(img, L('NOT ONLY IN THE MINES', 'గనుల్లో మాత్రమే కాదు'), W / 2, 400, 40, CREAM, INK, a=sm_((t - s0) / .4)); return img
    img = cov('T6', t, c_w, s1, (.52, .5), (.48, .5), 1.0, 1.14, 1.0); u = sm_((t - c_w) / max(.6, s1 - c_w - .3))
    head = thread_line(img, [(430, 1010), (560, 1090), (700, 1120), (800, 1180)], u, AMBER, 8)
    if u > .85: bale_at(img, 820, 1230, 300, sm_((u - .85) / .15))
    chip(img, L('A MAJOR EXPORT · NOT THE ONLY WEALTH', 'ప్రధాన ఎగుమతి · ఏకైక సంపద కాదు'), W / 2, 400, 38, AMBER, INK, a=sm_((t - c_w) / .4))
    return img

def s_tease(t, s0, s1):
    """the payment: FOREIGN BUYER -> BROKER -> WEAVER; a cut stays at each hand (no amounts)"""
    img = cov('G14', t, s0, s1, (.34, .5), (.40, .5), 1.0, 1.12, .50); v = t - s0; d = ImageDraw.Draw(img)
    nodes = [(190, L('FOREIGN BUYER', 'విదేశీ కొనుగోలుదారు')), (540, L('BROKER', 'దళారి')), (890, L('WEAVER', 'నేతగాడు'))]; y = 760
    for i, (x, lab) in enumerate(nodes):
        k = sm_((v - i * .15) / .3); r = 62 * k; d.ellipse((x - r, y - r, x + r, y + r), fill=(20, 18, 16), outline=AMBER, width=5)
        f = pick(lab, 'monob', 28); ws = wrap(lab, 'monob', 28, 300)
        for j, ln in enumerate(ws): text(img, ln, x, y + 100 + j * 34, 28, CREAM, kind='monob', a=k)
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dl = ImageDraw.Draw(lay)
    for leg, (xa, xb, n, t0) in enumerate(((190, 540, 7, .35), (540, 890, 4, 1.45))):
        for i in range(n):
            u = sm_((v - t0 - i * .07) / .8)
            if u <= 0: continue
            x = lerp(xa, xb, u); yy = y - 150 * math.sin(math.pi * u) - 4 * i; SP.coin(dl, x, yy, 17)
    for leg, (x, n, t0) in enumerate(((540, 3, 1.25), (890, 0, 9))):   # coins that stay: the cut
        for i in range(n):
            u = sm_((v - t0 - i * .1) / .5)
            if u > 0: SP.coin(dl, x - 34 + i * 34, lerp(y - 20, y - 150, u), 17)
    img.paste(lay, (0, 0), lay)
    c_cut = AT('T', 'cut', 'వాటా') - .1; kc = e_back(prog(t, c_cut, c_cut + .3))
    if kc > .01: chip(img, L('A CUT STAYS AT EVERY HAND', 'ప్రతి చేతిలో ఒక వాటా'), W / 2, 500, 40, AMBER, INK, a=min(1, kc), scale=min(1, kc))
    c_who = AT('T', 'Who', 'సంపద') - .1; kw = e_back(prog(t, c_who, c_who + .3))
    if kw > .01:
        dark_panel(img, (90, 1130, 990, 1290), 28, int(230 * min(1, kw)), AMBER + (255,))
        text(img, L('WHO CONTROLLED THE WEALTH?', 'సంపద అసలు ఎవరి చేతిలో?'), W / 2, 1210, 50, AMBER, kind='head', a=min(1, kw), maxw=840)
    text(img, L('ILLUSTRATIVE · NO AMOUNTS IMPLIED', 'ఉదాహరణ · మొత్తాలు సూచించడం లేదు'), W / 2, 1690, 24, CREAM, kind='monob')
    return img

ZOOM = ('cartoon1', 'cartoon2', 'cartoon3', 'slide', 'tavernier', 'kohinoor', 'tease')
def render(t):
    scn, s0, s1 = scene_at(t)
    if scn == 'loop':
        img = s_loop(t, s0, s1); captions(img, t, 'loop'); return img
    if scn.startswith('cartoon'):
        q = {'cartoon1': 'Q1', 'cartoon2': 'Q2', 'cartoon3': 'Q3'}[scn]; img = cartoon(t, s0, [('CHELLI', q)])
    elif scn == 'slide': img = s_slide(t, s0, s1)
    else: img = globals()['s_' + scn](t, s0, s1)
    img = img.convert('RGB')
    if scn in ZOOM: img = zoom(img, 1 + 0.04 * e_io(prog(t, s0, s1)))
    overlays(img, t, scn); captions(img, t, scn); return img
