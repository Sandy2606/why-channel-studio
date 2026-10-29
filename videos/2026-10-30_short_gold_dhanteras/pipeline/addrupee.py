from fontTools.ttLib import TTFont
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.transformPen import TransformPen
def add(dst_path, src_path, out_path, embolden=0):
    d = TTFont(dst_path); s = TTFont(src_path)
    sn = s.getBestCmap()[0x20B9]; sc = d['head'].unitsPerEm / s['head'].unitsPerEm
    gs = s.getGlyphSet(); pen = TTGlyphPen(None)
    # match digit height: scale by ratio of '1' heights
    def h(f, gsx):
        g = f['glyf'][f.getBestCmap()[ord('1')]]; return g.yMax
    k = h(d, None) / h(s, None)
    adv_s = s['hmtx'][sn][0]; tp = TransformPen(pen, (k, 0, 0, k, 0, 0))
    gs[sn].draw(tp); g = pen.glyph()
    name = 'uni20B9'
    d['glyf'][name] = g; d.setGlyphOrder(d.getGlyphOrder() + [name]) if name not in d.getGlyphOrder() else None
    mono = d['post'].isFixedPitch
    adv = d['hmtx'][d.getBestCmap()[ord('1')]][0] if mono else int(adv_s * k)
    g.recalcBounds(d['glyf'])
    lsb = g.xMin if hasattr(g, 'xMin') else 0
    if mono:  # center in cell
        from fontTools.pens.recordingPen import RecordingPen
        w = g.xMax - g.xMin; dx = (adv - w) / 2 - g.xMin
        pen = TTGlyphPen(None); gs[sn].draw(TransformPen(pen, (k, 0, 0, k, dx, 0))); g = pen.glyph(); d['glyf'][name] = g; g.recalcBounds(d['glyf'])
    d['hmtx'][name] = (adv, g.xMin)
    for t in d['cmap'].tables:
        if t.isUnicode(): t.cmap[0x20B9] = name
    d['maxp'].numGlyphs = len(d.getGlyphOrder())
    d.save(out_path); print('ok', out_path)
O = '/root/fonts_orig/'
add(O + 'ArchivoBlack-Regular.ttf', '/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf', '/root/.fonts/ArchivoBlack-Regular.ttf')
add(O + 'SpaceMono-Bold.ttf', '/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf', '/root/.fonts/SpaceMono-Bold.ttf')
add(O + 'SpaceMono-Regular.ttf', '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', '/root/.fonts/SpaceMono-Regular.ttf')
