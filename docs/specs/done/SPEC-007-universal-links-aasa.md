# SPEC-007 — Universal Links: AASA + fallback `/get-app` (TASK-564)

**Status:** done (2026-07-14)
**Priorytet:** P0 (naprawia martwe linki share — viral loop kart meczu)
**Utworzony:** 2026-07-14
**Origin:** `padelwatch-pro/wiki/req-universal-links.md` (TASK-564, audyt KOMERCJA-03) — wszystkie deep-linki apki to custom scheme `padelore://`; link wysłany osobie BEZ apki jest martwy. Landing wchodzi PIERWSZY (cache Apple CDN ~tydzień), apka (entitlements + router) dopiero po weryfikacji AASA na produkcji.
**Preview:** `get-app.html` sam jest podglądem — `python3 -m http.server` i otwarcie `/get-app.html` (dark + light, 8 języków przez `?lang=xx`).

---

## Cel

`padelore.app` obsługuje Universal Links: iPhone z apką otwiera `https://padelore.app/m/*` i `/t/*` prosto w Padelore; iPhone bez apki dostaje stronę fallback z kontekstowym copy i przyciskiem App Store.

## Zakres

- **`.well-known/apple-app-site-association`** (bez rozszerzenia) — format modern `applinks.details[].appIDs/components`; appID `GDK8A962M9.app.padelore.ios`; ścieżki `/m/*` (udostępniony mecz) + `/t/*` (kod turnieju). Bez `webcredentials`.
- **`vercel.json`** — (1) header `Content-Type: application/json` dla AASA (Vercel nie zna typu pliku bez rozszerzenia; Apple CDN wymaga JSON bez redirectu); (2) `rewrites`: `/t/:code` i `/m/:payload` → `/get-app` (destination bez `.html`, bo `cleanUrls: true` — rewrite na `.html` groziłby 308 i utratą oryginalnego URL z paska). Istniejące nagłówki security nietknięte.
- **`get-app.html`** — fallback: reuse `ds.css?v=22`, `i18n.js`, `assets/app-icon.png`, wzorzec przycisku App Store z sekcji `#pobierz`. JS czyta `location.pathname`: `/t/` → copy „zaproszenie do turnieju", `/m/` → „czeka na Ciebie wynik meczu", inaczej generyczne. Ścieżki zasobów ABSOLUTNE (`/ds.css`…), bo strona serwuje się spod `/t/xxx`. Meta `apple-itunes-app` z samym `app-id` (statyczna strona — `app-argument` per-URL wymagałby meta w źródle; universal link i tak niesie pełny URL, gdy apka jest zainstalowana). `noindex`.
- **i18n** — 8 kluczy `getapp.*` × 8 języków (parytet — walidator wymaga pełnego kompletu, nie tylko PL+EN). Mechanizm `pick()/T()/apply()` z `index.html` zreplikowany inline (współdzieli `localStorage padelore.lang` — użytkownik, który wybrał język na landingu, dostaje fallback w tym samym języku).
- **Smart App Banner** — `<meta name="apple-itunes-app" content="app-id=6778968043">` w `index.html` + `support.html`.
- **README** — hosting poprawiony: Vercel git integration (było STALE „GitHub Pages").

## AC

- [x] `python3 -m json.tool .well-known/apple-app-site-association` — walidny JSON
- [x] `vercel.json` — walidny JSON, istniejące nagłówki zachowane
- [x] `get-app.html` serwuje się lokalnie (curl 200), warianty copy `/t/`, `/m/`, default działają z JS
- [x] `node scripts/validate-i18n.mjs` zielony (parytet 8 języków, 298 kluczy)
- [x] Meta Smart App Banner na `index.html` i `support.html`
- [ ] Po deployu: `curl -sI https://padelore.app/.well-known/apple-app-site-association` → 200, `application/json`, bez `location` (oba hosty: apex + www)
- [ ] Po deployu: `curl https://app-site-association.cdn-apple.com/a/v1/padelore.app` zwraca AASA

## Rekomendacja

1. **Destination rewrites = `/get-app` (bez `.html`)** — świadome odejście od litery specu (`get-app.html`): przy `cleanUrls: true` Vercel 308-uje żądania `*.html` na wersję bez rozszerzenia, co przy rewricie mogłoby zgubić oryginalny URL `/t/xxx` z paska adresu. Intencja specu (serwuj stronę fallback) zachowana. Rekomenduję zostawić.
2. **`app-argument` w meta pominięty** — strona statyczna nie może mieć meta per-URL w źródle, a doklejanie JS-em jest niedeterministyczne między wersjami Safari. Samo `app-id` wystarcza (banner otwiera App Store; kontekst niesie universal link). Jeśli kiedyś wejdzie SSR/edge function — dodać `app-argument` z pełnym URL.
3. **`noindex` na get-app** — strona techniczna, `/t|/m` z losowymi payloadami nie powinny lądować w Google. Rekomenduję zostawić.
4. **Kolejność wdrożenia (twarda):** merge + deploy landinga → smoke AASA na produkcji (oba hosty) → dopiero wtedy entitlements + router w apce (repo `padelwatch-pro`). Cache Apple CDN ~tydzień — im wcześniej deploy, tym szybciej linki zadziałają u użytkowników.

## Wynik

Branch `feat/task-564-universal-links-aasa` lokalnie (deploy = decyzja Remiego; push do `main` uruchamia produkcję). Weryfikacja lokalna zielona.
