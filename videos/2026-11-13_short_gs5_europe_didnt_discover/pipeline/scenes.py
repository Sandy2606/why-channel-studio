# ------------------------------------------------------------------ GS 5/6 scenes ("Europe didn't discover India")
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

def small(img, s, x, y, px=24, col=MUTED, anchor='mm', a=1.0, maxw=None):
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
    plate(img, box, a); x0, y0, x1, y1 = box; inner = x1 - x0 - 70; cx = (x0 + x1) / 2
    lines = wrap(title, 'head', px, inner); f = pick(title, 'head', px); lh = px + 12
    kpx = 24 if not TE else 27; spx = 22 if not TE else 24
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

# ------------------------------------------------------------------ PREVIEW A: the busy ocean (53A + 5.3b [+ TE 5.4]) and the monsoon (5.5)
def ocean_lit(t):
    lit = {}
    for g, (en, te) in RWORD.items():
        c = AT('53A', en, te) - .12; lit[g] = e_io(prog(t, c, c + 1.1))
    return lit

def s_ocean(t, s0, s1):
    m = OM(*MAP_A); img = m.base.copy()
    lit = ocean_lit(t); thick = {}
    c_long = AT('53A', 'long', 'ఎంతో') - .1; c_arr = AT('53A', 'arrived.', 'రాకముందే', end=True) - (.2 if not TE else 0)
    c_mal = S('5.3b') - .05
    # INDIAN route to Malacca thickens once Malacca is named
    km = e_io(prog(t, c_mal + .2, c_mal + 1.0))
    if km > 0: thick['INDIAN'] = int(4 + 4 * km)
    draw_routes(img, m, t, lit, thick=thick)
    for g, (lab, ll) in RLAB.items():
        k = e_out(prog(t, AT('53A', *RWORD[g]) - .05, AT('53A', *RWORD[g]) + .45))
        k54 = (1 - e_io(prog(t, S('5.4') - .2, S('5.4') + .3))) if TE and has('5.4') else 1   # labels step aside for the coin
        if k > .01 and k54 > .01: x, y = m.P(*ll); map_label(img, lab, x, y, 30 if not TE else 30, INK, k * k54 * (1 - .35 * km if g != 'INDIAN' else 1), bg=(244, 236, 214))
    # the time rail: Roman trade ... 1498, da Gama arrives last
    k_in = e_out(prog(t, s0 + .1, s0 + .7))
    if TE: k_fill = prog(t, s0 + .4, c_arr + .6); k_end = e_out(prog(t, s0 + .3, s0 + .9))
    else: k_fill = prog(t, c_long, c_arr); k_end = e_out(prog(t, c_arr - .1, c_arr + .4))
    k_out = 1 - e_io(prog(t, c_mal, c_mal + .6))
    time_rail(img, k_in * k_out, k_fill, k_end * k_out)
    # Malacca: the Gujarati merchants (museum label tied to the pin)
    if km > 0:
        x, y = m.P(*PORTS['MALACCA']); pin(img, x, y, km, AMBER, 13, pulse=(t - c_mal) * .8)
        map_label(img, PNAME['MALACCA'], x - 40, y - 52, 26 if not TE else 28, INK, km)
        box = (90, 1150, W - 90, 1330); k2 = e_out(prog(t, c_mal + .5, c_mal + 1.1)) * (1 - (e_io(prog(t, S('5.4') - .2, S('5.4') + .3)) if TE and has('5.4') else 0))
        lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); d.line((x, y + 16, x - 40, 1150), fill=GOLD_A + (int(220 * k2),), width=2); img.paste(lay, (0, 0), lay)
        plate_text(img, box, L('TOMÉ PIRES · SUMA ORIENTAL · c. 1515', 'టోమే పిరెస్ · సుమా ఓరియెంటల్ · c. 1515'),
                   L('GUJARATI MERCHANTS: AMONG THE BIGGEST AT MALACCA', 'మలక్కాలో అతిపెద్ద వ్యాపారుల్లో గుజరాతీలు'), k2, 40 if not TE else 40, owner='pires')
    small(img, L('PORTS AND ROUTES SHOWN ARE EXAMPLES · c. 1400–1500', 'చూపిన రేవులు, మార్గాలు ఉదాహరణలు · c. 1400–1500'), W / 2, 1360, 22 if not TE else 24, (226, 220, 204), 'mm', e_out(prog(t, s0 + .6, s0 + 1.2)) * (1 - km))
    if TE and has('5.4') and t >= S('5.4') - .1: s_coin(img, m, t)
    return img

def s_coin(img, m, t):
    """TE 5.4: our coast traded long before; a Roman gold coin found at Phanigiri (the coin shown is an illustrative example)"""
    c0 = S('5.4') - .1; c_coin = AT('5.4', 'తెలుగు', 'తెలుగు') - .15
    k = e_out(prog(t, c0, c0 + .6))
    # India's coastline glows (the Malacca label leaves)
    x, y = m.P(*PORTS['PHANIGIRI']); kp = e_out(prog(t, c_coin, c_coin + .5))
    pin(img, x, y, kp, AMBER, 12, pulse=(t - c_coin) * .8 if kp > 0 else None)
    if kp > 0: map_label(img, PNAME['PHANIGIRI'] + ' · తెలంగాణ', x + 10, y - 50, 26, INK, kp)
    kc = e_out(prog(t, c_coin + .35, c_coin + 1.0))
    if kc <= .01: return
    box = (70, 1040, W - 70, 1340); plate(img, box, kc, alpha=230)
    # coin photo: native pixels at 0.18 (1747 px -> 314 px), clearly marked as an illustrative example
    panel_nat(img, 'COIN', (100, 1066, 100 + 250, 1066 + 250), 1.0, (.5, .5), (.5, .5), sc=250 / 1747 * 1.0, radius=125, a=kc)
    tx_ = 385; text(img, 'రోమన్ బంగారు నాణెం', tx_, 1105, 44, CREAM, 'lm', 'head', kc, W - 120 - tx_, None)
    small(img, 'క్రీ.శ. 1వ శతాబ్దం · ఫణిగిరిలో దొరికింది', tx_, 1168, 28, AMBER, 'lm', kc, W - 120 - tx_)
    small(img, 'చిత్రం: ఉదాహరణ మాత్రమే', tx_, 1228, 27, PARCH, 'lm', kc, W - 120 - tx_)
    small(img, 'ఫణిగిరి నాణెం కాదు · ANS (MANTIS) · CC0', tx_, 1272, 23, MUTED, 'lm', kc, W - 120 - tx_)
    LY.reg('card', box, owner='coin')

