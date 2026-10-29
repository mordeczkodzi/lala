# Podręcznik: robienie i montaż filmów reklamowych Otulka

Wszystko, czego nauczyliśmy się przy Filmach A, B i C. Skrypty są w `handoff/video-tools/`.
Przetestowane: z tych skryptów da się odtworzyć Film B klatka w klatkę.

---

## 1. Schemat pracy

1. **Scenariusz:** tekst lektora (15–23 s), lista ujęć i hook na górę.
2. **Klipy w Gemini Omni:** ujęcia po 5–10 s, bez napisów i bez muzyki.
3. **Lektor w ElevenLabs:** głos *Kinga – Warm, Energetic Polish Voice*, eksport mp3.
4. **Cięcie:** `cut.sh` tnie klipy na kawałki pod tempo lektora i skleja w `joined.mp4`.
5. **Napisy:** `subs_json.py` robi z pliku `chunks.json` przezroczyste PNG z napisami.
6. **Hook:** `hook2.py` (lub `hook.py` z emoji) robi kremową plakietkę na górę na pierwsze 3 s.
7. **Plakietki:** opcjonalnie `badge.py`, np. liczniki 3/2/1 w Filmie C.
8. **Składanie:** `render.py` łączy obraz, lektora, napisy i hook, robi rozmyty koniec z kartą logo i ustawia głośność na -14 LUFS.
9. **Kontrola:** wyciągnij 8–10 klatek (`ffmpeg -ss T -frames:v 1`), sklej obok siebie i obejrzyj, zanim oddasz.

Wymagania: `ffmpeg`, Python 3 z Pillow, font **Inter** (`/usr/share/fonts/opentype/inter/`, w Debianie/Ubuntu: pakiet `fonts-inter`).

---

## 2. Gemini Omni: jak pisać prompty

- Jeden klip ma maksymalnie **10 s**. Krótsze prompty działają lepiej niż w Veo.
- **Do każdego klipu dołączaj zdjęcia produktu:** packshot Otulki i zdjęcie pasa na ciele. Od klipu 2 dołączaj też **zrzut twarzy dziewczyny z klipu 1**, żeby była to ta sama osoba.
- **Stała końcówka promptu, wklejana zawsze:**
  > Vertical 9:16, handheld phone footage, natural light, realistic, no text, no music, only soft ambient room sound. Same young woman as in the reference image, mid-20s, light brown hair in a messy bun. Use the plush belt from the images exactly – same color, shape and pocket, no cables.
- **Przykład** (klip „dłoń na pluszu”):
  > Close-up of a woman lying in bed on white sheets, her hand slowly stroking the soft beige plush belt on her belly, morning window light. + stała końcówka
- **Poprawki rób rozmową,** zamiast generować od nowa: „make the lighting warmer”, „slow down the last 3 seconds”, „remove the music”.
- **Mowa po polsku z Omni** często brzmi dziwnie. Lepiej robić klip bez mowy i dograć lektora z ElevenLabs.

### Na co uważać w klipach z AI (sprawdzone na naszych klipach)

| Problem | Co zrobiliśmy |
|---|---|
| Szeroki kadr przy laptopie wyglądał jak **brzuch ciążowy** | Użyliśmy tylko zbliżenia, 0.9 s |
| Kręcenie się przed lustrem: po 2.5 s **błąd odbicia** | Ucięte na 0–2.5 s |
| Bluza: na początku **pas założony NA bluzę** | Wzięte tylko 4–6.8 s |
| Film B, herbata: **inna kobieta i inny mężczyzna** niż w reszcie | Do wygenerowania ponownie z referencją twarzy |
| AI „ulepsza” produkt (dodaje kabel, zmienia kształt) | Taki klip wyrzucamy, bo produkt musi wyglądać jak prawdziwy |

**Zawsze oglądaj każdy klip klatka po klatce** przed cięciem. Robimy arkusz klatek co 0.5–1 s.

---

## 3. Lektor (ElevenLabs)

- Głos: **Kinga – Warm, Energetic Polish Voice**. Ustawienia z pliku: speed 100, stability 50, similarity 75, model v4.
- **Długość filmu = długość lektora.** Plansza z logo idzie na ostatnie ~2 s, w trakcie ostatniego zdania.
- Głośność ustawia `render.py`: `loudnorm I=-14 TP=-1.5`, wyciszenie na ostatnie 0.3 s.
- **AI-lektor nie może udawać klientki.** Nie mówi „kupiłam”, „używam od miesiąca” ani „uratowało mi okres”.

---

## 4. Cięcie (`cut.sh`)

```
./cut.sh pracownia/v films/filmA_cuts.txt
```

- **Plik listy:** jedna linia na ujęcie: `ścieżka start_s długość_s`. Komentarze po `#` są pomijane.
- **Każdy kawałek:** 1080×1920, 30 fps, bez dźwięku, CRF 18, więc sklejanie idzie bez ponownego kodowania.
- **Ujęcia 0.8–3.5 s.** Krótkie (0.8–1.2 s) przy wyliczankach („do pracy, pod bluzę, pod koc”), dłuższe (2.5–3.5 s) na start i przy zapinaniu pasa.
- **Cięcie pod lektora:** zmiana ujęcia wypada na początku nowego zdania albo słowa-klucza.
- Gotowe listy cięć z Filmów A, B i C są w `video-tools/films/`.

