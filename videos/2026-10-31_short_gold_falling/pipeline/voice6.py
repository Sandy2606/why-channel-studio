"""GOLD 6/6 voice: per-segment pacing (info faster, the Subscribe/Follow line at regular pace)."""
import sys, json, re, subprocess, numpy as np, scipy.io.wavfile as wf
sys.path.insert(0, '/home/claude/sandy2606/why-channel-studio/pipeline/shorts'); import proasm

SR = 48000; D = '/home/claude/why-channel-studio/videos/2026-10-31_short_gold_falling/'
def load(p):
    return np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',p,'-ar',str(SR),'-ac','1','-f','f32le','-'],capture_output=True).stdout,np.float32).copy()
def fade(x):
    f=int(.01*SR); x=x.copy(); x[:f]*=np.linspace(0,1,f); x[-f:]*=np.linspace(1,0,f); return x
def trim(x, thr=-50):
    hop=480; n=len(x)//hop; db=20*np.log10(np.sqrt((x[:n*hop].reshape(n,hop)**2).mean(1))+1e-9); v=np.where(db>thr)[0]
    return x[max(0,v[0]*hop-1200):min(len(x),(v[-1]+1)*hop+2400)]
def tempo(x, t):
    wf.write('/tmp/s.wav',SR,(np.clip(x,-1,1)*32767).astype(np.int16))
    subprocess.run(['ffmpeg','-v','error','-y','-i','/tmp/s.wav','-af',f'atempo={t}','-ar',str(SR),'/tmp/s2.wav'],check=True)
    return load('/tmp/s2.wav')
# ---- segment boundaries (raw block seconds)
EN = load('en/block.wav'); TE = load('te/block.wav')
from faster_whisper import WhisperModel
m = WhisperModel('small.en', device='cpu', compute_type='int8')
segs,_ = m.transcribe(EN[::3].copy(), word_timestamps=True, language='en', condition_on_previous_text=False)
W = [(w.start, w.end, re.sub(r'[^\w]','',w.word.lower())) for s in segs for w in s.words]
def at(word, after=0.0, start=True):
    for s,e,w in W:
        if s >= after and w == word: return s if start else e
    raise KeyError(word)
b_q = at('but', after=at('weeks', start=False) - 0.1); b_w = at('thats', after=at('comment', after=88) ); b_s = at('if', after=b_w); b_sub = at('subscribe', after=b_s+5); b_fol = at('go', after=b_sub+1) if any(w=='go' and s>b_sub+1 for s,e,w in W) else at('follow', after=b_sub+1)
ENB = {'body':(0,b_q),'q':(b_q,b_w),'wrap':(b_w,b_s),'sched':(b_s,b_sub),'sub':(b_sub,b_fol),'fol':(b_fol,len(EN)/SR)}
print('EN', {k:(round(a,2),round(b,2)) for k,(a,b) in ENB.items()})
import tealign5 as TA  # reuse align()
TEL = open(D+'te.txt').read().strip().split('\n')
tail = TEL[-1].split(' | '); TEL = TEL[:-1] + tail
units = [u.strip() for l in TEL for u in re.split(r'(?<=[.?])\s+', l) if u.strip()]
st, en = TA.align(TE, units); ends = st[1:] + [en]
def ui(prefix): return next(i for i,u in enumerate(units) if u.startswith(prefix))
iq, iw, isch, isub, ifol = ui('కానీ gold లో'), ui('Gold week'), ui('ఇలాంటి కొత్త'), ui('Subscribe'), ui('Follow')
TEB = {'body':(0,st[iq]),'q':(st[iq],st[iw]),'wrap':(st[iw],st[isch]),'sched':(st[isch],st[isub]),'sub':(st[isub],st[ifol]),'fol':(st[ifol],len(TE)/SR)}
TEU = {'body':units[:iq],'q':units[iq:iw],'wrap':units[iw:isch],'sched':units[isch:isub],'sub':[units[isub]],'fol':[units[ifol]]}
print('TE', {k:(round(a,2),round(b,2)) for k,(a,b) in TEB.items()})
json.dump({'en':ENB,'te':TEB,'teu':TEU}, open('bounds.json','w'), ensure_ascii=False)
PACE = {'en': {'body':1.12,'q':1.10,'wrap':1.10,'sched':1.10,'sub':1.03,'fol':1.03},
        'te': {'body':1.12,'q':1.10,'wrap':1.10,'sched':1.10,'sub':1.05,'fol':1.05}}
GAP = {'q':0.40,'wrap':0.35,'sched':0.30,'sub':0.12,'fol':0.12}
for lang, X, B in (('en',EN,ENB),('te',TE,TEB)):
    db = proasm.rms_db(X); thr = np.percentile(db,10)+16; med = np.median(db[db>thr])
    for plat in ('yt','ig'):
        order = ['body','q','wrap','sched','sub' if plat=='yt' else 'fol']
        out=[]; marks={}; t=0.0
        for k in order:
            a,b = B[k]; x = trim(fade(X[int(a*SR):int(b*SR)]))
            proasm.CUTS.clear(); x = proasm.squeeze(x, med-24, maxgap=0.22, keep=0.14)
            x = tempo(x, PACE[lang][k])
            if k in GAP: out.append(np.zeros(int(GAP[k]*SR),np.float32)); t += GAP[k]
            marks[k]=(round(t,3), round(t+len(x)/SR,3)); out.append(x); t += len(x)/SR
        y = np.concatenate(out); z = proasm.CHAIN(y[None,:], SR)[0]
        wf.write(f'v_{lang}_{plat}.ch.wav', SR, (np.clip(z,-1,1)*32767).astype(np.int16))
        subprocess.run(['ffmpeg','-v','error','-y','-i',f'v_{lang}_{plat}.ch.wav','-af','loudnorm=I=-14:TP=-1.0:LRA=6','-ar','48000',f'voice_{lang}_{plat}.wav'],check=True)
        json.dump(marks, open(f'marks_{lang}_{plat}.json','w'))
        print(lang, plat, round(t,2), marks)
