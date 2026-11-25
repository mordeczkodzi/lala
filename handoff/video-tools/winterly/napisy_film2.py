"""Napisy w stylu FILMU 2 (zwycięska reklama): nakłada je na gotowy, czysty montaż (bez napisów).
- hook: duży biały tekst z cienkim czarnym obrysem + emoji, ok. 30% wysokości,
- napisy: małe, białe, jedno zdanie, bez emoji i bez kolorowych słów, z delikatnym cieniem, ok. 66% wysokości,
- plansza końcowa: lekko rozmyte tło (bez przyciemniania) i jasna zaokrąglona plakietka z czarnym tekstem.
Użycie: python3 -I napisy_film2.py napisy.json   (pola: in, out, emoji_dir, hook{lines,emoji,until}, subs[[od,do,tekst]], end{from,lines})
"""
import json, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont
W, H, FPS = 1080, 1920, 30
FD = '/usr/share/fonts/opentype/inter/'
cfg = json.load(open(sys.argv[1])); base = os.path.dirname(os.path.abspath(sys.argv[1]))
P = lambda x: x if os.path.isabs(x) else os.path.join(base, x)
F_HOOK = ImageFont.truetype(FD + 'Inter-Bold.otf', 74); F_SUB = ImageFont.truetype(FD + 'Inter-SemiBold.otf', 41)
F_END = ImageFont.truetype(FD + 'Inter-Bold.otf', 54)

def emoji(code, size):
    f = os.path.join(cfg.get('emoji_dir', ''), code + '.png')
    if not os.path.exists(f): f = os.path.join(cfg.get('emoji_dir', ''), code + '-fe0f.png')
    return Image.open(f).convert('RGBA').resize((size, size), Image.LANCZOS) if os.path.exists(f) else None

def hook_img(lines, code):
    em = emoji(code, 70) if code else None; lh = 88; pad = 24
    ws = [F_HOOK.getlength(l) + (78 if (em and i == len(lines) - 1) else 0) for i, l in enumerate(lines)]
    img = Image.new('RGBA', (int(max(ws)) + 2 * pad, lh * len(lines) + 2 * pad), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    for i, l in enumerate(lines):
        x = (img.width - ws[i]) / 2; y = pad + i * lh
        d.text((x, y), l, font=F_HOOK, fill='white', stroke_width=3, stroke_fill=(20, 20, 20))
        if em and i == len(lines) - 1: img.alpha_composite(em, (int(x + F_HOOK.getlength(l) + 8), int(y + 8)))
    sh = Image.new('RGBA', img.size, (0, 0, 0, 0)); sh.putalpha(img.split()[3].point(lambda a: int(a * 0.35)))
    out = Image.new('RGBA', img.size, (0, 0, 0, 0)); out.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8))); out.alpha_composite(img)
    return out

SUB_MAXW = 760  # bezpieczna szerokość: nie wchodzi pod przyciski Reels/TikTok po prawej

def wrap(text, font, maxw):
    """Łamie zdanie na maks. 2 wyrównane linie (dzieli w miejscu, gdzie obie są najbardziej równe)."""
    if font.getlength(text) <= maxw: return [text]
    words = text.split(); best = None
    for i in range(1, len(words)):
        a, b = ' '.join(words[:i]), ' '.join(words[i:]); w = max(font.getlength(a), font.getlength(b))
        if best is None or w < best[0]: best = (w, [a, b])
    return best[1]

def sub_img(text):
    lines = [l for part in text.split('|') for l in wrap(part, F_SUB, SUB_MAXW)]
    pad = 22; lh = 54; ws = [F_SUB.getlength(l) for l in lines]
    img = Image.new('RGBA', (int(max(ws)) + 2 * pad, lh * len(lines) + 2 * pad), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    for i, l in enumerate(lines):
        d.text(((img.width - ws[i]) / 2, pad + i * lh), l, font=F_SUB, fill='white', stroke_width=2, stroke_fill=(0, 0, 0, 150))
    sh = Image.new('RGBA', img.size, (0, 0, 0, 0)); sh.putalpha(img.split()[3].point(lambda a: int(a * 0.85)))
    out = Image.new('RGBA', img.size, (0, 0, 0, 0)); out.alpha_composite(sh.filter(ImageFilter.GaussianBlur(5)), (0, 3)); out.alpha_composite(img)
    return out

def end_card(lines):
    lh = 76; padx, pady = 52, 30
    parts = [l.split('|') for l in lines]  # "tekst|emoji_kod"
    ws = [F_END.getlength(p[0]) + (62 if len(p) > 1 else 0) for p in parts]
    bw, bh = int(max(ws)) + 2 * padx, lh * len(lines) + 2 * pady
    k = min(1.0, 980 / bw)
    img = Image.new('RGBA', (bw, bh), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, bw - 1, bh - 1), 34, fill=(250, 244, 236, 242))
    for i, p in enumerate(parts):
        x = (bw - ws[i]) / 2; y = pady + i * lh + 4
        d.text((x, y), p[0], font=F_END, fill=(24, 20, 18))
        if len(p) > 1:
            e = emoji(p[1], 54)
            if e: img.alpha_composite(e, (int(x + F_END.getlength(p[0]) + 8), int(y + 2)))
    return img.resize((int(bw * k), int(bh * k)), Image.LANCZOS) if k < 1 else img

def place(fr, im, cx, cy, a=1.0):
    if a < 1: im = im.copy(); im.putalpha(im.split()[3].point(lambda v: int(v * a)))
    fr.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))

hk = cfg.get('hook'); HOOK = hook_img(hk['lines'], hk.get('emoji')) if hk else None
SUBS = [(a, b, sub_img(t)) for a, b, t in cfg['subs']]
EC = cfg['end']; CARD = end_card(EC['lines'])
src = P(cfg['in']); dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', src], capture_output=True, text=True).stdout)
dec = subprocess.Popen(['ffmpeg', '-nostdin', '-v', 'error', '-i', src, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
enc = subprocess.Popen(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                        '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', P(cfg['out'])], stdin=subprocess.PIPE)
n = int(round(dur * FPS)); last = None
for k in range(n):
    t = k / FPS; raw = dec.stdout.read(W * H * 3)
    if len(raw) == W * H * 3: last = raw
    fr = Image.frombytes('RGB', (W, H), last)
    if t >= EC['from']:
        te = t - EC['from']; fr = fr.filter(ImageFilter.GaussianBlur(min(1, te / 0.3) * EC.get('blur', 6)))
        fr = fr.convert('RGBA'); place(fr, CARD, W / 2, H * EC.get('y', 0.385), min(1, te / 0.2))
    else:
        fr = fr.convert('RGBA')
        if HOOK and t < hk['until']: place(fr, HOOK, W / 2, H * hk.get('y', 0.3))
        for a, b, im in SUBS:
            if a <= t < b: place(fr, im, W / 2, H * cfg.get('sub_y', 0.66))
    enc.stdin.write(fr.convert('RGB').tobytes())
enc.stdin.close(); enc.wait(); dec.kill(); print('OK', P(cfg['out']))
