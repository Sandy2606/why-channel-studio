"""GOLD · 5/6 'Why do Indians trust gold more than banks?' — kinetic data + evidence, style v2."""
import sys, os, json, math, subprocess
import numpy as np, cairo
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
_argv = sys.argv; sys.argv = sys.argv[:1]
LANGV = os.environ.get('LANGV', 'en'); PLAT = os.environ.get('PLAT', 'yt')
sys.path.insert(0, '/home/claude/g3'); sys.path.insert(0, '/home/claude/rv')
import render3 as R3
import render2 as K
import host
sys.argv = _argv
W, H, FPS = 1080, 1920, 30
LEAD, TAIL = 0.15, 0.7
ROOT = '/home/claude/g5/'
CREAM, AMBER, AMBER2, INK = K.CREAM, K.AMBER, K.AMBER2, K.INK
prog, e_out, e_io, e_back, clamp = K.prog, K.e_out, K.e_io, K.e_back, K.clamp
font, mono, head, rrect = K.font, K.mono, K.head, K.rrect
glowdot, glass_dark, agrad = K.glowdot, K.glass_dark, K.agrad
surf_from_pil, torn, thread, board_bg = R3.surf_from_pil, R3.torn, R3.thread, R3.board_bg
def pill(c, *a, **k):
    if k.get('s', 1.0) <= 0.01: return
    K.pill(c, *a, **k)


# ---------------- voice / words / anchors ----------------
VFILE = ROOT + f'voice_{LANGV}_{PLAT}.wav'
VOICE_LEN = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', VFILE], capture_output=True, text=True).stdout)
DUR = LEAD + VOICE_LEN + TAIL
KEYS = {  # key: (EN word, nth, TE unit, frac or substring)
    'tonnes': ('tonnes', 1, 0, 0.7), 'add': ('add', 1, 1, 0.0),
    'america': ('america', 1, 2, 'America'), 'germany': ('germany', 1, 2, 'Germany'), 'italy': ('italy', 1, 2, 'Italy'),
    'france': ('france', 1, 2, 'France'), 'russia': ('russia', 1, 2, 'Russia'), 'china': ('china', 1, 2, 'China'),
    'switz': ('switzerland', 1, 2, 'Switzerland'), 'rbi': ('rbi', 1, 2, 'RBI'), 'japan': ('japan', 1, 2, 'Japan'), 'neth': ('netherlands', 1, 2, 'Netherlands'),
    'more': ('indian', 2, 3, 0.0), 'why': ('why', 1, 4, 0.0), 'trad': ('tradition', 1, 5, 0.3), 'math': ('math', 1, 6, 0.2),
    'say': ('say', 1, 7, 0.0), 'y2006': ('2006', 1, 7, 0.0), 'lakh': ('lakh', 1, 8, 0.7), 'nearly': ('nearly', 1, 9, 0.0),
    'same': ('same', 1, 10, 0.0), 'fd': ('fd', 1, 10, 0.25), 'k38': ('38,000', 1, 11, 0.3),
    'hidden': ('hidden', 1, 12, 0.0), 'oneprice': ('one', 1, 13, 0.0), 'rupee1': ('rupee', 1, 14, 0.0),
    'y2006b': ('2006', 2, 15, 0.0), 'd45': ('45', 1, 15, 0.6), 'd95': ('95', 1, 16, 0.5),
    'loses': ('loses', 1, 17, 0.3), 'gold2': ("doesn't", 2, 18, 0.0), 'protects': ('protects', 1, 19, 0.3),
    'cash': ('cash', 1, 20, 0.0), 'pledge': ('pledge', 1, 21, 0.0), 'minutes': ('minutes', 1, 21, 0.4), 'paper': ('paperwork', 1, 21, 0.8),
    'thats': ("that's", 1, 22, 0.0), 'second': ('second-biggest', 1, 22, 0.45), 'l16': ('16', 1, 23, 0.1),
    'next': ('next', 1, 24, 0.0), 'mom': ('mom', 1, 24, 'అమ్మ'), 'sister': ('sister', 1, 24, 'చెల్లి'), 'gf': ('girlfriend', 1, 24, 'girlfriend'),
    'wasting': ('wasting', 1, 25, 0.5), 'saving': ('saving', 1, 26, 0.0), 'future': ('future', 1, 26, 0.6),
    'full': ('full', 1, 27, 0.0), 'cta': ('if', 1, 28, 0.0), 'comment': ('comment', 1, 29, 0.0),
}
if LANGV == 'en':
    WORDS = json.load(open(ROOT + f'words_en_{PLAT}.json'))
    def norm(w): return w.strip('.,?!$%').lower()
    def T(word, n=1):
        k = 0
        for s, e, w in WORDS:
            if norm(w) == word or (word.isdigit() and norm(w).startswith(word)):
                k += 1
                if k == n: return s + LEAD
        raise KeyError(word)
    A = {key: T(w, n) for key, (w, n, u, f) in KEYS.items()}
else:
    _J = json.load(open(ROOT + f'words_te_{PLAT}.json')); WORDS = _J['words']; SS = _J['sent'] + [VOICE_LEN]; UN = _J['units']
    A = {}
    for key, (w, n, u, f) in KEYS.items():
        if isinstance(f, str): f = max(0, UN[u].find(f)) / len(UN[u])
        A[key] = SS[u] + f * (SS[u + 1] - SS[u]) + LEAD
A['end'] = DUR

