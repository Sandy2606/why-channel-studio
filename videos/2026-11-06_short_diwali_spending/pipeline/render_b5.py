"""DIWALI · 5/6 '₹7 lakh crore of festive trade: where does it go' — style v2, loops into its own opening."""
import sys, os, json, math, subprocess
import numpy as np, cairo
from PIL import Image, ImageDraw, ImageFont, ImageFilter
_argv = sys.argv; sys.argv = sys.argv[:1]
LANGV = os.environ.get('LANGV', 'en'); PLAT = os.environ.get('PLAT', 'yt')
sys.path.insert(0, '/home/claude/g3'); sys.path.insert(0, '/home/claude/rv')
import render3 as R3
import render2 as K
sys.argv = _argv
W, H, FPS = 1080, 1920, 30
LEAD, TAIL = 0.15, 0.30
ROOT = '/home/claude/b5/'
CREAM, AMBER, AMBER2, INK = K.CREAM, K.AMBER, K.AMBER2, K.INK
prog, e_out, e_io, e_back, clamp = K.prog, K.e_out, K.e_io, K.e_back, K.clamp
font, rrect = K.font, K.rrect
glowdot, glass_dark, agrad = K.glowdot, K.glass_dark, K.agrad
surf_from_pil, torn, board_bg = R3.surf_from_pil, R3.torn, R3.board_bg
import te_text as TT
def head(c, txt, x, y, px, col=CREAM, a=1.0, anchor='c', shadow=True):
    if LANGV == 'te' and txt in TT.TR: return TT.draw(c, TT.TR[txt], x, y, px * 0.80, col, a, anchor, 'Black', stroke=3 if shadow else 0)
    return K.head(c, txt, x, y, px, col, a, anchor, shadow)
def mono(c, txt, x, y, px, col=AMBER, a=1.0, anchor='c', kind='monob'):
    if LANGV == 'te' and txt in TT.TR: return TT.draw(c, TT.TR[txt], x, y, px * (1.15 if px < 30 else 0.95), col, a, anchor, 'Bold')
    return K.mono(c, txt, x, y, px, col, a, anchor, kind)
def pill(c, txt, cx, cy, px=34, fill=AMBER, col=K.BLACK, a=1.0, s=1.0, kind='head'):
    if s <= 0.01 or a <= 0: return
    if LANGV == 'te' and txt in TT.TR:
        sf, _ = TT.surf(TT.TR[txt], px * 0.95, INK if fill == AMBER else CREAM, 'Bold'); w = sf.get_width() + px * 1.1; h = px * 1.85
        c.save(); c.translate(cx, cy); c.scale(s, s)
        if fill == AMBER: rrect(c, -w / 2, -h / 2, w, h, h / 2); c.set_source_rgba(*AMBER, a); c.fill()
        else: glass_dark(c, -w / 2, -h / 2, w, h, h / 2, a)
        c.set_source_surface(sf, -sf.get_width() / 2, -sf.get_height() / 2); c.paint_with_alpha(a); c.restore(); return
    K.pill(c, txt, cx, cy, px, fill, col, a, s, kind)

# ---------------- voice / words / anchors ----------------
VFILE = ROOT + f'voice_{LANGV}.wav'
VOICE_LEN = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', VFILE], capture_output=True, text=True).stdout)
DUR = LEAD + VOICE_LEN + TAIL
MK = {k: (a + LEAD, b + LEAD) for k, (a, b) in json.load(open(ROOT + f'marks_{LANGV}.json')).items()}
def S(k): return MK[k][0]
def E(k): return MK[k][1]
if LANGV == 'en':
    WORDS = json.load(open(ROOT + 'words_en.json'))
else:
    WORDS = json.load(open(ROOT + 'words_te.json'))['words']
def AT(line, en, te, n=1, off=0.0):
    sub = en if LANGV == 'en' else te
    if sub is None: return S(line) + off
    if isinstance(sub, float): return S(line) + sub * (E(line) - S(line)) + off
    k = 0
    for s, e, w, ln in WORDS:
        if ln == line and sub.lower() in w.lower():
            k += 1
            if k == n: return s + LEAD + off
    raise KeyError((LANGV, line, sub))

# ---------------- anchors ----------------
A = {
    'trade1': AT('1', 'trade', 'వ్యాపారం'), 'where': AT('1', 'Where', 'ఎక్కడికి'),
    'notgold': AT('3', 'gold', 'కాదు'), 'groc': AT('3', 'Groceries', 'కిరాణా'),
    'gold4': AT('4', 'Gold', 'బంగారం'), 'elec': AT('4', 'Electronics', 'Electronics'),
    'appl': AT('5', 'appliances', 'appliances'),
    'decor': AT('6', 'décor', 'అలంకరణ'), 'sweets': AT('6', 'sweets', 'స్వీట్లకి'),
    'services': AT('7', 'Services', 'services'), 'k80': AT('7', '80,000', '80,000'),
    'lakshmi': AT('8', 'Lakshmi', 'లక్ష్మి'), 'busiest': AT('8', 'busiest', 'busy'),
    'p85': AT('9', '85', '85'),
    'j50': AT('10', '50', '50'),
    'small': AT('11', 'small', 'చిన్న'),
    'tomorrow': S('12'), 'loop': S('L'),
}
A['end'] = DUR
# captions (same grouping as Gold 6)
GROUPS = []; g = []; MAXC = 16 if LANGV == 'en' else 22
CAP = [[s, e, w] for s, e, w, ln in WORDS]
for i, (s, e, w) in enumerate(CAP):
    g.append((s + LEAD, e + LEAD, w))
    nxt = CAP[i + 1][0] if i + 1 < len(CAP) else 99
    if len(g) >= 3 or w[-1] in '.,?!…:' or nxt - e > 0.35 or sum(len(x[2]) for x in g) > MAXC:
        GROUPS.append(g); g = []
if g: GROUPS.append(g)
K.GROUPS = GROUPS; R3.GROUPS = GROUPS; R3.TECACHE = {}

