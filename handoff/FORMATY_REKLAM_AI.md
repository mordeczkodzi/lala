# 7 formatów reklam z AI: research, Higgsfield i montaż

Notatki z materiałów „6 formatów reklam z AI” (therealones.io, kanał Kamil Działo), dopasowane do naszych sklepów. Przyklejone przez właściciela 05.11.2026. Uzupełniają `PRZEWODNIK_FILMY_REKLAMY.md`, czyli nasz sposób montażu skryptem `video-tools/montaz.py`.

## Proces w trzech krokach

1. **Claude: research, potem prompt.** Najpierw research klientów, dopiero potem kąt, hak, skrypt, prompt do Higgsfield i lista B-roli.
2. **Higgsfield: generowanie.** Wideo z osobą albo produktem, osobno czysty polski głos, osobno B-rolle.
3. **Claude: montaż.** Cięcia pod zdania lektora, napisy słowo w słowo, hak na górze, plansza końcowa.

Koszt jednej reklamy: około 250–400 kredytów Higgsfield.
- Wideo Marketing Studio: ok. 75.
- Seedance 2.5: ok. 105 (około 10 minut generowania).
- Głos: kilka kredytów.
- B-roll: ok. 30 za klip.

## Krok 1. Research klientów (zawsze przed skryptem)

Szukamy opinii i rozmów o takich produktach: Amazon, AliExpress, Allegro, Reddit, komentarze pod reklamami, TikTok. Wypisujemy:

- kto kupuje i dla kogo: dla siebie czy na prezent, okazja, wiek, sytuacja;
- 3 największe problemy albo pragnienia, które produkt rozwiązuje;
- 3 najczęstsze obiekcje przed zakupem;
- 10 zwrotów, których klienci używają własnymi słowami.

Z tego wybieramy **jeden kąt**: do kogo mówimy i co obiecujemy. Hak i skrypt piszemy językiem klienta. Research zapisujemy w `research.md` i używamy go ponownie, zamiast robić od nowa.

**Gdy jest wzór** (reklama konkurencji z Biblioteki Reklam Meta, filtr „aktywne”):
- im starsza data startu, tym lepszy wzór;
- wyciągamy klatkę co 1 s i spisujemy mowę;
- w 3 zdaniach opisujemy styl, hak w pierwszej sekundzie i kolejność scen.

## Krok 2. Co ma dać Claude dla każdej reklamy

- **Prompt do Higgsfield po angielsku**, maks. 120 słów, w tej kolejności:
  1. format i kamera;
  2. kto i gdzie;
  3. produkt: `the exact [produkt] from the reference image, unchanged`;
  4. co się dzieje po kolei, z sekundami;
  5. mowa: dokładne zdanie po polsku w cudzysłowie albo `no voice`;
  6. na końcu `no on-screen text, no logos`.
- **Hak na ekran po polsku:** maks. 6 słów.
- **Skrypt lektora po polsku na 12–14 s** albo informacja, że reklama jest bez mowy.
- **5–8 ujęć B-roli.** Każde ujęcie ma dwa prompty:
  - **Image (GPT Image 2):** pionowo 9:16, produkt „the exact … from the reference image, unchanged”, `no text, no logos`;
  - **Video (Kling 3.0):** ruch, który ożywia ten kadr w 5 s.
- **Ustawienia Higgsfield i koszt w kredytach** (patrz ściąga niżej).
- Wszystko w jednym pliku, np. `prompty/4-unboxing.md`.

## Krok 3. Higgsfield: jak generować

**a) Wideo w Marketing Studio** (UGC, unboxing, produkt „wow”)
- Ścieżka: Marketing Studio → Video, wklejamy prompt.
- Styl: UGC → At home, UGC → Unboxing albo Motion → Hypermotion.
- Ustawienia: 9:16, 15 s, Product = zdjęcie produktu.
- Uwaga: polska mowa z Marketing Studio ma obcy akcent, więc głosu stamtąd nie używamy.

**b) Czysty polski głos**
- Ścieżka: Audio → Text to Speech → ElevenLabs.
- Głos Ainsley (kobiecy) albo Arthur (męski). U nas działa też ElevenLabs „Kinga”.
- Plik zapisujemy jako `glos.mp3`.

**c) Usta zgrane z polskim głosem** (Video → Seedance 2.5)
1. Zatrzymujemy wideo z kroku a na klatce z twarzą i produktem i robimy zrzut. Dzięki temu w kolejnym wideo jest ta sama osoba, ubranie i pokój.
2. W Video przez „+” dodajemy: zrzut osoby, zdjęcie produktu, `glos.mp3`. Wklejamy prompt „ruch ust”.
3. Model Seedance 2.5 (domyślnie jest 2.0, trzeba przełączyć), 15 s, dźwięk włączony.
4. Wynik zapisujemy jako `a-roll.mp4`.

