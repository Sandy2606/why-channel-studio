import subprocess, re, html, json
from PIL import Image
def words(pdf, pg):
    o = subprocess.run(['pdftotext','-bbox','-f',str(pg),'-l',str(pg),pdf,'-'],capture_output=True,text=True).stdout
    return [(float(a)*2.5,float(b)*2.5,float(c)*2.5,float(d)*2.5,html.unescape(w)) for a,b,c,d,w in re.findall(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">(.*?)</word>',o)]
def clip(pdf, pg, phrase, name, ctx_before=0, ctx_after=0, xpad=30, extra=None, ypad=5):
    ws = words(pdf, pg); toks = phrase.split(); n = len(toks)
    for i in range(len(ws)-n+1):
        if all(ws[i+k][4].strip('.,;:') == toks[k].strip('.,;:') for k in range(n)): break
    else: raise KeyError(phrase)
    seg = ws[i:i+n]
    lines = {}
    for w in ws: lines.setdefault(round(w[1]/12), []).append(w)
    keys = sorted(lines); segk = sorted({round(w[1]/12) for w in seg})
    a = keys.index(segk[0]) - ctx_before; b = keys.index(segk[-1]) + ctx_after
    sel = [w for k in keys[max(0,a):b+1] for w in lines[k]]
    x0 = min(w[0] for w in sel) - xpad; y0 = min(w[1] for w in sel) - ypad; x1 = max(w[2] for w in sel) + xpad; y1 = max(w[3] for w in sel) + ypad
    subprocess.run(['pdftoppm','-r','180','-f',str(pg),'-l',str(pg),'-png','-singlefile',pdf,'/tmp/b3pg'],check=True)
    im = Image.open('/tmp/b3pg.png').convert('RGB'); im.crop((int(x0),int(y0),int(x1),int(y1))).save(f'clip_{name}.png')
    hl = {}
    for w in seg: hl.setdefault(round(w[1]/12), []).append(w)
    if extra:
        toks = extra.split(); n2 = len(toks)
        for j in range(len(ws)-n2+1):
            if all(ws[j+k][4].strip('.,;:') == toks[k].strip('.,;:') for k in range(n2)): break
        seg2 = ws[j:j+n2]; ex = {}
        for w in seg2: ex.setdefault(round(w[1]/12), []).append(w)
        rects2 = [[int(min(q[0] for q in L)-x0), int(min(q[1] for q in L)-y0), int(max(q[2] for q in L)-x0), int(max(q[3] for q in L)-y0)] for k, L in sorted(ex.items())]
    else: rects2 = []
    rects = [[int(min(q[0] for q in L)-x0), int(min(q[1] for q in L)-y0), int(max(q[2] for q in L)-x0), int(max(q[3] for q in L)-y0)] for k, L in sorted(hl.items())]
    print(name, (int(x1-x0), int(y1-y0)), rects, rects2); return rects, rects2
CJ = {}
a, b = clip('src/imd.pdf', 1, '❖ Southwest monsoon has withdrawn from the entire country today, the 15th October, 2026.', 'imd', ctx_after=2, extra='Northeast monsoon rainfall activity has commenced over Tamil Nadu, Puducherry &amp; Karaikal, Coastal Andhra Pradesh, Rayalaseema,')
CJ['imd'] = {'hl': a, 'hl2': b}
a, _ = clip('src/sr.pdf', 1, 'The strong alkalinity (pH 12.4, 25 °C) of', 'sr_ph', ctx_after=1)
CJ['sr_ph'] = {'hl': a}
CJ['epa'] = {'hl': [[531,104,801,148],[0,154,596,199]]}
json.dump(CJ, open('clips.json','w'))
