import sys, numpy as np
from PIL import Image
lang, asp = sys.argv[1], sys.argv[2]; sys.argv = ['x', lang, asp]
import render_test as R
picks = []
for k, label, fn in R.SEGS:
    shots, ovs, a, b = fn()
    for f in (0.15, 0.5, 0.85): picks.append(a + (b - a) * f)
M = R.M; picks += [R.phrases('0.1')[-1] + 0.4, M['0.4'][0] + 1.5, R.TL['title_hit'] + 1.5, M['1.4'][1] - 0.5, M['F1.3'][0] + 1]
segs = [fn() for _, _, fn in R.SEGS]
ims = []
for t in picks:
    for shots, ovs, a, b in segs:
        if a <= t < b: ims.append(Image.fromarray(R.frame_at(shots, ovs, t))); break
cols = 4 if asp == 'land' else 6; w = 480 if asp == 'land' else 270; h = int(w * R.H / R.W)
S = Image.new('RGB', (cols * w, ((len(ims) + cols - 1) // cols) * h))
for i, im in enumerate(ims): S.paste(im.resize((w, h)), ((i % cols) * w, (i // cols) * h))
S.save(f'/tmp/claude-0/stills_{lang}_{asp}.jpg', quality=85); print(len(ims))
