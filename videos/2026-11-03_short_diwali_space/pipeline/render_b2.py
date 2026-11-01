"""DIWALI · 1/6 'That India-from-space Diwali photo' — style v2, loops into its own opening."""
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
ROOT = '/home/claude/b2/'
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
    'nasa1': AT('1', 'NASA', 'NASA'), 'itsnot': AT('1', 'not.', 'కాదు'),
    'raju': AT('2', 'Raju', 'రాజు'), 'fwd': AT('2', 'forwards', 'forward'),
    'y2003': AT('3', '2003', '2003'), 'elvidge': AT('3', 'Elvidge', 'Elvidge'), 'mil': AT('3', 'military', 'military'),
    'fire': AT('4', 'fireworks', 'బాణాసంచా'), 'years4': AT('4', 'years', 'సంవత్సరాలు'),
    'white': AT('5', 'White', 'తెలుపు'), 'blue': AT('5', 'Blue', 'నీలం'), 'green': AT('5', 'Green', 'ఆకుపచ్చ'), 'red': AT('5', 'Red', 'ఎరుపు'),
    'growing': AT('6', 'growing', 'పెరిగాయో'), 'onenight': AT('6', 'night', 'రాత్రి'),
    'clouds': AT('7', 'clouds', 'మేఘాలను'), 'city7': AT('7', 'city', 'నగరాల'),
    'real8': AT('8', "NASA's", 'NASA'),
    'rainbow': AT('9', 'rainbow', 'ఇంద్రధనుస్సు'),
    'subtle': AT('10', 'subtle', 'తక్కువ'),
    'k824': AT('11', '824', '824'), 'm750': AT('11', '750', '750'), 'hood': AT('11', 'neighbourhood', 'colony'),
    'street': AT('12', 'Street', 'Street'), 'blends': AT('12', 'blends', 'కలిసిపోతుంది'),
    'reply': AT('13', 'reply', 'reply'), 'wrong': AT('13', 'Wrong', 'తప్పు'),
    'tomorrow': S('14'), 'loop': S('L'),
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
    txt = 'DIWALI · 2/6' if LANGV == 'en' else 'దీపావళి · 2/6'
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
        (sx, sy), (ex, ey) = SL[LANGV][3][1], SL[LANGV][4][1]; sy += 200; ey += 200
        x = sx + (ex - sx) * e_io(k); y = sy + (ey - sy) * e_io(k) - math.sin(k * math.pi) * 120
        glowdot(c, x, y, 13 if k < 1 else 10 + 2 * math.sin(t * 6))
    c.pop_group_to_source(); c.paint_with_alpha(a); c.restore()


