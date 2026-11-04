"""Montaż reklamy pionowej 1080x1920 z jednego pliku konfiguracyjnego JSON.

Użycie:  python3 -I montaz.py config.json

Co robi:
  1. tnie ujęcia z klipów (1080x1920, 30 fps, bez dźwięku) i skleja je,
  2. pierwsze sekundy: DUŻY hook (biały tekst z obrysem, bez tła) – potem znika,
  3. napisy do lektora: zwykłe, białe, cienki obrys, lekko przezroczyste, bez tła,
  4. koniec: rozmyte tło + karta z logo + kremowa ramka z wezwaniem do zakupu (CTA),
  5. dźwięk: delikatne odszumianie, stałe podbicie do ~-15 LUFS (bez pompowania), ogranicznik szczytów, wyciszenie na końcu.

config.json (przykład):
{
  "out": "reklama.mp4",
  "voice": "lektor.mp3",
  "duration": 22.05,                       # = długość lektora
  "hook": {"lines": ["Nie musisz już", "leżeć pod kocem"], "emoji": "emoji/1f64c.png", "until": 2.5},
  "subs": [[0.05, 1.15, "Nie musisz już leżeć"], [1.15, 2.38, "pod kocem w trudne dni."]],
  "end": 18.69,                            # od tej sekundy plansza końcowa
  "logo": "logo.png",                      # PNG z przezroczystym tłem (opcjonalnie)
  "logo_url": "twojsklep.pl",
  "cta": {"lines": ["BLACK MONTH", "Drugi zestaw -50%", "Zamów na twojsklep.pl"], "emoji": "emoji/1f447.png"},
  "end_blur": 6,                           # rozmycie tła planszy końcowej (0 = ostre, 18 = mocne)
  "segments": [["klip1.mp4", 0.0, 2.4], ["klip2.mp4", 1.2, 0.95, 0.25]]
}
segments: [plik, start_s, długość_s, (opcjonalnie) przytnij_gore]. przytnij_gore = ułamek wysokości
odcinany od góry (np. 0.25), obraz jest przybliżany do 1080x1920 – sposób na cudze napisy u góry kadru
bez używania rozmytych wersji „bez napisów”.
Suma długości segmentów powinna być równa "duration".
Wymaga: ffmpeg, Python 3 + Pillow, font Inter (Debian/Ubuntu: pakiet fonts-inter).
"""
import json
import os
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1080, 1920
FONT_DIR = '/usr/share/fonts/opentype/inter'
F_HOOK = ImageFont.truetype(f'{FONT_DIR}/Inter-ExtraBold.otf', 84)
F_SUB = ImageFont.truetype(f'{FONT_DIR}/Inter-Bold.otf', 48)
F_CTA = ImageFont.truetype(f'{FONT_DIR}/Inter-ExtraBold.otf', 64)
F_URL = ImageFont.truetype(f'{FONT_DIR}/Inter-SemiBold.otf', 38)
INK, CREAM = (59, 42, 33, 255), (255, 248, 240, 252)


def wrap(text, font, maxw):
    words, lines, cur = text.split(), [], ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if font.getlength(t) <= maxw:
            cur = t
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    return lines


def paste_emoji(img, path, x, y, size):
    if path and os.path.exists(path):
        e = Image.open(path).convert('RGBA').resize((size, size), Image.LANCZOS)
        img.alpha_composite(e, (int(x), int(y)))


