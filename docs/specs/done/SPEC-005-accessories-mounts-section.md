# SPEC-005 — Sekcja „Akcesoria / uchwyty na telefon na kort"

**Status:** done (2026-07-06)
**Priorytet:** P2 (dodatkowa wartość dla użytkownika; wsparcie feature Fence)
**Utworzony:** 2026-07-06
**Origin:** prośba Remiego 2026-07-06 — „zrób sekcję gdzie mógłbym polecać uchwyty do telefonu na kort", pierwszy produkt: GIMADD (amzn.eu/d/00SyjhcR)
**Preview:** render live `#uchwyt` (zweryfikowany dark + light przed deployem)

---

## Cel

Sekcja `#uchwyt` przed `#pobierz`, w której Remi poleca uchwyty na telefon na kort —
sprzęt potrzebny, by realnie korzystać z feature **Fence** (telefon-tablica na ogrodzeniu).
Struktura **rozszerzalna**: dodanie kolejnego uchwytu = skopiowanie jednej karty + 1 klucz i18n.

## Zakres

- Nowa sekcja `#uchwyt` (`index.html`) między `#aktywnosc` a `#pobierz`.
- Grid kart produktów `.mount-grid` (CSS w `ds.css`, `ds.css?v=21`): zdjęcie (białe tło),
  badge „Nasz typ", nazwa (marka), opis, cena, CTA „Zobacz na Amazon".
- Pierwszy produkt: **GIMADD** — magnetyczny uchwyt neodymowy, ~204 zł, link Remiego (`amzn.eu`).
- Zdjęcie hostowane lokalnie (`assets/mounts/gimadd.jpg`, 679×725, 41 KB) — hotlink Amazona zawodny.
- i18n: 7 kluczy `acc.*` × 8 języków (natywne), parytet zachowany.
- Link: `rel="noopener nofollow"`, `target="_blank"`.

## Jak dodać kolejny uchwyt (dla Remiego)

1. W `#uchwyt .mount-grid` skopiuj cały `<a class="mount-card">…</a>`.
2. Podmień: `href` (link Amazon), `src` zdjęcia (wrzuć do `assets/mounts/`), `.mount-name`, `.mount-price`.
3. Dodaj klucz opisu `acc.<nazwa>_desc` w 8 blokach `i18n.js` (parytet — inaczej walidator czerwony).
4. `node scripts/validate-i18n.mjs` musi być zielony.

## AC

- [x] Sekcja renderuje się w dark i light, czytelna w obu (weryfikacja wizualna)
- [x] Karta wycentrowana przy 1 produkcie, grid rośnie w prawo przy kolejnych
- [x] Zdjęcie produktu widoczne (czarny uchwyt na białym tle panelu)
- [x] i18n 8 języków, walidator + `node --check` zielone
- [x] Link prowadzi do produktu Remiego (amzn.eu/d/00SyjhcR)

## Rekomendacja

1. **Afiliacja — do decyzji Remiego.** Link `amzn.eu` ma jego tagi `ref_`. Jeśli to link
   afiliacyjny (prowizja), UE wymaga jawnego ujawnienia („linki afiliacyjne") + `rel="sponsored"`.
   Teraz: `rel="noopener nofollow"` + neutralny disclaimer „Linki prowadzą do Amazon". Rekomenduję:
   jeśli afiliacja — dodać krótkie „Część linków to linki afiliacyjne" do `acc.note`.
2. **Placement przed `#pobierz`** — świadomie: najpierw sprzedaj feature, potem praktyczne akcesorium,
   potem CTA download. Rekomenduję zostawić.
3. **Bez linku w nav** — sekcja wspierająca, nie core. Rekomenduję nie dodawać (nav i tak gęsty).
4. **Cena statyczna `≈ 204 zł`** — zestarzeje się. Rekomenduję: albo Remi aktualizuje przy zmianie,
   albo usuwamy cenę (sam link). Na teraz zostawiam z „≈".

## Wynik

Deployed. Sekcja live, GIMADD jako pierwszy typ. Gotowa na kolejne uchwyty wg instrukcji wyżej.
