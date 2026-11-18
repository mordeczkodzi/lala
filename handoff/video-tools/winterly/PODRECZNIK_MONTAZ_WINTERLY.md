# Winterly: jak robimy i montujemy reklamy wideo

Podręcznik dla nowego czatu (i dla właściciela). Opisuje cały proces, który dał reklamy A „Sąsiadka z pretensjami” i B „Konkurs na najładniejszy balkon”, oraz narzędzia z tego folderu:

| Plik | Do czego służy |
|---|---|
| `render_winterly.py` | Montaż obrazu: ujęcia, napisy, hak, naklejki, plansza końcowa. |
| `miks_audio.sh` | Lektor i muzyka, sklejenie z obrazem w gotowy film. |
| `podmiana_wzoru.py` | Podmiana wzoru na kurtynie w gotowym ujęciu, np. choinka, potem bałwanek, potem śnieżynki. |
| `przyklad_reklama_A.json`, `przyklad_reklama_B.json` | Prawdziwe konfiguracje reklam A i B (wzór do kopiowania). |
| `przyklad_podmiana.json` | Przykład podmiany wzoru. |

**Instrukcja dla asystenta:** przeczytaj całość, zainstaluj narzędzia z punktu 1, a potem pracuj według punktów 2–8. Przed oddaniem filmu zawsze obejrzyj klatki (punkt 6).

---

## 1. Instalacja (raz)

**Mac** (w Terminalu):
```
brew install ffmpeg python
pip3 install pillow numpy opencv-python
```
Windows: ffmpeg z gyan.dev, Python z python.org, potem to samo `pip install`.

**Czcionka Inter.** Pobierz paczkę z github.com/rsms/inter (zakładka Releases) i skopiuj `Inter-Black`, `Inter-Bold` i `Inter-ExtraBold` (pliki .otf albo .ttf) do folderu `fonts/` obok configu. Można też podać ścieżkę w configu: `"font_dir": "/ścieżka"`.

**Kolorowe emoji Google:**
```
npm pack emoji-datasource-google@15.1.2
tar -xzf emoji-datasource-google-15.1.2.tgz package/img/google/64
mv package/img/google/64 emoji/64
```
W configu: `"emoji_dir": "emoji/64"`. Emoji podajesz kodem, np. `1f525` 🔥, `1f3c6` 🏆, `2728` ✨, `1f384` 🎄, `26c4` ⛄, `2744` ❄️, `1f4f1` 📱, `1f440` 👀, `1f633` 😳, `1f644` 🙄, `1f923` 🤣, `1f605` 😅, `1f4f8` 📸, `1f447` 👇, `1f6d2` 🛒, `1f50c` 🔌, `23f1` ⏱️. Kody znajdziesz w nazwach plików w `emoji/64`.

**Logo:** plik `logo_winterly.png` (jasne lub złote logo na przezroczystym tle, np. z Shopify: Ustawienia → Marka). Bez pliku plansza końcowa pokaże złoty napis „Winterly”.

**Układ folderu projektu:**
```
Winterly/
  fonts/  emoji/64/  logo_winterly.png
  muzyka/  (darmowe utwory z Pixabay)
  reklama_C/   c1.mp4 c2.mp4 ...  lektor.mp3  config.json
```

## 2. Scenariusz i lektor

- **Długość:** 20–26 s, jeden lektor przez cały film.
- **Format, który sprzedaje: historia, nie lista zalet.**
  1. Hak z problemem albo zaciekawieniem („Sąsiadka przyszła z pretensjami”).
  2. Rozwinięcie.
  3. Odsłonięcie balkonu z kurtyną.
  4. 2–3 wzory pod rząd i „jednym kliknięciem w telefonie”.
  5. Dowód społeczny („ludzie robią zdjęcia”).
  6. „Link do kurtyny zostawiam pod filmem”.
- **Scena:** polski blok, balkon, podwórko. Amerykańskie domy z garażami sprzedają słabo.
- **Wzory na kurtynie muszą zgadzać się z tym, co mówi lektor** (np. „raz choinka, raz bałwanek, a raz śnieżynki”). Nie wymieniaj wzorów, których nie widać na ekranie.
- **Uczciwie:** nie mów „Mikołaj w saniach z reniferami”, bo na 400 kropkach to nieczytelne. Lepiej „Mikołaj”. Kostki nie ma w zestawie, więc mów „wtyczka do USB”, a nie „kabel w zestawie”.
- **ElevenLabs:** model Multilingual v2, Stability ok. 40–50%, Similarity 75%, Style 0–15%.
  - Głos kobiecy: **Kinga**. Głos męski z humorem: **Kamil – Expressive, Joyful**.
  - Unikaj „Adama” (najczęstszy głos z TikToka, od razu słychać AI).
  - Przed puentą wpisz „...”: zrobi pauzę.

