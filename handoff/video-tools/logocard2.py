import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
logo_p, out = sys.argv[1], sys.argv[2]
W, H = 1080, 1920
logo = Image.open(logo_p).convert('RGBA')
lw = 380; logo = logo.resize((lw, int(logo.height * lw / logo.width)), Image.LANCZOS)
font = ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-SemiBold.otf', 38)
url = 'otully.pl'
bw, bh = lw + 120, logo.height + 50 + 40 + 44
bx, by = (W - bw) // 2, int(H * float(sys.argv[3]))
img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle((bx, by + 10, bx + bw, by + bh + 10), 40, fill=(0, 0, 0, 80))
img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14)))
d = ImageDraw.Draw(img); d.rounded_rectangle((bx, by, bx + bw, by + bh), 40, fill=(255, 251, 245, 248))
img.alpha_composite(logo, ((W - lw) // 2, by + 44))
d.text(((W - font.getlength(url)) / 2, by + 44 + logo.height + 22), url, font=font, fill=(110, 80, 62, 255))
img.save(out)
