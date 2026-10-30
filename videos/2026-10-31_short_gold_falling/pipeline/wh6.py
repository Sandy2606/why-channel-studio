import json, re, subprocess, difflib, numpy as np
from faster_whisper import WhisperModel
m = WhisperModel('small.en', device='cpu', compute_type='int8')
D='/home/claude/why-channel-studio/videos/2026-10-31_short_gold_falling/'
def tr(x, off):
    segs,_ = m.transcribe(x, word_timestamps=True, language='en', initial_prompt='CERN, FD, Fed, Andhra Pradesh, Olympic.', condition_on_previous_text=False)
    return [[float(w.start)+off, float(w.end)+off, w.word.strip()] for s in segs for w in s.words]
def n(w): return re.sub(r"[^\w%]","",w.lower())
L=open(D+'en.txt').read().strip().split('\n'); tail=L[-1].split(' | ')
for plat in ('yt','ig'):
    x=np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',f'voice_en_{plat}.wav','-ar','16000','-ac','1','-f','f32le','-'],capture_output=True).stdout,np.float32).copy()
    W=[]; total=len(x)/16000; off=0.0
    while off < total-0.3:
        lim=min(total, off+22); seg=tr(x[int(off*16000):int(lim*16000)], off)
        last = W[-1][1] if W else -1
        for w in seg:
            if w[0] >= last-0.05 and (lim>=total or w[1] < lim-0.6): W.append(w); last=w[1]
        off = lim-4.0 if lim<total else total
    text=' '.join(L[:-1]+[tail[0] if plat=='yt' else tail[1]]).replace('…',' ').replace('7 percent','7%').replace('30 percent','30%')
    toks=text.split(); a=[n(t) for t in toks]; b=[n(w[2]) for w in W]; T=[None]*len(toks)
    for blk in difflib.SequenceMatcher(None,a,b,autojunk=False).get_matching_blocks():
        for k in range(blk.size): T[blk.a+k]=W[blk.b+k][:2]
    if T[0] is None: T[0]=[0.0,0.3]
    i=0
    while i<len(T):
        if T[i] is None:
            j=i
            while j<len(T) and T[j] is None: j+=1
            s0=T[i-1][1]; e0=T[j][0] if j<len(T) else s0+0.4*(j-i); L_=j-i
            for k in range(L_): T[i+k]=[s0+(e0-s0)*k/L_, s0+(e0-s0)*(k+1)/L_]
            print(plat,'fill',toks[i:j]); i=j
        i+=1
    json.dump([[round(t[0],3),round(t[1],3),w] for t,w in zip(T,toks)],open(f'words_en_{plat}.json','w'))
    print(plat, len(toks), 'last', T[-1])