Szablon promptu „ruch ust”:
> The same [woman/man] from the first reference image (same face, hair, clothes, same room) holds the exact [produkt] from the second reference image and talks directly to the camera. [She/He] lip-syncs exactly to the provided Polish voice audio, word for word, with natural mouth movements. Around [X] seconds [akcja z produktem]. Use only the provided audio as [her/his] voice, no music, no other speech. Handheld, authentic, natural light, no on-screen text, no logos.

Formaty bez osoby mówiącej (problem → rozwiązanie, kopia zwycięzcy) robimy od razu w Seedance 2.5 ze zdjęciem produktu.

**d) B-rolle, dwa ruchy na ujęcie**
1. Image → GPT Image 2, 9:16, zdjęcie produktu i prompt „Image”. Powstaje kadr.
2. Video → Kling 3.0, ten kadr jako pierwsza klatka, prompt „Video”, 5 s, dźwięk wyłączony.

Na 15 s reklamy wystarczą 4–5 klipów.

**Grafiki do tych samych kątów:**
- Ads Studio → Create ads: zdjęcie albo link produktu, format 3:4. Bez promptu robi kilkanaście grafik z tekstami.
- GPT Image 2, gdy chcemy konkretny układ: przed i po, diagram cech, prezent z ceną, „N światów w jednym produkcie”. Polskie znaki wychodzą czysto.

## Krok 4. Zasady montażu

- **Hak:** w białej zaokrąglonej ramce u góry przez pierwsze 2–3 s.
- **Napisy:** słowo w słowo co 1–2 s, białe, grube, z czarnym obrysem, na dole kadru. Czasy słów bierzemy z `glos.mp3`. Napisy nie dublują haka.
  - **Nasza zasada wygrywa:** właściciel woli napisy bez tła, półprzezroczyste, a hak duży i tylko na chwilę (patrz `PRZEWODNIK_FILMY_REKLAMY.md`).
- **Cięcia:** przy każdym zdaniu cięcie na B-roll pasujący do tego, o czym akurat mowa. Fragmenty a-roll wstawiamy dokładnie w czasie słów tej osoby, żeby zgadzał się ruch ust.
- **Reklama bez mowy:** bez napisów, z muzyką bez praw autorskich.
- **Koniec:** 2 s planszy z jednym zdaniem obietnicy.
- **Plik:** zapisujemy bez metadanych i robimy stykówkę klatek co 1 s do sprawdzenia.

## Bezpieczeństwo konta reklamowego

- Używamy tylko zdjęć i klipów od dostawcy albo z Higgsfield.
- Cudze reklamy to wyłącznie wzór układu scen. Nie wklejamy ich zdjęć, filmów, logo ani tekstów.
- W każdym prompcie: `no logos, no on-screen text`.
- Dzieci pokazujemy tylko od tyłu, bez twarzy.

## 7 formatów

| # | Format | Kiedy | Budowa | Wideo | Głos | Ruch ust |
|---|---|---|---|---|---|---|
| 1 | **UGC: „ktoś jak klient” poleca** | produkt rozwiązuje codzienny problem | osobista historia w 1. sekundzie → produkt w rękach → jak działa → efekt, napis co 1–2 s | Marketing Studio: UGC → At home | Ainsley | Seedance 2.5 + kadr + `glos.mp3` |
| 2 | **Problem → rozwiązanie** | problem da się pokazać w 1 s, produkt w 2. | 1. s problem, 2. s produkt, reszta efekt, bez gadania do kamery | Seedance 2.5 + zdjęcie produktu | Ainsley | nie |
| 3 | **Produkt „wow”** | sam efekt robi wrażenie (światło, ruch, przemiana) | produkt w akcji, co 2–3 s inny efekt, bez ludzi i mowy | Marketing Studio: Motion → Hypermotion | brak, muzyka | nie |
| 4 | **Unboxing prezentu** | prezenty, cały IV kwartał | odliczanie 3-2-1, 2–3 s rozpakowania, 10+ s efektu i reakcji obdarowanego | Marketing Studio: UGC → Unboxing | Ainsley | nie |
| 5 | **Recenzja z obiekcją** | klienci boją się, że to tandeta | start od obiekcji („kupiłeś głupią lampkę?”), test, zaskoczenie | Marketing Studio: UGC → At home (kadr) | Arthur | Seedance 2.5 |
| 6 | **Sonda uliczna** | chcemy oglądalności do końca, wygląda jak treść, nie reklama | pytanie z mikrofonem → zabawna odpowiedź → produkt w kadrze → „gdzie to kupić?” | Marketing Studio: UGC (kadr sceny) | Ainsley (pytanie) + Arthur (odpowiedzi), każde zdanie osobno, sklejone w jeden plik | Seedance 2.5 (dialog) |
| 7 | **Kopia zwycięzcy konkurencji** | reklama konkurencji chodzi ponad rok | kopiujemy układ scen, nie nagranie: szybkie demo, co 2–3 s inny świat, hak tekstowy na górze, bez mowy | Seedance 2.5 + zdjęcie produktu | brak | nie |

