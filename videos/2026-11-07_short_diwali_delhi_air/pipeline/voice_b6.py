"""Diwali 1/6 voice: per-line clips -> trimmed, squeezed, paced; marks per line. One voice per language (YT/IG differ only on screen)."""
import sys, json, subprocess, numpy as np, scipy.io.wavfile as wf
sys.path.insert(0, '/home/claude/why-channel-studio/pipeline/shorts'); import proasm
SR = 48000
ORDER = [str(i) for i in range(1,19)]+['L']
PACE = {'en': 1.08, 'te': 1.10}
GAP = {**{str(i):0.28 for i in range(2,19)}, '3':0.35,'8':0.35,'9':0.40,'11':0.22,'15':0.40,'17':0.35,'18':0.35,'L':0.22}
def load(p):
    return np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',p,'-ar',str(SR),'-ac','1','-f','f32le','-'],capture_output=True).stdout,np.float32).copy()
def fade(x):
    f=int(.008*SR); x=x.copy(); x[:f]*=np.linspace(0,1,f); x[-f:]*=np.linspace(1,0,f); return x
def trim(x, thr=-50):
    hop=480; n=len(x)//hop; db=20*np.log10(np.sqrt((x[:n*hop].reshape(n,hop)**2).mean(1))+1e-9); v=np.where(db>thr)[0]
    return x[max(0,v[0]*hop-960):min(len(x),(v[-1]+1)*hop+1900)]
def tempo(x, t):
    wf.write('/tmp/b1s.wav',SR,(np.clip(x,-1,1)*32767).astype(np.int16))
    subprocess.run(['ffmpeg','-v','error','-y','-i','/tmp/b1s.wav','-af',f'atempo={t}','-ar',str(SR),'/tmp/b1s2.wav'],check=True)
    return load('/tmp/b1s2.wav')
S = {}
for row in open('takes.txt'):
    l,n,s = row.split(); S[(l,n)] = f'/home/claude/dwv/raw/{s}.mp3'
for lang in ('en','te'):
    X = {n: load(S[(lang,n)]) for n in ORDER}
    allx = np.concatenate(list(X.values())); db = proasm.rms_db(allx); thr = np.percentile(db,10)+16; med = np.median(db[db>thr])
    out=[]; marks={}; t=0.0
    for n in ORDER:
        x = trim(fade(X[n]))
        proasm.CUTS.clear(); x = proasm.squeeze(x, med-24, maxgap=0.24, keep=0.15)
        x = tempo(x, PACE[lang])
        if n in GAP: out.append(np.zeros(int(GAP[n]*SR),np.float32)); t += GAP[n]
        marks[n] = (round(t,3), round(t+len(x)/SR,3)); out.append(x); t += len(x)/SR
    y = np.concatenate(out); z = proasm.CHAIN(y[None,:], SR)[0]
    wf.write(f'v_{lang}.ch.wav', SR, (np.clip(z,-1,1)*32767).astype(np.int16))
    subprocess.run(['ffmpeg','-v','error','-y','-i',f'v_{lang}.ch.wav','-af','loudnorm=I=-14:TP=-1.0:LRA=6','-ar','48000',f'voice_{lang}.wav'],check=True)
    json.dump(marks, open(f'marks_{lang}.json','w'))
    print(lang, round(t,2), f'{int(t//60)}:{t%60:04.1f}')
