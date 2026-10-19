"""Generuje templates/product.otulka.json i templates/page.otulka.json (treści po polsku)."""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def blocks(items, btype):
    out, order = {}, []
    for i, settings in enumerate(items, 1):
        key = f"{btype}{i}"
        out[key] = {"type": btype, "settings": settings}
        order.append(key)
    return out, order


def section(stype, settings, items=None, btype=None):
    sec = {"type": stype, "settings": settings}
    if items:
        sec["blocks"], sec["block_order"] = blocks(items, btype)
    return sec


hero_blocks = {}
hero_order = []
for i, text in enumerate([
    "Ciepło dokładnie tam, gdzie boli – na brzuchu albo plecach",
    "Pod bluzą nikt jej nie zauważy",
    "Wolne ręce – pracujesz, chodzisz, podróżujesz",
    "Bez prądu i kabli – wystarczy gorąca woda",
], 1):
    hero_blocks[f"usp{i}"] = {"type": "usp", "settings": {"text": text}}
    hero_order.append(f"usp{i}")
for i, (title, content, use_desc) in enumerate([
    ("Opis produktu", "<p>Opis produktu.</p>", True),
    ("Co jest w zestawie?", "<ul><li><strong>Przytulny:</strong> termofor 1000 ml, regulowany pas i pluszowy pokrowiec</li><li><strong>Standard:</strong> termofor 1000 ml i regulowany pas</li><li><strong>Sam pasek:</strong> dodatkowy pas na zmianę</li></ul>", False),
    ("Regulowany rozmiar", "<p>Pas zapinasz i regulujesz, więc dopasujesz go do talii albo bioder. Nie wiesz, czy będzie pasował? Napisz do nas – podamy dokładne wymiary.</p>", False),
    ("Wysyłka i zwroty", "<p>Każdą paczkę wysyłamy z numerem śledzenia, który dostaniesz e-mailem. Masz 14 dni na zwrot bez podawania przyczyny.</p>", False),
    ("Bezpieczeństwo", "<p>Napełniaj gorącą, ale nie wrzącą wodą (maks. ok. 70°C) i zawsze mocno zakręcaj korek. Nie podgrzewaj termoforu w mikrofalówce. Otulka nie jest wyrobem medycznym – przy silnym lub nietypowym bólu skonsultuj się z lekarzem.</p>", False),
], 1):
    hero_blocks[f"acc{i}"] = {"type": "accordion", "settings": {"title": title, "content": content, "use_description": use_desc}}
    hero_order.append(f"acc{i}")

hero = {
    "type": "otulka-hero",
    "blocks": hero_blocks,
    "block_order": hero_order,
    "settings": {
        "promo_text": "🔥 JESIENNA WYPRZEDAŻ – OSZCZĘDZASZ DO [rabat]%",
        "sale_badge": "Wyprzedaż",
        "badge_text": "Bestseller",
        "display_title": "Otulka",
        "subtitle": "Termofor do noszenia z pasem",
        "bundle_label": "Zestaw",
        "bundle_a_value": "Przytulny",
        "bundle_a_desc": "Termofor 1000 ml + pas + pluszowy pokrowiec",
        "bundle_a_ribbon": "Bestseller",
        "bundle_b_value": "Standard",
        "bundle_b_desc": "Termofor 1000 ml + regulowany pas",
        "show_addon": True,
        "addon_value": "Sam pasek",
        "addon_title": "Dodaj drugi pasek",
        "addon_text": "Na zmianę albo w prezencie – w tym samym kolorze",
        "urgency_text": "Jesienna wyprzedaż trwa – oszczędzasz do [rabat]%",
        "cta_label": "Dodaj do koszyka",
        "sticky_label": "Do koszyka",
        "trust_1": "Bezpieczne płatności",
        "trust_2": "14 dni na zwrot",
        "trust_3": "Wysyłka z numerem śledzenia",
        "payment_fallback": "BLIK, Przelewy24, Visa, Mastercard, Apple Pay, Google Pay",
    },
}

marquee = section("otulka-marquee", {
    "items": "Ciepło tam, gdzie boli | Pod bluzą nikt jej nie zauważy | Wolne ręce | Bez prądu i kabli | Mięciutki plusz",
    "style": "accent",
    "speed": 32,
})

