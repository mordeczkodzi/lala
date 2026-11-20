"""Montaż reklamy pionowej 1080x1920 dla Winterly (styl reklam A „Sąsiadka” i B „Konkurs”).

Film składa się z „bitów” (bit = jedno zdanie lektora). Każdy bit ma długość, ujęcia i napisy.
Efekty: pop-in napisów po 2–3 słowa, złote słowo (*słowo*), emoji Google, hak na górze,
plakietka winterly.pl, naklejki (np. BLACK FRIDAY), zasłanianie obcych napisów białą etykietą,
biały błysk przy zmianie wzoru, delikatne przenikanie na cięciach, plansza końcowa z przyciskiem.

Użycie:   python3 -I render_winterly.py config.json
Dźwięk:   ten skrypt robi sam obraz; głos i muzykę dokłada miks_audio.sh (osobno, żeby łatwo stroić).
Wymaga:   ffmpeg, Python 3 + Pillow, czcionka Inter (Inter-Black/Bold/ExtraBold), opcjonalnie emoji Google.
"""
import json, math, os, subprocess, sys, tempfile
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS = 1080, 1920, 30
GOLD, WHITE, INK = (255, 205, 72, 255), (255, 255, 255, 255), (30, 22, 18, 255)
RED, GREEN = (196, 30, 45, 255), (22, 120, 72, 255)
F_SUB = F_HOOK = F_LAB = F_PILL = F_BIG = F_BTN = F_SM = F_BADGE = None


def init_fonts(cfg, base):
    """Szuka czcionki Inter: config 'font_dir', zmienna WL_FONT_DIR, folder fonts/ obok skryptu, typowe miejsca."""
    here = os.path.dirname(os.path.abspath(__file__))
    cands = [cfg.get('font_dir'), os.environ.get('WL_FONT_DIR'), os.path.join(base, 'fonts'), os.path.join(here, 'fonts'),
             '/usr/share/fonts/opentype/inter', '/usr/share/fonts/truetype/inter',
             os.path.expanduser('~/Library/Fonts'), '/Library/Fonts', 'C:/Windows/Fonts']
    for d in cands:
        if not d:
            continue
        for ext in ('.otf', '.ttf'):
            if os.path.exists(os.path.join(d, 'Inter-Black' + ext)):
                F = lambda w, s: ImageFont.truetype(os.path.join(d, f'Inter-{w}{ext}'), s)
                global F_SUB, F_HOOK, F_LAB, F_PILL, F_BIG, F_BTN, F_SM, F_BADGE
                F_SUB, F_HOOK, F_LAB, F_PILL, F_BIG, F_BTN = F('Black', 80), F('Black', 100), F('Black', 66), F('Black', 56), F('Black', 92), F('Black', 70)
                F_SM, F_BADGE = F('Bold', 40), F('ExtraBold', 38)
                return d
    sys.exit('Nie znaleziono czcionki Inter (Inter-Black, Inter-Bold, Inter-ExtraBold). '
             'Pobierz ją z github.com/rsms/inter (Releases) i wskaż folder w configu: "font_dir": "/sciezka".')


def text_block(lines, font, stroke, emoji=None, gap=1.12, color=WHITE, gold=GOLD, stroke_col=(0, 0, 0, 255), shadow=True):
    lh = int(font.size * gap); esz = int(font.size * 1.0); pad = stroke * 2 + 20
    widths = []
    for i, ln in enumerate(lines):
        w = font.getlength(ln.replace('*', ''))
        if emoji and i == len(lines) - 1:
            w += esz + 16
        widths.append(w)
    bw, bh = int(max(widths) + pad * 2), lh * len(lines) + pad * 2
    img = Image.new('RGBA', (bw, bh), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    for i, ln in enumerate(lines):
        x = (bw - widths[i]) / 2; y = pad + i * lh; g = False
        for part in ln.split('*'):
            if part:
                d.text((x, y), part, font=font, fill=gold if g else color, stroke_width=stroke, stroke_fill=stroke_col)
                x += font.getlength(part)
            g = not g
        if emoji and i == len(lines) - 1 and os.path.exists(emoji):
            e = Image.open(emoji).convert('RGBA').resize((esz, esz), Image.LANCZOS)
            img.alpha_composite(e, (int(x + 14), int(y + font.size * 0.12)))
    if not shadow:
        return img
    sh = Image.new('RGBA', img.size, (0, 0, 0, 0)); sh.putalpha(img.split()[3].point(lambda a: int(a * 0.45)))
    out = Image.new('RGBA', img.size, (0, 0, 0, 0)); out.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10))); out.alpha_composite(img)
    return out


