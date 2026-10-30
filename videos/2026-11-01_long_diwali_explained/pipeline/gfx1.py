"""Explainer graphics: cold open, chapters 1-3."""
from base import *
import room as RM

MONTHS = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
MONTHS_TE = ['జన', 'ఫిబ్ర', 'మార్చి', 'ఏప్రి', 'మే', 'జూన్', 'జూలై', 'ఆగ', 'సెప్టె', 'అక్టో', 'నవం', 'డిసె']


def cal_page(c, cx, cy, w, top, big, sub=None, t=0, t0=0, rot=0, a=1.0, hl=False):
    u = e_back(prog(t, t0, t0 + 0.35))
    if u <= 0.01: return
    h = w * 1.1
    c.save(); c.translate(cx, cy); c.rotate(math.radians(rot)); c.scale(u, u)
    c.set_source_rgba(0, 0, 0, 0.4 * a); rrect(c, -w / 2 + 8, -h / 2 + 14, w, h, 22); c.fill()
    c.set_source_rgba(0.97, 0.95, 0.90, a); rrect(c, -w / 2, -h / 2, w, h, 22); c.fill()
    c.save(); rrect(c, -w / 2, -h / 2, w, h, 22); c.clip(); c.rectangle(-w / 2, -h / 2, w, h * 0.26); c.clip(); c.set_source(agrad(-w / 2, 0, w / 2, 0)); c.paint_with_alpha(a); c.restore()
    txt(c, top, 0, -h / 2 + h * 0.13, w * 0.13, INK, a)
    txt(c, big, 0, h * 0.08, w * 0.42, INK, a)
    if sub: txt(c, sub, 0, h * 0.36, w * 0.09, (0.35, 0.3, 0.25), a, kind='monob')
    for dx in (-w * 0.25, w * 0.25):
        c.set_source_rgba(0.2, 0.2, 0.2, a); c.arc(dx, -h / 2 + 4, 9, 0, 2 * math.pi); c.fill()
    if hl: c.set_source_rgba(*AMBER, a); c.set_line_width(8); rrect(c, -w / 2 - 8, -h / 2 - 8, w + 16, h + 16, 26); c.stroke()
    c.restore()


def sun(c, x, y, r, t, a=1.0):
    c.save(); c.translate(x, y); c.rotate(t * 0.4)
    g = cairo.RadialGradient(0, 0, 0, 0, 0, r * 2.2); g.add_color_stop_rgba(0, *AMBER, 0.45 * a); g.add_color_stop_rgba(1, *AMBER, 0)
    c.set_source(g); c.arc(0, 0, r * 2.2, 0, 2 * math.pi); c.fill()
    c.set_source_rgba(*AMBER, a); c.set_line_width(r * 0.16); c.set_line_cap(cairo.LINE_CAP_ROUND)
    for i in range(12):
        an = i * math.pi / 6; c.move_to(math.cos(an) * r * 1.25, math.sin(an) * r * 1.25); c.line_to(math.cos(an) * r * 1.6, math.sin(an) * r * 1.6); c.stroke()
    c.set_source(agrad(-r, -r, r, r)); c.arc(0, 0, r, 0, 2 * math.pi); c.fill(); c.restore()


def moon(c, x, y, r, phase=0.25, a=1.0, glow=True):
    """phase 0=new, 0.5=full. draws lit part in cream over dark disk."""
    if glow:
        g = cairo.RadialGradient(x, y, 0, x, y, r * 2); g.add_color_stop_rgba(0, *CREAM, 0.25 * a * (0.3 + phase)); g.add_color_stop_rgba(1, *CREAM, 0)
        c.set_source(g); c.arc(x, y, r * 2, 0, 2 * math.pi); c.fill()
    c.set_source_rgba(0.16, 0.16, 0.20, a); c.arc(x, y, r, 0, 2 * math.pi); c.fill()
    k = math.cos(phase * 2 * math.pi)  # 1 new .. -1 full
    c.save(); c.arc(x, y, r, 0, 2 * math.pi); c.clip()
    c.set_source_rgba(*CREAM, a)
    if phase <= 0.5:   # waxing: lit on right
        c.arc(x, y, r, -math.pi / 2, math.pi / 2)
        c.save(); c.translate(x, y); c.scale(max(0.001, abs(k)), 1); c.arc_negative(0, 0, r, math.pi / 2, -math.pi / 2) if k > 0 else c.arc(0, 0, r, math.pi / 2, 3 * math.pi / 2); c.restore()
    else:
        c.arc(x, y, r, math.pi / 2, 3 * math.pi / 2)
        c.save(); c.translate(x, y); c.scale(max(0.001, abs(k)), 1); c.arc_negative(0, 0, r, 3 * math.pi / 2, math.pi / 2) if k > 0 else c.arc(0, 0, r, -math.pi / 2, math.pi / 2); c.restore()
    c.fill(); c.restore()
    c.set_source_rgba(1, 1, 1, 0.15 * a); c.set_line_width(2); c.arc(x, y, r, 0, 2 * math.pi); c.stroke()


def title_label(c, s, t, t0, y=150, px=46):
    u = e_out(prog(t, t0, t0 + 0.35))
    if u <= 0: return
    txt(c, s, W / 2, y - (1 - u) * 30, px, CREAM, u, maxw=1500)


# ---------- cold open ----------
QCARDS = [('Date changes?', 'తేదీ ఎందుకు మారుతుంది?'), ('Deep cleaning?', 'ఇల్లంతా శుభ్రం ఎందుకు?'), ('Bonus = gift?', 'Bonus బహుమతా?'),
          ('India from space?', 'Space photo నిజమా?'), ('Market on Diwali?', 'దీపావళికి Market?'), ("Delhi's air?", 'Delhi గాలి?'),
          ("Nepal's dogs?", 'Nepal కుక్కల పూజ?'), ('NYC school holiday?', 'New York సెలవు?'), ('Green crackers?', 'Green crackers?')]
