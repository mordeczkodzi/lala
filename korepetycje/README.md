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

## Jak uruchomić

1. Otwórz `index.html` w przeglądarce (Chrome, Safari, Firefox).
2. Na telefonie najlepiej wystawić plik pod stałym adresem, np. przez GitHub Pages, i dodać go do ekranu głównego („Dodaj do ekranu początkowego”). Wtedy działa jak zwykła aplikacja.

## Ważne: gdzie są dane

Dane są zapisywane **tylko w tej przeglądarce, na tym urządzeniu** (localStorage). Wyczyszczenie danych przeglądarki je usunie. Dlatego rób regularnie kopię: **Ustawienia → Pobierz kopię**, a plik trzymaj np. na Dysku Google. Tym samym plikiem przeniesiesz dane na inne urządzenie (**Wczytaj kopię**).
