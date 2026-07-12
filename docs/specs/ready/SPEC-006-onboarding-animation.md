# SPEC-006 — Animacja onboardingu „krok po kroku" (telefon → zegarek)

**Status:** ready (preview do akceptacji Remiego)
**Priorytet:** P1 (główny hero-enhancer pod 1.13.0 — pokazuje wartość zamiast opisywać)
**Utworzony:** 2026-07-12
**Origin:** prośba Remiego 2026-07-12 — „mało to wszystko sexi. A jakby na pierwszej stronie była animacja krok po kroku co nacisnąć — najpierw telefon, potem to samo na zegarku z podpisem co się dzieje na ekranie".
**Decyzje Remiego:** flow = „szybki mecz → zegarek → karta"; ekrany = odbudowane w HTML/CSS (nie zrzuty).
**Preview:** `docs/specs/preview/SPEC-006-onboarding-animation.html` (live: `padelore.app/docs/specs/preview/SPEC-006-onboarding-animation.html`)

---

## Cel

Prowadzony pokaz „jak używać Padelore" — od pustego ekranu do karty meczu. Zamiast opisu,
widz **widzi dokładnie co nacisnąć**: pulsujący wskaźnik tapnięcia na konkretnym przycisku,
podpis „co się dzieje", i płynne przejście telefon → zegarek. 7 kroków, ~20 s pętli.

## Koncept (zweryfikowany w preview)

- **Dwie ramki naraz** — telefon (lewo) + zegarek (prawo). Aktywne urządzenie świeci
  (pełna jasność, skala 1), drugie przygaszone (opacity .34, skala .82). Przejście do aktu
  zegarka = zegarek się rozjaśnia → wizualny „handoff", bez słów.
- **Ekrany odbudowane w HTML/CSS** z design-tokenów landingu (spójne z resztą, aktualizowalne).
- **Wskaźnik tapnięcia** — pulsujący lime ring + kropka, pozycjonowany na docelowym elemencie.
- **Pasek podpisu** — badge „Krok N/7 · Telefon/Zegarek" + zdanie „co robisz".
- **Sterowanie** — autoplay (pętla, 2,8 s/krok), klikalne kropki kroków, pauza, „od nowa".
- Dark + light (przełącznik w preview), responsywne (mobile: urządzenia jedno pod drugim).

### Flow (7 kroków)

| # | Urządzenie | Ekran | Tap | Podpis |
|---|---|---|---|---|
| 1 | Telefon | Home | „Nowy mecz" | Otwórz Padelore i wybierz Nowy mecz |
| 2 | Telefon | Kto gra? (MY/ONI + format) | „Start" | Ustaw pary i naciśnij Start |
| 3 | Telefon→Zegarek | Handoff | — | Mecz sam ląduje na zegarku |
| 4 | Zegarek | Graj | „Graj" | Na zegarku naciśnij Graj |
| 5 | Zegarek | Wynik 0:0 → tap MY → 1 | strefa MY | Tapnij swój wynik kciukiem |
| 6 | Zegarek | Kto zdobył punkt? | „Ja" | Zaznacz źródło punktu (opcjonalne, 10 s) |
| 7 | Telefon | Karta meczu 21:8 + Match Effort | — | Koniec → karta meczu i profil „jak grasz" |

## Zakres integracji (po akceptacji)

- Nowa sekcja tuż pod hero (kandydat: przed `#vs` albo zaraz po hero-CTA).
- Wciągnięcie stylów do `ds.css` (bump wersji), markup do `index.html`, teksty kroków do `i18n.js`
  (klucze `demo.*` × 8 języków — parytet).
- Reduced-motion: statyczny pierwszy krok + kropki (bez autoplay).

## AC

- [ ] 7 kroków, autoplay + ręczne kroki, pauza — działa (preview: ✅)
- [ ] Tap trafia w docelowy element na każdym kroku (preview: ✅ zweryfikowane pomiarem)
- [ ] Handoff telefon→zegarek czytelny bez słów (preview: ✅)
- [ ] Dark i light OK
- [ ] i18n 8 języków, walidator zielony
- [ ] Reduced-motion nie łamie sekcji

## Rekomendacja

1. **To jest brakujący element „pokaż, nie opowiadaj".** Landing dziś opisuje wartość; ta sekcja
   pokazuje ją w 20 s. Rekomenduję jako główny hero-enhancer 1.13.0.
2. **Placement: zaraz pod hero-CTA, przed `#vs`.** Widz najpierw łapie „o co chodzi" wizualnie,
   dopiero potem czyta „po co druga apka". Alternatywa (integracja w sam hero) — odrzucam: hero
   już gęsty (makieta + watch + fence), dołożenie animacji = przeładowanie.
3. **Ekrany HTML, nie zrzuty — słusznie (Twoja decyzja).** Płynne tapnięcia i tick wyniku, których
   nie da się zrobić na PNG. Koszt: przy realnej zmianie UI w appce trzeba ręcznie dociągnąć makietę
   (ale to stylizowany demo-happy-path, nie 1:1 z buildem — drift jest akceptowalny).
4. **Do rozważenia w v2:** dźwięk tapnięcia (haptic-vibe wizualnie), albo „scrub" — przewijanie
   kroków scrollem zamiast autoplay. Na teraz autoplay + kropki wystarczą.

## Wynik

Preview zbudowany i zweryfikowany (tap trafia, handoff czytelny, wynik tyka, dark+light).
Czeka na akceptację Remiego przed integracją na live.
