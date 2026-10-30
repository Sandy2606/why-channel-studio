import sys, os, json
os.environ.setdefault('LANGV', 'en')
sys.argv = [sys.argv[0]] + sys.argv[1:]
import render as R
names = sys.argv[1].split(',')
ts = []
for n in names:
    if n.startswith('@'): ts.append(float(n[1:]))
    else:
        f = 0.6
        if ':' in n: n, f = n.split(':'); f = float(f)
        ts.append(R.F(n, f))
from PIL import Image
import numpy as np
ims = []
for t in ts:
    s = R.frame(t); a = np.ndarray((R.H, R.W, 4), np.uint8, s.get_data())[:, :, [2, 1, 0]].copy(); ims.append(Image.fromarray(a))
cols = 3; tw, th = 640, 360; sheet = Image.new('RGB', (cols * tw, ((len(ims) + cols - 1) // cols) * th))
for i, im in enumerate(ims): sheet.paste(im.resize((tw, th)), ((i % cols) * tw, (i // cols) * th))
sheet.save(sys.argv[2], quality=88)
