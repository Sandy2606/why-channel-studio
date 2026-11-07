"""Golden Sparrow film engine: assets, stills (Ken Burns + depth parallax), maps, cards, overlays."""
import os, sys, json, math, re, functools, subprocess
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter
VIS = '/home/claude/why-channel-studio/videos/2026-11-08_long_golden_sparrow_s1/visuals/'
CACHE = '/home/claude/gs/film/cache/'; os.makedirs(CACHE, exist_ok=True)
F = '/home/claude/gs/vis/fonts/'; RAQM = ImageFont.Layout.RAQM
W, H, FPS = 1920, 1080, 30
INK = (13, 12, 18); PAPER = (240, 232, 214); MUTED = (160, 155, 170); GOLD = (228, 178, 72); RUST = (186, 84, 60); TEAL = (88, 168, 160)
LANG = 'en'
def set_lang(l):
    global LANG; LANG = l

# ---------------------------------------------------------------- assets
ARC = VIS + 'archive/'
A = {
 'T1': VIS + 'test_batch/T1_chatgpt_v1.png', 'T2': VIS + 'test_batch/T2_chatgpt_v1.png', 'T3': VIS + 'test_batch/T3_chatgpt_v1.png',
 'T4': VIS + 'test_batch/T4_chatgpt_v1.png', 'T5': VIS + 'test_batch/T5_chatgpt_v1.png', 'T6': VIS + 'test_batch/T6_chatgpt_v2.png',
 'T7': VIS + 'test_batch/T7_chatgpt_v1.png', 'T8': VIS + 'test_batch/T8_chatgpt_v2.png',
 'MET1': VIS + 'source/met_1982_66.jpg',
 'PD10': ARC + '01_PD10_Cantino_planisphere_(1502).jpg', 'PD17': ARC + '02_PD17_Shah_Alam_conveying_the_grant_of_the_Diwani_to_Lord_Clive.jpg',
 'PD12': ARC + '03_PD12_Coat_of_arms_of_the_East_India_Company.svg', 'PD02': ARC + '04_PD02_Diamonds_and_precious_stones_-_Tavernier_Jean_Baptiste_-_1703.jpg',
 'PD16': ARC + '05_PD16_A_Perspective_View_of_Fort_William_by_Jan_Van_Ryne_1754.jpg', 'PD14': ARC + '06_PD14_Fort_of_St.George_on_the_Coromandel_Coast_by_Jan_van_Ryne.jpg',
 'PD15': ARC + '07_PD15_A_Front_View_of_the_East_India_House_in_Leadenhall_Street.jpg', 'FARMAN': ARC + '08_NEW_Farman_of_Aurangzeb_National_Museum_New_Delhi_62.5.jpg',
 'PD11': ARC + '09_PD11_Roteiro_da_primeira_viagem_de_Vasco_da_Gama.jpg', 'PD18a': ARC + '10_PD18a_Silver_Rupee_Aurangzeb_Surat_AH1109.jpg',
 'PD18b': ARC + '11_PD18b_Pagoda_or_Varaha_coins_of_Southern_India_Pl_II.jpg', 'PD19': ARC + '12_PD19_Gold_Aureus_of_Nerva_MANTIS.jpg',
 'PD07': ARC + '13_PD07_Vedanta_manuscript_Telugu_script.jpg', 'PD09': ARC + '14_PD09_Mundy_famine_p236.jpg', 'PD03': ARC + '15_PD03_Calico_Act_Cap_VII.jpg',
 'PD06': ARC + '16_PD06_Masulipatnam_Rijksmuseum.jpg', 'PD01': ARC + '17alt_Indus_carnelian_bead_Nippur.jpg', 'PD04': ARC + '18_PD04_Dress_chintz_robe_a_langlaise.jpg',
 'PD13': ARC + '19_PD13_Jahangir_Darbar_David_Collection.jpg', 'PD08': ARC + '20_PD08_Abul_Fazl_presenting_Akbarnama.jpg',
 'PD20a': ARC + '21a_PD20_Chintz_wall_panel_MET.jpg', 'PD20b': ARC + '21b_PD20_Textile_panel_chintz_MET.jpg', 'PD20c': ARC + '21c_PD20_Chintz_palampore_India_18c.jpg',
 'CC01': ARC + '22_CC01_Golconda_Fort_sunset.jpg', 'CC02': ARC + '23_CC02_Qutb_Shahi_Tombs.jpg', 'CC03': ARC + '24a_CC03_Hampi_Vittala_Temple.jpg',
 'CC06': ARC + '25_CC06_Kalamkari.jpg', 'CC04': ARC + '26_CC04_Cracked_dry_earth_Pexels_9692860.jpg', 'CC05': ARC + '27_CC05_Storm_clouds_over_sea_Pexels_9712998.jpg',
}
for g in range(1, 31):
    k = f'G{g:02d}'
    for v in ('v3', 'v2', 'v1'):
        p = VIS + f'pack2/{k}_{v}.png'
        if os.path.exists(p): A[k] = p; break
