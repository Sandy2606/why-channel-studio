
# ------------------------------------------------------------------ GS 3/6 scenes (previews: hook, payoff, ships, port)
import cv2, fx as FX, sprites as SP
ACC = AMBER; DBLUE = (60, 110, 190)
def sm_(x): x = clamp(x); return x * x * (3 - 2 * x)

# ---- aged map (real geography via gsmap, Mercator)
class AMap:
    def __init__(self, lon0, lon1, latc):
        self.s = W / ((lon1 - lon0) * gsmap.AX); self.x0 = gsmap.to_svg(lon0, 0)[0]; self.yc = gsmap.to_svg(0, latc)[1]
        self.base = self._render()
    def P(self, lon, lat):
        x, y = gsmap.to_svg(lon, lat); return ((x - self.x0) * self.s, H / 2 + (y - self.yc) * self.s)
    def _tr(self, q): return [((x - self.x0) * self.s, H / 2 + (y - self.yc) * self.s) for x, y in q]
    def _render(self):
        SS = 2; im = Image.new('RGB', (W * SS, H * SS), (176, 186, 178)); d = ImageDraw.Draw(im)
        names = [f['properties']['name'] for f in gsmap.GEO['features'] if f['properties']['name'] != 'India']
        for n in names:
            for q in gsmap.polys(n):
                if len(q) > 2:
                    p = [(x * SS, y * SS) for x, y in self._tr(q)]
                    if max(x for x, y in p) < 0 or min(x for x, y in p) > W * SS: continue
                    d.polygon(p, fill=(206, 190, 152), outline=(150, 128, 92))
        for q in gsmap.india_polys():
            if len(q) > 2: d.polygon([(x * SS, y * SS) for x, y in self._tr([tuple(z) for z in q])], fill=(222, 200, 150))
        for n in ('Pakistan', 'Bangladesh'):
            for q in gsmap.polys(n):
                if len(q) > 2: d.polygon([(x * SS, y * SS) for x, y in self._tr(q)], fill=(222, 200, 150))
        im = im.resize((W, H), Image.LANCZOS); a = np.asarray(im).astype(np.float32)
        rng = np.random.default_rng(3); n = cv2.GaussianBlur(cv2.resize(rng.random((12, 7)).astype(np.float32), (W, H), interpolation=cv2.INTER_CUBIC), (0, 0), 60)[..., None]
        a = a * (0.95 + 0.08 * n) * VIG() * 1.02 * np.array([1.0, .96, .86])
        return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))

@functools.lru_cache(4)
def amap(lon0, lon1, latc): return AMap(lon0, lon1, latc)
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
    """restrained moving light: a narrow diagonal band lifts only the bright facets"""
    a = DIAMOND().astype(np.float32); Y, X = np.mgrid[0:H, 0:W].astype(np.float32)
    pos = ((t * 0.42) % 1.6 - 0.3) * (W + H); band = np.exp(-((X + Y * .6 - pos) ** 2) / (2 * 120.0 ** 2))
    lum = a.mean(2) / 255.0; a = a * (0.80 + 0.5 * band[..., None] * (lum[..., None] ** 1.5) * 2.2) * k
    im = Image.fromarray(np.clip(a * VIG(), 0, 255).astype(np.uint8))
    return zoom(im, z) if z > 1.001 else im

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
        return diamond_lit(0.0 if frame0 else t, 1.0, 1.0 + 0.04 * (0 if frame0 else t))
    M = amap(72.0, 86.0, 16.6); gx, gy = M.P(*GOLC)
    if t < c_but:
        u = sm_((t - c_pull) / 1.1); img = Image.blend(diamond_lit(t, 1.0, 1.0 + 0.04 * t), M.base, sm_((t - c_pull) / 0.7))
        d = ImageDraw.Draw(img); kr = sm_((t - c_pull - 0.5) / 1.4)
        pts = [M.P(*p) for p in KRISHNA]; n = max(2, int(len(pts) * kr) + 1)
        if kr > 0: d.line(pts[:n], fill=(70, 110, 150), width=6, joint='curve')
        dc = DIA_CUT(); sz = lerp(1.0, 0.15, u); paste_c(img, dc, lerp(W / 2, gx, u), lerp(H * .46, gy, u), 1.0, sz)
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
    # whole fleets: the harbour, pulling back; the small diamond stays in the corner for scale
    img = cov('G09', t, c_fleet, s1 + 0.4, (.74, .40), (.60, .46), 1.55, 1.0, 1.0, alive=lambda a_, tt: FX.water(a_, 'G09', tt))
    kd = sm_((t - c_fleet) / 0.5); paste_c(img, DIA_CUT(), 190, 560, kd, 0.20)
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(lay).ellipse((190 - 105, 560 - 105, 190 + 105, 560 + 105), outline=CREAM + (int(190 * kd),), width=4); img.paste(lay, (0, 0), lay)
    kl = e_back(prog(t, c_fleet + 0.9, c_fleet + 1.25))
    if kl > .01: chip(img, L('TEXTILES · A MAJOR EXPORT TRADE', 'గుడ్డ · ఒక ప్రధాన ఎగుమతి వ్యాపారం'), W / 2, 1210, 40, AMBER, INK, a=min(1, kl), scale=min(1, kl))
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
    if t < c_weave:
        img = cov('G10', t, c_loc, c_weave, (.42, .52), (.50, .50), 1.0, 1.22, 1.0)
        k = e_back(prog(t, c_loc + .2, c_loc + .5))
        if k > .01: chip(img, L('BROKERS & INTERPRETERS', 'దళారులు · దుబాసీలు'), W / 2, 400, 42, AMBER, INK, a=min(1, k), scale=min(1, k))
        return img
    # our bale is swung aboard
    img = cov('G21', t, c_weave, s1, (.44, .55), (.46, .45), 1.0, 1.12, 1.0, alive=lambda a_, tt: FX.water(FX.swing(a_, tt, (1140, 80), FX.G21_BALE, amp=1.3, period=2.6), 'G21', tt))
    k = e_back(prog(t, c_weave + .25, c_weave + .55))
    if k > .01: chip(img, L('FROM THE WEAVING VILLAGES · ABOARD', 'నేత గ్రామాల నుంచి · ఓడలోకి'), W / 2, 400, 38, AMBER, INK, a=min(1, k), scale=min(1, k))
    return img

def _todo(key):
    return lambda t, s0, s1: cov(key, t, s0, s1, (.5, .5), (.52, .5), 1.0, 1.1)
s_kollur = _todo('G12'); s_mine = _todo('G12'); s_tavernier = _todo('PD02'); s_kohinoor = _todo('CC01'); s_golconda = _todo('CC01'); s_b3 = _todo('G13'); s_tease = _todo('G14')

ZOOM = ('cartoon1', 'cartoon2', 'cartoon3')
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