## 3. Ujęcia z Google Omni (Veo)

- **Każde ujęcie osobno:** jedna prosta akcja, bez cięć, 8 s, pion 9:16. Na końcu promptu: `Audio: ..., no speech. No text, no logos, no jump cuts.`
- **Ruch kamery i przejścia robimy w montażu**, a nie w jednym klipie. Gdy Omni ma pokazać „dzieci, a potem balkon” w jednym ujęciu, wymyśla przeskoki i zmienia budynek.
- **Kurtyna musi wyglądać prawdziwie** (3 × 2 m ma tylko 400 diod). Wklejaj ten opis do każdego promptu:
  > a 3 m wide, 2 m tall LED curtain hung on the OUTSIDE of the balcony railing, top edge fixed with small hooks along the handrail, about 20 thin transparent vertical wires, about 20 LEDs each, dots 10–15 cm apart with big dark gaps, showing simple blocky low-resolution pixel art like a 20 x 20 pixel icon, other LEDs off, not a screen
- **Obraz referencyjny:** prawdziwe zdjęcie kurtyny od dostawcy albo obrazek wzoru z kropek (np. Mikołaj 20 × 20).
- **Spójność:** najpierw zrób obrazki referencyjne bloku i postaci, potem używaj ich jako pierwszej klatki lub postaci w kolejnych klipach.
- **Odrzucaj ujęcia, w których:**
  - kurtyna wygląda jak gładki ekran albo telewizor;
  - wisi w powietrzu albo w środku podwórka;
  - na balkonie są dodatkowe lampki (sople), których nie ma w zestawie;
  - w środku klipu zmienia się budynek albo osoba.
- **Każde ujęcie zrób w 2 wersjach.**
- **Ujęcia konkurencji** wolno użyć tylko jako zastępstwo w wersji roboczej. Przed publikacją właściciel podmienia je w Higgsfield.

## 4. Przegląd klipów i czasy słów

**Podgląd klipu (1 klatka na sekundę z numerem sekundy):**
```
ffmpeg -i klip.mp4 -vf "fps=1,scale=160:-1,drawtext=fontfile=fonts/Inter-Bold.otf:text='%{eif\:t\:d}':x=4:y=4:fontsize=18:fontcolor=yellow:box=1:boxcolor=black@0.6,tile=10x1" -frames:v 1 podglad.jpg
```

**Gdzie w klipie są cięcia** (AI często wstawia ukryte przeskoki):
```
ffmpeg -i klip.mp4 -vf "select='gt(scene,0.2)',metadata=print" -an -f null - 2>&1 | grep -o "pts_time:[0-9.]*"
```

**Pauzy w lektorze:**
```
ffmpeg -i lektor.mp3 -af silencedetect=n=-32dB:d=0.06 -f null - 2>&1 | grep -oE "silence_(start|end): [0-9.]+"
```
- Duże pauzy (ponad 0,3 s) to końce zdań. Drobne (n=-27dB, d=0.035) to granice słów.
- Gdy brak pauzy między słowami, dziel czas proporcjonalnie do liczby sylab (ok. 0,18–0,2 s na sylabę).
- Napis pojawia się w momencie, gdy lektor zaczyna dane słowo.

## 5. Config i montaż

**Struktura `config.json`** (patrz `przyklad_reklama_A.json`):

- **`beats`**, czyli bity, jeden na każde zdanie lektora:
  - `dur`: czas od początku tego zdania do początku następnego.
  - `segs`: ujęcia w formacie `[plik, start_w_klipie, długość, kadrowanie_od_góry, {opcje}]`.
    - Długości w bicie są przeliczane proporcjonalnie do `dur`.
    - `kadrowanie_od_góry` (np. 0.2) obcina górę, żeby ukryć obcy napis.
    - Opcje: `{"flash": true}` to biały błysk na początku ujęcia (używaj tylko przy zmianie wzoru, wygląda jak „klik”). `{"speed": 0.9}` zwalnia ujęcie. `{"cover": {"y": 0.25, "h": 0.11, "w": 0.82, "label": "WZÓR Z TELEFONU", "emoji": "1f4f1"}}` to biała etykieta na obcy napis.
  - `subs`: napisy w formacie `[czas_od_początku_bitu, "tekst z *złotym* słowem", "emoji", wysokość]`.
    - `|` łamie linię.
    - Wysokość podana jako ułamek ekranu, np. 0.84 (domyślnie `sub_y`, czyli 0.69).
