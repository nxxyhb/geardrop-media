# EP02 sound: numpy pizzicato BGM + SFX + narration mix
import numpy as np, subprocess, sys, json
from scipy.io import wavfile
SR = 44100; DUR = 19.9
N = int(SR * DUR)
def load(p):
    sr, a = wavfile.read(p); a = a.astype(np.float32)
    if a.ndim > 1: a = a.mean(1)
    return a / (np.abs(a).max() + 1e-9)
def env_exp(n, tau): return np.exp(-np.arange(n) / (SR * tau))
def pluck(f, dur=0.35, amp=0.3, tau=0.12):
    n = int(SR * dur); t = np.arange(n) / SR
    s = np.sin(2*np.pi*f*t) + 0.45*np.sin(4*np.pi*f*t) + 0.2*np.sin(6*np.pi*f*t)
    a = env_exp(n, tau); a[:60] *= np.linspace(0, 1, 60)
    return s * a * amp
def add(buf, x, t):
    i = int(t * SR); j = min(len(buf), i + len(x))
    if j > i: buf[i:j] += x[:j - i]
def noise(n, seed=1): return np.random.default_rng(seed).standard_normal(n).astype(np.float32)
def lowpass(x, a=0.1):
    y = np.zeros_like(x); acc = 0.0
    for i in range(len(x)): acc += a * (x[i] - acc); y[i] = acc
    return y
NOTE = lambda m: 440 * 2 ** ((m - 69) / 12)

bgm = np.zeros(N, np.float32)
# chord progression C - G - Am - F (pizzicato arpeggio)
prog = [[60, 64, 67, 72], [55, 59, 62, 67], [57, 60, 64, 69], [53, 57, 60, 65]]
mel = [72, 74, 76, 79, 76, 74, 72, 67, 69, 72, 74, 72, 76, 74, 72, 71]
def section(t0, t1, bpm, amp=1.0):
    beat = 60 / bpm / 2  # 8th notes
    t = t0; k = 0
    while t < t1 - 0.01:
        ch = prog[(k // 8) % 4]
        if k % 2 == 0: add(bgm, pluck(NOTE(ch[0] - 12), 0.5, 0.32 * amp, 0.18), t)
        add(bgm, pluck(NOTE(ch[1 + k % 3]), 0.3, 0.13 * amp, 0.09), t)
        if k % 2 == 0: add(bgm, pluck(NOTE(mel[(k // 2) % 16]), 0.35, 0.16 * amp, 0.11), t)
        t += beat; k += 1
section(0.0, 8.6, 120)
section(8.6, 11.0, 136)
section(11.0, 11.75, 150)
section(12.6, 16.5, 112, 0.8)
section(16.5, 18.6, 140, 0.9)

sfx = np.zeros(N, np.float32)
def boom(t, amp=0.9, f=55, dur=0.7):
    n = int(SR * dur); tt = np.arange(n) / SR
    s = np.sin(2*np.pi*(f + 60*np.exp(-tt*18))*tt) * env_exp(n, 0.18)
    s += lowpass(noise(n, int(t*100)), 0.08) * env_exp(n, 0.12) * 2.0
    add(sfx, s * amp, t)
def pop(t, amp=0.35, f=900):
    n = int(SR * 0.09); tt = np.arange(n) / SR
    s = np.sin(2*np.pi*(f + 1400*tt/0.09)*tt) * env_exp(n, 0.025)
    add(sfx, s * amp, t)
def whoosh(t, dur, amp=0.3, up=True, seed=3):
    n = int(SR * dur); x = noise(n, seed)
    a = np.linspace(0.02, 0.35, n) if up else np.linspace(0.35, 0.02, n)
    y = np.zeros(n, np.float32); acc = 0.0
    for i in range(n): acc += a[i] * (x[i] - acc); y[i] = acc
    e = np.sin(np.linspace(0, np.pi, n))
    add(sfx, y * e * amp * 3, t)
def tone(t, f, dur, amp, tau=0.3):
    n = int(SR * dur); tt = np.arange(n) / SR
    s = (np.sin(2*np.pi*f*tt) + 0.3*np.sin(2*np.pi*2*f*tt)) * env_exp(n, tau)
    add(sfx, s * amp, t)
def rumble(t, dur, amp=0.6, seed=5):
    n = int(SR * dur); y = lowpass(noise(n, seed), 0.03) * 4
    e = np.minimum(1, np.arange(n) / (SR * 0.05)) * env_exp(n, dur * 0.5)
    add(sfx, y * e * amp, t)
    rng = np.random.default_rng(seed)
    for k in range(10): pop(t + rng.random() * dur * 0.8, 0.12, 400 + rng.random() * 600)

boom(0.0, 0.8)
for k in range(8): pop(0.05 + k * 0.06, 0.15, 600 + k * 80)
whoosh(0.52, 0.3, 0.35, up=False, seed=11)           # rewind
tone(0.85, 1318, 0.35, 0.22, 0.15); tone(1.05, 1046, 0.5, 0.22, 0.2)  # ding-dong
# kimbap doubling pops
EXP = [[0.8,1],[1.95,1],[2.0,2],[3.0,2],[3.05,3],[4.5,6],[4.8,7],[5.2,10],[6.2,10]]
def expAt(t):
    e = EXP[0][1]
    for (a, ea), (b, eb) in zip(EXP, EXP[1:]):
        if a <= t <= b: e = ea + (eb - ea) * (t - a) / (b - a)
        if t > b: e = eb
    return int(np.floor(e + 1e-6))
last = expAt(0.8); t = 0.8
while t < 6.1:
    e = expAt(t)
    if e != last: pop(t, 0.3 if t < 2.5 else 0.22, 800 + e * 60); last = e
    t += 1 / 60
pop(1.75, 0.4, 1000)
rumble(4.85, 1.2, 0.55, 7)
boom(6.1, 0.85, 48, 0.9)
rumble(8.65, 2.0, 0.6, 9)
boom(11.05, 0.7, 42, 0.5); boom(11.35, 0.8, 38, 0.7)   # 두둥
whoosh(12.7, 0.45, 0.35, up=True, seed=13)              # 쑥
tone(14.55, 2093, 0.16, 0.25, 0.5)                      # 삑
pop(14.0, 0.2, 900); pop(15.6, 0.2, 950)
for k, bt in enumerate([16.5, 16.85, 17.2, 17.55, 17.9, 18.2]):
    for j in range(min(2 ** k, 6)): pop(bt + j * 0.035, 0.3, 800 + k * 120 + j * 40)
tone(18.6, 1568, 1.2, 0.3, 0.45); tone(18.6, 2093, 1.0, 0.12, 0.35)  # ending ding

# narration
SEG = json.loads(sys.argv[1])  # [[path, start], ...]
vo = np.zeros(N, np.float32); duck = np.ones(N, np.float32)
for p, st in SEG:
    a = load(p) * 0.92; add(vo, a, st)
    i0 = int((st - 0.08) * SR); i1 = int((st + len(a) / SR + 0.1) * SR)
    duck[max(0, i0):i1] = 0.3
# smooth duck curve
k = int(SR * 0.06); duck = np.convolve(duck, np.ones(k) / k, mode='same').astype(np.float32)
bgm *= duck
mix = vo * 1.0 + bgm * 0.8 + sfx * 0.6
mix /= np.abs(mix).max() / 0.89
fo = int(SR * 0.5); mix[-fo:] *= np.linspace(1, 0, fo)
wavfile.write(sys.argv[2], SR, (mix * 32767).astype(np.int16))
print('ok', len(mix) / SR)
