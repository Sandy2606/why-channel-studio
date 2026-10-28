"""Build paper clippings from real print-to-PDF captures: crop regions found by text, highlight exact phrases."""
import re, subprocess, json, html
from PIL import Image
DPI = 300; S = DPI / 72.0
Z = '/home/claude/g4/z/'
_words = {}; _pages = {}

def words(pdf, page):
    k = (pdf, page)
    if k not in _words:
        out = subprocess.run(['pdftotext', '-bbox', '-f', str(page), '-l', str(page), Z + pdf, '/dev/stdout'], capture_output=True, text=True).stdout
        ws = []
        for m in re.finditer(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">(.*?)</word>', out):
            ws.append((float(m[1]), float(m[2]), float(m[3]), float(m[4]), html.unescape(m[5])))
        _words[k] = ws
    return _words[k]

def page_img(pdf, page):
    k = (pdf, page)
    if k not in _pages:
        base = f'/home/claude/g4/pg/hi_{pdf[:-4]}_{page}'
        subprocess.run(['pdftoppm', '-r', str(DPI), '-f', str(page), '-l', str(page), '-singlefile', '-png', Z + pdf, base], check=True)
        _pages[k] = Image.open(base + '.png').convert('RGB')
    return _pages[k]

def norm(w): return re.sub(r'[^\w$%.]', '', w.lower())

def find(pdf, page, phrase, nth=1):
    ws = words(pdf, page); tgt = [norm(t) for t in phrase.split()]; k = 0
    for i in range(len(ws) - len(tgt) + 1):
        if all(norm(ws[i + j][4]) == tgt[j] for j in range(len(tgt))):
            k += 1
            if k == nth: return ws[i:i + len(tgt)]
    raise KeyError(f'{pdf} p{page}: {phrase}')

def box(seq, pad=(6, 4)):
    return (min(w[0] for w in seq) - pad[0], min(w[1] for w in seq) - pad[1], max(w[2] for w in seq) + pad[0], max(w[3] for w in seq) + pad[1])

def line_rects(seq):
    """group a phrase's words into per-line rectangles (pts)."""
    lines = []
    for w in seq:
        if lines and abs(lines[-1][1] - w[1]) < 3: l = lines[-1]; lines[-1] = (l[0], l[1], max(l[2], w[2]), max(l[3], w[3]))
        else: lines.append((w[0], w[1], w[2], w[3]))
    return lines

def build(parts):
    """parts: list of (pdf, page, region_pts, [highlight phrases]). Returns stacked PIL image + highlight rects (px)."""
    crops = []; hls = []; y = 0; gap = 26
    for pdf, page, reg, hp in parts:
        im = page_img(pdf, page)
        x0, y0, x1, y1 = [int(v * S) for v in reg]
        crops.append((im.crop((x0, y0, x1, y1)), x0, y0))
    wmax = max(c[0].width for c in crops)
    out = Image.new('RGB', (wmax, sum(c[0].height for c in crops) + gap * (len(crops) - 1)), (250, 249, 245))
    for (c, x0, y0), (pdf, page, reg, hp) in zip(crops, parts):
        ox = (wmax - c.width) // 2; out.paste(c, (ox, y));
        for ph in hp:
            for (a, b, cc, d) in line_rects(find(pdf, page, ph)):
                hls.append((a * S - x0 + ox, b * S - y0 + y, cc * S - x0 + ox, d * S - y0 + y))
        y += c.height + gap
    return out, hls
