# SPEC-006 — Animacja onboardingu „krok po kroku" (telefon → zegarek)

**Status:** ready (preview do akceptacji Remiego)
**Priorytet:** P1 (główny hero-enhancer pod 1.13.0 — pokazuje wartość zamiast opisywać)
**Utworzony:** 2026-07-12
**Origin:** prośba Remiego 2026-07-12 — „mało to wszystko sexi. A jakby na pierwszej stronie była animacja krok po kroku co nacisnąć — najpierw telefon, potem to samo na zegarku z podpisem co się dzieje na ekranie".
**Decyzje Remiego:** flow = „szybki mecz → zegarek → tablica → karta → statystyki"; ekrany = REALNE zrzuty z produkcji (nie odbudowane w HTML — feedback Remiego 2026-07-12: „ekran home to nie jest ekran home z produkcji", „mockupy nie są zgodne z produkcją"). Zrzuty łapane rig-iem XCUITest (`ScreenshotTests`).
**Preview:** `docs/specs/preview/SPEC-006-onboarding-animation.html` (live: `padelore.app/docs/specs/preview/SPEC-006-onboarding-animation.html`)

---

## Cel

Prowadzony pokaz „jak używać Padelore" — od pustego ekranu do karty meczu. Zamiast opisu,
widz **widzi dokładnie co nacisnąć**: pulsujący wskaźnik tapnięcia na konkretnym przycisku,
podpis „co się dzieje", i płynne przejście telefon → zegarek. 7 kroków, ~20 s pętli.

## Koncept (v5 — zweryfikowany w preview)

- **Trzy urządzenia, jedno naraz w kadrze** — telefon (portrait), zegarek (Apple Watch z koroną
  + przyciskiem), telefon-poziomo (tablica na kracie). Aktywne świeci, przejście = crossfade.
- **REALNE zrzuty z produkcji** — nie odbudowa w HTML. Home, gracze, konfiguracja, zegarek,
  tablica, karta meczu, statystyki „Twoje ciało" — wszystkie łapane rig-iem (`ScreenshotTests`
  w padelwatch-pro, `--seed`), downscale do 294×640 (telefon) / 416×496 (zegarek) / 1000×460 (tablica).
- **Wskaźnik tapnięcia** — pulsujący lime ring + kropka na docelowym elemencie (kroki 1–4).
- **Pasek podpisu** — badge „Krok N/7 · Telefon/Zegarek/Tablica/Statystyki" + zdanie „co robisz".
- **Sterowanie** — autoplay (pętla, 3,4 s/krok), klikalne kropki, pauza, „od nowa".
- Dark + light (przełącznik w preview), responsywne.

### Flow (7 kroków)

| # | Urządzenie | Ekran (realny zrzut) | Tap | Podpis |
|---|---|---|---|---|
| 1 | Telefon | Home (`demo-1`) | Pojedynczy mecz | Otwórz Padelore → Pojedynczy mecz |
| 2 | Telefon | Gracze 2v2 (`demo-2`) | Dalej · konfiguracja | Ustaw pary — Ty, partner, rywale |
| 3 | Telefon | Ustawienia/punktacja (`demo-3`) | Rozpocznij mecz | Wybierz punktację (np. 21) i start |
| 4 | Zegarek | Wynik na nadgarstku (`demo-watch`) | strefa MY | Wynik zapisujesz na nadgarstku — tapnij MY |
| 5 | Tablica | Wynik na kracie (`demo-fence`) | — | Telefon na kracie → wielki wynik z drugiego końca kortu |
| 6 | Telefon | Karta meczu (`demo-5`) | — | Koniec → karta meczu: wynik, sety, kluczowe momenty |
| 7 | Statystyki | Twoje ciało (`demo-6`) | — | Zjeżdżasz niżej → ile Cię kosztował: wysiłek, strefy tętna, regeneracja |

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
