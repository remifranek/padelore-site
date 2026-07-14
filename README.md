# padelore-site

Landing + strony prawne Padelore (App Store).

**Hosting: Vercel** (git integration) — push do `main` = deploy produkcyjny `padelore.app`. Cloudflare robi wyłącznie DNS. Konfiguracja routingu i nagłówków: `vercel.json`.

- `/index.html` — landing (i18n 8 języków przez `i18n.js`, walidator: `node scripts/validate-i18n.mjs`)
- `/privacy.html` — Polityka prywatności (PL/EN) → wymagane przez App Store
- `/support.html` — Wsparcie + FAQ (PL/EN) → Support URL w App Store
- `/get-app.html` — fallback Universal Links: `/m/*` (udostępniony mecz) i `/t/*` (kod turnieju) rewritowane na tę stronę, gdy apka nie jest zainstalowana
- `/.well-known/apple-app-site-association` — AASA dla Universal Links (Content-Type `application/json` wymuszony w `vercel.json`; bez redirectów na tej ścieżce)

Specy zmian: `docs/specs/` (ready → done, preview w `docs/specs/preview/`).