CROP = {  # source-pixel crops (x0, y0, x1, y1)
 'PD18a': (1037, 933, 2557, 2453), 'PD18b': (1080, 890, 1900, 1320), 'FARMAN': (0, 0, 815, 1390), 'PD14': (0, 0, 705, 468),
 'PD10': (0, 0, 10643, 4998),
}
CIRCLE = {'PD18a', 'PD19'}
ILLUS = {k for k in A if k[0] in 'TG'}          # own illustrations -> parallax + DRAMATIZED tag

def grade(a):
    a = a.astype(np.float32) / 255; a = 0.03 + 0.95 * a; a = a ** np.array([0.98, 1.0, 1.06], np.float32)
    l = a.mean(2, keepdims=True); a = l + (a - l) * 0.93
    return (np.clip(a, 0, 1) * 255).astype(np.uint8)

@functools.lru_cache(maxsize=12)
def img(key):
    """graded RGB uint8, at least ~1.35x frame cover size"""
    cp = CACHE + key + '.png'
    if os.path.exists(cp): return np.asarray(Image.open(cp).convert('RGB'))
    p = A[key]
    if p.endswith('.svg'):
        if not os.path.exists(CACHE + key + '_svg.png'):
            import cairosvg; cairosvg.svg2png(url=p, write_to=CACHE + key + '_svg.png', output_width=1800)
        im = Image.open(CACHE + key + '_svg.png').convert('RGBA'); bg = Image.new('RGBA', im.size, (232, 222, 200, 255)); bg.alpha_composite(im); im = bg.convert('RGB')
    else:
        im = Image.open(p).convert('RGB')
    if key in CROP: im = im.crop(CROP[key])
    if key in CIRCLE:
        m = Image.new('L', im.size, 0); ImageDraw.Draw(m).ellipse((8, 8, im.width - 8, im.height - 8), fill=255)
        bg = Image.new('RGB', im.size, (22, 20, 28)); bg.paste(im, (0, 0), m.filter(ImageFilter.GaussianBlur(3))); im = bg
    s = max(W * 1.4 / im.width, H * 1.4 / im.height)
    if s > 1: im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS).filter(ImageFilter.UnsharpMask(2, 50, 2))
    elif max(im.size) > 3600:
        r = 3600 / max(im.size); im = im.resize((int(im.width * r), int(im.height * r)), Image.LANCZOS)
    a = grade(np.asarray(im)); Image.fromarray(a).save(cp)
    return a

DEPTH = None
@functools.lru_cache(maxsize=12)
def depth(key):
    cp = CACHE + key + '_d.png'
    a = img(key); h, w = a.shape[:2]
    if not os.path.exists(cp):
        global DEPTH
        import onnxruntime as ort
        if DEPTH is None: DEPTH = ort.InferenceSession('/home/claude/gs/poc/models/depth_small.onnx')
        th = 518; tw = int(round(w / h * th / 14)) * 14
        x = cv2.resize(a, (tw, th), interpolation=cv2.INTER_AREA).astype(np.float32) / 255
        x = (x - [0.485, 0.456, 0.406]) / [0.229, 0.224, 0.225]
        d = DEPTH.run(None, {'pixel_values': x.transpose(2, 0, 1)[None].astype(np.float32)})[0][0]
        d = (d - d.min()) / (d.max() - d.min() + 1e-6)
        Image.fromarray((d * 255).astype(np.uint8)).save(cp)
    d = np.asarray(Image.open(cp).convert('L')).astype(np.float32) / 255
    d = cv2.resize(d, (w, h), interpolation=cv2.INTER_LINEAR); return cv2.GaussianBlur(d, (0, 0), 4)

