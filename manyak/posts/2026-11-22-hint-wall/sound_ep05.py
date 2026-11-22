# EP05 sound (힌트 담장): numpy pizzicato BGM + SFX + narration mix
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
section(0.0, 0.8, 120)
section(1.1, 5.8, 120)
section(5.8, 12.5, 150)             # climax (구름 돌파~우주)
# 12.5-13.4 반전 직전 BGM 정적 0.9초
section(13.5, 18.0, 110, 0.7, -2)   # 방탈출 카페

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



RES = [2.08, 2.62, 3.07, 3.52, 4.07, 4.57, 5.07, 5.57, 6.2, 6.6, 8.0, 8.3, 8.6, 8.9, 9.2, 9.62, 9.92, 10.22, 10.52, 11.1]
for i, r in enumerate(RES):
    vis = i < 8 or i >= 15 or i == 19
    click(r - 0.14, 0.4 if vis else 0.15)
    if i < 8: boom(r, 0.45, 60, 0.45, 1.0)                      # 쿵 (담장 2배)
    elif i in (8, 9): boom(r, 0.6, 48, 0.8, 1.6); rumble(r, 0.5, 0.25, 40 + i)
    elif i < 15: boom(r, 0.15, 70, 0.3, 0.5)
    elif i < 19: boom(r, 0.3, 65, 0.35, 0.8)
    else: boom(r, 0.85, 40, 1.1, 2.0); rumble(r, 0.9, 0.35, 77)  # 20번째 쾅
pop(2.2, 0.25, 900)
whoosh(0.78, 0.34, 0.25, up=False, seed=11); sweep(0.8, 1600, 200, 0.3, 0.07)   # 되감기 휘리릭
whoosh(5.8, 1.0, 0.3, up=True, seed=21)                                         # 구름 바람
pop(7.2, 0.3, 1200); whoosh(7.2, 0.35, 0.2, up=True, seed=5)                     # 모자 퐁
whoosh(8.0, 1.3, 0.38, up=True, seed=8); sweep(8.1, 300, 900, 1.1, 0.08)         # 비행기 휘익
sweep(12.0, 800, 2400, 1.2, 0.07); tone(12.0, 1318, 1.0, 0.08, 0.5)              # 우주 반짝
whoosh(13.4, 0.4, 0.45, up=True, seed=31); sweep(13.4, 1200, 300, 0.3, 0.12)    # 반전 휙
boom(13.75, 0.35, 70, 0.35, 1.2)                                                  # 털썩
tone(18.0, 1568, 1.2, 0.3, 0.45); tone(18.0, 2093, 1.0, 0.12, 0.35)              # 엔딩 띵
def gate(x, a, b, f=0.08):
    i0, i1 = int(a*SR), int(b*SR); k = int(f*SR)
    x[i0-k:i0] *= np.linspace(1, 0, k); x[i0:i1] = 0
gate(bgm, 0.8, 1.1, 0.04)
gate(bgm, 12.5, 13.4, 0.12)   # 반전 직전 정적: 피치카토 꼬리까지 끊어 또렷하게

SEG = json.loads(sys.argv[1])
vo = np.zeros(N, np.float32); duck = np.ones(N, np.float32)
for p, st in SEG:
    a = load(p) * 0.92; add(vo, a, st)
    i0 = int((st - 0.08) * SR); i1 = int((st + len(a) / SR + 0.1) * SR)
    duck[max(0, i0):i1] = 0.3
k = int(SR * 0.06); duck = np.convolve(duck, np.ones(k) / k, mode='same').astype(np.float32)
bgm *= duck
sduck = 1 - (1 - duck) / 0.7 * 0.8   # 내레이션 구간 효과음 0.2배(약 -14dB)
sfx *= sduck
mix = vo * 1.0 + bgm * 0.8 + sfx * 0.6
mix /= np.abs(mix).max() / 0.89
fo = int(SR * 0.5); mix[-fo:] *= np.linspace(1, 0, fo)
wavfile.write(sys.argv[2], SR, (mix * 32767).astype(np.int16))
print('ok', len(mix) / SR)