def plain(img, lines, font, cy, lh, stroke, alpha=255, emoji=None):
    """Biały tekst z czarnym obrysem i miękkim cieniem, BEZ tła. cy = środek w ułamku wysokości."""
    esz = int(font.size * 1.05)
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    y0 = cy * H - lh * len(lines) / 2
    last_end = (0, 0)
    for i, line in enumerate(lines):
        extra = esz + 14 if emoji and i == len(lines) - 1 else 0
        x = (W - font.getlength(line) - extra) / 2
        d.text((x, y0 + i * lh), line, font=font, fill=(255, 255, 255, alpha),
               stroke_width=stroke, stroke_fill=(0, 0, 0, int(alpha * 0.85)))
        last_end = (x + font.getlength(line) + 8, y0 + i * lh)
    shadow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    shadow.putalpha(layer.split()[3].point(lambda a: int(a * 0.35)))
    img.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(8)), (0, 4))
    img.alpha_composite(layer)
    if emoji:
        paste_emoji(img, emoji, last_end[0], last_end[1] + 6, esz)


def cream_box(img, lines, font, cy, lh, emoji=None):
    """Kremowa zaokrąglona ramka z ciemnym tekstem (do planszy końcowej z CTA)."""
    esz = int(font.size * 1.05)
    widths = [font.getlength(l) for l in lines]
    if emoji:
        widths[-1] += esz + 14
    bw, bh = int(max(widths) + 96), lh * len(lines) + 56
    bx, by = (W - bw) // 2, int(cy * H - bh / 2)
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((bx, by + 8, bx + bw, by + bh + 8), 32, fill=(0, 0, 0, 80))
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(12)))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((bx, by, bx + bw, by + bh), 32, fill=CREAM)
    ty = by + 28 - 4
    for i, (line, w) in enumerate(zip(lines, widths)):
        x = (W - w) / 2
        d.text((x, ty + i * lh), line, font=font, fill=INK)
        if emoji and i == len(lines) - 1:
            paste_emoji(img, emoji, x + font.getlength(line) + 8, ty + i * lh + 4, esz)


