#!/usr/bin/env python3
"""Aktualizacja copy landingu do wersji aplikacji 1.13.2 (PL + EN).

Zakres (zaakceptowany 2026-07-28, makieta: padelwatch-pro/wiki/ux/landing-1132-copy.html):
  1. hero — claim z App Store 1.13.2 + kategoria multi-sport w eyebrow
  2. NOWA sekcja `sport.*` — pięć sportów z prawdziwymi zasadami
  3. watch-first — korekta 3 zdań stawiających telefon na równi z zegarkiem
  4. NOWA sekcja `share.*` — wyślij mecz (pętla wzrostu)
  5. `akt.lead_html` — cross-sport + koniec z „drugą zakładką" (nawigacja ma 4)
  6. `meta.desc` — dotąd NIE ISTNIAŁ, polski opis z HTML szedł na wszystkie języki

UWAGA: i18n.js edytujemy wyłącznie skryptem. Edit-tool zamienia cudzysłowy strukturalne
JSON-a na typograficzne i łamie parsowanie pliku.

Cudzysłowy w wartościach: pl „…”, en “…”. Nigdy proste " — łamią string.
Walidacja po uruchomieniu: node scripts/validate-i18n.mjs
"""
import re
import sys

PATH = "i18n.js"

# ── 1. Podmiany istniejących kluczy ────────────────────────────────────────────
REPLACE = {
    "pl": {
        "meta.title": "Padelore — licznik meczu na Apple Watch",
        "hero.eyebrow": "Apple Watch · padel · pickleball · tenis · squash · badminton",
        "hero.title_a": "Kort rezerwujesz gdzie indziej.",
        "hero.title_b": "Tu liczysz mecz.",
        "hero.lead": "Punkty stukasz w zegarek — między serwisami, spoconym palcem. Telefon stoi oparty o kratę i pokazuje wynik całemu kortowi. Po ostatniej piłce dostajesz kartę meczu: czyje winnery, gdzie błędy, ile Cię to kosztowało.",
        "start.lead": "Gotowe w 15 sekund. Zero rejestracji, zero obowiązkowych profili. Na telefonie dodajesz graczy i ustawiasz zasady — liczysz na zegarku.",
        "start.li3_html": "<b>Zegarek</b> — stukasz punkty na nadgarstku, telefon zostaje na kracie.",
        "tour.s2_li2": "Wynik leci z zegarka na żywo — albo wpisujesz go na telefonie.",
        "akt.lead_html": "Zakładka „Aktywność” czyta Apple Health: obciążenie tydzień po tygodniu, tętno w strefach, regenerację. Grasz w kilka sportów? Zobaczysz podział czasu i to, który kosztuje Cię najwięcej na minutę. Ciało masz jedno.",
        "footer.copy": "© 2026 Padelore · mecz, który liczy się sam",
    },
    "en": {
        "meta.title": "Padelore — match scorekeeper on Apple Watch",
        "hero.eyebrow": "Apple Watch · pickleball · padel · tennis · squash · badminton",
        "hero.title_a": "Book the court somewhere else.",
        "hero.title_b": "Here you count the match.",
        "hero.lead": "You tap points on your watch — between serves, with a sweaty finger. Your phone leans against the fence and shows the score to the whole court. After the last rally you get a match card: whose winners, where the errors fell, what it cost you.",
        "start.lead": "Ready in 15 seconds. No sign-up, no mandatory profiles. Add players and set the rules on your phone — then score on the watch.",
        "start.li3_html": "<b>Watch</b> — you tap points on your wrist, the phone stays on the fence.",
        "tour.s2_li2": "Scores arrive live from the watch — or you type them on the phone.",
        "akt.lead_html": "The “Activity” tab reads Apple Health: weekly load, heart-rate zones, recovery. Play more than one sport? You will see how your time splits and which one costs you most per minute. You only get one body.",
        "footer.copy": "© 2026 Padelore · the match counts itself",
    },
}

