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