WIND_AT = [(61.0, 15.0), (66.5, 5.5), (87.5, 13.0), (79.0, 2.0)]
def wind_arrow(img, x, y, ang, k, s=1.0, phase=0.0):
    """a large, readable wind arrow (cream with an ink edge); it drifts along its own direction"""
    if k <= .01: return
    L_, Wd, Hd = 150 * s, 30 * s, 64 * s; dx, dy = math.cos(ang), math.sin(ang)
    off = (phase % 1.0) * 26 * s - 13 * s; cx, cy = x + dx * off, y + dy * off
    def P(u, v): return (cx + dx * u - dy * v, cy + dy * u + dx * v)
    pts = [P(-L_ / 2, -Wd / 2), P(L_ / 2 - Hd, -Wd / 2), P(L_ / 2 - Hd, -Hd / 2), P(L_ / 2, 0), P(L_ / 2 - Hd, Hd / 2), P(L_ / 2 - Hd, Wd / 2), P(-L_ / 2, Wd / 2)]
    lay = Image.new('RGBA', (W * 2, H * 2), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.polygon([(a * 2, b * 2) for a, b in pts], fill=(244, 236, 214, int(240 * k)), outline=(20, 18, 14, int(255 * k)), width=6)
    lay = lay.resize((W, H), Image.LANCZOS); sh = lay.filter(ImageFilter.GaussianBlur(6)); img.paste(sh, (4, 6), sh); img.paste(lay, (0, 0), lay)

def s_monsoon(t, s0, s1):
    m = OM(*MAP_A); img = m.base.copy()
    c_back = AT('5.5', 'back', 'మిగతా') - .1; c_sail = AT('5.5', 'Sailors', 'నావికులు') - .15
    k_in = e_out(prog(t, s0, s0 + .6))
    # permanent trade routes: thin, quiet, no traffic (the wind is the subject now)
    draw_routes(img, m, t, {g: 1.0 for g in ROUTES}, alpha=.32, dots=False)
    # temporary wind: soft streaks + four big arrows that swing round at the reversal
    rev = e_io(prog(t, c_back, c_back + .9)); turning = 0 < rev < 1
    base = math.atan2(-.64, .77)                                    # south-west monsoon blows towards the north-east
    wind(img, m, t, 1 if rev < .5 else -1, .55 * k_in * (1 - math.sin(math.pi * rev)), n=420)
    for i, ll in enumerate(WIND_AT):
        x, y = m.P(*ll); wind_arrow(img, x, y, base + math.pi * rev, k_in, 1.0, phase=t * .9 + i * .25 if not turning else 0)
    # ships ride the wind: east to India in summer, west and home in winter
    for summer, winter, off in ((ROUTES['ARAB'][0], ROUTES['ARAB'][0], 0.0),
                                ([(41.5, -2.6), (52.0, 3.0), (64.0, 8.5), (75.6, 11.2)], [(41.5, -2.6), (50.0, 5.0), (61.0, 14.5), (70.4, 20.4)], .18)):
        if t < c_back: pts = m.path(summer); f = e_io(prog(t, s0 + .3 + off, c_back + .1)); (x, y), ang = poly_at(pts, f)
        else: pts = m.path(winter); f = e_io(prog(t, c_back + .5 + off * 4, c_sail + 1.6 + off * 4)); (x, y), ang = poly_at(pts, 1 - f); ang += math.pi
        dhow(img, x, y - 26, ang, k_in, 1.25)
    # season plate: one sentence a viewer can read without sound
    for kk, kick, ttl in ((1 - rev, L('JUN – SEP · SOUTH-WEST MONSOON', 'జూన్ – సెప్టెంబర్ · నైరుతి రుతుపవనాలు'), L('WIND BLOWS TO INDIA', 'గాలి భారత్ వైపు')),
                          (rev, L('NOV – FEB · NORTH-EAST MONSOON', 'నవంబర్ – ఫిబ్రవరి · ఈశాన్య రుతుపవనాలు'), L('WIND BLOWS BACK HOME', 'గాలి తిరిగి వెనక్కి'))):
        if kk > .5 or (kk > .02 and not turning): plate_text(img, (80, 300, W - 80, 470), kick, ttl, k_in, 52 if not TE else 50, owner='season')
    # sailing calendar (simplified): the year split by the two winds
    kc = e_out(prog(t, c_sail, c_sail + .5))
    if kc > .01:
        box = (70, 1120, W - 70, 1335); plate(img, box, kc, alpha=232)
        ms = L(list('JFMAMJJASOND'), ['జన', 'ఫి', 'మా', 'ఏ', 'మే', 'జూ', 'జు', 'ఆ', 'సె', 'అ', 'న', 'డి'])
        cw = (W - 200) / 12; lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        for i in range(12):
            x0 = 100 + i * cw; sw_ = 5 <= i <= 8; ne = i in (10, 11, 0, 1)
            col = RCOL['INDIAN'] if sw_ else ((124, 156, 176) if ne else (60, 56, 50))
            d.rounded_rectangle((x0 + 4, 1180, x0 + cw - 4, 1238), 8, fill=col + (int(235 * kc),))
        img.paste(lay, (0, 0), lay)
        for i, ch in enumerate(ms): small(img, ch, 100 + i * cw + cw / 2, 1209, 28 if not TE else 24, INK, 'mm', kc)
        small(img, L('→ TO INDIA', '→ భారత్ వైపు'), 100 + 6.5 * cw, 1278, 28, RCOL['INDIAN'], 'mm', kc)
        small(img, L('← HOME', '← తిరుగు'), 100 + 11 * cw - 10, 1278, 28, (150, 180, 200), 'mm', kc)
        small(img, L('SAILING SEASONS · SIMPLIFIED', 'ప్రయాణ కాలాలు · సరళీకృతం'), W / 2, 1150, 25, MUTED, 'mm', kc)
        LY.reg('card', box, owner='calendar')
    return img

# ------------------------------------------------------------------ PREVIEW B: Malindi -> Calicut, the pilot evidence trail, the Gujarat conclusion
TRACK = [(33.5, -30.0), (36.5, -24.5), (40.6, -16.0), (40.9, -10.0), (40.3, -5.2), (40.12, -3.22)]
ARCLL = [(40.12, -3.22), (47.0, 0.8), (56.0, 5.4), (66.0, 9.0), (72.5, 10.8), (75.78, 11.25)]

def dates_plate(img, t, c0, c1, a):
    import datetime as dt
    d0 = dt.date(1498, 4, 24); d1 = dt.date(1498, 5, 20); n = (d1 - d0).days; dd = d0 + dt.timedelta(days=int(round(n * e_io(prog(t, c0, c1)))))
    mo = L(['', '', '', '', 'APR', 'MAY'][dd.month], ['', '', '', '', 'ఏప్రిల్', 'మే'][dd.month])
    plate_text(img, (170, 306, W - 170, 440), L("DATES FROM THE CREW'S JOURNAL", 'తేదీలు: సిబ్బంది డైరీ నుంచి'), f'{dd.day} {mo} 1498', a, 50, owner='dates')

def pilot_icon(img, x, y, k, q=1.0):
    """an ink silhouette (not a portrait) with an amber question mark"""
    if k <= .01: return
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); a = int(255 * k)
    d.ellipse((x - 17, y - 66, x + 17, y - 32), fill=(24, 20, 16, a), outline=PARCH + (a,), width=3)
    d.polygon([(x - 30, y + 18), (x + 30, y + 18), (x + 20, y - 28), (x - 20, y - 28)], fill=(24, 20, 16, a), outline=PARCH + (a,))
    img.paste(lay, (0, 0), lay)
    if q > .01: text(img, '?', x, y - 108, 64, AMBER, 'mm', 'head', k * q, None, (0, 0, 0))