def logo_card(img, logo_path, url, top_frac=0.07):
    """Kremowa karta z logo i adresem sklepu u góry ekranu."""
    if not logo_path or not os.path.exists(logo_path):
        return
    logo = Image.open(logo_path).convert('RGBA')
    lw = 380
    logo = logo.resize((lw, int(logo.height * lw / logo.width)), Image.LANCZOS)
    bw, bh = lw + 120, logo.height + 50 + 40 + 44
    bx, by = (W - bw) // 2, int(H * top_frac)
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((bx, by + 10, bx + bw, by + bh + 10), 40, fill=(0, 0, 0, 80))
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14)))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((bx, by, bx + bw, by + bh), 40, fill=(255, 251, 245, 248))
    img.alpha_composite(logo, ((W - lw) // 2, by + 44))
    if url:
        d.text(((W - F_URL.getlength(url)) / 2, by + 44 + logo.height + 22), url, font=F_URL, fill=(110, 80, 62, 255))


def main(cfg_path):
    cfg = json.load(open(cfg_path))
    base = os.path.dirname(os.path.abspath(cfg_path))
    p = lambda x: x if os.path.isabs(x) else os.path.join(base, x)
    D, end = float(cfg['duration']), float(cfg['end'])
    hook = cfg.get('hook') or {}
    hook_until = float(hook.get('until', 0))
    work = tempfile.mkdtemp(prefix='montaz_')

    # 1) cięcie i sklejanie ujęć
    names = []
    for i, seg in enumerate(cfg['segments']):
        src, start, dur = seg[:3]
        top = float(seg[3]) if len(seg) > 3 else 0.0
        crop = f'crop=iw*{1 - top}:ih*{1 - top}:iw*{top / 2}:ih*{top},' if top > 0 else ''
        out = f'{work}/c{i:02d}.mp4'
        subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-ss', str(start), '-i', p(src), '-t', str(dur), '-an',
                        '-vf', f'{crop}scale=1080:1920:flags=lanczos,fps=30,setsar=1', '-c:v', 'libx264', '-preset', 'fast', '-crf', '18',
                        '-pix_fmt', 'yuv420p', out], check=True)
        names.append(out)
    with open(f'{work}/list.txt', 'w') as f:
        f.writelines(f"file '{n}'\n" for n in names)
    joined = f'{work}/joined.mp4'
    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', f'{work}/list.txt',
                    '-c', 'copy', joined], check=True)

    # 2) plansze: jedna pełnoekranowa nakładka PNG na każdy odcinek czasu
    subs = cfg.get('subs', [])
    cont = []  # napis trwa do początku następnego, żeby nie migał
    for i, (a, b, t) in enumerate(subs):
        nxt = subs[i + 1][0] if i + 1 < len(subs) else D
        cont.append((a, nxt, t))
    cuts = sorted({round(x, 3) for x in [0, D, end, hook_until] + [c[0] for c in cont] if 0 <= x <= D})
    overlays = []
    for i in range(len(cuts) - 1):
        a, b = cuts[i], cuts[i + 1]
        mid = (a + b) / 2
        img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        if mid < hook_until and hook.get('lines'):
            plain(img, hook['lines'], F_HOOK, 0.30, 100, 6, 255, p(hook['emoji']) if hook.get('emoji') else None)
        if hook_until <= mid < end:
            txt = next((t for s0, s1, t in cont if s0 <= mid < s1), '')
            if txt:
                plain(img, wrap(txt, F_SUB, 880), F_SUB, 0.66, 60, 3, 225)
        if mid >= end:
            logo_card(img, p(cfg['logo']) if cfg.get('logo') else None, cfg.get('logo_url', ''))
            cta = cfg.get('cta') or {}
            if cta.get('lines'):
                cream_box(img, cta['lines'], F_CTA, 0.385, 80, p(cta['emoji']) if cta.get('emoji') else None)
        path = f'{work}/o{i:02d}.png'
        img.save(path)
        overlays.append((path, a, b))

    # 3) składanie: rozmycie końcówki, nakładki, lektor
    cmd = ['ffmpeg', '-nostdin', '-v', 'error', '-y', '-i', joined, '-i', p(cfg['voice'])]
    for path, _, _ in overlays:
        cmd += ['-i', path]
    blur = int(cfg.get('end_blur', 6))
    fc = (f"[0:v]boxblur=luma_radius={blur}:luma_power=2:enable='gte(t,{end})',eq=brightness=-0.06:enable='gte(t,{end})'[v0]"
          if blur > 0 else f"[0:v]eq=brightness=-0.06:enable='gte(t,{end})'[v0]")
    last = 'v0'
    for i, (_, a, b) in enumerate(overlays):
        fc += f";[{last}][{i + 2}:v]overlay=0:0:enable='between(t,{a},{b - 0.001})'[v{i + 1}]"
        last = f'v{i + 1}'
    # dźwięk: delikatne odszumianie, potem STAŁE podbicie do ~-15 LUFS i łagodny ogranicznik szczytów
    # (bez dynamicznego loudnorm, który pompował głośność i podbijał szum tła z ElevenLabs)
    pre = 'highpass=f=80,afftdn=nf=-45:nr=12'
    meas = subprocess.run(['ffmpeg', '-nostdin', '-hide_banner', '-i', p(cfg['voice']), '-af', f'{pre},ebur128',
                           '-f', 'null', '-'], capture_output=True, text=True).stderr
    integ = float(meas[meas.rindex('I:'):].split()[1])
    gain = max(-10.0, min(15.0, -15.0 - integ))
    fc += (f";[1:a]{pre},volume={gain:.2f}dB,alimiter=limit=0.89:attack=5:release=50:level=false,"
           f"apad,atrim=0:{D},afade=t=out:st={D - 0.3}:d=0.3[a]")
    cmd += ['-filter_complex', fc, '-map', f'[{last}]', '-map', '[a]', '-c:v', 'libx264', '-preset', 'slow', '-crf', '18',
            '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', '-t', str(D), p(cfg['out'])]
    subprocess.run(cmd, check=True)
    print('gotowe:', p(cfg['out']))


if __name__ == '__main__':
    main(sys.argv[1])