# ---------------- clippings: evidence flashes (rest of the clipping dims) ----------------
CJ = json.load(open(ROOT + 'clips.json')); CL = {}
def clip(name):
    if name not in CL:
        im = Image.open(ROOT + f'clip_{name}.png').convert('RGB')
        paper, pad = torn(im, seed=len(name))
        CL[name] = (surf_from_pil(paper), [(a + pad, b + pad, c_ + pad, d + pad) for a, b, c_, d in CJ[name]['hl']])
    return CL[name]
def draw_clip(c, name, cx, cy, wpx, t, t0, rot=-1.0, hl_t0=None, hl_dur=0.9, a=1.0, focus=True, t1=None):
    if t < t0: return
    if t1 is not None and t > t1 + 0.25: return
    (sf, _), rects = clip(name)
    u = e_out(prog(t, t0, t0 + 0.35)); v = 1 - prog(t, t1, t1 + 0.25) if t1 is not None else 1.0
    sc = wpx / sf.get_width() * (1 + 0.04 * prog(t, t0, t0 + 3)); w, h = sf.get_width(), sf.get_height()
    c.save(); c.translate(cx, cy + (1 - u) * 200); c.rotate(math.radians(rot + (1 - u) * 5)); c.scale(sc, sc)
    c.set_source_rgba(0, 0, 0, 0.45 * u * a * v); c.rectangle(-w / 2 + 10, -h / 2 + 16, w, h); c.fill()
    c.set_source_surface(sf, -w / 2, -h / 2); c.paint_with_alpha(u * a * v)
    tip = None
    if hl_t0 is not None and t >= hl_t0 and rects:
        tot = sum(r[2] - r[0] for r in rects); k = prog(t, hl_t0, hl_t0 + hl_dur); done = k * tot
        if focus:  # dim everything except the quoted words
            d = 0.42 * e_io(prog(t, hl_t0, hl_t0 + 0.3)) * v
            c.set_fill_rule(cairo.FILL_RULE_EVEN_ODD); c.rectangle(-w / 2, -h / 2, w, h)
            for (x0, y0, x1, y1) in rects: c.rectangle(-w / 2 + x0 - 6, -h / 2 + y0 - 6, x1 - x0 + 12, y1 - y0 + 12)
            c.set_source_rgba(0.05, 0.05, 0.07, d); c.fill(); c.set_fill_rule(cairo.FILL_RULE_WINDING)
        for (x0, y0, x1, y1) in rects:
            wl = x1 - x0; f = clamp(done / wl); done -= wl
            if f <= 0: break
            xa, xb = -w / 2 + x0 - 3, -w / 2 + x0 + wl * f + 3
            c.set_source_rgba(1.0, 0.70, 0.14, 0.45 * v); c.rectangle(xa, -h / 2 + y0 - 2, xb - xa, y1 - y0 + 4); c.fill()
            tip = c.user_to_device(xb, -h / 2 + (y0 + y1) / 2)
    for tx in (-w / 2 + 70, w / 2 - 70):
        c.save(); c.translate(tx, -h / 2 + 4); c.rotate(math.radians(-30 if tx < 0 else 30)); s2 = 1 / sc
        c.set_source_rgba(0.95, 0.89, 0.70, 0.75 * u * v); c.rectangle(-55 * s2, -14 * s2, 110 * s2, 28 * s2); c.fill(); c.restore()
    c.restore()
    if tip and prog(t, hl_t0, hl_t0 + hl_dur) < 1: glowdot(c, tip[0], tip[1], 10)
def source_tag(c, txt, x, y, a=1.0):
    if a <= 0: return
    font(c, 'mono', 20); e = c.text_extents(txt)
    glass_dark(c, x - 14, y - 22, e.x_advance + 28, 40, 20, a); c.move_to(x, y + 6); c.set_source_rgba(*CREAM, a); c.show_text(txt)

# ---------------- graphics ----------------
def big_num(c, txt, x, y, px, t, t0, a=1.0, strike=0.0):
    if t < t0: return
    u = e_back(prog(t, t0, t0 + 0.3))
    if LANGV == 'te' and txt in TT.TR:
        c.save(); c.translate(x, y); c.scale(max(0.01, u), max(0.01, u)); TT.draw(c, TT.TR[txt], 0, 0, px * 0.78, AMBER, a, 'c', 'Black', stroke=6); c.restore(); return
    font(c, 'head', px); e = c.text_extents(txt)
    c.save(); c.translate(x, y); c.scale(max(0.01, u), max(0.01, u))
    xx = -e.width / 2 - e.x_bearing
    c.move_to(xx, px * 0.36); c.text_path(txt); c.set_line_join(cairo.LINE_JOIN_ROUND)
    c.set_source_rgba(0, 0, 0, 0.85 * a); c.set_line_width(px * 0.1); c.stroke_preserve()
    if a < 1: c.set_source_rgba(*CREAM, a)
    else: c.set_source(agrad(xx, 0, xx + e.width, 0))
    c.fill()
    if strike > 0:
        c.set_source_rgba(*CREAM, 0.95); c.set_line_width(px * 0.08); c.set_line_cap(cairo.LINE_CAP_ROUND)
        c.move_to(xx - 10, 0); c.line_to(xx - 10 + (e.width + 20) * e_out(strike), 0); c.stroke()
    c.restore()
def stamp_txt(c, txt_, x, y, t, t0, px=96, rot=-10, col=CREAM, a=1.0):
    if t < t0: return
    u = prog(t, t0, t0 + 0.18); sc = 1.8 - 0.8 * e_out(u)
    c.save(); c.translate(x, y); c.rotate(math.radians(rot)); c.scale(sc, sc)
    if LANGV == 'te' and txt_ in TT.TR:
        sf, _ = TT.surf(TT.TR[txt_], px * 0.8, col, 'Black'); w, h = sf.get_width() + 60, px + 40
        c.set_source_rgba(*col, u * a); c.set_line_width(8); rrect(c, -w / 2, -h / 2, w, h, 16); c.stroke()
        c.set_source_surface(sf, -sf.get_width() / 2, -sf.get_height() / 2); c.paint_with_alpha(u * a); c.restore(); return
    font(c, 'head', px); e = c.text_extents(txt_); w, h = e.width + 60, px + 40
    c.set_source_rgba(*col, u * a); c.set_line_width(8); rrect(c, -w / 2, -h / 2, w, h, 16); c.stroke()
    c.move_to(-e.width / 2 - e.x_bearing, px * 0.36); c.show_text(txt_); c.restore()
