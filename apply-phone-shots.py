#!/usr/bin/env python3
"""Podmień zrzuty TELEFONU na wersje per język (rig PadelMatchProUITests).

Landing pokazywał zrzuty telefonu wyłącznie po polsku — na wszystkich 11 wersjach
językowych. Ten skrypt kopiuje kadry z rigu (resize do 640 px: ramka na stronie ma
284 px, więc to zapas na retinę; oryginały 1206×2622 dałyby ~51 MB) i podpina je pod
`data-i18n-src`, ten sam mechanizm co dla zegarka.

NIE OBJĘTE rigiem (zostają polskie — dług do osobnego taska):
  screens-19/10-matchcard.png  — karta meczu
  screens-19/08-standings.png  — tabela ligowa

Usage: python3 apply-phone-shots.py <katalog-z-kadrami>
Po uruchomieniu: node scripts/validate-i18n.mjs
"""
import os
import shutil
import subprocess
import sys

LANGS = ["pl", "en", "es", "it", "pt-PT", "de", "nl", "sv", "fr", "ru", "uk"]
WIDTH = 640
DEST = "assets/phone"

# stara ścieżka w index.html -> (nazwa kadru w rigu, nazwa docelowa)
MAP = {
    "assets/01-home.png": ("01-home", "home"),
    "assets/02-single-players.png": ("02-single-players", "players"),
    "assets/screens-19/03-wizard-format.png": ("03-wizard-format", "wizard"),
    "assets/screens-19/05-tournament.png": ("05-tournament", "tournament"),
    "assets/screens-19/06-stats.png": ("06-stats", "stats"),
    "assets/screens-19/09-activity.png": ("09-activity", "activity"),
}


def main():
    src_dir = sys.argv[1] if len(sys.argv) > 1 else None
    if not src_dir or not os.path.isdir(src_dir):
        sys.exit("Podaj katalog z kadrami rigu iOS")

    os.makedirs(DEST, exist_ok=True)
    copied = skipped = 0

    for old_path, (rig_name, dest_name) in MAP.items():
        for lang in LANGS:
            src = os.path.join(src_dir, f"{rig_name}-{lang}.png")
            tag = "pt" if lang == "pt-PT" else lang
            dst = os.path.join(DEST, f"{dest_name}-{tag}.png")
            if not os.path.exists(src):
                skipped += 1
                continue
            shutil.copy(src, dst)
            subprocess.run(["sips", "-Z", str(WIDTH), dst], capture_output=True)
            copied += 1

    print(f"skopiowane i przeskalowane: {copied}, brakujące kadry: {skipped}")

    # podmiana w index.html
    html = open("index.html", encoding="utf-8").read()
    changed = 0
    for old_path, (_, dest_name) in MAP.items():
        needle = f'src="{old_path}"'
        if needle not in html:
            print(f"  ⚠️  brak w index.html: {old_path}")
            continue
        repl = (f'src="{DEST}/{dest_name}-en.png" '
                f'data-i18n-src="{DEST}/{dest_name}-{{lang}}.png"')
        n = html.count(needle)
        html = html.replace(needle, repl)
        changed += n
    open("index.html", "w", encoding="utf-8").write(html)
    print(f"podmienione odwołania w index.html: {changed}")

    total = sum(os.path.getsize(os.path.join(DEST, f)) for f in os.listdir(DEST))
    print(f"rozmiar {DEST}: {total/1024/1024:.1f} MB")


if __name__ == "__main__":
    main()
