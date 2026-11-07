"""Technical QC of a final film: format, duration, black/frozen/silent sections, loudness, peaks."""
import sys, json, subprocess, re
p = sys.argv[1]; R = {}
pr = json.loads(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration,size:stream=codec_type,codec_name,width,height,r_frame_rate,duration,sample_rate,channels', '-of', 'json', p], capture_output=True, text=True).stdout)
v = [s for s in pr['streams'] if s['codec_type'] == 'video'][0]; a = [s for s in pr['streams'] if s['codec_type'] == 'audio'][0]
R['file'] = p; R['size_MB'] = round(int(pr['format']['size']) / 1e6, 1); R['duration_s'] = round(float(pr['format']['duration']), 2)
R['video'] = f"{v['codec_name']} {v['width']}x{v['height']} {v['r_frame_rate']} dur {float(v['duration']):.2f}s"
R['audio'] = f"{a['codec_name']} {a['sample_rate']} Hz {a['channels']}ch dur {float(a['duration']):.2f}s"
def run(args): return subprocess.run(['ffmpeg', '-nostats', '-hide_banner', '-i', p] + args + ['-f', 'null', '-'], capture_output=True, text=True).stderr
e = run(['-vf', 'blackdetect=d=0.5:pix_th=0.06', '-an'])
R['black'] = re.findall(r'black_start:([\d.]+) black_end:([\d.]+)', e)
e = run(['-vf', 'freezedetect=n=0.0008:d=6', '-an'])
R['frozen'] = list(zip(re.findall(r'freeze_start: ([\d.]+)', e), re.findall(r'freeze_end: ([\d.]+)', e)))
e = run(['-af', 'silencedetect=n=-45dB:d=2', '-vn'])
R['silent'] = list(zip(re.findall(r'silence_start: ([\d.]+)', e), re.findall(r'silence_end: ([\d.]+)', e)))
e = run(['-af', 'ebur128=peak=true', '-vn'])
s = e[e.rfind('Summary'):]
R['loudness_LUFS'] = float(re.search(r'I:\s+(-?[\d.]+)', s)[1]); R['true_peak_dBFS'] = float(re.search(r'Peak:\s+(-?[\d.]+)', s)[1]); R['LRA'] = float(re.search(r'LRA:\s+([\d.]+)', s)[1])
e = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-f', 'null', '-'], capture_output=True, text=True).stderr
R['decode_errors'] = len(e.strip().splitlines()) if e.strip() else 0
print(json.dumps(R, indent=1))
