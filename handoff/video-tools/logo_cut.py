import sys
from PIL import Image
src, out = sys.argv[1], sys.argv[2]
im = Image.open(src).convert('RGB')
crop = im.crop((395, 20, 730, 145))
bg = crop.getpixel((3, 3))
px = crop.load(); w, h = crop.size
res = Image.new('RGBA', (w, h))
rp = res.load()
for y in range(h):
    for x in range(w):
        r, g, b = px[x, y]
        d = ((r-bg[0])**2 + (g-bg[1])**2 + (b-bg[2])**2) ** 0.5
        a = max(0, min(255, int((d - 18) * 4)))
        rp[x, y] = (r, g, b, a)
bbox = res.getbbox(); res = res.crop(bbox)
print('bg', bg, 'size', res.size)
res.save(out)