# ---------------- 2/6 assets ----------------
IMGD = '/home/claude/why-channel-studio/videos/2026-11-01_long_diwali_explained/assets/images/'
VIRAL = IMGD + '09-india-diwali-rainbow-composite.jpg'
NASAIMG = IMGD + '10-nasa-suomi-npp-india-2012-11-12.jpg'
MASK = {}
def viral_mask(kind, w):
    key = (kind, w)
    if key not in MASK:
        im = Image.open(VIRAL).convert('RGB').resize((w, int(577 * w / 600)), Image.LANCZOS)
        a = np.asarray(im).astype(np.float32) / 255
        hsv = np.asarray(im.convert('HSV')).astype(np.float32) / 255
        h, s_, v = hsv[..., 0] * 360, hsv[..., 1], hsv[..., 2]
        lit = v > 0.30
        sel = {'white': lit & (s_ < 0.28),
               'blue': lit & (s_ >= 0.2) & (h >= 180) & (h < 270),
               'green': lit & (s_ >= 0.2) & (h >= 75) & (h < 180),
               'red': lit & (s_ >= 0.2) & ((h < 40) | (h >= 300))}[kind]
        out = a * 0.10; out[sel] = np.clip(a[sel] * 1.6, 0, 1)
        if kind != 'white':
            gl = np.zeros_like(a); gl[sel] = a[sel] / np.maximum(a[sel].max(axis=1, keepdims=True), 1e-3)
            gim = Image.fromarray((gl * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(4))
            out = np.clip(out + np.asarray(gim).astype(np.float32) / 255 * 1.4, 0, 1)
        MASK[key] = surf_from_pil(Image.fromarray((np.clip(out, 0, 1) * 255).astype(np.uint8)))[0]
    return MASK[key]

def burst_icon(c, x, y, s, a=1.0):
    c.save(); c.translate(x, y); c.scale(s, s); c.set_line_cap(cairo.LINE_CAP_ROUND)
    for k in range(12):
        an = k * math.pi / 6; c.set_source_rgba(*(AMBER if k % 2 else CREAM), a); c.set_line_width(8)
        c.move_to(math.cos(an) * 25, math.sin(an) * 25); c.line_to(math.cos(an) * 70, math.sin(an) * 70); c.stroke()
    c.restore()
def calendar_icon(c, x, y, s, a=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    rrect(c, -70, -60, 140, 130, 14); c.set_source_rgba(*CREAM, a); c.fill()
    rrect(c, -70, -60, 140, 36, 14); c.set_source_rgba(*AMBER, a); c.fill()
    for i in range(3):
        for j in range(3): c.set_source_rgba(*INK, 0.8 * a); c.rectangle(-48 + i * 36, -8 + j * 26, 22, 16); c.fill()
    c.restore()
def satellite(c, x, y, s, a=1.0, ang=0.0):
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    for d in (-1, 1):
        c.set_source_rgba(0.25, 0.40, 0.75, a); c.rectangle(d * 40 - (90 if d < 0 else 0), -22, 90, 44); c.fill()
        c.set_source_rgba(1, 1, 1, 0.3 * a); c.set_line_width(2)
        for k in range(1, 4): c.move_to(d * 40 - (90 if d < 0 else 0) + k * 22, -22); c.line_to(d * 40 - (90 if d < 0 else 0) + k * 22, 22)
        c.stroke()
    rrect(c, -38, -30, 76, 60, 10); c.set_source_rgba(0.85, 0.85, 0.88, a); c.fill()
    c.set_source_rgba(*AMBER, a); c.arc(0, 34, 10, 0, 2 * math.pi); c.fill()
    c.restore()
def raju(c, x, y, s, t, a=1.0, react=0.0):
    person(c, x, y, s, (0.55, 0.22, 0.30), prop=None, a=a, t=t)
    bob = 3 * math.sin(t * 3.0)
    c.save(); c.translate(x, y); c.scale(s, s)
    c.set_source_rgba(0.1, 0.1, 0.1, a); c.set_line_width(4)               # glasses
    for d in (-1, 1): c.arc(d * 20, -345 + bob, 13, 0, 2 * math.pi); c.stroke()
    c.move_to(-7, -345 + bob); c.line_to(7, -345 + bob); c.stroke()
    c.set_source_rgba(0.85, 0.85, 0.85, a); c.arc(0, -400 + bob, 40, math.pi * 1.1, math.pi * 1.9); c.set_line_width(10); c.stroke()  # grey hair
    c.set_source_rgba(*SKIN, a); c.arc(70, -180 + bob, 18, 0, 2 * math.pi); c.fill()                   # hand + phone
    rrect(c, 60, -250 + bob, 44, 80, 8); c.set_source_rgba(0.12, 0.12, 0.14, a); c.fill()
    c.set_source_rgba(*AMBER, 0.8 * a); c.rectangle(65, -243 + bob, 34, 60); c.fill()
    c.restore()
    if react > 0:
        u = e_back(react); c.save(); c.translate(x + 120 * s, y - 470 * s); c.scale(max(0.01, u), max(0.01, u))
        c.set_source_rgba(*CREAM, a); c.arc(0, 0, 46, 0, 2 * math.pi); c.fill()
        font(c, 'head', 56); e = c.text_extents('!'); c.move_to(-e.width / 2 - e.x_bearing, 20); c.set_source_rgba(*INK, a); c.show_text('!'); c.restore()
def chat_panel(c, t, t0, x=470, y=330, w=560, h=760, count_t=None, reply_t=None, reply_full=None, a=1.0):
    if t < t0: return
    u = e_out(prog(t, t0, t0 + 0.35)) * a
    c.save(); c.translate(0, (1 - u) * 40)
    glass_dark(c, x, y, w, h, 34, u)
    c.set_source_rgba(*AMBER, u); c.arc(x + 50, y + 50, 18, 0, 2 * math.pi); c.fill()
    mono(c, 'FAMILY GROUP', x + 85, y + 50, 26, CREAM, a=u, anchor='l', kind='monob')
    # forwarded bubble with the photo
    bx, by = x + 30, y + 110
    rrect(c, bx, by, w - 110, 420, 22); c.set_source_rgba(0.16, 0.16, 0.19, u); c.fill()
    mono(c, 'Forwarded many times', bx + 22, by + 32, 18, CREAM, a=0.7 * u, anchor='l', kind='mono')
    sf = img(VIRAL, w - 150); c.save(); rrect(c, bx + 20, by + 60, w - 150, 340, 14); c.clip(); c.set_source_surface(sf, bx + 20, by + 40); c.paint_with_alpha(u); c.restore()
    if count_t is not None and t >= count_t:   # reactions count up
        k = prog(t, count_t, count_t + 1.3); n = int(52 * e_out(k))
        rrect(c, bx + 20, by + 395, 230, 54, 27); c.set_source_rgba(0.24, 0.24, 0.28, u); c.fill()
        for i, col in enumerate(((1.0, 0.35, 0.45), AMBER, (1.0, 0.85, 0.3))):
            c.set_source_rgba(*col, u); c.arc(bx + 50 + i * 30, by + 422, 12, 0, 2 * math.pi); c.fill()
        font(c, 'monob', 26); c.move_to(bx + 150, by + 432); c.set_source_rgba(*CREAM, u); c.show_text(f'{n}+')
    if reply_t is not None and t >= reply_t:   # the reply types out
        k = prog(t, reply_t, reply_t + 1.4); full = reply_full; n = max(1, int(len(full) * k))
        rx, ry = x + 90, y + h - 190
        rrect(c, rx, ry, w - 120, 120, 24); c.set_source_rgba(*AMBER, u); c.fill()
        txt_ = full[:n] + ('|' if k < 1 and int(t * 4) % 2 == 0 else '')
        if LANGV == 'te': TT.draw(c, txt_, rx + 24, ry + 60, 30, INK, u, 'l', 'Bold', maxw=w - 160)
        else:
            font(c, 'monob', 28); c.move_to(rx + 24, ry + 70); c.set_source_rgba(*INK, u); c.show_text(txt_)
    c.restore()

def sc_hook(c, t, frozen=False):
    sf = img(VIRAL, 900); w, h = sf.get_width(), sf.get_height()
    z = 1.0 if frozen else 1.0 + 0.05 * prog(t, 0, S('2'))
    c.save(); c.translate(W / 2, 680); c.scale(z, z)
    c.set_source_rgba(0, 0, 0, 0.5); rrect(c, -w / 2 + 10, -h / 2 + 16, w, h, 26); c.fill()
    rrect(c, -w / 2, -h / 2, w, h, 26); c.save(); c.clip(); c.set_source_surface(sf, -w / 2, -h / 2); c.paint(); c.restore()
    c.restore()
    pill(c, "NASA'S DIWALI PHOTO?", W / 2, 1210, 46, AMBER)
    if not frozen:
        for i, (lab, y, r) in enumerate((('NOT DIWALI', 470, -8), ('NOT FIREWORKS', 690, 6), ('NOT ONE NIGHT', 910, -5))):
            stamp_txt(c, lab, W / 2, y, t, A['itsnot'] - 0.15 + 0.22 * i, px=72, rot=r, col=AMBER)

def frame(t):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s)
    board_bg(c, t)
    caps = True
    if t < S('2') + 0.6:
        sc_hook(c, t)
    # 2 Raju uncle
    elif t < S('3') - 0.05:
        raju(c, 250, 1180, 1.05, t, a=prog(t, S('2') + 0.6, S('2') + 0.9))
        mono(c, 'RAJU UNCLE', 250, 1235, 28, CREAM, a=prog(t, S('2') + 0.7, S('2') + 1.0), kind='monob')
        chat_panel(c, t, A['fwd'] - 0.3, count_t=A['fwd'] + 0.4)
    # 3 what it really is
    elif t < S('4') - 0.05:
        draw_clip(c, 'es_head', W / 2, 400, 900, t, S('3') - 0.05, rot=-1.0)
        draw_clip(c, 'es_cap', W / 2, 680, 1010, t, S('3') + 0.4, rot=0.8, hl_t0=S('3') + 0.8, hl_dur=1.3)
        source_tag(c, 'EARTHSKY · NOV 6, 2018', 90, 820, a=prog(t, S('3') + 0.3, S('3') + 0.6))
        if t >= A['y2003'] - 0.2:
            name_card(c, 230, 900, 'CHRIS ELVIDGE', 'NOAA SCIENTIST', '2003', t, A['y2003'] - 0.2, w=620)
        if t >= A['mil'] - 0.2:
            pill(c, 'DMSP · US DEFENSE METEOROLOGICAL SATELLITE PROGRAM', W / 2, 1150, 20, CREAM, s=e_back(prog(t, A['mil'] - 0.2, A['mil'] + 0.1)))
    # 4 colours are years
    elif t < S('5') - 0.05:
        sf = img(VIRAL, 700); w, h = sf.get_width(), sf.get_height()
        c.save(); c.translate(W / 2, 560); rrect(c, -w / 2, -h / 2, w, h, 22); c.clip(); c.set_source_surface(sf, -w / 2, -h / 2); c.paint(); c.restore()
        cols = [CREAM, (0.35, 0.55, 1.0), (0.3, 0.9, 0.45), (1.0, 0.3, 0.25)]
        for i, col in enumerate(cols):
            k = e_back(prog(t, S('4') + 0.1 + 0.12 * i, S('4') + 0.4 + 0.12 * i))
            if k > 0: c.set_source_rgba(*col, 1); c.arc(300 + i * 160, 1000, 40 * min(k, 1.1), 0, 2 * math.pi); c.fill()
        if t < A['years4'] - 0.1:
            burst_icon(c, W / 2, 1180, 1.0, a=prog(t, A['fire'] - 0.2, A['fire']))
            if t >= A['fire'] + 0.3: cross(c, W / 2, 1180, 2.0, prog(t, A['fire'] + 0.3, A['fire'] + 0.6), CREAM)
        else:
            calendar_icon(c, W / 2, 1180, 1.0 * e_back(prog(t, A['years4'] - 0.1, A['years4'] + 0.2)))
            head(c, 'THEY\'RE YEARS', W / 2, 1300, 52, AMBER, a=prog(t, A['years4'], A['years4'] + 0.3))
    # 5 legend
    elif t < S('6') - 0.05:
        order = [('white', A['white'], 'BEFORE 1992', CREAM), ('blue', A['blue'], '1992', (0.35, 0.55, 1.0)),
                 ('green', A['green'], '1998', (0.3, 0.9, 0.45)), ('red', A['red'], '2003', (1.0, 0.3, 0.25))]
        cur = 0
        for i, (_, tt, _, _) in enumerate(order):
            if t >= tt - 0.15: cur = i
        sf = viral_mask(order[cur][0], 860); w, h = sf.get_width(), sf.get_height()
        c.save(); c.translate(W / 2, 640); rrect(c, -w / 2, -h / 2, w, h, 22); c.clip(); c.set_source_surface(sf, -w / 2, -h / 2); c.paint(); c.restore()
        for i, (_, tt, lab, col) in enumerate(order):
            if t < tt - 0.15: continue
            x = 160 + i * 253; on = i == cur; u = e_out(prog(t, tt - 0.15, tt + 0.1))
            glass_dark(c, x - 115, 1110, 230, 150, 24, u)
            if on: c.set_source_rgba(*col, u); c.set_line_width(5); rrect(c, x - 115, 1110, 230, 150, 24); c.stroke()
            c.set_source_rgba(*col, u); c.arc(x, 1160, 22, 0, 2 * math.pi); c.fill()
            mono(c, lab, x, 1222, 24 if len(lab) < 6 else 19, col if on else CREAM, a=u, kind='monob')
    # 6 hero: 11 years vs 1 night
    elif t < S('7') - 0.05:
        mono(c, 'A MAP OF INDIA GROWING', W / 2, 300, 30, CREAM, a=prog(t, S('6'), S('6') + 0.3), kind='monob')
        if t >= A['growing'] - 0.2:
            mono(c, '1992 → 2003', W / 2, 430, 44, AMBER, a=prog(t, A['growing'] - 0.2, A['growing']), kind='monob')
            big_num(c, '11 YEARS', W / 2, 590, 170, t, A['growing'])
        if t >= A['onenight'] - 0.6:
            head(c, 'NOT', W / 2, 800, 60, CREAM, a=prog(t, A['onenight'] - 0.6, A['onenight'] - 0.4))
            head(c, '1 NIGHT', W / 2, 950, 150, CREAM, a=prog(t, A['onenight'] - 0.4, A['onenight'] - 0.1))
            kk = e_out(prog(t, A['onenight'], A['onenight'] + 0.3))
            if kk > 0:
                c.set_source_rgba(*AMBER, 1); c.set_line_width(16); c.set_line_cap(cairo.LINE_CAP_ROUND)
                c.move_to(200, 960); c.line_to(200 + 680 * kk, 940); c.stroke()
    # 7 satellites built for clouds by moonlight
    elif t < S('8') - 0.05:
        g = cairo.RadialGradient(W / 2, 2500, 900, W / 2, 2500, 1500); g.add_color_stop_rgba(0, 0.05, 0.12, 0.28, 1); g.add_color_stop_rgba(1, 0.02, 0.05, 0.12, 1)
        c.set_source(g); c.arc(W / 2, 2500, 1500, 0, 2 * math.pi); c.fill()
        mk = prog(t, A['clouds'] - 0.3, A['clouds'] + 0.4)
        c.set_source_rgba(0.95, 0.95, 0.85, 0.9); c.arc(880, 330, 55, 0, 2 * math.pi); c.fill()
        g2 = cairo.RadialGradient(880, 330, 50, 880, 330, 260); g2.add_color_stop_rgba(0, 1, 1, 0.9, 0.25 * mk); g2.add_color_stop_rgba(1, 1, 1, 0.9, 0); c.set_source(g2); c.paint()
        for i, (cx, cy) in enumerate(((260, 1110), (520, 1060), (790, 1120), (400, 1190), (680, 1200))):
            c.set_source_rgba(0.85, 0.88, 0.95, 0.15 + 0.55 * mk)
            for dx, dy, r in ((-40, 0, 40), (0, -18, 50), (45, 0, 38)): c.arc(cx + dx, cy + dy, r, 0, 2 * math.pi); c.fill()
        ck = prog(t, A['city7'] - 0.2, A['city7'] + 0.8)
        rng = np.random.default_rng(7)
        for i in range(60):
            x = rng.uniform(120, 960); y = rng.uniform(1020, 1320); k = clamp(ck * 60 - i)
            if k > 0: glowdot(c, x, y, 5 + 3 * rng.random(), a=k)
        satellite(c, 200 + 680 * prog(t, S('7'), S('8')), 520, 1.0, ang=0.15)
        if mk > 0: mono(c, 'CLOUDS BY MOONLIGHT', W / 2, 760, 30, CREAM, a=mk, kind='monob')
        if ck > 0: mono(c, '+ CITY LIGHTS', W / 2, 830, 34, AMBER, a=prog(t, A['city7'] - 0.2, A['city7'] + 0.1), kind='monob')
    # 8 NASA's real image
    elif t < S('9') - 0.05:
        head(c, "NASA'S REAL IMAGE", W / 2, 260, 56, CREAM, a=prog(t, A['real8'] - 0.3, A['real8']))
        if t >= A['real8'] - 0.3:
            sf = img(NASAIMG, 880); w, h = sf.get_width(), sf.get_height(); u = e_out(prog(t, A['real8'] - 0.3, A['real8'] + 0.2))
            z = 1.0 + 0.06 * prog(t, A['real8'], S('9'))
            c.save(); c.translate(W / 2, 760 + (1 - u) * 100); c.scale(z, z); rrect(c, -w / 2, -h / 2, w, h, 22); c.clip(); c.set_source_surface(sf, -w / 2, -h / 2); c.paint_with_alpha(u); c.restore()
            pill(c, 'NOV 12, 2012 · DIWALI WEEK', W / 2, 1250, 32, AMBER, s=e_back(prog(t, A['real8'] + 0.4, A['real8'] + 0.7)))
            mono(c, 'NASA EARTH OBSERVATORY · VIIRS / SUOMI NPP', W / 2, 1320, 18, CREAM, a=0.8 * u, kind='mono')
    # 9 fake vs real
    elif t < S('10') - 0.05:
        for j, (path, lab, ok) in enumerate(((VIRAL, 'VIRAL', False), (NASAIMG, 'REAL', True))):
            u = e_out(prog(t, S('9') - 0.05 + 0.15 * j, S('9') + 0.3 + 0.15 * j)); x = 90 + j * 470
            sf = img(path, 430); w, h = sf.get_width(), min(sf.get_height(), 430)
            c.save(); c.translate(0, (1 - u) * 50); rrect(c, x, 400, 430, 430, 22); c.clip(); c.set_source_surface(sf, x, 400); c.paint_with_alpha(u); c.restore()
            if ok: c.set_source_rgba(*AMBER, u); c.set_line_width(6); rrect(c, x, 400, 430, 430, 22); c.stroke()
            head(c, lab, x + 215, 900, 60, AMBER if ok else CREAM, a=u, shadow=False)
            k = prog(t, (S('9') + 0.6) if ok else A['rainbow'] - 0.2, (S('9') + 0.9) if ok else A['rainbow'] + 0.1)
            (tick if ok else cross)(c, x + 215, 1040, 1.6, k, AMBER if ok else CREAM)
        mono(c, 'ORANGE + WHITE = STREET LIGHTS', W / 2, 1200, 26, AMBER, a=prog(t, S('9') + 0.4, S('9') + 0.7), kind='monob')
    # 10 NASA proof card
    elif t < S('11') - 0.05:
        c.set_source_rgba(0, 0, 0, 0.35); c.paint()
        draw_clip(c, 'nasa_h1', W / 2, 560, 760, t, S('10') - 0.05, rot=-1.0)
        draw_clip(c, 'nasa_para', W / 2, 840, 1010, t, S('10') + 0.15, rot=0.6, hl_t0=A['subtle'] - 0.2, hl_dur=1.6)
        source_tag(c, 'NASA EARTH OBSERVATORY · SOUTH ASIAN NIGHT LIGHTS', 90, 960, a=prog(t, S('10') + 0.3, S('10') + 0.6))
    # 11 the pixel
    elif t < S('12') - 0.05:
        satellite(c, W / 2, 300, 0.9)
        k = prog(t, A['k824'] - 0.4, A['k824'] + 0.3)
        c.set_source_rgba(*AMBER, 0.8); c.set_line_width(4); c.set_dash([10, 10]); c.move_to(W / 2, 360); c.line_to(W / 2, 360 + 500 * k); c.stroke(); c.set_dash([])
        if t >= A['k824'] - 0.1: big_num(c, '824 KM', 790, 600, 90, t, A['k824'] - 0.1)
        # colony map
        gy = 900
        for i in range(9):
            for j in range(4):
                c.set_source_rgba(0.22, 0.22, 0.26, 1); c.rectangle(160 + i * 86, gy + j * 86, 70, 70); c.fill()
        if t >= A['m750'] - 0.3:
            u = e_out(prog(t, A['m750'] - 0.3, A['m750'] + 0.1)); yy = 360 + (gy - 20 - 360) * u
            c.set_source_rgba(*AMBER, 0.25); c.rectangle(300, yy, 480, 380); c.fill()
            c.set_source_rgba(*AMBER, 1); c.set_line_width(6); c.rectangle(300, yy, 480, 380); c.stroke()
            if u >= 1:
                pill(c, '1 PIXEL ≈ 750 m', W / 2, 820, 40, AMBER)
                mono(c, 'VIIRS DAY/NIGHT BAND · NOMINAL RESOLUTION', W / 2, 1300, 18, CREAM, a=0.8, kind='mono')
        if t >= A['hood'] - 0.2: head(c, 'A WHOLE NEIGHBOURHOOD', W / 2, 1240, 52, CREAM, a=prog(t, A['hood'] - 0.2, A['hood'] + 0.1))
    # 12 diyas blend in
    elif t < S('13') - 0.05:
        c.set_source_rgba(*AMBER, 1); c.set_line_width(6); c.rectangle(140, 330, 640, 640); c.stroke()
        mono(c, 'INSIDE 1 PIXEL', 460, 300, 24, AMBER, kind='monob')
        rng = np.random.default_rng(3)
        for i in range(70):
            x, y = 170 + rng.uniform(0, 580), 360 + rng.uniform(0, 580); fl = 0.6 + 0.4 * math.sin(t * 9 + i)
            c.set_source_rgba(1.0, 0.75, 0.3, 0.9 * fl * prog(t, S('12'), S('12') + 0.5)); c.arc(x, y, 3, 0, 2 * math.pi); c.fill()
        if t >= A['street'] - 0.2:
            k = prog(t, A['street'] - 0.2, A['street'] + 0.4)
            for i in range(6):
                for j in range(6): glowdot(c, 200 + i * 104, 390 + j * 104, 11, a=k)
        mono(c, 'DIYAS', 300, 1010, 26, CREAM, a=prog(t, S('12'), S('12') + 0.3), kind='monob')
        if t >= A['street'] - 0.2: mono(c, 'STREET LIGHTS · EVERY NIGHT', 520, 1060, 22, AMBER, a=prog(t, A['street'] - 0.2, A['street']), kind='monob')
        # brightness meter
        glass_dark(c, 840, 330, 140, 640, 30)
        lev = 0.72 + 0.04 * prog(t, A['blends'] - 0.4, A['blends'])
        rrect(c, 870, 330 + 610 - 580 * lev, 80, 580 * lev, 20); c.set_source(agrad(870, 0, 950, 0)); c.fill()
        mono(c, 'BRIGHTNESS', 910, 1000, 18, CREAM, kind='monob')
        if t >= A['blends'] - 0.2: head(c, 'DIWALI BLENDS IN', W / 2, 1200, 64, AMBER, a=prog(t, A['blends'] - 0.2, A['blends'] + 0.1))
    # 13 the reply
    elif t < S('14') - 0.05:
        full = 'Beautiful map. Wrong night.' if LANGV == 'en' else 'Map బాగుంది. రాత్రే తప్పు.'
        raju(c, 250, 1180, 1.05, t, react=prog(t, A['wrong'] + 0.4, A['wrong'] + 0.7))
        mono(c, 'RAJU UNCLE', 250, 1235, 28, CREAM, kind='monob')
        chat_panel(c, t, S('13') - 0.3, count_t=S('13') - 2.0, reply_t=A['reply'] + 0.1, reply_full=full)
    # 14 series slide + CTA
    elif t < S('L') - 0.05:
        caps = t < END_T0 - 0.3
        sc_ = 1.0 - 0.14 * e_io(prog(t, END_T0 - 0.5, END_T0))
        slide(c, t, S('14') - 0.05, scale=sc_)
        CTA.draw(c, t, END_T0, PLAT, LANGV, y=1745)
    else:
        k = e_io(prog(t, S('L') - 0.05, S('L') + 0.7))
        c.push_group(); slide(c, t, S('14') - 0.05, scale=0.86); CTA.draw(c, t, END_T0, PLAT, LANGV, y=1745); c.pop_group_to_source(); c.paint_with_alpha(1 - k)
        c.push_group(); board_bg(c, 0.0); sc_hook(c, 0.0, frozen=True); tag(c); c.pop_group_to_source(); c.paint_with_alpha(k)
    if caps: (K.captions(c, t, y=1440) if LANGV == 'en' else R3.te_captions(c, t, y=1440))
    if t < S('14') - 0.05: tag(c)
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