- **`hook`**: duży napis na górze przez pierwsze ~3,5 s (`until`, `y` ok. 0.12–0.14).
- **`stickers`**: czerwone plakietki, np. „BLACK FRIDAY: do −35%”, albo złota „1. MIEJSCE” (`bg` [255,205,72,255], `fg` [30,22,18,255]).
- **`badge_from`**: od której sekundy w rogu pojawia się „winterly.pl”. Ustaw po haku.
- **`end_dur`** i **`end`**: plansza końcowa. Ok. 4,5 s, zaczyna się razem ze zdaniem „Link do kurtyny…”.
- **`dissolve`**: 3 klatki (delikatne przenikanie). **`punch`**: false.

**Gdzie stawiać napisy:**
- nigdy na kurtynie: w ujęciach balkonu pod kurtyną (0.80–0.84);
- przy telefonie nad telefonem (0.35–0.5);
- domyślnie 0.69;
- naklejki BF tam, gdzie nie zasłaniają twarzy ani zapalającej się kurtyny;
- dolne ok. 10% ekranu zostaw wolne (przyciski Reels).

**Uruchomienie:**
```
python3 -I render_winterly.py config.json                         # obraz (bez dźwięku)
bash miks_audio.sh lektor.mp3 muzyka/jazz.mp3 obraz.mp4 Winterly_C.mp4   # dźwięk i gotowy film
```

**Podmiana wzoru na kurtynie** (`podmiana_wzoru.py`):
1. Wyciągnij stopklatkę z miejsca, gdzie kończysz oryginalne ujęcie: `ffmpeg -ss 3.79 -i balkon.mp4 -frames:v 1 stopklatka.png`.
2. Zmierz górną i dolną krawędź kurtyny jako linie `y = a + b·x`. Narysuj je na klatce i popraw, aż spod nowego wzoru nie prześwituje stary.
3. W configu montażu wstaw `podmiana.mp4` zaraz po oryginalnym ujęciu, z `flash` przy każdej zmianie wzoru.

## 6. Kontrola przed oddaniem (obowiązkowo)

- **Klatki w kluczowych momentach:** wyciągnij 8–16 klatek (`ffmpeg -ss T -i film.mp4 -frames:v 1 -vf scale=270:480 k_T.png`), sklej w siatkę i obejrzyj. Sprawdź:
  - czy napisy mieszczą się w ekranie;
  - czy niczego nie zasłaniają;
  - czy na kurtynie nie prześwituje stary wzór;
  - czy przejścia mają sens.
- **Głośność:** ok. −14 LUFS, szczyt poniżej −1 dBFS (`miks_audio.sh` wypisuje to na końcu).
- **Plansza końcowa:** logo, BLACK FRIDAY • do −35%, „Zamów na winterly.pl”, KUP TERAZ, „Kurtyna 3 × 2 m: 239,99 zł | Płatność przy odbiorze • 30 dni na zwrot”.
- **Napisy:** jeśli lektor powiedział coś inaczej niż w scenariuszu, popraw napisy.

## 7. Czego właściciel nie chce (uwagi z poprzednich wersji)

- **Bez rozmytego paska za etykietami.** Etykieta ma być biała, pełna, wystarczająco duża, żeby zakryć obcy napis.
- **Bez szarpanych przybliżeń przy cięciach** („zbyt chaotyczne”). Dłuższe ujęcia, spokojny rytm, przenikanie 3–6 klatek.
- **Bez losowych przejść:** cała historia w jednym miejscu (blok, balkon, podwórko). Na końcu nie wstawiaj nagle domów z garażami.
- **Dźwięk:** głos bez odszumiania (inaczej brzmi sztucznie). Muzyka cicho i równo, bez „pompowania” pod głosem.
- **Muzyka tylko darmowa** (Pixabay). Żadnych znanych piosenek (prawa autorskie).
- **Kurtyna zawsze uczciwie:** kropki, nie gładki ekran. Prawdziwa ma ok. 20 × 20 kropek.

## 8. Po montażu: zapis i wgranie

1. **Zapisz gotowy film na stałe:** w folderze projektu i w plikach Shopify (Treści → Pliki). Folder tymczasowy czatu w chmurze może się wyczyścić.
2. **Wgraj do Meta** z adresu URL pliku w Shopify (`https://cdn.shopify.com/videos/c/o/v/<klucz>.mp4`, oryginalna jakość).
3. **Kreacja:**
   - wyłącz wszystkie ulepszenia Advantage+ (teksty AI, muzyka, przycinanie, naklejki itd.);
   - przycisk SHOP_NOW;
   - link z `utm_content=<nazwa_filmu>`, żeby w Shopify było widać, która reklama sprzedała;
   - 3 teksty główne, 3 nagłówki, 2 opisy;
   - okładka: klatka z hakiem.
4. **Publikacja:** reklamę dodajesz jako szkic i publikujesz tylko ją, dopiero po „go” właściciela.
5. **Ocena wersji:** po 3–4 dniach patrz na zamówienia w Shopify według `utm_content`, a nie tylko na zakupy w Meta (pobrań Meta czasem nie widzi).
