import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
out, text, emoji = sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else ''
W, H = 1080, 1920
font = ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf', 72)
esz = 70 if emoji else 0
tw = font.getlength(text) + (esz + 14 if emoji else 0)
padx, pady = 44, 30
bw, bh = int(tw + 2 * padx), 72 + 2 * pady + 6
bx, by = (W - bw) // 2, int(H * 0.20)
img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle((bx, by + 8, bx + bw, by + bh + 8), 34, fill=(0, 0, 0, 90))
img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(12)))
d = ImageDraw.Draw(img)
d.rounded_rectangle((bx, by, bx + bw, by + bh), 34, fill=(255, 248, 240, 245))
x = bx + padx; y = by + pady - 4
d.text((x, y), text, font=font, fill=(59, 42, 33, 255))
if emoji:
    e = Image.open(emoji).convert('RGBA').resize((esz, esz), Image.LANCZOS)
    img.alpha_composite(e, (int(x + font.getlength(text) + 14), by + (bh - esz) // 2))
img.save(out)
