import json, subprocess, hashlib, numpy as np, re, sys, difflib
import scipy.io.wavfile as wf
sys.argv=['x']
LIB='/home/claude/why-channel-studio/'; idx=json.load(open(LIB+'voice_lib/index.json'))
D='/home/claude/why-channel-studio/videos/2026-10-31_short_gold_falling/'
def load(p):
    raw=subprocess.run(['ffmpeg','-v','error','-i',p,'-ar','48000','-ac','1','-f','f32le','-'],capture_output=True).stdout; return np.frombuffer(raw,np.float32)
def save(lang,text,x,voice):
    if any(e['text']==text for e in idx): return
    h=hashlib.md5(text.encode()).hexdigest()[:12]; f=f'voice_lib/{lang}/{h}.mp3'
    wf.write('/tmp/seg.wav',48000,(np.clip(x,-1,1)*32767).astype(np.int16))
    subprocess.run(['ffmpeg','-v','error','-y','-i','/tmp/seg.wav','-b:a','128k',LIB+f],check=True)
    idx.append({'lang':lang,'text':text,'file':f,'voice':voice,'model':'eleven_v4','source':'Gold Short 6, Oct 30 2026','tag':'gold6' if not text.startswith(('If you like learning','Subscribe, and','Follow, and','ఇలాంటి కొత్త','Subscribe చేయండి, మీకు','Follow అవ్వండి, మీకు')) else 'cta'})
def cut(x,s,e):
    y=x[int(max(0,s)*48000):int(e*48000)].copy(); n=480; y[:n]*=np.linspace(0,1,n); y[-n:]*=np.linspace(1,0,n); return y
# EN
from faster_whisper import WhisperModel
m=WhisperModel('small.en',device='cpu',compute_type='int8')
x=load('en/block.wav'); x16=load('en/block.wav')[::3].copy()
segs,_=m.transcribe(x16,word_timestamps=True,language='en',condition_on_previous_text=False)
W=[[w.start,w.end,w.word.strip()] for s in segs for w in s.words]
lines=open(D+'en.txt').read().strip().split('\n'); lines=lines[:-1]+lines[-1].split(' | ')
def n(w): return re.sub(r"[^\w]","",w.lower())
toks=[]; li=[]
for i,l in enumerate(lines):
    for t in l.split(): toks.append(n(t)); li.append(i)
b=[n(w[2]) for w in W]; T={}
for blk in difflib.SequenceMatcher(None,toks,b,autojunk=False).get_matching_blocks():
    for k in range(blk.size): T[blk.a+k]=W[blk.b+k]
for i,l in enumerate(lines):
    ks=[k for k in range(len(toks)) if li[k]==i and k in T]
    if not ks: print('miss',l); continue
    s=T[ks[0]][0]-0.12; e=T[ks[-1]][1]+0.18
    save('en',l,cut(x,s,e),'Sandeep English (grcC6bYJfJbBq5S549Id)'); print('en',round(s,2),round(e,2),l[:40])
# TE
import tealign5 as TA5; ns={'align':TA5.align}
xt=load('te/block.wav'); tl=open(D+'te.txt').read().strip().split('\n'); tl=tl[:-1]+tl[-1].split(' | ')
st,en=ns['align'](xt,tl); ends=st[1:]+[en]
for l,s,e in zip(tl,st,ends):
    save('te',l,cut(xt,s-0.05,e),'Sandeep Telugu (YudnU7tnCElqOrj11puE)'); print('te',round(s,2),round(e,2),l[:30])
json.dump(idx,open(LIB+'voice_lib/index.json','w'),ensure_ascii=False,indent=1); print(len(idx))
