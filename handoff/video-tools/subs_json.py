import sys, json
from PIL import Image, ImageDraw, ImageFont
outdir, chunks = sys.argv[1], json.load(open(sys.argv[2]))
W, H = 1080, 1920
font = ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf', 64)
def wrap(text, maxw=900):
    words, lines, cur = text.split(), [], ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if font.getlength(t) <= maxw: cur = t
        else: lines.append(cur); cur = w
    lines.append(cur); return lines
meta = []
for i, (a, b, t) in enumerate(chunks):
    img = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    lines = wrap(t); lh = 80; y = int(H * 0.60) - (len(lines) - 1) * lh // 2
    for j, ln in enumerate(lines):
        d.text(((W - font.getlength(ln)) / 2, y + j * lh), ln, font=font, fill=(255, 255, 255, 255), stroke_width=6, stroke_fill=(0, 0, 0, 255))
    p = f'{outdir}/s{i:02d}.png'; img.save(p); meta.append((p, a, b))
json.dump(meta, open(f'{outdir}/meta.json', 'w'))