relief = section("otulka-cards", {
    "eyebrow": "Dlaczego ją pokochasz",
    "heading": "Przynosimy ulgę.",
    "text": "Otulka to termofor, który nosisz jak pas – ciepło trafia tam, gdzie go potrzebujesz, a Ty masz wolne ręce.",
    "background": "cream",
}, [
    {"media_index": 2, "title": "Szybko i naturalnie", "text": "Gorąca woda, zakręcony korek i gotowe. Bez kabli, baterii i ładowania."},
    {"media_index": 3, "title": "Miękka i wygodna", "text": "Plusz otula brzuch jak ciepły koc – przyjemnie od pierwszej minuty."},
    {"media_index": 4, "title": "Dopasowuje się do Ciebie", "text": "Regulowany pas: na brzuch albo na dolny odcinek pleców."},
    {"media_index": 5, "title": "Zawsze przy Tobie", "text": "W pracy, na uczelni, w podróży – ciepło idzie razem z Tobą."},
], "card")

story = section("otulka-rows", {
    "eyebrow": "Termofor nowej generacji",
    "heading": "Ciepło, które idzie z Tobą",
    "background": "white",
}, [
    {"media_index": 8, "eyebrow": "Dyskretna", "title": "Pod bluzą nikt jej nie zauważy",
     "text": "<p>Płaski, miękki pas przylega do ciała, więc spokojnie schowasz go pod bluzą, swetrem czy luźną koszulą. Nikt nie musi wiedzieć, że masz dziś trudny dzień.</p>",
     "points": "Płaski profil – nie odstaje\nNosisz w pracy, w szkole i w drodze\nCicha – bez kabli i ładowarek"},
    {"media_index": 10, "eyebrow": "Celne ciepło", "title": "Ciepło dokładnie tam, gdzie boli",
     "text": "<p>Termofor 1000 ml siedzi w pasie dokładnie na brzuchu albo na krzyżu. Ciepło pomaga rozluźnić spięte mięśnie i przetrwać skurcze – bez trzymania termoforu w rękach.</p>",
     "points": "Duży wkład 1000 ml – ciepło na dłużej\nNa brzuch albo na dolny odcinek pleców\nRegulowany pas trzyma się na miejscu"},
    {"media_index": 13, "eyebrow": "Zestaw Przytulny", "title": "Mięciutka jak ulubiony koc",
     "text": "<p>W zestawie Przytulnym termofor dostaje pluszowy pokrowiec. Jest miły dla skóry, oddziela ją od gorącego wkładu i dłużej trzyma ciepło.</p>",
     "points": "Pluszowy pokrowiec w zestawie\nMiły dla skóry, nie drapie\n5 kolorów do wyboru"},
], "row")

uses = section("otulka-tiles", {
    "style": "icons",
    "eyebrow": "Na co dzień",
    "heading": "Pomaga wszędzie",
    "text": "Nie tylko w trudne dni – Otulka przydaje się częściej, niż myślisz.",
    "background": "peach",
}, [
    {"icon": "🌸", "title": "Trudne kobiece dni", "text": "Ciepło na brzuch, gdy skurcze nie odpuszczają."},
    {"icon": "💼", "title": "Praca i nauka", "text": "Siedzisz przy biurku, a ciepło robi swoje."},
    {"icon": "🧘", "title": "Spięte plecy", "text": "Rozluźnia dolny odcinek pleców po długim dniu."},
    {"icon": "🚗", "title": "Podróż", "text": "W aucie, pociągu czy samolocie – bez gniazdka."},
    {"icon": "🛋️", "title": "Wieczór z serialem", "text": "Zamiast koca na kolanach – ciepło, które się nie zsuwa."},
    {"icon": "❄️", "title": "Zimne dni", "text": "Na spacer, mecz czy przystanek – ciepło pod kurtką."},
], "tile")

