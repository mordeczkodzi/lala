import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
out, n = sys.argv[1], sys.argv[2]
W, H = 1080, 1920; r = 78; cx, cy = 140, int(H * 0.36)
img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).ellipse((cx - r, cy - r + 8, cx + r, cy + r + 8), fill=(0, 0, 0, 90))
img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)))
d = ImageDraw.Draw(img); d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(246, 168, 128, 250))
f = ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf', 104)
bb = d.textbbox((0, 0), n, font=f); d.text((cx - (bb[2] + bb[0]) / 2, cy - (bb[3] + bb[1]) / 2), n, font=f, fill=(59, 42, 33, 255))
img.save(out)
