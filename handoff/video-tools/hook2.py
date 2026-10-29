import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
out, lines = sys.argv[1], sys.argv[2].split('|')
W, H = 1080, 1920
font = ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf', 66)
lh, padx, pady = 80, 40, 26
bw = int(max(font.getlength(l) for l in lines) + 2 * padx); bh = lh * len(lines) + 2 * pady
bx, by = (W - bw) // 2, int(H * 0.18)
img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle((bx, by + 8, bx + bw, by + bh + 8), 34, fill=(0, 0, 0, 90))
img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(12)))
d = ImageDraw.Draw(img); d.rounded_rectangle((bx, by, bx + bw, by + bh), 34, fill=(255, 248, 240, 245))
for i, l in enumerate(lines):
    d.text(((W - font.getlength(l)) / 2, by + pady - 4 + i * lh), l, font=font, fill=(59, 42, 33, 255))
img.save(out)