# ── 2. Nowe klucze (wstawiane na początku bloku języka) ────────────────────────
NEW = {
    "pl": [
        ("meta.desc", "Padel, pickleball, tenis, squash i badminton na Apple Watch. Stukasz punkty na zegarku, telefon pokazuje wynik na kracie. Po meczu karta z winnerami, błędami i tętnem."),
        ("nav.sports", "Sporty"),
        ("nav.share", "Wyślij mecz"),
        ("sport.kicker", "Pięć sportów"),
        ("sport.h2_html", "Jeden licznik. <span style='color:var(--accent)'>Pięć kompletów zasad.</span>"),
        ("sport.lead", "Nie jedna punktacja przemalowana pięć razy. Każdy sport liczy się po swojemu i ma swój kort na tablicy."),
        ("sport.padel_h", "Padel"),
        ("sport.padel_p", "Punkty albo sety, złoty punkt, limit przewag. Americano i Mexicano dla ekipy."),
        ("sport.pickle_h", "Pickleball"),
        ("sport.pickle_p", "Side-out od „0-0-2” albo rally. Do 11, przewagą dwóch."),
        ("sport.badm_h", "Badminton"),
        ("sport.badm_p", "Do 21, przewagą dwóch, cap 30 wg BWF. Stronę serwisu liczy sama."),
        ("sport.squash_h", "Squash"),
        ("sport.squash_p", "Do 11 bez capu, do trzech wygranych setów. Kort z tinem."),
        ("sport.tennis_h", "Tenis"),
        ("sport.tennis_p", "Gemy, sety, tie-break. Domyślnie singiel."),
        ("sport.note", "Sport wybierasz na zegarku — bez sięgania po telefon."),
        ("share.kicker", "Po meczu"),
        ("share.h2_html", "Wyślij mecz. <span style='color:var(--accent)'>Zadziała bez apki.</span>"),
        ("share.lead", "Po ostatniej piłce wysyłasz link. Znajomy otwiera i widzi mecz ze swojej strony — swoje winnery, swoje błędy, przebieg punkt po punkcie."),
        ("share.li1_html", "<b>Trafia do jego historii</b> — to nie jest podgląd na jeden raz."),
        ("share.li2_html", "<b>Sam wskazuje, którym był graczem</b> — apka podpowiada, jeśli go rozpozna."),
        ("share.li3_html", "<b>Do rankingu liczy tylko autorowi</b> — jeden mecz nie wpada do tabeli dwa razy."),
        ("share.note", "Nie ma Padelore? Link otworzy stronę z wynikiem i podpowie, skąd wziąć apkę."),
    ],
    "en": [
        ("meta.desc", "Pickleball, padel, tennis, squash and badminton on Apple Watch. Tap points on your wrist, let the phone show the score on the fence. After the match: winners, errors and heart rate."),
        ("nav.sports", "Sports"),
        ("nav.share", "Send a match"),
        ("sport.kicker", "Five sports"),
        ("sport.h2_html", "One scorekeeper. <span style='color:var(--accent)'>Five sets of rules.</span>"),
        ("sport.lead", "Not one scoring system repainted five times. Every sport counts its own way and gets its own court on the board."),
        ("sport.padel_h", "Padel"),
        ("sport.padel_p", "Points or sets, golden point, advantage limit. Americano and Mexicano for the group."),
        ("sport.pickle_h", "Pickleball"),
        ("sport.pickle_p", "Side-out from “0-0-2” or rally scoring. Games to 11, win by 2."),
        ("sport.badm_h", "Badminton"),
        ("sport.badm_p", "To 21, win by 2, capped at 30 per BWF. Serving side tracked for you."),
        ("sport.squash_h", "Squash"),
        ("sport.squash_p", "To 11 with no cap, best of five. Court with the tin."),
        ("sport.tennis_h", "Tennis"),
        ("sport.tennis_p", "Games, sets, tie-break. Singles by default."),
        ("sport.note", "You pick the sport on the watch — no need to reach for the phone."),
        ("share.kicker", "After the match"),
        ("share.h2_html", "Send the match. <span style='color:var(--accent)'>Works without the app.</span>"),
        ("share.lead", "After the last rally you send a link. Your partner opens it and sees the match from their own side — their winners, their errors, the rally-by-rally story."),
        ("share.li1_html", "<b>It lands in their history</b> — not a one-off preview."),
        ("share.li2_html", "<b>They pick which player they were</b> — the app suggests it if it recognises them."),
        ("share.li3_html", "<b>Only the author gets the ranking points</b> — one match never counts twice."),
        ("share.note", "No Padelore? The link still opens a page with the score and points to the App Store."),
    ],
}


def block_bounds(src, lang, langs):
    """Zwróć (start, end) bloku języka — od `lang: {` do początku kolejnego bloku.

    Bloki języków zaczynają się NA POCZĄTKU LINII (bez wcięcia), klucze mają 2 spacje.
    """
    start = src.index(f"\n{lang}: {{")
    idx = langs.index(lang)
    if idx + 1 < len(langs):
        end = src.index(f"\n{langs[idx + 1]}: {{")
    else:
        end = len(src)
    return start, end


def main():
    src = open(PATH, encoding="utf-8").read()
    langs = re.findall(r"\n([a-z]{2}(?:-[A-Z]{2})?): \{", src)
    print(f"Języki w pliku: {langs}")

    changed = added = 0

    for lang in ("pl", "en"):
        start, end = block_bounds(src, lang, langs)
        block = src[start:end]

        # (a) podmiany
        for key, val in REPLACE[lang].items():
            pattern = r'("' + re.escape(key) + r'"\s*:\s*")(?:[^"\\]|\\.)*(")'
            new_block, n = re.subn(pattern, lambda m: m.group(1) + val + m.group(2), block, count=1)
            if n == 0:
                print(f"  ⚠️  [{lang}] nie znaleziono klucza {key} — POMINIĘTY")
            else:
                block = new_block
                changed += 1

        # (b) nowe klucze — wstaw tuż po otwarciu bloku (kolejność kluczy nieistotna)
        opener = f"\n{lang}: {{\n"
        lines = []
        for key, val in NEW[lang]:
            if f'"{key}"' in block:
                print(f"  ⏭  [{lang}] {key} już istnieje — pomijam")
                continue
            lines.append(f'  "{key}": "{val}",')
            added += 1
        if lines:
            block = block.replace(opener, opener + "\n".join(lines) + "\n", 1)

        src = src[:start] + block + src[end:]

    open(PATH, "w", encoding="utf-8").write(src)
    print(f"\nPodmienione: {changed} · dodane: {added}")
    print("Teraz: node scripts/validate-i18n.mjs")


if __name__ == "__main__":
    sys.exit(main())
