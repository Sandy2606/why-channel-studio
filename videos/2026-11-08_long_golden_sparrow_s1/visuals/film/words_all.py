import json, numpy as np, subprocess, sys
sys.path.insert(0,'/home/claude/gs')
from lines import L
from faster_whisper import WhisperModel
m = WhisperModel('small', device='cpu', compute_type='int8')
T = json.load(open('/home/claude/gs/out/timeline_en.json'))['lines']
def load_trim(p):
    x=np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',p,'-ar','48000','-ac','1','-f','f32le','-'],capture_output=True).stdout,np.float32)
    hop=480;n=len(x)//hop;db=20*np.log10(np.sqrt((x[:n*hop].reshape(n,hop)**2).mean(1))+1e-9);v=np.where(db>-50)[0]
    return x[max(0,v[0]*hop-960):min(len(x),(v[-1]+1)*hop+2400)][::3].copy()
out={}
for i in T:
    segs,_=m.transcribe(load_trim(f'/home/claude/gs/rec/take/en_{i}.mp3'),language='en',word_timestamps=True)
    out[i]=[(w.word.strip(),round(T[i][0]+w.start,2),round(T[i][0]+w.end,2)) for s in segs for w in s.words]
json.dump(out,open('/home/claude/gs/film/words_en_all.json','w'))
print('done',len(out))
