"""v3 pass, part 2: opening, Chapter 4 money + famine, subscribe card, Plassey numbers, 1765 revenue redirect, silver->taxes payoff."""
import math, functools, sys
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFilter
import flib as FL, fx
from flib import W, H, put, text, eo, GOLD, PAPER, INK, MUTED, RUST
sm, lerp, to_rgba, cam = fx.sm, fx.lerp, fx.to_rgba, fx.cam
RED = (196, 44, 36)
import seqs
C_TE = lambda: seqs.C['TE']

# ------------------------------------------------------------------ hand-drawn red marker (documentary annotation)
def marker_line(d, p0, p1, k, seed=0, w=9, col=RED, a=210):
    if k <= 0: return
    rng = np.random.default_rng(seed); n = 24
    xs = np.linspace(p0[0], p1[0], n); ys = np.linspace(p0[1], p1[1], n) + np.cumsum(rng.normal(0, 0.6, n))
    m = max(2, int(n * min(1, k)))
    d.line(list(zip(xs[:m], ys[:m])), fill=col + (a,), width=w, joint='curve')
def marker_box(d, box, k, seed=0, w=7, col=RED, a=210):
    x0, y0, x1, y1 = box; rng = np.random.default_rng(seed); pts = []
    for s in np.linspace(0, 1.08, 60):
        ang = 2 * math.pi * s - 2.4; r = 1 + rng.normal(0, 0.012)
        pts.append(((x0 + x1) / 2 + (x1 - x0) / 2 * 1.06 * r * math.cos(ang), (y0 + y1) / 2 + (y1 - y0) / 2 * 1.25 * r * math.sin(ang)))
    m = max(2, int(len(pts) * min(1, k))); d.line(pts[:m], fill=col + (a,), width=w, joint='curve')

def doc_cam(key, u, c0, c1, z0, z1):
    """camera on a document; returns frame + projector for source coords."""
    a = FL.img(key); h, w = a.shape[:2]; base = max(W / w, H / h); e = sm(u) * .8 + u * .2
    s = base * lerp(z0, z1, e); fx_, fy_ = lerp(c0[0], c1[0], e), lerp(c0[1], c1[1], e); hw, hh = W / 2 / s, H / 2 / s
    cx = min(max(fx_ * w, hw), w - hw); cy = min(max(fy_ * h, hh), h - hh)
    fr = to_rgba(fx.view(a, cx, cy, s)); P = lambda X, Y: ((X - cx) * s + W / 2, (Y - cy) * s + H / 2)
    return fr, P

def stamp(fr, t, c, label, x, y, col=RED, size=96, rot=-8, t_out=1e9):
    k = (t - c) / 0.18
    if k <= 0: return
    fo = 1 - sm((t - t_out) / 0.35)
    if fo <= 0: return
    im = text(label, 'disp', size, col); im2 = text(label, 'disp', size, col)
    pad = Image.new('RGBA', (im.width + 70, im.height + 50), (0, 0, 0, 0)); pd = ImageDraw.Draw(pad)
    pd.rounded_rectangle((5, 5, pad.width - 6, pad.height - 6), 16, fill=(240, 228, 210, 70), outline=col + (255,), width=12)
    for ox, oy in ((0, 0), (2, 0), (0, 2), (2, 2)): pad.alpha_composite(im2, (35 + ox, 25 + oy))
    rng = np.random.default_rng(3); a = np.array(pad); hole = rng.random(a.shape[:2]) < 0.10; a[hole, 3] = (a[hole, 3] * 0.35).astype(np.uint8); pad = Image.fromarray(a)
    sc = 1 + 1.4 * (1 - sm(min(1, k))); pad = pad.rotate(rot, expand=True, resample=Image.BICUBIC)
    pad = pad.resize((int(pad.width * sc), int(pad.height * sc)), Image.BICUBIC)
    put(fr, pad, x, y, min(1, k) * 0.92 * fo, 'cc')