def route_layer(img, m, t, k_track, k_arc, ship_f=None, a=1.0, w=7):
    lay = Image.new('RGBA', (W * 2, H * 2), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    tr = poly_part(m.path(TRACK), k_track)
    for i in range(0, len(tr) - 1, 2): d.line([(tr[i][0] * 2, tr[i][1] * 2), (tr[i + 1][0] * 2, tr[i + 1][1] * 2)], fill=CREAM + (int(210 * a),), width=6)
    arc = poly_part(m.path(ARCLL, 14), k_arc)
    if len(arc) > 1: d.line([(x * 2, y * 2) for x, y in arc], fill=AMBER + (int(255 * a),), width=w * 2, joint='curve')
    lay = lay.resize((W, H), Image.LANCZOS); g_ = lay.filter(ImageFilter.GaussianBlur(9)); img.paste(g_, (0, 0), g_); img.paste(lay, (0, 0), lay)
    if ship_f is not None:
        (x, y), ang = poly_at(m.path(ARCLL, 14), ship_f); dhow(img, x, y - 24, ang, a, .8)

def s_route(t, s0, s1):
    c_mal = AT('5.6a', 'Malindi', 'మాలిండి') - .15; c_pil = AT('5.6a', 'pilot…', 'దారిచూపే') - .15
    c_gui = AT('5.6a', 'guided', 'అతనే') - .15; c_cal = AT('5.6a', 'Calicut.', 'కాలికట్') - .1
    kz = e_io(prog(t, s0, s0 + 1.4)); m = om_lerp(kz); img = m.base.copy()
    draw_routes(img, m, t, {g: 1.0 for g in ROUTES}, alpha=.38 * (1 - .4 * kz))
    if kz >= 1: wind(img, m, t, 1, .45, n=380)
    route_layer(img, m, t, e_io(prog(t, s0 + .6, c_mal + .2)), e_io(prog(t, c_gui, c_cal + .3)), ship_f=e_io(prog(t, c_gui, c_cal + .3)) if t >= c_gui else None)
    small(img, L('APPROXIMATE ROUTE', 'సుమారు మార్గం'), 210, 1250, 22 if not TE else 24, PARCH, 'mm', e_out(prog(t, s0 + 1.0, s0 + 1.6)))
    xm, ym = m.P(*PORTS['MALINDI']); km = e_out(prog(t, c_mal, c_mal + .5))
    pin(img, xm, ym, km, CREAM, 12); map_label(img, PNAME['MALINDI'], xm + 30, ym + 50, 28 if not TE else 30, INK, km)
    kp = e_out(prog(t, c_pil, c_pil + .5)); pilot_icon(img, xm + 95, ym - 10, kp * (1 - e_io(prog(t, c_gui, c_gui + .6))), 1.0)
    if kp > 0: map_label(img, L('A LOCAL PILOT', 'స్థానిక దారిచూపే నావికుడు'), xm + 110, ym + 110, 24 if not TE else 26, INK, kp * (1 - e_io(prog(t, c_gui, c_gui + .6))))
    xc, yc = m.P(*PORTS['CALICUT']); kc = e_out(prog(t, c_cal, c_cal + .5))
    pin(img, xc, yc, kc, AMBER, 13, pulse=(t - c_cal) * .8 if kc > 0 else None)
    if kc > 0: map_label(img, PNAME['CALICUT'], xc - 10, yc + 54, 28 if not TE else 30, INK, kc)
    if t >= c_gui - .3: dates_plate(img, t, c_gui, c_cal + .3, e_out(prog(t, c_gui - .3, c_gui + .2)))
    return img

# ---- evidence cards: real screenshots of the 1898 English translation (Project Gutenberg), cropped to the quoted lines
CLIPS = json.load(open(EV + 'clips.json'))
@functools.lru_cache(8)
def CLIP(key, lines_before=1, lines_after=1):
    """crop the screenshot to whole text lines around the highlighted words (cuts in the gaps between lines)"""
    im = Image.open(EV + key + '.png').convert('RGB'); r = CLIPS[key]['rects']
    g = np.asarray(im.convert('L')); ink = (g < 140).sum(1) > 2
    bands = []; i = 0
    while i < len(ink):
        if ink[i]:
            j = i
            while j < len(ink) and ink[j]: j += 1
            bands.append([i, j]); i = j
        else: i += 1
    merged = []                                   # join tiny bands (dots, superscripts) to their line
    for b_ in bands:
        if merged and (b_[0] - merged[-1][1] < 6 or b_[1] - b_[0] < 10): merged[-1][1] = max(merged[-1][1], b_[1])
        else: merged.append(b_)
    ys = [q['y'] + q['h'] / 2 for q in r]
    hit = [n for n, (a_, b2) in enumerate(merged) if any(a_ - 8 <= y <= b2 + 8 for y in ys)]
    n0 = max(0, min(hit) - lines_before); n1 = min(len(merged) - 1, max(hit) + lines_after)
    y0 = (merged[n0][0] + (merged[n0 - 1][1] if n0 > 0 else 0)) / 2 if n0 > 0 else max(0, merged[0][0] - 14)
    y1 = (merged[n1][1] + merged[n1 + 1][0]) / 2 if n1 + 1 < len(merged) else min(im.height, merged[n1][1] + 14)
    im = im.crop((0, int(y0), im.width, int(y1)))
    a = np.asarray(im).astype(np.float32); a = a * (np.array([246, 238, 220]) / 255.0)          # paper tone
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)), [(q['x'], q['y'] - y0, q['w'], q['h']) for q in r]

def clip_card(img, key, cx, cy, wd, a=1.0, hl=0.0, lb=1, la=1, owner=None):
    """paper clipping at <= 1.0 scale with an animated highlighter on the quoted words; returns its box"""
    if a <= .01: return None
    im, rects = CLIP(key, lb, la); sc = min(1.0, wd / im.width); w_, h_ = int(im.width * sc), int(im.height * sc)
    x0, y0 = int(cx - w_ / 2), int(cy - h_ / 2); box = (x0, y0, x0 + w_, y0 + h_)
    shadow(img, box, a, 18, 10)
    pic = im.resize((w_, h_), Image.LANCZOS).convert('RGBA')
    if hl > 0:
        lay = Image.new('RGBA', pic.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay); tot = sum(r[2] for r in rects) * hl
        for rx, ry, rw, rh in rects:
            if tot <= 0: break
            ww = min(rw, tot); d.rectangle((rx * sc - 3, ry * sc + rh * sc * .12, (rx + ww) * sc + 3, (ry + rh) * sc - rh * sc * .02), fill=(255, 196, 60, 110)); tot -= ww
        pic = Image.alpha_composite(pic, lay)
    m = Image.new('L', pic.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w_ - 1, h_ - 1), 10, fill=int(255 * a)); img.paste(pic.convert('RGB'), (x0, y0), m)
    LY.reg('image', box, owner=owner or key); return box

def case_strip(img, m_unused, t, a, q=1.0, gujarat=0.0):
    """the case file: a small, subordinate schematic of the route that stays at the top while documents are shown"""
    if a <= .01: return
    y = 300; x0, x1 = 180, W - 180; lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); al = int(200 * a)
    d.line((x0, y, x1, y), fill=AMBER + (al,), width=4)
    for x in (x0, x1): d.ellipse((x - 9, y - 9, x + 9, y + 9), fill=CREAM + (al,))
    img.paste(lay, (0, 0), lay)
    small(img, PNAME['MALINDI'], x0, y + 34, 25 if not TE else 26, PARCH, 'mm', a * .9)
    small(img, PNAME['CALICUT'], x1, y + 34, 25 if not TE else 26, PARCH, 'mm', a * .9)
    xs = lerp(x0 + 40, x1 - 40, clamp(prog(t, S('PILOT'), E('PILOT')))); dhow(img, xs, y - 22, 0, a * .9, .55)
    small(img, L('THE PILOT · 1498', 'దారిచూపే నావికుడు · 1498'), W / 2, y + 34, 25 if not TE else 26, AMBER, 'mm', a * .9)
    LY.reg('card', (x0 - 30, y - 50, x1 + 30, y + 52), owner='case strip')

