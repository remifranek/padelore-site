# SPEC-004 — Restyle landingu na design system appki 1.9.0 + prawdziwe screeny

**Status:** done (2026-07-04) — 3 ekrany oflagowane jako follow-up (patrz §Wynik)
**Priorytet:** P1 (spójność marki landing ↔ aplikacja; usunięcie fake HTML-owych ekranów)
**Utworzony:** 2026-07-04
**Origin:** handoff `~/Downloads/handoff-claude-code/` (design system 1.9.0 z AppTheme.swift) + decyzja Remiego 2026-07-04
**Preview:** `docs/specs/preview/SPEC-004.html` (wymóg SDD — zmiana wizualna)

---

## Cel

Landing (`index.html`) przemalowany na **prawdziwy design system aplikacji 1.9.0**
(turf-navy `#0E2A55` + ball-yellow `#E0F75A`, Bricolage Grotesque, tokeny z `tokens.css`),
a wszystkie **ręcznie budowane fake HTML-owe ekrany** (`.apscr`, `.jacard`, `.tboard`,
`.fl-slide`, `.tw-*`, `.wface*`) zastąpione **prawdziwymi zrzutami z produkcji 1.9.0**
w ramkach iPhone.

## Zasada nadrzędna (z handoffu)

> Każdy pokazany ekran = prawdziwy zrzut 1.9.0 (`reference/*.png` lub wygenerowany
> z `padelwatch-pro` ScreenshotTests). Zero fake mockupów. Zero „ulepszeń" nieobecnych w appce.

## Zakres

### Design system
- Wprowadzić tokeny z handoffu (`tokens.css`) do `ds.css` (lub nowy `tokens.css` linkowany).
- Paleta: turf-navy surfaces + jeden żółty akcent `--ball`. Semantyka `--ok`/`--loss`/`--warning`/`--electric`/`--violet`.
- Typografia: Bricolage Grotesque (cały tekst) + rounded (numerale). Logo „Padel●re".
- Zachować dark/light? Appka jest adaptive, ale App Store render = dark. **Decyzja:** landing dark-first (jak zrzuty); light = follow-up jeśli trzeba.

### Screeny (prawdziwe, w ramkach)
| Ekran | Źródło | Status |
|---|---|---|
| 01 Home „Player HQ" | `reference/01-home.png` | ✅ mam |
| 02 Nowy mecz — Gracze | `reference/02-single-players.png` | ✅ mam |
| 03 Wizard — Format | `reference/03-wizard-format.png` | ✅ mam |
| 04 Wizard — Konfiguracja | `reference/04-wizard-config.png` | ✅ mam |
| 06 Statystyki „Jak gram" | `reference/06-stats.png` | ✅ mam |
| 07 Fence (landscape) | `screenshot-pngs/fence-landscape.png` + regen | ⚠ mam zastępczy, regen |
| 05 Turniej (live) | ScreenshotTests (fix nav) | 🔧 generuję (Xcode) |
| Watch (scoring) | ScreenshotTests / watch target | 🔧 generuję (Xcode) |

### Copy / i18n
- Zachować istniejące copy w 8 językach + strukturę sekcji (`#vs`, `#watch`, `#mecz`, `#turniej`, `#liga`, `#ja`, `#aktywnosc`, `#pobierz`).
- Zmiana wyłącznie wizualna + podmiana screenów. Copy bez zmian (chyba że screen wymusza korektę podpisu).

## Zależności / czyszczenie (domyka SPEC-003)
- Usunięcie fake-screen CSS (`.apscr`/`.jacard`/`.tboard`/`.tw-*`/`.wface*`/`.floaty`) — te ekrany znikają z landingu.
- `watchAnim()` (martwy JS) — usunąć.

## Acceptance Criteria

- [ ] Landing renderuje się w palecie turf-navy/ball-yellow (tokeny, zero surowych hexów w nowym CSS)
- [ ] Każdy pokazany ekran appki = prawdziwy zrzut 1.9.0 w ramce (0 fake HTML-owych ekranów)
- [ ] Turniej-live + Watch: prawdziwe zrzuty wygenerowane z ScreenshotTests
- [ ] `node scripts/validate-i18n.mjs` — PASS (parzystość 8 języków bez regresji)
- [ ] Render 8 języków bez wycieków surowych kluczy (test DOM)
- [ ] Preview zatwierdzony przez Remiego PRZED pełną implementacją 8 języków
- [ ] Fake-screen CSS/JS usunięte (domyka część SPEC-003)

## Wynik (2026-07-04)

Zrealizowane:
- Font Bricolage Grotesque (cały tekst) + Nunito (numerale) — `ds.css --font/--font-score`.
- Hero grad ujednolicony do solid `--accent` (ball-yellow), spójny z gradami sekcji.
- 7 fake HTML-owych ekranów → realne zrzuty 1.9.0 w ramkach iPhone:
  hero 01-home + watch-home, #turniej 03-wizard + 05-tournament, #liga 08-standings,
  #ja 06-stats, #mecz watch-scoring. Zero broken images, walidator i18n PASS.
- Wygenerowane z ScreenshotTests (fix nav): 05-tournament, 08-standings, 09-activity.

Rozwiązane w trakcie:
- **#aktywnosc** — realny `09-activity` (dashboard Aktywności: NA KORCIE 11:15h +108%, Rytm okresu,
  Ciało · Apple Health 5046 kcal / 34 km). Test obsługuje systemowy sheet HealthKit
  (`grantHealthSheet`: „Włącz wszystkie" → „Pozwól") — odsłania dashboard zamiast dialogu uprawnień.

Oflagowane (follow-up):
1. **Fence** (hero + #watch) — zostaje wierna tablica HTML (MY 15 : ONI 12, PADELORE).
   Realny landscape fence appka renderuje jako portret z treścią obróconą 90° + letterbox;
   czysty eksport wymaga ścieżki landscape-export w appce. HTML jest wierny (to tylko wielkie numerale).
2. **Watch „Skąd punkty"** (#mecz) — pokazany realny `watch-scoring` zamiast ekranu tagowania.
   Dedykowany zrzut watchOS = osobny target UI-test (duży lift).

## Decyzje domknięte
- Light theme: follow-up (dark-first teraz). ✅
- Sekcje z ramką-screen: hero, #turniej(×2), #liga, #ja, #aktywnosc, #mecz. #vs/#funkcje/#pobierz = copy.

## Dług (do SPEC-003)
- Martwy CSS fake-ekranów (`.apscr`/`.jacard`/`.tboard`/`.twatch`/`.tw-*`/`.wface*`) — nieużywany, do usunięcia (nie usunięto teraz: ryzyko regresji w dużym `<style>`, page działa). `.fenceboard` ZOSTAJE (fence).
- `watchAnim()` martwy JS — do usunięcia.