# ------------------------------------------------------------------ 0.1  the 1721 Act, underlined; the cloth, stamped
def s01(t, a, b, cue, L):
    c_ban = cue('0.1', 'banning', 'చట్టం'); c_cloth = cue('0.1', 'printed', 'నిషేధం') - 0.1; c_why = cue('0.1', 'Why', 'ఎందుకు')
    if t < c_cloth:
        fr, P = doc_cam('PD03', (t - a) / max(0.1, c_cloth - a), (.565, .175), (.55, .18), 1.62, 1.78)
        d = ImageDraw.Draw(fr)
        marker_line(d, P(1955, 584), P(2215, 584), sm((t - c_ban + 0.1) / 0.5), 1)
        marker_line(d, P(850, 644), P(1545, 644), sm((t - c_ban - 0.35) / 0.7), 2)
        return fr
    fr = to_rgba(cam(FL.img('MET1'), (t - c_cloth) / max(0.1, b - c_cloth), (.47, .40), (.48, .41), 2.3, 2.45))
    stamp(fr, t, c_cloth + 0.55, L('BANNED · 1721', 'నిషేధం · 1721'), W * 0.64, H * 0.40, col=(178, 30, 26), size=130, t_out=c_why - 0.4)
    return fr

# ------------------------------------------------------------------ 0.2  cotton vs wool & silk: the scale tips
@functools.lru_cache(maxsize=4)
def swatch(kind, size=280):
    rng = np.random.default_rng(11); Y, X = np.mgrid[0:size, 0:size].astype(np.float32)
    if kind == 'wool':
        base = np.array([196, 186, 168], np.float32); tw = 0.85 + 0.15 * np.sin((X + Y) * 0.55)          # twill
        a = base * tw[..., None] + rng.normal(0, 9, (size, size, 1))
    else:
        base = np.array([188, 150, 170], np.float32); sh = 0.75 + 0.35 * np.exp(-((X - Y * 0.6 - 90) ** 2) / 1800)  # silk sheen
        a = base * sh[..., None] + rng.normal(0, 3, (size, size, 1))
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert('RGBA')
    m = Image.new('L', (size, size), 0); ImageDraw.Draw(m).ellipse((4, 4, size - 4, size - 4), fill=255); im.putalpha(m)
    ring = Image.new('RGBA', (size + 16, size + 16), (0, 0, 0, 0)); ImageDraw.Draw(ring).ellipse((2, 2, size + 13, size + 13), outline=GOLD + (255,), width=5)
    ring.alpha_composite(im, (8, 8)); return ring
def scale_scene(fr, t, c_in, c_tip, left, right, lab_l, lab_r, tilt_deg, y0=430):
    d = ImageDraw.Draw(fr); pcx = W / 2; ex = 400
    ang = math.radians(tilt_deg * eo((t - c_tip) / 0.9)) if t > c_tip else 0.0
    lx, ly = pcx - ex * math.cos(ang), y0 + ex * math.sin(ang); rx, ry = pcx + ex * math.cos(ang), y0 - ex * math.sin(ang)
    k = eo((t - c_in) / 0.5)
    d.line((lx, ly, rx, ry), fill=GOLD + (int(230 * k),), width=6)
    d.polygon([(pcx, y0 + 4), (pcx - 30, y0 + 70), (pcx + 30, y0 + 70)], fill=GOLD + (int(230 * k),))
    d.line((pcx, y0 + 70, pcx, y0 + 330), fill=GOLD + (int(160 * k),), width=4)
    put(fr, left, lx, ly + 40, k, 'ct'); put(fr, right, rx, ry + 40, k, 'ct')
    put(fr, text(lab_l, 'label', 34, PAPER), lx, ly + 360, k, 'ct'); put(fr, text(lab_r, 'label', 34, PAPER), rx, ry + 360, k, 'ct')
def s02(t, a, b, cue, L):
    c_vs = cue('0.2', 'Indian', 'పత్తి') - 0.15; c_tip = cue('0.2', 'challenging', 'గట్టి')
    if t < c_vs:
        return to_rgba(cam(FL.img('MET1'), (t - a) / max(0.1, c_vs - a), (.48, .40), (.5, .5), 2.0, 1.0))
    fr = fx.dark(); cot = fx.medallion('MET1', 1260, 1050, 420, 280)
    pair = Image.new('RGBA', (300 * 2 + 20, 300), (0, 0, 0, 0)); pair.alpha_composite(swatch('wool'), (0, 0)); pair.alpha_composite(swatch('silk'), (310, 0))
    pair = pair.resize((int(pair.width * 0.62), int(pair.height * 0.62)))
    scale_scene(fr, t, c_vs, c_tip, cot, pair, L('INDIAN COTTON', 'మన పత్తి గుడ్డ'), L("BRITAIN'S WOOL · SILK", 'బ్రిటన్ ఉన్ని · పట్టు'), 10)
    return fr

