#!/usr/bin/env python3
"""Scal tłumaczenia przepisanego „Kroku 0" (+ korekty rozjazdów) do i18n.js.

Wejście: /tmp/i18n-start-<lang>.json (13 kluczy od tłumaczy).
Dwa klucze poprawione po starcie tłumaczy (`ja.li3_html`, `tour.s2_p_html`) NIE są w tych
plikach — dociągane osobno, patrz LATE poniżej.

Bramki: komplet kluczy, zero prostych " (łamią i18n.js), parytet tagów <b> wobec pl.
Po scaleniu: node scripts/validate-i18n.mjs
"""
import json
import os
import re
import sys

PATH = "i18n.js"
SRC = "/tmp/keys-start.json"
LANGS = ["es", "it", "pt", "de", "nl", "sv", "ru", "uk", "fr"]


def bounds(s, lang, langs):
    st = s.index(f"\n{lang}: {{")
    i = langs.index(lang)
    en = s.index(f"\n{langs[i+1]}: {{") if i + 1 < len(langs) else s.rindex("\n};")
    return st, en


def main():
    expected = list(json.load(open(SRC, encoding="utf-8")).keys())
    s = open(PATH, encoding="utf-8").read()
    pl_block = s[bounds(s, "pl", re.findall(r"\n([a-z]{2}(?:-[A-Z]{2})?): \{", s))[0]:
                 bounds(s, "pl", re.findall(r"\n([a-z]{2}(?:-[A-Z]{2})?): \{", s))[1]]
    pl = {m.group(1): m.group(2) for m in re.finditer(r'"([a-zA-Z0-9_.]+)"\s*:\s*"((?:[^"\\]|\\.)*)"', pl_block)}

    ok, bad = [], []
    for lang in LANGS:
        p = f"/tmp/i18n-start-{lang}.json"
        if not os.path.exists(p):
            print(f"[{lang}] brak pliku — pomijam")
            continue
        try:
            data = json.load(open(p, encoding="utf-8"))
        except Exception as e:
            print(f"[{lang}] ODRZUCONY — zły JSON: {e}"); bad.append(lang); continue

        problems = [f"brak {k}" for k in expected if k not in data]
        for k, v in data.items():
            if not isinstance(v, str):
                problems.append(f"{k}: nie tekst"); continue
            if '"' in v:
                problems.append(f'{k}: proste "')
            if "\n" in v or "\t" in v:
                problems.append(f"{k}: nowa linia")
            if k in pl and pl[k].count("<b>") != v.count("<b>"):
                problems.append(f"{k}: <b> {pl[k].count('<b>')} vs {v.count('<b>')}")
        if problems:
            print(f"[{lang}] ODRZUCONY — {len(problems)}:")
            for x in problems[:5]:
                print("    ·", x)
            bad.append(lang); continue

        langs = re.findall(r"\n([a-z]{2}(?:-[A-Z]{2})?): \{", s)
        st, en = bounds(s, lang, langs)
        b = s[st:en]
        cnt = 0
        for k, v in data.items():
            pat = r'("' + re.escape(k) + r'"\s*:\s*")(?:[^"\\]|\\.)*(")'
            b, c = re.subn(pat, lambda m: m.group(1) + v + m.group(2), b, count=1)
            cnt += c
        s = s[:st] + b + s[en:]
        print(f"[{lang}] ✓ {cnt}")
        ok.append(lang)

    if ok:
        open(PATH, "w", encoding="utf-8").write(s)
    print(f"\nScalone: {', '.join(ok) if ok else '—'}")
    if bad:
        print(f"ODRZUCONE: {', '.join(bad)}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