def ex_kicker(img, n, sub, a):
    """small exhibit kicker: EXHIBIT n OF 3 · what it is"""
    if a <= .01: return
    small(img, L(f'EXHIBIT {n} OF 3 · ', f'ఆధారం {n} / 3 · ') + sub, W / 2, 404, 27 if not TE else 27, AMBER, 'mm', a, ST.sw - 40)

def key_term(img, s, a, px=84, col=CREAM, y=480):
    """the one thing to read: big, centred, alone on its line"""
    if a <= .01: return
    f, px = fit(s, 'head', px, ST.sw - 80); text(img, s, W / 2, y + (1 - a) * 14, px, col, 'mm', 'head', a, ST.sw - 80, (0, 0, 0))
    bb = f.getbbox(s, anchor='mm'); LY.reg('label', (W / 2 + bb[0] - 10, y + bb[1] - 8, W / 2 + bb[2] + 10, y + bb[3] + 8), owner=s)

def doc_label(img, y, kicker, sub, a, w=None):
    if a <= .01: return
    small(img, kicker, W / 2, y, 26 if not TE else 27, PARCH, 'mm', a, w or ST.sw - 60)
    if sub: small(img, sub, W / 2, y + 38, 24 if not TE else 24, MUTED, 'mm', a, w or ST.sw - 60)

def s_pilot(t, s0, s1):
    # cues on the actual voice (EN: Whisper word times; TE: script words aligned to the Telugu ASR chunks)
    c_x = AT('PILOT', "'Christian'…", "'క్రైస్తవుడు'") - .25
    c_h = AT('PILOT', 'but', 'కానీ') - .15; c_so = AT('PILOT', 'so', 'అందుకే') - .1
    c_lat = AT('PILOT', 'Later', 'తర్వాతి') - .2; c_name = AT('PILOT', 'Malemo', 'మాలెమో') - .15
    c_tit = AT('PILOT', 'title,', 'బిరుదు:') - .3; c_fam = AT('PILOT', 'famous', 'అతను') - .2
    c_unl = AT('PILOT', 'unlikely.', 'కానీ', n=1 if not TE else 2) - .2; c_ver = AT('PILOT', 'So', 'అంటే', n=2 if not TE else 1) - .2
    c_guj = AT('PILOT', 'Gujarat,', 'గుజరాత్‌కు', n=2) - .2
    if t >= c_ver: return s_verdict(t, c_ver, c_guj, s1)
    img = radial_bg(W, H, (30, 26, 20), (9, 9, 9), cy=.45, reach=.85).copy()
    k_in = e_out(prog(t, s0 - .1, s0 + .5)); case_strip(img, None, t, .7 * k_in)
    pop = lambda c, d=.28: e_out(prog(t, c, c + d))           # elements arrive on a clean background (no cross-dissolves)
    SRC1 = L('ENGLISH TRANSLATION · RAVENSTEIN 1898 · PROJECT GUTENBERG', 'ఆంగ్ల అనువాదం · RAVENSTEIN 1898 · PROJECT GUTENBERG')
    # ---- EXHIBIT 1 · the voyage journal and the problem with "Christian"   (clean cut to exhibit 2 at c_lat)
    if t < c_lat:
        ex_kicker(img, 1, L("THE CREW'S JOURNAL, 1498", 'సిబ్బంది డైరీ, 1498'), k_in)
        if t < c_x:   # (a) the journal itself, alone: a surviving manuscript copy
            key_term(img, L("THE CREW'S JOURNAL", 'సిబ్బంది డైరీ'), k_in, 60)
            panel_nat(img, 'ROTEIRO', (190, 560, W - 190, 1110), 1.0, (.5, .30), (.5, .34), sc=.62, radius=10, a=k_in)
            doc_label(img, 1170, L('A SURVIVING MANUSCRIPT COPY · EARLY 1500s', 'మిగిలిన చేతిరాత ప్రతి · 1500ల మొదట్లో'),
                      L('PORTO MUNICIPAL LIBRARY, MS 804 · PUBLIC DOMAIN', 'పోర్టో మునిసిపల్ లైబ్రరీ, MS 804 · పబ్లిక్ డొమైన్'), k_in)
            return img
        # (b) cut to the English translation (1898): the key word, then the two quotations
        key_term(img, L("'CHRISTIAN'", "'క్రైస్తవుడు'"), pop(c_x), 92, AMBER)
        a_ = pop(c_x + .05); sw_ = e_io(prog(t, c_h, c_h + .3))
        b1 = clip_card(img, 'A1_christian_pilot', W / 2, 660 + 16 * (1 - a_), 940, a_ * (1 - .4 * sw_), e_io(prog(t, c_x + .4, c_x + 1.2)), 2, 0, 'A1')
        if TE and b1: small(img, "'రాజు ఒక క్రైస్తవ నావికుడిని పంపాడు'", W / 2, b1[3] + 34, 25, PARCH, 'mm', a_ * (1 - sw_))
        if t >= c_h:
            a2 = pop(c_h)
            small(img, L('THE SAME JOURNAL, ON CALICUT', 'అదే డైరీ, కాలికట్ గురించి'), W / 2, 852, 26 if not TE else 27, PARCH, 'mm', a2)
            b2 = clip_card(img, 'A2_calecut_christians', W / 2, 935 + 16 * (1 - a2), 940, a2, e_io(prog(t, c_h + .4, c_h + 1.3)), 0, 0, 'A2')
            if TE and b2: small(img, "'కాలికట్ నగరంలో క్రైస్తవులు ఉంటారు'", W / 2, b2[3] + 34, 25, PARCH, 'mm', a2)
        if t >= c_so:
            plate_text(img, (110, 1100, W - 110, 1300), None, L("THE WORD DOESN'T TELL US HIS FAITH", 'ఈ మాట అతని మతాన్ని చెప్పదు'), pop(c_so), 48 if not TE else 44, owner='ex1 label',
                       sub=L("THE CREW CALLED CALICUT'S HINDUS 'CHRISTIANS' TOO", 'కాలికట్ హిందువులనూ వాళ్లు అలాగే పిలిచారు'))
        else: small(img, SRC1, W / 2, 1330, 24 if not TE else 24, MUTED, 'mm', a_)
        return img
    # ---- EXHIBIT 2 · later Portuguese chroniclers: a Gujarati navigator, "Malemo" a title   (clean cut to exhibit 3 at c_fam)
    if t < c_fam:
        a2 = pop(c_lat); ex_kicker(img, 2, L('LATER PORTUGUESE CHRONICLERS', 'తర్వాతి పోర్చుగీస్ చరిత్రకారులు'), a2)
        if t < c_name:
            key_term(img, L('JOÃO DE BARROS, 1552', 'జోవో డి బారోస్, 1552'), a2, 60)
            ph = 560; pw = int(ph * 700 / 640)
            panel_nat(img, 'BARROS', (W / 2 - pw / 2, 560, W / 2 + pw / 2, 560 + ph), 1.0, (.47, .245), (.47, .245), sc=ph / 640, radius=8, a=a2, tint=(246, 238, 220))
            doc_label(img, 1170, L('DÉCADAS DA ÁSIA · LISBON 1552 · TITLE PAGE', 'DÉCADAS DA ÁSIA · లిస్బన్ 1552 · టైటిల్ పేజీ'),
                      L('ALSO GÓIS AND CASTANHEDA · PUBLIC DOMAIN', 'గోయిస్, కాస్టన్హెడా కూడా · పబ్లిక్ డొమైన్'), a2)
            return img
        an = pop(c_name); key_term(img, L('MALEMO CANAQUA', 'మాలెమో కనాక్వా'), an, 92, AMBER)
        ph = 400; pw = int(ph * 700 / 640)
        panel_nat(img, 'BARROS', (W / 2 - pw / 2, 580, W / 2 + pw / 2, 580 + ph), 1.0, (.47, .245), (.47, .245), sc=ph / 640, radius=8, a=1.0, tint=(246, 238, 220))
        small(img, L('BARROS · GÓIS · CASTANHEDA · 16th CENTURY', 'బారోస్ · గోయిస్ · కాస్టన్హెడా · 16వ శతాబ్దం'), W / 2, 1030, 25 if not TE else 26, PARCH, 'mm', 1.0)
        box = (110, 1090, W - 110, 1300)
        if t < c_tit: plate_text(img, box, None, L('A NAVIGATOR FROM GUJARAT', 'గుజరాత్‌కు చెందిన నావికుడు'), pop(c_name + .2), 54 if not TE else 48, owner='name', sub=L('RAVENSTEIN 1898, NOTE 132', 'RAVENSTEIN 1898, NOTE 132'))
        else: plate_text(img, box, L("'MALEMO' = MU'ALLIM", "'మాలెమో' = ముఅల్లిమ్"), L('MASTER NAVIGATOR: A TITLE, NOT A NAME', 'నావికుల నాయకుడు: పేరు కాదు, బిరుదు'), pop(c_tit), 46 if not TE else 42, owner='title',
                        sub=L('RAVENSTEIN 1898, NOTE 132', 'RAVENSTEIN 1898, NOTE 132'))
        return img
    # ---- EXHIBIT 3 · the Ibn Majid identification, and why it is questioned   (clean cut to the map at c_ver)
    a3 = pop(c_fam); ex_kicker(img, 3, L('A LATER, FAMOUS STORY', 'తర్వాత వచ్చిన ఒక ప్రసిద్ధ కథ'), a3)
    ku = pop(c_unl, .35)
    kd = e_io(prog(t, c_fam + .8, c_unl + .4))                   # doubt grows while the story is told: the name slowly greys
    key_term(img, L('IBN MAJID?', 'ఇబ్న్ మాజిద్?'), a3, 96, tuple(int(lerp(c1, c2, kd)) for c1, c2 in zip(CREAM, (120, 114, 104))))
    plate_text(img, (110, 600, W - 110, 820), L('THE STORY SAYS THE PILOT WAS', 'ఆ కథ ప్రకారం నావికుడు'), L('THE FAMOUS ARAB NAVIGATOR', 'ప్రసిద్ధ అరబ్ నావికుడు'), a3, 50 if not TE else 46, owner='ibn majid')
    if ku > .01:
        plate_text(img, (110, 930, W - 110, 1200), L('HISTORIANS TODAY', 'ఈ రోజు చరిత్రకారులు'), L('MOST THINK IT UNLIKELY', 'చాలామంది: నిజం కాకపోవచ్చు'), ku, 58 if not TE else 50, owner='unlikely',
                   sub='TIBBETTS 1971 · SUBRAHMANYAM 1997')
    return img

