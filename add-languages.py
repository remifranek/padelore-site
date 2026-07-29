#!/usr/bin/env python3
"""Dodaj nowe bloki językowe (sv, fr, nl) do i18n.js — parytet z aplikacją (11 języków).

Tłumacze dostarczyli 185 kluczy UŻYWANYCH w HTML. Blok musi mieć komplet kluczy z `pl`
(walidator wymaga parzystości), więc brakujące — martwe pozostałości po wyciętych makietach —
kopiujemy z `en`. Nie tłumaczymy tego, czego strona nie renderuje.

Po uruchomieniu: node scripts/validate-i18n.mjs
"""
import json
import os
import re
import sys

I18N = "i18n.js"
NEW_LANGS = ["sv", "fr", "nl"]
TAGS = ("<b>", "</b>", "<span", "</span>", "<br>")


def main():
    s = open(I18N, encoding="utf-8").read()
    g_pl = block_dict(s, "pl")
    g_en = block_dict(s, "en")
    all_keys = list(g_pl.keys())

    added = []
    for lang in NEW_LANGS:
        path = f"/tmp/i18n-{lang}.json"
        if not os.path.exists(path):
            print(f"[{lang}] brak {path} — pomijam")
            continue
        if f"\n{lang}: {{" in s:
            print(f"[{lang}] blok już istnieje — pomijam")
            continue

        data = json.load(open(path, encoding="utf-8"))

        # bramka: cudzysłowy i markup
        problems = []
        for k, v in data.items():
            if not isinstance(v, str):
                problems.append(f"{k}: nie tekst")
                continue
            if "\n" in v or "\t" in v:
                problems.append(f"{k}: nowa linia/tab")
            if k in g_pl:
                for tag in TAGS:
                    if g_pl[k].count(tag) != v.count(tag):
                        problems.append(f"{k}: markup {tag} ({g_pl[k].count(tag)} vs {v.count(tag)})")
        if problems:
            print(f"[{lang}] ODRZUCONY — {len(problems)} problemów:")
            for p in problems[:6]:
                print(f"    · {p}")
            continue

        # komplet: brakujące (martwe klucze) z EN
        filled = 0
        block_lines = []
        for k in all_keys:
            v = data.get(k)
            if v is None:
                v = g_en.get(k, g_pl[k])
                filled += 1
            # wartość musi być bezpieczna dla stringa w podwójnych cudzysłowach
            v = v.replace('"', "”")
            block_lines.append(f'  "{k}": "{v}",')

        block = f"\n{lang}: {{\n" + "\n".join(block_lines) + "\n}\n"

        # Wstaw przed zamknięciem window.I18N. GOTCHA: ostatni blok kończy się `}` BEZ
        # przecinka — doklejenie kolejnego bez poprawki daje „Unexpected identifier".
        marker = "\n};"
        idx = s.rindex(marker)
        head = s[:idx].rstrip()
        if head.endswith("}"):
            head += ","
        s = head + "\n" + block + s[idx:]
        print(f"[{lang}] ✓ dodany — {len(data)} przetłumaczonych, {filled} skopiowanych z en (martwe klucze)")
        added.append(lang)

    if added:
        open(I18N, "w", encoding="utf-8").write(s)
    print(f"\nDodane: {', '.join(added) if added else '—'}")
    return 0


def block_dict(src, lang):
    """Wyciągnij słownik klucz→wartość dla bloku języka (naiwny, ale wystarcza: 1 klucz = 1 para)."""
    start = src.index(f"\n{lang}: {{")
    langs = re.findall(r"\n([a-z]{2}(?:-[A-Z]{2})?): \{", src)
    i = langs.index(lang)
    end = src.index(f"\n{langs[i+1]}: {{") if i + 1 < len(langs) else src.rindex("\n};")
    block = src[start:end]
    return {m.group(1): m.group(2)
            for m in re.finditer(r'"([a-zA-Z0-9_.]+)"\s*:\s*"((?:[^"\\]|\\.)*)"', block)}


if __name__ == "__main__":
    sys.exit(main())