steps = section("otulka-tiles", {
    "style": "steps",
    "eyebrow": "3 proste kroki",
    "heading": "Jak to działa?",
    "cta_label": "Wybieram zestaw Przytulny",
    "cta_bundle": "Przytulny",
    "background": "white",
}, [
    {"icon": "1", "title": "Napełnij", "text": "Wlej gorącą (nie wrzącą) wodę, wypuść powietrze i mocno zakręć korek."},
    {"icon": "2", "title": "Włóż do pasa", "text": "Wsuń termofor do kieszeni pasa – w zestawie Przytulnym najpierw załóż pluszowy pokrowiec."},
    {"icon": "3", "title": "Zapnij i działaj", "text": "Dopasuj pas na brzuchu albo plecach i wracaj do swoich spraw."},
], "tile")

marquee2 = section("otulka-marquee", {
    "items": "Wypróbuj bez ryzyka | 14 dni na zwrot | Bezpieczne płatności | Wysyłka z numerem śledzenia",
    "style": "dark",
    "speed": 36,
})

compare = section("otulka-compare", {
    "eyebrow": "Porównanie",
    "heading": "Otulka kontra reszta",
    "text": "Zobacz, dlaczego zwykły termofor zostaje w szafie.",
    "col_us": "Otulka",
    "col_a": "Zwykły termofor",
    "col_b": "Poduszka elektryczna",
    "cta_label": "Chcę Otulkę",
    "background": "cream",
}, [
    {"feature": "Wolne ręce", "us": True, "a": False, "b": True},
    {"feature": "Możesz chodzić i pracować", "us": True, "a": False, "b": False},
    {"feature": "Dyskretna pod ubraniem", "us": True, "a": False, "b": False},
    {"feature": "Bez prądu i kabli", "us": True, "a": True, "b": False},
    {"feature": "Nie zsuwa się przy ruchu", "us": True, "a": False, "b": False},
    {"feature": "Pluszowy pokrowiec w zestawie", "us": True, "a": False, "b": False},
], "row")

reviews = section("otulka-reviews", {
    "enabled": False,
    "heading": "Opinie, które dostajemy",
    "background": "white",
}, [
    {"rating": 5, "title": "Tytuł opinii", "text": "Wklej tutaj prawdziwą opinię klientki.", "author": "Imię, miasto"},
    {"rating": 5, "title": "Tytuł opinii", "text": "Wklej tutaj prawdziwą opinię klientki.", "author": "Imię, miasto"},
    {"rating": 5, "title": "Tytuł opinii", "text": "Wklej tutaj prawdziwą opinię klientki.", "author": "Imię, miasto"},
], "review")

faq = section("otulka-faq", {
    "eyebrow": "Masz pytania?",
    "heading": "Często zadawane pytania",
    "background": "white",
    "show_guarantee": True,
    "g1_title": "14 dni na zwrot",
    "g1_text": "Nie pasuje? Odeślij bez podawania przyczyny.",
    "g2_title": "Bezpieczne płatności",
    "g2_text": "Szyfrowana kasa Shopify – nie widzimy danych Twojej karty.",
    "g3_title": "Jesteśmy dla Ciebie",
    "g3_text": "Masz pytanie? Napisz – odpowiadamy na każdą wiadomość.",
}, [
    {"question": "Czy pod ubraniem widać termofor?", "answer": "<p>Pas jest płaski i miękki, więc pod bluzą, swetrem czy luźniejszą koszulą zwykle nikt go nie zauważy. Pod bardzo obcisłymi ubraniami może być lekko widoczny.</p>"},
    {"question": "Czym różni się zestaw Standard od Przytulnego?", "answer": "<p><strong>Standard</strong> to termofor 1000 ml z regulowanym pasem. <strong>Przytulny</strong> ma dodatkowo pluszowy pokrowiec – jest miękki w dotyku, oddziela skórę od gorącego wkładu i dłużej trzyma ciepło.</p>"},
    {"question": "Jak długo trzyma ciepło?", "answer": "<p>To zależy od temperatury wody i otoczenia. Pas i pluszowy pokrowiec spowalniają stygnięcie, więc ciepło czujesz dłużej niż przy gołym termoforze. Gdy woda przestygnie, po prostu ją wymień.</p>"},
    {"question": "Jaką wodą napełniać termofor?", "answer": "<p>Gorącą, ale nie wrzącą (maks. ok. 70°C). Napełnij do ok. 2/3, wypuść powietrze i mocno zakręć korek. Nie podgrzewaj termoforu w mikrofalówce.</p>"},
    {"question": "Czy pomoże na bóle menstruacyjne?", "answer": "<p>Ciepło pomaga rozluźnić mięśnie i złagodzić skurcze – dlatego tak wiele kobiet sięga po termofor w trudne dni. Otulka nie jest wyrobem medycznym; przy silnym lub nietypowym bólu skonsultuj się z lekarzem.</p>"},
    {"question": "Czy pas będzie na mnie pasował?", "answer": "<p>Pas ma regulowane zapięcie, więc dopasujesz go do talii albo bioder. Jeśli masz wątpliwości, napisz do nas – podamy dokładne wymiary.</p>"},
    {"question": "Jak dbać o pas i pokrowiec?", "answer": "<p>Przed praniem wyjmij termofor. Pas i pokrowiec najlepiej prać ręcznie w letniej wodzie i suszyć na płasko.</p>"},
    {"question": "Ile trwa dostawa?", "answer": "<p>Szacowany czas dostawy zobaczysz przy wyborze metody wysyłki w kasie. Po nadaniu paczki dostaniesz e-mail z numerem śledzenia.</p>"},
    {"question": "Czy mogę zwrócić produkt?", "answer": "<p>Tak. Masz 14 dni na odstąpienie od umowy bez podawania przyczyny. Napisz do nas, a przeprowadzimy Cię przez zwrot krok po kroku.</p>"},
    {"question": "Jakie są metody płatności?", "answer": "<p>Płacisz w bezpiecznej, szyfrowanej kasie Shopify. Wszystkie dostępne metody płatności zobaczysz przy składaniu zamówienia.</p>"},
], "faq")