def s_verdict(t, c_ver, c_guj, s1):
    """back to the map: the Malindi -> Calicut arc, and a thread to Gujarat (hedged)"""
    m = OM(*MAP_B); img = m.base.copy(); kin = e_io(prog(t, c_ver, c_ver + .35))
    draw_routes(img, m, t, {g: 1.0 for g in ROUTES}, alpha=.3)
    route_layer(img, m, t, 1.0, 1.0, a=1.0, w=8)
    xm, ym = m.P(*PORTS['MALINDI']); xc, yc = m.P(*PORTS['CALICUT']); xg, yg = m.P(*PORTS['GUJARAT'])
    pin(img, xm, ym, 1, CREAM, 11); pin(img, xc, yc, 1, AMBER, 12)
    map_label(img, PNAME['MALINDI'], xm + 30, ym + 50, 26 if not TE else 28, INK, 1); map_label(img, PNAME['CALICUT'], xc - 10, yc + 52, 26 if not TE else 28, INK, 1)
    # the pilot icon rides the arc; its thread rises to Gujarat
    (px_, py_), _ = poly_at(m.path(ARCLL, 14), lerp(.40, .58, e_io(prog(t, c_ver, c_guj + .2))))
    kq = 1 - e_io(prog(t, c_guj, c_guj + .5)); pilot_icon(img, px_, py_ - 20, kin, kq)
    kt = e_io(prog(t, c_guj - .1, c_guj + 1.0))
    if kt > 0:
        pts = _smooth([(px_, py_ - 50), (lerp(px_, xg, .5) - 40, lerp(py_, yg, .5) - 30), (xg, yg)], 12)
        lay = Image.new('RGBA', (W * 2, H * 2), (0, 0, 0, 0)); ImageDraw.Draw(lay).line([(x * 2, y * 2) for x, y in poly_part(pts, kt)], fill=AMBER + (240,), width=10, joint='curve')
        lay = lay.resize((W, H), Image.LANCZOS); g_ = lay.filter(ImageFilter.GaussianBlur(7)); img.paste(g_, (0, 0), g_); img.paste(lay, (0, 0), lay)
        kg = e_out(prog(t, c_guj + .7, c_guj + 1.2)); pin(img, xg, yg, kg, AMBER, 15, pulse=(t - c_guj) * .8)
        map_label(img, PNAME['GUJARAT'], xg - 70, yg - 50, 30 if not TE else 32, INK, kg)
    # the conclusion, clearly hedged
    kc = e_out(prog(t, c_guj + .3, c_guj + .9))
    if kc > .01:
        plate_text(img, (80, 290, W - 80, 540), L('THE ANSWER', 'జవాబు'), L('MOST LIKELY FROM GUJARAT', 'బహుశా గుజరాత్ నుంచే'), kc, 66 if not TE else 60, owner='verdict',
                   sub=L('INDIA · BASED ON 16th-CENTURY PORTUGUESE CHRONICLES', 'భారత్ · 16వ శతాబ్దపు పోర్చుగీస్ చరిత్రకారుల ఆధారంగా'))
    # the case strip fades back into the full map
    case_strip(img, None, t, .75 * (1 - kin))
    return img

# ------------------------------------------------------------------ remaining scenes (full render)
PK2 = '/home/claude/why-channel-studio/videos/2026-11-08_long_golden_sparrow_s1/visuals/pack2/'
SRC.update({'CANTINO': (ARC + '01_PD10_Cantino_planisphere_(1502).jpg', (4700, 0, 8550, 4998)), 'G22': (PK2 + 'G22_v2.png', None), 'G23': (PK2 + 'G23_v2.png', None)})
@functools.lru_cache(4)
def NATS(key, s):
    im = NAT(key); return im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
