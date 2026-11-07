"""v5: THE THREAD - one cotton thread connects the story (chapter cards, opening setup, ending payoff). Editorial: typed facts, cut-out photos."""
import math, functools
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import flib as FL, fx
from flib import W, H, put, text, eo, GOLD, PAPER, INK, MUTED
sm, lerp = fx.sm, fx.lerp
X = {}
def init(**k): X.update(k)
def L(en, te): return te if X['TE'] else en
THREAD = (236, 226, 204)

def bez(p0, p1, p2, p3, n=60):
    out = []
    for i in range(n + 1):
        s = i / n; a = (1 - s) ** 3; b = 3 * (1 - s) ** 2 * s; c = 3 * (1 - s) * s * s; d = s ** 3
        out.append((a * p0[0] + b * p1[0] + c * p2[0] + d * p3[0], a * p0[1] + b * p1[1] + c * p2[1] + d * p3[1]))
    return out
def thread(d, pts, k, alpha=1.0, w=4):
    """a cotton thread: cream core, twist ticks, soft shadow; drawn progressively (k 0..1)."""
    if k <= 0: return
    m = max(2, int(len(pts) * min(1, k)))
    p = pts[:m]
    d.line([(x + 3, y + 4) for x, y in p], fill=(0, 0, 0, int(90 * alpha)), width=w + 2, joint='curve')
    d.line(p, fill=THREAD + (int(255 * alpha),), width=w, joint='curve')
    for i in range(1, m - 1, 2):
        x0, y0 = p[i]; x1, y1 = p[i + 1]; ang = math.atan2(y1 - y0, x1 - x0) + 0.9
        d.line((x0 - 3 * math.cos(ang), y0 - 3 * math.sin(ang), x0 + 3 * math.cos(ang), y0 + 3 * math.sin(ang)), fill=(176, 160, 128, int(220 * alpha)), width=1)
    hx, hy = p[-1]
    if k < 1: d.ellipse((hx - 5, hy - 5, hx + 5, hy + 5), fill=THREAD + (int(255 * alpha),))
def knot(d, x, y, r, a):
    d.ellipse((x - r, y - r, x + r, y + r), fill=(214, 196, 150, int(255 * a)), outline=(120, 100, 60, int(255 * a)), width=2)
    d.arc((x - r * 0.6, y - r * 0.6, x + r * 0.6, y + r * 0.6), 30, 300, fill=(150, 130, 90, int(255 * a)), width=2)

