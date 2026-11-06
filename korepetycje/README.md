# Korepetycje – aplikacja do rozliczania zajęć

Prosta aplikacja do własnego użytku. To jeden plik `index.html`: działa w przeglądarce na telefonie i komputerze, bez serwera, bez konta i bez opłat.

## Co umie

- **Uczniowie** – imię, telefon (kliknij, żeby zadzwonić albo napisać SMS), rodzic, e-mail, przedmiot, klasa, stawka za godzinę, opis/notatki.
- **Stały plan zajęć** – np. „wtorek 16:00, 60 min”, także co 2 tygodnie. Terminy same pojawiają się w kalendarzu.
- **Kalendarz** – widok tygodnia i miesiąca, dodawanie, przenoszenie i odwoływanie zajęć.
- **Potwierdzanie zajęć** jednym kliknięciem: „✓ Odbyte”, „✓ + gotówka”, „✓ + przelew”, „✓ + BLIK”, „✕ Odwołane”, „Odwołane – płatne”.
- **Wpłaty** – gotówka, przelew, BLIK, inne. Widać, kto zapłacił gotówką.
- **Saldo ucznia** – ile jest winien albo ile ma nadpłaty (zapłacone z góry). Pełna historia z saldem narastającym.
- **Pulpit** – zarobek w tym tygodniu i miesiącu, wpłaty (w tym gotówka), suma zaległości.
- **Prognozy** – najbliższe 7 dni, 2 tygodnie, następny miesiąc oraz stały plan na tydzień, 2 tygodnie i miesiąc.
- **Raporty** – miesiąc po miesiącu, rozbicie na uczniów, wykres z 12 miesięcy, podsumowanie roku.
- **Kopia zapasowa** do pliku JSON i eksport zajęć oraz wpłat do CSV (Excel).

## Jak liczone jest saldo

```
saldo = saldo początkowe + wpłaty − (zajęcia odbyte + odwołane-płatne)
```

- Saldo ujemne oznacza, że uczeń jest winien.
- Saldo dodatnie oznacza nadpłatę.
- Zajęcia ze stałego planu liczą się do salda dopiero po potwierdzeniu. Niepotwierdzone czekają na pulpicie w sekcji „Do potwierdzenia”.

## Jak mieć ją na telefonie

Aplikacja jest instalowalna (PWA): ma własną ikonę, otwiera się na pełnym ekranie i działa bez internetu.

### 1. Wystaw ją pod adresem (jednorazowo, za darmo – GitHub Pages)

1. Na GitHubie wejdź w repozytorium **mordeczkodzi/lala** → **Settings** → **Pages**.
2. **Source:** „Deploy from a branch”.
3. **Branch:** `claude/tutoring-accounting-app-ruo74o` (albo `main`, jeśli zmiany zostaną tam scalone), folder **/ (root)** → **Save**.
4. Po 1–2 minutach aplikacja będzie pod adresem:
   **https://mordeczkodzi.github.io/lala/korepetycje/**

### 2. Zainstaluj na telefonie

- **Android (Chrome):** otwórz adres → menu ⋮ → **„Zainstaluj aplikację”** (albo przycisk w *Ustawieniach* aplikacji).
- **iPhone (Safari):** otwórz adres → przycisk **Udostępnij** □↑ → **„Do ekranu początkowego”**.

Na iPhonie aplikacja z ikony ma **osobne dane** niż ta sama strona w Safari. Najpierw ją zainstaluj, a dopiero potem wpisuj dane (albo przenieś je kopią zapasową).

Aktualizacje wgrane do repozytorium pojawią się w aplikacji same, po ponownym otwarciu z internetem.

Na komputerze wystarczy otworzyć `index.html` w przeglądarce.

## Ważne: gdzie są dane

Dane są zapisywane **tylko w tej przeglądarce, na tym urządzeniu** (localStorage). Wyczyszczenie danych przeglądarki je usunie. Dlatego rób regularnie kopię: **Ustawienia → Pobierz kopię**, a plik trzymaj np. na Dysku Google. Tym samym plikiem przeniesiesz dane na inne urządzenie (**Wczytaj kopię**).