about_settings = {
    "background": "cream",
    "show_about": True,
    "about_media_index": 9,
    "about_eyebrow": "O nas",
    "about_heading": "Ciepło, które jest przy Tobie",
    "about_text": "<p>Otulka powstała z prostej potrzeby: ciepło w trudne dni powinno być przy Tobie – w pracy, na uczelni, w drodze – a nie tylko na kanapie pod kocem.</p><p>Dlatego zamknęliśmy klasyczny termofor w miękkim, regulowanym pasie. Bez kabli, bez ładowania, bez kombinowania. Wystarczy gorąca woda i kilka sekund.</p><p>Każde zamówienie pakujemy tak, żeby dotarło do Ciebie jak mały prezent – dla siebie albo dla kogoś, kto potrzebuje odrobiny ciepła.</p>",
    "about_sign": "Zespół Otulki",
    "show_contact": True,
    "contact_eyebrow": "Kontakt",
    "contact_heading": "Skontaktuj się z nami",
    "contact_text": "Masz pytanie o rozmiar, zamówienie albo zwrot? Napisz do nas – chętnie pomożemy.",
    "hours": "Odpisujemy w dni robocze",
    "contact_note": "Odpowiadamy na każdą wiadomość",
    "success_text": "Dziękujemy! Wiadomość dotarła – odezwiemy się najszybciej, jak to możliwe.",
    "show_final": True,
    "final_heading": "Zasługujesz na lepsze dni",
    "final_text": "Zrób sobie ciepło. Wybierz kolor i zestaw – Otulka zajmie się resztą.",
    "final_button": "Chcę swoją Otulkę",
}
about = section("otulka-about", about_settings)

product_template = {
    "sections": {
        "hero": hero,
        "marquee": marquee,
        "relief": relief,
        "story": story,
        "uses": uses,
        "steps": steps,
        "marquee2": marquee2,
        "compare": compare,
        "reviews": reviews,
        "faq": faq,
        "about": about,
    },
    "order": ["hero", "marquee", "relief", "story", "uses", "steps", "marquee2", "compare", "reviews", "faq", "about"],
}

page_about = dict(about_settings)
page_about.update({"about_media_index": 1, "cta_product": "otulka-termofor-z-pasem"})
page_template = {
    "sections": {"about": section("otulka-about", page_about)},
    "order": ["about"],
}

for name, data in [("product.otulka.json", product_template), ("page.otulka.json", page_template)]:
    with open(os.path.join(ROOT, "templates", name), "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print("wrote", name)