@functools.lru_cache(maxsize=32)
def photo(key, fx_, fy_, zoom, wpx, hpx, rot):
    a = FL.img(key); h, w = a.shape[:2]; cw = int(w / zoom); ch = int(cw * hpx / wpx)
    cx, cy = int(fx_ * w), int(fy_ * h); x0 = max(0, min(w - cw, cx - cw // 2)); y0 = max(0, min(h - ch, cy - ch // 2))
    im = Image.fromarray(a[y0:y0 + ch, x0:x0 + cw]).resize((wpx, hpx), Image.LANCZOS)
    b = 14; card = Image.new('RGBA', (wpx + 2 * b, hpx + 2 * b + 10), (236, 230, 216, 255)); card.paste(im, (b, b))
    sh = Image.new('RGBA', (card.width + 40, card.height + 40), (0, 0, 0, 0)); ImageDraw.Draw(sh).rectangle((20, 26, card.width + 20, card.height + 26), fill=(0, 0, 0, 120))
    sh = sh.filter(ImageFilter.GaussianBlur(9)); sh.alpha_composite(card, (20, 20))
    return sh.rotate(rot, expand=True, resample=Image.BICUBIC)
def typed(fr, s, x, y, t, c0, cps=30, size=30, col=PAPER, maxw=560, anchor='lt', bg=False):
    """typewriter reveal (whole words wrap correctly because the full string is laid out first)."""
    n = int(max(0, t - c0) * cps)
    if n <= 0: return 0
    full = text(s, 'label', size, col, maxw=maxw)
    part = text(s[:min(n, len(s))] + (' ' * max(0, len(s) - n)), 'label', size, col, maxw=maxw)
    if bg:
        pad = Image.new('RGBA', (full.width + 36, full.height + 22), (10, 8, 14, 200)); pad.alpha_composite(part, (18, 11)); part = pad
    put(fr, part, x, y, 1.0, anchor)
    if n < len(s) and int(t * 3) % 2 == 0:
        d = ImageDraw.Draw(fr)
    return min(1, n / max(1, len(s)))
def type_dur(s, cps=30): return len(s) / cps

# ------------------------------------------------------------------ chapter cards: what we learned -> thread -> the next question
CARDS = {1: (('PD03', .45, .17, 2.2), ('1721 · BRITAIN BANS INDIAN PRINTED COTTON', '1721 · భారత అచ్చు cotton పై బ్రిటన్ నిషేధం')),
         2: (('G01', .5, .55, 1.4), ('c.1700 · ABOUT A QUARTER OF WORLD OUTPUT · ONE ESTIMATE', 'సుమారు 1700 · ప్రపంచ ఉత్పత్తిలో దాదాపు నాలుగో వంతు · ఒక అంచనా')),
         3: (('MET1', .47, .40, 2.6), ('WEEKS OF SKILLED HANDWORK · BANNED IN BRITAIN', 'వారాల తరబడి నైపుణ్యమైన చేతిపని · బ్రిటన్‌లో నిషేధం')),
         4: (('G09', .07, .75, 4.0), ('VILLAGE → BROKER → PORT → SHIP', 'గ్రామం → దళారి → రేవు → ఓడ')),
         5: (('G16', .30, .48, 1.8), ('WEALTH AT THE TOP · HUNGER AT THE BOTTOM', 'పైన సంపద · కింద ఆకలి')),
         6: (('T1', .5, .55, 1.3), ('SPICES BROUGHT THEM EAST · INDIAN CLOTH BECAME THE BIG PRIZE', 'సుగంధ ద్రవ్యాలు వాళ్లను తూర్పుకు తెచ్చాయి · భారత గుడ్డే పెద్ద బహుమతి అయింది'))}
def chapter_card(t, a, b, n, base_card):
    fr = X['paper']().convert('RGBA'); d = ImageDraw.Draw(fr)
    (key, fxx, fyy, z), txt = CARDS[n]; s = L(*txt)
    kp = eo((t - a - 0.05) / 0.45)
    ph = photo(key, fxx, fyy, z, 400, 266, -3)
    put(fr, ph, 400, 440 - 30 * (1 - kp), kp, 'cc')
    typed(fr, s, 200, 620, t, a + 0.45, cps=34, size=30, col=PAPER, maxw=460)
    # the next question (the narrated chapter title), right half
    from film import SC, CH_NUM
    ttl = SC[f'{n}.0']['te' if X['TE'] else 'en'].split(' · '); title = ttl[1] if len(ttl) > 1 else ''
    k1 = eo((t - a - 0.2) / 0.6); k2 = eo((t - a - 0.5) / 0.7); cx = 1300
    put(fr, text(CH_NUM[n][1 if X['TE'] else 0], 'label', 34, GOLD), cx, 400, k1, 'cb', (1 - k1) * 12)
    wl = int(140 * k1); d.rectangle((cx - wl, 418, cx + wl, 421), fill=GOLD + (255,))
    put(fr, text(title, 'disp', 70 if not X['TE'] else 62, PAPER, glow=True, maxw=880), cx, 450, k2, 'ct', (1 - k2) * 18)
    pts = bez((610, 400), (760, 250), (cx - 380, 260), (cx - 160, 385))
    thread(d, pts, sm((t - a - 1.0) / 1.2))
    for j in range(6):
        x = W / 2 - 75 + j * 30; on = j < n
        d.ellipse((x - 6, H - 120 - 6, x + 6, H - 120 + 6), fill=(GOLD if on else (70, 66, 80)) + (int(255 * k1),))
    return fr

# ------------------------------------------------------------------ opening setup lines
def opening_lines(fr, t, c0, lines, x=90, y=150, size=42):
    for j, s in enumerate(lines):
        cj = c0 + sum(type_dur(q, 34) + 0.35 for q in lines[:j])
        if t >= cj:
            typed(fr, s, x, y + j * 74, t, cj, cps=34, size=size, col=PAPER if j < len(lines) - 1 else GOLD, maxw=1500, bg=True)

# ------------------------------------------------------------------ ending payoff: the thread, knot by knot
KNOTS = [('PERMISSION', 'అనుమతి', '1613'), ('WAR', 'యుద్ధం', '1686–90'), ('CHOOSING RULERS', 'రాజుల ఎంపిక', '1750s'), ('PLASSEY', 'ప్లాసీ', '1757'), ('REVENUE', 'ఆదాయం', '1765')]
def payoff(t, a, b, c_perm, c_tax):
    fr = fx.to_rgba(fx.blurred('T8', 0.30)); d = ImageDraw.Draw(fr)
    y = 560; xs = [260 + i * 330 for i in range(len(KNOTS))]
    kq = eo((t - a) / 0.5)
    typed(fr, L('HOW DID TRADE TURN INTO RULE?', 'వ్యాపారం పాలనగా ఎలా మారింది?'), W / 2, 170, t, a + 0.1, cps=32, size=40, col=GOLD, maxw=1500, anchor='ct')
    span = max(1.5, c_tax - c_perm)
    pts = bez((120, y), (W * 0.35, y - 30), (W * 0.65, y + 30), (W - 120, y), 120)
    kt = sm((t - c_perm + 0.3) / span)
    thread(d, pts, kt, w=5)
    for i, (en, te, yr) in enumerate(KNOTS):
        ki = eo((t - (c_perm + span * (xs[i] - 120) / (W - 240))) / 0.4)
        if ki <= 0: continue
        knot(d, xs[i], y, 16, ki)
        put(fr, text(yr, 'label', 26, MUTED), xs[i], y - 34, ki, 'cb')
        put(fr, text(L(en, te), 'label', 30, PAPER if i < len(KNOTS) - 1 else GOLD, maxw=300), xs[i], y + 34, ki, 'ct')
    if t > c_tax + 0.6:
        k = eo((t - c_tax - 0.6) / 0.5); put(fr, text('?', 'disp', 120, GOLD), W - 110, y - 10, k, 'cc')
        put(fr, text(L('SEASON 2', 'సీజన్ 2'), 'label', 28, MUTED), W - 110, y + 80, k, 'ct')
    return fr