QPOS = [(250, 200), (560, 130), (870, 190), (1180, 120), (1500, 210), (1700, 400), (180, 430), (1650, 610), (230, 650)]


def qcard(c, i, x, y, t, t0, wob=0.0, a=1.0, sc=1.0, locked=False):
    u = e_back(prog(t, t0, t0 + 0.3))
    if u <= 0.01 or a <= 0.01: return
    s = L(*QCARDS[i]); px = 30
    w = text_w(c, s, px) + 90; h = 74
    rot = (-4 + (i * 37 % 9)) + wob * 6 * math.sin(t * 18 + i)
    c.save(); c.translate(x, y); c.rotate(math.radians(rot)); c.scale(u * sc, u * sc)
    glass(c, -w / 2, -h / 2, w, h, 20, a)
    if locked:
        c.set_source_rgba(*AMBER, a); c.set_line_width(5); c.arc(-w / 2 + 40, -6, 10, math.pi, 2 * math.pi); c.stroke()
        rrect(c, -w / 2 + 26, -6, 28, 22, 4); c.fill()
    else:
        txt(c, '?', -w / 2 + 40, 0, 34, grad=True, a=a)
    txt(c, s, -w / 2 + 70, 0, px, CREAM, a, anchor='l')
    c.restore()


def title_slide(c, t, t0, tl_prog):
    board_bg(c, 0.10)
    cx, cy = W / 2, 450
    u = prog(t, t0, t0 + 0.5)
    # diya centre
    g = cairo.RadialGradient(cx, cy, 0, cx, cy, 420); g.add_color_stop_rgba(0, *AMBER, 0.25 * u); g.add_color_stop_rgba(1, *AMBER, 0)
    c.set_source(g); c.arc(cx, cy, 420, 0, 2 * math.pi); c.fill()
    RM.diya(c, cx, cy + 60, 1.6 * e_back(u) if u > 0 else 0.01, t)
    pos = [(cx + 660 * math.cos(a), cy + 290 * math.sin(a)) for a in [math.radians(-90 + k * 40) for k in range(9)]]
    for i, (x, y) in enumerate(pos):
        tt = t0 + 0.15 + i * 0.12
        thread(c, cx, cy + 10, x, y, t, tt + 0.15, 0.45, sag=30)
    for i, (x, y) in enumerate(pos):
        qcard(c, i, x, y, t, t0 + 0.15 + i * 0.12, locked=i >= 6, sc=1.05)
    v = e_out(prog(t, t0 + 1.2, t0 + 1.6))
    if v > 0:
        c.set_source_rgba(0, 0, 0, 0.55 * v); rrect(c, W / 2 - 560, 860, 1120, 140, 30); c.fill()
        txt(c, L('DIWALI, EXPLAINED', 'దీపావళి, వివరంగా'), W / 2, 930 + (1 - v) * 20, 86, grad=True, a=v, stroke=4)


# ---------- chapter 1 ----------
def g_dates(c, t, a1, a2):   # overlay on room
    cal_page(c, 420, 330, 260, L('LAST YEAR', 'పోయిన ఏడాది'), '20', L('OCT · 2025', 'అక్టో · 2025'), t, a1, rot=-5)
    cal_page(c, 1500, 330, 260, L('THIS YEAR', 'ఈ ఏడాది'), '8', L('NOV · 2026', 'నవం · 2026'), t, a2, rot=5, hl=True)


def g_sunmoon(c, t, t0, tm):
    board_bg(c)
    cal_page(c, W / 2, 560, 360, L('CALENDAR', 'క్యాలెండర్'), '?', None, t, t0)
    u = e_io(prog(t, tm - 0.3, tm + 0.5))
    sun(c, W / 2 - 480 - 900 * u, 520, 90, t, a=1 - u)
    if u > 0: moon(c, W / 2 + 480 + 600 * (1 - u), 520, 95, 0.28, a=u)
    if u > 0.6: pill(c, L('FOLLOWS THE MOON', 'చంద్రుడిని అనుసరిస్తుంది'), W / 2 + 480, 700, 30, a=prog(t, tm + 0.2, tm + 0.5))
    title_label(c, L('DIWALI', 'దీపావళి'), t, t0, 170, 60)


def g_moons(c, t, t0, t29, t354):
    board_bg(c)
    for i in range(12):
        x = 210 + i * 136; tt = t0 + 0.1 + i * 0.09
        if t < tt: continue
        moon(c, x, 330, 56 * e_back(prog(t, tt, tt + 0.3)), (i + 1) / 12.0 * 0.999, glow=False)
        txt(c, str(i + 1), x, 420, 28, CREAM, 0.6, kind='monob')
    if t >= t29:
        pill(c, L('29.5 DAYS EACH', 'ఒక్కొక్కటి 29.5 రోజులు'), W / 2, 180, 40, sc=e_back(prog(t, t29, t29 + 0.3)))
    if t >= t354:
        u = e_out(prog(t, t354, t354 + 0.9))
        for k, (lab, val, col, y) in enumerate(((L('MOON YEAR', 'చంద్ర సంవత్సరం'), 354, AMBER, 660), (L('SUN YEAR', 'సూర్య సంవత్సరం'), 365, CREAM, 790))):
            ww = 1100 * val / 365 * u
            c.set_source_rgba(*col, 0.9); rrect(c, 520, y - 40, max(10, ww), 80, 40); c.fill()
            txt(c, lab, 490, y, 36, CREAM, anchor='r')
            txt(c, f'{int(val * u)}', 520 + ww - 24, y, 52, INK, anchor='r')
        if u >= 1: marker_line(c, 520 + 1100 * 354 / 365, 620, 520 + 1100, 620, t, t354 + 1.0, 0.4)


def g_eleven(c, t, t0):
    big_num(c, L('−11 DAYS', '−11 రోజులు'), 1500, 420, 120, t, t0)


