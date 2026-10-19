# Otulka – strona produktu (Shopify, motyw Helio)

Źródła strony produktu „Otulka – termofor do noszenia z pasem” zbudowanej na kopii motywu Helio
(`Otulka — DRAFT (strona termoforu)`, id `210102583626`) w sklepie `p20cwe-y1.myshopify.com`.

## Co jest w środku

| Plik | Rola |
| --- | --- |
| `sections/otulka-hero.liquid` | Galeria (`product.media`), wybór Kolor × Zestaw, dodatek „Sam pasek”, formularz koszyka, lepki pasek „Do koszyka” (działa też na stronie głównej z wybranym produktem) |
| `sections/otulka-banner.liquid` | Baner na górze strony głównej |
| `sections/otulka-split.liquid` | „Bez Otulki / Z Otulką” – przed i po |
| `sections/otulka-footer-info.liquid` | Godziny pracy i kontakt w stopce |
| `sections/otulka-marquee.liquid` | Przewijany pasek tekstu |
| `sections/otulka-cards.liquid` | Karty „Przynosimy ulgę” |
| `sections/otulka-rows.liquid` | Wiersze korzyści (zdjęcie + tekst + punkty) |
| `sections/otulka-tiles.liquid` | Kafelki „Pomaga wszędzie” i kroki „Jak to działa?” |
| `sections/otulka-compare.liquid` | Tabela porównawcza |
| `sections/otulka-reviews.liquid` | Opinie – ukryte w sklepie, dopóki nie wpiszesz prawdziwych |
| `sections/otulka-faq.liquid` | FAQ + pasek gwarancji |
| `sections/otulka-about.liquid` | O nas, formularz kontaktowy, końcowe wezwanie do zakupu |
| `snippets/otulka-cart-upsell.liquid` + `assets/otulka-cart.js` | „Klienci też kochali” (sam pasek) w szufladzie koszyka |
| `snippets/cart-drawer.liquid` | Szuflada koszyka motywu z wpiętym upsellem |
| `assets/otulka.css`, `assets/otulka-extra.css`, `assets/otulka.js` | Wspólne style i logika strony |
| `templates/product.otulka.json` | Szablon produktu (kolejność sekcji i treści) |
| `templates/page.otulka.json` | Szablon strony „O nas” |
| `templates/index.json` | Strona główna |
| `sections/footer-group.json` | Stopka (newsletter, godziny pracy, menu) |
| `templates/404.json`, `cart.json`, `password.json`, `list-collections.json` | Teksty motywu po polsku |
| `locales/en.default.json` | Polskie tłumaczenia motywu (domyślny język sklepu to wciąż angielski) |
| `config/settings_data.json` | Kolory i czcionki motywu (Fraunces + Jost, krem / brąz / pomarańcz) |
| `tools/build_templates.py` | Generuje szablony produktu, strony „O nas” i strony głównej z treściami po polsku |

## Wymagania po stronie produktu

- Opcja 1 = kolor, opcja 2 = zestaw o wartościach `Przytulny`, `Standard`, `Sam pasek`.
- Uchwyt produktu `otulka-termofor-z-pasem` (z niego korzysta upsell w koszyku).
- Szablon produktu: `otulka`.

Wszystkie teksty, zdjęcia (wybór zdjęcia albo numer zdjęcia produktu) i przyciski zmienisz w edytorze motywu.