def tick(c, x, y, s, u=1.0, col=AMBER, a=1.0):
    if u <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s); c.set_line_width(14); c.set_line_cap(cairo.LINE_CAP_ROUND); c.set_line_join(cairo.LINE_JOIN_ROUND)
    c.set_source_rgba(*col, a); p = [(-30, 0), (-8, 24), (34, -26)]
    L1 = math.dist(p[0], p[1]); L2 = math.dist(p[1], p[2]); d = (L1 + L2) * u
    c.move_to(*p[0])
    if d <= L1: c.line_to(p[0][0] + (p[1][0] - p[0][0]) * d / L1, p[0][1] + (p[1][1] - p[0][1]) * d / L1)
    else: c.line_to(*p[1]); f = (d - L1) / L2; c.line_to(p[1][0] + (p[2][0] - p[1][0]) * f, p[1][1] + (p[2][1] - p[1][1]) * f)
    c.stroke(); c.restore()
def cross(c, x, y, s, u=1.0, col=CREAM, a=1.0):
    if u <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s); c.set_line_width(14); c.set_line_cap(cairo.LINE_CAP_ROUND); c.set_source_rgba(*col, a)
    f1 = clamp(u * 2); f2 = clamp(u * 2 - 1)
    c.move_to(-26, -26); c.line_to(-26 + 52 * f1, -26 + 52 * f1); c.stroke()
    if f2 > 0: c.move_to(26, -26); c.line_to(26 - 52 * f2, -26 + 52 * f2); c.stroke()
    c.restore()
def score(c, y, old, new, t, t0, t_new=None, h=190):
    """OLD LAW · 1965 | NEW LAW · 2025 scoreboard. values: 'Y', 'N', or short text."""
    if t < t0: return
    t_new = t0 + 0.35 if t_new is None else t_new
    for j, (lab, val, tv) in enumerate((('OLD LAW · 1965', old, t0), ('NEW LAW · 2025', new, t_new))):
        x = 90 + j * 460; u = e_out(prog(t, t0 + 0.1 * j, t0 + 0.1 * j + 0.3))
        c.save(); c.translate(0, (1 - u) * 50)
        glass_dark(c, x, y, 440, h, 30, u)
        c.set_source_rgba(*(AMBER if j else CREAM), 0.9 * u); c.rectangle(x + 22, y + 22, 6, h - 44); c.fill()
        mono(c, lab, x + 240, y + 46, 24, AMBER if j else CREAM, a=u, kind='monob')
        k = prog(t, tv, tv + 0.35)
        if val == 'Y': tick(c, x + 240, y + h - 70, 1.25, k, AMBER if j else CREAM, a=u)
        elif val == 'N': cross(c, x + 240, y + h - 70, 1.05, k, CREAM, a=u)
        elif k > 0:
            font(c, 'head', 46); e = c.text_extents(val); sc = min(1.0, 380 / max(1, e.width))
            head(c, val, x + 240, y + h - 72, 46 * sc, AMBER if j else CREAM, a=u * k, shadow=False)
        c.restore()
SKIN = (0.80, 0.58, 0.42); HAIR = (0.10, 0.08, 0.07)
def person(c, x, y, s, shirt, prop=None, a=1.0, t=0.0, wave=0.0):
    """flat 2D avatar standing with feet at (x, y)"""
    if a <= 0.01 or s <= 0.01: return
    c.save(); c.translate(x, y); c.scale(s, s); c.push_group()
    bob = 3 * math.sin(t * 3.0)
    c.set_source_rgb(0.15, 0.15, 0.18); rrect(c, -48, -120, 40, 120, 16); c.fill(); rrect(c, 8, -120, 40, 120, 16); c.fill()   # legs
    c.set_source_rgb(*shirt); rrect(c, -72, -290 + bob, 144, 190, 50); c.fill()                                                  # body
    c.set_source_rgb(*SKIN); c.arc(0, -350 + bob, 56, 0, 2 * math.pi); c.fill()                                                    # head
    c.set_source_rgb(*HAIR); c.arc(0, -362 + bob, 58, math.pi * 1.02, math.pi * 1.98); c.fill()
    c.set_source_rgb(*HAIR); c.arc(-20, -345 + bob, 6, 0, 2 * math.pi); c.fill(); c.arc(20, -345 + bob, 6, 0, 2 * math.pi); c.fill()
    c.set_source_rgb(*HAIR); c.set_line_width(5); c.set_line_cap(cairo.LINE_CAP_ROUND); c.arc(0, -330 + bob, 18, 0.2 * math.pi, 0.8 * math.pi); c.stroke()
    if prop == 'box':
        c.set_source_rgb(0.62, 0.43, 0.24); c.rectangle(-70, -230 + bob, 140, 100); c.fill()
        c.set_source_rgb(0.85, 0.72, 0.45); c.rectangle(-70, -190 + bob, 140, 14); c.fill()
        c.set_source_rgb(*SKIN); c.arc(-74, -170 + bob, 18, 0, 2 * math.pi); c.fill(); c.arc(74, -170 + bob, 18, 0, 2 * math.pi); c.fill()
    elif prop == 'laptop':
        c.set_source_rgb(0.75, 0.76, 0.80); rrect(c, -80, -230 + bob, 160, 100, 10); c.fill()
        c.set_source_rgba(*AMBER, 0.9); c.arc(0, -180 + bob, 12, 0, 2 * math.pi); c.fill()
        c.set_source_rgb(0.55, 0.56, 0.60); c.rectangle(-95, -132 + bob, 190, 14); c.fill()
    elif prop == 'helmet':
        c.set_source_rgb(*AMBER); c.arc(0, -372 + bob, 60, math.pi, 2 * math.pi); c.fill(); c.rectangle(-72, -376 + bob, 144, 12); c.fill()
    if wave > 0:
        c.set_source_rgb(*SKIN); c.save(); c.translate(70, -260 + bob); c.rotate(-0.5 - 0.4 * math.sin(t * 8) * wave)
        rrect(c, -14, -110, 28, 110, 14); c.fill(); c.restore()
    c.pop_group_to_source(); c.paint_with_alpha(a); c.restore()
