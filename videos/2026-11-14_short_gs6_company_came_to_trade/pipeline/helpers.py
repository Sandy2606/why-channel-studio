# ------------------------------------------------------------------ GS 6/6 scenes ("The company that came to trade") · shared helpers from GS 5/6
# Sharp-pictures rule: every source image is shown at <= 1.0 source px per output px; maps and graphics are drawn at output size.
ARC = '/home/claude/why-channel-studio/videos/2026-11-08_long_golden_sparrow_s1/visuals/archive/'
EV = '/home/claude/gs5/src/'
DUSK = (16, 16, 15); MUTED = (170, 164, 150); PARCH = (226, 210, 172); GOLD_A = (196, 160, 92)
def sm_(x): x = clamp(x); return x * x * (3 - 2 * x)

SRC = {'ROTEIRO': (ARC + '09_PD11_Roteiro_da_primeira_viagem_de_Vasco_da_Gama.jpg', None),
       'COIN': (ARC + '12_PD19_Gold_Aureus_of_Nerva_MANTIS.jpg', None),
       'BARROS': (EV + 'barros_p1.jpg', None)}
@functools.lru_cache(8)
def NAT(key):
    p, cr = SRC[key]; im = Image.open(p).convert('RGB')
    if cr: im = im.crop(cr)
    return im

def panel_nat(img, key, box, u, f0, f1, sc=1.0, radius=18, a=1.0, border=None, tint=None):
    """native-pixel window: a box-sized region of the source at scale sc (<= 1), panning f0 -> f1"""
    assert sc <= 1.0001, (key, sc)
    im = NAT(key); x0, y0, x1, y1 = [int(v) for v in box]; bw, bh = x1 - x0, y1 - y0; sw, sh = bw / sc, bh / sc
    sw, sh = min(sw, im.width), min(sh, im.height)    # rounding guard (never more than the source)
    k = e_io(clamp(u)); fx, fy = lerp(f0[0], f1[0], k), lerp(f0[1], f1[1], k)
    cx = min(max(fx * im.width, sw / 2), im.width - sw / 2); cy = min(max(fy * im.height, sh / 2), im.height - sh / 2)
    crop = im.resize((bw, bh), Image.LANCZOS, box=(cx - sw / 2, cy - sh / 2, cx + sw / 2, cy + sh / 2))
    if tint: crop = Image.fromarray(np.clip(np.asarray(crop).astype(np.float32) * np.array(tint) / 255, 0, 255).astype(np.uint8))
    shadow(img, box, a)
    if border:
        lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(lay).rounded_rectangle((x0 - 3, y0 - 3, x1 + 3, y1 + 3), radius + 3, fill=border + (int(255 * a),)); img.paste(lay, (0, 0), lay)
    m = Image.new('L', (bw, bh), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, bw - 1, bh - 1), radius, fill=int(255 * a))
    img.paste(crop, (x0, y0), m); LY.reg('image', (x0, y0, x1, y1), owner=key)

def shadow(img, box, a=1.0, r=22, o=12):
    if a <= .02: return
    x0, y0, x1, y1 = box; lay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(lay).rounded_rectangle((x0 + 4, y0 + o, x1 + 4, y1 + o), 18, fill=(0, 0, 0, int(150 * a)))
    lay = lay.filter(ImageFilter.GaussianBlur(r)); img.paste(lay, (0, 0), lay)

def _tel(s): return any('\u0c00' <= ch <= '\u0c7f' for ch in str(s))
def small(img, s, x, y, px=24, col=MUTED, anchor='mm', a=1.0, maxw=None):
    if _tel(s): px = int(px * 1.22)    # GS 6/6: Telugu glyphs read smaller than mono caps at the same px
    text(img, s, x, y, px, col, anchor, 'monob', a, maxw or ST.sw, None)

def rule_frame(d, box, a):
    x0, y0, x1, y1 = box; c1 = GOLD_A + (int(230 * a),); c2 = GOLD_A + (int(140 * a),)
    d.rectangle(box, outline=c1, width=2); d.rectangle((x0 + 9, y0 + 9, x1 - 9, y1 - 9), outline=c2, width=1)
    for cx, cy in ((x0, y0), (x1, y0), (x0, y1), (x1, y1)):
        d.polygon([(cx, cy - 9), (cx + 9, cy), (cx, cy + 9), (cx - 9, cy)], fill=GOLD_A + (int(255 * a),))

