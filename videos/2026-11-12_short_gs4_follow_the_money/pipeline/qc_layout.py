"""automated layout QC: renders every Nth frame in [a,b], runs layout.check(), writes a defect log"""
import sys, os, json
sys.argv = ['x']; exec(open('/home/claude/gs4/render.py').read().split("if __name__ == '__main__':")[0])
a, b, step = float(os.environ['A']), float(os.environ['B']), float(os.environ.get('STEP', '0.25'))
out = {}; t = a
while t < b:
    render(t); d = LY.check()
    if d: out[f'{t:.2f}'] = d
    t += step
print(json.dumps(out, ensure_ascii=False, indent=0)[:6000]); print('frames with defects:', len(out))