CAP = []
for s, e, w in WORDS:
    w = {'tons': 'tonnes'}.get(w, w)
    CAP.append([s, e, w])
GROUPS = []; g = []; MAXC = 16 if LANGV == 'en' else 22
for i, (s, e, w) in enumerate(CAP):
    g.append((s + LEAD, e + LEAD, w))
    nxt = CAP[i + 1][0] if i + 1 < len(CAP) else 99
    if len(g) >= 3 or w[-1] in '.,?!…' or nxt - e > 0.35 or sum(len(x[2]) for x in g) > MAXC:
        GROUPS.append(g); g = []
if g: GROUPS.append(g)
K.GROUPS = GROUPS; R3.GROUPS = GROUPS; R3.TECACHE = {}
# ---------------- clippings (real print-to-PDF captures) ----------------
CJ = json.load(open(ROOT + 'clips.json')); CL = {}
def clip(name):
    if name not in CL:
        im = Image.open(ROOT + f'clip_{name}.png').convert('RGB')
        paper, pad = torn(im, seed=len(name))
        CL[name] = (surf_from_pil(paper), [(a + pad, b + pad, c_ + pad, d + pad) for a, b, c_, d in CJ[name]['hl']])
    return CL[name]
def draw_clip(c, name, cx, cy, wpx, t, t0, rot=-1.5, hl_t0=None, hl_dur=0.9, a=1.0, guide=True):
    if t < t0: return
    (sf, _), rects = clip(name)
    u = e_out(prog(t, t0, t0 + 0.4)); sc = wpx / sf.get_width(); w, h = sf.get_width(), sf.get_height()
    c.save(); c.translate(cx, cy + (1 - u) * 260); c.rotate(math.radians(rot + (1 - u) * 6)); c.scale(sc, sc)
    c.set_source_rgba(0, 0, 0, 0.45 * u * a); c.rectangle(-w / 2 + 10, -h / 2 + 18, w, h); c.fill()
    c.set_source_surface(sf, -w / 2, -h / 2); c.paint_with_alpha(u * a)
    tip = None
    if hl_t0 is not None and t >= hl_t0:
        tot = sum(r[2] - r[0] for r in rects); done = prog(t, hl_t0, hl_t0 + hl_dur) * tot
        for (x0, y0, x1, y1) in rects:
            wl = x1 - x0; f = clamp(done / wl); done -= wl
            if f <= 0: break
            xa, xb = -w / 2 + x0 - 3, -w / 2 + x0 + wl * f + 3
            c.set_source_rgba(1.0, 0.70, 0.14, 0.42); c.rectangle(xa, -h / 2 + y0 - 2, xb - xa, y1 - y0 + 4); c.fill()
            tip = c.user_to_device(xb, -h / 2 + (y0 + y1) / 2)
    for tx in (-w / 2 + 90, w / 2 - 90):
        c.save(); c.translate(tx, -h / 2 + 4); c.rotate(math.radians(-30 if tx < 0 else 30)); s2 = 1 / sc
        c.set_source_rgba(0.95, 0.89, 0.70, 0.75 * u); c.rectangle(-55 * s2, -14 * s2, 110 * s2, 28 * s2); c.fill(); c.restore()
    c.restore()
    if tip and guide and prog(t, hl_t0, hl_t0 + hl_dur) < 1: glowdot(c, tip[0], tip[1], 10)
def source_tag(c, txt, x, y, a=1.0):
    font(c, 'mono', 20); e = c.text_extents(txt)
    glass_dark(c, x - 14, y - 22, e.x_advance + 28, 40, 20, a); c.move_to(x, y + 6); c.set_source_rgba(*CREAM, a); c.show_text(txt)

# ---------------- photos ----------------
PH = {}
def photo(name):
    if name not in PH:
        im = Image.open(ROOT + name).convert('RGB')
        s = max(W * 1.12 / im.width, H * 1.12 / im.height); im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
        PH[name] = surf_from_pil(im)
    return PH[name][0]
def full_photo(c, name, t, t0, t1, z=(1.0, 1.08), focus=(0.5, 0.5), dim=0.3, label=None):
    sf = photo(name); u = e_io(prog(t, t0, t1)); zz = z[0] + (z[1] - z[0]) * u
    sw, sh = sf.get_width(), sf.get_height()
    c.save(); c.translate(W / 2, H / 2); c.scale(zz, zz); c.translate(-sw * focus[0], -sh * focus[1]); c.set_source_surface(sf, 0, 0); c.paint(); c.restore()
    if dim: c.set_source_rgba(0, 0, 0, dim); c.paint()
    g = cairo.LinearGradient(0, 1150, 0, H); g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0, 0, 0, 0.8); c.set_source(g); c.paint()
    if label: mono(c, label, W - 150, 1250, 18, (1, 1, 1), a=0.7, anchor='r', kind='mono')
def print_photo(c, name, cx, cy, w, t, t0, rot=3, caption=None):
    R3.ROOT = ROOT; R3.print_photo(c, name, cx, cy, w, t, t0, rot=rot, caption=caption)
