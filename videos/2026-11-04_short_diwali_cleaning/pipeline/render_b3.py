"""DIWALI · 3/6 'Why every home gets deep-cleaned before Diwali' — style v2, loops into its own opening."""
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
ROOT = '/home/claude/b3/'
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
    'cupboards': AT('1', 'Cupboards', 'బీరువాలు'), 'fans': AT('1', 'Fans', 'Fans'), 'walls': AT('1', 'Walls', 'గోడలకి'), 'why1': AT('1', 'Why', 'ఎందుకు'),
    'lakshmi': AT('2', 'Lakshmi', 'లక్ష్మీదేవి'), 'timing2': AT('2', 'timing', 'timing'),
    'oct15': AT('3', 'October', 'October'), 'nov8': AT('3', 'November', 'November'),
    'damp': AT('4', 'Damp', 'తడి', n=2 if LANGV == 'en' else 1), 'black': AT('4', 'Black', 'నల్ల'), 'smell': AT('4', 'smell', 'వాసన'),
    'epa': AT('5', 'EPA', 'EPA'), 'sixty': AT('5', '60', '60'), 'hard': AT('5', 'hard', 'కష్టం'),
    'clean6': AT('6', 'clean', 'శుభ్రం'),
    'lime7': AT('7', 'Lime', 'సున్నం'),
    'ph': AT('8', '12.4', '12.4'), 'germs8': AT('8', 'germs', 'క్రిములను'),
    'white9': AT('9', 'white', 'తెలుపు'), 'while9': AT('9', 'while', 'కాలం'),
    'co2': AT('10', 'carbon', 'carbon'), 'caco3': AT('10', 'calcium', 'calcium'), 'limestone': AT('10', 'limestone', 'సున్నపురాయిలో'),
    'practical': AT('11', 'practical', 'practical'),
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
    txt = 'DIWALI · 3/6' if LANGV == 'en' else 'దీపావళి · 3/6'
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
        (sx, sy), (ex, ey) = SL[LANGV][4][1], SL[LANGV][5][1]; sy += 200; ey += 200
        x = sx + (ex - sx) * e_io(k); y = sy + (ey - sy) * e_io(k) - math.sin(k * math.pi) * 120
        glowdot(c, x, y, 13 if k < 1 else 10 + 2 * math.sin(t * 6))
    c.pop_group_to_source(); c.paint_with_alpha(a); c.restore()


# ---------------- 3/6 drawings ----------------
WALL = (0.80, 0.74, 0.62); FLOOR = (0.30, 0.24, 0.20)
def room(c, t, chaos=1.0, painted=0.5, a=1.0):
    """drawn living room, wall area y 260..1180"""
    c.save(); c.push_group()
    c.set_source_rgb(*WALL); c.rectangle(60, 260, 960, 820); c.fill()
    c.set_source_rgb(0.92, 0.90, 0.84); c.rectangle(60, 260, 960 * painted, 820); c.fill()           # fresh paint part
    c.set_source_rgb(*FLOOR); c.rectangle(60, 1080, 960, 100); c.fill()
    # cupboard (left)
    c.set_source_rgb(0.45, 0.30, 0.20); c.rectangle(110, 560, 260, 520); c.fill()
    if chaos > 0:
        c.save(); c.translate(110, 560); c.rotate(-0.6 * chaos); c.set_source_rgb(0.55, 0.37, 0.24); c.rectangle(-120, 0, 120, 520); c.fill(); c.restore()
        for i, col in enumerate(((0.9, 0.4, 0.4), (0.4, 0.6, 0.9), (0.95, 0.8, 0.3), (0.5, 0.8, 0.5))):
            c.set_source_rgba(*col, chaos); rrect(c, 140 + i * 50, 1000 - (i % 2) * 30, 120, 60, 18); c.fill()
    # ceiling fan + stepladder (middle)
    c.set_source_rgb(0.25, 0.25, 0.28); c.rectangle(535, 260, 10, 80); c.fill()
    for k in range(3):
        an = k * 2 * math.pi / 3 + (0 if chaos > 0 else t * 4)
        c.save(); c.translate(540, 345); c.rotate(an); c.set_source_rgb(0.55, 0.55, 0.58); rrect(c, 10, -14, 150, 28, 12); c.fill(); c.restore()
    if chaos > 0:
        c.set_source_rgba(0.75, 0.6, 0.3, chaos); c.set_line_width(12)
        c.move_to(470, 1080); c.line_to(520, 640); c.move_to(610, 1080); c.line_to(560, 640); c.stroke()
        for y in range(700, 1080, 90): c.move_to(500 - (y - 700) * 0.0, y); c.line_to(580, y)
        c.stroke()
    # paint roller on the wall (right)
    if chaos > 0:
        rx = 60 + 960 * painted
        c.set_source_rgba(0.3, 0.3, 0.32, chaos); c.set_line_width(10); c.move_to(rx + 30, 760); c.line_to(rx + 30, 980); c.stroke()
        rrect(c, rx, 700, 70, 70, 14); c.set_source_rgba(0.95, 0.93, 0.88, chaos); c.fill()
    # broom leaning (right corner) — same spot as the loop line
    broom(c, 900, 1080, 1.0, a=1.0)
    c.pop_group_to_source(); c.paint_with_alpha(a); c.restore()
