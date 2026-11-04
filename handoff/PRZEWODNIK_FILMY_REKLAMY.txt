# PRZEWODNIK: robienie i montaż reklam wideo (Meta / TikTok / Reels)

Samodzielny plik do wklejenia w nowy czat (np. projekt Winterly). Zawiera cały sposób pracy i **pełny kod** narzędzia do montażu. Nie potrzebujesz żadnych innych plików.

**Instrukcja dla asystenta, który to czyta:** odtwórz skrypt z sekcji 9 jako `montaz.py`, zainstaluj `ffmpeg`, Pillow i font Inter, a potem montuj według sekcji 1–8.

---

## 1. Schemat pracy
1. **Scenariusz.** Tekst lektora na 18–25 s, układ: hook → produkt → jak działa → gdzie/kiedy → oferta → wezwanie do zakupu.
2. **Ujęcia.** Generowane w AI (Gemini Omni / Veo / Higgsfield) albo nagrane telefonem. Pionowo 9:16, bez napisów i bez muzyki.
3. **Lektor.** ElevenLabs, eksport do mp3. Długość filmu = długość lektora.
4. **Czasy napisów.** Pauzy w nagraniu znajdziesz przez `silencedetect` (sekcja 5). Każde zdanie ląduje między dwiema pauzami.
5. **Montaż.** Uzupełniasz `config.json` (ujęcia, napisy, hook, CTA), a `python3 -I montaz.py config.json` robi gotowy film.
6. **Kontrola.** Wyciągasz 6–8 klatek i oglądasz je przed oddaniem (sekcja 7).

## 2. Struktura tekstu, która sprzedała
Najlepiej zadziałał prosty układ:
- **pytanie, w którym widz się rozpoznaje** („Znasz te dni, kiedy…?”);
- **czym jest produkt** w jednym zdaniu;
- **jak się go używa** w jednym zdaniu;
- **szybka wyliczanka „gdzie”** („Do pracy, pod bluzę, pod koc.”);
- **oferta** („Teraz w Black Month drugi zestaw o połowę taniej.”);
- **hasło marki i gdzie kupić** („…Zamów na twojsklep.pl.”).

Przykład dla produktu w Black Month:
> Znasz te dni, kiedy chcesz tylko ciepła i koca? [Produkt] to [co to jest] w [cecha]. [Jak się używa]… i [korzyść] idzie z Tobą wszędzie. Do pracy, pod bluzę, pod koc. Teraz w Black Month drugi zestaw kupisz o połowę taniej. [Marka] – [hasło]. Zamów na [sklep].pl.

Wersja do mężczyzn (prezent):
> Panowie, nie wiecie, co jej kupić? Jeśli widzisz, że [problem jej] – to jest prezent, na który czeka. [Produkt] to [co to jest]. [Jak używa]. W Black Month drugi zestaw kupisz o połowę taniej – jeden dla niej, drugi dla mamy albo siostry. Wejdź na [sklep].pl i zamów, póki trwa promocja.

**Hook (pierwsze 2–3 s, duży napis)**, sprawdzone schematy:
- „Nie musisz już [męczące zachowanie]”;
- „Panowie, nie wiecie, co jej kupić? 🎁”;
- „Zanim kupisz zwykły [produkt], zobacz to 👀”;
- „Znasz te dni, kiedy…?”.

## 3. Styl wizualny, który przyjął się najlepiej
**Unikaj** dużych ramek, pasków i tekstu stale na ekranie. Odciągają uwagę od filmu i tak to odbierali widzowie.

