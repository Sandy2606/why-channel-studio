"""DIWALI · 1/6 'Is your Diwali bonus a gift… or the law?' — style v2, loops into its own opening."""
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
ROOT = '/home/claude/b1/'
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
A = {
    'gift': AT('1', 'gift', 'బహుమతా'), 'law1': AT('1', 'law', 'చట్టం'), 'company1': AT('1', 'company', 'company'), 'n21': AT('1', '21,000', '21,000'),
    'corr': AT('2', 'correction', 'correction'), 'y1965': AT('2', '1965', '1965'), 'sorry': AT('2', 'Sorry', 'Sorry'), 'since': AT('2', 'Since', 'November'), 'code2': AT('2', 'Code', 'Code'),
    'merge': AT('3', 'one.', 'కలిపింది'), 'never': AT('3', 'never', 'Diwali'), 'annual': AT('3', 'annual', 'సంవత్సరానికి'), 'many': AT('3', 'Many', 'Companies'),
    'test': AT('4', 'test', 'test'), 'ravi': AT('4', 'Ravi', 'రవి'), 'boxes': AT('4', 'boxes', 'boxes'), 'counts': AT('4', 'counts', 'లెక్కించే'), 'r18': AT('4', '18,000', '18,000'),
    'less': AT('5', 'less', 'తక్కువ'), 'd30': AT('5', '30', '30'), 'must': AT('5', 'must', 'ఇవ్వాల్సిందే'), 'old5': AT('5', 'Old', 'పాత'),
    'arjun': AT('6', 'Arjun', 'అర్జున్'), 'a45': AT('6', '45,000', '45,000'), 'more': AT('6', 'more', 'ఎక్కువ'), 'cover': AT('6', 'cover', 'వర్తించదు'), 'contract': AT('6', 'contract', 'contract'),
    'howmuch': S('8'), 'catch': AT('8', 'catch', 'trick'), 'notfull': AT('8', 'not', 'పూర్తి'),
    'minw': S('9'), 'skilled': AT('9', 'skilled', 'skill'), 'where': AT('9', 'where', 'ఎక్కడ'), 'city': AT('9', 'city', 'City'),
    'earlier': S('10'), 'every': AT('10', 'every', 'ప్రతి'),
    'say': S('11'), 'm12': AT('11', '12,000', '12,000'), 'that12': AT('11', '12,000', '12,000', n=2), 'not18': AT('11', '18,000', '18,000'),
    'pct': S('12'), 'twelve': AT('12', 'twelve', 'పన్నెండు'), 'about12': AT('12', '12,000', '12,000'), 'minimum': AT('12', 'minimum', 'కనీసం'),
    'surplus': AT('12', 'surplus', 'surplus'), 'p20': AT('12', '20', '20'), 'r288': AT('12', '28,800', '28,800'),
    'changed': S('13'), 'four': AT('13', 'Four', 'నాలుగు'),
    'one': S('14'), 'bank': AT('14', 'bank', 'bank'), 'cash': AT('14', 'cash', 'cash'),
    'two': S('15'), 'w12': AT('15', '12', '12'), 'w20': AT('15', '20', '20'), 'suresh': AT('15', 'Suresh', 'సురేష్'), 'lose': AT('15', 'lose', 'కోల్పోవచ్చు'),
    'three': S('16'), 'notif': AT('16', 'notification', 'notification'), 'aug': AT('16', 'August', 'August'),
    'fourth': S('17'), 'fraud': AT('17', 'fraud', 'fraud'), 'now17': AT('17', 'Now', 'ఇప్పుడు'), 'harass': AT('17', 'harassment', 'harassment'),
    'eight': AT('18', 'eight', 'ఎనిమిది'), 'nov30': AT('18', 'November', 'November'), 'didnt': AT('18', "Didn't", 'రాలేదా'), 'claim': AT('18', 'claim', 'claim'),
    'tomorrow': S('19'), 'space': AT('19', 'space', 'space'), 'notwhat': AT('19', 'not', 'అనుకునేది'),
    'loop': S('L'),
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
    txt = 'DIWALI · 1/6' if LANGV == 'en' else 'దీపావళి · 1/6'
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
        (sx, sy), (ex, ey) = SL[LANGV][2][1], SL[LANGV][3][1]; sy += 200; ey += 200
        x = sx + (ex - sx) * e_io(k); y = sy + (ey - sy) * e_io(k) - math.sin(k * math.pi) * 120
        glowdot(c, x, y, 13 if k < 1 else 10 + 2 * math.sin(t * 6))
    c.pop_group_to_source(); c.paint_with_alpha(a); c.restore()

# ---------------- scenes ----------------
def sc_hook(c, t, frozen=False):
    """line 1. frozen=True draws the loop-target state (identical to frame 0)."""
    tt = 0.0 if frozen else t
    head(c, 'YOUR DIWALI BONUS:', W / 2, 300, 64, CREAM)
    head(c, 'GIFT… OR LAW?', W / 2, 400, 92, AMBER)
    gl = 0.0 if frozen else prog(t, A['gift'] - 0.2, A['gift'] + 0.1) * (1 - prog(t, A['law1'] - 0.2, A['law1']))
    ll = 0.0 if frozen else prog(t, A['law1'] - 0.1, A['law1'] + 0.2)
    sub_g = 'COMPANY CHOICE' if (not frozen and t >= A['company1'] - 0.1) else None
    gi = 0.0 if frozen else prog(t, A['company1'] - 0.1, A['company1'] + 0.2)
    fo = 1.0 if frozen else 1 - 0.85 * e_io(prog(t, A['n21'] - 0.05, A['n21'] + 0.25))
    c.push_group()
    option_card(c, 90, 'GIFT?', gift_icon, tt, max(gl, gi * 0.6), sub=sub_g)
    option_card(c, 560, 'LAW?', lambda c_, x, y, s, a=1.0, glow=0.0: gavel_icon(c_, x, y, s, a, glow, hit=prog(t, A['law1'], A['law1'] + 0.15) if not frozen else 0), tt, ll, sub='FOR MILLIONS' if ll > 0.5 else None)
    c.pop_group_to_source(); c.paint_with_alpha(fo)
    bk = 1.0 if frozen else 1 - prog(t, A['n21'] - 0.15, A['n21'] + 0.05)
    if bk > 0:   # the number is on screen from frame 0
        c.save(); c.translate(W / 2, 795)
        c.set_source_rgba(0, 0, 0, 0.6 * bk); c.arc(0, 8, 112, 0, 2 * math.pi); c.fill()
        g_ = agrad(-110, 0, 110, 0); c.set_source(g_); c.arc(0, 0, 108, 0, 2 * math.pi); c.fill()
        c.set_source_rgba(0, 0, 0, 0.85 * bk); c.set_line_width(6); c.arc(0, 0, 108, 0, 2 * math.pi); c.stroke()
        font(c, 'head', 44); e = c.text_extents('₹21,000'); c.move_to(-e.width / 2 - e.x_bearing, 16); c.set_source_rgba(*INK, bk); c.show_text('₹21,000')
        c.restore()
        mono(c, 'DECIDES WHICH ONE', W / 2, 1095, 30, AMBER, a=bk, kind='monob')
    if not frozen and t >= A['n21'] - 0.05:
        k = e_io(prog(t, A['n21'] - 0.05, A['n21'] + 0.25))
        big_num(c, '₹21,000', W / 2, 800, 200, t, A['n21'] - 0.05)
        mono(c, 'A MONTH · DECIDES WHICH ONE', W / 2, 960, 30, CREAM, a=prog(t, A['n21'] + 0.3, A['n21'] + 0.6), kind='monob')

def frame(t):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s)
    board_bg(c, t)
    caps = True
    zoom_on = (S('8') - 0.05 <= t < S('11') - 0.05) or (S('12') - 0.05 <= t < S('19') - 0.05)
    if zoom_on: c.save(); c.translate(540, 760); c.scale(1.1, 1.1); c.translate(-540, -760)
    if t < S('2') - 0.05:
        sc_hook(c, t)
    # 2 correction
    elif t < S('3') - 0.05:
        t2 = A['since'] - 0.2
        if t < t2 + 0.25:
            card_img(c, img(THUMB, 820), W / 2, 560, t, S('2') - 0.05, rot=-2, a=1 - prog(t, t2, t2 + 0.25))
            mono(c, 'OUR FULL VIDEO · SUNDAY', W / 2, 300, 26, CREAM, a=prog(t, S('2'), S('2') + 0.3) * (1 - prog(t, t2, t2 + 0.25)), kind='monob')
            stamp_txt(c, 'CORRECTION', W / 2, 560, t, A['corr'], px=92, rot=-8, col=AMBER, a=1 - prog(t, t2, t2 + 0.25))
            if t >= A['y1965'] - 0.1:
                k = prog(t, A['y1965'] - 0.1, A['y1965'] + 0.2) * (1 - prog(t, t2, t2 + 0.25))
                pill(c, 'PAYMENT OF BONUS ACT, 1965', W / 2, 900, 36, CREAM, s=max(0.01, e_back(prog(t, A['y1965'] - 0.1, A['y1965'] + 0.2))), a=k)
                if t >= A['sorry']:
                    font(c, 'head', 36); e = c.text_extents('PAYMENT OF BONUS ACT, 1965'); f = e_out(prog(t, A['sorry'], A['sorry'] + 0.3))
                    c.set_source_rgba(*AMBER, k); c.set_line_width(7); c.move_to(W / 2 - e.width / 2 - 20, 900); c.line_to(W / 2 - e.width / 2 - 20 + (e.width + 40) * f, 900); c.stroke()
                    mono(c, 'OUT OF DATE', W / 2, 990, 28, AMBER, a=k * f, kind='monob')
        else:
            draw_clip(c, 'c1_taxmann_bonus_repealed_z', W / 2, 540, 1010, t, t2, rot=-1.0, hl_t0=t2 + 0.35, hl_dur=1.1)
            source_tag(c, 'TAXMANN · SEP 2026 (ARTICLE TEXT)', 90, 380, a=prog(t, t2 + 0.2, t2 + 0.5))
            if t >= A['code2'] - 0.1:
                big_num(c, 'CODE ON WAGES', W / 2, 860, 96, t, A['code2'] - 0.1)
                mono(c, 'IN FORCE SINCE 21 NOV 2025', W / 2, 960, 28, CREAM, a=prog(t, A['code2'] + 0.2, A['code2'] + 0.5), kind='monob')
    # 3 four laws merged; never says Diwali
    elif t < S('4') - 0.05:
        LAWS = [('WAGES ACT', '1936'), ('MINIMUM WAGES', '1948'), ('BONUS ACT', '1965'), ('EQUAL PAY', '1976')]
        m = e_io(prog(t, A['merge'] - 0.5, A['merge'] + 0.1))
        if t < A['never'] - 0.1:
            for i, (n_, y_) in enumerate(LAWS):
                t0 = S('3') + 0.15 * i
                if t < t0: continue
                u = e_out(prog(t, t0, t0 + 0.3)); bx = 90 + (i % 2) * 460; by = 330 + (i // 2) * 230
                tx, ty = W / 2 - 220, 700
                x = bx + (tx - bx) * m; y = by + (ty - by) * m
                glass_dark(c, x, y + (1 - u) * 40, 440, 200, 28, u * (1 - m))
                head(c, n_, x + 220, y + 80, 40, CREAM, a=u * (1 - m), shadow=False)
                mono(c, y_, x + 220, y + 140, 30, AMBER if y_ == '1965' else CREAM, a=u * (1 - m), kind='monob')
            if m > 0:
                u = e_back(prog(t, A['merge'] - 0.1, A['merge'] + 0.25))
                c.save(); c.translate(W / 2, 800); c.scale(max(0.01, u), max(0.01, u))
                glass_dark(c, -400, -130, 800, 260, 36); c.set_source_rgba(*AMBER, 1); c.set_line_width(5); rrect(c, -400, -130, 800, 260, 36); c.stroke()
                head(c, 'CODE ON WAGES, 2019', 0, -30, 58, AMBER, shadow=False); mono(c, '4 OLD LAWS → 1', 0, 50, 30, CREAM, kind='monob')
                c.restore()
            draw_clip(c, 'c2_taxmann_govt_four_acts_z', W / 2, 1150, 860, t, S('3') + 0.4, rot=1.2, hl_t0=S('3') + 0.8, hl_dur=0.8, t1=A['merge'] - 0.3)
        else:
            u = e_out(prog(t, A['never'] - 0.1, A['never'] + 0.2))
            mono(c, 'THE LAW NEVER SAYS', W / 2, 360, 30, CREAM, a=u, kind='monob')
            big_num(c, '"DIWALI"', W / 2, 520, 150, t, A['never'] - 0.1, a=0.99 if t < A['annual'] else 0.6, strike=prog(t, A['never'] + 0.4, A['never'] + 0.8))
            if t >= A['annual'] - 0.1:
                pill(c, 'IT\'S AN ANNUAL BONUS', W / 2, 760, 46, AMBER, s=e_back(prog(t, A['annual'] - 0.1, A['annual'] + 0.2)))
            if t >= A['many'] - 0.1:
                mono(c, 'MANY COMPANIES JUST PAY IT AROUND DIWALI', W / 2, 900, 26, CREAM, a=prog(t, A['many'] - 0.1, A['many'] + 0.2), kind='monob')
                for i in range(7):
                    x = 200 + i * 113; fl = 0.6 + 0.4 * math.sin(t * 9 + i)
                    c.set_source_rgba(1.0, 0.75, 0.3, 0.9 * fl * prog(t, A['many'] + 0.05 * i, A['many'] + 0.05 * i + 0.3)); c.arc(x, 1050, 9 + 3 * fl, 0, 2 * math.pi); c.fill()
                    c.set_source_rgba(0.75, 0.45, 0.2, prog(t, A['many'] + 0.05 * i, A['many'] + 0.05 * i + 0.3)); c.arc(x, 1080, 26, 0, math.pi); c.fill()
    # 4 Ravi
    elif t < S('5') - 0.05:
        head(c, 'THE ₹21,000 TEST', W / 2, 270, 70, AMBER, a=prog(t, A['test'] - 0.2, A['test'] + 0.1))
        if t >= A['ravi'] - 0.15:
            u = e_back(prog(t, A['ravi'] - 0.15, A['ravi'] + 0.2))
            person(c, 300, 1110, 1.25 * min(1, u), (0.24, 0.42, 0.62), prop='box' if t >= A['boxes'] - 0.1 else None, t=t)
            name_card(c, 530, 470, 'RAVI', 'WAREHOUSE PACKER · 50 WORKERS', '₹18,000 / MONTH' if t >= A['r18'] - 0.1 else None, t, A['ravi'] + 0.1)
        if t >= A['counts'] - 0.1:
            k = prog(t, A['counts'] - 0.1, A['counts'] + 0.2)
            glass_dark(c, 530, 700, 470, 150, 24, k)
            mono(c, 'WAGES, AS THE LAW COUNTS THEM:', 765, 735, 18, AMBER, a=k, kind='monob')
            mono(c, 'BASIC + DA', 765, 780, 30, CREAM, a=k, kind='monob')
            mono(c, '(+ RETAINING ALLOWANCE)', 765, 820, 18, CREAM, a=0.75 * k, kind='mono')
    # 5 / 6 / 7: the ₹21,000 line
    elif t < S('8') - 0.05:
        LY = 640
        c.set_source_rgba(*AMBER, 0.9); c.set_line_width(5); c.set_dash([18, 12]); c.move_to(60, LY); c.line_to(W - 60, LY); c.stroke(); c.set_dash([])
        pill(c, '₹21,000 / MONTH', 250, LY, 30, AMBER)
        in6 = t >= S('6') - 0.05; in7 = False
        # Ravi below the line
        rx = 260 if not in6 else 260
        rdim = 0.3 if (in6 and not in7 and A['cover'] - 0.1 <= t < A['contract'] - 0.2) else 1.0
        person(c, rx, 1190, 0.95, (0.24, 0.42, 0.62), prop='box', t=t, a=rdim)
        if not in6:
            name_card(c, 520, 760, 'RAVI · ₹18,000', 'BELOW THE LINE', None, t, S('5'), w=480)
            if t >= A['less'] - 0.3:
                tick(c, 940, 815, 0.8, prog(t, A['less'] - 0.3, A['less']), AMBER)
            if t >= A['d30'] - 0.1: pill(c, '30+ DAYS WORKED THIS YEAR', W / 2, 330, 34, CREAM, s=e_back(prog(t, A['d30'] - 0.1, A['d30'] + 0.2)))
            if t >= A['must'] - 0.1: stamp_txt(c, 'LAW: MUST PAY', 720, 1010, t, A['must'] - 0.1, px=60, rot=-6, col=AMBER)
            score(c, 1140, 'Y', 'Y', t, A['old5'] - 0.1)
            if t >= A['old5'] - 0.1: mono(c, 'SAME ANSWER', W / 2, 1110, 24, AMBER, a=prog(t, A['old5'] + 0.4, A['old5'] + 0.7), kind='monob')
        else:
            mono(c, 'RAVI · ₹18,000', 260, 1235, 24, CREAM, a=rdim if rdim == 1.0 else 0.0, kind='monob')
            if not in7:
                u = e_out(prog(t, A['arjun'] - 0.15, A['arjun'] + 0.5))
                person(c, 780, 1190 - 600 * u, 0.95, (0.30, 0.30, 0.34), prop='laptop', t=t, a=prog(t, A['arjun'] - 0.15, A['arjun'] + 0.1))
                if t >= A['a45'] - 0.1: name_card(c, 560, 230, 'ARJUN · ₹45,000', 'SOFTWARE ENGINEER · ABOVE THE LINE', None, t, A['a45'] - 0.1, w=470)
                if t >= A['cover'] - 0.1 and t < A['contract'] - 0.2:
                    score(c, 1290 - 140, 'N', 'N', t, A['cover'] - 0.1)
                    mono(c, 'THE BONUS RULE DOESN\'T COVER HIM', W / 2, 1120, 22, CREAM, a=prog(t, A['cover'], A['cover'] + 0.3), kind='monob')
                if t >= A['contract'] - 0.2:
                    u2 = e_out(prog(t, A['contract'] - 0.2, A['contract'] + 0.15))
                    glass_dark(c, 480, 720, 540, 210, 30, u2); c.set_source_rgba(*AMBER, u2); c.rectangle(500, 740, 6, 170); c.fill()
                    mono(c, 'HIS BONUS COMES FROM', 760, 770, 22, CREAM, a=u2, kind='monob')
                    head(c, 'CONTRACT /', 760, 830, 48, AMBER, a=u2, shadow=False); head(c, 'COMPANY POLICY', 760, 890, 48, AMBER, a=u2, shadow=False)
                    mono(c, 'NOT FROM THIS LAW', 760, 960, 22, CREAM, a=u2 * prog(t, A['contract'] + 0.6, A['contract'] + 0.9), kind='monob')
                    mono(c, 'ELIGIBILITY ₹21,000 OR LESS · S.O. 4711(E), 25 AUG 2026', W / 2, 1300, 16, CREAM, a=0.75 * u2, kind='mono')
            else:
                person(c, 780, 590, 0.95, (0.30, 0.30, 0.34), prop='laptop', t=t)
                mono(c, 'ARJUN · ₹45,000', 780, 175, 24, CREAM, kind='monob')
                u = e_back(prog(t, A['protect'] - 0.2, A['protect'] + 0.2))
                if t >= A['protect'] - 0.2:   # shield over Ravi
                    c.save(); c.translate(260, 820); c.scale(max(0.01, u) * 1.4, max(0.01, u) * 1.4)
                    c.move_to(0, -90); c.curve_to(60, -70, 80, -60, 80, -60); c.line_to(80, 10); c.curve_to(70, 70, 0, 100, 0, 100); c.curve_to(0, 100, -70, 70, -80, 10)
                    c.line_to(-80, -60); c.curve_to(-80, -60, -60, -70, 0, -90); c.close_path()
                    c.set_source_rgba(*AMBER, 0.85); c.fill_preserve(); c.set_source_rgba(0, 0, 0, 0.6); c.set_line_width(4); c.stroke()
                    tick(c, 0, 0, 1.0, prog(t, A['protect'], A['protect'] + 0.4), INK); c.restore()
                    pill(c, 'BUILT FOR LOWER-PAID WORKERS', W / 2, 1060, 34, AMBER, s=u)
                if t < A['protect']: head(c, 'SURPRISED?', W / 2, 330, 80, CREAM, a=prog(t, S('7'), S('7') + 0.2))
    # 8 how much
    elif t < S('9') - 0.05:
        head(c, 'HOW MUCH DOES RAVI GET?', W / 2, 300, 54, CREAM, a=prog(t, S('8'), S('8') + 0.2))
        big_num(c, '₹18,000', W / 2, 640, 170, t, S('8') + 0.1, strike=0.0)
        if t >= A['catch'] - 0.2:
            u = e_back(prog(t, A['catch'] - 0.2, A['catch'] + 0.2))
            c.save(); c.translate(950, 450); c.scale(max(0.01, u) * 0.8, max(0.01, u) * 0.8); c.rotate(0.15 * math.sin(t * 3))
            font(c, 'head', 220); c.move_to(-60, 80); c.text_path('?'); c.set_source_rgba(0, 0, 0, 0.8); c.set_line_width(14); c.stroke_preserve(); c.set_source(agrad(-60, 0, 60, 0)); c.fill(); c.restore()
        if t >= A['notfull'] - 0.2: pill(c, 'NOT COUNTED ON THE FULL SALARY', W / 2, 900, 36, CREAM, s=e_back(prog(t, A['notfull'] - 0.2, A['notfull'] + 0.1)))
    # 9 / 10 minimum wage
    elif t < S('11') - 0.05:
        if t < S('10') - 0.05:
            pill(c, 'MINIMUM WAGE', W / 2, 260, 44, AMBER, s=e_back(prog(t, S('9'), S('9') + 0.3)))
            mono(c, 'THE LOWEST PAY THE LAW ALLOWS FOR A JOB', W / 2, 350, 24, CREAM, a=prog(t, S('9') + 0.4, S('9') + 0.7), kind='monob')
            if t >= A['skilled'] - 0.25:   # one job card, skill sets the level
                u = e_out(prog(t, A['skilled'] - 0.25, A['skilled'] + 0.1))
                c.save(); c.translate(0, (1 - u) * 40); glass_dark(c, 140, 420, 800, 230, 30, u)
                c.set_source_rgba(*AMBER, u); c.rectangle(160, 440, 6, 190); c.fill()
                mono(c, 'EXAMPLE JOB', W / 2, 465, 22, CREAM, a=0.8 * u, kind='monob')
                head(c, 'WAREHOUSE PACKER', W / 2, 535, 56, CREAM, a=u, shadow=False)
                mono(c, 'MORE SKILL = HIGHER MINIMUM', W / 2, 605, 24, AMBER, a=u * prog(t, A['skilled'] + 0.2, A['skilled'] + 0.5), kind='monob'); c.restore()
            if t >= A['where'] - 0.2:   # same job, two places
                u = e_out(prog(t, A['where'] - 0.2, A['where'] + 0.15))
                glass_dark(c, 140, 690, 800, 480, 30, u)
                mono(c, 'SAME JOB · DIFFERENT PLACE', W / 2, 735, 24, CREAM, a=u, kind='monob')
                for j, (lab, hh) in enumerate((('CITY', 230), ('VILLAGE', 140))):
                    x = 340 + j * 400; k = e_out(prog(t, A['city'] - 0.1 + 0.4 * j, A['city'] + 0.3 + 0.4 * j))
                    c.set_source_rgba(*AMBER, u); c.arc(x, 820, 26, 0, 2 * math.pi); c.fill(); c.move_to(x - 19, 834); c.line_to(x, 868); c.line_to(x + 19, 834); c.fill()
                    c.set_source_rgba(*INK, u); c.arc(x, 820, 9, 0, 2 * math.pi); c.fill()
                    head(c, lab, x, 905, 44, CREAM, a=u, shadow=False)
                    rrect(c, x - 60, 1120 - hh * k, 120, hh * k, 12); c.set_source_rgba(*(AMBER if j == 0 else CREAM), 0.9 * u); c.fill()
                mono(c, 'CAN DIFFER', W / 2, 1140, 26, AMBER, a=prog(t, A['city'] + 0.7, A['city'] + 1.0), kind='monob')
        else:
            pill(c, 'WHO GETS A MINIMUM WAGE?', W / 2, 260, 40, AMBER)
            for j, (lab, n_on) in enumerate((('OLD: LISTED JOBS ONLY', 4), ('NOW: EVERY JOB', 16))):
                t0 = S('10') if j == 0 else A['every'] - 0.2
                if t < t0: continue
                u = e_out(prog(t, t0, t0 + 0.3)); y0 = 400 + j * 430
                glass_dark(c, 90, y0, 900, 380, 30, u)
                mono(c, lab, W / 2, y0 + 50, 28, AMBER if j else CREAM, a=u, kind='monob')
                for i in range(16):
                    x = 175 + (i % 8) * 104; y = y0 + 150 + (i // 8) * 120
                    on = i < n_on and (j == 0 and i in (1, 5, 10, 14) or j == 1)
                    k = prog(t, t0 + 0.2 + 0.03 * i, t0 + 0.4 + 0.03 * i)
                    c.set_source_rgba(*(AMBER if on else (0.4, 0.4, 0.45)), (0.95 if on else 0.6) * k * u); c.arc(x, y - 20, 18, 0, 2 * math.pi); c.fill()
                    rrect(c, x - 28, y + 4, 56, 44, 18); c.fill()
    # 11 counted on 12,000
    elif t < S('12') - 0.05:
        mono(c, "RAVI'S JOB · MINIMUM WAGE (EXAMPLE)", W / 2, 270, 24, CREAM, a=prog(t, S('11'), S('11') + 0.3), kind='monob')
        big_num(c, '₹18,000', W / 2, 430, 110, t, S('11') + 0.05, a=0.6, strike=prog(t, A['not18'] - 0.3, A['not18']) if t >= A['that12'] else 0.0)
        if t >= A['m12'] - 0.15:
            big_num(c, '₹12,000', W / 2, 640, 180, t, A['m12'] - 0.15)
            tick(c, 985, 640, 0.9, prog(t, A['that12'] - 0.2, A['that12'] + 0.2), AMBER)
        if t >= A['that12'] - 0.1:
            mono(c, 'BONUS IS COUNTED ON THIS', W / 2, 770, 26, AMBER, a=prog(t, A['that12'] - 0.1, A['that12'] + 0.2), kind='monob')
        draw_clip(c, 'c3_scc_7000_minwage_z', W / 2, 1010, 1010, t, A['that12'] + 0.2, rot=-0.8, hl_t0=A['that12'] + 0.5, hl_dur=1.1)
        if t >= A['that12'] + 0.4:
            source_tag(c, 'SCC ONLINE · AUG 26, 2026 (ARTICLE TEXT)', 90, 1150, a=prog(t, A['that12'] + 0.4, A['that12'] + 0.7))
            mono(c, 'BASE = YOUR WAGE, CAPPED AT ₹7,000 OR THE MINIMUM WAGE (WHICHEVER IS HIGHER)', W / 2, 1240, 15, CREAM, a=0.8 * prog(t, A['that12'] + 0.6, A['that12'] + 0.9), kind='mono')
    # 12 staged calculation
    elif t < S('13') - 0.05:
        steps = [('₹12,000', S('12') - 0.05), ('× 12 MONTHS', A['twelve'] - 0.1), ('× 8.33%', S('12') + 0.05)]
        steps = sorted(steps, key=lambda s_: s_[1])
        y = 300
        for txt_, t0 in (('₹12,000', S('12') - 0.05), ('× 8.33%', S('12') + 0.25), ('× 12 MONTHS', A['twelve'] - 0.1)):
            if t >= t0:
                u = e_out(prog(t, t0, t0 + 0.25)); glass_dark(c, 240, y - 50, 600, 100, 28, u)
                head(c, txt_, W / 2, y, 50, CREAM, a=u, shadow=False)
            y += 120
        if t >= A['about12'] - 0.15:
            c.set_source_rgba(*AMBER, 0.9); c.set_line_width(4); c.move_to(240, 660); c.line_to(840, 660); c.stroke()
            big_num(c, '≈ ₹12,000', W / 2, 740, 100, t, A['about12'] - 0.15)
        if t >= A['minimum'] - 0.15: pill(c, 'MINIMUM · 8.33%', W / 2, 850, 32, CREAM, s=e_back(prog(t, A['minimum'] - 0.15, A['minimum'] + 0.15)))
        if t >= A['surplus'] - 0.3:   # bar to the max
            u = e_out(prog(t, A['surplus'] - 0.3, A['surplus']))
            glass_dark(c, 90, 940, 900, 300, 30, u)
            x0, w0 = 130, 820; k = e_io(prog(t, A['p20'] - 0.3, A['r288'] + 0.2))
            rrect(c, x0, 1060, w0 * (12000 / 28800), 70, 35); c.set_source_rgba(*CREAM, 0.85 * u); c.fill()
            if k > 0: rrect(c, x0, 1060, max(70, w0 * ((12000 + 16800 * k) / 28800)), 70, 35); c.set_source(agrad(x0, 0, x0 + w0, 0)); c.fill()
            mono(c, 'MIN 8.33%', x0 + 10, 1010, 22, CREAM, a=u, anchor='l', kind='monob')
            mono(c, 'MAX 20%', x0 + w0 - 10, 1010, 22, AMBER, a=u, anchor='r', kind='monob')
            if t >= A['r288'] - 0.2: head(c, '₹28,800 MAX', W / 2, 1180, 56, AMBER, a=prog(t, A['r288'] - 0.2, A['r288'] + 0.1), shadow=False)
            mono(c, 'MAX NEEDS ENOUGH ALLOCABLE SURPLUS · EXCEPTIONS, E.G. NEW ESTABLISHMENTS', W / 2, 1290, 14, CREAM, a=0.75 * u, kind='mono')
    # 13–17 what changed
    elif t < S('18') - 0.05:
        n_act = 0 if t < S('14') - 0.05 else 1 if t < S('15') - 0.05 else 2 if t < S('16') - 0.05 else 3 if t < S('17') - 0.05 else 4
        c.restore(); chips(c, n_act, t, S('13')); c.save(); c.translate(540, 760); c.scale(1.1, 1.1); c.translate(-540, -760)
        if n_act == 0:
            head(c, 'WHAT CHANGED', W / 2, 520, 92, CREAM, a=prog(t, S('13'), S('13') + 0.2))
            head(c, 'IN THE NEW LAW?', W / 2, 630, 72, AMBER, a=prog(t, S('13') + 0.2, S('13') + 0.4))
            if t >= A['four'] - 0.1: big_num(c, '4 THINGS', W / 2, 820, 110, t, A['four'] - 0.1)
        elif n_act == 1:
            head(c, 'PAID INTO YOUR BANK', W / 2, 360, 60, CREAM, a=prog(t, S('14'), S('14') + 0.2))
            u = e_out(prog(t, A['bank'] - 0.2, A['bank'] + 0.2))
            c.save(); c.translate(W / 2, 700); glass_dark(c, -170, -230, 340, 460, 46, u)
            rrect(c, -150, -200, 300, 400, 30); c.set_source_rgba(0.12, 0.12, 0.14, u); c.fill()
            if u > 0.5:
                k = prog(t, A['bank'] + 0.2, A['bank'] + 0.5)
                glass_dark(c, -130, -80 + 40 * (1 - k), 260, 150, 20, k)
                tick(c, -80, -5 + 40 * (1 - k), 0.6, k, AMBER); mono(c, 'CREDITED', 40, -30 + 40 * (1 - k), 22, AMBER, a=k, kind='monob')
                mono(c, 'BONUS', 40, 20 + 40 * (1 - k), 22, CREAM, a=k, kind='monob')
            c.restore()
            score(c, 1030, 'CASH', 'BANK', t, A['cash'] - 0.3, t_new=A['cash'] + 0.2)
        elif n_act == 2:
            head(c, 'SMALL FACTORIES', W / 2, 360, 66, CREAM, a=prog(t, S('15'), S('15') + 0.2))
            u = e_out(prog(t, S('15') + 0.2, S('15') + 0.5))
            # factory
            c.save(); c.translate(300, 700); c.set_source_rgba(0.35, 0.35, 0.4, u)
            c.move_to(-170, 0); c.line_to(-170, -150); c.line_to(-100, -110); c.line_to(-100, -150); c.line_to(-30, -110); c.line_to(-30, -150); c.line_to(40, -110); c.line_to(40, -260); c.line_to(90, -260); c.line_to(90, 0); c.close_path(); c.fill()
            for i in range(3):
                c.set_source_rgba(*AMBER, 0.8 * u); c.rectangle(-150 + i * 70, -70, 40, 30); c.fill()
            sm = prog(t, S('15'), S('15') + 3)
            c.set_source_rgba(0.7, 0.7, 0.75, 0.35 * u); c.arc(65 + 70 * sm, -250 - 10 * sm, 20 + 10 * sm, 0, 2 * math.pi); c.fill(); c.restore()
            if t >= A['suresh'] - 0.2:
                person(c, 300, 1005, 0.55, (0.55, 0.40, 0.25), prop='helmet', t=t, a=prog(t, A['suresh'] - 0.2, A['suresh'] + 0.1))
                mono(c, 'SURESH', 300, 1040, 24, CREAM, a=prog(t, A['suresh'] - 0.2, A['suresh'] + 0.1), kind='monob')
            if t >= A['w12'] - 0.2:   # worker counter vs 20+
                k = prog(t, A['w12'] - 0.2, A['w12'] + 0.3)
                glass_dark(c, 560, 480, 420, 360, 30, k)
                head(c, '12', 770, 600, 110, AMBER, a=k, shadow=False); mono(c, 'WORKERS', 770, 690, 26, CREAM, a=k, kind='monob')
                if t >= A['w20'] - 0.2:
                    k2 = prog(t, A['w20'] - 0.2, A['w20'] + 0.2)
                    c.set_source_rgba(*CREAM, k2); c.set_line_width(4); c.set_dash([10, 8]); c.move_to(590, 750); c.line_to(950, 750); c.stroke(); c.set_dash([])
                    mono(c, 'RULE STARTS AT 20+', 770, 795, 24, CREAM, a=k2, kind='monob')
            score(c, 1085, 'COULD BE', 'N', t, A['w20'] + 0.1, t_new=A['lose'] - 0.1, h=170)
        elif n_act == 3:
            head(c, 'WHO SETS ₹21,000?', W / 2, 360, 64, CREAM, a=prog(t, S('16'), S('16') + 0.2))
            if t < A['notif'] - 0.2:
                u = e_out(prog(t, S('16') + 0.2, S('16') + 0.5))
                glass_dark(c, 140, 520, 800, 220, 30, u); mono(c, 'OLD LAW', W / 2, 570, 26, CREAM, a=u, kind='monob')
                head(c, '₹21,000 · IN THE ACT', W / 2, 650, 54, CREAM, a=u, shadow=False)
            else:
                draw_clip(c, 'c3_scc_head', W / 2, 600, 860, t, A['notif'] - 0.2, rot=-1.2)
                draw_clip(c, 'c3_scc_21000_z', W / 2, 900, 1010, t, A['aug'] - 0.3, rot=0.8, hl_t0=A['aug'], hl_dur=1.0)
                draw_clip(c, 'c3_scc_retro_z', W / 2, 1060, 1010, t, A['aug'] + 1.2, rot=-0.6, hl_t0=A['aug'] + 1.5, hl_dur=0.8)
                source_tag(c, 'SCC ONLINE · AUG 26, 2026 (ARTICLE TEXT)', 90, 1170, a=prog(t, A['notif'], A['notif'] + 0.3))
                mono(c, 'CENTRAL NOTIFICATION · STATES NOTIFY FOR THEIR OWN ESTABLISHMENTS', W / 2, 1250, 15, CREAM, a=0.75 * prog(t, A['aug'] + 1.5, A['aug'] + 1.8), kind='mono')
        else:
            head(c, 'YOU LOSE THE BONUS IF', W / 2, 360, 52, CREAM, a=prog(t, S('17'), S('17') + 0.2))
            mono(c, 'DISMISSED FOR…', W / 2, 440, 26, CREAM, a=prog(t, S('17') + 0.2, S('17') + 0.4), kind='monob')
            for i, lab in enumerate(('FRAUD', 'VIOLENCE', 'THEFT')):
                t0 = A['fraud'] - 0.1 + 0.3 * i
                if t >= t0:
                    u = e_out(prog(t, t0, t0 + 0.25)); glass_dark(c, 190, 500 + i * 130, 700, 105, 26, u * (0.6 if t >= A['now17'] else 1))
                    head(c, lab, W / 2, 552 + i * 130, 46, CREAM, a=u * (0.6 if t >= A['now17'] else 1), shadow=False)
            if t >= A['now17'] - 0.1:
                u = e_back(prog(t, A['now17'] - 0.1, A['now17'] + 0.25))
                c.save(); c.translate(W / 2, 980); c.scale(max(0.01, u), max(0.01, u))
                rrect(c, -420, -80, 840, 160, 30); c.set_source(agrad(-420, 0, 420, 0)); c.fill()
                mono(c, 'NEW', -360, -40, 22, INK, anchor='l', kind='monob')
                head(c, 'SEXUAL-HARASSMENT', 0, -10, 44, INK, shadow=False); head(c, 'CONVICTION', 0, 45, 44, INK, shadow=False)
                c.restore()
    # 18 deadline + claim
    elif t < S('19') - 0.05:
        head(c, 'WHEN MUST THEY PAY?', W / 2, 300, 60, CREAM, a=prog(t, S('18'), S('18') + 0.2))
        months = ['APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV']
        u = e_out(prog(t, S('18') + 0.1, S('18') + 0.4))
        glass_dark(c, 90, 400, 900, 470, 30, u)
        mono(c, 'YEAR ENDS 31 MAR → 8 MONTHS', W / 2, 450, 24, CREAM, a=u, kind='monob')
        for i, mth in enumerate(months):
            x = 165 + (i % 4) * 250; y = 560 + (i // 4) * 150
            k = prog(t, A['eight'] - 0.2 + 0.1 * i, A['eight'] + 0.1 * i)
            glass_dark(c, x - 95, y - 50, 190, 100, 20, u)
            if k > 0: rrect(c, x - 95, y - 50, 190 * k, 100, 20); c.set_source_rgba(*AMBER, 0.25); c.fill()
            head(c, mth, x, y, 44, AMBER if i == 7 else CREAM, a=u, shadow=False)
        if t >= A['nov30'] - 0.2:
            k3 = e_out(prog(t, A['nov30'] - 0.2, A['nov30'] + 0.25)); c.save(); c.translate(915, 710); c.scale(1.0, 0.62)
            c.set_source_rgba(*AMBER, 1); c.set_line_width(7); c.arc(0, 0, 135, -math.pi / 2, -math.pi / 2 + 2 * math.pi * k3); c.restore(); c.stroke()
            big_num(c, 'NOV 30', W / 2, 960, 100, t, A['nov30'])
        if t >= A['didnt'] - 0.1:
            u2 = e_out(prog(t, A['didnt'] - 0.1, A['didnt'] + 0.2))
            glass_dark(c, 90, 1060, 900, 230, 30, u2); c.set_source_rgba(*AMBER, u2); c.rectangle(110, 1080, 6, 190); c.fill()
            mono(c, "DIDN'T GET IT?", W / 2, 1110, 26, CREAM, a=u2, kind='monob')
            head(c, 'FILE A CLAIM', W / 2, 1175, 58, AMBER, a=u2 * prog(t, A['claim'] - 0.3, A['claim']), shadow=False)
            mono(c, 'LABOUR AUTHORITY · CLAIM PERIOD GENERALLY 3 YEARS (SEC. 45(6))', W / 2, 1245, 16, CREAM, a=0.8 * u2 * prog(t, A['claim'], A['claim'] + 0.3), kind='mono')
    # 19 tomorrow + series slide + CTA
    elif t < S('L') - 0.05:
        caps = t < END_T0 - 0.3
        sc_ = 1.0 - 0.14 * e_io(prog(t, END_T0 - 0.5, END_T0))
        slide(c, t, S('19') - 0.05, scale=sc_)
        CTA.draw(c, t, END_T0, PLAT, LANGV, y=1745)
    # loop: fade back to the opening frame
    else:
        caps = True
        k = e_io(prog(t, S('L') - 0.05, S('L') + 0.7))
        c.push_group(); slide(c, t, S('19') - 0.05, scale=0.86); CTA.draw(c, t, END_T0, PLAT, LANGV, y=1745); c.pop_group_to_source(); c.paint_with_alpha(1 - k)
        c.push_group(); board_bg(c, 0.0); sc_hook(c, 0.0, frozen=True); tag(c); c.pop_group_to_source(); c.paint_with_alpha(k)
    if zoom_on: c.restore()
    if caps: (K.captions(c, t, y=1440) if LANGV == 'en' else R3.te_captions(c, t, y=1440))
    if t < S('19') - 0.05: tag(c)
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
