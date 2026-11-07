"""Stylised South Asia map: official India outline (svg-maps, MIT) + neighbours from countries.geojson, fitted to one Mercator frame."""
import json, math
from PIL import Image, ImageDraw
IND = json.load(open('/home/claude/gs/vis/src/india_official.json'))
GEO = json.load(open('/home/claude/why-channel-studio/pipeline/lib/countries.geojson'))
def my(lat): return math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))
# fit svg px <- (lon, mercY): x extremes Gujarat W 68.11E -> 0, Arunachal E 97.40E -> 611.86 ; y extremes official top 37.08N -> 0, Indira Pt 6.75N -> 695.7
AX = 611.86 / (97.40 - 68.11); BX = -68.11 * AX
AY = 695.7 / (my(6.75) - my(37.08)); BY = -my(37.08) * AY
def to_svg(lon, lat): return (AX * lon + BX, AY * my(lat) + BY)
def polys(name):
    for f in GEO['features']:
        if f['properties']['name'] == name:
            g = f['geometry']; cs = g['coordinates'] if g['type'] == 'MultiPolygon' else [g['coordinates']]
            for p in cs:
                yield [to_svg(*pt) for pt in p[0]]
def india_polys():
    for v in IND.values():
        for p in v: yield [tuple(q) for q in p]
NEIGH = ['Pakistan', 'Bangladesh', 'Afghanistan', 'Iran', 'China', 'Nepal', 'Bhutan', 'Myanmar', 'Sri Lanka', 'Tajikistan', 'Turkmenistan', 'Uzbekistan', 'Oman', 'Thailand', 'Laos', 'Kyrgyzstan']
def render(view, size, style):
    """view = (x0, y0, x1, y1) in svg px; style: dict name->(fill, outline) with keys 'IND','PAK','BGD','other','sea'."""
    W, H = size; x0, y0, x1, y1 = view; s = min(W / (x1 - x0), H / (y1 - y0))
    ox = (W - (x1 - x0) * s) / 2 - x0 * s; oy = (H - (y1 - y0) * s) / 2 - y0 * s
    T = lambda p: [(x * s + ox, y * s + oy) for x, y in p]
    im = Image.new('RGBA', (W, H), style['sea']); d = ImageDraw.Draw(im)
    for n in NEIGH:
        key = {'Pakistan': 'PAK', 'Bangladesh': 'BGD'}.get(n, 'other')
        for p in polys(n):
            if len(p) > 2: d.polygon(T(p), fill=style[key][0], outline=style[key][1])
    for p in india_polys():
        if len(p) > 2: d.polygon(T(p), fill=style['IND'][0])
    # outer edge only (no state borders): edge of the India mask
    from PIL import ImageFilter, ImageChops
    m = Image.new('L', (W, H), 0); md = ImageDraw.Draw(m)
    for p in india_polys():
        if len(p) > 2: md.polygon(T(p), fill=255)
    edge = ImageChops.subtract(m.filter(ImageFilter.MaxFilter(3)), m)
    im.paste(style['IND'][1], (0, 0), edge)
    return im, (s, ox, oy)
if __name__ == '__main__':
    st = dict(sea=(18, 20, 34, 255), other=((48, 46, 58, 255), (70, 68, 82, 255)), PAK=((90, 160, 90, 255), (200, 255, 200, 255)),
              BGD=((90, 160, 90, 255), (200, 255, 200, 255)), IND=((200, 150, 40, 255), (255, 230, 160, 255)))
    im, _ = render((-260, -60, 760, 740), (1200, 940), st); im.save('/tmp/claude-0/mapfit.png')