# ---------------- graphics ----------------
def big_num(c, txt, x, y, px, t, t0, anchor='c'):
    if t < t0: return
    u = e_back(prog(t, t0, t0 + 0.3)); font(c, 'head', px); e = c.text_extents(txt)
    c.save(); c.translate(x, y); c.scale(u, u)
    xx = -e.width / 2 - e.x_bearing if anchor == 'c' else 0
    c.move_to(xx, px * 0.36); c.text_path(txt); c.set_line_join(cairo.LINE_JOIN_ROUND)
    c.set_source_rgba(0, 0, 0, 0.85); c.set_line_width(px * 0.1); c.stroke_preserve(); c.set_source(agrad(xx, 0, xx + e.width, 0)); c.fill(); c.restore()
def share_bar(c, y, label, frac, t, t0, col_grad=True):
    x0, w, h = 120, 840, 90
    glass_dark(c, x0, y, w, h, 45)
    u = e_out(prog(t, t0, t0 + 0.8)); fw = max(h, w * frac * u)
    rrect(c, x0, y, fw, h, 45); c.set_source(agrad(x0, 0, x0 + w, 0) if col_grad else cairo.SolidPattern(0.55, 0.55, 0.6)); c.fill()
    mono(c, label, x0, y - 30, 26, CREAM, anchor='l', kind='monob')
    if u > 0.2:
        font(c, 'head', 60); s = f'{int(round(frac * 100 * u))}%'; e = c.text_extents(s)
        c.move_to(x0 + fw - e.width - 30, y + h / 2 + 22); c.set_source_rgb(*INK); c.show_text(s)
def qmark(c, t, x, y, size, morph=0.0):
    host.draw(c, x, y, size, morph=morph, glow=0.8, eye='open', look=(0, 0), brow=0, tilt=3 * math.sin(t * 2), sq=1.0)

TAGS = None
def tag(c):
    global TAGS
    txt = 'GOLD · 5/6' if LANGV == 'en' else 'గోల్డ్ · 5/6'
    if LANGV == 'te':
        if TAGS is None:
            f = ImageFont.truetype('/home/claude/fonts/NotoSansTelugu.ttf', 26, layout_engine=ImageFont.Layout.RAQM)
            try: f.set_variation_by_name('Bold')
            except Exception: pass
            im = Image.new('RGBA', (300, 60), (0, 0, 0, 0)); ImageDraw.Draw(im).text((0, 30), txt, font=f, fill=(244, 241, 234, 255), anchor='lm')
            TAGS = surf_from_pil(im)
        glass_dark(c, 40, 92, 230, 54, 27); glowdot(c, 68, 119, 7); c.set_source_surface(TAGS[0], 88, 89); c.paint(); return
    font(c, 'monob', 24); e = c.text_extents(txt)
    glass_dark(c, 40, 92, e.x_advance + 80, 54, 27); glowdot(c, 68, 119, 7); c.move_to(88, 128); c.set_source_rgb(*CREAM); c.show_text(txt)

# ---------------- data ----------------
BANKS = [('us', 'USA', 8133, 'america'), ('de', 'GERMANY', 3351, 'germany'), ('it', 'ITALY', 2452, 'italy'), ('fr', 'FRANCE', 2437, 'france'),
         ('ru', 'RUSSIA', 2330, 'russia'), ('cn', 'CHINA', 2280, 'china'), ('ch', 'SWITZERLAND', 1040, 'switz'), ('in', 'INDIA · RBI', 880, 'rbi'),
         ('jp', 'JAPAN', 846, 'japan'), ('nl', 'NETHERLANDS', 612, 'neth')]
TOTAL10 = sum(b[2] for b in BANKS)
YEARS = list(range(2006, 2027))
GOLD = [8400, 9428, 12361, 15417, 18448, 24130, 29926, 28848, 27708, 26671, 30128, 29174, 30692, 35154, 47562, 47437, 51249, 58836, 77000, 133195, 149290]
USDINR = [45.3, 41.3, 43.5, 48.4, 45.7, 46.7, 53.4, 58.6, 61.0, 64.2, 67.2, 65.1, 68.4, 70.4, 74.1, 73.9, 78.6, 82.6, 83.7, 87.0, 95.0]

def rgb(h): return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
def flag(c, code, x, y, w, h, a=1.0):
    c.save(); rrect(c, x, y, w, h, 6); c.clip()
    def hb(cols):
        for i, col in enumerate(cols): c.set_source_rgba(*rgb(col), a); c.rectangle(x, y + h * i / len(cols), w, h / len(cols) + 1); c.fill()
    def vb(cols):
        for i, col in enumerate(cols): c.set_source_rgba(*rgb(col), a); c.rectangle(x + w * i / len(cols), y, w / len(cols) + 1, h); c.fill()
    if code == 'us':
        hb(['B22234', 'FFFFFF'] * 6 + ['B22234'])
        c.set_source_rgba(*rgb('3C3B6E'), a); c.rectangle(x, y, w * 0.42, h * 7 / 13); c.fill()
        c.set_source_rgba(1, 1, 1, a)
        for i in range(4):
            for j in range(3): c.arc(x + 6 + i * w * 0.1, y + 6 + j * h * 0.15, 1.6, 0, 2 * math.pi); c.fill()
    elif code == 'de': hb(['000000', 'DD0000', 'FFCE00'])
    elif code == 'it': vb(['009246', 'FFFFFF', 'CE2B37'])
    elif code == 'fr': vb(['0055A4', 'FFFFFF', 'EF4135'])
    elif code == 'ru': hb(['FFFFFF', '0039A6', 'D52B1E'])
    elif code == 'nl': hb(['AE1C28', 'FFFFFF', '21468B'])
    elif code == 'in':
        hb(['FF9933', 'FFFFFF', '138808']); c.set_source_rgba(*rgb('000080'), a); c.set_line_width(2); c.arc(x + w / 2, y + h / 2, h * 0.13, 0, 2 * math.pi); c.stroke()
    elif code == 'jp':
        hb(['FFFFFF']); c.set_source_rgba(*rgb('BC002D'), a); c.arc(x + w / 2, y + h / 2, h * 0.3, 0, 2 * math.pi); c.fill()
    elif code == 'ch':
        hb(['DA291C']); c.set_source_rgba(1, 1, 1, a); s = h * 0.6
        c.rectangle(x + w / 2 - s * 0.1, y + h / 2 - s / 2, s * 0.2, s); c.fill(); c.rectangle(x + w / 2 - s / 2, y + h / 2 - s * 0.1, s, s * 0.2); c.fill()
    elif code == 'cn':
        hb(['DE2910']); c.set_source_rgba(*rgb('FFDE00'), a); cx, cy, r = x + w * 0.2, y + h * 0.3, h * 0.17
        for i in range(10):
            ang = -math.pi / 2 + i * math.pi / 5; rr = r if i % 2 == 0 else r * 0.4
            (c.move_to if i == 0 else c.line_to)(cx + rr * math.cos(ang), cy + rr * math.sin(ang))
        c.close_path(); c.fill()
    c.restore()
    c.set_source_rgba(1, 1, 1, 0.25 * a); c.set_line_width(1.5); rrect(c, x, y, w, h, 6); c.stroke()