- **Hook:** duży biały tekst (Inter ExtraBold 84 px), czarny obrys 6 px, miękki cień, **bez tła**, na ~30% wysokości. Widoczny tylko przez pierwsze 2,5–3 s, potem znika. W tym czasie nie ma napisów u dołu.
- **Napisy do lektora:** zwykłe, białe (Inter Bold 48 px), cienki obrys 3 px, lekko przezroczyste (alfa ~225), **bez tła**, na ~66% wysokości, po 2–5 słów.
- **Dolne 20% ekranu zostaje puste,** bo tam Reels i TikTok mają przyciski.
- **Plansza końcowa:** od momentu „Zamów na…”. Tło lekko rozmyte (boxblur 18), u góry karta z logo i adresem sklepu, na środku kremowa ramka (#FFF8F0, tekst #3B2A21) z ofertą, np. „BLACK MONTH / Drugi zestaw -50% / Zamów na sklep.pl 👇”.
- **Dźwięk:** lektor znormalizowany do -14 LUFS, wyciszenie na ostatnie 0,3 s.
- **Eksport:** 1080×1920, 30 fps, H.264 CRF 18, yuv420p, AAC 192k, `+faststart`.

## 4. Ujęcia z AI: prompty i pułapki
**Stała końcówka promptu** (dopisuj do każdego klipu):
> Vertical 9:16, handheld phone footage, natural light, realistic, no text, no music, only soft ambient room sound. Same young woman as in the reference image. Use the product from the images exactly – same color, shape and details.

- **Do każdego klipu dołączaj zdjęcia produktu,** a od drugiego klipu także zrzut twarzy postaci z pierwszego (ta sama osoba w całym filmie).
- **Jeden klip ma 5–10 s.** Poprawiaj go rozmową („warmer light”, „slow down the end”) zamiast generować od nowa.
- **Oglądaj każdy klip klatka po klatce.** Typowe błędy AI: dziwne odbicia w lustrze, produkt założony na ubranie zamiast pod nie, inna osoba w środku filmu, kadr, który źle wygląda (np. jak brzuch ciążowy), „ulepszony” produkt (dodany kabel, zmieniony kształt). Takie fragmenty **wycinaj**.
- **Długość ujęć:** 0,8–3,5 s. Krótkie (0,7–1 s) przy wyliczankach, dłuższe (2–3 s) przy hooku i pokazywaniu produktu. Zmiana ujęcia wypada na początku nowego zdania.
- **Cudze reklamy (konkurencja) tylko jako wzór** kadrów i rytmu. Nie publikuj cudzych nagrań, nawet z podmienionym produktem, bo zostają cudze twarze i prawa autorskie. Jeśli robisz z nich szkic roboczy, w finalnej wersji podmień wszystko: osoby, produkt i tło.

## 5. Czasy napisów z pauz lektora
```
ffmpeg -nostdin -i lektor.mp3 -af silencedetect=noise=-35dB:d=0.12 -f null - 2>&1 | grep -o 'silence_[se][a-z]*: [0-9.]*'
```
- Mowa trwa między `silence_end` a następnym `silence_start`. Każdy taki odcinek to zwykle jedno zdanie scenariusza.
- Długie zdania dziel na kawałki po 2–5 słów proporcjonalnie do liczby sylab.
- Format w configu: `[[start, koniec, "tekst"], ...]`.
- Długość lektora: `ffprobe -v error -show_entries format=duration -of csv=p=0 lektor.mp3`.

## 6. Plik config.json, przykład
```json
{
  "out": "reklama_F.mp4",
  "voice": "lektor_F.mp3",
  "duration": 22.05,
  "hook": {"lines": ["Nie musisz już", "leżeć pod kocem", "w trudne dni"], "emoji": "emoji/1f64c.png", "until": 2.5},
  "subs": [
    [2.79, 3.95, "Otulka to termofor"], [3.95, 5.37, "w mięciutkim pasie."],
    [5.61, 7.0, "Zapinasz go na brzuchu"], [7.0, 7.9, "albo plecach"],
    [18.69, 20.65, "Zamów na sklep.pl –"], [20.9, 22.0, "link masz poniżej."]
  ],
  "end": 18.69,
  "logo": "logo.png",
  "logo_url": "sklep.pl",
  "cta": {"lines": ["BLACK MONTH", "Drugi zestaw -50%", "Zamów na sklep.pl"], "emoji": "emoji/1f447.png"},
  "segments": [
    ["klip_lozko.mp4", 0.0, 2.4],
    ["klip_plusz.mp4", 0.1, 1.0],
    ["klip_zakladanie.mp4", 2.6, 1.55]
  ]
}
```
- `segments`: `[plik, start_s, długość_s]`. **Suma długości musi się równać `duration`.**
- **Emoji** jako PNG: paczka npm `emoji-datasource-google`, plik `img/google/64/<kod>.png` (np. 1f64c 🙌, 1f381 🎁, 1f440 👀, 1f447 👇, 1f5a4 🖤, 2728 ✨). Pobierasz przez `curl https://registry.npmjs.org/emoji-datasource-google/latest`, a link z pola `dist.tarball` rozpakowujesz w osobnym folderze.

## 7. Kontrola przed oddaniem
```
for t in 1.2 5 9 13 17 21; do ffmpeg -nostdin -v error -y -ss $t -i reklama.mp4 -frames:v 1 -vf scale=240:-2 k_$t.jpg; done
ffmpeg -nostdin -y $(for t in 1.2 5 9 13 17 21; do echo -n "-i k_$t.jpg "; done) -filter_complex hstack=6 arkusz.jpg
```
Sprawdź w arkuszu:
- czy hook jest czytelny;
- czy napisy nie wchodzą na twarze;
- czy w ujęciach nie ma błędów AI;
- czy plansza końcowa jest na miejscu.

## 8. Reklamy w Meta: wnioski z testu
- **Przed pierwszą złotówką na reklamy:** w kasie BLIK, płatność przy odbiorze, polski jako język domyślny sklepu, poprawne koszty dostawy i piksel z testowym zakupem. Przy zepsutej kasie reklamy palą pieniądze.
- **Audience Network wyłącz od razu,** zostaw tylko Facebooka i Instagrama. Daje setki pustych kliknięć bez wejść na stronę.
- **Najlepiej działała jedna grupa reklam:** szeroko, cel „Sprzedaż” (zakup), 3–5 reklam. Przez pierwsze 3 dni nic nie zmieniaj.
- **Zasady wyłączania:**
  - ~100 zł wydane na reklamę bez dodania do koszyka → wyłącz tę reklamę;
  - kliknięcie droższe niż ~2 zł albo CTR poniżej 1% → zmień pierwsze 3 s filmu.
- **Marża przed testem:** policz, ile zostaje na sztuce po towarze, wysyłce, opłatach i podatku. To jest maksymalny koszt zakupu. Przy marży poniżej ~100 zł reklamy rzadko się zwracają, więc dodaj zestaw 2 sztuk (np. „druga -50%”).
- **Wgrywanie filmu do Meta z serwera:** Meta pobiera media tylko z publicznego linku. Działa to tak: Shopify `stagedUploadsCreate` (VIDEO) → POST pliku → `fileCreate` → link `cdn.shopify.com/...mp4` → `ads_creative_upload_media` (URL).
- **Prawo (Polska):**
  - bez twierdzeń medycznych;
  - bez zmyślonych opinii i liczb;
  - przekreślona cena musi być najniższą ceną z 30 dni (dyrektywa Omnibus);
  - lektor z AI nie udaje klientki;
  - „tylko do…” musi być prawdą.

---

## 9. PEŁNY KOD: montaz.py
Zapisz poniższy kod jako `montaz.py`. Wymaga `ffmpeg`, Pillow (`pip install pillow`) i fontu Inter (`apt install fonts-inter`, pliki w `/usr/share/fonts/opentype/inter/`).

```python
"""Montaż reklamy pionowej 1080x1920 z jednego pliku konfiguracyjnego JSON.

Użycie:  python3 -I montaz.py config.json

Co robi:
  1. tnie ujęcia z klipów (1080x1920, 30 fps, bez dźwięku) i skleja je,
  2. pierwsze sekundy: DUŻY hook (biały tekst z obrysem, bez tła) – potem znika,
  3. napisy do lektora: zwykłe, białe, cienki obrys, lekko przezroczyste, bez tła,
  4. koniec: rozmyte tło + karta z logo + kremowa ramka z wezwaniem do zakupu (CTA),
  5. dźwięk: lektor znormalizowany do -14 LUFS, wyciszenie na ostatnie 0,3 s.

config.json (przykład):
{
  "out": "reklama.mp4",
  "voice": "lektor.mp3",
  "duration": 22.05,                       # = długość lektora
  "hook": {"lines": ["Nie musisz już", "leżeć pod kocem"], "emoji": "emoji/1f64c.png", "until": 2.5},
  "subs": [[0.05, 1.15, "Nie musisz już leżeć"], [1.15, 2.38, "pod kocem w trudne dni."]],
  "end": 18.69,                            # od tej sekundy plansza końcowa
  "logo": "logo.png",                      # PNG z przezroczystym tłem (opcjonalnie)
  "logo_url": "twojsklep.pl",
  "cta": {"lines": ["BLACK MONTH", "Drugi zestaw -50%", "Zamów na twojsklep.pl"], "emoji": "emoji/1f447.png"},
  "segments": [["klip1.mp4", 0.0, 2.4], ["klip2.mp4", 1.2, 0.95]]   # [plik, start_s, długość_s]
}
Suma długości segmentów powinna być równa "duration".
Wymaga: ffmpeg, Python 3 + Pillow, font Inter (Debian/Ubuntu: pakiet fonts-inter).
"""
import json
import os
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1080, 1920
FONT_DIR = '/usr/share/fonts/opentype/inter'
F_HOOK = ImageFont.truetype(f'{FONT_DIR}/Inter-ExtraBold.otf', 84)
F_SUB = ImageFont.truetype(f'{FONT_DIR}/Inter-Bold.otf', 48)
F_CTA = ImageFont.truetype(f'{FONT_DIR}/Inter-ExtraBold.otf', 64)
F_URL = ImageFont.truetype(f'{FONT_DIR}/Inter-SemiBold.otf', 38)
INK, CREAM = (59, 42, 33, 255), (255, 248, 240, 252)


def wrap(text, font, maxw):
    words, lines, cur = text.split(), [], ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if font.getlength(t) <= maxw:
            cur = t
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    return lines


def paste_emoji(img, path, x, y, size):
    if path and os.path.exists(path):
        e = Image.open(path).convert('RGBA').resize((size, size), Image.LANCZOS)
        img.alpha_composite(e, (int(x), int(y)))


def plain(img, lines, font, cy, lh, stroke, alpha=255, emoji=None):
    """Biały tekst z czarnym obrysem i miękkim cieniem, BEZ tła. cy = środek w ułamku wysokości."""
    esz = int(font.size * 1.05)
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    y0 = cy * H - lh * len(lines) / 2
    last_end = (0, 0)
    for i, line in enumerate(lines):
        extra = esz + 14 if emoji and i == len(lines) - 1 else 0
        x = (W - font.getlength(line) - extra) / 2
        d.text((x, y0 + i * lh), line, font=font, fill=(255, 255, 255, alpha),
               stroke_width=stroke, stroke_fill=(0, 0, 0, int(alpha * 0.85)))
        last_end = (x + font.getlength(line) + 8, y0 + i * lh)
    shadow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    shadow.putalpha(layer.split()[3].point(lambda a: int(a * 0.35)))
    img.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(8)), (0, 4))
    img.alpha_composite(layer)
    if emoji:
        paste_emoji(img, emoji, last_end[0], last_end[1] + 6, esz)


def cream_box(img, lines, font, cy, lh, emoji=None):
    """Kremowa zaokrąglona ramka z ciemnym tekstem (do planszy końcowej z CTA)."""
    esz = int(font.size * 1.05)
    widths = [font.getlength(l) for l in lines]
    if emoji:
        widths[-1] += esz + 14
    bw, bh = int(max(widths) + 96), lh * len(lines) + 56
    bx, by = (W - bw) // 2, int(cy * H - bh / 2)
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((bx, by + 8, bx + bw, by + bh + 8), 32, fill=(0, 0, 0, 80))
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(12)))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((bx, by, bx + bw, by + bh), 32, fill=CREAM)
    ty = by + 28 - 4
    for i, (line, w) in enumerate(zip(lines, widths)):
        x = (W - w) / 2
        d.text((x, ty + i * lh), line, font=font, fill=INK)
        if emoji and i == len(lines) - 1:
            paste_emoji(img, emoji, x + font.getlength(line) + 8, ty + i * lh + 4, esz)


def logo_card(img, logo_path, url, top_frac=0.07):
    """Kremowa karta z logo i adresem sklepu u góry ekranu."""
    if not logo_path or not os.path.exists(logo_path):
        return
    logo = Image.open(logo_path).convert('RGBA')
    lw = 380
    logo = logo.resize((lw, int(logo.height * lw / logo.width)), Image.LANCZOS)
    bw, bh = lw + 120, logo.height + 50 + 40 + 44
    bx, by = (W - bw) // 2, int(H * top_frac)
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((bx, by + 10, bx + bw, by + bh + 10), 40, fill=(0, 0, 0, 80))
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14)))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((bx, by, bx + bw, by + bh), 40, fill=(255, 251, 245, 248))
    img.alpha_composite(logo, ((W - lw) // 2, by + 44))
    if url:
        d.text(((W - F_URL.getlength(url)) / 2, by + 44 + logo.height + 22), url, font=F_URL, fill=(110, 80, 62, 255))


def main(cfg_path):
    cfg = json.load(open(cfg_path))
    base = os.path.dirname(os.path.abspath(cfg_path))
    p = lambda x: x if os.path.isabs(x) else os.path.join(base, x)
    D, end = float(cfg['duration']), float(cfg['end'])
    hook = cfg.get('hook') or {}
    hook_until = float(hook.get('until', 0))
    work = tempfile.mkdtemp(prefix='montaz_')

    # 1) cięcie i sklejanie ujęć
    names = []
    for i, (src, start, dur) in enumerate(cfg['segments']):
        out = f'{work}/c{i:02d}.mp4'
        subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-ss', str(start), '-i', p(src), '-t', str(dur), '-an',
                        '-vf', 'scale=1080:1920,fps=30,setsar=1', '-c:v', 'libx264', '-preset', 'fast', '-crf', '18',
                        '-pix_fmt', 'yuv420p', out], check=True)
        names.append(out)
    with open(f'{work}/list.txt', 'w') as f:
        f.writelines(f"file '{n}'\n" for n in names)
    joined = f'{work}/joined.mp4'
    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', f'{work}/list.txt',
                    '-c', 'copy', joined], check=True)

    # 2) plansze: jedna pełnoekranowa nakładka PNG na każdy odcinek czasu
    subs = cfg.get('subs', [])
    cont = []  # napis trwa do początku następnego, żeby nie migał
    for i, (a, b, t) in enumerate(subs):
        nxt = subs[i + 1][0] if i + 1 < len(subs) else D
        cont.append((a, nxt, t))
    cuts = sorted({round(x, 3) for x in [0, D, end, hook_until] + [c[0] for c in cont] if 0 <= x <= D})
    overlays = []
    for i in range(len(cuts) - 1):
        a, b = cuts[i], cuts[i + 1]
        mid = (a + b) / 2
        img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        if mid < hook_until and hook.get('lines'):
            plain(img, hook['lines'], F_HOOK, 0.30, 100, 6, 255, p(hook['emoji']) if hook.get('emoji') else None)
        if hook_until <= mid < end:
            txt = next((t for s0, s1, t in cont if s0 <= mid < s1), '')
            if txt:
                plain(img, wrap(txt, F_SUB, 880), F_SUB, 0.66, 60, 3, 225)
        if mid >= end:
            logo_card(img, p(cfg['logo']) if cfg.get('logo') else None, cfg.get('logo_url', ''))
            cta = cfg.get('cta') or {}
            if cta.get('lines'):
                cream_box(img, cta['lines'], F_CTA, 0.385, 80, p(cta['emoji']) if cta.get('emoji') else None)
        path = f'{work}/o{i:02d}.png'
        img.save(path)
        overlays.append((path, a, b))

    # 3) składanie: rozmycie końcówki, nakładki, lektor
    cmd = ['ffmpeg', '-nostdin', '-v', 'error', '-y', '-i', joined, '-i', p(cfg['voice'])]
    for path, _, _ in overlays:
        cmd += ['-i', path]
    fc = f"[0:v]boxblur=luma_radius=18:luma_power=2:enable='gte(t,{end})',eq=brightness=0.04:enable='gte(t,{end})'[v0]"
    last = 'v0'
    for i, (_, a, b) in enumerate(overlays):
        fc += f";[{last}][{i + 2}:v]overlay=0:0:enable='between(t,{a},{b - 0.001})'[v{i + 1}]"
        last = f'v{i + 1}'
    fc += f";[1:a]loudnorm=I=-14:TP=-1.5:LRA=11,apad,atrim=0:{D},afade=t=out:st={D - 0.3}:d=0.3[a]"
    cmd += ['-filter_complex', fc, '-map', f'[{last}]', '-map', '[a]', '-c:v', 'libx264', '-preset', 'slow', '-crf', '18',
            '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', '-t', str(D), p(cfg['out'])]
    subprocess.run(cmd, check=True)
    print('gotowe:', p(cfg['out']))


if __name__ == '__main__':
    main(sys.argv[1])
```
