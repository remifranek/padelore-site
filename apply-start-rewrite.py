#!/usr/bin/env python3
"""Przepisanie sekcji „Krok 0 · Wejście" + korekty rozjazdów z aktualną koncepcją aplikacji.

Zgłoszenie Remiego 2026-07-29: opis kazał „wybrać kartę Single Match lub Turniej", podczas gdy
od TASK-642/651 obie są ZWINIĘTE pod „Więcej sposobów gry", a hero Home jest ZAWSZE zegarkowy.
Sekcja ma teraz uczyć KRYTERIUM WYBORU drogi, nie opisywać nieistniejący układ ekranu:

  • zegarek      — gdy grasz z kimś nowym albo nie chcesz nikogo wpisywać (domyślne)
  • Single Match — gdy grasz ze znajomymi, których wpiszesz; wtedy działa wysyłka meczu i ranking
  • Turniej      — gdy jest was więcej i chcecie rotować pary

Przy okazji trzy rozjazdy wyłapane przy przeglądzie pozostałych sekcji:
  vs.add_1_html — „tap po GEMIE" → po PUNKCIE (błąd merytoryczny; tagowanie i wynik idą per punkt)
  watch.lead    — flow telefon→zegarek podany jako jedyny; teraz rama „gdy chcesz mecz z imionami"
  watch.s2_p    — „Nie otwierasz nic na zegarku" wprost przeczyło tezie watch-first

i18n.js edytowany wyłącznie skryptem (Edit-tool psuje cudzysłowy strukturalne).
Po uruchomieniu: node scripts/validate-i18n.mjs
"""
import re
import sys

PATH = "i18n.js"

REPLACE = {
    "pl": {
        "start.kicker": "Trzy drogi do meczu",
        "start.h2": "Najkrótsza zaczyna się na nadgarstku.",
        "start.lead": "Zero rejestracji, zero obowiązkowych profili. Nie musisz nikogo wpisywać — stuknij GRAJ na zegarku i licz. Imiona, wysyłka meczu i ranking wchodzą wtedy, gdy grasz ze znajomymi.",
        "start.num": "NA ZEGARKU · DOMYŚLNIE",
        "start.h3": "Graj z kimkolwiek, bez wpisywania",
        "start.p": "Ekran główny prowadzi prosto na zegarek: otwórz Padelore, stuknij GRAJ, tap = punkt. Nikogo nie dodajesz, niczego nie ustawiasz — i tak masz wynik, tętno i mecz w historii. To droga na open play i na granie z kimś, kogo widzisz pierwszy raz.",
        "start.li1_html": "<b>Z zegarka</b> — gdy grasz z kimś nowym albo nie chce Ci się wpisywać nazwisk.",
        "start.li2_html": "<b>Single Match</b> — gdy grasz ze znajomymi i wpiszesz imiona. Wtedy wyślesz im mecz, a wynik liczy się do rankingu.",
        "start.li3_html": "<b>Turniej</b> — Americano albo Mexicano, gdy jest was więcej i pary mają rotować.",
        "start.privacy": "Single Match i Turniej znajdziesz pod „Więcej sposobów gry”. Wszystko działa offline, ranking globalny jest opcjonalny.",
        # rozjazdy wyłapane przy przeglądzie
        "vs.add_1_html": "<b>Liczenie z Apple Watch</b> — tap po punkcie, wynik na żywo na kracie",
        "watch.lead": "Tak wygląda mecz, gdy chcesz mieć go z imionami: pary ustawiasz na telefonie, a liczysz i tak na zegarku. Kciukiem zaliczasz punkty, telefon pokazuje wynik na żywo całemu kortowi.",
        "watch.s2_p": "Wystartuj mecz na iPhonie — Apple Watch sam wykrywa, że mecz trwa, i pyta tylko o potwierdzenie. Grając bez wpisywania graczy zaczynasz wprost na zegarku, przyciskiem GRAJ.",
    },
    "en": {
        "start.kicker": "Three ways in",
        "start.h2": "The shortest one starts on your wrist.",
        "start.lead": "No sign-up, no mandatory profiles. You do not have to add anyone — tap PLAY on the watch and start counting. Names, sharing and ranking come in when you play with friends.",
        "start.num": "ON THE WATCH · DEFAULT",
        "start.h3": "Play with anyone, type nothing",
        "start.p": "The home screen sends you straight to the watch: open Padelore, tap PLAY, tap = point. Nobody to add, nothing to configure — you still get the score, your heart rate and the match in your history. This is the one for open play and for people you just met.",
        "start.li1_html": "<b>From the watch</b> — when you play someone new, or simply do not feel like typing names.",
        "start.li2_html": "<b>Single Match</b> — when you play friends and enter their names. Then you can send them the match, and it counts towards the ranking.",
        "start.li3_html": "<b>Tournament</b> — Americano or Mexicano, when there are more of you and partners should rotate.",
        "start.privacy": "Single Match and Tournament live under “More ways to play”. Everything works offline; the global ranking is opt-in.",
        "vs.add_1_html": "<b>Scoring from Apple Watch</b> — a tap per point, live score on the fence",
        "watch.lead": "This is what a match looks like when you want it with names: you set the pairs on the phone and still score on the watch. Thumb taps the points, the phone shows the live score to the whole court.",
        "watch.s2_p": "Start the match on the iPhone — Apple Watch notices a match is running and only asks you to confirm. When you play without entering players, you start on the watch itself, with the PLAY button.",
    },
}


def block_bounds(src, lang, langs):
    start = src.index(f"\n{lang}: {{")
    i = langs.index(lang)
    end = src.index(f"\n{langs[i+1]}: {{") if i + 1 < len(langs) else src.rindex("\n};")
    return start, end


def main():
    s = open(PATH, encoding="utf-8").read()
    langs = re.findall(r"\n([a-z]{2}(?:-[A-Z]{2})?): \{", s)
    total = 0
    for lang, pairs in REPLACE.items():
        start, end = block_bounds(s, lang, langs)
        block = s[start:end]
        for key, val in pairs.items():
            pattern = r'("' + re.escape(key) + r'"\s*:\s*")(?:[^"\\]|\\.)*(")'
            nb, n = re.subn(pattern, lambda m: m.group(1) + val + m.group(2), block, count=1)
            if n == 0:
                print(f"  ⚠️  [{lang}] brak klucza {key}")
            else:
                block, total = nb, total + 1
        s = s[:start] + block + s[end:]
    open(PATH, "w", encoding="utf-8").write(s)
    print(f"podmienione: {total} (pl + en)")
    print("Teraz: tłumaczenia dla es/it/de/ru/uk/pt/sv/fr/nl + node scripts/validate-i18n.mjs")


if __name__ == "__main__":
    sys.exit(main())