def bar_h(c, x, y, w, h, frac, u, grad=True, a=1.0):
    fw = max(h, w * frac * u)
    rrect(c, x, y, fw, h, h / 2)
    if grad: c.set_source(agrad(x, 0, x + w, 0))
    else: c.set_source_rgba(0.78, 0.76, 0.72, a)
    c.fill(); return fw

def txt(c, s, x, y, px, col=CREAM, a=1.0, kind='head', anchor='l'):
    font(c, kind, px); e = c.text_extents(s)
    xx = x if anchor == 'l' else (x - e.x_advance if anchor == 'r' else x - e.x_advance / 2)
    c.move_to(xx, y); c.set_source_rgba(*col, a); c.show_text(s); return e.x_advance

def fmt_inr(v):
    s = str(int(round(v)));
    if len(s) <= 3: return s
    last = s[-3:]; rest = s[:-3]; parts = []
    while len(rest) > 2: parts.insert(0, rest[-2:]); rest = rest[:-2]
    if rest: parts.insert(0, rest)
    return ','.join(parts) + ',' + last

def strike(c, x0, x1, y, u, col=AMBER, wdt=8):
    if u <= 0: return
    c.set_source_rgba(*col, 0.95); c.set_line_width(wdt); c.set_line_cap(cairo.LINE_CAP_ROUND)
    c.move_to(x0, y); c.line_to(x0 + (x1 - x0) * u, y); c.stroke(); c.set_line_cap(cairo.LINE_CAP_BUTT)

def chart_box(c, x, y, w, h, a=1.0):
    glass_dark(c, x - 30, y - 30, w + 60, h + 90, 30, a)
    c.set_source_rgba(1, 1, 1, 0.08 * a); c.set_line_width(1)
    for i in range(5): c.move_to(x, y + h * i / 4); c.line_to(x + w, y + h * i / 4)
    c.stroke()

def poly(c, pts, u, col=None, wdt=7, grad=None):
    n = len(pts) - 1; k = u * n; i = int(k)
    if u <= 0: return None
    sub = pts[:i + 1]
    if i < n: f = k - i; p0, p1 = pts[i], pts[i + 1]; sub = sub + [(p0[0] + (p1[0] - p0[0]) * f, p0[1] + (p1[1] - p0[1]) * f)]
    c.set_line_width(wdt); c.set_line_join(cairo.LINE_JOIN_ROUND); c.set_line_cap(cairo.LINE_CAP_ROUND)
    c.move_to(*sub[0]); [c.line_to(*p) for p in sub[1:]]
    if grad is not None: c.set_source(grad)
    else: c.set_source_rgba(*col)
    c.stroke(); c.set_line_cap(cairo.LINE_CAP_BUTT); return sub[-1]

def stopwatch(c, x, y, r, frac, a=1.0):
    c.save(); c.translate(x, y)
    c.set_source_rgba(*CREAM, a); c.rectangle(-14, -r - 40, 28, 30); c.fill(); c.rectangle(-30, -r - 52, 60, 16); c.fill()
    c.set_line_width(14); c.arc(0, 0, r, 0, 2 * math.pi); c.stroke()
    c.move_to(0, 0); c.arc(0, 0, r - 18, -math.pi / 2, -math.pi / 2 + 2 * math.pi * frac); c.close_path(); c.set_source(agrad(-r, 0, r, 0)); c.fill()
    c.set_source_rgba(*CREAM, a); c.set_line_width(6); ang = -math.pi / 2 + 2 * math.pi * frac
    c.move_to(0, 0); c.line_to((r - 30) * math.cos(ang), (r - 30) * math.sin(ang)); c.stroke(); c.arc(0, 0, 10, 0, 2 * math.pi); c.fill()
    c.restore()

