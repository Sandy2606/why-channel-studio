import json, re, subprocess, difflib, numpy as np
import tealign5 as TA
SR=48000
L=json.load(open('/home/claude/dwv/s5_lines.json')); EN={n:t for n,t in L['en']}; TE={n:t for n,t in L['te']}
def clean(t): return re.sub(r'\s+',' ',re.sub(r'\[.*?\]','',t).replace(' … ',' ').replace('…','… ').replace('**','')).strip().replace('… ,',',')
json.dump({'en':{k:clean(v) for k,v in EN.items()},'te':{k:clean(v) for k,v in TE.items()}},open('lines.json','w'),ensure_ascii=False,indent=1)
def load(p,sr=SR): return np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',p,'-ar',str(sr),'-ac','1','-f','f32le','-'],capture_output=True).stdout,np.float32).copy()
# EN
from faster_whisper import WhisperModel
m=WhisperModel('small.en',device='cpu',compute_type='int8')
x=load('voice_en.wav',16000); mk=json.load(open('marks_en.json')); words=[]
def n_(w): return re.sub(r"[^\w%]","",w.lower())
for k,(a,b) in mk.items():
    seg=x[int(a*16000):int(b*16000)+1600]
    segs,_=m.transcribe(seg,word_timestamps=True,language='en',condition_on_previous_text=False,initial_prompt='7 lakh crore rupees, Navratri, Diwali, FMCG, atta, CAIT, 80,000 crore, Lakshmi aunty, kirana, 85 percent, mainline retail, 50 lakh, Delhi.')
    W=[[w.start+a,w.end+a,w.word.strip()] for s in segs for w in s.words]
    toks=clean(EN[k]).split(); A=[n_(t) for t in toks]; B=[n_(w[2]) for w in W]; T=[None]*len(toks)
    for blk in difflib.SequenceMatcher(None,A,B,autojunk=False).get_matching_blocks():
        for j in range(blk.size): T[blk.a+j]=W[blk.b+j][:2]
    if T[0] is None: T[0]=[a,a+0.25]
    if T[-1] is None: T[-1]=[b-0.3,b]
    i=0
    while i<len(T):
        if T[i] is None:
            j=i
            while T[j] is None: j+=1
            s0=T[i-1][1]; e0=T[j][0]
            for q in range(j-i): T[i+q]=[s0+(e0-s0)*q/(j-i), s0+(e0-s0)*(q+1)/(j-i)]
            i=j
        i+=1
    for t_,w in zip(T,toks): words.append([round(t_[0],3),round(t_[1],3),w,k])
json.dump(words,open('words_en.json','w'))
print('en',len(words))
# TE
SP={'12.4':'పన్నెండు పాయింట్ నాలుగు','15':'పదిహేను','60':'అరవై','70':'డెబ్భై','1992':'పంతొమ్మిది వందల తొంభై రెండు','1998':'పంతొమ్మిది వందల తొంభై ఎనిమిది','2003':'రెండు వేల మూడు','2012':'రెండు వేల పన్నెండు','824':'ఎనిమిది వందల ఇరవై నాలుగు','750':'ఏడు వందల యాభై','21,000':'ఇరవై ఒక్క వేల','18,000':'పద్దెనిమిది వేల','45,000':'నలభై ఐదు వేల','12,000':'పన్నెండు వేల','28,800':'ఇరవై ఎనిమిది వేల ఎనిమిది వందల','8.33':'ఎనిమిది పాయింట్ మూడు మూడు','1965':'పంతొమ్మిది వందల అరవై ఐదు','2025':'రెండు వేల ఇరవై ఐదు','2026':'రెండు వేల ఇరవై ఆరు','50':'యాభై','30':'ముప్పై','12':'పన్నెండు','20':'ఇరవై','21':'ఇరవై ఒకటి','2083':'రెండు వేల ఎనభై మూడు','1957':'పంతొమ్మిది వందల యాభై ఏడు','1994':'పంతొమ్మిది వందల తొంభై నాలుగు','11':'పదకొండు','9':'తొమ్మిది','7':'ఏడు','1':'ఒకటి','100':'వంద','80,000':'ఎనభై వేల','85':'ఎనభై ఐదు','8':'ఎనిమిది','5':'ఐదు'}
TA.SPOKEN_LEN.update(SP)
x=load('voice_te.wav'); mk=json.load(open('marks_te.json')); words=[]; sent=[]
for k,(a,b) in mk.items():
    us=[u.strip() for u in re.split(r'(?<=[.?:])\s+',clean(TE[k])) if u.strip()]
    seg=x[int(a*SR):int(b*SR)]
    if len(us)>1: st,en=TA.align(seg,us); ends=st[1:]+[en]
    else: st,ends=[0.0],[len(seg)/SR]
    for u,s,e in zip(us,st,ends):
        t0,t1=a+s,a+e; tk=u.split(); Lw=np.array([max(2,TA.splen(w)) for w in tk],float); cum=np.concatenate([[0],np.cumsum(Lw)])/Lw.sum()
        sent.append([round(t0,3),k,u])
        for i,w in enumerate(tk): words.append([round(t0+(t1-t0)*cum[i],3),round(t0+(t1-t0)*cum[i+1],3),w,k])
json.dump({'words':words,'sent':sent},open('words_te.json','w'),ensure_ascii=False)
print('te',len(words),len(sent))