def plate(img, box, a=1.0, rule=True, fill=INK, alpha=222):
    if a <= .01: return
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); d.rectangle(box, fill=fill + (int(alpha * a),))
    if rule: rule_frame(d, box, a)
    img.paste(lay, (0, 0), lay)

def plate_text(img, box, kicker, title, a=1.0, px=44, owner=None, sub=None, tcol=CREAM, kcol=AMBER):
    """ink plate: kicker (mono, amber) + title (head, cream) + sub (mono, muted); registers box and ink"""
    if a <= .01: return
    if _tel(title): px = int(px * 1.08)
    plate(img, box, a); x0, y0, x1, y1 = box; inner = x1 - x0 - 70; cx = (x0 + x1) / 2
    lines = wrap(title, 'head', px, inner); f = pick(title, 'head', px); lh = px + 12
    kpx = 31 if not _tel(kicker) else 34; spx = 24 if not _tel(sub) else 29
    block = (kpx + 16 if kicker else 0) + len(lines) * lh + (spx + 18 if sub else 0); y = (y0 + y1) / 2 - block / 2
    if kicker: small(img, kicker, cx, y + kpx / 2, kpx, kcol, 'mm', a, inner); y += kpx + 16
    ink = None
    for ln in lines:
        yy = y + lh / 2; text(img, ln, cx, yy, px, tcol, 'mm', 'head', a, None, None)
        bb = f.getbbox(ln, anchor='mm'); r = (cx + bb[0], yy + bb[1], cx + bb[2], yy + bb[3]); y += lh
        ink = r if ink is None else (min(ink[0], r[0]), min(ink[1], r[1]), max(ink[2], r[2]), max(ink[3], r[3]))
    if sub: small(img, sub, cx, y + 8 + spx / 2, spx, MUTED, 'mm', a, inner)
    LY.reg('card', box, ink, owner=owner or title)

def map_label(img, s, x, y, px=28, col=INK, a=1.0, bg=(244, 236, 214)):
    if a <= .01: return
    f = pick(s, 'monob', px); w = f.getlength(s) + 26; x0 = min(max(x - w / 2, 48), W - 48 - w)
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(lay).rounded_rectangle((x0, y - px * .85, x0 + w, y + px * .85), 9, fill=bg + (int(232 * a),))
    img.paste(lay, (0, 0), lay); text(img, s, x0 + w / 2, y, px, col, 'mm', 'monob', a, None, None)
    LY.reg('label', (x0, y - px * .85, x0 + w, y + px * .85), owner=s)

def pin(img, x, y, k, col=AMBER, r=13, pulse=None):
    if k <= .01: return
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    if pulse is not None:
        pr = r + 34 * (pulse % 1.0); d.ellipse((x - pr, y - pr, x + pr, y + pr), outline=col + (int(170 * (1 - pulse % 1.0) * k),), width=3)
    rr = r * e_back(min(1, k)); d.ellipse((x - rr, y - rr, x + rr, y + rr), fill=col + (int(255 * min(1, k)),), outline=(20, 16, 10, int(255 * min(1, k))), width=3)
    img.paste(lay, (0, 0), lay)

# ------------------------------------------------------------------ the map (real coastlines, drawn at output size)
def _smooth(pts, n=10):
    """Catmull-Rom through the points (screen space)"""
    if len(pts) < 3: return pts
    P = [pts[0]] + pts + [pts[-1]]; out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for j in range(n):
            t = j / n; t2, t3 = t * t, t * t * t
            out.append(tuple(.5 * ((2 * p1[c]) + (-p0[c] + p2[c]) * t + (2 * p0[c] - 5 * p1[c] + 4 * p2[c] - p3[c]) * t2 + (-p0[c] + 3 * p1[c] - 3 * p2[c] + p3[c]) * t3) for c in (0, 1)))
    out.append(pts[-1]); return out

def poly_len(pts): return sum(math.dist(a, b) for a, b in zip(pts, pts[1:]))
def poly_at(pts, f):
    """point and direction at fraction f of the polyline length"""
    tot = poly_len(pts) * clamp(f)
    for a, b in zip(pts, pts[1:]):
        s = math.dist(a, b)
        if tot <= s or b == pts[-1]:
            q = 0 if s == 0 else min(1, tot / s); return (lerp(a[0], b[0], q), lerp(a[1], b[1], q)), math.atan2(b[1] - a[1], b[0] - a[0])
        tot -= s
    return pts[-1], 0.0
