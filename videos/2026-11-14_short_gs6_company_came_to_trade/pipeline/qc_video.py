"""Frame-level + technical QC for one delivered video. usage: LANGV=en python3 qc_video.py out/GoldenSparrow5_EN_YT.mp4 tag"""
import os, sys, json, subprocess, numpy as np, cv2
from PIL import Image, ImageDraw
sys.path.insert(0, '/home/claude/gs6'); from cues import SC, DUR
f, tag = sys.argv[1], sys.argv[2]; od = f'/home/claude/gs6/qc/{tag}/'; os.makedirs(od, exist_ok=True)
def frame(t):
    b = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{t:.3f}', '-i', f, '-frames:v', '1', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
    return np.frombuffer(b, np.uint8).reshape(1920, 1080, 3)
dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f], capture_output=True, text=True).stdout)
rep = {'file': os.path.basename(f), 'duration': round(dur, 2)}
# technical
o = subprocess.run(['ffmpeg', '-i', f, '-vf', 'blackdetect=d=0.3:pix_th=0.06,freezedetect=n=0.002:d=2.5', '-af', 'ebur128=peak=true', '-f', 'null', '-'], capture_output=True, text=True).stderr
rep['black'] = [l.split('black_start:')[1].split()[0] for l in o.splitlines() if 'black_start' in l]
rep['freeze'] = [l.split('freeze_start: ')[1] for l in o.splitlines() if 'freeze_start' in l]
s = o[o.rfind('Summary:'):]; rep['loudness_I'] = s.split('I:')[1].split('LUFS')[0].strip(); rep['true_peak'] = s.split('Peak:')[1].split('dBFS')[0].strip()
err = subprocess.run(['ffmpeg', '-v', 'error', '-i', f, '-f', 'null', '-'], capture_output=True, text=True).stderr; rep['decode_errors'] = len(err.strip().splitlines())
a, b = frame(0.0).astype(float), frame(dur - 0.25).astype(float); rep['loop_seam_diff'] = round(float(np.abs(a - b).mean()), 2)
rep['frame1_mean'] = round(float(frame(0.0).mean()), 1)
# per-scene sharpness (Laplacian variance of the scene's middle frame, centre region)
sh = {}; scs = SC + [('end', DUR)]
for (n, s0), (_, s1) in zip(scs, scs[1:]):
    g = cv2.cvtColor(frame((s0 + s1) / 2), cv2.COLOR_RGB2GRAY)[300:1300]; sh[n] = round(float(cv2.Laplacian(g, cv2.CV_64F).var()), 1)
    Image.fromarray(frame((s0 + s1) / 2)).save(od + f'key_{s0:06.2f}_{n}.png')
    Image.fromarray(frame(min(s1 - .05, s0 + .35))).save(od + f'entry_{s0:06.2f}_{n}.png')
rep['sharpness'] = sh
# contact sheet of the whole video (every 1.0 s), first 3 s frame by frame, corner/caption crops, phone size
ts = np.arange(0, dur - 0.15, 1.0); cols = 10; rows = (len(ts) + cols - 1) // cols; cs = Image.new('RGB', (cols * 216, rows * 404), (30, 30, 30)); d = ImageDraw.Draw(cs)
for i, t in enumerate(ts): cs.paste(Image.fromarray(frame(t)).resize((216, 384), Image.LANCZOS), ((i % cols) * 216, (i // cols) * 404)); d.text(((i % cols) * 216 + 4, (i // cols) * 404 + 386), f'{t:.0f}s', fill='white')
cs.save(od + 'contact_sheet.jpg', quality=85)
fs = Image.new('RGB', (10 * 216, 9 * 384))
for i in range(90): fs.paste(Image.fromarray(frame(i / 30)).resize((216, 384), Image.LANCZOS), ((i % 10) * 216, (i // 10) * 384))
fs.save(od + 'first_3s.jpg', quality=85)
cr = Image.new('RGB', (1080, 12 * 200))
for i, t in enumerate(np.linspace(1, dur - 1, 12)):
    fr = frame(t); top = Image.fromarray(fr[110:250]); cap = Image.fromarray(fr[1360:1540]); cr.paste(top.resize((1080, 100)), (0, i * 200)); cr.paste(cap.resize((1080, 100)), (0, i * 200 + 100))
cr.save(od + 'corners_captions.jpg', quality=88)
ph = Image.new('RGB', (6 * 390, 2 * 693))
for i, t in enumerate(np.linspace(2, dur - 2, 12)): ph.paste(Image.fromarray(frame(t)).resize((390, 693), Image.LANCZOS), ((i % 6) * 390, (i // 6) * 693))
ph.save(od + 'phone_size.jpg', quality=85)
json.dump(rep, open(od + 'report.json', 'w'), indent=1); print(json.dumps(rep))
