# Korepetycje – aplikacja do rozliczania zajęć

Prosta aplikacja do własnego użytku. To jeden plik `index.html`: działa w przeglądarce na telefonie i komputerze, bez serwera, bez konta i bez opłat.

## Co umie

Układ jak w aplikacji mobilnej: granatowy pasek u góry i dolne menu **Główna · Uczniowie · Grafik · Finanse · Ustawienia**.

- **Główna:**
  - karta „Następna lekcja”;
  - kafelki: liczba lekcji w tygodniu, prognoza tygodnia, aktywni uczniowie, zarobek i wpłaty w miesiącu, zadłużenie;
  - lekcje do potwierdzenia i najbliższe lekcje;
  - dzwonek z powiadomieniami.
- **Uczniowie:**
  - wyszukiwarka, sortowanie, filtr przedmiotów, archiwum;
  - profil ucznia: przyciski „Zadzwoń” i „SMS”, saldo, opis, stały plan, najbliższe lekcje i historia rozliczeń.
- **Grupy:** kilku uczniów na jednej lekcji. Cena jest od osoby, zaznaczasz obecność, a płacą tylko obecni.
- **Grafik:** tydzień z paskiem dni (liczba lekcji przy każdym dniu) i oś godzin. Dotknij pustej godziny, żeby dodać lekcję.
- **Potwierdzanie lekcji jednym dotknięciem:** „Odbyta”, „Odbyta + gotówka / przelew / BLIK”, „Odwołana”, „Odwołana z opłatą”.
- **Finanse:**
  - przeprowadzone lekcje w miesiącu (np. 19/65) z paskiem postępu;
  - kwota przepracowana i otrzymana;
  - zadłużenie i nadpłaty;
  - prognoza na 7 dni, 2 tygodnie, następny miesiąc i ze stałego planu;
  - wykres dynamiki dochodu;
  - obecność i odwołania, formy płatności (ile gotówką);
  - zestawienie uczniów, wpłaty i podsumowanie roku.
- **Ustawienia:** instalacja na telefonie, kopia zapasowa (JSON), eksport do Excela (CSV).

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