def fit(im, maxw=1010):
    """Za szeroki napis zmniejsza tak, żeby nie wychodził poza ekran."""
    if im is None or im.width <= maxw:
        return im
    k = maxw / im.width
    return im.resize((maxw, max(1, int(im.height * k))), Image.LANCZOS)


def pill(text, bg=RED, fg=WHITE, font=None, rot=-3, emoji=None, padx=40):
    font = font or F_PILL
    t = text_block([text], font, 0, emoji, color=fg, gold=GOLD if tuple(bg) != (255, 205, 72, 255) else INK, shadow=False)
    bw, bh = t.width + padx, int(font.size * 1.75)
    img = Image.new('RGBA', (bw + 40, bh + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    d.rounded_rectangle((20, 26, 20 + bw, 26 + bh), bh // 2, fill=(0, 0, 0, 90))
    img = img.filter(ImageFilter.GaussianBlur(6)); d = ImageDraw.Draw(img)
    d.rounded_rectangle((20, 20, 20 + bw, 20 + bh), bh // 2, fill=tuple(bg))
    img.alpha_composite(t, (20 + (bw - t.width) // 2, 20 + (bh - t.height) // 2 + 2))
    return img.rotate(rot, resample=Image.BICUBIC, expand=True) if rot else img


def label_box(text, emoji=None, minw=0, minh=0):
    """Etykieta zasłaniająca obcy napis w cudzym klipie: biała ramka, ciemny tekst, BEZ rozmycia tła."""
    t = text_block([text], F_LAB, 0, emoji, color=INK, gold=RED, shadow=False)
    bw, bh = max(t.width + 50, 760, int(minw)), max(t.height + 24, int(minh))
    img = Image.new('RGBA', (bw + 40, bh + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    d.rounded_rectangle((20, 28, 20 + bw, 28 + bh), 34, fill=(0, 0, 0, 110))
    img = img.filter(ImageFilter.GaussianBlur(10)); d = ImageDraw.Draw(img)
    d.rounded_rectangle((20, 20, 20 + bw, 20 + bh), 34, fill=(255, 255, 255, 250))
    img.alpha_composite(t, (20 + (bw - t.width) // 2, 20 + (bh - t.height) // 2))
    return img


def pop(t, dur=0.2):
    if t >= dur: return 1.0
    if t < dur * 0.6: return 0.72 + (1.08 - 0.72) * (t / (dur * 0.6))
    return 1.08 - 0.08 * ((t - dur * 0.6) / (dur * 0.4))


def place(fr, im, cx, cy, scale=1.0, alpha=1.0):
    if scale != 1.0:
        im = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))), Image.BICUBIC)
    if alpha < 1.0:
        im = im.copy(); im.putalpha(im.split()[3].point(lambda v: int(v * alpha)))
    fr.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))


def main(cfg_path):
    cfg = json.load(open(cfg_path)); base = os.path.dirname(os.path.abspath(cfg_path))
    p = lambda x: x if os.path.isabs(x) else os.path.join(base, x)
    init_fonts(cfg, base)
    emo = p(cfg['emoji_dir']) if cfg.get('emoji_dir') else ''

    def E(n):
        if not n or not emo:
            return None
        for name in (n, n + '-fe0f'):
            f = os.path.join(emo, name + '.png')
            if os.path.exists(f):
                return f
        return None

    work = tempfile.mkdtemp(prefix='wl_')
    # --- bity -> segmenty, napisy, etykiety
    segs, subs, covers, flashes, cuts = [], [], [], [], []
    t0 = 0.0
    for b in cfg['beats']:
        dur = float(b['dur']); raw = b['segs']
        tot = sum(s[2] for s in raw)
        acc = 0.0
        for j, s in enumerate(raw):
            ln = s[2] * dur / tot if j < len(raw) - 1 else dur - acc
            st = t0 + acc
            o = s[4] if len(s) > 4 else {}
            segs.append((s[0], s[1], ln, s[3] if len(s) > 3 else 0.0, o.get('speed', 1.0)))
            if o.get('cover'):
                c = o['cover']
                covers.append((st, st + ln, c['y'], label_box(c['label'], E(c.get('emoji')), c.get('w', 0) * W, c.get('h', 0.1) * H)))
            if o.get('flash'): flashes.append(st)
            cuts.append(st); acc += ln
        for s in b.get('subs', []):
            subs.append([t0 + s[0], s[1], s[2] if len(s) > 2 else None, s[3] if len(s) > 3 else None])
        t0 += dur
    D = t0; end = D - float(cfg['end_dur'])
    # --- cięcie ujęć (liczba klatek liczona narastająco, żeby nic się nie rozjeżdżało)
    names = []; acc_t = 0.0
    for i, (src, start, ln, top, spd) in enumerate(segs):
        nfr = int(round((acc_t + ln) * FPS)) - int(round(acc_t * FPS)); acc_t += ln
        # top > 0: obcina górę (np. obcy napis na górze); top < 0: obcina dół (np. napisy na dole cudzego klipu)
        if top > 0:
            cr = f'crop=iw*{1 - top}:ih*{1 - top}:iw*{top / 2}:ih*{top},'
        elif top < 0:
            b = -top
            cr = f'crop=iw*{1 - b}:ih*{1 - b}:iw*{b / 2}:0,'
        else:
            cr = ''
        crop = (f'setpts=PTS/{spd},' if spd != 1.0 else '') + cr
        out = f'{work}/c{i:02d}.mp4'
        subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-ss', str(start), '-t', f'{ln * spd + 0.2:.3f}', '-i', p(src), '-an',
                        '-vf', f'{crop}scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,fps=30,setsar=1,tpad=stop_mode=clone:stop_duration=1',
                        '-frames:v', str(nfr), '-c:v', 'libx264', '-preset', 'fast', '-crf', '15', '-pix_fmt', 'yuv420p', out], check=True)
        names.append(out)
    with open(f'{work}/list.txt', 'w') as f:
        f.writelines(f"file '{n}'\n" for n in names)
    joined = f'{work}/joined.mp4'
    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', f'{work}/list.txt', '-c', 'copy', joined], check=True)
    # --- grafiki
    hook = cfg.get('hook') or {'lines': [], 'until': 0}
    hook_img = fit(text_block(hook['lines'], F_HOOK, 9, E(hook.get('emoji'))), 1040) if hook['lines'] else None
    sub_imgs = []
    for i, (a, txt, em, sy) in enumerate(subs):
        b = subs[i + 1][0] if i + 1 < len(subs) else end
        sub_imgs.append((a, b, fit(text_block(txt.split('|'), F_SUB, 7, E(em))) if txt else None, sy))
    stickers = [(s['from'], s['to'], fit(pill(s['text'], bg=tuple(s.get('bg', RED)), fg=tuple(s.get('fg', WHITE)), rot=s.get('rot', -4),
                 emoji=E(s.get('emoji'))), 1000), s['x'], s['y']) for s in cfg.get('stickers', [])]
    badge = pill(cfg.get('badge_text', 'winterly.pl'), bg=(255, 255, 255, 235), fg=INK, font=F_BADGE, rot=0, emoji=E('1f6d2'), padx=30)
    badge_from = cfg.get('badge_from', 3.0)
    if cfg.get('logo') and os.path.exists(p(cfg['logo'])):
        logo = Image.open(p(cfg['logo'])).convert('RGBA'); lw = 470
        logo = logo.resize((lw, int(logo.height * lw / logo.width)), Image.LANCZOS)
    else:  # brak pliku z logo: złoty napis zamiast logo
        logo = text_block([f"*{cfg.get('logo_text', 'Winterly')}*"], F_BIG, 6)
    ec = cfg['end']
    e_pill = pill(ec['pill'], rot=-3, emoji=E(ec.get('pill_emoji')))
    e_txt = text_block(ec['lines'], F_BIG, 8)
    e_btn = pill(ec['button'], bg=GREEN, fg=WHITE, font=F_BTN, rot=0, padx=90)
    e_arrow = Image.open(E('1f447')).convert('RGBA').resize((120, 120), Image.LANCZOS) if E('1f447') else None
    e_small = text_block(ec['small'].split('|'), F_SM, 4) if ec.get('small') else None
    # --- klatka po klatce
    dec = subprocess.Popen(['ffmpeg', '-nostdin', '-v', 'error', '-i', joined, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    enc = ['ffmpeg', '-nostdin', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
           '-t', f'{D:.3f}', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', p(cfg['out'])]
    encp = subprocess.Popen(enc, stdin=subprocess.PIPE)
    n = int(round(D * FPS)); fsz = W * H * 3; last = None
    DIS = int(cfg.get('dissolve', 0)); PUNCH = cfg.get('punch', False)
    cut_frames = {int(round(c * FPS)) for c in cuts if c > 0 and all(abs(c - f) > 1e-6 for f in flashes)}
    hold, hold_k, prev_base = None, -99, None
    for k in range(n):
        t = k / FPS
        raw = dec.stdout.read(fsz)
        if len(raw) == fsz: last = raw
        fr = Image.frombytes('RGB', (W, H), last)
        if t < end:  # etykiety na obraz bazowy (przed przenikaniem, żeby obcy napis nie prześwitywał)
            for a, b, y, im in covers:
                if a <= t < b:
                    fr = fr.convert('RGBA'); place(fr, im, W / 2, H * y); fr = fr.convert('RGB')
        if DIS and k in cut_frames and prev_base is not None and t < end:
            hold, hold_k = prev_base, k
        prev_base = fr
        if hold is not None and 0 <= k - hold_k < DIS:
            fr = Image.blend(hold, fr, (k - hold_k + 1) / (DIS + 1))
        since = min([t - c for c in cuts if c <= t + 1e-6] or [9])
        if PUNCH and since < 0.25 and t < end:
            z = 1.0 + 0.07 * (1 - since / 0.25) ** 2
            cw, chh = int(W / z), int(H / z)
            fr = fr.crop(((W - cw) // 2, (H - chh) // 2, (W - cw) // 2 + cw, (H - chh) // 2 + chh)).resize((W, H), Image.BILINEAR)
        fr = fr.convert('RGBA')
        if t >= end:  # plansza końcowa
            te = t - end
            fr = fr.filter(ImageFilter.GaussianBlur(16)); fr.alpha_composite(Image.new('RGBA', (W, H), (8, 20, 15, 130)))
            place(fr, logo, W / 2, H * 0.22, pop(te), min(1, te / 0.15))
            if te > 0.2: place(fr, e_pill, W / 2, H * 0.36, pop(te - 0.2))
            if te > 0.4: place(fr, e_txt, W / 2, H * 0.48, pop(te - 0.4))
            if te > 0.6:
                pulse = 1 + 0.035 * math.sin((te - 0.6) * 2 * math.pi * 1.6)
                place(fr, e_btn, W / 2, H * 0.605, pop(te - 0.6) * pulse)
            if te > 0.8 and e_arrow is not None:
                place(fr, e_arrow, W / 2, H * 0.69 + 18 * abs(math.sin((te - 0.8) * math.pi * 2.2)), pop(te - 0.8))
            if te > 0.9 and e_small is not None: place(fr, e_small, W / 2, H * 0.765, 1.0, min(1, (te - 0.9) / 0.3))
        else:
            if hook_img is not None and t < hook['until']:
                place(fr, hook_img, W / 2, H * hook.get('y', 0.25), pop(t))
            for a, b, im, sy in sub_imgs:
                if a <= t < b and im is not None: place(fr, im, W / 2, H * (sy or cfg.get('sub_y', 0.69)), pop(t - a))
            for a, b, im, x, y in stickers:
                if a <= t < b: place(fr, im, W * x, H * y, pop(t - a, 0.25))
            if t >= badge_from:
                place(fr, badge, W - badge.width / 2 - 24, H * 0.155, 1.0, min(1, (t - badge_from) / 0.3))
        for fl in flashes:
            if 0 <= t - fl < 0.2:
                a = int(200 * (1 - (t - fl) / 0.2)); fr.alpha_composite(Image.new('RGBA', (W, H), (255, 255, 255, a)))
        encp.stdin.write(fr.convert('RGB').tobytes())
    encp.stdin.close(); encp.wait(); dec.kill()
    print('OK', p(cfg['out']), f'{D:.2f}s')


if __name__ == '__main__':
    main(sys.argv[1])
