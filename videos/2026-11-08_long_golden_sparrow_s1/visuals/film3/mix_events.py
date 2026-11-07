"""Mix spot events onto a film mix (voice+music [+beds]), ducked under the narration; returns float32 stereo."""
import subprocess, numpy as np
SR = 48000; SFX = '/home/claude/why-channel-studio/sfx/'
_cache = {}
def load(p, ss=None, t=None):
    a = ['ffmpeg', '-v', 'error'] + (['-ss', str(ss)] if ss else []) + ['-i', p] + (['-t', str(t)] if t else []) + ['-f', 'f32le', '-ac', '2', '-ar', str(SR), '-']
    return np.frombuffer(subprocess.run(a, capture_output=True, check=True).stdout, np.float32).reshape(-1, 2).copy()
def mix(base, voice, ev, t0=0.0):
    """base, voice: arrays starting at film time t0."""
    n = len(base); out = base.copy()
    D = 480; m_ = n // D * D; lv = np.abs(voice[:m_]).mean(1).reshape(-1, D).mean(1)
    env = np.convolve(lv, np.ones(30) / 30, 'same'); act = np.clip(env / (np.percentile(env[env > 1e-4], 50) * 0.35 + 1e-9), 0, 1)
    act = np.concatenate([np.repeat(act, D), np.full(n - m_, act[-1] if len(act) else 0)])
    for f, t, g, off, dur, fade, duck in ev:
        key = (f, off, dur)
        if key not in _cache: _cache[key] = load(SFX + f, off if off else None, dur)
        s = _cache[key] * 10 ** (g / 20); i0 = int((t - t0) * SR)
        if i0 >= n or i0 + len(s) <= 0: continue
        s = s.copy(); fl = int(fade * SR)
        if fl > 1 and len(s) > 2 * fl: s[:fl] *= np.linspace(0, 1, fl)[:, None]; s[-fl:] *= np.linspace(1, 0, fl)[:, None]
        a = max(0, i0); b = min(n, i0 + len(s)); seg = s[a - i0:b - i0]
        gd = 1 - (1 - 10 ** (duck / 20)) * act[a:b]
        out[a:b] += seg * gd[:, None]
    return out