def note(c, x, y, w, a=1.0):
    h = w * 0.48; c.save(); c.translate(x, y)
    rrect(c, -w / 2, -h / 2, w, h, 10); c.set_source_rgba(0.55, 0.72, 0.55, a); c.fill()
    c.set_source_rgba(0.2, 0.35, 0.22, a); c.set_line_width(3); rrect(c, -w / 2 + 10, -h / 2 + 10, w - 20, h - 20, 6); c.stroke()
    font(c, 'head', h * 0.5); e = c.text_extents('₹'); c.move_to(-e.width / 2 - e.x_bearing, h * 0.18); c.show_text('₹'); c.restore()

def card_title(c, l1, l2, y, u, sub=None):
    c.save(); c.translate(0, (1 - u) * 40); glass_dark(c, 90, y, 900, 250 if sub else 210, 34, u)
    c.set_source_rgba(*AMBER, u); c.rectangle(112, y + 25, 6, 160 if not sub else 200); c.fill()
    head(c, l1, 150, y + 85, 58, CREAM, a=u, anchor='l', shadow=False)
    head(c, l2, 150, y + 160, 58, AMBER, a=u, anchor='l', shadow=False)
    if sub: mono(c, sub, 150, y + 215, 22, CREAM, a=0.7 * u, anchor='l', kind='mono')
    c.restore()