@functools.lru_cache(maxsize=12)
def blurfill(key):
    a = img(key); s = max(W / a.shape[1], H / a.shape[0]) * 1.1
    b = cv2.resize(a, (int(a.shape[1] * s), int(a.shape[0] * s)), interpolation=cv2.INTER_AREA)
    y0 = (b.shape[0] - H) // 2; x0 = (b.shape[1] - W) // 2; b = b[y0:y0 + H, x0:x0 + W]
    return (cv2.GaussianBlur(b, (0, 0), 30) * 0.42).astype(np.uint8)

GX, GY = np.meshgrid(np.arange(W, dtype=np.float32), np.arange(H, dtype=np.float32))
def still(key, u, z0, z1, fx0, fy0, fx1, fy1, par=0.0, fit=False):
    """u in [0,1]. z: 1 = cover. fit=True: contain (whole image visible) on a blurred fill."""
    a = img(key); h, w = a.shape[:2]
    e = u * u * (3 - 2 * u) * 0.8 + u * 0.2
    base = min(W / w, H / h) if fit else max(W / w, H / h)
    s = base * (z0 + (z1 - z0) * e); fx = fx0 + (fx1 - fx0) * e; fy = fy0 + (fy1 - fy0) * e
    hw, hh = W / 2 / s, H / 2 / s
    cx = fx * w if w * s < W else min(max(fx * w, hw), w - hw)
    cy = fy * h if h * s < H else min(max(fy * h, hh), h - hh)
    if par > 0 and key in ILLUS:
        d = depth(key)
        sx = cx + (GX - W / 2) / s; sy = cy + (GY - H / 2) / s
        dd = cv2.remap(d, sx, sy, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
        k = 1 + par * e * (dd - 0.5) * 2
        out = cv2.remap(a, cx + (GX - W / 2) / (s * k), cy + (GY - H / 2) / (s * k), cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
        return out
    M = np.float32([[s, 0, W / 2 - cx * s], [0, s, H / 2 - cy * s]])
    if w * s < W - 2 or h * s < H - 2:
        out = blurfill(key).copy()
        cv2.warpAffine(a, M, (W, H), dst=out, flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_TRANSPARENT)
        return out
    return cv2.warpAffine(a, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)

# ---------------------------------------------------------------- text
@functools.lru_cache(None)
def font(kind, size):
    size = int(size)
    if LANG == 'te' and kind in ('ui', 'label', 'small', 'disp'):
        return ImageFont.truetype(F + {'disp': 'NotoSerifTelugu-700', 'ui': 'NotoSerifTelugu-600', 'label': 'NotoSerifTelugu-600', 'small': 'NotoSerifTelugu-400'}[kind] + '.ttf', int(size * 0.92), layout_engine=RAQM)
    return ImageFont.truetype(F + {'num': 'Cinzel-700', 'disp': 'Cinzel-700', 'ui': 'SourceSans3-600', 'label': 'SourceSans3-700', 'small': 'SourceSans3-400'}[kind] + '.ttf', size, layout_engine=RAQM)
def has_te(s): return any('ఀ' <= c <= '౿' for c in s)
@functools.lru_cache(maxsize=512)
def text(s, kind, size, fill=PAPER, glow=False, maxw=None):
    s = s.replace('→', '›').replace('←', '‹').replace('₹', 'RS ' if not has_te(s) else 'రూ. ').replace('≈', '~')
    if has_te(s) and kind in ('num',): kind = 'disp'
    f = font(kind, size); maxw = maxw or W - 200
    words = s.split(' '); lines = []; cur = ''
    for wd in words:
        t = (cur + ' ' + wd).strip()
        if f.getlength(t) > maxw and cur: lines.append(cur); cur = wd
        else: cur = t
    lines.append(cur)
    asc, desc = f.getmetrics(); lh = int((asc + desc) * 1.08)
    tw = int(max(f.getlength(l) for l in lines)) + 8; th = lh * len(lines) + 8
    pad = 30 if glow else 0
    im = Image.new('RGBA', (tw + 2 * pad, th + 2 * pad), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for i, l in enumerate(lines): d.text((pad + 2, pad + 2 + i * lh), l, font=f, fill=tuple(fill) + (255,))
    if glow:
        g = im.filter(ImageFilter.GaussianBlur(12)); a = g.split()[3].point(lambda v: int(v * 0.65))
        gl = Image.new('RGBA', im.size, tuple(fill) + (0,)); gl.putalpha(a); gl.alpha_composite(im); im = gl
    return im
def put(fr, im, x, y, a=1.0, anchor='lt', dy=0.0):
    if a <= 0.01: return
    if anchor[0] == 'c': x -= im.width / 2
    if anchor[0] == 'r': x -= im.width
    if anchor[1] == 'c': y -= im.height / 2
    if anchor[1] == 'b': y -= im.height
    if a < 0.999: im = im.copy(); im.putalpha(im.split()[3].point(lambda v: int(v * a)))
    fr.alpha_composite(im, (int(x), int(y + dy)))
def eo(x): x = min(max(x, 0), 1); return 1 - (1 - x) ** 3
def win(t, a, b, fi=0.4, fo=0.4):
    if t < a or t > b: return 0.0
    return min(1.0, (t - a) / fi if fi else 1, (b - t) / fo if fo else 1)
def shade(fr, box, alpha=150, blur=40):
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).rectangle(box, fill=(0, 0, 0, alpha))
    fr.alpha_composite(sh.filter(ImageFilter.GaussianBlur(blur)))
def chip(fr, t, a, b, s, x=70, y=None, size=34, color=PAPER, anchor='lb', maxw=1150, kind='label'):
    """lower-third: gold rule + text, enters with a small rise"""
    if not s or t < a or t > b: return
    y = H - 90 if y is None else y
    k = eo((t - a) / 0.5) * min(1.0, (b - t) / 0.4); dy = (1 - eo((t - a) / 0.5)) * 16
    im = text(s, kind, size, color, maxw=maxw)
    yy = y - im.height if anchor[1] == 'b' else y
    shade(fr, (x - 50, yy - 45, x + im.width + 50, yy + im.height + 35), int(190 * k), 30)
    bg = Image.new('RGBA', fr.size, (0, 0, 0, 0)); ImageDraw.Draw(bg).rounded_rectangle((x - 24, yy - 30 + dy, x + im.width + 24, yy + im.height + 16 + dy), 10, fill=INK + (int(170 * k),))
    fr.alpha_composite(bg)
    d = ImageDraw.Draw(fr); d.rectangle((x, yy - 14 + dy, x + int(70 * k), yy - 11 + dy), fill=GOLD + (int(255 * k),))
    put(fr, im, x, yy, k, 'lt', dy)

# ---------------------------------------------------------------- maps (Mercator, rendered once per shot)
GEO = json.load(open('/home/claude/why-channel-studio/pipeline/lib/countries.geojson'))
sys.path.insert(0, '/home/claude/gs/vis'); import gsmap
def merc(lat): return math.degrees(math.log(math.tan(math.pi / 4 + math.radians(lat) / 2)))
def svg2ll(x, y): return gsmap.svg2ll(x, y) if hasattr(gsmap, 'svg2ll') else ((x - gsmap.BX) / gsmap.AX, math.degrees(2 * math.atan(math.exp((y - gsmap.BY) / gsmap.AY)) - math.pi / 2))
_IND = None
def india_ll():
    global _IND
    if _IND is None: _IND = [[svg2ll(x, y) for x, y in p] for p in gsmap.india_polys()]
    return _IND
def country_polys(skip=('India',)):
    for f in GEO['features']:
        if f['properties']['name'] in skip: continue
        g = f['geometry']; cs = g['coordinates'] if g['type'] == 'MultiPolygon' else [g['coordinates']]
        for p in cs: yield f['properties']['name'], p[0]
SEA = (17, 19, 30); LANDC = (46, 44, 56); EDGE = (82, 79, 96)
@functools.lru_cache(maxsize=6)
def map_base(box, pxw, india_gold):
    """box = (lon0, lon1, lat0, lat1); returns (RGB array, projector)"""
    lon0, lon1, lat0, lat1 = box; top, bot = merc(lat1), merc(lat0)
    pxh = int(pxw * (top - bot) / (lon1 - lon0))
    P = lambda lon, lat: ((lon - lon0) / (lon1 - lon0) * pxw, (top - merc(min(max(lat, -84), 84))) / (top - bot) * pxh)
    im = Image.new('RGB', (pxw, pxh), SEA); d = ImageDraw.Draw(im)
    for lon in range(-180, 181, 10): d.line([P(lon, -80), P(lon, 80)], fill=(30, 31, 46), width=2)
    for lat in range(-80, 81, 10): d.line([P(-180, lat), P(180, lat)], fill=(30, 31, 46), width=2)
    for n, p in country_polys(): d.polygon([P(*q) for q in p], fill=LANDC, outline=EDGE)
    m = Image.new('L', (pxw, pxh), 0); md = ImageDraw.Draw(m)
    for p in india_ll(): md.polygon([P(*q) for q in p], fill=255)
    im.paste(GOLD if india_gold else LANDC, (0, 0), m)
    k = max(3, (pxw // 1400) * 2 + 1)
    edge = Image.fromarray(cv2.dilate(np.asarray(m), np.ones((k, k), np.uint8)) - np.asarray(m))
    im.paste((255, 226, 150) if india_gold else EDGE, (0, 0), edge)
    return np.asarray(im), P, pxw, pxh

TE_PLACE = {'Machilipatnam': 'మచిలీపట్నం', 'Golconda': 'గోల్కొండ', 'Kollur': 'కొల్లూరు', 'Srikalahasti': 'శ్రీకాళహస్తి', 'Pedana': 'పెడన', 'Palakollu': 'పాలకొల్లు',
 'Madras': 'మద్రాసు', 'Surat': 'సూరత్', 'Swally': 'స్వాలీ', 'Bombay': 'బొంబాయి', 'Calcutta': 'కలకత్తా', 'Plassey': 'ప్లాసీ', 'Buxar': 'బక్సర్', 'Calicut': 'కాలికట్',
 'Malindi': 'మాలిండి', 'Malacca': 'మలక్కా', 'Aden': 'ఏడెన్', 'Hormuz': 'హోర్ముజ్', 'Aceh': 'ఆచే', 'Arakan': 'అరకాన్', 'Venice': 'వెనిస్', 'Lisbon': 'లిస్బన్',
 'London': 'లండన్', 'Pondicherry': 'పాండిచ్చేరి', 'Talikota': 'తళ్లికోట', 'Vijayanagara': 'విజయనగరం', 'Penukonda': 'పెనుగొండ', 'Chandragiri': 'చంద్రగిరి',
 'Vellore': 'వెల్లూరు', 'Arcot': 'ఆర్కాట్', 'Hyderabad': 'హైదరాబాద్', 'Delhi': 'ఢిల్లీ', 'Agra': 'ఆగ్రా', 'Mehrgarh': 'మెహర్‌గఢ్', 'Dhaka': 'ఢాకా',
 'Isfahan': 'ఇస్ఫహాన్', 'Mocha': 'మోచా', 'Pegu': 'పెగూ', 'Panigiri': 'పణిగిరి', 'Cape of Good Hope': 'గుడ్ హోప్ అగ్రం', 'Bengal': 'బెంగాల్',
 'Persia': 'పర్షియా', 'Arabia': 'అరేబియా', 'Burma': 'బర్మా', 'Southeast Asia': 'ఆగ్నేయాసియా', 'West Africa': 'పశ్చిమ ఆఫ్రికా', 'Deccan sultanates': 'దక్కన్ సుల్తానులు',
 'Mughal empire': 'మొఘల్ సామ్రాజ్యం', 'Golconda kingdom': 'గోల్కొండ రాజ్యం', 'Northern Circars · French 1753': 'ఉత్తర సర్కారులు · ఫ్రెంచ్ 1753', 'Bengal · Bihar · Orissa': 'బెంగాల్ · బీహార్ · ఒరిస్సా',
 'Hyderabad (Nizam)': 'హైదరాబాద్ (నిజాం)', 'Arcot (Carnatic)': 'ఆర్కాట్ (కర్ణాటక)', 'Krishna': 'కృష్ణా', 'SW monsoon · summer': 'నైరుతి రుతుపవనాలు · వేసవి',
 'NE monsoon · winter': 'ఈశాన్య రుతుపవనాలు · చలికాలం', 'Indian Ocean': 'హిందూ మహాసముద్రం', 'Europe': 'యూరప్', 'Thames': 'థేమ్స్'}
def pl(name): return TE_PLACE.get(name, name) if LANG == 'te' else name.upper() if len(name) < 20 else name

def render_map(fr, t, spec, t0, t1):
    """spec: box0, box1 (lon0,lon1,lat0,lat1), pins[(name, lon, lat, cue)], routes[([(lon,lat)..], cue, color)],
       glows[(name, lon, lat, r_deg, color, cue)], arrows[...], gold (bool)"""
    b0, b1 = spec['box0'], spec.get('box1', spec['box0'])
    ub = (min(b0[0], b1[0]), max(b0[1], b1[1]), min(b0[2], b1[2]), max(b0[3], b1[3]))
    span = min(b0[1] - b0[0], b1[1] - b1[0]); pxw = int(min(9000, max(2600, W * 1.25 * (ub[1] - ub[0]) / span)))
    base, P, pw, ph = map_base(ub, pxw, spec.get('gold', False))
    u = min(max((t - t0) / max(0.1, t1 - t0), 0), 1); e = u * u * (3 - 2 * u)
    bx = [b0[i] + (b1[i] - b0[i]) * e for i in range(4)]
    x0, y0 = P(bx[0], bx[3]); x1, y1 = P(bx[1], bx[2])
    s = min(W / (x1 - x0), H / (y1 - y0)) if spec.get('contain') else max(W / (x1 - x0), H / (y1 - y0))
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    M = np.float32([[s, 0, W / 2 - cx * s], [0, s, H / 2 - cy * s]])
    a = cv2.warpAffine(base, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=SEA)
    out = Image.fromarray(a).convert('RGBA'); d = ImageDraw.Draw(out)
    V = lambda lon, lat: (P(lon, lat)[0] * s + M[0, 2], P(lon, lat)[1] * s + M[1, 2])
    for g in spec.get('glows', []):
        name, lon, lat, r, col, cue = g[:6]; k = eo((t - cue) / 0.9)
        if k <= 0: continue
        cxp, cyp = map(float, V(lon, lat)); rx = max(2.0, float(abs(V(lon + r, lat)[0] - cxp)))
        gl = Image.new('RGBA', (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(gl)
        gd.ellipse((cxp - rx, cyp - rx, cxp + rx, cyp + rx), fill=tuple(col) + (int(120 * k),))
        out.alpha_composite(gl.filter(ImageFilter.GaussianBlur(rx * 0.35)))
        if name: put(out, text(pl(name), 'label', 30, tuple(min(255, c + 60) for c in col)), cxp, cyp, k, 'cc')
    for rt in spec.get('routes', []):
        pts, cue, col = rt[0], rt[1], (rt[2] if len(rt) > 2 else GOLD)
        k = eo((t - cue) / 1.6)
        if k <= 0: continue
        vp = [V(*q) for q in pts]; segs = [math.dist(vp[i], vp[i + 1]) for i in range(len(vp) - 1)]; L = sum(segs) * k; acc = 0; draw = [vp[0]]
        for i, sg in enumerate(segs):
            if acc + sg <= L: draw.append(vp[i + 1]); acc += sg
            else:
                f = (L - acc) / sg; draw.append((vp[i][0] + (vp[i + 1][0] - vp[i][0]) * f, vp[i][1] + (vp[i + 1][1] - vp[i][1]) * f)); break
        d.line(draw, fill=tuple(col) + (230,), width=5, joint='curve')
        hx, hy = draw[-1]; d.ellipse((hx - 7, hy - 7, hx + 7, hy + 7), fill=tuple(col) + (255,))
    for pn in spec.get('pins', []):
        name, lon, lat, cue = pn[:4]; side = pn[4] if len(pn) > 4 else 'r'
        k = eo((t - cue) / 0.5)
        if k <= 0: continue
        x, y = V(lon, lat); r = 9 + 22 * (1 - eo((t - cue) / 0.8))
        d.ellipse((x - 9, y - 9, x + 9, y + 9), fill=GOLD + (int(255 * k),), outline=(30, 26, 20, int(255 * k)), width=2)
        if t - cue < 0.8: d.ellipse((x - r, y - r, x + r, y + r), outline=GOLD + (int(200 * (1 - eo((t - cue) / 0.8))),), width=3)
        lab = text(pl(name), 'label', 30, PAPER)
        if side == 'r': put(out, lab, x + 18, y, k, 'lc')
        elif side == 'l': put(out, lab, x - 18, y, k, 'rc')
        elif side == 'u': put(out, lab, x, y - 16, k, 'cb')
        else: put(out, lab, x, y + 16, k, 'ct')
    for sh in spec.get('ships', []):    # (pts origin->port, cue, dur): a ship sails in, leaving a wake
        pts, cue, dur = sh; k = (t - cue) / dur
        if k <= 0: continue
        kk = min(1.0, k); e_ = kk * kk * (3 - 2 * kk); al = 1.0 if k < 1.15 else max(0.0, 1 - (k - 1.15) / 0.3)
        if al <= 0: continue
        vp = [V(*q) for q in pts]; segs = [math.dist(vp[i], vp[i + 1]) for i in range(len(vp) - 1)]; tot = sum(segs)
        def at(L_):
            acc = 0
            for i, sg in enumerate(segs):
                if acc + sg >= L_: f = (L_ - acc) / sg; return (vp[i][0] + (vp[i + 1][0] - vp[i][0]) * f, vp[i][1] + (vp[i + 1][1] - vp[i][1]) * f)
                acc += sg
            return vp[-1]
        Lh = tot * e_; wake = [at(max(0, Lh - tot * 0.22 * (1 - j / 12))) for j in range(13)]
        for j in range(12): d.line([wake[j], wake[j + 1]], fill=(236, 226, 204, int(150 * al * j / 12)), width=3)
        x, y = at(Lh)
        d.polygon([(x - 20, y + 2), (x + 20, y + 2), (x + 13, y + 12), (x - 13, y + 12)], fill=(232, 214, 170, int(255 * al)), outline=(40, 30, 20, int(255 * al)))
        d.polygon([(x - 2, y - 30), (x - 2, y), (x - 18, y - 2)], fill=(250, 244, 228, int(255 * al)))
        d.polygon([(x + 2, y - 26), (x + 2, y), (x + 17, y - 3)], fill=(250, 244, 228, int(230 * al)))
        d.line((x, y - 34, x, y + 2), fill=(60, 44, 30, int(255 * al)), width=2)
    if spec.get('net'):                 # hub -> weaving villages
        hub, vil, cue, lab = spec['net']; hx, hy = V(*hub)
        for j, q in enumerate(vil):
            k = eo((t - cue - j * 0.12) / 0.45)
            if k <= 0: continue
            vx, vy = V(*q); ex_, ey_ = hx + (vx - hx) * k, hy + (vy - hy) * k
            d.line((hx, hy, ex_, ey_), fill=GOLD + (int(200 * k),), width=3)
            r_ = 7 + 10 * (1 - eo((t - cue - j * 0.12 - 0.45) / 0.5)) if k >= 1 else 0
            d.ellipse((vx - 7, vy - 7, vx + 7, vy + 7), fill=PAPER + (int(255 * k),))
            if r_ > 7: d.ellipse((vx - r_, vy - r_, vx + r_, vy + r_), outline=PAPER + (int(150 * k),), width=2)
        if lab:
            cxs = sum(V(*q)[0] for q in vil) / len(vil); cys = min(V(*q)[1] for q in vil)
            put(out, text(lab, 'label', 34, PAPER), cxs, cys - 40, eo((t - cue - 0.5) / 0.5), 'cb')
    for ar in spec.get('arrows', []):   # monsoon arrows: (lon0,lat0,lon1,lat1,cue,cue_off)
        lo0, la0, lo1, la1, cue, off = ar; k = win(t, cue, off, 0.6, 0.6)
        if k <= 0: continue
        p0, p1 = V(lo0, la0), V(lo1, la1); d.line([p0, p1], fill=(200, 220, 240, int(200 * k)), width=6)
        ang = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
        for sgn in (1, -1): d.line([p1, (p1[0] - 26 * math.cos(ang + sgn * 0.5), p1[1] - 26 * math.sin(ang + sgn * 0.5))], fill=(200, 220, 240, int(200 * k)), width=6)
    return out

# ---------------------------------------------------------------- finishing
rng = np.random.default_rng(3)
YY, XX = np.mgrid[0:H, 0:W]
VIG = (1 - 0.36 * (((XX - W / 2) / (W / 2)) ** 2 + ((YY - H / 2) / (H / 2)) ** 2) ** 1.4).clip(0.45, 1).astype(np.float32)[..., None]
GRAIN = [rng.normal(0, 2.4, (H, W, 1)).astype(np.float32) for _ in range(4)]
def finish(a, t):
    return np.clip(a.astype(np.float32) * VIG + GRAIN[int(t * FPS) % 4], 0, 255).astype(np.uint8)