def cover_nat(key, u, f0, f1, prescale=.5, k=.95):
    """full-screen view of an archive picture that never enlarges it (scale <= 1.0), with a slow pan"""
    im = NATS(key, prescale); w, h = im.size; base = max(W / w, H / h); assert base <= 1.0001, (key, base)
    hw, hh = W / 2 / base, H / 2 / base; kk = e_io(clamp(u)); fx, fy = lerp(f0[0], f1[0], kk), lerp(f0[1], f1[1], kk)
    cx = min(max(fx * w, hw), w - hw); cy = min(max(fy * h, hh), h - hh)
    return grade(im.resize((W, H), Image.LANCZOS, box=(cx - hw, cy - hh, cx + hw, cy + hh)), k)
def credit_line(img, s, y=1330, a=1.0):
    if a <= .01: return
    f = pick(s, 'monob', 24); w = f.getlength(s) + 30; lay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(lay).rounded_rectangle((W / 2 - w / 2, y - 22, W / 2 + w / 2, y + 22), 12, fill=(10, 10, 10, int(190 * a))); img.paste(lay, (0, 0), lay)
    small(img, s, W / 2, y, 24, (214, 206, 188), 'mm', a, ST.sw - 20); LY.reg('credit', (W / 2 - w / 2, y - 22, W / 2 + w / 2, y + 22), owner=s[:30])
def dramatized(img, x1, y0, a=1.0):
    s = L('DRAMATIZED · ILLUSTRATION', 'నాటకీకరణ · చిత్రణ'); w = pick(s, 'head', 22).getlength(s); chip(img, s, x1 - 24 - w / 2 - 18, y0 + 34, 22, (24, 22, 19), CREAM, a=a)

# ---- 1 · hook: a real European map of 1502 -> the busy ocean -> one small ship with a question
def s_hook(t, s0, s1, frame0=False):
    c_disc = AT('S5_hook', 'discover', 'కనిపెట్టలేదు.') - .1; c_busy = AT('S5_hook', 'busy', 'ఎవరో') - .2; c_show = AT('S5_hook', 'show', 'చూపించారు.') - .15
    if frame0: t = 0.0
    if t < c_busy + .5:
        img = cover_nat('CANTINO', prog(t, 0, c_busy + .5), (.42, .55), (.56, .52), .5, .98)
        ka = 1.0 if frame0 else 1.0
        plate_text(img, (150, 330, W - 150, 520), L('VASCO DA GAMA · 1498', 'వాస్కో డ గామా · 1498'), L('DISCOVERED INDIA?', 'భారత్‌ను కనిపెట్టాడా?'), ka * (1 if t < c_disc + .2 else 1), 60 if not TE else 56, owner='hook')
        credit_line(img, L('CANTINO PLANISPHERE · 1502 · BIBLIOTECA ESTENSE, MODENA', 'కాంటినో ప్రపంచ పటం · 1502 · ఎస్టెన్స్ లైబ్రరీ, మోడెనా'))
        if t < c_busy: return img
        m = OM(*MAP_A); mp = m.base.copy(); draw_routes(mp, m, t, {g: 1.0 for g in ROUTES})
        return Image.blend(img, mp, e_io(prog(t, c_busy, c_busy + .5)))
    m = OM(*MAP_A); img = m.base.copy(); draw_routes(img, m, t, {g: 1.0 for g in ROUTES})
    small(img, L('TRADE ROUTES, LONG BEFORE 1498', '1498కి ఎంతో ముందే వ్యాపార మార్గాలు'), W / 2, 380, 28, PARCH, 'mm', e_out(prog(t, c_busy + .4, c_busy + .9)))
    ks = e_out(prog(t, c_show, c_show + .4))
    if ks > .01:
        tr = m.path([(33.5, -34.0), (36.0, -27.0), (38.5, -20.0)]); lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        for i in range(0, len(tr) - 1, 2): d.line((tr[i], tr[i + 1]), fill=CREAM + (int(220 * ks),), width=3)
        img.paste(lay, (0, 0), lay); x, y = m.P(38.5, -20.0); dhow(img, x, y - 24, -1.2, ks, 1.0); text(img, '?', x + 4, y - 110, 72, AMBER, 'mm', 'head', ks, None, (0, 0, 0))
    return img

# ---- 9 · the welcome at Calicut: shore (dramatized) -> the journal's words -> the question -> the answer
def s_welcome(t, s0, s1):
    c_two = AT('5.7', 'Two', 'ట్యూనిస్') - .15; c_q = AT('5.7', "'What", "'ఇంత") - .15; c_a = AT('5.7', "'Christians…", "'క్రైస్తవుల") - .3
    img = radial_bg(W, H, (30, 26, 20), (9, 9, 9), cy=.4, reach=.85).copy(); k = e_out(prog(t, s0, s0 + .4))
    panel_nat(img, 'G22', (40, 300, W - 40, 300 + 560), prog(t, s0, s1), (.40, .5), (.58, .5), sc=.66, radius=14, a=k)
    dramatized(img, W - 40, 300, k)
    if t < c_two:
        small(img, L("CALICUT · MAY 1498", 'కాలికట్ · మే 1498'), W / 2, 930, 30, AMBER, 'mm', k)
        text(img, L("A STRANGE WELCOME", 'ఒక విచిత్రమైన స్వాగతం'), W / 2, 1000, 58 if not TE else 52, CREAM, 'mm', 'head', k, ST.sw - 60, None)
        return img
    if t < c_q:
        a = e_out(prog(t, c_two, c_two + .3))
        small(img, L("THE CREW'S JOURNAL · TR. RAVENSTEIN 1898", 'సిబ్బంది డైరీ · ఆంగ్ల అనువాదం 1898'), W / 2, 935, 25, AMBER, 'mm', a)
        b = clip_card(img, 'W1_tunis', W / 2, 1090 + 14 * (1 - a), 940, a, e_io(prog(t, c_two + .3, c_two + 1.6)), 0, 0, 'W1')
        if TE and b: small(img, "'ట్యూనిస్ నుంచి వచ్చిన ఇద్దరు వ్యాపారులు, స్పానిష్, ఇటాలియన్ మాట్లాడేవారు'", W / 2, b[3] + 34, 24, PARCH, 'mm', a)
        return img
    if t < c_a:
        plate_text(img, (90, 960, W - 90, 1290), L('TWO MERCHANTS FROM TUNIS ASKED', 'ట్యూనిస్ వ్యాపారులు అడిగారు'), L("'WHAT BROUGHT YOU HERE?'", "'ఇంత దూరం ఎందుకొచ్చారు?'"), e_out(prog(t, c_q, c_q + .3)), 66 if not TE else 58, owner='q',
                   sub=L("THE CREW'S JOURNAL, 1498", 'సిబ్బంది డైరీ, 1498'))
        return img
    plate_text(img, (90, 960, W - 90, 1290), L('THE PORTUGUESE ANSWER', 'పోర్చుగీసుల జవాబు'), L("'CHRISTIANS… AND SPICES.'", "'క్రైస్తవుల కోసం… సుగంధ ద్రవ్యాల కోసం.'"), e_out(prog(t, c_a, c_a + .3)), 66 if not TE else 54, owner='a',
               sub=L("THE CREW'S JOURNAL, 1498", 'సిబ్బంది డైరీ, 1498'))
    return img

# ---- 10 · the gifts: labels land on the objects; the officials laughed
GIFTS = [(('Hats,', 'టోపీలు,'), L('HATS', 'టోపీలు'), (620, 640), (-170, -150)), (('coral,', 'పగడాలు,'), L('CORAL', 'పగడాలు'), (720, 725), (-90, 150)),
         (('sugar,', 'చక్కెర,'), L('SUGAR', 'చక్కెర'), (905, 612), (150, 150)), (('honey.', 'తేనె.'), L('HONEY', 'తేనె'), (1010, 540), (170, -190))]
