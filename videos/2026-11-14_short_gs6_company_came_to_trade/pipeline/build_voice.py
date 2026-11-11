# GS 6/6 voice: approved S6 Short audio cut only inside measured pauses + the two approved Chelli lines (one take each).
import json, subprocess, numpy as np, scipy.io.wavfile as wf
SR = 48000; VD = '/home/claude/why-channel-studio/videos/2026-11-14_short_gs6_company_came_to_trade/voice/'
SRC = {l: f'/home/claude/gs/out/{l}/GS_S1_S6_{l.upper()}_voice.wav' for l in ('en', 'te')}
def load(f, ss=None, to=None):
    cmd = ['ffmpeg', '-v', 'error', '-i', f] + (['-ss', str(ss)] if ss is not None else []) + (['-to', str(to)] if to is not None else []) + ['-ac', '1', '-ar', str(SR), '-f', 'f32le', '-']
    return np.frombuffer(subprocess.run(cmd, capture_output=True).stdout, np.float32).copy()
def rms(a):
    x = a[np.abs(a) > 0.02]; return float(np.sqrt(np.mean(x ** 2))) if len(x) else 1e-3
def trim(a, th=0.012, pad=0.04):
    i = np.where(np.abs(a) > th)[0]; return a[max(0, i[0] - int(pad * SR)):min(len(a), i[-1] + int(pad * SR))] if len(i) else a
def fade(a, ms=8):
    f = int(ms / 1000 * SR); a[:f] *= np.linspace(0, 1, f); a[-f:] *= np.linspace(1, 0, f); return a
# (name, start, end) cuts sit inside measured pauses (pauses.py, threshold 0.01; Whisper / Telugu ASR chunk times)
SEQ = {'en': [('A', 0.00, 68.86), ('Q1',), ('B', 68.86, 115.36), ('Q2',), ('C', 115.36, 157.92), ('SLIDE',)],
       'te': [('A', 0.00, 48.30), ('Q1',), ('B', 48.30, 107.58), ('Q2',), ('C1', 107.58, 118.55), ('C2', 126.82, 166.00), ('SLIDE',)]}   # TE 7.4 (118.55-126.82) dropped
if __name__ == '__main__':
    rep = {}
    for l in ('en', 'te'):
        R = rms(load(SRC[l])); out = []; marks = {}; t = 0.0; lv = {}
        for it in SEQ[l]:
            k = it[0]
            if k == 'SLIDE': a = np.zeros(int(2.5 * SR), np.float32); g = 0.0
            elif len(it) == 1:   # Chelli line: 0.25 s before (the cut already sits in a pause), 0.40 s after
                a = trim(load(VD + f'{l}_{k}.mp3')); lv[k] = round(20 * np.log10(rms(a) / R), 1); a = fade(a * R / rms(a), 10); g = 0.40
                out.append(np.zeros(int(0.25 * SR), np.float32)); t += 0.25
            else: a = fade(load(SRC[l], it[1], it[2])); g = 0.0 if k in ('A', 'B', 'C1') else 0.30
            marks[k] = [round(t, 3), round(t + len(a) / SR, 3)]; out += [a, np.zeros(int(g * SR), np.float32)]; t += len(a) / SR + g
        v = np.clip(np.concatenate(out), -1, 1); wf.write(f'/home/claude/gs6/voice_{l}.wav', SR, (v * 32767).astype(np.int16))
        json.dump(marks, open(f'/home/claude/gs6/marks_{l}.json', 'w'), indent=0)
        tot = len(v) / SR; rep[l] = dict(total=round(tot, 2), new_take_level_vs_film_dB=lv, marks=marks)
        print(l, f'{int(tot // 60)}:{tot % 60:04.1f}', lv)
    json.dump(rep, open('/home/claude/gs6/voice_report.json', 'w'), indent=1)