Przykładowe haki z materiałów (lampka-projektor dla dzieci):
- „Mój syn bał się ciemności” (1)
- „Twoje dziecko boi się ciemności?” (2)
- „POV: sufit w pokoju dziecka zamienia się w kosmos” (3)
- „Prezent, o którym marzy każde dziecko” (4)
- „»Kupiłeś głupią lampkę za stówę«” (5)
- „Sonda: jaki prezent dla dziecka naprawdę działa?” (6)
- „Zmień porę snu w przygodę” (7)

Przykładowe plansze końcowe:
- „Prezent, który świeci co wieczór”
- „6 światów w jednej lampce”
- „Koniec ze strachem przed ciemnością”

## Te same kroki bez Higgsfield (właściciel ma ChatGPT i narzędzia Google, Higgsfield ma kolega)

| Krok | Higgsfield (kolega) | U nas |
|---|---|---|
| Kadr B-roll z produktem | Image → GPT Image 2 | ChatGPT (generowanie obrazów) albo generator obrazów Google; zdjęcie produktu jako referencja, ten sam prompt „Image” |
| Ruch 5 s z kadru | Video → Kling 3.0 | wideo Google (image → video), ten sam prompt „Video”, pionowo 9:16 |
| Polski lektor | Audio → ElevenLabs | ElevenLabs (głos Kinga, już używany) |
| Osoba mówi po polsku, usta zgrane | Seedance 2.5 + kadr + `glos.mp3` | brak pewnego odpowiednika; polska mowa generowana w wideo zwykle ma akcent → formaty z osobą mówiącą (1, 5, 6) robi kolega w Seedance albo zamieniamy je na lektora z offu |
| Montaż | Claude + ffmpeg | `video-tools/montaz.py` (nasz styl napisów) |

Bez Higgsfield najlepiej wychodzą formaty bez gadania do kamery: 2, 3, 4 i 7, z lektorem z offu albo z samą muzyką.

## Nasze gotowe filmy Winterly a formaty

- **`Winterly_reklama_lektor_v2.mp4`** („Zwykłe lampki w 2026? Serio?”): format **2, problem → rozwiązanie**, z montażem efektów jak w formacie 3. Problem: plątanina i nuda. Rozwiązanie: pudełko, montaż, aplikacja, efekt, sąsiedzi. Lektor z offu, nikt nie mówi do kamery. Ujęcia z cudzych reklam są tylko szkicem pod podmianę na nasze.
- **`Winterly_historia_lektor.mp4`** („Pięć minut montażu… i mój balkon stał się atrakcją osiedla”): format **7, kopia zwycięzcy**, czyli układ narracyjnej reklamy GlowMax. Opowieść w 1. osobie brzmi jak UGC (format 1), ale bez osoby w kadrze.
- Brakuje nam jeszcze: **4 unboxing prezentu** (najlepszy na IV kwartał), **5 recenzji z obiekcją** (cena) i czystego **3 „wow”** bez lektora.

## Jak to przekładamy na Winterly (lampki na choinkę i kurtyna LED)

Propozycje do sprawdzenia researchem, zanim powstanie skrypt:

| # | Format | Kąt i hak (propozycja) |
|---|---|---|
| 1 | UGC | „Co roku plątanina lampek…” → gwiazda na czubek, pasma w dół, wzór z telefonu |
| 2 | Problem → rozwiązanie | ciemny, nudny balkon albo choinka → klik → animacja; „Twój balkon wygląda tak samo jak u wszystkich?” |
| 3 | Produkt „wow” | sama kurtyna albo choinka, co 2–3 s inny motyw (Mikołaj, sanie, bałwan, śnieg); „POV: Twoja choinka robi pokaz” |
| 4 | Unboxing prezentu | **najlepszy na listopad i grudzień**: otwarcie pudełka Winterly (nasz klip), odliczanie, reakcja rodziny; „Prezent, który robi wow przy choince” |
| 5 | Recenzja z obiekcją | „Żona mówi, że kupiłem drogie lampki za 250 zł. No to patrzcie…”, zbija obiekcję ceny |
| 6 | Sonda uliczna | „Jakie lampki macie w tym roku na święta?” → kurtyna Winterly → „Dobra. Gdzie to kupić?” |
| 7 | Kopia zwycięzcy | układ reklamy GlowMax (historia z balkonem i sąsiadami), już zrobione jako `Winterly_historia_lektor.mp4` |

Nasze uwagi, przenoszone z wcześniejszej pracy:
- Black Month: CTA ma mówić o promocji (u nas: drugi zestaw −50 zł) i o tym, gdzie kupić (winterly.pl).
- Strona docelowa reklam lampek: `/products/inteligentne-lampki-na-choinke`, nie strona główna.
- Gęstość diod na wygenerowanym obrazie ma odpowiadać prawdziwej kurtynie (400 diod, 20 × 20). Inaczej będą zwroty i komentarze „nie wygląda jak w reklamie”.