def drift_band(c, y=560, x0=200, x1=1720):
    c.set_source_rgba(1, 1, 1, 0.07); rrect(c, x0, y - 70, x1 - x0, 140, 34); c.fill()
    # Sep 15 .. Dec 15 => 91 days
    days = 91
    for d in range(0, days + 1):
        x = x0 + (x1 - x0) * d / days
        if d in (16, 46, 77):
            c.set_source_rgba(*CREAM, 0.7); c.rectangle(x - 1.5, y - 60, 3, 120); c.fill()
    for lab, d in ((L('OCTOBER', 'అక్టోబర్'), 31), (L('NOVEMBER', 'నవంబర్'), 61)):
        txt(c, lab, x0 + (x1 - x0) * d / days, y - 150, 44, CREAM, 0.85, kind='monob')
    return lambda day: x0 + (x1 - x0) * (day + 16) / days   # day 0 = Oct 1


def marker(c, x, y, lab, a=1.0, col=AMBER):
    glowdot(c, x, y, 16, a)
    c.set_source_rgba(*col, a); c.set_line_width(5); c.move_to(x, y + 24); c.line_to(x, y + 110); c.stroke()
    pill(c, lab, x, y + 150, 38, a=a)


def g_drift(c, t, t0):
    board_bg(c); X = drift_band(c)
    u = e_io(prog(t, t0 + 0.8, t0 + 2.4))
    day = 38 - 11 * u   # Nov 8 -> Oct 28
    marker(c, X(day), 560, 'DIWALI' if LANG == 'en' else 'దీపావళి')
    if u > 0.05:
        c.set_source_rgba(*AMBER, 0.7); c.set_line_width(7); c.move_to(X(38), 440); c.line_to(X(day), 440); c.stroke()
        arrow_head(c, X(day) - 4, 440, math.pi, 28)
        txt(c, L('11 DAYS EARLIER EVERY YEAR', 'ప్రతి ఏడాది 11 రోజులు ముందు'), W / 2, 880, 54, CREAM, prog(t, t0 + 1.4, t0 + 1.8))


def g_adhik(c, t, t0, tm):
    board_bg(c); X = drift_band(c)
    u = e_io(prog(t, t0 + 0.2, t0 + 1.4)); day = 27 - 22 * u
    v = e_io(prog(t, tm + 0.5, tm + 1.3)); day = day + 25 * v
    marker(c, X(day), 560, 'DIWALI' if LANG == 'en' else 'దీపావళి')
    if t >= tm:
        w = e_back(prog(t, tm, tm + 0.35))
        c.save(); c.translate(W / 2, 260); c.scale(w, w); glass(c, -420, -80, 840, 160, 28)
        txt(c, L('+1 MONTH', '+1 నెల'), -200, 0, 64, grad=True); txt(c, 'ADHIK MAAS' if LANG == 'en' else 'అధిక మాసం', 190, 0, 44, CREAM); c.restore()
    if u > 0.9 and v < 0.1 and t < tm:
        txt(c, L('drifting towards summer…', 'వేసవి వైపు జారుతోంది…'), W / 2, 880, 44, CREAM, 0.85)


def clock(c, cx, cy, r, ang_m, ang_h, a=1.0, fast=False):
    c.set_source_rgba(0.97, 0.95, 0.90, a); c.arc(cx, cy, r, 0, 2 * math.pi); c.fill()
    c.set_source(agrad(cx - r, cy - r, cx + r, cy + r)); c.set_line_width(r * 0.1); c.arc(cx, cy, r, 0, 2 * math.pi); c.stroke()
    for i in range(12):
        an = i * math.pi / 6; c.set_source_rgba(*INK, a); c.set_line_width(6)
        c.move_to(cx + math.cos(an) * r * 0.78, cy + math.sin(an) * r * 0.78); c.line_to(cx + math.cos(an) * r * 0.88, cy + math.sin(an) * r * 0.88); c.stroke()
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    for ang, ln, wd in ((ang_h, 0.5, 14), (ang_m, 0.75, 9)):
        c.set_source_rgba(*INK, a); c.set_line_width(wd); c.move_to(cx, cy); c.line_to(cx + math.cos(ang - math.pi / 2) * r * ln, cy + math.sin(ang - math.pi / 2) * r * ln); c.stroke()
    c.set_source_rgba(*AMBER, a); c.arc(cx, cy, 12, 0, 2 * math.pi); c.fill()


def g_watch(c, t, t0, tfix):
    board_bg(c)
    if t < tfix:
        k = (t - t0) * 6; clock(c, W / 2, 520, 260, k, k / 12)
        pill(c, L('RUNS A LITTLE FAST', 'కొంచెం fast గా నడుస్తుంది'), W / 2, 870, 32, a=prog(t, t0 + 0.3, t0 + 0.6))
    else:
        k0 = (tfix - t0) * 6; u = e_out(prog(t, tfix, tfix + 0.5)); k = k0 + (round(k0 / (2 * math.pi)) * 2 * math.pi - k0) * u
        clock(c, W / 2, 520, 260, k, k / 12)
        stamp(c, L('FIXED', 'సరిచేశారు'), W / 2 + 330, 330, t, tfix + 0.2, 70, rot=8)
        pill(c, L('= ADHIK MAAS', '= అధిక మాసం'), W / 2, 870, 32, a=prog(t, tfix + 0.2, tfix + 0.5))


