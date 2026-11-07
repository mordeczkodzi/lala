"""Robi wersję 9:16 (1080x1920) z grafiki 4:5 do Stories i Reels.

Grafika zostaje cała, na środku, w bezpiecznej strefie (ok. 250 px od góry,
ok. 285 px od dołu nic nie zasłania interfejs). Górę i dół dopełnia
mocno rozmyta, powiększona ta sama grafika, żeby nie było pustych pasów.

Użycie: python story_916.py wejscie.jpg wyjscie.jpg
"""
import sys
from PIL import Image, ImageFilter

W, H = 1080, 1920


def make(src, dst):
    im = Image.open(src).convert("RGB")
    s = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    top = (H - s.height) // 2
    bot = H - top - s.height
    canvas = Image.new("RGB", (W, H))

    # tło: ta sama grafika powiększona do całego kadru i mocno rozmyta
    k = max(W / im.width, H / im.height)
    bg = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
    l, t = (bg.width - W) // 2, (bg.height - H) // 2
    canvas.paste(bg.crop((l, t, l + W, t + H)).filter(ImageFilter.GaussianBlur(45)), (0, 0))
    # miękkie łączenie: 60 px gradientu na krawędziach grafiki
    mask = Image.new("L", s.size, 255)
    f = 60
    px = mask.load()
    for y in range(f):
        a = round(255 * y / f)
        for x in range(W):
            px[x, y] = a
            px[x, s.height - 1 - y] = a
    canvas.paste(s, (0, top), mask)
    canvas.save(dst, quality=93)
    print(dst, canvas.size, "grafika od y =", top, "do", top + s.height)


if __name__ == "__main__":
    make(sys.argv[1], sys.argv[2])