# ------------------------------------------------------------------ 0.3  the world sails to India: pepper, diamonds, above all cloth
def pepper_medallion(size=220):
    im = Image.new('RGBA', (size + 16, size + 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse((8, 8, size + 8, size + 8), fill=(46, 40, 34, 255)); rng = np.random.default_rng(4)
    for _ in range(70):
        x, y = rng.uniform(40, size - 24, 2); r = rng.uniform(9, 14); c = int(rng.uniform(30, 70))
        if (x - size / 2) ** 2 + (y - size / 2) ** 2 < (size / 2 - 22) ** 2:
            d.ellipse((x - r, y - r, x + r, y + r), fill=(c + 30, c + 18, c, 255)); d.ellipse((x - r * .4, y - r * .5, x - r * .1, y - r * .2), fill=(c + 70, c + 60, c + 40, 255))
    d.ellipse((2, 2, size + 13, size + 13), outline=GOLD + (255,), width=5); return im
def s03(t, a, b, cue, L, mapfn):
    c_map = cue('0.3', 'pepper', 'మిరియాల') - 0.35
    if t < c_map:
        arr = FL.img('T1'); return to_rgba(cam(arr, (t - a) / max(0.1, c_map - a), (.5, .55), (.5, .52), 1.05, 1.16))
    fr = mapfn(t, c_map, b)
    items = [(cue('0.3', 'pepper', 'మిరియాల'), pepper_medallion(), L('PEPPER', 'మిరియాలు'), 520),
             (cue('0.3', 'diamonds', 'గోల్కొండ'), fx.medallion('PD02', 1340, 1500, 420, 220), L('DIAMONDS', 'వజ్రాలు'), 960),
             (cue('0.3', 'cloth', 'గుడ్డ'), fx.medallion('MET1', 1260, 1050, 420, 300), L('CLOTH', 'గుడ్డ'), 1400)]
    for c, im, lab, x in items:
        k = eo((t - c) / 0.4)
        if k <= 0: continue
        sc = 0.6 + 0.4 * eo((t - c) / 0.3); im2 = im.resize((int(im.width * sc), int(im.height * sc)))
        put(fr, im2, x, 250, k, 'cc'); put(fr, text(lab, 'label', 36, PAPER), x, 250 + im.height / 2 + 20, k, 'ct')
    return fr

# ------------------------------------------------------------------ 0.4  a quarter of world output: a ring that fills
def ring_overlay(fr, t, c, frac, x, y, r, lab, sub):
    k = sm((t - c) / 1.4)
    if t < c - 0.2: return
    d = ImageDraw.Draw(fr)
    d.ellipse((x - r, y - r, x + r, y + r), outline=(80, 76, 92, 230), width=26)
    if k > 0: d.arc((x - r, y - r, x + r, y + r), -90, -90 + 360 * frac * k, fill=GOLD + (255,), width=26)
    put(fr, text(lab, 'disp', 64, GOLD), x, y - 6, eo((t - c) / 0.5), 'cc')
    put(fr, text(sub, 'label', 28, PAPER, maxw=380), x, y + r + 34, eo((t - c - 0.3) / 0.5), 'ct')

# ------------------------------------------------------------------ 4.6  follow the money (illustrated)
FLOW_POS = dict(farmer=(220, 470), coll=(680, 470), state=(1140, 470), army=(1600, 470), bank=(910, 830), merch=(1480, 830))
def flow2(t, a, b, cue, L):
    fr = fx.dark(); d = ImageDraw.Draw(fr)
    cs = dict(farmer=a + 0.2, crop=cue('4.6', 'third', 'మూడో'), coll=cue('4.6', 'Collectors', 'వసూలు'), cut=cue('4.6', 'cut', 'వాటా'),
              state=cue('4.6', 'state', 'రాజ్యం'), army=cue('4.6', 'armies', 'సైన్యాలకు'), bank=cue('4.6', 'Bankers', 'వడ్డీ'),
              merch=cue('4.6', 'foreign', 'విదేశీ'), farman=cue('4.6', 'permission', 'ఫర్మానా'))
    put(fr, text(L('FOLLOW THE MONEY', 'డబ్బు వెనకే'), 'label', 34, GOLD), 70, 70, eo((t - a) / 0.5))
    med = dict(farmer=fx.medallion('G02', 1290, 560, 260, 190), coll=fx.medallion('G18', 860, 500, 300, 190),
               state=fx.medallion('PD08', 1340, 1400, 700, 190), army=fx.medallion('PD13', 1340, 1500, 700, 190),
               bank=fx.medallion('G19', 860, 520, 330, 170), merch=fx.medallion('G10', 1820, 560, 300, 170))
    labs = dict(farmer=L('FARMER', 'రైతు'), coll=L('COLLECTORS · LOCAL LORDS', 'వసూలుదారులు · స్థానిక పెద్దలు'), state=L('STATE', 'రాజ్యం'),
                army=L('ARMIES · COURTS', 'సైన్యాలు · దర్బార్లు'), bank=L('BANKERS', 'వడ్డీ వ్యాపారులు'), merch=L('FOREIGN MERCHANT', 'విదేశీ వ్యాపారి'))
    order = ['farmer', 'coll', 'state', 'army']
    # harvest: 12 sacks above the farmer; a third to a half leave towards the collectors
    ks = eo((t - a - 0.3) / 0.5)
    for i in range(12):
        x0, y0 = 90 + (i % 6) * 52, 140 + (i // 6) * 58
        mv = 0.0
        if i >= 6 or (i >= 4 and i < 6):
            pass
        leaving = i >= 6 or i in (4, 5)              # 4..6 of 12 = 1/3 .. 1/2 (two shaded as the uncertain part)
        if leaving and t > cs['crop']:
            mv = sm((t - cs['crop'] - (0.1 if i >= 6 else 0.6)) / 1.0)
        j = [4, 5, 6, 7, 8, 9, 10, 11].index(i) if leaving else 0
        x = lerp(x0, 600 + (j % 4) * 48, mv); y = lerp(y0, 250 + (j // 4) * 52, mv)
        col = (214, 186, 120) if not (i in (4, 5)) else (170, 150, 100)
        d.rounded_rectangle((x, y, x + 42, y + 46), 9, fill=col + (int(255 * ks),), outline=(110, 86, 44, int(255 * ks)), width=2)
        d.line((x + 10, y + 8, x + 32, y + 8), fill=(110, 86, 44, int(255 * ks)), width=3)
    if t > cs['crop']:
        put(fr, text(L('1/3 TO 1/2 OF THE CROP · HISTORIANS\' ESTIMATE', 'పంటలో 1/3 నుంచి 1/2 · చరిత్రకారుల అంచనా'), 'label', 26, MUTED, maxw=470), 90, 268, eo((t - cs['crop'] - 0.4) / 0.5))
    for i, k_ in enumerate(order):
        kk = eo((t - cs[k_]) / 0.5)
        if kk <= 0: continue
        x, y = FLOW_POS[k_]
        put(fr, med[k_], x, y, kk, 'cc'); put(fr, text(labs[k_], 'label', 28, PAPER, maxw=330), x, y + 115, kk, 'ct')
        role = {'farmer': L('PAYS', 'కడతాడు'), 'coll': L('COLLECTS · KEEPS A CUT', 'వసూలు · వాటా'), 'state': L('RECEIVES', 'అందుకుంటుంది'), 'army': L('IS PAID', 'ఖర్చు')}[k_]
        put(fr, text(role, 'label', 24, GOLD, maxw=330), x, y + 190, eo((t - cs[k_] - 0.3) / 0.4), 'ct')
        if i > 0:
            x0 = FLOW_POS[order[i - 1]][0] + 110; x1 = x - 112
            d.line((x0, y, x1, y), fill=GOLD + (int(220 * kk),), width=4); d.polygon([(x1, y - 10), (x1 + 18, y), (x1, y + 10)], fill=GOLD + (int(220 * kk),))
            for c in range(4):
                f = ((t - cs[k_]) * 0.5 + c / 4) % 1; cx = x0 + (x1 - x0) * f
                if k_ == 'state' and t > cs['cut'] and c % 2 == 1: continue          # the collectors keep their cut
                d.ellipse((cx - 9, y - 9 - 0, cx + 9, y + 9), fill=(232, 190, 90, int(230 * kk)), outline=(140, 100, 30, int(230 * kk)))
    if t > cs['coll'] + 0.5:                                    # porters carry the share to the collectors
        import sprites as SP
        for j in range(2):
            f = ((t - cs['coll']) * 0.35 + j * 0.5) % 1; px = lerp(FLOW_POS['farmer'][0] + 120, FLOW_POS['coll'][0] - 120, f)
            SP.man(d, px, 640, 70, (200, 186, 160), min(1, f / 0.1, (1 - f) / 0.1), musket=False); d.rounded_rectangle((px - 14, 640 - 86, px + 14, 640 - 62), 5, fill=(214, 186, 120, int(255 * min(1, f / 0.1, (1 - f) / 0.1))))
    if t > cs['cut']:                                           # coins dropping into the collectors' pile
        kc = eo((t - cs['cut']) / 0.6); x, y = FLOW_POS['coll']
        for j in range(5): d.ellipse((x - 60 + j * 26, y + 82 - (j % 2) * 6, x - 42 + j * 26, y + 96 - (j % 2) * 6), fill=(232, 190, 90, int(230 * kc)))
    for k_ in ('bank', 'merch'):
        kk = eo((t - cs[k_]) / 0.5)
        if kk <= 0: continue
        x, y = FLOW_POS[k_]; put(fr, med[k_], x, y, kk, 'cc'); put(fr, text(labs[k_], 'label', 26, PAPER, maxw=330), x, y + 102, kk, 'ct')
        if k_ == 'bank': put(fr, text(L('LEND TO EVERYONE', 'అందరికీ అప్పు'), 'label', 22, GOLD), x, y + 138, eo((t - cs[k_] - 0.3) / 0.4), 'ct')
        if k_ == 'bank':
            for tx in ('farmer', 'coll', 'state', 'army', 'merch'):
                px, py = FLOW_POS[tx]; d.line((x, y - 90, px, py + 95 if tx != 'merch' else py), fill=(120, 140, 178, int(150 * kk)), width=2)
    if t > cs['farman']:
        x, y = FLOW_POS['merch']; k = eo((t - cs['farman']) / 0.4)
        put(fr, text(L('NEEDS A FARMAN · ROYAL PERMISSION', 'ఫర్మానా కావాలి · రాజు అనుమతి'), 'label', 26, GOLD, maxw=420), x, y + 150, k, 'ct')
    return fr

# ------------------------------------------------------------------ 4.9 / 4.10  famine
@functools.lru_cache(maxsize=1)
def crack_mask():
    a = FL.img('CC04').astype(np.float32).mean(2); m = np.clip((110 - a) / 50, 0, 1)
    rng = np.random.default_rng(2); n = cv2.resize(rng.random((20, 36)).astype(np.float32), (a.shape[1], a.shape[0]), interpolation=cv2.INTER_CUBIC)
    return m, n
def cracks(arr, t, c):
    m, n = crack_mask(); p = sm((t - c) / 2.5)
    show = np.clip((p * 1.2 - n) / 0.08, 0, 1) * m
    out = arr.astype(np.float32); out = out * (1 - 0.55 * show[..., None]) ; return np.clip(out, 0, 255).astype(np.uint8)
def desat(arr, k, warm=True):
    a = arr.astype(np.float32); l = a.mean(2, keepdims=True); a = l + (a - l) * (1 - k)
    if warm: a *= np.array([1.02, 0.98, 0.92]) * (1 - 0.15 * k) + 0.15 * k
    return np.clip(a, 0, 255).astype(np.uint8)
def dust(fr, t, box, n=60, seed=1):
    d = ImageDraw.Draw(fr); rng = np.random.default_rng(seed); x0, y0, x1, y1 = box
    for i in range(n):
        px = x0 + ((rng.random() * (x1 - x0)) + t * rng.uniform(4, 14)) % (x1 - x0)
        py = y0 + ((rng.random() * (y1 - y0)) - t * rng.uniform(2, 8)) % (y1 - y0)
        r = rng.uniform(1.2, 3.2); al = int(90 + 80 * math.sin(t * rng.uniform(1, 3) + i))
        d.ellipse((px - r, py - r, px + r, py + r), fill=(255, 236, 200, max(0, al)))
def s49(t, a, b, cue, L):
    c_fail = cue('4.9', 'failed', 'పడకపోతే'); c_top = cue('4.9', 'wealth', 'పైనున్న') - 0.1; c_bot = cue('4.9', 'bottom', 'కిందున్నవాళ్లను') - 0.3
    if t < c_top:
        return to_rgba(cam(cracks(FL.img('CC04'), t, c_fail - 0.4), (t - a) / max(0.1, c_top - a), (.5, .5), (.5, .5), 1.05, 1.12))
    if t < c_bot:
        return to_rgba(cam(FL.img('G19'), (t - c_top) / max(0.1, c_bot - c_top), (.30, .70), (.30, .66), 1.7, 1.8))
    return to_rgba(cam(desat(FL.img('G16'), 0.45), (t - c_bot) / max(0.1, b - c_bot), (.30, .48), (.28, .50), 1.75, 1.65))

FAMINE = [('Gujarat', 72.5, 22.6, 3.2), ('Deccan', 76.5, 18.6, 3.6)]
def famine_map(t, a, b, c_yr, L):
    spec = dict(box0=(64, 88, 9, 30), box1=(66, 86, 11, 28), glows=[(L(n, {'Gujarat': 'గుజరాత్', 'Deccan': 'దక్కన్'}[n]), lo, la, r * (0.6 + 0.4 * sm((t - c_yr) / 3.0)), (150, 40, 34), c_yr - 0.2 + k * 0.6) for k, (n, lo, la, r) in enumerate(FAMINE)])
    fr = FL.render_map(None, t, spec, a, b)
    yr = 1630 + int(min(2, max(0, (t - c_yr) / 0.9)))
    put(fr, text(str(yr), 'disp', 120, (220, 120, 100)), W - 120, 110, eo((t - c_yr + 0.2) / 0.4), 'rt')
    return fr
def millions(fr, t, c, L):
    d = ImageDraw.Draw(fr); rng = np.random.default_rng(9); k = sm((t - c) / 2.4)
    n = int(2600 * k)
    xs = rng.uniform(60, W - 60, 2600); ys = rng.uniform(170, H - 160, 2600)
    for i in range(n): d.ellipse((xs[i] - 3, ys[i] - 3, xs[i] + 3, ys[i] + 3), fill=(210, 200, 186, 170))
    put(fr, text(L('ESTIMATES RUN INTO THE MILLIONS', 'పదుల లక్షల్లో · అంచనా'), 'label', 40, PAPER), W / 2, 90, eo((t - c) / 0.5), 'ct')
def s410(t, a, b, cue, L):
    c_yr = cue('4.10', '1630', '1630'); c_mundy = cue('4.10', 'Peter', 'Peter') - 0.15; c_mil = cue('4.10', 'Estimates', 'చనిపోయినవాళ్లు') - 0.15
    c_weav = cue('4.10', 'Many', 'ఎంతోమంది') - 0.15
    if t < c_mundy: return famine_map(t, a, c_mundy, c_yr, L)
    if t < c_mil:
        u = (t - c_mundy) / max(0.1, c_mil - c_mundy)
        fr, P = doc_cam('PD09', u, (.30, .30), (.28, .32), 1.55, 1.75); d = ImageDraw.Draw(fr)
        marker_line(d, P(320, 1452), P(860, 1452), sm((t - c_mundy - 1.2) / 0.7), 4)
        put(fr, text(L("PETER MUNDY'S TRAVELS · 'GREAT DEARTH'", "పీటర్ మండీ యాత్రా రచనలు · 'great dearth'"), 'label', 30, PAPER), 70, H - 70, eo((t - c_mundy - 0.3) / 0.5), 'lb')
        return fr
    if t < c_weav:
        fr = fx.dark(); millions(fr, t, c_mil, L); return fr
    u = (t - c_weav) / max(0.1, b - c_weav)
    fr = to_rgba(cam(desat(FL.img('G20'), 0.25 + 0.45 * u), u, (.45, .55), (.45, .57), 1.05, 1.14))
    dust(fr, t, (900, 150, 1700, 900)); return fr

# ------------------------------------------------------------------ 3.12  the channel's animated subscribe card (chapter break)
def subscribe(t, a, b, c_sub, lang):
    sys.path.insert(0, '/home/claude/why-channel-studio/pipeline/style_v2'); import cta_card, cairo
    bg = fx.blurred('G14', 0.42); fr = Image.fromarray(bg).convert('RGBA')
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s)
    c.translate((W - 1080 * 1.25) / 2, 0); c.scale(1.25, 1.25)
    cta_card.draw(c, t, c_sub - 0.3, 'yt', lang, y=H / 2 / 1.25, t_out=b - 0.4)
    buf = np.ndarray((H, W, 4), np.uint8, s.get_data()); rgba = buf[..., [2, 1, 0, 3]].copy()
    fr.alpha_composite(Image.fromarray(rgba, 'RGBA'))
    return fr
def subscribe_events(c_sub):
    sys.path.insert(0, '/home/claude/why-channel-studio/pipeline/style_v2'); import cta_card
    return cta_card.events(c_sub - 0.3, 'yt')

# ------------------------------------------------------------------ 7.2 / 7.3  Plassey: 1 dot = 100 soldiers
def armies(fr, t, c_co, c_nb, c_never, L):
    d = ImageDraw.Draw(fr)
    k1 = eo((t - c_co) / 0.6)
    for i in range(30):
        x, y = 260 + (i % 6) * 22, 520 + (i // 6) * 22
        if k1 > 0: d.ellipse((x - 7, y - 7, x + 7, y + 7), fill=(200, 60, 50, int(255 * k1)))
    put(fr, text(L('~3,000 COMPANY', '~3,000 కంపెనీ'), 'label', 32, PAPER), 315, 470, k1, 'cb')
    n = int(500 * sm((t - c_nb) / 1.2)); rng = np.random.default_rng(1)
    never = rng.random(500) < 0.62
    for i in range(n):
        x, y = 820 + (i % 25) * 36, 330 + (i // 25) * 24
        grey = t > c_never and never[i]; kg = eo((t - c_never - (i % 25) * 0.02) / 0.6) if grey else 0
        col = (int(lerp(210, 90, kg)), int(lerp(170, 90, kg)), int(lerp(90, 96, kg)))
        d.ellipse((x - 7, y - 7, x + 7, y + 7), fill=col + (255,))
    put(fr, text(L('~50,000 NAWAB\'S ARMY', '~50,000 నవాబు సైన్యం'), 'label', 32, PAPER), 1250, 290, eo((t - c_nb) / 0.6), 'cb')
    put(fr, text(L('1 DOT ≈ 100 SOLDIERS', '1 చుక్క ≈ 100 మంది'), 'label', 24, MUTED), W - 70, H - 60, eo((t - c_co) / 0.6), 'rb')
    if t > c_never:
        put(fr, text(L('MUCH OF IT NEVER FOUGHT', 'చాలామంది యుద్ధమే చేయలేదు'), 'label', 34, (200, 200, 210)), 1250, 860, eo((t - c_never - 0.4) / 0.5), 'ct')
def s72(t, a, b, cue, L):
    c_co = cue('7.2', 'three', 'మూడు') if C_TE() else cue('7.2', '3', 'మూడు')
    if t < c_co - 0.5:
        return to_rgba(cam(FL.img('G30'), (t - a) / max(0.1, c_co - a), (.5, .55), (.48, .55), 1.02, 1.08))
    fr = Image.fromarray(fx.blurred('G30', 0.38)).convert('RGBA')
    armies(fr, t, cue('7.2', 'three', 'మూడు') if C_TE() else cue('7.2', '3', 'మూడు'), cue('7.2', 'fifty', 'యాభై') if C_TE() else cue('7.2', '50', 'యాభై'), 1e9, L); return fr
def s73(t, a, b, cue, L):
    c_cmd = cue('7.3', 'Its', 'సేనాని') - 0.15
    if t < c_cmd:
        fr = Image.fromarray(fx.blurred('G30', 0.38)).convert('RGBA')
        armies(fr, t, a - 5, a - 5, cue('7.3', 'never', 'చేయలేదు') - 0.3, L); return fr
    return to_rgba(cam(FL.img('G30'), (t - c_cmd) / max(0.1, b - c_cmd), (.36, .45), (.33, .46), 1.45, 1.6))

# ------------------------------------------------------------------ 7.5  1765: the revenue changes direction
def s75(t, a, b, cue, L, mapfn):
    c_rev = cue('7.5', '1765', '1765'); c_paint = cue('7.5', 'revenue', 'ఆదాయం') + 1.2
    if t >= c_paint:
        return to_rgba(cam(FL.img('PD17'), (t - c_paint) / max(0.1, b - c_paint), (.5, .5), (.52, .48), 1.0, 1.08))
    fr = mapfn(t, a, b); d = ImageDraw.Draw(fr)
    k = eo((t - c_rev) / 0.6)
    if k <= 0: return fr
    src = (1090, 480)
    emp = fx.medallion('PD17', 1500, 760, 260, 170); co = fx.medallion('PD12', 1340, 1340, 1200, 170)
    ex, ey, cx_, cy_ = 1500, 300, 1500, 820
    put(fr, emp, ex, ey, k, 'cc'); put(fr, text(L('MUGHAL EMPEROR', 'మొఘల్ చక్రవర్తి'), 'label', 26, PAPER), ex, ey + 100, k, 'ct')
    put(fr, co, cx_, cy_, k, 'cc'); put(fr, text(L('THE COMPANY', 'కంపెనీ'), 'label', 26, PAPER), cx_, cy_ + 100, k, 'ct')
    sw = sm((t - c_rev - 0.8) / 1.0)                                # revenue swings from the emperor to the Company
    tx, ty = lerp(ex - 100, cx_ - 100, sw), lerp(ey, cy_, sw)
    d.line((src[0], src[1], tx, ty), fill=((232, 190, 90) if sw < 0.5 else RED) + (int(230 * k),), width=6)
    for c in range(5):
        f = ((t - c_rev) * 0.6 + c / 5) % 1; px, py = lerp(src[0], tx, f), lerp(src[1], ty, f)
        d.ellipse((px - 10, py - 10, px + 10, py + 10), fill=(232, 190, 90, int(240 * k)), outline=(140, 100, 30, int(240 * k)))
    if sw > 0.6:
        put(fr, text(L('REVENUE OF BENGAL · BIHAR · ORISSA', 'బెంగాల్ · బీహార్ · ఒరిస్సా ఆదాయం'), 'label', 30, GOLD), src[0], src[1] + 60, eo((sw - 0.6) / 0.4), 'ct')
    return fr

# ------------------------------------------------------------------ 7.6  silver from the world -> taxes from India
def s76(t, a, b, cue, L):
    c_sil = cue('7.6', 'silver', 'వెండి') - 0.2; c_tax = cue('7.6', 'taxes', 'పన్నులతో') - 0.2
    c_cloth = cue('7.6', 'Think', 'మన') + 0.1
    if t < c_sil - 0.1:
        return to_rgba(cam(FL.img('MET1'), (t - a) / max(0.1, c_sil - a), (.5, .45), (.5, .47), 1.6, 1.75))
    fr = fx.dark(); d = ImageDraw.Draw(fr)
    cloth = fx.medallion('MET1', 1260, 1050, 420, 220); sx, sy = 960, 540
    put(fr, cloth, sx, sy, 1.0, 'cc'); put(fr, text(L('OUR CLOTH', 'మన గుడ్డ'), 'label', 30, PAPER), sx, sy + 135, 1.0, 'ct')
    sw = sm((t - c_tax) / 0.9) if t > c_tax else 0.0
    # source A: ships with silver from across the world (left); source B: taxes collected in India (bottom)
    ka = 1 - sw; kb = sw
    shipx, shipy = 260, 540; taxx, taxy = 960, 930
    if ka > 0.02:
        d.polygon([(shipx - 70, shipy + 10), (shipx + 70, shipy + 10), (shipx + 50, shipy + 40), (shipx - 50, shipy + 40)], fill=(232, 214, 170, int(255 * ka)))
        d.polygon([(shipx - 4, shipy - 80), (shipx - 4, shipy + 5), (shipx - 60, shipy)], fill=(250, 244, 228, int(255 * ka)))
        d.polygon([(shipx + 4, shipy - 70), (shipx + 4, shipy + 5), (shipx + 55, shipy - 4)], fill=(250, 244, 228, int(230 * ka)))
        put(fr, text(L('SILVER FROM ACROSS THE WORLD', 'ప్రపంచం నుంచి వెండి'), 'label', 28, PAPER, maxw=360), shipx, shipy + 70, ka, 'ct')
    if kb > 0.02:
        put(fr, fx.medallion('PD12', 1340, 1340, 1200, 150), taxx, taxy, kb, 'cc')
        put(fr, text(L('TAXES COLLECTED IN INDIA', 'భారత్‌లోనే వసూలైన పన్నులు'), 'label', 28, RED + (0,) if False else (220, 120, 100), maxw=420), taxx + 110, taxy, kb, 'lc')
    for c in range(6):
        f = ((t - c_sil) * 0.55 + c / 6) % 1
        if ka > 0.02:
            px, py = lerp(shipx + 80, sx - 130, f), shipy
            d.ellipse((px - 11, py - 11, px + 11, py + 11), fill=(206, 206, 214, int(240 * ka)), outline=(120, 120, 130, int(240 * ka)))
        if kb > 0.02:
            px, py = sx, lerp(taxy - 90, sy + 130, f)
            d.ellipse((px - 11, py - 11, px + 11, py + 11), fill=(206, 206, 214, int(240 * kb)), outline=(120, 120, 130, int(240 * kb)))
    # bales leave for London (right) the whole time
    for c in range(3):
        f = ((t - c_sil) * 0.4 + c / 3) % 1; px = lerp(sx + 140, W - 160, f)
        d.rounded_rectangle((px - 26, sy - 22, px + 26, sy + 22), 8, fill=(214, 186, 120, 255), outline=(110, 86, 44, 255), width=2)
    put(fr, text(L('TO LONDON', 'లండన్‌కు'), 'label', 28, PAPER), W - 160, sy + 50, 1.0, 'ct')
    return fr
