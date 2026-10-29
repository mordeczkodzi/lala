# Otully: przekazanie projektu do nowego czatu

**Jak użyć:** w nowym oknie Claude Code (repo `mordeczkodzi/lala`, gałąź `claude/zen-babbage-tvt5u7`) wklej:

> Przeczytaj `handoff/PRZEKAZANIE.md` i `handoff/PODRECZNIK_FILMY.md`. Kontynuujemy projekt Otully: sklep Shopify z Otulką i kampanię Meta. Skrypty do filmów są w `handoff/video-tools/`.

Pełny eksport poprzedniej rozmowy (wszystkie prompty, scenariusze i decyzje) to `czat_otully.md`, osobny plik, który dostałeś do pobrania. Wrzuć go do nowego czatu, jeśli potrzebny jest pełny kontekst.

---

## Sklep

- **Shopify:** „Otully”, `p20cwe-y1.myshopify.com`, domena **otully.pl**.
- **Produkt:** „Otulka – termofor do noszenia z pasem”, handle `otulka-termofor-z-pasem`, ID `gid://shopify/Product/16119587668298`.
  - Kolory: Beżowy, Jasnoszary, Grafitowy, Różowy, Czekoladowy.
  - Zestawy: **Standard 159 zł** (przekreślona 191), **Przytulny 185 zł** (przekreślona 336), **Sam pasek 69 zł** (dokupywany osobno, nie reklamujemy).
  - Link w reklamach: `https://otully.pl/products/otulka-termofor-z-pasem?variant=63990651322698` (Beżowy / Przytulny).
- **Motywy:**
  - prace tylko w szkicu „Otulka — DRAFT” (`210102583626`);
  - **nigdy nie pisać do motywu na żywo** `210100814154`, chyba że właściciel wyraźnie każe;
  - jeśli szkic został w międzyczasie opublikowany, sprawdź w Shopify, który motyw jest teraz na żywo.
- **Kod motywu:** w repo `shopify-otulka/`. Najważniejsze zmiany:
  - szuflada koszyka: pasek darmowej wysyłki od 200 zł, „Wyczyść koszyk”, polecany produkt, przycisk „Przejdź do kasy · kwota”;
  - pasek UGC „Otulka w akcji” w hero;
  - 3 opinie ze zdjęciami (od klientów z maila);
  - e-mail kontakt@otully.pl.
- **Do zrobienia ręcznie w panelu:** e-mail sklepu i e-mail w polityce prywatności. Brak uprawnień API.

## Meta Ads

- **Konto reklamowe:** SferaKobiety `1287540323347655`, PLN, firma SferaKobiety `1291890349122529`.
- **Strona FB:** **Otully** `1076974198837564`.
- **Instagram:** @otullypl połączony ze stroną Otully, ale konto reklamowe nie widziało go przez API. Tożsamość IG przełącza się w Menedżerze: Edytuj → Tożsamość → Konto na Instagramie → otullypl. W razie braku: Ustawienia firmy → Konta na Instagramie → Przypisz zasoby → konto reklamowe.
- **Piksel / zbiór danych:** **Otully.pl** `1891261918903113`. Zbiera PageView i ViewContent. **Zakup trzeba potwierdzić testowym zamówieniem.**

### Kampania (stan na 29.10.2026, WSTRZYMANA)

- **Kampania:** „Otully | Sprzedaż | Szeroko | Test 1” `120250721442330554`.
  - Cel: Sprzedaż, budżet 100 zł dziennie na całą kampanię, najniższy koszt.
- **Grupa reklam:** „PL | Szeroko | Zakup | start 30.10” `120250731756310554`.
  - Polska, 18+, szeroko (Advantage+ Audience), umiejscowienia automatyczne.
  - Optymalizacja: zakup (PURCHASE).
  - **Start 30.10.2026 00:01.** DSA: Otully / Otully.