def s_gifts(t, s0, s1):
    c_l = AT('5.8', 'laughed.', 'నవ్వారు.') - .25
    img = radial_bg(W, H, (30, 26, 20), (9, 9, 9), cy=.4, reach=.85).copy(); k = e_out(prog(t, s0, s0 + .35)); sc = .66
    box = (40, 300, W - 40, 300 + 600); u = prog(t, s0, s1); f0, f1 = (.47, .5), (.53, .5); panel_nat(img, 'G23', box, u, f0, f1, sc=sc, radius=14, a=k)
    dramatized(img, W - 40, 300, k)
    im = NAT('G23'); bw, bh = box[2] - box[0], box[3] - box[1]; kk_ = e_io(clamp(u)); fx = lerp(f0[0], f1[0], kk_) * im.width
    fx = min(max(fx, bw / sc / 2), im.width - bw / sc / 2); ox = fx - bw / sc / 2; oy = im.height / 2 - bh / sc / 2
    P = lambda x, y: (box[0] + (x - ox) * sc, box[1] + (y - oy) * sc)
    for (w_en, w_te), lab, (gx, gy), (dx, dy) in GIFTS:
        kk = e_out(prog(t, AT('5.8', w_en, w_te) - .1, AT('5.8', w_en, w_te) + .25))
        if kk <= .01: continue
        x, y = P(gx, gy); lx, ly = min(max(x + dx * .55, 150), W - 150), min(max(y + dy * .55, 360), 860)
        lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); d.line((x, y, lx, ly), fill=GOLD_A + (int(240 * kk),), width=3)
        d.ellipse((x - 7, y - 7, x + 7, y + 7), fill=AMBER + (int(255 * kk),)); img.paste(lay, (0, 0), lay); map_label(img, lab, lx, ly, 32, INK, kk)
    if t < c_l:
        small(img, L("DA GAMA'S GIFTS FOR THE KING", 'రాజు కోసం డ గామా కానుకలు'), W / 2, 960, 30, AMBER, 'mm', k)
        small(img, L('THE FULL LIST ALSO HAD CLOTH, HOODS, BASINS AND OIL', 'జాబితాలో గుడ్డ, టోపీలు, పళ్లేలు, నూనె కూడా ఉన్నాయి'), W / 2, 1010, 24, MUTED, 'mm', k)
        return img
    plate_text(img, (90, 960, W - 90, 1300), L("THE KING'S OFFICIALS LAUGHED", 'రాజు అధికారులు నవ్వారు'), L("'THE POOREST MERCHANT FROM MECCA… GAVE MORE'", "'మక్కా నుంచి వచ్చే అతి పేద వ్యాపారి కూడా ఇంతకంటే ఎక్కువ ఇస్తాడు'"),
               e_out(prog(t, c_l, c_l + .3)), 52 if not TE else 44, owner='mecca', sub=L("THE CREW'S JOURNAL, 1498 · TR. RAVENSTEIN", 'సిబ్బంది డైరీ, 1498 · RAVENSTEIN అనువాదం'))
    return img

