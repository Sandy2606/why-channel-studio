import json,subprocess,numpy as np,re,sys,difflib
sys.path.insert(0,'/home/claude/gs')
from lines import L
from faster_whisper import WhisperModel
m=WhisperModel('small',device='cpu',compute_type='int8')
jobs=json.load(open('jobs.json')); rows={r['id']:r for r in L}
def load(p): return np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',p,'-ar','16000','-ac','1','-f','f32le','-'],capture_output=True).stdout,np.float32).copy()
norm=lambda s: re.sub(r"[^a-z0-9 ]"," ",s.lower().replace('**','')).split()
ids=[x['id'] for x in L if x['only'] in (None,'en') and x['en']]+[j['id'] for j in jobs if j['lang']=='en' and j['id'] not in rows]
out=[]
for i in ids:
    ref=rows[i]['en'] if i in rows else next(j['text'] for j in jobs if j['lang']=='en' and j['id']==i)
    segs,_=m.transcribe(load(f'rec/take/en_{i}.mp3'),language='en',beam_size=1)
    hyp=' '.join(s.text for s in segs)
    r=difflib.SequenceMatcher(None,norm(ref),norm(hyp)).ratio()
    out.append((i,round(r,2),hyp))
    if r<0.85: print(i,round(r,2),'\n  REF',ref,'\n  HYP',hyp)
json.dump(out,open('rec/asr_en.json','w'),indent=0)
print('done',len(out))