# ---------------- frame ----------------
def frame(t):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s)
    board_bg(c, t)
    # 1. hook: 25,000 tonnes in Indian homes
    if t < A['add'] - 0.05:
        full_photo(c, 'bangles.jpg', t, 0, A['add'], z=(1.12, 1.02), focus=(0.5, 0.35), dim=0.5, label='Ravi Gond · Pexels')
        big_num(c, '25,000', W / 2, 380, 230, t, -0.3)
        pill(c, 'TONNES OF GOLD', W / 2, 560, 44, AMBER, s=e_back(prog(t, 0.25, 0.55)))
        mono(c, 'SITTING IN INDIAN HOMES', W / 2, 660, 28, CREAM, a=prog(t, 0.6, 0.9), kind='monob')
        if t >= A['tonnes'] - 0.3:
            draw_clip(c, 'bs', W / 2, 950, 980, t, A['tonnes'] - 0.3, rot=-1.2, hl_t0=A['tonnes'] + 0.1, hl_dur=1.2)
            source_tag(c, 'BUSINESS STANDARD (VIA ICMAI DIGEST) · MAR 2025', 70, 1170, a=prog(t, A['tonnes'], A['tonnes'] + 0.3))
    # 2. top-10 central banks race, then the totals
    elif t < A['why'] - 0.05:
        if t < A['more'] - 0.05:
            mono(c, 'TOP 10 CENTRAL BANKS · GOLD (TONNES)', W / 2, 250, 28, AMBER, kind='monob', a=prog(t, A['add'], A['add'] + 0.3))
            run = 0
            for i, (code, name, tn, key) in enumerate(BANKS):
                t0 = A[key] - 0.1
                if t < t0: continue
                u = e_out(prog(t, t0, t0 + 0.35)); y = 310 + i * 96
                c.save(); c.translate((1 - u) * -120, 0)
                flag(c, code, 60, y, 96, 64, u)
                txt(c, name, 180, y + 44, 34, CREAM, u)
                fw = bar_h(c, 520, y + 14, 400, 36, tn / 8133, e_out(prog(t, t0, t0 + 0.6)))
                txt(c, f'{tn:,}', 520 + fw + 14, y + 45, 30, AMBER, u, kind='monob')
                c.restore(); run += tn * e_out(prog(t, t0, t0 + 0.6))
            if t >= A['america']:
                glass_dark(c, 140, 1290, 800, 80, 40); mono(c, f'RUNNING TOTAL  {int(run):,} T', W / 2, 1342, 32, CREAM, kind='monob')
        else:
            u = e_out(prog(t, A['more'] - 0.05, A['more'] + 0.3))
            mono(c, 'WHO HOLDS MORE GOLD?', W / 2, 330, 30, AMBER, kind='monob', a=u)
            for j, (lab, val, grad, t0) in enumerate((('TOP 10 CENTRAL BANKS, COMBINED', TOTAL10, False, A['more'] - 0.05), ('INDIAN HOMES', 25000, True, A['more'] + 0.5))):
                y = 520 + j * 300; v = e_out(prog(t, t0, t0 + 0.7))
                if t < t0: continue
                mono(c, lab, 120, y - 30, 28, CREAM, anchor='l', kind='monob', a=prog(t, t0, t0 + 0.2))
                glass_dark(c, 120, y, 840, 110, 55)
                fw = bar_h(c, 120, y, 840 * 25000 / 25000 * 0.98, 110, val / 25000, v, grad=grad)
                font(c, 'head', 64); sv = f'≈{int(round(val * v, -2)):,} T' if not grad else f'{int(round(val * v, -2)):,} T'
                e = c.text_extents(sv); c.move_to(120 + fw - e.x_advance - 36, y + 78); c.set_source_rgb(*INK); c.show_text(sv)
            if t >= A['more'] + 1.1: pill(c, 'INDIAN HOMES WIN', W / 2, 1120, 44, AMBER, s=e_back(prog(t, A['more'] + 1.1, A['more'] + 1.4)))
            mono(c, 'CENTRAL BANKS: WORLD GOLD COUNCIL DATA · 10TH PLACE VARIES BY DATE', W / 2, 1250, 17, CREAM, a=0.6 * u, kind='mono')
    # 3. why trust gold more than a bank?
    elif t < A['say'] - 0.05:
        full_photo(c, 'rupee-notes.jpg', t, A['why'], A['say'], z=(1.05, 1.15), focus=(0.5, 0.5), dim=0.62, label='Ravi Roshan · Pexels')
        card_title(c, 'WHY TRUST GOLD', 'MORE THAN A BANK?', 330, e_out(prog(t, A['why'] - 0.05, A['why'] + 0.3)))
        if t < A['math'] - 0.1: qmark(c, t, W / 2, 1090, 290)
        if t >= A['trad'] - 0.2:
            u = e_back(prog(t, A['trad'] - 0.2, A['trad'] + 0.1)); pill(c, 'JUST TRADITION?', W / 2, 760, 40, CREAM, s=u)
            font(c, 'head', 40); e = c.text_extents('JUST TRADITION?'); strike(c, W / 2 - e.width / 2 - 20, W / 2 + e.width / 2 + 20, 760, prog(t, A['trad'] + 0.35, A['trad'] + 0.7))
        if t >= A['math'] - 0.1:
            big_num(c, "IT'S MATH.", W / 2, 1000, 150, t, A['math'] - 0.1)
    # 4. 10,000 in 2006 -> 1.77 lakh
    elif t < A['same'] - 0.05:
        pill(c, '₹10,000 IN GOLD · 2006', W / 2, 260, 38, CREAM, s=e_back(prog(t, A['say'] - 0.05, A['say'] + 0.25)))
        u = e_io(prog(t, A['y2006'], A['lakh'] + 0.2)); val = 10000 * (1 + (149290 / 8400 - 1) * u)
        val = 177000 if u >= 1 else val
        big_num(c, '₹' + fmt_inr(round(val, -2)), W / 2, 420, 150, t, A['say'])
        X0, Y0, CW, CH = 120, 560, 840, 460; chart_box(c, X0, Y0, CW, CH)
        pts = [(X0 + CW * i / (len(YEARS) - 1), Y0 + CH - CH * g / 150000) for i, g in enumerate(GOLD)]
        tip = poly(c, pts, u, grad=agrad(X0, 0, X0 + CW, 0), wdt=8)
        mono(c, '2006', X0, Y0 + CH + 40, 22, CREAM, anchor='l', kind='mono'); mono(c, 'TODAY', X0 + CW, Y0 + CH + 40, 22, CREAM, anchor='r', kind='mono')
        mono(c, 'GOLD · ₹ PER 10 G', X0, Y0 + 10, 22, AMBER, anchor='l', kind='monob')
        mono(c, '₹8,400', X0 + 10, Y0 + CH - 30, 26, CREAM, anchor='l', kind='monob')
        if tip: glowdot(c, tip[0], tip[1], 12)
        if u >= 1: mono(c, '₹1,49,290', X0 + CW - 60, pts[-1][1] + 22, 30, AMBER, anchor='r', kind='monob')
        if t >= A['nearly'] - 0.1: pill(c, 'NEARLY 18×', 700, 820, 50, AMBER, s=e_back(prog(t, A['nearly'] - 0.1, A['nearly'] + 0.2)))
        draw_clip(c, 'abc', W / 2, 1195, 1000, t, A['y2006'] + 0.2, rot=-1.0, hl_t0=A['y2006'] + 0.5, hl_dur=1.0)
        if t >= A['lakh']: mono(c, 'ADITYA BIRLA CAPITAL · TODAY: PSU CONNECT, 13 OCT 2026', W / 2, 1300, 18, CREAM, a=0.75 * prog(t, A['lakh'], A['lakh'] + 0.3), kind='mono')
    # 5. vs FD
    elif t < A['hidden'] - 0.05:
        mono(c, '₹10,000 IN 2006 → TODAY', W / 2, 250, 32, AMBER, kind='monob')
        base = 1180; hmax = 760
        for j, (lab, val, sv, grad, t0, sub) in enumerate((('GOLD', 177000, '₹1.77 LAKH', True, A['same'] - 0.05, ''), ('BANK FD', 38000, '₹38,000', False, A['fd'], 'AT 7% A YEAR'))):
            if t < t0: continue
            x = 200 + j * 400; v = e_out(prog(t, t0, t0 + 0.7)); hh = max(40, hmax * val / 177000 * v)
            rrect(c, x, base - hh, 280, hh, 26); c.set_source(agrad(x, 0, x + 280, 0) if grad else cairo.SolidPattern(0.62, 0.62, 0.66)); c.fill()
            head(c, lab, x + 140, base + 70, 50, CREAM, shadow=False)
            if sub: mono(c, sub, x + 140, base + 115, 22, CREAM, a=0.7, kind='mono')
            if v > 0.6 and (j == 0 or t >= A['k38'] - 0.2): head(c, sv, x + 140, base - hh - 36, 52, AMBER if grad else CREAM, shadow=False)
        if t >= A['k38'] + 0.4: mono(c, 'FD MATH: ₹10,000 AT 7% FOR 20 YEARS ≈ ₹38,700', W / 2, 1330, 20, CREAM, a=0.7 * prog(t, A['k38'] + 0.4, A['k38'] + 0.7), kind='mono')
    # 6. hidden reason: one world price, the rupee doesn't
    elif t < A['loses'] - 0.05:
        pill(c, "THE HIDDEN REASON", W / 2, 240, 38, CREAM, s=e_back(prog(t, A['hidden'] - 0.05, A['hidden'] + 0.25)))
        if t >= A['oneprice'] - 0.1:
            u = e_out(prog(t, A['oneprice'] - 0.1, A['oneprice'] + 0.3))
            R3.gold_bar(c, W / 2, 470, 0.85 * u, glow=0.9)
            mono(c, 'ONE PRICE FOR THE WHOLE WORLD', W / 2, 620, 30, AMBER, a=u, kind='monob')
        if t >= A['rupee1'] - 0.1 and t < A['y2006b'] - 0.1:
            u = e_back(prog(t, A['rupee1'] - 0.1, A['rupee1'] + 0.2)); pill(c, 'THE RUPEE? IT MOVES.', W / 2, 900, 46, CREAM, s=u)
        if t >= A['y2006b'] - 0.1:
            u = e_out(prog(t, A['y2006b'] - 0.1, A['y2006b'] + 0.3)); flip = e_io(prog(t, A['d95'] - 0.15, A['d95'] + 0.2))
            c.save(); c.translate(0, (1 - u) * 40); glass_dark(c, 110, 740, 860, 480, 40, u)
            mono(c, '2006' if flip < 0.5 else 'TODAY', W / 2, 820, 30, AMBER, a=u, kind='monob')
            head(c, '$1 =', W / 2, 960, 110, CREAM, a=u, shadow=False)
            c.save(); c.translate(W / 2, 1110); c.scale(1, abs(1 - 2 * flip) if flip < 1 else 1)
            big_num(c, '₹45' if flip < 0.5 else '₹95', 0, 0, 150, t, A['d45'] - 0.15 if flip < 0.5 else -1); c.restore()
            c.restore()
    # 7. rupee falls, gold holds
    elif t < A['cash'] - 0.05:
        X0, Y0, CW, CH = 120, 330, 840, 760; chart_box(c, X0, Y0, CW, CH)
        lo, hi = math.log(0.3), math.log(25)
        def yv(v): return Y0 + CH - CH * (math.log(v) - lo) / (hi - lo)
        u1 = e_io(prog(t, A['loses'] - 0.1, A['loses'] + 1.4)); u2 = e_io(prog(t, A['gold2'] - 0.1, A['gold2'] + 1.4))
        base = yv(1.0); c.set_source_rgba(1, 1, 1, 0.3); c.set_dash([8, 8]); c.set_line_width(2); c.move_to(X0, base); c.line_to(X0 + CW, base); c.stroke(); c.set_dash([])
        mono(c, 'START: 2006', X0 + 10, base - 16, 20, CREAM, anchor='l', kind='mono', a=0.7)
        rp = [(X0 + CW * i / 20, yv(45.3 / r)) for i, r in enumerate(USDINR)]
        gp = [(X0 + CW * i / 20, yv(g / 8400)) for i, g in enumerate(GOLD)]
        tp = poly(c, rp, u1, col=(0.75, 0.75, 0.8, 1), wdt=7)
        if tp:
            glowdot(c, *tp, 10)
            if u1 >= 1: mono(c, 'YOUR RUPEE vs $ · −52%', X0 + CW - 10, tp[1] + 50, 26, CREAM, anchor='r', kind='monob')
        tg = poly(c, gp, u2, grad=agrad(X0, 0, X0 + CW, 0), wdt=8)
        if tg:
            glowdot(c, *tg, 12)
            if u2 >= 1: mono(c, 'YOUR GOLD in ₹ · 18×', X0 + CW - 10, tg[1] + 50, 26, AMBER, anchor='r', kind='monob')
        mono(c, '2006', X0, Y0 + CH + 40, 22, CREAM, anchor='l', kind='mono'); mono(c, 'TODAY', X0 + CW, Y0 + CH + 40, 22, CREAM, anchor='r', kind='mono')
        if t >= A['protects'] - 0.1: pill(c, 'IT QUIETLY PROTECTS YOUR SAVINGS', W / 2, 1230, 34, AMBER, s=e_back(prog(t, A['protects'] - 0.1, A['protects'] + 0.2)))
    # 8. cash fast: pledge -> loan in minutes
    elif t < A['thats'] - 0.05:
        full_photo(c, 'rupee-notes.jpg', t, A['cash'], A['thats'], z=(1.15, 1.25), focus=(0.4, 0.5), dim=0.75)
        pill(c, 'NEED CASH FAST?', W / 2, 260, 44, CREAM, s=e_back(prog(t, A['cash'] - 0.05, A['cash'] + 0.25)))
        if t >= A['pledge'] - 0.1:
            u = e_out(prog(t, A['pledge'] - 0.1, A['pledge'] + 0.3)); R3.gold_bar(c, 250, 560, 0.55 * u, glow=0.7)
            mono(c, 'PLEDGE GOLD', 250, 680, 26, AMBER, a=u, kind='monob')
            c.set_source_rgba(*CREAM, u); c.set_line_width(8); c.move_to(420, 560); c.line_to(640, 560); c.stroke()
            c.move_to(640, 530); c.line_to(680, 560); c.line_to(640, 590); c.close_path(); c.fill()
        if t >= A['minutes'] - 0.3:
            u = e_out(prog(t, A['minutes'] - 0.3, A['minutes']))
            note(c, 830, 545, 240 * u, u); note(c, 850, 575, 240 * u, u); mono(c, 'CASH LOAN', 840, 680, 26, CREAM, a=u, kind='monob')
        if t >= A['pledge']:
            stopwatch(c, W / 2, 940, 150, clamp((t - A['pledge']) / 2.2) * 0.25)
        if t >= A['minutes']: pill(c, 'IN MINUTES', W / 2, 1160, 44, AMBER, s=e_back(prog(t, A['minutes'], A['minutes'] + 0.25)))
        if t >= A['paper'] - 0.1: pill(c, 'VERY LITTLE PAPERWORK', W / 2, 1270, 34, CREAM, s=e_back(prog(t, A['paper'] - 0.1, A['paper'] + 0.2)))
    # 9. gold loans: #2 retail loan, 16 lakh crore (Mint)
    elif t < A['next'] - 0.05:
        draw_clip(c, 'mint', W / 2, 520, 1000, t, A['thats'] - 0.05, rot=-1.0, hl_t0=A['second'], hl_dur=1.2)
        source_tag(c, 'MINT · APR 15, 2026', 90, 720, a=prog(t, A['thats'], A['thats'] + 0.3))
        if t >= A['second'] + 0.3: pill(c, '#2 RETAIL LOAN · AFTER HOME LOANS', W / 2, 830, 34, AMBER, s=e_back(prog(t, A['second'] + 0.3, A['second'] + 0.6)))
        draw_clip(c, 'mint16', W / 2, 980, 960, t, A['l16'] - 0.4, rot=1.0, hl_t0=A['l16'] - 0.1, hl_dur=0.8)
        big_num(c, '₹16 LAKH CRORE', W / 2, 1180, 110, t, A['l16'] + 0.2)
    # 10. mom / sister / girlfriend -> saving for the future
    elif t < A['full'] - 0.1:
        dimmed = prog(t, A['saving'] - 0.2, A['saving'] + 0.2)
        print_photo(c, 'mother.jpg', 330, 470, 480, t, A['mom'] - 0.1, rot=-4, caption='MOM')
        print_photo(c, 'young-woman.jpg', 800, 600, 300, t, A['sister'] - 0.1, rot=4, caption='SISTER')
        print_photo(c, 'couple.jpg', 380, 1000, 300, t, A['gf'] - 0.1, rot=-2, caption='GIRLFRIEND')
        thread(c, 420, 640, 760, 380, t, A['sister'], 0.5); thread(c, 380, 760, 400, 820, t, A['gf'], 0.5)
        if t >= A['wasting'] - 0.2 and t < A['saving'] - 0.1:
            u = e_back(prog(t, A['wasting'] - 0.2, A['wasting'] + 0.1)); pill(c, 'WASTING MONEY?', 790, 1150, 32, CREAM, s=u)
            font(c, 'head', 32); e = c.text_extents('WASTING MONEY?'); strike(c, 790 - e.width / 2 - 20, 790 + e.width / 2 + 20, 1150, prog(t, A['wasting'] + 0.3, A['wasting'] + 0.6))
        if dimmed > 0:
            c.set_source_rgba(0, 0, 0, 0.6 * dimmed); c.paint()
            card_title(c, "THEY'RE SAVING IT.", 'FOR THE FUTURE.', 470, e_out(dimmed))
            qmark(c, t, W / 2, 1060, 360, morph=e_io(prog(t, A['future'], A['future'] + 0.5)))
    # 11. board + CTA
    else:
        print_photo(c, 'bangles.jpg', 250, 470, 260, t, A['full'] - 0.1, rot=-4)
        draw_clip(c, 'bs', 660, 360, 640, t, A['full'], rot=3, guide=False)
        draw_clip(c, 'mint', 620, 690, 660, t, A['full'] + 0.15, rot=-2, guide=False)
        draw_clip(c, 'abc', 520, 930, 640, t, A['full'] + 0.3, rot=1.5, guide=False)
        thread(c, 380, 560, 520, 420, t, A['full'] + 0.3, 0.5); thread(c, 770, 460, 640, 640, t, A['full'] + 0.5, 0.5); thread(c, 330, 640, 300, 920, t, A['full'] + 0.7, 0.5)
        if t >= A['comment'] - 0.1:
            u2 = e_back(prog(t, A['comment'] - 0.1, A['comment'] + 0.2))
            c.save(); c.translate(W / 2, 1150); c.scale(u2, u2); glass_dark(c, -400, -90, 800, 180, 40)
            head(c, 'GOT A WHY?', 0, -26, 60, CREAM, shadow=False); mono(c, 'COMMENT IT · WE FIND THE ANSWER', 0, 42, 24, AMBER, kind='monob'); c.restore()
    (K.captions(c, t, y=1440) if LANGV == 'en' else R3.te_captions(c, t, y=1440))
    tag(c)
    return s

def main(part=0, parts=1, out=None, still=None):
    if still is not None:
        os.makedirs(ROOT + 'stills', exist_ok=True)
        for tt in still: frame(tt).write_to_png(f'{ROOT}stills/{LANGV}_{tt:05.2f}.png')
        return
    n = int(DUR * FPS); a = n * part // parts; b = n * (part + 1) // parts
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgra', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
    for i in range(a, b):
        s = frame(i / FPS); s.flush(); p.stdin.write(bytes(s.get_data()))
    p.stdin.close(); p.wait()

if __name__ == '__main__':
    if sys.argv[1] == 'still': main(still=[float(x) for x in sys.argv[2:]])
    elif sys.argv[1] == 'anchors': print({k: round(v, 2) for k, v in A.items()})
    else: main(int(sys.argv[1]), int(sys.argv[2]), sys.argv[3])
