import sys,json,numpy as np,scipy.io.wavfile as wf
from faster_whisper import WhisperModel
name,lang=sys.argv[1],sys.argv[2]
_,a=wf.read(f"rec/{name}_16k.wav"); a=a.astype(np.float32)/32768
if lang=='en':
    m=WhisperModel("small.en",device="cpu",compute_type="int8",cpu_threads=2)
    r,_=m.transcribe(a,word_timestamps=True,beam_size=5,condition_on_previous_text=False)
    out=[(w.start,w.end,w.word.strip()) for s in r for w in s.words]
    json.dump(out,open(f"{name}.words.json","w"))
    line=[]
    for s,e,w in out:
        line.append(f"{w}@{s:.2f}")
        if len(line)==12: print(' '.join(line)); line=[]
    print(' '.join(line))
else:
    sys.path.insert(0,'.'); from rep import segs
    m=WhisperModel("/home/claude/models/te_med",device="cpu",compute_type="int8",cpu_threads=2)
    out=[]
    for s,e in segs(name,0.22,0.25):
        x=a[max(0,int((s-.08)*16000)):int((e+.12)*16000)]
        r,_=m.transcribe(x,language="te",beam_size=5,condition_on_previous_text=False,without_timestamps=True)
        t=" ".join(q.text.strip() for q in r); out.append((s,e,t)); print(f"{s:7.2f}-{e:7.2f} {t}",flush=True)
    json.dump(out,open(f"{name}.seg.json","w"),ensure_ascii=False)
