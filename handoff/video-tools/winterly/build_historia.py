"""Buduje config montażu „Winterly historia” (schemat filmu 2) z czasów zdań lektora.
Użycie: python3 build_historia.py czasy.json out_cfg.json
czasy.json: {"P1":[start,koniec], ... "P7":[start,koniec], "_total": dlugosc}
P1 Pięć minut montażu… | P2 i mój balkon stał się atrakcją osiedla | P3 Zawiesiłam lampki, odpaliłam aplikację i wybrałam Mikołaja na saniach
P4 Wieczorem wracam z psem, a pod blokiem ludzie patrzą w górę | P5 Śnieg, bałwan, choinka – jednym kliknięciem
P6 Rano sąsiad pyta na grupie, skąd mam takie lampki | P7 Winterly. Zamów na winterly.pl"""
import json, os, re, subprocess, sys
T = json.load(open(sys.argv[1])); r = lambda v: round(v, 3)
SRC = os.path.dirname(os.path.abspath(sys.argv[2])); _cuts = {}
def scene_cuts(f):  # cięcia w oryginale (żeby żadne ujęcie nie złapało sąsiedniej sceny)
    if f not in _cuts:
        o = subprocess.run(['ffmpeg', '-nostdin', '-i', os.path.join(SRC, f), '-vf', "select='gt(scene,0.2)',showinfo", '-an', '-f', 'null', '-'],
                           capture_output=True, text=True).stderr
        _cuts[f] = [float(m) for m in re.findall(r'pts_time:([0-9.]+)', o)]
    return _cuts[f]
S = lambda k: T[k][0]; E = lambda k: T[k][1]
frac = lambda k, f: S(k) + f * (E(k) - S(k))
cut = lambda t: r(t - 0.06)
c = {k: cut(S(k)) for k in ['P2', 'P3', 'P4', 'P5', 'P6', 'P7']}
end = r(T['_total'] + 1.3)
def beat(a, b, segs, subs):  # segs: (plik, start_zrodla, udzial albo None=reszta)
    dur = r(b - a); out = []; acc = 0.0
    for i, (f, st, ln) in enumerate(segs):
        ln = r(dur - acc) if ln is None else r(ln); acc += ln
        nxt = [x for x in scene_cuts(f) if x > st + 0.02]; avail = (nxt[0] - 0.05 - st) if nxt else 99
        if ln <= avail: out.append([f, st, ln])
        else:
            sp = r(avail / ln)
            if sp < 0.6: print(f'UWAGA: {f} od {st}s scena za krótka ({avail:.2f}s na {ln:.2f}s)')
            out.append([f, st, ln, 0, {"speed": max(sp, 0.6)}])
    return {"dur": dur, "segs": out, "subs": [[r(t - a)] + list(x) for t, *x in subs]}
p3a, p3b = cut(frac('P3', 0.30)), cut(frac('P3', 0.58))
p4a = cut(frac('P4', 0.45))
p5a, p5b, p5c = cut(frac('P5', 0.22)), cut(frac('P5', 0.42)), cut(frac('P5', 0.62))
p6a = cut(frac('P6', 0.50))
beats = [
 beat(0, c['P2'], [("s5.mp4", 3.25, None)], []),
 beat(c['P2'], c['P3'], [("s16.mp4", 21.65, (c['P3'] - c['P2']) / 2), ("s11.mp4", 32.4, None)],
      [(S('P2'), "i mój balkon stał się", None), (frac('P2', 0.45), "*atrakcją osiedla*", "2728")]),
 beat(c['P3'], p3a, [("s16.mp4", 7.15, None)], [(S('P3'), "Zawiesiłam *lampki*,", None)]),
 beat(p3a, p3b, [("s11.mp4", 2.2, None)], [(p3a + 0.06, "odpaliłam *aplikację*", "1f4f1")]),
 beat(p3b, c['P4'], [("s11.mp4", 26.55, None)], [(p3b + 0.06, "i wybrałam|*Mikołaja na saniach*", "1f385")]),
 beat(c['P4'], p4a, [("s11.mp4", 12.75, None)], [(S('P4'), "Wieczorem wracam z psem,", None)]),
 beat(p4a, c['P5'], [("s11.mp4", 10.45, None)], [(p4a + 0.06, "a pod blokiem ludzie|*patrzą w górę*", "1f440")]),
 beat(c['P5'], p5c, [("s20.mp4", 3.5, p5a - c['P5']), ("s18.mp4", 1.0, p5b - p5a), ("s19.mp4", 0.3, None)],
      [(S('P5'), "*Śnieg*,", "2744"), (p5a + 0.06, "*bałwan*,", "2603"), (p5b + 0.06, "*choinka*", "1f384")]),
 beat(p5c, c['P6'], [("s16.mp4", 1.15, None)], [(p5c + 0.06, "jednym *kliknięciem*", "1f446")]),
 beat(c['P6'], p6a, [("s11.mp4", 15.72, None)], [(S('P6'), "Rano *sąsiad* pyta na grupie,", None)]),
 beat(p6a, c['P7'], [("s11.mp4", 25.48, 0.9), ("s16.mp4", 5.32, None)], [(p6a + 0.06, "skąd mam *takie lampki*", "1f60d")]),
 beat(c['P7'], end, [("s5.mp4", 5.0, None)], []),
]
cfg = {"_opis": "Winterly historia (schemat filmu 2) – generowane z czasów lektora przez build_historia.py",
       "out": "historia_obraz.mp4", "emoji_dir": sys.argv[3] if len(sys.argv) > 3 else "emoji/64",
       "sub_y": 0.69, "punch": False, "dissolve": 0, "badge_from": c['P2'],
       "hook": {"lines": ["Sąsiedzi stoją", "pod moim *balkonem*"], "emoji": "1f440", "until": c['P2'], "y": 0.2},
       "stickers": [{"from": c['P4'], "to": c['P7'], "text": "BLACK WEEK: druga kurtyna −40%", "emoji": "1f525", "x": 0.5, "y": 0.235, "rot": -3}],
       "end_dur": r(end - c['P7']),
       "end": {"pill": "BLACK WEEK • druga kurtyna −40%", "pill_emoji": "1f525", "lines": ["Balkon,", "na który się *patrzy*"],
               "button": "ZAMÓW NA WINTERLY.PL", "small": "Płatność przy odbiorze • 30 dni na zwrot"},
       "beats": beats}
json.dump(cfg, open(sys.argv[2], 'w'), ensure_ascii=False, indent=1)
for b in beats: print(b['dur'], [tuple(s) for s in b['segs']])
print('koniec filmu', end)
