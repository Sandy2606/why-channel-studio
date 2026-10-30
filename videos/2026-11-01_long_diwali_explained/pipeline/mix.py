"""Mix voice + music (2 tracks, ducked) + real SFX for the Diwali long video. LANGV=en|te python3 mix.py"""
import os, json, subprocess, numpy as np, soundfile as sf
LANG = os.environ.get('LANGV', 'en'); SR = 48000
R = '/home/claude/why-channel-studio/'; D = '/home/claude/dl/'
EVJ = json.load(open(D + f'events_{LANG}.json')); CAT = json.load(open(R + 'sfx/catalog.json'))
DUR = EVJ['dur']; LEAD = EVJ['lead']; N = int(DUR * SR) + SR


def load(p, af=None):
    cmd = ['ffmpeg', '-v', 'error', '-i', p] + (['-af', af] if af else []) + ['-ar', str(SR), '-ac', '2', '-f', 'f32le', '-']
    return np.frombuffer(subprocess.run(cmd, capture_output=True).stdout, np.float32).reshape(-1, 2).copy()


# voice: light chain (HPF, gentle compression), loudness set on the final mix
v = load(D + f'voice_{LANG}_raw.wav', 'highpass=f=70,acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120:makeup=2,alimiter=limit=0.95')
voice = np.zeros((N, 2), np.float32); i0 = int(LEAD * SR); voice[i0:i0 + len(v)] = v[:N - i0]
# voice activity envelope (for ducking)
mono = np.abs(voice[:, 0]); hop = 480; n = len(mono) // hop
env = mono[:n * hop].reshape(-1, hop).max(1); act = (env > 0.02).astype(np.float32)
k = np.ones(25) / 25; act = np.clip(np.convolve(act, k, 'same') * 1.6, 0, 1)
act = np.repeat(act, hop); act = np.pad(act, (0, N - len(act)))[:N]

# music: track 1 until chapter 4 card, track 2 after
eq = 'equalizer=f=2200:t=q:w=1:g=-5,highshelf=f=6000:g=-5,lowpass=f=10000'
t_switch = EVJ['chapters']['4']
m1 = load(R + 'music/where_the_river_bends.mp3', eq); m2 = load(R + 'music/before_the_world_wakes.mp3', eq)
music = np.zeros((N, 2), np.float32)
def place_loop(m, a, b, fin=1.5, fout=2.0):
    a, b = int(a * SR), min(N, int(b * SR)); L = b - a
    reps = np.concatenate([m] * (L // len(m) + 1))[:L].copy()
    g = np.ones(L, np.float32); fi, fo = int(fin * SR), int(fout * SR)
    g[:fi] = np.linspace(0, 1, fi); g[-fo:] = np.minimum(g[-fo:], np.linspace(1, 0, fo))
    music[a:b] += reps * g[:, None]
place_loop(m1, 0, t_switch + 1.0, fin=0.05, fout=1.6)
place_loop(m2, t_switch + 0.4, DUR, fin=2.0, fout=3.0)
mg = 0.23 * (1 - 0.62 * act)
# chapter dips: music dips under the card then swells
for kk, s in EVJ['chapters'].items():
    a, b = int(s * SR), int((s + 1.8) * SR)
    if b < N: mg[a:b] *= np.concatenate([np.linspace(1, 0.45, (b - a) // 2), np.linspace(0.45, 1.15, b - a - (b - a) // 2)])
music *= mg[:, None]

# sfx
fx = np.zeros((N, 2), np.float32)
SPECIAL = {'footsteps_soft_indoor': ('atempo=1.3', 1.4), 'rain_light_loop': (None, 9.0), 'wind_ambience': ('atrim=7', 5.5),
           'firework_whistle_echo': ('lowpass=f=1800', 4.0), 'typing_run': ('atrim=start=2', 1.6), 'swoosh_slow': (None, 2.2),
           'match_light': ('volume=3', 2.0), 'impact_big': (None, 4.0), 'impact_trailer': (None, 3.0), 'broom_sweep': ('atrim=start=2.5', 3.0)}
cache = {}
for name, t, g in EVJ['ev']:
    c = CAT[name]; fn = R + 'sfx/' + os.path.basename(c['file'])
    af, maxlen = SPECIAL.get(name, (None, None))
    key = (name, af)
    if key not in cache: cache[key] = load(fn, af)
    x = cache[key]
    hit = c.get('hit_at') or 0.0
    if name == 'wind_ambience': hit = 0.0
    if name == 'typing_run' or name == 'broom_sweep': hit = 0.0
    if maxlen: x = x[:int(maxlen * SR)].copy(); fo = min(len(x), int(0.4 * SR)); x[-fo:] *= np.linspace(1, 0, fo)[:, None]
    a = int((t - hit) * SR)
    if a < 0: x = x[-a:]; a = 0
    b = min(N, a + len(x)); fx[a:b] += x[:b - a] * g
fx *= (1 - 0.45 * act)[:, None]

mix = voice + music + fx * 0.9
sf.write(D + f'mixpre_{LANG}.wav', mix[:int(DUR * SR)], SR)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', D + f'mixpre_{LANG}.wav', '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11', '-ar', '48000', D + f'mix_{LANG}.wav'], check=True)
print('mixed', LANG)
