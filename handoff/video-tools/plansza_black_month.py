"""Plansza końcowa „Black Month” (PNG 1080x1920 z przezroczystym tłem) do montaz.py (klucz "end_card").
Użycie: python3 plansza_black_month.py config.json wyjscie.png
Wersja z małymi cenami: "small_prices": true, "headline": "do −190 zł", "headline_sub": "...", "fine": "..."
config: {"title": "BLACK MONTH", "product": "...", "price": "239,99 zł", "old": "309,99 zł", "save": "−70 zł",
         "extra": "Przy 2 sztukach oszczędzasz 190 zł", "cta": "Zamów na winterly.pl", "sparkle": "emoji/2728.png",
         "point": "emoji/1f447.png"}"""
import json, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1080, 1920
FD = '/usr/share/fonts/opentype/inter/'
F = lambda name, size: ImageFont.truetype(FD + name, size)
GOLD, GOLD_SOFT, CREAM, BERRY = (242, 193, 78, 255), (244, 232, 196, 255), (255, 246, 230, 255), (142, 31, 47, 255)

cfg = json.load(open(sys.argv[1]))
img = Image.new('RGBA', (W, H), (0, 0, 0, 0))


def center(d, y, text, font, fill, spacing=0):
    if spacing:
        widths = [font.getlength(ch) for ch in text]
        total = sum(widths) + spacing * (len(text) - 1)
        x = (W - total) / 2
        for ch, w in zip(text, widths):
            d.text((x, y), ch, font=font, fill=fill)
            x += w + spacing
        return
    d.text(((W - font.getlength(text)) / 2, y), text, font=font, fill=fill)


# karta: ciemna zieleń z gradientem, złota ramka, cień
cx0, cx1, cy0, cy1 = 80, W - 80, 470, 1180
shadow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
ImageDraw.Draw(shadow).rounded_rectangle((cx0, cy0 + 18, cx1, cy1 + 18), 48, fill=(0, 0, 0, 140))
img.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(26)))
grad = Image.new('RGBA', (cx1 - cx0, cy1 - cy0))
gd = ImageDraw.Draw(grad)
for y in range(cy1 - cy0):
    k = y / (cy1 - cy0)
    gd.line([(0, y), (cx1 - cx0, y)], fill=(int(24 - 10 * k), int(64 - 30 * k), int(46 - 20 * k), 238))
mask = Image.new('L', grad.size, 0)
ImageDraw.Draw(mask).rounded_rectangle((0, 0, grad.width - 1, grad.height - 1), 48, fill=255)
img.paste(grad, (cx0, cy0), mask)
d = ImageDraw.Draw(img)
d.rounded_rectangle((cx0, cy0, cx1, cy1), 48, outline=(201, 162, 39, 255), width=4)
d.rounded_rectangle((cx0 + 14, cy0 + 14, cx1 - 14, cy1 - 14), 38, outline=(201, 162, 39, 90), width=2)

# BLACK MONTH z iskierkami
ft = F('Inter-Black.otf', 98)
center(d, cy0 + 62, cfg['title'], ft, GOLD, spacing=6)
if cfg.get('sparkle'):
    sp = Image.open(cfg['sparkle']).convert('RGBA').resize((64, 64), Image.LANCZOS)
    tw = sum(ft.getlength(c) for c in cfg['title']) + 6 * (len(cfg['title']) - 1)
    img.alpha_composite(sp, (int((W - tw) / 2 - 80), cy0 + 82))
    img.alpha_composite(sp, (int((W + tw) / 2 + 16), cy0 + 82))
center(d, cy0 + 186, cfg['product'], F('Inter-SemiBold.otf', 48), CREAM)
d.line([(W / 2 - 150, cy0 + 268), (W / 2 + 150, cy0 + 268)], fill=(201, 162, 39, 200), width=3)

# rabat na pierwszym planie, ceny małym druczkiem
if cfg.get('small_prices'):
    fh = F('InterDisplay-Black.otf', 150)
    center(d, cy0 + 296, cfg['headline'], fh, (255, 255, 255, 255))
    center(d, cy0 + 478, cfg['headline_sub'], F('Inter-Bold.otf', 46), GOLD_SOFT)
    fine = cfg['fine'] if isinstance(cfg['fine'], list) else [cfg['fine']]
    for i, line in enumerate(fine):
        center(d, cy0 + 572 + i * 42, line, F('Inter-Medium.otf', 31), (255, 246, 230, 170))
else:
    fp, fo = F('InterDisplay-Black.otf', 150), F('Inter-Medium.otf', 54)
    center(d, cy0 + 300, cfg['price'], fp, (255, 255, 255, 255))
    ow = fo.getlength(cfg['old'])
    fs = F('Inter-ExtraBold.otf', 46)
    sw = fs.getlength(cfg['save']) + 44
    row_w = ow + 26 + sw
    ox, oy = (W - row_w) / 2, cy0 + 488
    d.text((ox, oy), cfg['old'], font=fo, fill=(255, 246, 230, 150))
    d.line([(ox - 4, oy + 33), (ox + ow + 4, oy + 33)], fill=(255, 246, 230, 190), width=4)
    px = ox + ow + 26
    d.rounded_rectangle((px, oy - 4, px + sw, oy + 66), 35, fill=BERRY)
    d.text((px + 22, oy + 4), cfg['save'], font=fs, fill=(255, 255, 255, 255))
    center(d, cy0 + 600, cfg['extra'], F('Inter-Bold.otf', 44), GOLD_SOFT)

# przycisk CTA pod kartą
fc = F('Inter-ExtraBold.otf', 56)
cw = fc.getlength(cfg['cta']) + (78 if cfg.get('point') else 0)
bx0, by0 = (W - cw) / 2 - 56, cy1 + 70
bx1, by1 = (W + cw) / 2 + 56, by0 + 124
sh = Image.new('RGBA', (W, H), (0, 0, 0, 0))
ImageDraw.Draw(sh).rounded_rectangle((bx0, by0 + 14, bx1, by1 + 14), 62, fill=(80, 10, 20, 150))
img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(18)))
d = ImageDraw.Draw(img)
d.rounded_rectangle((bx0, by0, bx1, by1), 62, fill=BERRY)
d.rounded_rectangle((bx0, by0, bx1, by1), 62, outline=(242, 193, 78, 200), width=3)
tx = bx0 + 56
d.text((tx, by0 + 30), cfg['cta'], font=fc, fill=(255, 255, 255, 255))
if cfg.get('point'):
    pt = Image.open(cfg['point']).convert('RGBA').resize((64, 64), Image.LANCZOS)
    img.alpha_composite(pt, (int(tx + fc.getlength(cfg['cta']) + 14), int(by0 + 30)))
img.save(sys.argv[2])
print('gotowe:', sys.argv[2])
