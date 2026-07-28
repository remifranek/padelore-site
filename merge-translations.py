#!/usr/bin/env python3
"""Scal tłumaczenia z /tmp/i18n-<lang>.json do i18n.js.

Wzorzec z audytu i18n aplikacji: każdy tłumacz pisze WŁASNY plik (zero konfliktów na
wspólnym i18n.js), tu następuje centralny merge z bramkami.

BRAMKI (odrzucają wadliwe tłumaczenie ZANIM trafi do pliku):
  1. komplet kluczy — brak choćby jednego = odrzuć cały język
  2. zero prostych " w wartości — łamią string JSON-a w i18n.js
  3. parytet markupu — liczba <b>, </b>, <span, </span> musi się zgadzać z PL
  4. zakaz \\n i \\t w wartościach

Użycie: python3 merge-translations.py [lang ...]      (domyślnie: wszystkie znalezione)
Po scaleniu ZAWSZE: node scripts/validate-i18n.mjs
"""
import json
import os
import re
import sys

I18N = "i18n.js"
SRC = "/tmp/keys-to-translate.json"
TAGS = ("<b>", "</b>", "<span", "</span>")


def block_bounds(src, lang, langs):
    start = src.index(f"\n{lang}: {{")
    i = langs.index(lang)
    end = src.index(f"\n{langs[i + 1]}: {{") if i + 1 < len(langs) else len(src)
    return start, end


def check(lang, data, expected_keys, pl):
    """Zwróć listę problemów. Pusta = tłumaczenie wpuszczone."""
    problems = []

    missing = [k for k in expected_keys if k not in data]
    if missing:
        problems.append(f"brak {len(missing)} kluczy: {', '.join(missing[:6])}")

    for k, v in data.items():
        if not isinstance(v, str):
            problems.append(f"{k}: wartość nie jest tekstem")
            continue
        if '"' in v:
            problems.append(f'{k}: proste \" w wartości (złamie i18n.js)')
        if "\n" in v or "\t" in v:
            problems.append(f"{k}: znak nowej linii / tabulacja")
        if k in pl:
            for tag in TAGS:
                if pl[k].count(tag) != v.count(tag):
                    problems.append(
                        f"{k}: markup {tag} — PL ma {pl[k].count(tag)}, tłumaczenie {v.count(tag)}")
    return problems


def main():
    src_keys = json.load(open(SRC, encoding="utf-8"))
    expected = list(src_keys.keys())
    pl = {k: v["pl"] for k, v in src_keys.items()}

    wanted = sys.argv[1:] or [
        f[len("i18n-"):-len(".json")]
        for f in sorted(os.listdir("/tmp"))
        if f.startswith("i18n-") and f.endswith(".json")
    ]

    s = open(I18N, encoding="utf-8").read()
    langs = re.findall(r"\n([a-z]{2}(?:-[A-Z]{2})?): \{", s)

    merged, rejected = [], []

    for lang in wanted:
        path = f"/tmp/i18n-{lang}.json"
        if not os.path.exists(path):
            print(f"[{lang}] BRAK PLIKU {path} — pomijam")
            continue
        if lang not in langs:
            print(f"[{lang}] brak bloku w i18n.js — pomijam (nowe języki dodaj osobno)")
            continue

        try:
            data = json.load(open(path, encoding="utf-8"))
        except Exception as e:
            print(f"[{lang}] ODRZUCONY — plik nie jest poprawnym JSON-em: {e}")
            rejected.append(lang)
            continue

        problems = check(lang, data, expected, pl)
        if problems:
            print(f"[{lang}] ODRZUCONY — {len(problems)} problemów:")
            for p in problems[:8]:
                print(f"    · {p}")
            rejected.append(lang)
            continue

        start, end = block_bounds(s, lang, langs)
        block = s[start:end]
        upd = add = 0

        for key, val in data.items():
            pattern = r'("' + re.escape(key) + r'"\s*:\s*")(?:[^"\\]|\\.)*(")'
            nb, n = re.subn(pattern, lambda m: m.group(1) + val + m.group(2), block, count=1)
            if n:
                block, upd = nb, upd + 1
            else:
                opener = f"\n{lang}: {{\n"
                block = block.replace(opener, opener + f'  "{key}": "{val}",\n', 1)
                add += 1

        s = s[:start] + block + s[end:]
        langs = re.findall(r"\n([a-z]{2}(?:-[A-Z]{2})?): \{", s)
        print(f"[{lang}] ✓ podmienione {upd}, dodane {add}")
        merged.append(lang)

    if merged:
        open(I18N, "w", encoding="utf-8").write(s)

    print(f"\nScalone: {', '.join(merged) if merged else '—'}")
    if rejected:
        print(f"ODRZUCONE: {', '.join(rejected)} — popraw i uruchom ponownie")
    print("Teraz: node scripts/validate-i18n.mjs")
    return 1 if rejected else 0


if __name__ == "__main__":
    sys.exit(main())