def g_window(c, t, t0):
    board_bg(c); X = drift_band(c)
    u = e_out(prog(t, t0, t0 + 0.6))
    c.set_source_rgba(*AMBER, 0.22 * u); rrect(c, X(14), 500, X(45) - X(14), 120, 20); c.fill()
    c.set_source_rgba(*AMBER, 0.9 * u); c.set_line_width(4); rrect(c, X(14), 500, X(45) - X(14), 120, 20); c.stroke()
    txt(c, L('MID-OCT → MID-NOV', 'అక్టో మధ్య → నవం మధ్య'), (X(14) + X(45)) / 2, 250, 72, grad=True, a=u, stroke=4)
    for k, (d, lab) in enumerate(((19, '2025'), (38, '2026'), (28, '2027'))):
        tt = t0 + 0.6 + k * 0.35
        if t >= tt: glowdot(c, X(d), 560, 11); pill(c, lab, X(d), 700 + (k % 2) * 80, 34, sc=e_back(prog(t, tt, tt + 0.3)))


def kite(c, x, y, s, t, a=1.0):
    c.save(); c.translate(x, y + 6 * math.sin(t * 2)); c.rotate(math.radians(8 * math.sin(t * 1.5))); c.scale(s, s)
    c.move_to(0, -60); c.line_to(45, 0); c.line_to(0, 70); c.line_to(-45, 0); c.close_path()
    c.set_source_rgba(1.0, 0.45, 0.25, a); c.fill_preserve(); c.set_source_rgba(0.1, 0.05, 0.03, a); c.set_line_width(3); c.stroke()
    c.move_to(0, -60); c.line_to(0, 70); c.move_to(-45, 0); c.line_to(45, 0); c.stroke()
    c.set_source_rgba(*CREAM, 0.8 * a); c.set_line_width(2); c.move_to(0, 70); c.curve_to(20, 120, -20, 160, 10, 210); c.stroke(); c.restore()


def g_sankranti(c, t, t0):
    board_bg(c)
    for i, yr in enumerate(('2024', '2025', '2026', '2027')):
        cal_page(c, 360 + i * 400, 560, 260, L('JANUARY', 'జనవరి'), '14' if i != 2 else '14', yr, t, t0 + 0.2 + i * 0.25, rot=-3 + i * 2)
    kite(c, W / 2, 200, 1.0, t)
    pill(c, L('SANKRANTI · FOLLOWS THE SUN', 'సంక్రాంతి · సూర్యుడిని అనుసరిస్తుంది'), W / 2, 870, 40, a=prog(t, t0 + 1.0, t0 + 1.3))


def g_eid(c, t, t0):
    board_bg(c)
    x0, x1, y = 160, 1760, 560
    seasons = [(L('WINTER', 'చలికాలం'), SKY), (L('SUMMER', 'వేసవి'), AMBER), (L('MONSOON', 'వర్షాకాలం'), TEAL), (L('WINTER', 'చలికాలం'), SKY)]
    seg = (x1 - x0) / 4
    for i, (lab, col) in enumerate(seasons):
        c.set_source_rgba(*col, 0.35); rrect(c, x0 + i * seg + 6, y - 80, seg - 12, 160, 26); c.fill()
        txt(c, lab, x0 + i * seg + seg / 2, y + 125, 40, CREAM, 0.85, kind='monob')
    u = prog(t, t0 + 0.3, t0 + 5.5)
    xm = x1 - 60 - (x1 - x0 - 120) * u
    moon(c, xm, y, 60, 0.12)
    txt(c, 'EID' if LANG == 'en' else 'ఈద్', xm, y - 120, 44, grad=True)
    pill(c, L('NO EXTRA MONTH → MOVES ALL YEAR', 'అదనపు నెల లేదు → ఏడాదంతా తిరుగుతుంది'), W / 2, 230, 40, a=prog(t, t0 + 1.0, t0 + 1.3))


def g_amavasya(c, t, t0, tdiya):
    k = prog(t, t0, t0 + 1.8)
    c.set_source_rgb(lerp(0.10, 0.02, k), lerp(0.12, 0.02, k), lerp(0.25, 0.06, k)); c.paint()
    rng = np.random.default_rng(5)
    for i in range(90):
        x, y = rng.uniform(0, W), rng.uniform(0, 650); tw = 0.5 + 0.5 * math.sin(t * 2 + i)
        c.set_source_rgba(1, 1, 1, (0.2 + 0.6 * k) * tw * 0.8); c.arc(x, y, rng.uniform(1, 2.6), 0, 2 * math.pi); c.fill()
    moon(c, W / 2, 300, 110, 0.5 * (1 - k) + 0.001 * k, a=1 - 0.75 * k)
    if k > 0.8:
        pill(c, 'AMAVASYA · KARTIKA' if LANG == 'en' else 'అమావాస్య · కార్తీకం', W / 2, 470, 32, a=prog(t, t0 + 1.6, t0 + 2.0), outline=True)
    c.set_source_rgb(0.08, 0.06, 0.05); c.rectangle(0, 860, W, 220); c.fill()
    for i in range(9):
        tt = tdiya + i * 0.28
        RM.diya(c, 260 + i * 175, 880, 0.9, t, lit=e_out(prog(t, tt, tt + 0.25)))


def g_2027(c, t, t0, ts):
    board_bg(c)
    # month grid Oct 2027 (Oct 1 2027 is a Friday)
    gx, gy, cw, chh = 560, 230, 114, 96
    glass(c, gx - 40, gy - 110, cw * 7 + 80, chh * 6 + 160, 30, edge=False)
    txt(c, L('OCTOBER 2027', 'అక్టోబర్ 2027'), gx + cw * 3.5, gy - 55, 40, CREAM)
    for d in range(1, 32):
        idx = d - 1 + 5; r, col = divmod(idx, 7)
        x, y = gx + col * cw + cw / 2, gy + 30 + r * chh
        txt(c, str(d), x, y, 34, AMBER if d == 29 else CREAM, 0.95 if d == 29 else 0.55, kind='monob')
        if d == 29: marker_circle(c, x, y, 44, 38, t, t0 + 0.4)
    stamp(c, '2027 · OCT 29', W / 2, 860, t, ts, 72, rot=-6)


