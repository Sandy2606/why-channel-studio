import json, subprocess, numpy as np
from faster_whisper import WhisperModel
m = WhisperModel('small.en', device='cpu', compute_type='int8')
def tr(x, off):
    segs,_ = m.transcribe(x, word_timestamps=True, language='en', initial_prompt='RBI, FD, lakh, crore, Netherlands, Switzerland.', condition_on_previous_text=False)
    return [[round(float(w.start)+off,3),round(float(w.end)+off,3),w.word.strip()] for s in segs for w in s.words]
for plat in ('yt','ig'):
    raw = subprocess.run(['ffmpeg','-v','error','-i',f'voice_en_{plat}.wav','-ar','16000','-ac','1','-f','f32le','-'],capture_output=True).stdout
    x = np.frombuffer(raw, np.float32).copy(); W=[]; off=0.0
    for lim in (25, 50, 70):
        seg = tr(x[int(off*16000):int(min(lim,len(x)/16000)*16000)], off)
        if lim<70: seg=seg[:-1]
        W+=seg; off=W[-1][1]+0.02
    out=[]
    for s,e,w in W:
        if out and (w[0] in ',.' ) and out[-1][2][-1].isdigit(): out[-1][2]+=w; out[-1][1]=e; continue
        out.append([s,e,w.replace('tons','tonnes').replace('$1','one dollar')])
    json.dump(out,open(f'words_en_{plat}.json','w')); print(plat,' '.join(w[2] for w in out)); print(out[-1])