---

## 5. Napisy (`subs_json.py`)

```
python3 -I subs_json.py pracownia/subs films/filmB_chunks.json
```

- **Format `chunks.json`:** `[[start, koniec, "tekst"], ...]`. Czasy bierzemy z nasłuchu lektora.
- **Styl:** Inter ExtraBold 64 px, biały, **czarny obrys 6 px**, wyśrodkowany, na **60% wysokości** ekranu. Dolne 20% zostaje puste, bo tam Reels ma przyciski.
- **Kawałki po 2–6 słów,** maksymalnie 2 linie (zawijanie przy 900 px).
- Napisy są dla oglądających **bez dźwięku**, a takich jest większość.

---

## 6. Hook (górna plakietka, pierwsze ~3 s)

```
python3 -I hook2.py hook.png "Panowie, ten prezent|zrobi z Was bohaterów"
python3 -I hook.py  hook.png "Termofor, który się nosi" assets/emoji_2728_sparkles.png
```

- **Wygląd:** kremowa zaokrąglona ramka (#FFF8F0), ciemnobrązowy tekst (#3B2A21), Inter ExtraBold, na **18–20% wysokości**.
- **Z doświadczenia:** długi napis-mem na górze przez cały film (np. „Kiedy masz okres, a Twój chłopak kupuje Ci to”) **przeszkadzał** w wersji z lektorem. Zastąpiliśmy go krótkim hookiem na 3 s.
- **Hooki, które zrobiliśmy:**
  - Film A: „Termofor, który się nosi ✨”;
  - Film B: „Panowie, ten prezent / zrobi z Was bohaterów”;
  - Film C: „3 powody, żeby mieć / Otulkę w trudne dni”.
- **Emoji:** PNG z paczki npm `emoji-datasource-google` (`img/google/64/<kod>.png`). Ściągaj z registry npm, bo jsdelivr i unpkg bywają zablokowane.

---

## 7. Plakietki i koniec z logo

- `badge.py out.png 3`: brzoskwiniowe kółko z cyfrą po lewej, na 36% wysokości. Wyliczanka w Filmie C: 3 → 2 → 1.
- **Koniec:** `render.py` od sekundy `end` **rozmywa tło** (boxblur 18) i lekko je rozjaśnia, a na środek kładzie kartę z logo `assets/logocard_mid.png`.
  - Pierwsza wersja z kartą na ostrym obrazie zasłaniała twarze, stąd rozmycie.
- **Karta logo:** `logocard2.py logo.png out.png 0.33`, gdzie ostatni argument to pozycja w pionie (0.33 to środek).
- Logo było wycięte z Twojej grafiki przez `logo_cut.py`. Gotowe: `assets/otully_logo.png`.

---

## 8. Składanie (`render.py`)

Przykład konfiguracji: `video-tools/films/filmB_config.json`. Pola:
- `base`: sklejony obraz;
- `audio`: lektor;
- `subs`: `meta.json` z napisów;
- `hook`: [plik, do której sekundy];
- `end`: od kiedy plansza z logo;
- `badges`: opcjonalne plakietki;
- `duration`: długość filmu;
- `out`: plik wynikowy.

**Eksport:** H.264 CRF 18, yuv420p, AAC 192k, `+faststart`, 1080×1920. Gotowe pod Reels, TikTok i Meta.

**Szybka kontrola:**
```
for t in 1 5 9 13 17 19.5; do ffmpeg -v error -y -ss $t -i out.mp4 -frames:v 1 -vf scale=216:-1 f_$t.jpg; done
ffmpeg -y $(for t in 1 5 9 13 17 19.5; do echo -n "-i f_$t.jpg "; done) -filter_complex hstack=6 arkusz.jpg
```

---

## 9. Treść reklam: zasady, których się trzymamy

- **Bez twierdzeń medycznych.** Nie piszemy „leczy”, „bez leków”, „na ból miesiączkowy”. Piszemy o cieple, wygodzie i wolnych rękach.
- **Nie zwracamy się do widza tak, jakbyśmy znali jego zdrowie** (zasada Meta). Nie piszemy „Masz bolesne miesiączki?”, piszemy ogólnie.
- **Bez zmyślonych opinii i liczb** („10 000 zadowolonych klientek”). Promocji nie ogłaszamy bez spełnienia zasady najniższej ceny z 30 dni (Omnibus).
- **Ceny:** zestaw Standard 159 zł, zestaw Przytulny 185 zł, **sam pasek 69 zł** (dokupywany osobno, więc 69 zł nie reklamujemy).

---

## 10. Wgrywanie do Meta, gdy pliki są lokalnie

Meta pobiera media tylko z publicznego linku. Działająca metoda:
1. Shopify `stagedUploadsCreate`: IMAGE dla jpg, VIDEO dla mp4.
2. POST pliku na staged URL.
3. `fileCreate`.
4. Link `cdn.shopify.com/...` przekazujesz do `ads_creative_upload_media` (URL).

Uwaga: jeśli Meta nie pobierze obrazka, podaj link **bez** `?v=...`.