# ---------- chapter 2 ----------
def wall_bg(c, damp=0.0, light=0.0):
    c.set_source_rgb(lerp(0.78, 0.62, damp), lerp(0.70, 0.60, damp), lerp(0.58, 0.52, damp)); c.paint()
    if light:
        g = cairo.LinearGradient(W, 0, 400, H); g.add_color_stop_rgba(0, 1, 0.95, 0.75, 0.5 * light); g.add_color_stop_rgba(1, 1, 0.95, 0.75, 0)
        c.set_source(g); c.paint()


def g_damp(c, t, t0):
    u = prog(t, t0, t0 + 3.5); wall_bg(c, 0.5 * u)
    rng = np.random.default_rng(11)
    for i in range(16):
        x, y, r = rng.uniform(80, 1300), rng.uniform(80, 1000), rng.uniform(40, 150) * min(1, u * 1.6 + 0.2)
        g = cairo.RadialGradient(x, y, 0, x, y, r); g.add_color_stop_rgba(0, 0.28, 0.34, 0.24, 0.55); g.add_color_stop_rgba(1, 0.28, 0.34, 0.24, 0)
        c.set_source(g); c.arc(x, y, r, 0, 2 * math.pi); c.fill()
    # window with rain
    wx, wy = 1400, 160
    c.set_source_rgb(0.35, 0.25, 0.17); rrect(c, wx - 16, wy - 16, 432, 552, 12); c.fill()
    c.set_source_rgb(0.25, 0.32, 0.40); c.rectangle(wx, wy, 400, 520); c.fill()
    c.set_source_rgba(0.85, 0.92, 1.0, 0.55); c.set_line_width(2.5)
    for i in range(70):
        x = wx + (i * 53) % 400; y = wy + ((i * 97 + t * 900) % 560) - 40
        c.move_to(x, y); c.line_to(x - 8, y + 34); c.stroke()
    # insects
    for i in range(6):
        x = 300 + 900 * ((i * 0.37 + t * 0.05 * (1 + i % 3)) % 1); y = 700 + 80 * math.sin(t * 2 + i)
        c.set_source_rgba(0.1, 0.08, 0.05, 0.8); c.arc(x, y, 6, 0, 2 * math.pi); c.fill()
    pill(c, L('4 MONTHS OF RAIN', '4 నెలల వర్షం'), 700, 160, 36, a=prog(t, t0 + 0.2, t0 + 0.5), outline=True)


def gauge(c, cx, cy, r, val, lab):
    c.set_source_rgba(1, 1, 1, 0.12); c.set_line_width(36); c.arc(cx, cy, r, math.pi, 2 * math.pi); c.stroke()
    c.set_source(agrad(cx - r, cy, cx + r, cy)); c.arc(cx, cy, r, math.pi, math.pi + math.pi * val); c.stroke()
    txt(c, f'{int(val * 100)}%', cx, cy - 50, 90, CREAM, stroke=6)
    txt(c, lab, cx, cy + 40, 26, CREAM, 0.8, kind='monob')


def g_dry(c, t, t0):
    u = e_io(prog(t, t0 + 0.2, t0 + 1.4)); wall_bg(c, 0.2 * (1 - u), u)
    wx, wy = 300, 160
    c.set_source_rgb(0.35, 0.25, 0.17); rrect(c, wx - 16, wy - 16, 532, 632, 12); c.fill()
    sk = cairo.LinearGradient(0, wy, 0, wy + 600); sk.add_color_stop_rgb(0, 0.45, 0.70, 0.95); sk.add_color_stop_rgb(1, 0.85, 0.92, 1.0)
    c.set_source(sk); c.rectangle(wx, wy, 500, 600); c.fill(); sun(c, wx + 360, wy + 160, 60, t)
    for side in (0, 1):  # shutters open
        ang = u * 1.3
        c.save(); c.translate(wx + (500 if side else 0), wy); sx = math.cos(ang) * (1 if side == 0 else -1)
        c.scale(sx, 1); c.set_source_rgb(0.55, 0.38, 0.24); c.rectangle(0, 0, 250, 600); c.fill()
        c.set_source_rgba(0, 0, 0, 0.2); c.set_line_width(3)
        for k in range(1, 12): c.move_to(10, k * 50); c.line_to(240, k * 50); c.stroke()
        c.restore()
    val = lerp(0.85, 0.45, e_io(prog(t, t0 + 0.8, t0 + 3.0)))
    glass(c, 1080, 260, 620, 460, 30); gauge(c, 1390, 560, 210, val, L('HUMIDITY', 'తేమ'))
    pill(c, L('DRY AIR · CLEAN, DRY, PAINT', 'పొడి గాలి · శుభ్రం, ఆరబెట్టు, రంగు'), 1390, 800, 32, a=prog(t, t0 + 1.5, t0 + 1.8))