def poly_part(pts, k):
    if k <= 0: return []
    tot = poly_len(pts) * min(1, k); out = [pts[0]]
    for a, b in zip(pts, pts[1:]):
        s = math.dist(a, b)
        if tot <= 0: break
        q = min(1, tot / s) if s else 1; out.append((lerp(a[0], b[0], q), lerp(a[1], b[1], q))); tot -= s
    return out

class OMap:
    """Indian Ocean map at output size: all coastlines, muted sea/land; land mask for the wind field"""
    def __init__(self, lon0, lon1, latc):
        self.s = W / ((lon1 - lon0) * gsmap.AX); self.x0 = gsmap.to_svg(lon0, 0)[0]; self.yc = gsmap.to_svg(0, latc)[1]
        SS = 2; im = Image.new('RGB', (W * SS, H * SS), (108, 128, 130)); d = ImageDraw.Draw(im); lm = Image.new('L', (W * SS, H * SS), 0); dl = ImageDraw.Draw(lm)
        for f in gsmap.GEO['features']:
            for q in gsmap.polys(f['properties']['name']):
                if len(q) > 2:
                    pts = [(x * SS, y * SS) for x, y in self._tr(q)]; d.polygon(pts, fill=(170, 156, 124), outline=(128, 114, 88)); dl.polygon(pts, fill=255)
        im = im.resize((W, H), Image.LANCZOS); a = np.asarray(im).astype(np.float32)
        yy, xx = np.mgrid[0:H, 0:W]; r = np.sqrt(((xx - W / 2) / (W * .8)) ** 2 + ((yy - H * .48) / (H * .62)) ** 2); a *= np.clip(1.12 - .5 * r, .4, 1)[..., None]
        self.base = Image.fromarray(np.clip(a * .9, 0, 255).astype(np.uint8)); self.land = np.asarray(lm.resize((W, H), Image.BILINEAR)) > 100
    def _tr(self, q): return [((x - self.x0) * self.s, H / 2 + (y - self.yc) * self.s) for x, y in q]
    def P(self, lon, lat):
        x, y = gsmap.to_svg(lon, lat); return ((x - self.x0) * self.s, H / 2 + (y - self.yc) * self.s)
    def path(self, ll, n=10): return _smooth([self.P(*p) for p in ll], n)

MAP_A = (34.0, 102.0, 5.0)      # the whole ocean
MAP_B = (34.0, 90.0, 7.0)        # Malindi -> Calicut -> Gujarat
@functools.lru_cache(64)
def OM(lon0, lon1, latc): return OMap(lon0, lon1, latc)
def om_lerp(k, steps=24):
    q = round(clamp(k) * steps) / steps
    return OM(*(round(lerp(a, b, q), 3) for a, b in zip(MAP_A, MAP_B)))

# trade routes (lon, lat) – illustrative examples of documented routes c. 1400–1500; drawn over water
ROUTES = {
 'INDIAN':  [[(72.5, 21.6), (70.6, 17.5), (73.2, 9.5), (77.5, 5.6), (82.0, 5.4), (92.0, 6.2), (98.0, 4.6), (102.2, 2.2)],
             [(75.7, 11.2), (66.0, 12.6), (55.0, 13.2), (45.3, 12.3)], [(72.5, 21.6), (66.5, 22.6), (60.0, 24.2), (56.6, 26.4)]],
 'ARAB':    [[(45.0, 12.6), (52.0, 11.5), (62.0, 10.5), (70.0, 10.8), (75.6, 11.2)], [(45.0, 12.6), (49.0, 10.8), (51.5, 7.0), (47.0, 1.0), (41.5, -2.6)],
             [(39.2, 21.4), (41.0, 17.0), (43.3, 12.9), (45.0, 12.6)]],
 'PERSIAN': [[(56.5, 26.5), (58.5, 24.0), (62.0, 22.6), (66.6, 21.6), (70.4, 20.6), (72.4, 21.4)], [(56.5, 26.5), (59.5, 22.5), (64.0, 17.0), (70.5, 12.6), (75.6, 11.3)]],
 'AFRICAN': [[(39.6, -8.8), (40.1, -6.2), (39.9, -4.2), (40.3, -3.0), (42.5, -0.4), (45.5, 2.0), (49.6, 7.6), (51.6, 11.4), (46.0, 12.4)]],
 'CHINESE': [[(110.0, 9.0), (106.5, 5.5), (104.5, 2.5), (102.3, 2.3)], [(102.0, 2.3), (97.0, 5.6), (88.0, 6.0), (80.6, 5.6), (77.2, 7.4), (75.7, 11.2)]],
 'MALAY':   [[(102.2, 2.1), (104.0, -1.0), (106.5, -4.5)], [(102.0, 2.4), (96.0, 6.6), (86.0, 8.6), (81.5, 7.0)]],
}
RCOL = {'INDIAN': (222, 178, 96), 'ARAB': (188, 128, 92), 'PERSIAN': (124, 156, 176), 'AFRICAN': (176, 140, 92), 'CHINESE': (196, 132, 110), 'MALAY': (128, 160, 112)}
RLAB = {'INDIAN': (L('INDIAN', 'భారతీయులు'), (78.5, 19.5)), 'ARAB': (L('ARAB', 'అరబ్బులు'), (46.5, 19.0)), 'PERSIAN': (L('PERSIAN', 'పర్షియన్లు'), (58.0, 31.0)),
        'AFRICAN': (L('AFRICAN', 'ఆఫ్రికన్లు'), (35.0, -1.0)), 'CHINESE': (L('CHINESE', 'చైనీయులు'), (100.5, 15.5)), 'MALAY': (L('MALAY', 'మలయా'), (98.5, -4.6))}