- **Reklamy** (każda: 3 teksty główne, 3 nagłówki, 2 opisy, przycisk „Kup teraz”, UTM `utm_source=meta&utm_medium=paid&utm_campaign=test1&utm_content=<nazwa>`):

  | Reklama | ID | Kreacja |
  |---|---|---|
  | Film A – termofor który się nosi | 120250731759700554 | 1135316245551041 |
  | Film C – 3 powody | 120250731760080554 | 1172053092182082 |
  | Grafika B – niezastąpiony | 120250731760580554 | 1228807149573849 |
  | Film B – panowie bohaterowie | 120250731761100554 | 1730446845137810 |
  | Grafika A – najlepszy prezent | 120250731761360554 | 1461965609213108 |

- **Media w koncie Meta:**
  - filmy: A `1471695624816658`, B `1517923276778254`, C `1147969921012912`;
  - grafiki (hash): A `8a223eb493dfa7e6493fc78060bdc990`, B `a6303e27a35719978d3fb9316805aefc`;
  - miniatury: A `478242f8edf570e7d953a2fadf076897`, B `e15ca6bd062579431008a34426bbc7a4`, C `ece145322ea7d248689d2d28cc6139a4`.
- **Kopie plików:** `cdn.shopify.com/s/files/1/1090/2536/2250/files/otully_*.jpg` oraz filmy w Plikach Shopify (alt „meta filmA/B/C”).
- **Decyzje właściciela:**
  - **bez oznaczenia AI** (pole puste);
  - na razie bez podziału na grupy odbiorców, szeroko.
- **Usunięte:** stara kampania `120250721049130554` i stara grupa reklam `120250721444630554`.

### Zostało do zrobienia przed startem

1. Przełączyć tożsamość IG w 5 reklamach na @otullypl (patrz wyżej).
2. W „Ulepszeniach Advantage+” każdej reklamy wyłączyć **Muzykę**, bo zagłusza lektora.
3. Zrobić testowe zamówienie i sprawdzić, czy Purchase trafia do piksela.
4. **Włączyć kampanię.** Ze startem 30.10 00:01 włączenie wcześniej niczego nie wydaje do tej godziny. Bez włączenia nic nie wystartuje.
5. **Uwaga:** jeśli godzina startu minie, zanim kampania zostanie włączona, Meta blokuje zmianę daty. Trzeba wtedy zrobić nową grupę reklam z nową datą i przenieść reklamy.

### Zasady testu (pierwsze 10–14 dni)

- **Pierwsze 3 dni nic nie zmieniać,** bo trwa faza nauki.
- **~100 zł wydane na reklamę i 0 dodań do koszyka** → wyłączyć tę reklamę.
- **CTR < 1% albo CPC > 2 zł** → zmienić pierwsze 3 sekundy filmu (hook).
- **Koszt zakupu < ~80 zł** → podnosić budżet o 20–30% co 2–3 dni.

## Konkurencja (z WinningHunter)

- **Hot Hugger** (huggercomfort.com):
  - działa naprawdę: 82% ruchu z Francji, ~23 tys. wizyt miesięcznie (176 tys. w grudniu);
  - działają u nich montaże UGC z napisem-memem, kąt „prezent” i lista o endometriozie.
- **Otulaj.pl i Ciepłopas:** reklamy już wyłączone, wydawali grosze. Otulaj miał gładkie, sztuczne kreacje, tego unikamy.

## Pliki kreacji

- **Filmy końcowe:** A 16.8 s, B 20.2 s, C 23.1 s, 1080×1920 z lektorem, napisami, hookiem i logo na końcu. Właściciel ma je u siebie.
- **Grafiki 4:5 (1080×1350):**
  - A: „Najlepszy prezent dla osoby z bolesną miesiączką”;
  - B: „Niezastąpiony podczas miesiączki”.
- **Jak zrobić następne filmy:** `PODRECZNIK_FILMY.md`.

## Pomysły na dalej

- Wygenerować ponownie klip z herbatą w Filmie B, z referencją twarzy, bo teraz występuje tam inna para.
- Dodatkowe wersje hooka do testu, np. „Koniec z trzymaniem termoforu w rękach”, „Wstajesz… i termofor ląduje na podłodze 🙄”.
- Wersje z samą muzyką, bez lektora (potrzebna muzyka od właściciela albo z biblioteki Meta).
- Po teście: osobne grupy dla kobiet i dla mężczyzn (prezent), jeśli dane pokażą różnicę.
