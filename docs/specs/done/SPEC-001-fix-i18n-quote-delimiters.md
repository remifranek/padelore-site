# SPEC-001 — Hotfix: błędne cudzysłowy-ograniczniki w i18n.js

**Status:** done
**Priorytet:** P0 (produkcja: cała treść poniżej hero nie renderowała się w 8 językach)
**Utworzony:** 2026-07-03
**Typ:** hotfix (`fix:`), 1 plik → hotfix lane, bez preview/Rekomendacja
**Origin:** commit `9cf3c92` („comprehensive storytelling redesign", 2026-07-03 20:43) — audyt renderowania wykrył pustą stronę poniżej hero na `padelore.app`

---

## Problem

`padelore.app` renderował tylko sekcję hero. Wszystkie 8 sekcji poniżej (vs, start,
watch, mecz, funkcje, turniej, liga, ja, aktywnosc, pobierz) — pusto. Na produkcji
i lokalnie, od 20:43.

Nie wykrywalne przez `git`, WebFetch ani statyczny podgląd HTML — błąd tylko w runtime
JS. WebFetch pokazywał statyczny fallback z HTML, więc „wyglądało OK".

## Root cause

`i18n.js` nie parsował się (`SyntaxError`). Skutek: `window.I18N` = undefined →
`setLang()` rzucał `TypeError` PRZED rejestracją `IntersectionObserver` (index.html
~linia 1119) → elementy `.reveal{opacity:0}` nigdy nie dostawały klasy `.in` → cała
treść niewidoczna.

Dwie klasy błędów wprowadzone przez skrypty `add-i18n-keys.py` / `fix-tabs-i18n.py`:
- **A** — 81 linii: ograniczniki JS jako krzywe cudzysłowy `“ ”` (U+201C/U+201D) zamiast `"`.
- **B** — kilkanaście linii EN/DE: nieescapowane proste `"` wewnątrz stringów (emfaza: `"Single match"`, `"From watch"`).

Dodatkowa trudność: znak `”` (U+201D) przeciążony — raz zepsuty ogranicznik, raz legalny
cudzysłów w treści (`„Gracze”` po PL/DE/UK).

## Fix

Fixer zakotwiczony na strukturze klucza (`"klucz":"wartość"`), traktujący `" “ ”` jako
znaki-cudzysłowy i odtwarzający ograniczniki z gramatyki obiektu:
- ograniczniki → proste `"`;
- wewnętrzne proste `"` → `\"` (escape, identyczny wygląd);
- typograficzne `„ " « »` w treści — nietknięte.

Zmiana: `i18n.js`, 81 ins / 81 del (symetryczna, tylko cudzysłowy, zero zmian treści).

## Acceptance Criteria

- [x] `node --check i18n.js` — PASS (zero błędów składni)
- [x] `window.I18N` ładuje się z 8 językami (pl, en, es, it, de, ru, uk, pt)
- [x] Konsola przeglądarki — zero `SyntaxError` / `TypeError` przy starcie
- [x] Render lokalny (localhost:3006): sekcje `#vs`, `#watch`, `#ja` pokazują treść (EN + PL)
- [x] Wysokość strony po naprawie 11380px (było: pusto poniżej hero)
- [x] Treść wartości nienaruszona (PL `„Pojedynczy mecz”`, RU `„как ты играешь”`, UK `«Де ти»`)

## Bramki jakości (dostosowane do statycznego repo)

`tsc`/`npm build`/`vitest` nie mają zastosowania (brak `package.json`, brak buildu).
Odpowiedniki: `node --check i18n.js` PASS + user test renderowania na Vercel preview.

## Notatki / follow-up

- Winowajcy (`add-i18n-keys.py`, `fix-tabs-i18n.py`) wstawiają krzywe cudzysłowy —
  do naprawy lub usunięcia, inaczej bug wróci. Na razie: `.gitignore` (nie commitować).
