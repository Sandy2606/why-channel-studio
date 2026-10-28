"""The '?' host: a geometric round-stroke question mark (from the WHY? logo) with one eye.
Pose params:
  tilt   degrees (+ = leans right)
  sq     squash/stretch (1 = neutral, >1 tall, <1 squashed)
  eye    'open' | 'wide' | 'happy' | 'squint' | 'blink'
  look   (dx,dy) pupil offset, -1..1
  brow   -1 (worried) .. 0 none .. +1 (raised/surprised)
  morph  0 = '?', 1 = '!'
  glow   0..1 amber dot glow
  alpha  0..1
"""
import math, cairo

CREAM = (0.957, 0.945, 0.918)
AMBER = (1.0, 0.698, 0.141)
INK = (0.04, 0.04, 0.04)

N = 120

def _q_points():
    """'?' centreline in unit space (height ~1.0, origin = dot centre)."""
    pts = []
    R = 0.24
    cx, cy = 0.0, -0.76          # hook centre
    # hook: from angle 200deg (left, slightly low) clockwise over top to 70deg (right-bottom)
    a0, a1 = math.radians(195), math.radians(-60 + 360 * 0)  # go via top: 195 -> 90 -> 0 -> -60
    span = (math.radians(195) - math.radians(-60))
    nh = 80
    for i in range(nh):
        t = i / (nh - 1)
        a = math.radians(195) - span * t
        pts.append((cx + R * math.cos(a), cy - R * math.sin(a)))
    # curve into the stem: from hook end towards centre-down
    ex, ey = pts[-1]
    sx, sy = 0.0, -0.30           # stem bottom
    ns = N - nh
    for i in range(1, ns + 1):
        t = i / ns
        # quadratic bezier: end of hook -> control (0,-0.5) -> stem bottom
        c = (0.0, -0.46)
        x = (1 - t) ** 2 * ex + 2 * (1 - t) * t * c[0] + t * t * sx
        y = (1 - t) ** 2 * ey + 2 * (1 - t) * t * c[1] + t * t * sy
        pts.append((x, y))
    return pts

def _resample(pts, n):
    d = [0.0]
    for i in range(1, len(pts)):
        d.append(d[-1] + math.dist(pts[i], pts[i - 1]))
    L = d[-1]; out = []; j = 0
    for k in range(n):
        s = L * k / (n - 1)
        while j < len(d) - 2 and d[j + 1] < s: j += 1
        t = (s - d[j]) / max(1e-9, d[j + 1] - d[j])
        out.append((pts[j][0] + (pts[j + 1][0] - pts[j][0]) * t, pts[j][1] + (pts[j + 1][1] - pts[j][1]) * t))
    return out, L

Q, QLEN = _resample(_q_points(), N)
# '!' target: vertical line from top to stem bottom (same start ordering: top first)
EX = [(0.0, -1.02 + (0.72) * k / (N - 1)) for k in range(N)]

def ease(t):
    t = max(0.0, min(1.0, t)); return t * t * (3 - 2 * t)

def draw(ctx, x, y, size, tilt=0, sq=1.0, eye='open', look=(0, 0), brow=0, morph=0.0, glow=0.6, alpha=1.0,
         stroke=0.155, color=CREAM):
    """x,y = position of dot centre (feet). size = pixel height of the glyph."""
    m = ease(morph)
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(math.radians(tilt))
    ctx.scale(size / sq ** 0.5, size * sq)
    pts = [(a[0] + (b[0] - a[0]) * m, a[1] + (b[1] - a[1]) * m) for a, b in zip(Q, EX)]
    # glow under dot
    if glow > 0:
        g = cairo.RadialGradient(0, 0, 0, 0, 0, 0.32)
        g.add_color_stop_rgba(0, *AMBER, 0.55 * glow * alpha)
        g.add_color_stop_rgba(1, *AMBER, 0)
        ctx.set_source(g); ctx.arc(0, 0, 0.32, 0, 2 * math.pi); ctx.fill()
    # stroke (shadow then body)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.set_line_width(stroke)
    ctx.move_to(*pts[0])
    for p in pts[1:]: ctx.line_to(*p)
    ctx.set_source_rgba(*color, alpha); ctx.stroke()
    # amber dot
    ctx.arc(0, 0, stroke * 0.62, 0, 2 * math.pi); ctx.set_source_rgba(*AMBER, alpha); ctx.fill()
    # eye: sits on the hook top-right (path index ~ 30), fades into the bar of '!' gracefully
    k = 34
    ex, ey = pts[k]
    _eye(ctx, ex, ey, stroke, eye, look, brow, alpha)
    ctx.restore()

def _eye(ctx, ex, ey, s, kind, look, brow, alpha):
    r = s * 0.36
    ctx.save(); ctx.translate(ex, ey)
    if kind == 'happy':
        ctx.set_line_width(s * 0.13); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.arc(0, r * 0.35, r * 0.8, math.radians(200), math.radians(340))
        ctx.set_source_rgba(*INK, alpha); ctx.stroke()
    elif kind == 'blink':
        ctx.set_line_width(s * 0.12); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.move_to(-r * 0.8, 0); ctx.line_to(r * 0.8, 0)
        ctx.set_source_rgba(*INK, alpha); ctx.stroke()
    else:
        ry = {'open': 1.0, 'wide': 1.25, 'squint': 0.45}[kind]
        rx = {'open': 0.8, 'wide': 0.95, 'squint': 0.85}[kind]
        ctx.save(); ctx.scale(rx, ry); ctx.arc(0, 0, r, 0, 2 * math.pi); ctx.restore()
        ctx.set_source_rgba(*INK, alpha); ctx.fill()
        # highlight, shifted opposite the look direction
        hx = r * (0.28 - 0.18 * look[0]); hy = -r * (0.35 + 0.15 * look[1])
        ctx.arc(hx + look[0] * r * 0.25, hy + look[1] * r * 0.25, r * 0.22, 0, 2 * math.pi)
        ctx.set_source_rgba(*CREAM, alpha); ctx.fill()
    if brow:
        ctx.set_line_width(s * 0.11); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        by = -r * (1.75 + 0.35 * max(0, brow))
        tiltb = -0.35 * brow if brow < 0 else 0.0
        ctx.move_to(-r * 0.9, by + r * tiltb); ctx.line_to(r * 0.9, by - r * tiltb)
        ctx.set_source_rgba(*INK, alpha); ctx.stroke()
    ctx.restore()

# named poses used by the script cues
POSES = {
    'idle':     dict(tilt=0,   sq=1.0,  eye='open',  look=(0, 0),     brow=0),
    'curious':  dict(tilt=-14, sq=1.0,  eye='open',  look=(0.6, -0.3), brow=0.6),
    'shocked':  dict(tilt=0,   sq=1.18, eye='wide',  look=(0, -0.2),  brow=1.0),
    'thinking': dict(tilt=10,  sq=0.97, eye='squint', look=(0.5, -0.6), brow=-0.6),
    'point_r':  dict(tilt=16,  sq=1.02, eye='open',  look=(1, 0.1),   brow=0.3),
    'point_l':  dict(tilt=-16, sq=1.02, eye='open',  look=(-1, 0.1),  brow=0.3),
    'happy':    dict(tilt=4,   sq=1.04, eye='happy', look=(0, 0),     brow=0),
}