def broom(c, x, y, s, a=1.0, ang=-0.18):
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    c.set_source_rgba(0.55, 0.38, 0.22, a); c.rectangle(-6, -560, 12, 460); c.fill()
    c.set_source_rgba(0.82, 0.68, 0.36, a)
    c.move_to(-14, -110); c.line_to(14, -110); c.line_to(60, 0); c.line_to(-60, 0); c.close_path(); c.fill()
    c.set_source_rgba(0.6, 0.45, 0.2, a); c.set_line_width(3)
    for k in range(-50, 60, 12): c.move_to(k * 0.25, -105); c.line_to(k, 0)
    c.stroke(); c.restore()
def diya(c, x, y, s, t, a=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    fl = 0.8 + 0.2 * math.sin(t * 9 + x)
    g = cairo.RadialGradient(0, -30, 0, 0, -30, 70); g.add_color_stop_rgba(0, 1, 0.8, 0.4, 0.5 * a * fl); g.add_color_stop_rgba(1, 1, 0.8, 0.4, 0); c.set_source(g); c.arc(0, -30, 70, 0, 2 * math.pi); c.fill()
    c.set_source_rgba(0.78, 0.40, 0.18, a); c.move_to(-40, 0); c.curve_to(-30, 30, 30, 30, 40, 0); c.close_path(); c.fill()
    c.set_source_rgba(1.0, 0.75, 0.25, a); c.move_to(0, -10); c.curve_to(-10, -25, -4, -40, 0, -55 * fl); c.curve_to(4, -40, 10, -25, 0, -10); c.fill()
    c.restore()
CHAIN = ['MONSOON', 'MOISTURE', 'MOULD', 'DRY', 'LIME']
def chain(c, t, active, a=1.0):
    """subdued chain across the top; current word glows amber"""
    if a <= 0: return
    xs = [130, 330, 540, 730, 920]
    for i, (w_, x) in enumerate(zip(CHAIN, xs)):
        on = i == active; past = i < active
        if on: pill(c, w_, x, 215, 24, AMBER, a=a)
        else: mono(c, w_, x, 215, 20, AMBER if past else CREAM, a=a * (0.75 if past else 0.35), kind='monob')
        if i < 4: mono(c, '→', (x + xs[i + 1]) / 2 + 8, 215, 20, CREAM, a=0.35 * a, kind='monob')
def germ(c, x, y, r, a=1.0, kind=0):
    if a <= 0.01: return
    c.save(); c.translate(x, y)
    col = (0.45, 0.75, 0.40) if kind == 0 else (0.70, 0.45, 0.85)
    c.set_source_rgba(*col, a); c.set_line_width(4)
    for k in range(8):
        an = k * math.pi / 4; c.move_to(math.cos(an) * r, math.sin(an) * r); c.line_to(math.cos(an) * r * 1.4, math.sin(an) * r * 1.4)
    c.stroke(); c.arc(0, 0, r, 0, 2 * math.pi); c.fill()
    c.set_source_rgba(0, 0, 0, 0.4 * a); c.arc(-r * 0.3, -r * 0.2, r * 0.18, 0, 2 * math.pi); c.fill(); c.arc(r * 0.3, -r * 0.2, r * 0.18, 0, 2 * math.pi); c.fill()
    c.restore()
def meter(c, cx, cy, val, a=1.0):
    """semicircle humidity meter, val 0..1 (0.6 = the EPA line)"""
    c.save(); c.translate(cx, cy)
    for k in range(60):
        f0, f1 = k / 60, (k + 1) / 60; col = (0.35, 0.8, 0.45) if f0 < 0.6 else (0.95, 0.55, 0.2)
        c.set_source_rgba(*col, a); c.set_line_width(36); c.new_path(); c.arc(0, 0, 260, math.pi + f0 * math.pi, math.pi + f1 * math.pi + 0.005); c.stroke()
    an = math.pi + val * math.pi
    c.set_source_rgba(*CREAM, a); c.set_line_width(10); c.set_line_cap(cairo.LINE_CAP_ROUND); c.move_to(0, 0); c.line_to(math.cos(an) * 230, math.sin(an) * 230); c.stroke()
    c.arc(0, 0, 18, 0, 2 * math.pi); c.fill()
    an6 = math.pi + 0.6 * math.pi; c.set_source_rgba(*CREAM, a); c.set_line_width(4); c.move_to(math.cos(an6) * 200, math.sin(an6) * 200); c.line_to(math.cos(an6) * 300, math.sin(an6) * 300); c.stroke()
    mono(c, '60%', math.cos(an6) * 335, math.sin(an6) * 335, 26, CREAM, a=a, kind='monob')
    c.restore()

def chem(c, x, y, px):
    """Ca(OH)2 -> CaCO3 with real subscripts"""
    parts = [('Ca(OH)', 0), ('2', 1), ('CaCO', 0), ('3', 1)]
    font(c, 'head', px); tot = 0
    for txt_, sub in parts: font(c, 'head', px * (0.6 if sub else 1)); tot += c.text_extents(txt_).x_advance
    tot += px * 1.75; xx = x - tot / 2
    for i, (txt_, sub) in enumerate(parts):
        font(c, 'head', px * (0.6 if sub else 1)); c.move_to(xx, y + px * 0.35 + (px * 0.18 if sub else 0)); c.set_source_rgb(*AMBER); c.show_text(txt_); xx += c.text_extents(txt_).x_advance
        if i == 1:
            xx += px * 0.4; c.set_line_width(6); c.move_to(xx, y); c.line_to(xx + px * 0.75, y); c.stroke()
            c.move_to(xx + px * 0.85, y); c.line_to(xx + px * 0.55, y - px * 0.22); c.line_to(xx + px * 0.55, y + px * 0.22); c.close_path(); c.fill(); xx += px * 1.25
def sc_hook(c, t, frozen=False):
    tt = 0.0 if frozen else t
    chaos = 1.0
    room(c, tt, chaos=chaos, painted=0.45)
    mono(c, 'DIWALI CLEANING', W / 2, 1230, 30, CREAM, kind='monob')
    head(c, 'WHY RIGHT NOW?', W / 2, 1320, 84, AMBER)
    if not frozen:
        for i, (lab, key, x, y) in enumerate((('CUPBOARDS OUT', 'cupboards', 240, 480), ('FANS DOWN', 'fans', 540, 470), ('WALLS PAINTED', 'walls', 830, 600))):
            if t >= A[key] - 0.1: pill(c, lab, x, y, 26, AMBER, s=e_back(prog(t, A[key] - 0.1, A[key] + 0.15)))

def frame(t):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s)
    board_bg(c, t)
    caps = True
    if t < S('2') - 0.05:
        sc_hook(c, t)
    # 2 belief + timing
    elif t < S('3') - 0.05:
        c.set_source_rgb(0.35, 0.18, 0.12); c.rectangle(300, 330, 480, 700); c.fill()            # doorway
        c.set_source_rgb(0.08, 0.06, 0.06); c.rectangle(340, 370, 400, 660); c.fill()
        for i in range(5): diya(c, 260 + i * 140, 1110, 0.8, t, a=prog(t, S('2') + 0.1 * i, S('2') + 0.3 + 0.1 * i))
        for r_, col in ((150, (0.95, 0.3, 0.35)), (110, AMBER), (70, (0.3, 0.7, 0.9)), (30, CREAM)):     # rangoli
            c.set_source_rgba(*col, 0.85); c.save(); c.translate(W / 2, 1180); c.scale(1, 0.35); c.arc(0, 0, r_, 0, 2 * math.pi); c.restore(); c.fill()
        for j, (lab, t0) in enumerate((('BELIEF', A['lakshmi'] - 0.2), ('TIMING', A['timing2'] - 0.2))):
            if t < t0: continue
            u = e_back(prog(t, t0, t0 + 0.3)); x = 290 + j * 500
            c.save(); c.translate(x, 520); c.scale(max(0.01, u), max(0.01, u)); glass_dark(c, -200, -70, 400, 140, 30)
            c.set_source_rgba(*AMBER, 1); c.set_line_width(4); rrect(c, -200, -70, 400, 140, 30); c.stroke()
            head(c, lab, 0, 0, 60, AMBER, shadow=False); c.restore()
    # 3 calendar + IMD
    elif t < S('4') - 0.05:
        chain(c, t, 0)
        u = e_out(prog(t, S('3'), S('3') + 0.4))
        for j, (lab, sub, t0) in enumerate((('OCT 15', 'MONSOON GONE', A['oct15'] - 0.2), ('NOV 8', 'DIWALI', A['nov8'] - 0.2))):
            if t < t0: continue
            k = e_out(prog(t, t0, t0 + 0.3)); x = 110 + j * 560
            glass_dark(c, x, 330, 300, 230, 30, k); c.set_source_rgba(*AMBER, k); c.rectangle(x, 330, 300, 56); c.fill()
            mono(c, sub, x + 150, 358, 20, INK, a=k, kind='monob'); head(c, lab, x + 150, 470, 66, CREAM, a=k, shadow=False)
        if t >= A['nov8']:
            k = prog(t, A['nov8'], A['nov8'] + 0.8); n = int(round(24 * e_out(k)))
            c.set_source_rgba(*AMBER, 0.9); c.set_line_width(6); c.set_dash([12, 10]); c.move_to(420, 445); c.line_to(420 + 250 * k, 445); c.stroke(); c.set_dash([])
            big_num(c, str(n), W / 2 - 90, 650, 110, t, A['nov8']); head(c, 'DAYS', W / 2 + 90, 655, 70, AMBER, a=prog(t, A['nov8'], A['nov8'] + 0.3))
        t1 = A['oct15'] + 0.2
        draw_clip(c, 'imd', 644, 900, 1250, t, t1, rot=-0.8, hl_t0=t1 + 0.4, hl_dur=1.1)
        source_tag(c, 'IMD PRESS RELEASE · 15 OCT 2026', 90, 1010, a=prog(t, t1 + 0.2, t1 + 0.5))
    # 4 damp walls
    elif t < A['damp'] - 0.4:
        # "across much of India": the same IMD release, highlight shifts to the south (NE monsoon)
        chain(c, t, 1)
        draw_clip(c, 'imd2', 515, 700, 1250, t, S('4') - 0.3, rot=0.6, hl_t0=S('4') + 0.1, hl_dur=1.3)
        source_tag(c, 'IMD PRESS RELEASE · 15 OCT 2026', 90, 810, a=1.0)
        pill(c, 'SOUTH INDIA DIFFERS · NE MONSOON OCT–DEC', W / 2, 960, 26, AMBER, s=e_back(prog(t, S('4') + 0.6, S('4') + 0.9)))
    elif t < S('5') - 0.05:
        chain(c, t, 1)
        c.set_source_rgb(*WALL); c.rectangle(90, 300, 900, 900); c.fill()
        k = prog(t, A['damp'] - 0.3, A['damp'] + 1.2)
        for i in range(5):
            g = cairo.RadialGradient(200 + i * 170, 420 + (i % 2) * 300, 0, 200 + i * 170, 420 + (i % 2) * 300, 180 * k)
            g.add_color_stop_rgba(0, 0.45, 0.42, 0.35, 0.6 * k); g.add_color_stop_rgba(1, 0.45, 0.42, 0.35, 0); c.set_source(g); c.paint()
        rng = np.random.default_rng(5)
        for i in range(60):
            x, y = 110 + rng.uniform(0, 300), 320 + rng.uniform(0, 400); k2 = clamp((t - A['black'] + 0.3) * 30 - i)
            if k2 > 0: c.set_source_rgba(0.08, 0.08, 0.06, 0.85 * min(1, k2)); c.arc(x, y, rng.uniform(4, 16), 0, 2 * math.pi); c.fill()
        if t >= A['smell'] - 0.3:        # cupboard + smell lines
            kk = prog(t, A['smell'] - 0.3, A['smell'])
            c.set_source_rgba(0.45, 0.30, 0.20, kk); c.rectangle(640, 700, 300, 480); c.fill()
            c.set_source_rgba(0.55, 0.65, 0.35, kk); c.set_line_width(7)
            for j in range(3):
                x0 = 720 + j * 70; c.move_to(x0, 680)
                for yy in range(680, 480, -20): c.line_to(x0 + 14 * math.sin(yy / 18 + t * 4), yy)
                c.stroke()
        cur = None
        for lab, key in (('DAMP WALLS', 'damp'), ('BLACK SPOTS', 'black'), ('THAT SMELL', 'smell')):
            if t >= A[key] - 0.1: cur = (lab, key)
        if cur: pill(c, cur[0], W / 2, 1270, 34, AMBER, s=e_back(prog(t, A[cur[1]] - 0.1, A[cur[1]] + 0.2)))
    # 5 humidity meter + EPA
    elif t < S('6') - 0.05:
        chain(c, t, 2)
        v = 0.25 + 0.6 * e_io(prog(t, S('5'), A['sixty']))
        meter(c, W / 2, 700, v)
        mono(c, 'INDOOR HUMIDITY', W / 2, 760, 26, CREAM, kind='monob')
        if v > 0.65: pill(c, 'MOULD ZONE', W / 2, 340, 30, AMBER)
        ct0 = min(A['epa'], A['sixty']) - 0.4
        draw_clip(c, 'epa', W / 2, 1000, 900, t, ct0, rot=0.8, hl_t0=max(A['sixty'] - 0.3, ct0 + 0.5), hl_dur=1.3)
        source_tag(c, 'US EPA · MOLD COURSE', 90, 1250, a=prog(t, ct0 + 0.2, ct0 + 0.5))
    # 6 dry weeks
    elif t < S('7') - 0.05:
        chain(c, t, 3)
        k = e_io(prog(t, S('6'), S('6') + 1.6))
        g = cairo.RadialGradient(W / 2, 300, 0, W / 2, 300, 700); g.add_color_stop_rgba(0, 1, 0.85, 0.5, 0.45 * k); g.add_color_stop_rgba(1, 1, 0.85, 0.5, 0); c.set_source(g); c.paint()
        c.set_source_rgba(0.55, 0.75, 0.95, 0.35 + 0.4 * k); c.rectangle(340, 300, 400, 300); c.fill()
        c.set_source_rgba(0.45, 0.30, 0.20, 1); c.set_line_width(14); c.rectangle(340, 300, 400, 300); c.stroke(); c.move_to(540, 300); c.line_to(540, 600); c.stroke()
        c.set_source_rgba(1, 0.9, 0.5, k); c.arc(640, 380, 50, 0, 2 * math.pi); c.fill()
        meter(c, W / 2, 1000, 0.85 - 0.55 * k)
        if k > 0.6: pill(c, 'DRY', W / 2, 1110, 40, AMBER, s=e_back(prog(t, S('6') + 1.0, S('6') + 1.3)))
        if t >= A['clean6'] - 0.2: mono(c, 'CLEAN · DRY · PAINT', W / 2, 1220, 34, CREAM, a=prog(t, A['clean6'] - 0.2, A['clean6'] + 0.2), kind='monob')
    # 7 lime
    elif t < S('8') - 0.05:
        chain(c, t, 4)
        c.set_source_rgb(0.55, 0.42, 0.30); c.move_to(160, 560); c.line_to(540, 360); c.line_to(920, 560); c.close_path(); c.fill()   # roof
        k = prog(t, A['lime7'] - 0.3, A['lime7'] + 0.6)
        c.set_source_rgb(0.62, 0.55, 0.45); c.rectangle(220, 560, 640, 460); c.fill()
        c.set_source_rgba(0.97, 0.96, 0.92, 1); c.rectangle(220, 560, 640 * k, 460); c.fill()
        c.set_source_rgb(0.35, 0.22, 0.14); c.rectangle(480, 760, 120, 260); c.fill()
        c.set_source_rgb(0.5, 0.5, 0.55); c.move_to(200, 1060); c.line_to(320, 1060); c.line_to(300, 1180); c.line_to(220, 1180); c.close_path(); c.fill()  # bucket
        c.set_source_rgb(0.97, 0.96, 0.92); c.save(); c.translate(260, 1065); c.scale(1, 0.25); c.arc(0, 0, 58, 0, 2 * math.pi); c.restore(); c.fill()
        if t >= A['lime7'] - 0.1: head(c, 'LIME · SUNNAM', W / 2, 1270, 60, AMBER, a=prog(t, A['lime7'] - 0.1, A['lime7'] + 0.2))
    # 8 pH
    elif t < S('9') - 0.05:
        chain(c, t, 4)
        x0, x1, y = 120, 960, 420
        for i in range(15):
            f = i / 14; col = (0.95 - 0.5 * f, 0.35 + 0.4 * (1 - abs(f - 0.5) * 2), 0.3 + 0.6 * f)
            c.set_source_rgba(*col, 1); c.rectangle(x0 + (x1 - x0) * i / 15, y, (x1 - x0) / 15 + 1, 70); c.fill()
            mono(c, str(i), x0 + (x1 - x0) * (i + 0.5) / 15, y + 105, 18, CREAM, a=0.8, kind='mono')
        mono(c, 'ACID', x0, y - 30, 20, CREAM, anchor='l', kind='monob'); mono(c, 'NEUTRAL', (x0 + x1) / 2, y - 30, 20, CREAM, kind='monob'); mono(c, 'ALKALINE', x1, y - 30, 20, CREAM, anchor='r', kind='monob')
        k = e_io(prog(t, S('8'), A['ph'])); px = x0 + (x1 - x0) * (7 + 5.4 * k) / 15
        c.set_source_rgba(*AMBER, 1); c.move_to(px, y - 8); c.line_to(px - 18, y - 40); c.line_to(px + 18, y - 40); c.close_path(); c.fill()
        if t >= A['ph'] - 0.1:
            big_num(c, 'pH 12.4', W / 2, 660, 120, t, A['ph'] - 0.1)
            mono(c, 'STRONGLY ALKALINE', W / 2, 760, 28, AMBER, a=prog(t, A['ph'], A['ph'] + 0.3), kind='monob')
        rng = np.random.default_rng(9)
        for i in range(8):
            gx, gy = 150 + i * 110, 870 + (i % 2) * 70; tf = A['germs8'] - 0.2 + 0.15 * i
            al = 1 - prog(t, tf, tf + 0.6)
            if i in (2, 6): al = max(al, 0.55)   # not everything vanishes
            germ(c, gx, gy, 26, a=al * prog(t, S('8'), S('8') + 0.4), kind=i % 2)
        if t >= A['germs8'] - 0.2: mono(c, 'CAN INACTIVATE MANY PATHOGENS', W / 2, 1010, 24, CREAM, a=prog(t, A['germs8'], A['germs8'] + 0.3), kind='monob')
        draw_clip(c, 'sr_ph', 38, 1150, 1700, t, A['ph'] + 0.3, rot=-0.6, hl_t0=A['ph'] + 0.6, hl_dur=1.0)
        source_tag(c, 'SCIENTIFIC REPORTS · 2021', 90, 1250, a=prog(t, A['ph'] + 0.5, A['ph'] + 0.8))
    # 9 fresh coat, for a while
    elif t < S('10') - 0.05:
        chain(c, t, 4)
        c.set_source_rgb(0.62, 0.55, 0.45); c.rectangle(140, 320, 800, 640); c.fill()
        k = e_io(prog(t, S('9'), A['white9'] + 0.3))
        c.set_source_rgba(0.98, 0.97, 0.93, 1); c.rectangle(140, 320, 800 * k, 640); c.fill()
        broom_x = 140 + 800 * k
        c.set_source_rgba(0.82, 0.68, 0.36, 1); c.rectangle(broom_x - 20, 600, 40, 120); c.fill()
        if t >= A['while9'] - 0.3:
            kk = prog(t, A['while9'] - 0.3, S('10'))
            c.set_source_rgba(1, 1, 1, 0.15); c.set_line_width(18); c.arc(W / 2, 1110, 90, 0, 2 * math.pi); c.stroke()
            c.set_source_rgba(*AMBER, 1); c.arc(W / 2, 1110, 90, -math.pi / 2, -math.pi / 2 + 2 * math.pi * (1 - kk * 0.6)); c.stroke()
            mono(c, 'FOR A WHILE', W / 2, 1110, 24, CREAM, kind='monob')
            for i in range(4): germ(c, 260 + i * 180, 640, 24, a=0.7 * (1 - prog(t, A['while9'] + 0.1 * i, A['while9'] + 0.5 + 0.1 * i)), kind=i % 2)
    # 10 carbonation
    elif t < S('11') - 0.05:
        chain(c, t, 4)
        c.set_source_rgba(0.98, 0.97, 0.93, 1); c.rectangle(140, 320, 800, 520); c.fill()
        k = prog(t, A['co2'] - 0.2, A['caco3'] + 0.8)
        c.set_source_rgba(0.75, 0.72, 0.65, 0.6 * k); c.rectangle(140, 320, 800, 520); c.fill()
        rng = np.random.default_rng(2)
        for i in range(16):
            x = 180 + rng.uniform(0, 720); y = 900 - ((t - A['co2'] + i * 0.2) * 160) % 560
            if t >= A['co2'] - 0.2:
                c.set_source_rgba(0.6, 0.8, 1.0, 0.7); c.set_line_width(3); c.new_path(); c.arc(x, y, 18, 0, 2 * math.pi); c.stroke()
                font(c, 'monob', 14); c.move_to(x - 15, y + 5); c.set_source_rgba(0.6, 0.8, 1.0, 0.9); c.show_text('CO₂')
        if t >= A['caco3'] - 0.2:
            u = e_back(prog(t, A['caco3'] - 0.2, A['caco3'] + 0.1))
            c.save(); c.translate(W / 2, 960); c.scale(max(0.01, u), max(0.01, u)); glass_dark(c, -420, -70, 840, 140, 30)
            chem(c, 0, 0, 58); c.restore()
        if t >= A['limestone'] - 0.3:
            pill(c, 'LIME → LIMESTONE MINERAL', W / 2, 1140, 34, CREAM, s=e_back(prog(t, A['limestone'] - 0.3, A['limestone'])))
            c.set_source_rgba(0.6, 0.58, 0.52, 1); c.move_to(470, 1290); c.line_to(510, 1220); c.line_to(580, 1210); c.line_to(620, 1260); c.line_to(600, 1300); c.close_path(); c.fill()
    # 11 belief + timing, equal
    elif t < S('12') - 0.05:
        for j, (lab, col) in enumerate((('OLD HOME', (0.97, 0.96, 0.92)), ('TODAY', (0.80, 0.82, 0.86)))):
            x = 90 + j * 470
            c.set_source_rgb(*col); c.rectangle(x, 360, 430, 420); c.fill()
            c.set_source_rgb(0.45, 0.32, 0.22) if j == 0 else c.set_source_rgb(0.35, 0.38, 0.45)
            c.rectangle(x, 780, 430, 50); c.fill()
            broom(c, x + 330, 820, 0.6)
            mono(c, lab, x + 215, 880, 24, CREAM, kind='monob')
        for j, lab in enumerate(('BELIEF', 'TIMING')):
            x = 320 + j * 440; u = e_back(prog(t, S('11') + 0.2 * j, S('11') + 0.3 + 0.2 * j))
            c.save(); c.translate(x, 1050); c.scale(max(0.01, u), max(0.01, u)); glass_dark(c, -190, -65, 380, 130, 30)
            c.set_source_rgba(*AMBER, 1); c.set_line_width(4); rrect(c, -190, -65, 380, 130, 30); c.stroke()
            head(c, lab, 0, 0, 56, AMBER, shadow=False); c.restore()
        if t >= A['practical']: head(c, '+', W / 2, 1050, 70, CREAM, a=prog(t, A['practical'], A['practical'] + 0.2), shadow=False)
    # 12 series slide
    elif t < S('L') - 0.05:
        caps = t < END_T0 - 0.3
        sc_ = 1.0 - 0.14 * e_io(prog(t, END_T0 - 0.5, END_T0))
        slide(c, t, S('12') - 0.05, scale=sc_)
        CTA.draw(c, t, END_T0, PLAT, LANGV, y=1745)
    else:
        # broom slides in to the exact spot it leans in frame 0, then the chaos room fades in around it
        k = e_io(prog(t, S('L') + 0.35, S('L') + 1.1)); ks = e_io(prog(t, S('L') - 0.05, S('L') + 0.45))
        c.push_group(); slide(c, t, S('12') - 0.05, scale=0.86); CTA.draw(c, t, END_T0, PLAT, LANGV, y=1745); c.pop_group_to_source(); c.paint_with_alpha(1 - ks)
        c.push_group(); board_bg(c, 0.0); sc_hook(c, 0.0, frozen=True); tag(c); c.pop_group_to_source(); c.paint_with_alpha(k)
        if k < 1:
            u = e_out(prog(t, S('L') - 0.05, S('L') + 0.6))
            broom(c, 900 + (1 - u) * 420, 1080, 1.0, a=1 - k)
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