RWORD = {'INDIAN': ('Indian,', 'భారతీయులు,'), 'ARAB': ('Arab,', 'అరబ్బులు,'), 'PERSIAN': ('Persian,', 'పర్షియన్లు,'),
         'AFRICAN': ('African,', 'ఆఫ్రికన్లు,'), 'CHINESE': ('Chinese', 'చైనీయులు,'), 'MALAY': ('Malay', 'మలయా')}
PORTS = {'MALINDI': (40.12, -3.22), 'CALICUT': (75.78, 11.25), 'MALACCA': (102.25, 2.19), 'GUJARAT': (72.4, 22.2), 'PHANIGIRI': (79.53, 17.29)}
PNAME = {'MALINDI': L('MALINDI', 'మాలిండి'), 'CALICUT': L('CALICUT', 'కాలికట్'), 'MALACCA': L('MALACCA', 'మలక్కా'), 'GUJARAT': L('GUJARAT', 'గుజరాత్'), 'PHANIGIRI': L('PHANIGIRI', 'ఫణిగిరి')}

def draw_routes(img, m, t, lit, glow_k=None, thick=None, alpha=1.0, dots=True):
    """lit: {group: 0..1 draw-on}. Moving lantern dots show traffic on every lit route."""
    lay = Image.new('RGBA', (W * 2, H * 2), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    dots = []
    for g, segs in ROUTES.items():
        k = lit.get(g, 0)
        if k <= .01: continue
        col = RCOL[g]; wd = (thick or {}).get(g, 4)
        for si, seg in enumerate(segs):
            pts = m.path(seg); part = poly_part(pts, k)
            if len(part) > 1: d.line([(x * 2, y * 2) for x, y in part], fill=col + (int(225 * alpha),), width=wd * 2, joint='curve')
            if k >= .999 and dots:
                L_ = poly_len(pts); n = max(1, int(L_ / 170))
                for j in range(n):
                    f = ((t * 46 / max(L_, 1)) + j / n + si * .37) % 1.0
                    if si % 2: f = 1 - f
                    (x, y), _ = poly_at(pts, f); dots.append((x, y, col))
    for x, y, col in dots:
        d.ellipse((x * 2 - 9, y * 2 - 9, x * 2 + 9, y * 2 + 9), fill=(250, 238, 210, int(235 * alpha)), outline=col + (int(255 * alpha),), width=3)
    lay = lay.resize((W, H), Image.LANCZOS)
    g_ = lay.filter(ImageFilter.GaussianBlur(5)); img.paste(g_, (0, 0), g_); img.paste(lay, (0, 0), lay)

def time_rail(img, k_in, k_fill, k_end, y=372):
    """1st c. CE (Roman coins in India) ... 1498 (da Gama): da Gama arrives last"""
    if k_in <= .01: return
    box = (70, y - 64, W - 70, y + 70); plate(img, box, k_in, alpha=210)
    x0, x1 = 150, W - 150; lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.line((x0, y + 4, x1, y + 4), fill=(110, 100, 80, int(255 * k_in)), width=4)
    xf = lerp(x0, x1, e_io(k_fill)); d.line((x0, y + 4, xf, y + 4), fill=GOLD_A + (int(255 * k_in),), width=6)
    d.ellipse((x0 - 10, y - 6, x0 + 10, y + 14), fill=GOLD_A + (int(255 * k_in),))
    img.paste(lay, (0, 0), lay)
    small(img, L('1st c. CE · ROMAN COINS IN INDIA', 'క్రీ.శ. 1వ శతాబ్దం · భారత్‌లో రోమన్ నాణేలు'), x0 - 30, y - 32, 27 if not TE else 28, PARCH, 'lm', k_in, 600)
    small(img, L('CENTURIES OF TRADE', 'శతాబ్దాల వ్యాపారం'), W / 2, y + 40, 25 if not TE else 26, MUTED, 'mm', k_in * clamp(k_fill * 2))
    if k_end > .01:
        pin(img, x1, y + 4, k_end, AMBER, 12)
        small(img, L('1498 · DA GAMA', '1498 · డ గామా'), x1 + 30, y + 40, 28 if not TE else 28, AMBER, 'rm', k_end, 400)
    LY.reg('card', box, owner='time rail')

def wind(img, m, t, dirk, strength=1.0, n=700, seed=3, col=(236, 230, 214)):
    """wind streaks over the sea; dirk = +1 south-west monsoon (blows towards the NE), -1 north-east monsoon"""
    if strength <= .01: return
    n = int(n * .6); rng = np.random.default_rng(seed); xs = rng.uniform(0, W, n); ys = rng.uniform(600, 1560, n); ph = rng.uniform(0, 1, n); sp = rng.uniform(.6, 1.2, n)
    vx, vy = .77, -.64
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    pos = t * 70
    for i in range(n):
        f = (ph[i] + t * .35 * sp[i]) % 1.0; life = math.sin(math.pi * f)
        x = (xs[i] + dirk * vx * (pos * sp[i] + 90 * f)) % W; y = 600 + ((ys[i] - 600 + dirk * vy * (pos * sp[i] + 90 * f)) % 960)
        xi, yi = int(x), int(y)
        if m.land[min(H - 1, yi), min(W - 1, xi)]: continue
        ln = 26 * sp[i] * abs(dirk) + 4
        d.line((x - dirk * vx * ln * 1.6, y - dirk * vy * ln * 1.6, x, y), fill=col + (int(118 * life * strength),), width=3)
    img.paste(lay, (0, 0), lay)

def dhow(img, x, y, ang, k=1.0, s=1.0):
    """small lateen-sail ship icon in ink with a cream sail"""
    if k <= .01: return
    sz = 64 * s; lay = Image.new('RGBA', (int(sz * 2), int(sz * 2)), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); c = sz
    d.polygon([(c - sz * .55, c + sz * .18), (c + sz * .6, c + sz * .18), (c + sz * .38, c + sz * .42), (c - sz * .38, c + sz * .42)], fill=(30, 24, 18, int(255 * k)))
    d.line((c - sz * .05, c + sz * .2, c + sz * .02, c - sz * .62), fill=(30, 24, 18, int(255 * k)), width=4)
    d.polygon([(c + sz * .02, c - sz * .62), (c + sz * .52, c + sz * .12), (c - sz * .42, c + sz * .12)], fill=(244, 236, 214, int(255 * k)), outline=(30, 24, 18, int(255 * k)))
    if math.cos(ang) < 0: lay = lay.transpose(Image.FLIP_LEFT_RIGHT)
    img.paste(lay, (int(x - c), int(y - c)), lay)


def dhow(img, x, y, ang, k=1.0, s=1.0):
    """small lateen-sail ship icon in ink with a cream sail"""
    if k <= .01: return
    sz = 64 * s; lay = Image.new('RGBA', (int(sz * 2), int(sz * 2)), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); c = sz
    d.polygon([(c - sz * .55, c + sz * .18), (c + sz * .6, c + sz * .18), (c + sz * .38, c + sz * .42), (c - sz * .38, c + sz * .42)], fill=(30, 24, 18, int(255 * k)))
    d.line((c - sz * .05, c + sz * .2, c + sz * .02, c - sz * .62), fill=(30, 24, 18, int(255 * k)), width=4)
    d.polygon([(c + sz * .02, c - sz * .62), (c + sz * .52, c + sz * .12), (c - sz * .42, c + sz * .12)], fill=(244, 236, 214, int(255 * k)), outline=(30, 24, 18, int(255 * k)))
    if math.cos(ang) < 0: lay = lay.transpose(Image.FLIP_LEFT_RIGHT)
    img.paste(lay, (int(x - c), int(y - c)), lay)

