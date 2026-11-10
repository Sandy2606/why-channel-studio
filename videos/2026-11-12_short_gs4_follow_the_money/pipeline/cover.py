"""GS 4/6 covers 1080x1920: full-bleed Akbarnama (never enlarged), uniform grade (no masked band), key text inside the IG 1080x1350 crop."""
import sys, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W, H = 1080, 1920; B = '/home/claude/why-channel-studio/brand/fonts/'
F_ARCH = lambda s: ImageFont.truetype(B + 'ArchivoBlack-Regular.ttf', s)
F_MONO = lambda s: ImageFont.truetype(B + 'SpaceMono-Bold.ttf', s)
def F_TE(s):
    f = ImageFont.truetype(B + 'NotoSansTelugu.ttf', s, layout_engine=ImageFont.Layout.RAQM); f.set_variation_by_name('Black'); return f
lang, plat = sys.argv[1], sys.argv[2]
src = Image.open('/home/claude/why-channel-studio/videos/2026-11-08_long_golden_sparrow_s1/visuals/archive/20_PD08_Abul_Fazl_presenting_Akbarnama.jpg').convert('RGB')
sc = max(W / src.width, H / src.height); assert sc <= 1.0
cw, ch = W / sc, H / sc; cx, cy = src.width * .5, src.height * .40
box = (cx - cw / 2, max(0, cy - ch / 2), cx + cw / 2, max(0, cy - ch / 2) + ch)
img = src.resize((W, H), Image.LANCZOS, box=box)
a = np.asarray(img).astype(np.float32)
yy = np.linspace(0, 1, H)[:, None, None]; v = 0.50 + 0.10 * np.cos((yy - .45) * 3.0)   # even, gentle darkening across the whole frame
a = a * v; fr = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert('RGBA')
def shadow_text(xy, s, font, fill, anchor='mm', sh=12):
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(lay).text(xy, s, font=font, fill=(0, 0, 0, 240), anchor=anchor)
    fr.alpha_composite(lay.filter(ImageFilter.GaussianBlur(sh))); ImageDraw.Draw(fr).text(xy, s, font=font, fill=fill, anchor=anchor)
def gold_text(xy, s, font, anchor='mm'):
    lay = Image.new('L', (W, H), 0); ImageDraw.Draw(lay).text(xy, s, font=font, fill=255, anchor=anchor)
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sh.putalpha(lay.filter(ImageFilter.GaussianBlur(12)).point(lambda x: int(x * .95))); fr.alpha_composite(sh)
    g = np.zeros((H, W, 4), np.uint8); t = (np.linspace(0, 1, H)[:, None] * np.ones((1, W)))[..., None]
    g[..., :3] = (np.array([255, 214, 120]) * (1 - (t * 1.7).clip(0, 1)) + np.array([255, 178, 36]) * (t * 1.7).clip(0, 1)).astype(np.uint8); g[..., 3] = np.asarray(lay)
    fr.alpha_composite(Image.fromarray(g, 'RGBA'))
d = ImageDraw.Draw(fr)
if lang == 'en':
    shadow_text((W // 2, 760), "INDIA MADE ~1/4 OF THE WORLD'S OUTPUT", F_MONO(34), (244, 241, 234))
    gold_text((W // 2, 935), 'WHO GOT', F_ARCH(140)); gold_text((W // 2, 1100), 'THE MONEY?', F_ARCH(118))
    shadow_text((W // 2, 1290), 'FOLLOW IT · FARMER TO KING', F_MONO(34), (244, 241, 234))
else:
    shadow_text((W // 2, 760), 'ప్రపంచ ఉత్పత్తిలో ~1/4 మనదే', F_TE(46), (244, 241, 234))
    gold_text((W // 2, 950), 'ఆ డబ్బంతా', F_TE(150)); gold_text((W // 2, 1140), 'ఎవరికి?', F_TE(150))
    shadow_text((W // 2, 1310), 'రైతు నుంచి రాజు వరకు', F_TE(48), (244, 241, 234))
# brand mark + series badge (same badge rules as the video: fill inside border, ink-centred text)
fw = F_ARCH(54); x0 = 80; d.text((x0, 320), 'WHY', font=fw, fill=(255, 255, 255)); d.text((x0 + d.textlength('WHY', font=fw), 320), '?', font=fw, fill=(255, 178, 36))
pill = 'GOLDEN SPARROW · 4/6' if lang == 'en' else 'బంగారు పిచ్చుక · 4/6'; f = F_MONO(30) if lang == 'en' else F_TE(32)
l, t, r, b = f.getbbox(pill, anchor='ls'); tw = r - l; hgt = 62; x1 = W - 80; xL = x1 - tw - 56; yT = 322
d.rounded_rectangle((xL, yT, x1, yT + hgt), 31, fill=(88, 70, 30)); d.rounded_rectangle((xL + 3, yT + 3, x1 - 3, yT + hgt - 3), 28, fill=(10, 10, 10))
d.text((xL + 28 - l, yT + hgt / 2 - (t + b) / 2), pill, font=f, fill=(255, 178, 36), anchor='ls')
img = fr.convert('RGB')
if plat == 'ig':
    d2 = ImageDraw.Draw(img); s = 'FULL FILM ON YOUTUBE' if lang == 'en' else 'పూర్తి సినిమా YouTube లో'; f2 = F_MONO(30) if lang == 'en' else F_TE(32)
    l, t, r, b = f2.getbbox(s, anchor='ls'); tw = r - l; xL = W / 2 - tw / 2 - 30; yT = 1640
    d2.rounded_rectangle((xL, yT, W / 2 + tw / 2 + 30, yT + 60), 30, fill=(255, 178, 36)); d2.text((W / 2 - tw / 2 - l, yT + 30 - (t + b) / 2), s, font=f2, fill=(10, 10, 10), anchor='ls')
out = f'/home/claude/why-channel-studio/videos/2026-11-12_short_gs4_follow_the_money/cover_GS4_{lang.upper()}_{plat.upper()}.jpg'
img.save(out, quality=93); print(out)
