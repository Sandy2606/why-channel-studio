"""Final v3 mix: the speech-safe ambience mix (_sfx.wav) + synced spot effects, ducked under the voice, loudnorm -14 LUFS / -1.5 dBTP."""
import sys, os, subprocess, numpy as np
L = sys.argv[1]; U = L.upper(); os.chdir('/home/claude/gs/film3'); sys.path.insert(0, '.'); sys.argv = ['film.py', L, 'x']
import film, seqs, sfx_events, mix_events as MX
ev = sfx_events.events(film, seqs)
base = MX.load(f'/home/claude/gs/out/{L}/GS_S1_film_{U}_sfx.wav'); voice = MX.load(f'/home/claude/gs/out/{L}/GS_S1_film_{U}_voice.wav')
n = min(len(base), len(voice)); out = MX.mix(base[:n], voice[:n], ev, 0.0)
if len(base) > n: out = np.concatenate([out, base[n:]])
tmp = f'/home/claude/gs/film3/out/{L}_v3_pre.wav'
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', '48000', '-ac', '2', '-i', '-', tmp], input=out.astype(np.float32).tobytes(), check=True)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', tmp, '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11', '-ar', '48000', f'/home/claude/gs/out/{L}/GS_S1_film_{U}_v3.wav'], check=True)
os.remove(tmp); print(L, 'events', len(ev))