def old_house(c, x, y, s, white=0.0, t=0, a=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.move_to(-320, -230); c.line_to(0, -400); c.line_to(320, -230); c.close_path(); c.set_source_rgba(0.62, 0.28, 0.16, a); c.fill()
    for k in range(8):
        c.set_source_rgba(0.45, 0.20, 0.10, a); c.set_line_width(3); c.move_to(-300 + k * 80, -235); c.line_to(-300 + k * 80 + 40, -330 + abs(k - 3.75) * 10); c.stroke()
    wall = (lerp(0.66, 0.97, white), lerp(0.52, 0.96, white), lerp(0.38, 0.92, white))
    c.set_source_rgba(*wall, a); c.rectangle(-280, -230, 560, 330); c.fill()
    c.set_source_rgba(0.42, 0.28, 0.18, a); c.rectangle(-60, -100, 120, 200); c.fill()
    for dx in (-190, 190): c.set_source_rgba(0.30, 0.22, 0.16, a); c.rectangle(dx - 45, -170, 90, 80); c.fill()
    c.set_source_rgba(0.50, 0.36, 0.22, a); c.rectangle(-360, 100, 720, 40); c.fill()
    c.restore()


def g_lime(c, t, t0):
    board_bg(c, 0.12)
    u = e_io(prog(t, t0 + 0.8, t0 + 3.4))
    old_house(c, 780, 680, 1.25, white=u, t=t)
    bx = 780 - 350 + 700 * u
    if 0 < u < 1:
        c.set_source_rgba(1, 1, 1, 0.9); c.set_line_width(14); c.set_line_cap(cairo.LINE_CAP_ROUND)
        c.move_to(bx, 400 + 60 * math.sin(t * 9)); c.line_to(bx + 40, 300); c.stroke()
    # bucket
    c.save(); c.translate(1500, 760)
    c.move_to(-110, -120); c.line_to(110, -120); c.line_to(85, 90); c.line_to(-85, 90); c.close_path(); c.set_source_rgb(0.55, 0.55, 0.58); c.fill()
    c.save(); c.scale(1, 0.25); c.arc(0, -480, 110, 0, 2 * math.pi); c.restore(); c.set_source_rgb(0.97, 0.97, 0.95); c.fill(); c.restore()
    pill(c, L('LIME · CHUNA', 'సున్నం'), 1500, 600, 30)
    pill(c, L('NATURAL DISINFECTANT', 'సహజ క్రిమిసంహారిణి'), 1500, 860, 30, a=prog(t, t0 + 1.4, t0 + 1.7), outline=True)


def apartment(c, x, y, s, t, a=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.set_source_rgba(0.80, 0.80, 0.84, a); c.rectangle(-200, -420, 400, 520); c.fill()
    for r in range(5):
        for k in range(3):
            c.set_source_rgba(1.0, 0.80, 0.45, a * (0.7 + 0.3 * math.sin(t * 2 + r + k))); c.rectangle(-160 + k * 120, -390 + r * 95, 80, 60); c.fill()
    c.restore()


def sparkle(c, x, y, s, t, ph=0):
    k = 0.5 + 0.5 * math.sin(t * 5 + ph); c.save(); c.translate(x, y); c.scale(s * (0.6 + 0.4 * k), s * (0.6 + 0.4 * k))
    c.move_to(0, -30); c.curve_to(4, -4, 4, -4, 30, 0); c.curve_to(4, 4, 4, 4, 0, 30); c.curve_to(-4, 4, -4, 4, -30, 0); c.curve_to(-4, -4, -4, -4, 0, -30)
    c.set_source_rgba(1, 0.95, 0.75, 0.9); c.fill(); c.restore()


def g_split(c, t, t0):
    board_bg(c)
    c.set_source_rgba(1, 1, 1, 0.08); c.rectangle(W / 2 - 2, 120, 4, 840); c.fill()
    old_house(c, 480, 720, 0.95, white=1.0, t=t)
    apartment(c, 1440, 760, 1.1, t)
    for i in range(5): sparkle(c, 300 + i * 90, 380 + (i % 2) * 60, 0.8, t, i); sparkle(c, 1260 + i * 90, 300 + (i % 2) * 70, 0.8, t, i + 3)
    pill(c, L('THEN', 'అప్పుడు'), 480, 200, 34, sc=e_back(prog(t, t0, t0 + 0.3)))
    pill(c, L('NOW', 'ఇప్పుడు'), 1440, 200, 34, sc=e_back(prog(t, t0 + 0.4, t0 + 0.7)))
    pill(c, L('THE HABIT STAYED', 'అలవాటు అలాగే ఉంది'), W / 2, 120, 34, a=prog(t, t0 + 1.4, t0 + 1.8), outline=True)


def ledger(c, x, y, s, open_=1.0, red=True, label=None, t=0, a=1.0, symbol=False):
    c.save(); c.translate(x, y); c.scale(s, s)
    cov = (0.62, 0.10, 0.12) if red else (0.45, 0.38, 0.30)
    c.set_source_rgba(0, 0, 0, 0.4 * a); rrect(c, -300, -190, 620, 420, 16); c.fill()
    # right page (always) + left page / cover rotating
    c.set_source_rgba(*cov, a); rrect(c, 0, -200, 300, 400, 12); c.fill()
    c.set_source_rgba(0.97, 0.94, 0.86, a); rrect(c, 8, -190, 280, 380, 8); c.fill()
    c.set_source_rgba(0.5, 0.4, 0.3, 0.35 * a); c.set_line_width(2)
    for k in range(10): c.move_to(30, -150 + k * 34); c.line_to(270, -150 + k * 34); c.stroke()
    sx = math.cos(open_ * math.pi)  # 1 closed (over right) .. -1 open (left)
    c.save(); c.scale(sx, 1)
    if sx > 0:
        c.set_source_rgba(*cov, a); rrect(c, 0, -200, 300, 400, 12); c.fill()
        c.set_source_rgba(*AMBER, a); c.rectangle(16, -200, 22, 400); c.fill()
    else:
        c.set_source_rgba(*cov, a); rrect(c, 0, -200, 300, 400, 12); c.fill()
        c.set_source_rgba(0.97, 0.94, 0.86, a); rrect(c, 8, -190, 280, 380, 8); c.fill()
    c.restore()
    if symbol and open_ > 0.6:
        v = prog(open_, 0.6, 1.0)
        sv = (0.85, 0.25, 0.10)
        c.save(); c.translate(150, -40); c.set_source_rgba(*sv, a * v); c.set_line_width(12); c.set_line_cap(cairo.LINE_CAP_ROUND)
        for r in range(4):
            c.save(); c.rotate(r * math.pi / 2); c.move_to(0, 0); c.line_to(0, -70); c.line_to(55, -70); c.stroke(); c.restore()
        for (dx, dy) in ((35, -35), (-35, -35), (35, 35), (-35, 35)): c.arc(dx, dy, 7, 0, 2 * math.pi); c.fill()
        c.restore()
        txt(c, 'SHUBH', -150, -40, 40, sv, a * v); txt(c, 'LABH', -150, 30, 40, sv, a * v)
        txt(c, 'शुभ · लाभ' if False else '', 0, 0, 10)
    c.restore()
    if label: pill(c, label, x, y + 260 * s, 28, a=a)


def g_ledger(c, t, t0, lab1, lab2, symbol=False):
    board_bg(c)
    u = e_io(prog(t, t0 + 0.3, t0 + 1.0))
    if u < 1:
        ledger(c, W / 2 - 60 * u, 540, 1.1, open_=1 - u, red=False, label=lab1, t=t, a=1)
    else:
        v = e_io(prog(t, t0 + 1.2, t0 + 2.0))
        ledger(c, W / 2, 540 + (1 - e_out(prog(t, t0 + 1.0, t0 + 1.3))) * 80, 1.1, open_=v, red=True, label=lab2, t=t, symbol=symbol)


# ---------- chapter 3 ----------
def gift_box(c, x, y, s, a=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.set_source_rgba(*TEAL, a); rrect(c, -120, -80, 240, 180, 10); c.fill()
    c.set_source_rgba(0.12, 0.45, 0.45, a); rrect(c, -135, -120, 270, 50, 8); c.fill()
    c.set_source_rgba(*AMBER, a); c.rectangle(-18, -120, 36, 220); c.fill()
    for d in (-1, 1):
        c.save(); c.translate(d * 30, -130); c.scale(1.4, 0.8); c.arc(0, 0, 30, 0, 2 * math.pi); c.restore(); c.set_line_width(12); c.stroke()
    c.restore()


def g_giftlaw(c, t, t0, tlaw):
    board_bg(c)
    gift_box(c, 620, 560, 1.4, a=1 - 0.5 * prog(t, tlaw, tlaw + 0.3))
    if t >= tlaw - 0.6:
        c.set_source_rgba(0.95, 0.95, 0.95, 0.85); c.set_line_width(16); c.set_line_cap(cairo.LINE_CAP_ROUND)
        u = e_io(prog(t, tlaw - 0.6, tlaw - 0.3)); c.move_to(420, 360); c.line_to(lerp(420, 820, u), lerp(360, 760, u)); c.stroke()
        v = e_io(prog(t, tlaw - 0.3, tlaw)); c.move_to(820, 360); c.line_to(lerp(820, 420, v), lerp(360, 760, v)) if v > 0 else None; c.stroke()
    txt(c, L('GIFT?', 'బహుమతా?'), 620, 220, 60, CREAM, prog(t, t0, t0 + 0.3))
    stamp(c, L('LAW', 'చట్టం'), 1320, 540, t, tlaw, 150, rot=-8)


def g_checklist(c, t, t0, ts):
    board_bg(c)
    rows = [(L('Earn up to ₹21,000 a month', 'నెలకు ₹21,000 వరకు జీతం'), '₹'), (L('Worked at least 30 days', 'కనీసం 30 రోజులు పని'), '30'), (L('Company has 20+ people', 'కంపెనీలో 20+ మంది'), '20+')]
    for i, ((lab, ic), tt) in enumerate(zip(rows, ts)):
        y = 300 + i * 200; u = e_out(prog(t, tt - 0.25, tt + 0.15))
        if u <= 0: continue
        c.save(); c.translate((1 - u) * 80, 0)
        glass(c, 330, y - 70, 1260, 140, 30, u)
        txt(c, ic, 430, y, 46, grad=True, a=u); txt(c, lab, 520, y, 42, CREAM, u, anchor='l')
        c.restore()
        if t >= tt + 0.15:
            k = e_back(prog(t, tt + 0.15, tt + 0.4)); c.save(); c.translate(1500, y); c.scale(k, k)
            c.set_source(agrad(-40, -40, 40, 40)); c.arc(0, 0, 44, 0, 2 * math.pi); c.fill()
            c.set_source_rgb(*INK); c.set_line_width(10); c.set_line_cap(cairo.LINE_CAP_ROUND); c.move_to(-18, 2); c.line_to(-4, 16); c.line_to(20, -14); c.stroke(); c.restore()


def g_pct(c, t, t0, t833, t20, clip_t):
    board_bg(c)
    big_num(c, '8.33%', 560, 330, 150, t, t833)
    txt(c, L('MINIMUM', 'కనీసం'), 560, 450, 30, CREAM, prog(t, t833, t833 + 0.3), kind='monob')
    if t >= t20:
        marker_line(c, 860, 330, 1040, 330, t, t20 - 0.25, 0.25, 10); arrow_head(c, 1060, 330, 0, 30)
    big_num(c, '20%', 1330, 330, 150, t, t20)
    txt(c, L('MAXIMUM', 'గరిష్టం'), 1330, 450, 30, CREAM, prog(t, t20, t20 + 0.3), kind='monob')
    draw_clip(c, 'bonus_k', W / 2, 760, 1500, t, clip_t, rot=-1, hl_t0=clip_t + 0.4, hl_dur=1.6, src='EZYLEGAL · PAYMENT OF BONUS ACT, 1965')


def g_tiles(c, t, t0, tglow):
    board_bg(c)
    names = MONTHS if LANG == 'en' else MONTHS_TE
    for i in range(12):
        x = 260 + (i % 6) * 230; y = 330 + (i // 6) * 230; tt = t0 + 0.05 * i
        u = e_back(prog(t, tt, tt + 0.3))
        if u <= 0: continue
        c.save(); c.translate(x, y); c.scale(u, u); glass(c, -95, -95, 190, 190, 24, edge=False); txt(c, names[i], 0, 0, 40, CREAM); c.restore()
    if t >= tglow:
        u = e_back(prog(t, tglow, tglow + 0.4)); c.save(); c.translate(1640, 445); c.scale(u, u)
        g = cairo.RadialGradient(0, 0, 0, 0, 0, 260); g.add_color_stop_rgba(0, *AMBER, 0.5); g.add_color_stop_rgba(1, *AMBER, 0); c.set_source(g); c.arc(0, 0, 260, 0, 2 * math.pi); c.fill()
        c.set_source(agrad(-120, -120, 120, 120)); rrect(c, -120, -120, 240, 240, 30); c.fill(); txt(c, '+1', 0, -20, 90, INK); txt(c, L('MONTH', 'నెల'), 0, 70, 30, INK); c.restore()
        txt(c, L('8.33% = 1 MONTH OUT OF 12', '8.33% = 12 లో 1 నెల'), W / 2, 900, 48, grad=True, a=prog(t, tglow + 0.3, tglow + 0.6))


def g_formula(c, t, t0):
    board_bg(c)
    parts = ['₹7,000', '×', '8.33%', '×', '12', '≈', '₹7,000']
    xs = [330, 600, 820, 1040, 1180, 1340, 1600]
    for i, (p, x) in enumerate(zip(parts, xs)):
        tt = t0 + 0.4 + i * 0.25
        if p in '×≈': txt(c, p, x, 480, 80, CREAM, prog(t, tt, tt + 0.2))
        else: big_num(c, p, x, 480, 96 if i < 6 else 110, t, tt)
    txt(c, L('per month   ·   bonus rate   ·   months   =   about one month’s pay', 'నెలకు · bonus శాతం · నెలలు = దాదాపు ఒక నెల జీతం'), W / 2, 620, 26, CREAM, 0.75 * prog(t, t0 + 2.2, t0 + 2.6), kind='monob')
    if t > t0 + 2.4: marker_circle(c, 1600, 480, 190, 90, t, t0 + 2.4)


def g_months8(c, t, t0):
    board_bg(c)
    x0, x1, y = 260, 1660, 420
    labs = (['APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV'] if LANG == 'en' else ['ఏప్రి', 'మే', 'జూన్', 'జూలై', 'ఆగ', 'సెప్టె', 'అక్టో', 'నవం'])
    u = e_out(prog(t, t0 + 0.3, t0 + 2.2))
    c.set_source_rgba(1, 1, 1, 0.08); rrect(c, x0, y - 40, x1 - x0, 80, 40); c.fill()
    c.set_source(agrad(x0, 0, x1, 0)); rrect(c, x0, y - 40, max(80, (x1 - x0) * u), 80, 40); c.fill()
    for i, lb in enumerate(labs):
        x = x0 + (x1 - x0) * (i + 0.5) / 8; txt(c, lb, x, y + 80, 26, CREAM, 0.75, kind='monob')
    txt(c, L('YEAR ENDS · MAR 31', 'సంవత్సరం ముగింపు · మార్చి 31'), x0, y - 90, 28, CREAM, anchor='l', kind='monob')
    txt(c, L('8 MONTHS TO PAY', 'చెల్లించడానికి 8 నెలలు'), x1, y - 90, 34, grad=True, anchor='r')
    if u > 0.75:
        xd = x0 + (x1 - x0) * 7.2 / 8; glowdot(c, xd, y, 12); pill(c, L('DIWALI', 'దీపావళి'), xd, y + 150, 26)
    draw_clip(c, 'bonus_8', W / 2, 820, 1560, t, t0 + 0.8, rot=-0.8, hl_t0=t0 + 1.3, hl_dur=1.4, src='EZYLEGAL · PAYMENT OF BONUS ACT, 1965')


def fmt_lakh(v):
    return f'₹{v:.2f} lakh crore' if LANG == 'en' else f'₹{v:.2f} లక్షల కోట్లు'


def g_counter(c, t, t0, tclip):
    board_bg(c)
    u = e_out(prog(t, t0 + 0.2, t0 + 2.0)); v = 6.05 * u
    txt(c, fmt_lakh(v), W / 2, 250, 110, grad=True, stroke=6)
    txt(c, L('DIWALI 2025 SALES', 'దీపావళి 2025 అమ్మకాలు'), W / 2, 360, 30, CREAM, 0.8, kind='monob')
    draw_clip(c, 'cait', W / 2, 670, 600, t, tclip, rot=1.2, hl_t0=tclip + 0.4, hl_dur=0.8, src='BUSINESS TODAY · CAIT REPORT · OCT 21, 2025')


def person(c, x, y, s, a=1.0, col=CREAM):
    c.set_source_rgba(*col, a); c.arc(x, y - 30 * s, 14 * s, 0, 2 * math.pi); c.fill()
    rrect(c, x - 18 * s, y - 12 * s, 36 * s, 44 * s, 12 * s); c.fill()


def g_jobs(c, t, t0):
    board_bg(c)
    n = 10 * 5
    for i in range(n):
        tt = t0 + 0.2 + i * 0.03; a = prog(t, tt, tt + 0.15)
        person(c, 330 + (i % 10) * 70, 300 + (i // 10) * 90, 1.4, a, AMBER if (i % 10 + i // 10) % 3 == 0 else CREAM)
    txt(c, L('50 LAKH', '50 లక్షల'), 1440, 380, 120, grad=True, a=prog(t, t0 + 0.6, t0 + 0.9), stroke=6)
    txt(c, L('TEMPORARY JOBS', 'తాత్కాలిక ఉద్యోగాలు'), 1440, 500, 40, CREAM, prog(t, t0 + 0.8, t0 + 1.1))
    txt(c, L('logistics · packaging · transport · retail', 'logistics · packing · రవాణా · షాపులు'), 1440, 570, 24, CREAM, 0.7 * prog(t, t0 + 1.0, t0 + 1.3), kind='monob')
    txt(c, L('1 icon ≈ 1 lakh people', '1 బొమ్మ ≈ 1 లక్ష మంది'), 680, 790, 22, CREAM, 0.6 * prog(t, t0 + 1.2, t0 + 1.5), kind='mono')
    draw_clip(c, 'cait', W / 2, 1300, 700, t, 10 ** 9)
