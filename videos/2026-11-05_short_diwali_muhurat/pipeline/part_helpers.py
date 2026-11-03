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
    txt = 'DIWALI · 4/6' if LANGV == 'en' else 'దీపావళి · 4/6'
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
        (sx, sy), (ex, ey) = SL[LANGV][5][1], SL[LANGV][6][1]; sy += 200; ey += 200
        x = sx + (ex - sx) * e_io(k); y = sy + (ey - sy) * e_io(k) - math.sin(k * math.pi) * 120
        glowdot(c, x, y, 13 if k < 1 else 10 + 2 * math.sin(t * 6))
    c.pop_group_to_source(); c.paint_with_alpha(a); c.restore()

