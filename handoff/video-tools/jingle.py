"""Świąteczna muzyczka bez praw autorskich: refren „Jingle Bells” (J. L. Pierpont, 1857, domena publiczna)
w naszej własnej syntezie (dzwonki FM, bas, dzwoneczki sań). Użycie: python3 jingle.py wyjscie.wav [bpm]"""
import sys, wave
import numpy as np

SR = 44100
OUT = sys.argv[1]
BPM = float(sys.argv[2]) if len(sys.argv) > 2 else 120
BEAT = 60 / BPM
N = {'C3': 130.81, 'F2': 87.31, 'G2': 98.0, 'C2': 65.41, 'C4': 261.63, 'D4': 293.66, 'E4': 329.63, 'F4': 349.23,
     'G4': 392.0, 'A4': 440.0, 'B3': 246.94, 'C5': 523.25, 'E5': 659.25, 'G5': 783.99}
# refren: 8 taktów po 4 ćwierćnuty
MEL = [('E4', 1), ('E4', 1), ('E4', 2), ('E4', 1), ('E4', 1), ('E4', 2), ('E4', 1), ('G4', 1), ('C4', 1.5), ('D4', .5),
       ('E4', 4), ('F4', 1), ('F4', 1), ('F4', 1.5), ('F4', .5), ('F4', 1), ('E4', 1), ('E4', 1), ('E4', .5), ('E4', .5),
       ('G4', 1), ('G4', 1), ('F4', 1), ('D4', 1), ('C4', 4)]
CHORDS = ['C', 'C', 'C', 'C', 'F', 'C', 'G', 'C']
ROOT = {'C': ('C2', ['C4', 'E4', 'G4']), 'F': ('F2', ['F4', 'A4', 'C5']), 'G': ('G2', ['G4', 'B3', 'D4'])}
total = 32 * BEAT + 1.5
out = np.zeros(int(total * SR) + SR)


def add(sig, t):
    i = int(t * SR)
    out[i:i + len(sig)] += sig[:len(out) - i]


def bell(f, dur, amp):
    n = int((dur + 1.2) * SR); t = np.arange(n) / SR
    env = np.exp(-t * 3.2)
    mod = 2.1 * np.exp(-t * 6) * np.sin(2 * np.pi * f * 3.5 * t)
    s = np.sin(2 * np.pi * f * t + mod) + 0.25 * np.sin(2 * np.pi * f * 2 * t) * np.exp(-t * 5)
    att = np.minimum(1, t / 0.004)
    return amp * s * env * att


def bass(f, dur, amp):
    n = int(dur * SR); t = np.arange(n) / SR
    s = np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * 2 * f * t)
    return amp * s * np.exp(-t * 2.5) * np.minimum(1, t / 0.01)


def pad(fs, dur, amp):
    n = int(dur * SR); t = np.arange(n) / SR
    s = sum(np.sin(2 * np.pi * f * t) + 0.5 * np.sin(2 * np.pi * f * 1.003 * t) for f in fs)
    env = np.minimum(1, t / 0.3) * np.minimum(1, (dur - t) / 0.4).clip(0)
    return amp * s * env


rng = np.random.default_rng(7)


def sleigh(amp):
    n = int(0.09 * SR); t = np.arange(n) / SR
    noise = rng.standard_normal(n)
    hp = np.diff(np.concatenate([[0], noise]))  # prosty filtr górnoprzepustowy
    tone = sum(np.sin(2 * np.pi * f * t) for f in (5200, 6900, 8400))
    return amp * (0.6 * hp + 0.4 * tone) * np.exp(-t * 45)


def kick(amp):
    n = int(0.25 * SR); t = np.arange(n) / SR
    f = 110 * np.exp(-t * 18) + 45
    return amp * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 14)


t0 = 0.0
for note, d in MEL:
    add(bell(N[note], d * BEAT, 0.33), t0)
    add(bell(N[note] * 2, d * BEAT, 0.06), t0)
    t0 += d * BEAT
for bar, ch in enumerate(CHORDS):
    root, tri = ROOT[ch]
    bt = bar * 4 * BEAT
    add(pad([N[x] / 2 for x in tri], 4 * BEAT, 0.035), bt)
    for k in (0, 2):
        add(bass(N[root], 1.6 * BEAT, 0.32), bt + k * BEAT)
    for k in range(4):
        add(kick(0.28), bt + k * BEAT)
    for k in range(8):
        add(sleigh(0.10 if k % 2 else 0.16), bt + k * BEAT / 2)
# lekkie „pogłos” z kilku odbić
rev = out.copy()
for dly, g in ((0.073, .25), (0.131, .18), (0.197, .12), (0.271, .08)):
    rev[int(dly * SR):] += g * out[:-int(dly * SR)]
rev = rev[:int(total * SR)]
rev /= np.max(np.abs(rev)) * 1.12
pcm = (rev * 32767).astype(np.int16)
with wave.open(OUT, 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print('gotowe:', OUT, round(len(pcm) / SR, 2), 's')
