# SPEC-003 — Walidator parzystości i18n + sprzątanie martwego kodu

**Status:** in-progress (walidator + sprzątanie martwych kluczy i18n — DONE; martwy CSS/JS — TODO)
**Priorytet:** P1 (prewencja — organizacyjna przyczyna SPEC-001/002; zapobiega nawrotowi)
**Utworzony:** 2026-07-03
**Origin:** audyty 2026-07-03 (proces + reużywalność) po hotfixie i18n

---

## Problem

`i18n.js` (178 KB, 8 bloków językowych) utrzymywany ręcznie + patchowany skryptami bez
walidacji. Skutek: dryf kluczy między językami (SPEC-002) i błędy składni (SPEC-001)
trafiły na produkcję niewykryte. Redesign (`9cf3c92`) zostawił też martwy CSS/JS/klucze.

## Cel

Uniemożliwić powtórkę: automat wyłapujący (a) błąd składni, (b) brak parzystości kluczy,
(c) klucz z HTML nieobecny w którymkolwiek języku — zanim trafi do repo.

## Zakres

### Walidator (pre-commit + Vercel build gate)
- `node --check i18n.js` — składnia.
- Zbierz `data-i18n`, `data-i18n-html`, `data-i18n-alt`, `data-i18n-aria` z `index.html`.
- Każdy klucz z HTML MUSI istnieć w każdym z 8 bloków.
- Wszystkie 8 bloków MUSZĄ mieć identyczny zestaw kluczy (źródło prawdy: `pl`).
- Exit ≠ 0 gdy którykolwiek warunek złamany.

### Sprzątanie martwego kodu (0 użyć — zweryfikowane audytem)
- Martwe klucze: `mock.r_*`, `watch.wface_set`, `graj.*`, `form.*`.
- Martwy CSS: `.tw-*`, `.wface`/`.wpair`/`.wzone`, `.phone*`, `.benefit`/`.bgrid`, `.steps3`, `.floaty`, `.glass`.
- Martwy JS: `watchAnim()` (steruje nieistniejącymi `#pmy`/`#poni`/`#smy`).

## Acceptance Criteria

- [x] Walidator `scripts/validate-i18n.mjs` — odrzuca `SyntaxError`, brak klucza z HTML, brak parzystości
- [x] Martwe klucze i18n usunięte: `mock.r_*` (5), `watch.wface_set` (+ duplikaty w es/it)
- [x] Walidator zielony: 8 języków × 242 klucze z HTML, parzystość 302/302
- [x] Render 8 języków bez regresji: `fallbackCount: 0` dla każdego (test DOM vs window.I18N)
- [ ] Martwy CSS usunięty: `.tw-*`, `.wface*`, `.phone*`, `.benefit`/`.bgrid`, `.steps3`, `.floaty`, `.glass`
- [ ] Martwy JS usunięty: `watchAnim()` (steruje nieistniejącymi `#pmy`/`#poni`/`#smy`)
- [ ] Martwe klucze `graj.*`, `form.*` usunięte (pozostałość starej sekcji „Jak grać")
- [ ] Walidator wpięty w pre-commit / Vercel build gate

## Nice-to-have (osobny spec jeśli warto)

- Migracja tłumaczeń do per-język JSON (`i18n/<lang>.json`) ładowanych na żądanie —
  koniec z edycją monolitu i skryptami patchującymi. Dla landingu opcjonalne.
