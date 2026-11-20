# EP03 sound (꿈속 시선): numpy pizzicato BGM + SFX + narration mix
import numpy as np, subprocess, sys, json
from scipy.io import wavfile
SR = 44100; DUR = 19.5
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
prog = [[60, 64, 67, 72], [57, 60, 64, 69], [53, 57, 60, 65], [55, 59, 62, 67]]
mel = [72, 76, 79, 76, 74, 72, 69, 72, 74, 77, 76, 74, 72, 71, 72, 67]
def section(t0, t1, bpm, amp=1.0, shift=0):
    beat = 60 / bpm / 2
    t = t0; k = 0
    while t < t1 - 0.01:
        ch = prog[(k // 8) % 4]
        if k % 2 == 0: add(bgm, pluck(NOTE(ch[0] - 12 + shift), 0.5, 0.32 * amp, 0.18), t)
        add(bgm, pluck(NOTE(ch[1 + k % 3] + shift), 0.3, 0.13 * amp, 0.09), t)
        if k % 2 == 0: add(bgm, pluck(NOTE(mel[(k // 2) % 16] + shift), 0.35, 0.16 * amp, 0.11), t)
        t += beat; k += 1
section(0.0, 7.8, 120)
section(7.8, 9.3, 135)
section(9.3, 11.95, 150)            # climax
# 11.95-12.95 silence before the reversal
section(13.0, 16.55, 104, 0.7, -2)  # awkward classroom
section(16.7, 18.0, 140, 0.85)

sfx = np.zeros(N, np.float32)
def boom(t, amp=0.9, f=55, dur=0.7, nz=2.0):
    n = int(SR * dur); tt = np.arange(n) / SR
    s = np.sin(2*np.pi*(f + 60*np.exp(-tt*18))*tt) * env_exp(n, 0.18)
    s += lowpass(noise(n, int(t*100)), 0.03) * env_exp(n, 0.12) * nz
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
def sweep(t, f0, f1, dur, amp):
    n = int(SR * dur); tt = np.arange(n) / SR
    f = f0 * (f1 / f0) ** (tt / dur); ph = 2*np.pi*np.cumsum(f) / SR
    add(sfx, np.sin(ph) * np.sin(np.linspace(0, np.pi, n)) * amp, t)
def rumble(t, dur, amp=0.6, seed=5):
    n = int(SR * dur); y = lowpass(noise(n, seed), 0.03) * 4
    e = np.minimum(1, np.arange(n) / (SR * 0.05)) * env_exp(n, dur * 0.5)
    add(sfx, y * e * amp, t)
def murmur(t, dur, amp=0.35, seed=9):
    n = int(SR * dur); x = noise(n, seed)
    y = lowpass(x, 0.12) - lowpass(x, 0.02)
    tt = np.arange(n) / SR; mod = 0.6 + 0.4 * np.sin(2*np.pi*5.3*tt) * np.sin(2*np.pi*1.7*tt)
    e = np.minimum(1, tt / 0.15) * np.minimum(1, (dur - tt) / 0.3)
    add(sfx, y * mod * e * amp * 4, t)
def click(t, amp=0.5):
    for k, dt in enumerate([0, 0.05]):
        n = int(SR * 0.03); add(sfx, noise(n, 40 + k) * env_exp(n, 0.004) * amp, t + dt)

whoosh(0.0, 0.35, 0.4, up=True, seed=1); murmur(0.0, 0.8, 0.25, 2)          # 휙 + crowd
whoosh(0.78, 0.8, 0.4, up=False, seed=11); sweep(0.8, 1600, 200, 0.8, 0.12)  # 되감기 휘리릭
pop(1.82, 0.3, 700); pop(2.5, 0.22, 1100)                                    # 처음엔 / 흘끔
whoosh(2.98, 0.22, 0.35, seed=4); pop(3.08, 0.25, 900); pop(3.12, 0.25, 1000)
whoosh(3.38, 0.22, 0.35, seed=5); [pop(3.48 + k * 0.04, 0.22, 900 + k * 90) for k in range(4)]
for k in range(3): whoosh(3.78 + k * 0.12, 0.16, 0.3, seed=6 + k)
for k in range(10): pop(3.95 + k * 0.025, 0.15, 700 + k * 70)
boom(5.0, 0.35, 50, 0.6, 0.6); boom(5.3, 0.4, 44, 0.8, 0.6)                             # 두둥
murmur(5.1, 1.0, 0.25, 12)
boom(6.2, 0.5, 60, 0.5); murmur(6.25, 1.5, 0.45, 13)                         # 웅성웅성
whoosh(7.7, 0.3, 0.35, seed=14); rumble(7.85, 1.4, 0.7, 15)                  # 쿠구궁
sweep(9.3, 300, 1400, 1.0, 0.18); sweep(9.5, 900, 500, 1.2, 0.1)              # 슈웅 UFO
click(11.48, 0.6); tone(11.5, 2637, 0.25, 0.12, 0.08)                         # 찰칵
sweep(11.86, 2400, 3200, 0.12, 0.08)                                            # 번쩍
tone(12.84, 880, 0.3, 0.06, 0.2)                                             # eye open
sweep(13.0, 900, 180, 0.35, 0.3); boom(13.05, 0.35, 70, 0.35)                # 뚝
sweep(15.5, 220, 110, 0.18, 0.4)                                             # 꿀꺽
whoosh(16.02, 0.25, 0.4, seed=17)                                            # 휙
boom(16.62, 1.0, 45, 0.8); murmur(16.65, 1.3, 0.3, 18)                       # 쾅 62명
tone(17.32, 523, 0.5, 0.15, 0.25); tone(17.55, 494, 0.6, 0.15, 0.3)          # ...또야?
tone(18.0, 1568, 1.2, 0.3, 0.45); tone(18.0, 2093, 1.0, 0.12, 0.35)          # 엔딩 띵
# pre-reversal silence 11.95-12.82
def gate(x, a, b, f=0.08):
    i0, i1 = int(a*SR), int(b*SR); k = int(f*SR)
    x[i0-k:i0] *= np.linspace(1, 0, k); x[i0:i1] = 0
gate(bgm, 11.95, 12.82); gate(sfx, 11.99, 12.82, 0.02)

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
