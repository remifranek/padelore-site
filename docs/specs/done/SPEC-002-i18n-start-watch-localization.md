# SPEC-002 — Lokalizacja: relokacja start.* + uzupełnienie watch.s4_hint / watch.s3_alt

**Status:** done
**Priorytet:** P1 (5 języków pokazywało fallback zamiast tłumaczeń sekcji „start")
**Utworzony:** 2026-07-03
**Typ:** content i18n, 1 plik (`i18n.js`) → bez preview/Rekomendacja (brak zmiany layoutu)
**Origin:** audyt lokalizacji po SPEC-001 — pełna macierz luk kluczy w 8 językach
**Zależność:** wymaga SPEC-001 (plik musi się parsować, żeby audyt kluczy był możliwy)

---

## Problem

Po naprawie składni (SPEC-001) audyt parzystości wykrył:
1. **`start.*` (10 kluczy) błędnie wrzucone** — cały 8-językowy zrzut sekcji „start"
   wylądował w JEDNYM miejscu wewnątrz bloku `es` (dawne linie 526–613). Skutek:
   - `es.start.*` = ostatni duplikat = **portugalski** („Do zero ao jogo") zamiast hiszpańskiego;
   - `it/de/ru/uk/pt` nie miały `start.*` wcale → fallback na PL/EN.
2. **`watch.s4_hint`** obecny tylko w pl/en → brak w es/it/de/ru/uk/pt.
3. **`watch.s3_alt`** (img alt) — brak w de/ru/uk/pt; w es wmieszane polskie „tętno", w it angielskie „heart rate".

## Root cause

Skrypt `add-i18n-keys.py` wstawił blok tłumaczeń w jedno miejsce zamiast rozłożyć go
per blok językowy. Poprawne tłumaczenia `start.*` dla wszystkich 8 języków **już
istniały** — tylko w złej lokalizacji.

## Fix

Relokacja (nie tłumaczenie od zera) — skrypt operujący na granicach bloków językowych:
- usunięto błędny 8-językowy zrzut z bloku `es`;
- wstawiono poprawne `start.*` do es/it/de/ru/uk/pt (przed `watch.kicker` każdego bloku);
- dopisano `watch.s4_hint` (nowe tłumaczenie, spójne z terminologią `watch.s4_p`:
  valla/rete/Zaun/на сетке/на сітці/na rede) do 6 języków;
- dopisano/naprawiono `watch.s3_alt` w es/it/de/ru/uk/pt.

Zmiana: `i18n.js`, łącznie ze SPEC-001: 148 ins / 160 del.

## Acceptance Criteria

- [x] Wszystkie 8 języków mają komplet 234 kluczy wymaganych przez `index.html` (0 braków)
- [x] Klucze renderowane: parzystość 303/303 dla en, es, it, de, ru, uk, pt (pl 307 — patrz niżej)
- [x] `es.start.kicker` = „De cero a jugar" (hiszpański, nie portugalski)
- [x] `pt.start.kicker` = „Do zero ao jogo" (portugalski we właściwym bloku)
- [x] Render lokalny: sekcja `#start` po DE pokazuje niemiecki („Öffnen, wählen, spielen.")
- [x] `node --check i18n.js` — PASS

## Znane / świadomie pominięte

- **Martwe klucze** (0 użyć w `index.html`): `mock.r_done/now/plan/live/saved` (tylko pl),
  `watch.wface_set` (brak w pl). Powód rozjazdu pl 307 vs 303. Kandydaci do usunięcia —
  patrz follow-up SPEC-003.

## Follow-up (nowe spece do ready/)

- **SPEC-003** — walidator parzystości i18n (pre-commit/CI): zbierz `data-i18n*` z HTML,
  wymuś identyczny zestaw kluczy w 8 blokach; usuń martwy kod po redesignie
  (`.tw-*`, `.wface`, `.phone`, `.floaty`, `watchAnim`, martwe klucze `graj.*`/`form.*`).
  Źródło: audyt reużywalności 2026-07-03.