# ---- 11 · not a new world, an old one: Portugal's thin Cape line plugs into the old network (EN: the middlemen routes to Europe)
EUROPE = [[(45.0, 12.6), (43.3, 12.9), (41.0, 17.0), (38.0, 23.0), (34.6, 27.6), (32.6, 29.9), (31.2, 33.0)], [(56.5, 26.5), (52.5, 27.6), (49.8, 29.4), (47.8, 30.3), (44.5, 33.3)]]
CAPE = [(28.0, -40.0), (33.5, -34.0), (36.5, -24.5), (40.6, -16.0), (40.9, -10.0), (40.12, -3.22), (47.0, 0.8), (56.0, 5.4), (66.0, 9.0), (75.78, 11.25)]
def s_old(t, s0, s1):
    k5 = '5.9' if has('5.9') else 'OLD'
    c_new = AT(k5, 'new', 'కొత్త') - .1; c_old = AT(k5, 'old', 'అప్పటికే') - .15; c_mid = AT(k5, 'middlemen', 'ప్రపంచంలోకి') - .2
    m = OM(*MAP_A); img = m.base.copy(); draw_routes(img, m, t, {g: 1.0 for g in ROUTES}, alpha=.85)
    km = e_io(prog(t, c_mid, c_mid + .8)) if not TE else 0
    if km > 0:
        lay = Image.new('RGBA', (W * 2, H * 2), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        for seg in EUROPE:
            p = poly_part(m.path(seg), km); d.line([(x * 2, y * 2) for x, y in p], fill=(196, 132, 110, 255), width=14, joint='curve')
        lay = lay.resize((W, H), Image.LANCZOS); img.paste(lay, (0, 0), lay)
        x, y = m.P(39.0, 21.0); map_label(img, 'TO EUROPE · MIDDLEMEN', x + 170, y + 10, 28, INK, km)
        small(img, 'RED SEA & GULF ROUTES', W / 2, 1300, 26, PARCH, 'mm', km)
    kc = e_io(prog(t, c_old, c_old + 1.4))
    if kc > 0:
        p = poly_part(m.path(CAPE, 12), kc); lay = Image.new('RGBA', (W * 2, H * 2), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        for i in range(0, len(p) - 1, 2): d.line(((p[i][0] * 2, p[i][1] * 2), (p[i + 1][0] * 2, p[i + 1][1] * 2)), fill=CREAM + (240,), width=8)
        lay = lay.resize((W, H), Image.LANCZOS); img.paste(lay, (0, 0), lay)
        if kc >= 1: x, y = m.P(75.78, 11.25); pin(img, x, y, 1, AMBER, 12, pulse=(t - c_old) * .8)
        small(img, L("PORTUGAL'S ROUTE, 1498", 'పోర్చుగల్ మార్గం, 1498'), 250, 1250, 26, CREAM, 'mm', e_out(prog(t, c_old + .6, c_old + 1.0)))
    a1 = e_out(prog(t, c_new, c_new + .3)); a2 = e_out(prog(t, c_old, c_old + .3))
    if a1 > .01:
        plate_text(img, (80, 300, W - 80, 470), '1498', L('NOT A NEW WORLD', 'కొత్త ప్రపంచం కాదు') if a2 < .5 else L('NOT A NEW WORLD · AN OLD ONE', 'కొత్త ప్రపంచం కాదు · పాత ప్రపంచం'), a1, 44 if not TE else 42, owner='old')
    return img

# ---- 12 · diplomacy and force: a two-row ledger, both columns filled for both powers
FORCE_PINS = {'COCHIN': (76.27, 9.93), 'CALICUT': (75.78, 11.25), 'SURAT': (72.83, 21.17)}
def s_force(t, s0, s1):
    c_tr = AT('FORCE', 'treaties', 'ఒప్పందాలు') - .1; c_ca = AT('FORCE', 'cannons:', 'ఫిరంగులు') - .1
    c_al = AT('FORCE', 'allied', 'ఒప్పందాలు') - .1; c_bo = AT('FORCE', 'bombarded', 'ఫిరంగులు') - .1
    c_ce = AT('FORCE', 'century', 'శతాబ్దం') - .15; c_pe = AT('FORCE', 'permissions…', 'అనుమతులు') - .1; c_fo = AT('FORCE', 'force', 'బలాన్ని') - .1
    m = OM(*MAP_B); img = m.base.copy(); draw_routes(img, m, t, {g: 1.0 for g in ROUTES}, alpha=.42)
    for name, c, lab in (('COCHIN', c_al, L('COCHIN · ALLY', 'కొచ్చి · మిత్రుడు')), ('CALICUT', c_bo, L('CALICUT · BOMBARDED', 'కాలికట్ · ఫిరంగి దాడి')), ('SURAT', c_pe, L('SURAT · SWALLY', 'సూరత్ · స్వాలీ'))):
        kk = e_out(prog(t, c, c + .4)); x, y = m.P(*FORCE_PINS[name])
        if kk <= .01: continue
        pin(img, x, y, kk, AMBER if name != 'COCHIN' else CREAM, 12)
        if name in ('CALICUT', 'SURAT') and ((name == 'CALICUT' and t > c_bo) or (name == 'SURAT' and t > c_fo)):
            c0 = c_bo if name == 'CALICUT' else c_fo; u = prog(t, c0, c0 + 4.5); lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
            for i in range(6):                                          # ink smoke drifts up and thins out over ~4.5 s
                r = 16 + 60 * u + i * 8; d.ellipse((x - 60 + i * 12 - r, y - 30 - 160 * u - i * 10 - r, x - 60 + i * 12 + r, y - 30 - 160 * u - i * 10 + r), fill=(64, 60, 54, int(120 * (1 - u))))
            lay = lay.filter(ImageFilter.GaussianBlur(6)); img.paste(lay, (0, 0), lay)
        map_label(img, lab, x - 190 if name != 'SURAT' else x - 170, y + (34 if name == 'COCHIN' else -34), 26, INK, kk)
    # the ledger
    box = (60, 960, W - 60, 1330); kL = e_out(prog(t, s0, s0 + .4)); plate(img, box, kL, alpha=235)
    c0x, c1x, c2x = 80, 330, 690; colw = 330
    small(img, L('DIPLOMACY', 'దౌత్యం'), c1x + colw / 2 - 10, 1000, 28, AMBER, 'mm', kL); small(img, L('FORCE', 'బలం'), c2x + colw / 2 - 20, 1000, 28, AMBER, 'mm', kL)
    rows = [(L('PORTUGUESE', 'పోర్చుగీసులు'), 1095, s0 + .1, (L('TREATIES', 'ఒప్పందాలు'), L('ALLY: COCHIN, 1500–03', 'మిత్రుడు: కొచ్చి, 1500–03'), c_tr), (L('CANNONS', 'ఫిరంగులు'), L('CALICUT: 1500, 1502', 'కాలికట్: 1500, 1502'), c_ca)),
            (L('ENGLISH', 'ఇంగ్లీష్'), 1235, c_ce, (L('PERMISSIONS', 'అనుమతులు'), L('SURAT: 1608–13', 'సూరత్: 1608–13'), c_pe), (L('FORCE', 'బలం'), L('SWALLY: 1612', 'స్వాలీ: 1612'), c_fo))]
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); d.line((80, 1030, W - 80, 1030), fill=GOLD_A + (int(160 * kL),), width=1); d.line((80, 1165, W - 80, 1165), fill=GOLD_A + (int(110 * kL),), width=1); img.paste(lay, (0, 0), lay)
    for lab, y, cr, cell1, cell2 in rows:
        kr = e_out(prog(t, cr, cr + .3)); text(img, lab, c0x + 10, y, 30 if not TE else 30, CREAM, 'lm', 'head', kr * kL, 240, None)
        for (ttl, sub, cc), x0 in ((cell1, c1x), (cell2, c2x)):
            kc = e_out(prog(t, cc, cc + .3)) * kL
            if kc <= .01: continue
            lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(lay).rounded_rectangle((x0, y - 54, x0 + colw - 20, y + 54), 10, fill=(58, 50, 36, int(230 * kc)), outline=GOLD_A + (int(200 * kc),), width=2); img.paste(lay, (0, 0), lay)
            text(img, ttl, x0 + (colw - 20) / 2, y - 16, 34 if not TE else 32, CREAM, 'mm', 'head', kc, colw - 50, None)
            small(img, sub, x0 + (colw - 20) / 2, y + 28, 23, PARCH, 'mm', kc, colw - 40)
    LY.reg('card', box, owner='ledger')
    return img

# ---- 13 · tease: the Company's arms, the next episode
@functools.lru_cache(1)
def ARMS():
    im = Image.fromarray(FL.img('PD12')).convert('RGB'); im.thumbnail((440, 440), Image.LANCZOS); return im
def s_tease(t, s0, s1):
    img = radial_bg(W, H, (40, 34, 24), (9, 9, 9), cy=.42, reach=.8).copy(); k = e_out(prog(t, s0, s0 + .4))
    a = ARMS(); m_ = Image.new('L', a.size, 0); ImageDraw.Draw(m_).rounded_rectangle((0, 0, a.width - 1, a.height - 1), 16, fill=int(255 * k))
    x0, y0 = int(W / 2 - a.width / 2), int(540 - 30 * e_io(prog(t, s0, s1))); shadow(img, (x0, y0, x0 + a.width, y0 + a.height), k); img.paste(a, (x0, y0), m_); LY.reg('image', (x0, y0, x0 + a.width, y0 + a.height), owner='arms')
    small(img, L('EAST INDIA COMPANY · ARMS · PUBLIC DOMAIN', 'ఈస్ట్ ఇండియా కంపెనీ చిహ్నం · పబ్లిక్ డొమైన్'), W / 2, y0 + a.height + 36, 24, MUTED, 'mm', k)
    plate_text(img, (90, 300, W - 90, 470), L('NEXT · 6/6', 'తర్వాత · 6/6'), L('THE COMPANY THAT CAME TO TRADE', 'వ్యాపారానికి వచ్చిన కంపెనీ'), k, 50 if not TE else 48, owner='tease')
    kq = e_out(prog(t, s0 + 1.0, s0 + 1.4))
    plate_text(img, (90, 1060, W - 90, 1280), None, L('ASKED FOR PERMISSION… GAVE ORDERS', 'అనుమతి అడిగింది… ఆజ్ఞలు ఇచ్చింది'), kq, 50 if not TE else 46, owner='tease2')
    return img

def s_todo(t, s0, s1, name):
    img = radial_bg(W, H, (30, 26, 20), (9, 9, 9)).copy(); text(img, f'[{name}]', W / 2, H / 2, 40, MUTED, 'mm', 'head'); return img

FUNCS = {'hook': s_hook, 'ocean': s_ocean, 'monsoon': s_monsoon, 'route': s_route, 'pilot': s_pilot, 'welcome': s_welcome, 'gifts': s_gifts, 'old': s_old, 'force': s_force, 'tease': s_tease}
def render(t):
    LY.reset(); name, s0, s1 = scene_at(t)
    if name.startswith('cartoon'):
        k = {'cartoon1': 'Q1', 'cartoon2': 'Q2', 'cartoon3': 'Q3'}[name]; img = cartoon(t, s0, [('CHELLI', k)])
    elif name == 'slide': img = s_slide(t, s0, s1)
    elif name == 'loop': img = s_loop(t, s0, s1)
    else: img = FUNCS[name](t, s0, s1)
    overlays(img, t, name); captions(img, t, name); return img