def name_card(c, x, y, name, sub, val, t, t0, a=1.0, w=470):
    if t < t0: return
    u = e_out(prog(t, t0, t0 + 0.3))
    c.save(); c.translate(0, (1 - u) * 40)
    glass_dark(c, x, y, w, 170 if val else 120, 28, u * a)
    c.set_source_rgba(*AMBER, u * a); c.rectangle(x + 18, y + 18, 6, (170 if val else 120) - 36); c.fill()
    head(c, name, x + 44, y + 46, 46, CREAM, a=u * a, anchor='l', shadow=False)
    mono(c, sub, x + 44, y + 92, 20, CREAM, a=0.8 * u * a, anchor='l', kind='mono')
    if val: head(c, val, x + 44, y + 138, 40, AMBER, a=u * a, anchor='l', shadow=False)
    c.restore()
def gift_icon(c, x, y, s, a=1.0, glow=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    if glow > 0:
        g = cairo.RadialGradient(0, 0, 0, 0, 0, 160); g.add_color_stop_rgba(0, *AMBER, 0.35 * glow); g.add_color_stop_rgba(1, *AMBER, 0); c.set_source(g); c.arc(0, 0, 160, 0, 2 * math.pi); c.fill()
    c.set_source_rgba(0.95, 0.55, 0.20, a); rrect(c, -80, -40, 160, 120, 10); c.fill()
    c.set_source_rgba(1.0, 0.65, 0.25, a); rrect(c, -92, -70, 184, 40, 10); c.fill()
    c.set_source_rgba(*CREAM, a); c.rectangle(-12, -70, 24, 150); c.fill()
    c.set_line_width(12); c.arc(-30, -84, 26, 0, 2 * math.pi); c.stroke(); c.arc(30, -84, 26, 0, 2 * math.pi); c.stroke()
    c.restore()
def gavel_icon(c, x, y, s, a=1.0, glow=0.0, hit=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    if glow > 0:
        g = cairo.RadialGradient(0, 0, 0, 0, 0, 160); g.add_color_stop_rgba(0, *AMBER, 0.35 * glow); g.add_color_stop_rgba(1, *AMBER, 0); c.set_source(g); c.arc(0, 0, 160, 0, 2 * math.pi); c.fill()
    c.set_source_rgba(0.55, 0.36, 0.20, a); rrect(c, -90, 60, 180, 30, 8); c.fill()
    c.save(); c.translate(10, 30); c.rotate(-0.6 + 0.5 * hit)
    c.set_source_rgba(0.70, 0.47, 0.27, a); rrect(c, -12, -130, 24, 150, 10); c.fill()
    c.set_source_rgba(0.60, 0.38, 0.22, a); rrect(c, -60, -170, 120, 56, 14); c.fill()
    c.set_source_rgba(*AMBER, a); c.rectangle(-60, -150, 120, 10); c.fill()
    c.restore(); c.restore()
def option_card(c, x, label, icon, t, glow, sub=None, a=1.0):
    glass_dark(c, x, 560, 430, 470, 36, a)
    if glow > 0:
        c.set_source_rgba(*AMBER, glow * a); c.set_line_width(5); rrect(c, x, 560, 430, 470, 36); c.stroke()
    icon(c, x + 215, 760, 1.0, a=a, glow=glow)
    head(c, label, x + 215, 940, 62, AMBER if glow > 0.5 else CREAM, a=a, shadow=False)
    if sub: mono(c, sub, x + 215, 995, 22, CREAM, a=0.8 * a, kind='monob')
TOP = None
def tag(c):
    global TOP
    txt = 'DIWALI · 5/6' if LANGV == 'en' else 'దీపావళి · 5/6'
    if LANGV == 'te':
        if TOP is None:
            f = ImageFont.truetype('/home/claude/fonts/NotoSansTelugu.ttf', 26, layout_engine=ImageFont.Layout.RAQM)
            try: f.set_variation_by_name('Bold')
            except Exception: pass
            im = Image.new('RGBA', (300, 60), (0, 0, 0, 0)); ImageDraw.Draw(im).text((0, 30), txt, font=f, fill=(244, 241, 234, 255), anchor='lm')
            TOP = surf_from_pil(im)
        glass_dark(c, 40, 92, 250, 54, 27); glowdot(c, 68, 119, 7); c.set_source_surface(TOP[0], 88, 89); c.paint(); return
    font(c, 'monob', 24); e = c.text_extents(txt)
    glass_dark(c, 40, 92, e.x_advance + 80, 54, 27); glowdot(c, 68, 119, 7); c.move_to(88, 128); c.set_source_rgb(*CREAM); c.show_text(txt)
def chips(c, active, t, t0):
    """progress 1/4 … 4/4 for 'what changed'"""
    if t < t0: return
    u = e_out(prog(t, t0, t0 + 0.3))
    for i in range(4):
        x = W / 2 - 330 + i * 220; on = i < active; cur = i == active - 1
        glass_dark(c, x - 90, 210, 180, 70, 35, u)
        if on:
            rrect(c, x - 90, 210, 180, 70, 35); c.set_source_rgba(*AMBER, (0.95 if cur else 0.35) * u); c.fill()
        mono(c, f'{i + 1}/4', x, 245, 30, INK if cur else CREAM, a=u, kind='monob')
    if active: glowdot(c, W / 2 - 330 + (active - 1) * 220, 292, 8 + 2 * math.sin(t * 6))

# ---------------- images ----------------
IMG = {}
def img(path, w=None, blur=0):
    key = (path, w, blur)
    if key not in IMG:
        im = Image.open(path).convert('RGB')
        if w: im = im.resize((w, int(im.height * w / im.width)), Image.LANCZOS)
        if blur: im = im.filter(ImageFilter.GaussianBlur(blur))
        IMG[key] = surf_from_pil(im)[0]
    return IMG[key]
THUMB = f'/home/claude/dl/thumb2_diwali_long_{LANGV.upper()}.jpg'
VIRAL = '/home/claude/why-channel-studio/videos/2026-11-01_long_diwali_explained/assets/images/09-india-diwali-rainbow-composite.jpg'
def card_img(c, sf, cx, cy, t, t0, rot=-2, a=1.0, border=AMBER):
    if t < t0: return
    u = e_out(prog(t, t0, t0 + 0.35)); w, h = sf.get_width(), sf.get_height()
    c.save(); c.translate(cx, cy + (1 - u) * 120); c.rotate(math.radians(rot))
    c.set_source_rgba(0, 0, 0, 0.5 * u * a); rrect(c, -w / 2 + 10, -h / 2 + 16, w, h, 22); c.fill()
    rrect(c, -w / 2, -h / 2, w, h, 22); c.save(); c.clip(); c.set_source_surface(sf, -w / 2, -h / 2); c.paint_with_alpha(u * a); c.restore()
    if border: rrect(c, -w / 2, -h / 2, w, h, 22); c.set_source_rgba(*border, u * a); c.set_line_width(5); c.stroke()
    c.restore()

# ---------------- extras ----------------
sys.path.insert(0, '/home/claude/why-channel-studio/pipeline/style_v2')
import cta_card as CTA
END_T0 = A['tomorrow'] + 0.9

SL = {}
def slide(c, t, t0, scale=1.0, a=1.0):
    if LANGV not in SL:
        SL[LANGV] = [(surf_from_pil(Image.open(ROOT + f).convert('RGBA'))[0], cxy) for f, cxy in json.load(open(ROOT + f'slide_{LANGV}.json'))]
    c.save(); c.translate(W / 2, 40); c.scale(scale, scale); c.translate(-W / 2, -40)
    c.push_group()
    starts = [0.0, 0.18] + [0.4 + 0.1 * i for i in range(6)] + [1.2]
    for (sf, (cx, cy)), st in zip(SL[LANGV], starts):
        tt = t - (t0 + st)
        if tt < 0: continue
        u = e_back(prog(tt, 0, 0.35)); al = prog(tt, 0, 0.2)
        c.save(); c.translate(cx, cy + (1 - min(u, 1)) * 60); c.scale(0.85 + 0.15 * min(u, 1.03), 0.85 + 0.15 * min(u, 1.03)); c.translate(-cx, -cy)
        c.set_source_surface(sf, 0, 0); c.paint_with_alpha(al); c.restore()
    k = prog(t, t0 + 1.0, t0 + 1.7)   # glow dot hops from 1/6 (here) to 2/6 (tomorrow)
    if 0 < k:
        (sx, sy), (ex, ey) = SL[LANGV][6][1], SL[LANGV][7][1]; sy += 200; ey += 200
        x = sx + (ex - sx) * e_io(k); y = sy + (ey - sy) * e_io(k) - math.sin(k * math.pi) * 120
        glowdot(c, x, y, 13 if k < 1 else 10 + 2 * math.sin(t * 6))
    c.pop_group_to_source(); c.paint_with_alpha(a); c.restore()


# ---------------- 5/6 drawings ----------------
NOTE = (540, 948)
GREEN = (0.30, 0.78, 0.45)
def note100(c, x, y, s, a=1.0, rot=0.0):
    if a <= 0: return
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.set_source_rgba(0, 0, 0, 0.35 * a); rrect(c, -78, -34, 160, 72, 8); c.fill()
    c.set_source_rgba(0.72, 0.66, 0.86, a); rrect(c, -80, -36, 160, 72, 8); c.fill()
    c.set_source_rgba(0.55, 0.48, 0.72, a); c.set_line_width(3); rrect(c, -72, -28, 144, 56, 6); c.stroke()
    c.set_source_rgba(0.88, 0.84, 0.95, a); c.arc(30, 0, 20, 0, 2 * math.pi); c.fill()
    font(c, 'head', 26); c.set_source_rgba(0.30, 0.22, 0.45, a); c.move_to(-66, 10); c.show_text('₹100')
    c.restore()
def coin(c, x, y, s, a=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.set_source_rgba(0.95, 0.75, 0.25, a); c.arc(0, 0, 16, 0, 2 * math.pi); c.fill()
    c.set_source_rgba(0.78, 0.56, 0.15, a); c.set_line_width(3); c.arc(0, 0, 11, 0, 2 * math.pi); c.stroke(); c.restore()
def market(c, t, a=1.0, note=True):
    c.save(); c.push_group()
    c.set_source_rgb(0.10, 0.09, 0.16); c.rectangle(60, 260, 960, 880); c.fill()
    for k in range(2):                                                     # string lights
        for i in range(20):
            x = 80 + i * 49; y = 300 + k * 60 + 26 * math.sin(i / 19 * math.pi)
            fl = 0.7 + 0.3 * math.sin(t * 3 + i * 1.7 + k)
            col = (1, 0.80, 0.35) if (i + k) % 3 else (1, 0.45, 0.35)
            g = cairo.RadialGradient(x, y, 0, x, y, 18); g.add_color_stop_rgba(0, *col, 0.9 * fl); g.add_color_stop_rgba(1, *col, 0); c.set_source(g); c.arc(x, y, 18, 0, 2 * math.pi); c.fill()
    for sx, col in ((120, (0.55, 0.20, 0.30)), (840, (0.20, 0.35, 0.55))):  # side stalls
        c.set_source_rgb(*col); c.rectangle(sx, 560, 120, 420); c.fill()
        for j in range(4): c.set_source_rgb(0.95, 0.85, 0.55) if j % 2 else c.set_source_rgb(*col); c.rectangle(sx - 10 + j * 35, 520, 35, 50); c.fill()
    c.set_source_rgb(0.32, 0.20, 0.14); c.rectangle(290, 500, 500, 460); c.fill()     # kirana shop
    for j in range(8):                                                     # awning
        c.set_source_rgb(0.90, 0.30, 0.20) if j % 2 == 0 else c.set_source_rgb(0.96, 0.92, 0.85)
        c.move_to(270 + j * 67.5, 440); c.line_to(270 + (j + 1) * 67.5, 440); c.line_to(270 + (j + 1) * 67.5, 510); c.curve_to(270 + (j + 0.5) * 67.5, 540, 270 + (j + 0.5) * 67.5, 540, 270 + j * 67.5, 510); c.close_path(); c.fill()
    font(c, 'head', 34); c.set_source_rgb(*AMBER); e = c.text_extents('KIRANA'); c.move_to(540 - e.width / 2 - e.x_bearing, 480); c.show_text('KIRANA')
    for r in range(3):                                                     # shelves with jars & packs
        y = 600 + r * 95; c.set_source_rgb(0.50, 0.34, 0.22); c.rectangle(310, y + 50, 460, 10); c.fill()
        for i in range(7):
            col = [(0.95, 0.75, 0.25), (0.35, 0.65, 0.40), (0.90, 0.35, 0.25), (0.40, 0.55, 0.85), (0.95, 0.90, 0.80), (0.80, 0.50, 0.25), (0.65, 0.40, 0.70)][(i + r) % 7]
            c.set_source_rgb(*col); rrect(c, 325 + i * 64, y, 44, 50, 6); c.fill()
    c.set_source_rgb(0.62, 0.42, 0.26); c.rectangle(250, 960, 580, 140); c.fill()     # counter
    c.set_source_rgb(0.75, 0.55, 0.35); c.rectangle(240, 950, 600, 18); c.fill()
    for i, col in enumerate(((0.95, 0.85, 0.6), (0.85, 0.75, 0.55))):      # sacks
        c.set_source_rgb(*col); c.move_to(300 + i * 80, 1100); c.curve_to(290 + i * 80, 1010, 370 + i * 80, 1010, 360 + i * 80, 1100); c.close_path(); c.fill()
    if note: note100(c, *NOTE, 1.0, rot=-0.06)
    c.pop_group_to_source(); c.paint_with_alpha(a); c.restore()
JARS = [  # key, label, amount, cx, cy, w, h
    ('groc', 'GROCERIES & FMCG', 12, 200, 560, 270, 220), ('gold', 'GOLD, SILVER & JEWELLERY', 10, 540, 560, 270, 220), ('elec', 'ELECTRONICS', 8, 880, 560, 270, 220),
    ('appl', 'APPLIANCES', 7, 200, 830, 270, 190), ('cloth', 'CLOTHES', 7, 540, 830, 270, 190), ('gift', 'GIFTS', 7, 880, 830, 270, 190),
    ('decor', 'HOME DÉCOR', 5, 200, 1070, 270, 170), ('furn', 'FURNITURE', 5, 540, 1070, 270, 170), ('sweet', 'SWEETS', 5, 880, 1070, 270, 170),
    ('else', 'EVERYTHING ELSE', 34, 540, 1300, 900, 110)]
def jar_t0(k):
    return {'groc': A['groc'], 'gold': A['gold4'], 'elec': A['elec'], 'appl': A['appl'], 'cloth': A['appl'], 'gift': A['appl'],
            'decor': A['decor'], 'furn': A['decor'], 'sweet': A['decor'], 'else': A['sweets'] + 0.4}[k]
def jars(c, t, a=1.0, only=None):
    tot = 0.0
    for k, lab, amt, cx, cy, w, h in JARS:
        if only and k not in only: continue
        t0 = jar_t0(k); f = e_out(prog(t, t0, t0 + 0.6)); tot += amt * f
        if k == 'else' and t < A['decor']: continue
        x0, y0 = cx - w / 2, cy - h / 2
        wob = 0.0
        if k == 'gold' and S('3') + 0.1 < t < A['groc']: wob = 0.06 * math.sin((t - S('3')) * 18)
        dim = 0.45 if (k == 'gold' and A['groc'] <= t < A['gold4']) else 1.0
        c.save(); c.translate(cx, cy); c.rotate(wob); c.translate(-cx, -cy)
        glass_dark(c, x0, y0, w, h, 20, a * dim)
        c.set_source_rgba(1, 1, 1, 0.25 * a * dim); c.set_line_width(3); rrect(c, x0, y0, w, h, 20); c.stroke()
        if f > 0:
            fh = (h - 112) * f * (min(1.0, amt / 12) if k != 'else' else 1.0) if k != 'else' else (h - 60) * f
            c.set_source_rgba(*(AMBER if k == 'groc' else (0.95, 0.75, 0.25)), 0.85 * a); rrect(c, x0 + 10, y0 + h - 10 - fh, w - 20, fh, 12); c.fill()
            if f < 1:
                for q in range(5): coin(c, cx - 60 + q * 30, y0 - 20 + ((t - t0) * 900 + q * 37) % (h - 20), 0.9, a=a)
            if k == 'else': head(c, f'₹{amt}', cx + 330, y0 + 28, 34, CREAM, a=a * prog(f, 0.3, 0.8), shadow=False)
            else: head(c, f'₹{amt}', cx, y0 + 70, 46, AMBER if k == 'groc' else CREAM, a=a * prog(f, 0.3, 0.8), shadow=False)
        mono(c, lab, cx, y0 + 26, 17 if k != 'else' else 20, CREAM, a=a * dim * 0.9, kind='monob')
        c.restore()
    return tot
def services_icons(c, t, t0, a=1.0):
    items = [('bike', 820, 560), ('cab', 820, 760), ('tent', 820, 950)]
    for i, (kind, x, y) in enumerate(items):
        u = e_back(prog(t, t0 + 0.2 * i, t0 + 0.2 * i + 0.3))
        if u <= 0: continue
        c.save(); c.translate(x, y); c.scale(max(0.01, u), max(0.01, u))
        glass_dark(c, -150, -80, 300, 160, 30, a)
        if kind == 'bike':
            c.set_source_rgba(*CREAM, a); c.set_line_width(8)
            for wx in (-55, 55): c.new_path(); c.arc(wx, 30, 28, 0, 2 * math.pi); c.stroke()
            c.set_source_rgba(*AMBER, a); rrect(c, -50, -30, 90, 40, 10); c.fill(); rrect(c, 20, -60, 50, 44, 8); c.fill()
        elif kind == 'cab':
            c.set_source_rgba(0.98, 0.80, 0.20, a); rrect(c, -95, -20, 190, 55, 14); c.fill(); rrect(c, -55, -55, 110, 45, 12); c.fill()
            c.set_source_rgba(0.1, 0.1, 0.12, a)
            for wx in (-55, 55): c.new_path(); c.arc(wx, 38, 18, 0, 2 * math.pi); c.fill()
        else:
            for j in range(4):
                c.set_source_rgba(*((0.90, 0.30, 0.20) if j % 2 == 0 else CREAM), a)
                c.move_to(-90 + j * 45, 50); c.line_to(-90 + (j + 1) * 45, 50); c.line_to(0, -55); c.close_path(); c.fill()
        c.restore()
def aunty(c, x, y, s, t, a=1.0):
    person(c, x, y, s, (0.82, 0.20, 0.42), t=t, a=a)
    c.save(); c.translate(x, y); c.scale(s, s)
    c.set_source_rgba(0.95, 0.75, 0.25, a); c.move_to(-72, -280); c.line_to(-40, -290); c.line_to(72, -120); c.line_to(40, -110); c.close_path(); c.fill()   # saree pallu
    c.set_source_rgba(*HAIR, a); c.arc(0, -410, 26, 0, 2 * math.pi); c.fill()                                                                   # bun
    c.set_source_rgba(0.85, 0.10, 0.10, a); c.arc(0, -372, 6, 0, 2 * math.pi); c.fill()                                                         # bindi
    c.restore()

def sc_hook(c, t, frozen=False):
    tt = 0.0 if frozen else t
    market(c, tt)
    mono(c, 'FESTIVE TRADE FORECAST · CAIT', W / 2, 1185, 28, CREAM, kind='monob')
    head(c, '₹7 LAKH CRORE', W / 2, 1265, 88, AMBER)
    if not frozen:
        draw_clip(c, 'bt', W / 2, 720, 780, t, A['trade1'] - 0.2, rot=-0.8, hl_t0=A['trade1'] + 0.1, hl_dur=0.9, t1=A['where'] - 0.35)
        if t < A['where'] - 0.1: source_tag(c, 'BUSINESS TODAY · 14 OCT 2026', 150, 900, a=prog(t, A['trade1'], A['trade1'] + 0.3) * (1 - prog(t, A['where'] - 0.4, A['where'] - 0.1)))
        if t >= A['where'] - 0.1: head(c, 'WHERE DOES IT GO?', W / 2, 1348, 60, CREAM, a=prog(t, A['where'] - 0.1, A['where'] + 0.15))

def heading(c, a=1.0):
    pill(c, '₹100 OF GOODS SALES · CAIT ESTIMATES', W / 2, 215, 22, CREAM, a=a)

def frame(t):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s)
    board_bg(c, t)
    caps = True
    if t < S('2') - 0.05:
        sc_hook(c, t)
    # 2 follow 100 rupees
    elif t < S('3') - 0.05:
        heading(c, a=prog(t, S('2') + 0.2, S('2') + 0.5))
        k = e_io(prog(t, S('2'), S('2') + 1.0))
        x = NOTE[0]; y = NOTE[1] + (640 - NOTE[1]) * k; sc_ = 1.0 + 1.6 * k
        burst = prog(t, S('2') + 1.3, S('2') + 2.0)
        note100(c, x, y, sc_, a=1 - burst, rot=-0.06 * (1 - k))
        if burst > 0:
            rng = np.random.default_rng(3)
            for i in range(40):
                an = rng.uniform(0, 2 * math.pi); r = 40 + 380 * e_out(burst) * rng.uniform(0.4, 1)
                coin(c, 540 + r * math.cos(an), 640 + r * math.sin(an) * 0.8, 1.0, a=1 - prog(burst, 0.7, 1.0))
        if t >= S('2') + 1.7: jars(c, t, a=prog(t, S('2') + 1.7, S('2') + 2.2))
    # 3-6 the jars
    elif t < S('7') - 0.05:
        heading(c)
        tot = jars(c, t)
        if S('3') + 0.1 < t < A['groc']:
            mono(c, 'BIGGEST SLICE?', 540, 410, 24, AMBER, kind='monob')
        if A['groc'] + 0.5 <= t < S('4') - 0.1:
            draw_clip(c, 'caitcat', W / 2, 1230, 820, t, A['groc'] + 0.5, rot=0.7, hl_t0=A['groc'] + 0.8, hl_dur=0.8)
        pill(c, f'₹{int(round(tot))} / 100', W / 2, 300, 26, AMBER if tot > 99.5 else CREAM)
    # 7 services (part of the ₹7 lakh crore)
    elif t < S('8') - 0.05:
        k = e_io(prog(t, S('7') - 0.05, S('7') + 0.5))
        c.save(); c.translate(80 * k, 260 * k); c.scale(1 - 0.45 * k, 1 - 0.45 * k)
        c.push_group(); jars(c, t); c.pop_group_to_source(); c.paint_with_alpha(1 - 0.65 * k); c.restore()
        mono(c, 'GOODS', 330, 470, 24, CREAM, a=0.7 * k, kind='monob')
        services_icons(c, t, A['services'] - 0.2)
        if t >= A['k80'] - 0.2:
            pill(c, 'SERVICES · ≈ ₹80,000 CR+ · 2026 FORECAST', W / 2, 1150, 28, AMBER, s=e_back(prog(t, A['k80'] - 0.2, A['k80'] + 0.1)))
        if t >= A['services']:
            mono(c, 'SERVICES INCLUDED IN ₹7 LAKH CR FORECAST', W / 2, 1230, 22, CREAM, a=prog(t, A['services'], A['services'] + 0.3), kind='monob')
    # 8 Lakshmi aunty (grocery coins flow to her counter)
    elif t < S('9') - 0.05:
        market(c, t, note=False)
        aunty(c, 540, 960, 0.95, t, a=prog(t, S('8'), S('8') + 0.3))
        c.set_source_rgb(0.62, 0.42, 0.26); c.rectangle(250, 960, 580, 140); c.fill(); c.set_source_rgb(0.75, 0.55, 0.35); c.rectangle(240, 950, 600, 18); c.fill()
        for i in range(3): person(c, 920, 1180, 0.45 + 0.02 * i, [(0.3, 0.5, 0.8), (0.4, 0.7, 0.4), (0.8, 0.6, 0.3)][i], t=t + i)
        glass_dark(c, 80, 300, 220, 150, 20); c.set_source_rgba(*AMBER, 0.85); rrect(c, 95, 360, 190, 76, 12); c.fill()
        mono(c, 'GROCERIES ₹12', 190, 330, 18, CREAM, kind='monob')
        k = prog(t, S('8') + 0.2, S('8') + 2.2)
        if 0 < k < 1:
            for q in range(8):
                f = (k * 3 + q / 8) % 1.0
                coin(c, 190 + (500 - 190) * f, 420 + (930 - 420) * f - math.sin(f * math.pi) * 160, 1.0)
        name_card(c, 600, 300, 'LAKSHMI AUNTY', 'EXAMPLE', None, t, A['lakshmi'] - 0.2, w=420)
        if t >= A['busiest'] - 0.3:
            u = prog(t, A['busiest'] - 0.3, A['busiest'] + 0.3)
            for i in range(8):
                on = i in (4, 5, 6); x = 150 + i * 100
                glass_dark(c, x - 42, 1150, 84, 60, 12, u)
                if on: c.set_source_rgba(*AMBER, 0.9 * u); rrect(c, x - 42, 1150, 84, 60, 12); c.fill()
            mono(c, 'BUSIEST WEEKS', 690, 1250, 22, AMBER, a=u, kind='monob')
    # 9 85% mainline retail
    elif t < S('10') - 0.05:
        t0 = A['p85'] - 0.3
        for i in range(100):
            r_, q = divmod(i, 10); x = 306 + q * 52; y = 380 + r_ * 52
            on = i < int(85 * prog(t, t0, t0 + 1.0))
            c.set_source_rgba(*(AMBER if on else CREAM), 0.95 if on else 0.18); c.new_path(); c.arc(x, y, 18, 0, 2 * math.pi); c.fill()
        if t >= t0 + 1.0: big_num(c, '85%', W / 2, 960, 120, t, t0 + 1.0)
        pill(c, 'MAINLINE RETAIL · 2025 · CAIT ESTIMATE', W / 2, 1060, 24, CREAM, s=e_back(prog(t, S('9'), S('9') + 0.3)))
        draw_clip(c, 'cait85', W / 2, 1240, 880, t, A['p85'] + 1.0, rot=-0.6, hl_t0=A['p85'] + 1.3, hl_dur=1.4)
    # 10 50 lakh temporary jobs
    elif t < S('11') - 0.05:
        n = int(60 * e_out(prog(t, S('10'), A['j50'] + 0.8)))
        cols = [(0.95, 0.55, 0.2), (0.3, 0.6, 0.9), (0.4, 0.75, 0.45)]
        for i in range(n):
            r_, q = divmod(i, 10); person(c, 130 + q * 92, 470 + r_ * 100, 0.2, cols[i % 3], t=t + i)
        if t >= A['j50'] - 0.1: big_num(c, '≈ 50 LAKH', W / 2, 1120, 110, t, A['j50'] - 0.1)
        mono(c, 'TEMPORARY JOBS · 2025 · CAIT ESTIMATE', W / 2, 1230, 24, CREAM, a=prog(t, A['j50'], A['j50'] + 0.3), kind='monob')
    # 11 caveat + small shops
    elif t < S('12') - 0.05:
        if t < A['small'] - 0.3:
            stamp_txt(c, "TRADERS' ESTIMATES · NOT OFFICIAL", W / 2, 700, t, S('11') + 0.1, px=44, rot=-5, col=AMBER)
        else:
            k = prog(t, A['small'] - 0.3, A['small'] + 0.2)
            market(c, t, a=k, note=False); aunty(c, 540, 960, 0.95, t, a=k)
            c.set_source_rgba(0.62, 0.42, 0.26, k); c.rectangle(250, 960, 580, 140); c.fill()
            head(c, 'SMALL SHOPS', W / 2, 1230, 80, AMBER, a=k)
            mono(c, 'BIG PART OF THE STORY', W / 2, 1310, 28, CREAM, a=k, kind='monob')
    # 12 series slide
    elif t < S('L') - 0.05:
        caps = t < END_T0 - 0.3
        sc_ = 1.0 - 0.14 * e_io(prog(t, END_T0 - 0.5, END_T0))
        slide(c, t, S('12') - 0.05, scale=sc_)
        CTA.draw(c, t, END_T0, PLAT, LANGV, y=1745)
    else:
        # a hand places the ₹100 note exactly where it lies in frame 0, then the market fades in around it
        ks = e_io(prog(t, S('L') - 0.05, S('L') + 0.45)); k = e_io(prog(t, S('L') + 0.8, S('L') + 1.5))
        c.push_group(); slide(c, t, S('12') - 0.05, scale=0.86); CTA.draw(c, t, END_T0, PLAT, LANGV, y=1745); c.pop_group_to_source(); c.paint_with_alpha(1 - ks)
        c.push_group(); board_bg(c, 0.0); sc_hook(c, 0.0, frozen=True); tag(c); c.pop_group_to_source(); c.paint_with_alpha(k)
        if k < 1:
            u = e_out(prog(t, S('L') + 0.1, S('L') + 0.8)); y = 1500 + (NOTE[1] - 1500) * u
            note100(c, NOTE[0], y, 1.0, a=1 - k * 0, rot=-0.06)
            c.set_source_rgba(*SKIN, (1 - k) * (1 - prog(t, S('L') + 0.8, S('L') + 1.1))); rrect(c, NOTE[0] + 30, y + 10, 70, 160, 30); c.fill()
    if caps: (K.captions(c, t, y=1440) if LANGV == 'en' else R3.te_captions(c, t, y=1440))
    if t < S('12') - 0.05: tag(c)
    return s

def main(part=0, parts=1, out=None, still=None):
    if still is not None:
        os.makedirs(ROOT + 'stills', exist_ok=True)
        for tt in still: frame(tt).write_to_png(f'{ROOT}stills/{LANGV}_{PLAT}_{tt:06.2f}.png')
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
