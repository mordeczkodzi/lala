"""Składa gotową reklamę: obraz + lektor + hook + napisy + plakietki + plansza z logo na końcu.

Użycie:  python3 -I render.py config.json

config.json:
{
  "base": "pracownia/v/joined.mp4",          # sklejony obraz z cut.sh
  "audio": "lektor.mp3",                     # nagranie z ElevenLabs
  "subs": "pracownia/subs/meta.json",        # wynik subs_json.py
  "hook": ["pracownia/hook.png", 3.0],       # plansza hooka i do której sekundy ją pokazywać
  "end": 18.2,                               # od tej sekundy rozmycie + karta z logo
  "card": "assets/logocard_mid.png",
  "badges": [["badge3.png", 3.5, 9.2]],      # opcjonalne plakietki [plik, od, do]
  "duration": 20.2,                          # długość filmu = długość lektora
  "out": "Otulka_FilmX_final.mp4"
}
"""
import json
import subprocess
import sys

cfg = json.load(open(sys.argv[1]))
meta = json.load(open(cfg['subs']))
badges = cfg.get('badges', [])
D, e = cfg['duration'], cfg['end']
hook_png, hook_until = cfg['hook']

cmd = ['ffmpeg', '-v', 'error', '-y', '-i', cfg['base'], '-i', cfg['audio'], '-i', hook_png, '-i', cfg['card']]
for p, _, _ in badges:
    cmd += ['-i', p]
for p, _, _ in meta:
    cmd += ['-i', p]

# końcówka: lekko rozmyte i rozjaśnione tło, na nim karta z logo (nie zasłania twarzy)
fc = (f"[0:v]boxblur=luma_radius=18:luma_power=2:enable='gte(t,{e})',eq=brightness=0.04:enable='gte(t,{e})'[b0];"
      f"[b0][2:v]overlay=0:0:enable='lte(t,{hook_until})'[c0];[c0][3:v]overlay=0:0:enable='gte(t,{e})'[c1]")
last, idx = 'c1', 4
for j, (p, a, b) in enumerate(badges):
    fc += f";[{last}][{idx}:v]overlay=0:0:enable='between(t,{a},{b})'[g{j}]"
    last, idx = f'g{j}', idx + 1
for i, (p, a, b) in enumerate(meta):
    fc += f";[{last}][{idx}:v]overlay=0:0:enable='between(t,{a},{b})'[s{i}]"
    last, idx = f's{i}', idx + 1
# głośność pod Reels/TikTok: -14 LUFS, wyciszenie na ostatnie 0.3 s
fc += f";[1:a]loudnorm=I=-14:TP=-1.5:LRA=11,apad,atrim=0:{D},afade=t=out:st={D - 0.3}:d=0.3[a]"

cmd += ['-filter_complex', fc, '-map', f'[{last}]', '-map', '[a]',
        '-c:v', 'libx264', '-preset', 'slow', '-crf', '18', '-pix_fmt', 'yuv420p',
        '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', '-t', str(D), cfg['out']]
subprocess.run(cmd, check=True)
print('gotowe:', cfg['out'])
