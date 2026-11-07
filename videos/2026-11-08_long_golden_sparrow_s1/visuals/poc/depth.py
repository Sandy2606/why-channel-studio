import sys, numpy as np, onnxruntime as ort
from PIL import Image
S = ort.InferenceSession('/home/claude/gs/poc/models/depth_small.onnx')
def depth(path, out):
    im = Image.open(path).convert('RGB'); w, h = im.size
    th = 518; tw = int(round(w / h * th / 14)) * 14
    x = np.asarray(im.resize((tw, th), Image.BICUBIC)).astype(np.float32) / 255
    x = (x - [0.485, 0.456, 0.406]) / [0.229, 0.224, 0.225]
    d = S.run(None, {'pixel_values': x.transpose(2, 0, 1)[None].astype(np.float32)})[0][0]
    d = (d - d.min()) / (d.max() - d.min() + 1e-6)          # 1 = near
    Image.fromarray((d * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC).save(out)
V = '/home/claude/why-channel-studio/videos/2026-11-08_long_golden_sparrow_s1/visuals/test_batch/'
for n in sys.argv[1:]: depth(V + n + '.png', f'/home/claude/gs/poc/{n}_depth.png'); print(n)
