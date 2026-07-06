# Changelog — padelore-site

Format: [Keep a Changelog](https://keepachangelog.com). Wpisy wiążą się ze specami w `docs/specs/`.

## [Unreleased]

### Added
- **Sekcja „Akcesoria · na kort" (`#uchwyt`)** (SPEC-005, prośba Remiego): rozszerzalny grid
  kart z polecanymi uchwytami na telefon na kort (wsparcie feature Fence). Pierwszy produkt:
  GIMADD (magnetyczny, neodymowy, ~204 zł). Zdjęcie hostowane lokalnie (`assets/mounts/`), i18n
  7 kluczy `acc.*` × 8 języków, `ds.css?v=21` (`.mount-*`). Dodanie kolejnego uchwytu = kopia
  1 karty + 1 klucz i18n (instrukcja w SPEC-005 i komentarzu HTML). Zweryfikowane dark + light.


### Fixed
- **Pełny audyt 8 języków (native, ~55 poprawek)**: przegląd każdego bloku pod kątem
  terminologii padlowej + naturalności + zrozumiałości. Najważniejsze: (1) **odzyskany zgubiony
  fence-fix UK** `hero.lead` „на сітці"→„на огорожі" (poprzedni regex urwał się na wewn. `\"`,
  a weryfikacja przegapiła przez deklinację сітці≠сітк); (2) `twatch.li3_html` „4 s"→„10 s" w 8
  językach (spójność z 10-sekundowym oknem tagowania); (3) **«» → cudzysłowy narodowe w EN/DE
  start.*** (ten sam spadek po SPEC-002 co PL — EN „", DE „"); (4) terminy: EN „fills the game"→
  „finds you a game", IT „segnala"→„segna"/„gioco"→„game"/„round"→„turno", PT duplas↔pares (zamienione),
  DE „füllt das Match"→„findet die Mitspieler"/„Holen"→„Download"; (5) „soczewka/lens/lente"→
  „zakładka/tab" w tłumaczeniach (jasność); (6) RU „Куба"(=kraj)→„Макс", „ход очки"→„динамика",
  spójność „Forma"→„Aktywność"/„Attività"/„Atividade" (nazwa zakładki). Parytet 8× + walidator zielone.
- **Fix terminologii „ogrodzenie kortu" w IT/PT/RU/UK (34 poprawki)** — mój błąd: ogrodzenie
  obwodowe kortu (na którym stawiasz telefon jako tablicę) było tłumaczone jako „net/siatka do
  gry": IT „rete", PT „rede" (systemowo w całym bloku — nie tylko nowa sekcja), miejscami RU/UK
  „сетка/сітка". Chrome auto-translate IT/PT „rete/rede"→„network" → stąd „put phone on the network".
  Naprawione natywnie: IT→„recinzione", PT→„vedação", RU→„ограждение", UK→„огорожа"; tab4_b
  IT/PT→„Fence" (nazwa funkcji). RU/UK „сетка za formą"=drabinka turniejowa zostawione (poprawne).
  Objęte: acc.*, hero.lead, watch.s4_*, watch.tab4_b, vs.add_1, tour.s2. Klucze `acc.*` napisane
  przeze mnie bez natywnego przeglądu — proces naprawiony (native-review także dla PL/nowych kluczy).
- **Fix: przycisk „Grupa WhatsApp" nieczytelny w light mode** (feedback Remiego):
  `.btn-ghost` w banerze CTA brał `color:var(--ink)`, który w light robi się ciemny granat
  (#0E1730) — a baner jest zawsze niebieski/ciemny (biały tekst h2/p). Ciemny tekst na ciemnym
  = niewidoczny. Dodany scoped override `.cta-band .btn-ghost{color:#fff}` (biały w obu
  motywach, jak reszta banera). Bump `ds.css?v=19→20`.
- **Fakt: czas na powód punktu 4 → 10 sekund** (feedback Remiego): `twatch.p_html`
  („Skąd punkty" — tagowanie źródła punktu na zegarku) mówił „masz 4 sekundy", realnie
  w appce okno to 10 sekund. Poprawione w 8 językach (z odmianą: PL „4 sekundy"→„10 sekund",
  RU/UK „секунды/секунди"→„секунд") + statyczny fallback HTML.
- **Spójność „fence": „na płocie" → „na kracie"** w kroku 4 (`watch.s4_h`, `watch.s4_p`):
  reszta strony konsekwentnie mówi „tablica na kracie" (hero, #vs, #turniej ×3), a krok 4
  wyłamywał się „na płocie" („płot" = wiejskie ogrodzenie, brzmi obco dla kortu padla).
- **Audyt polskiego źródła (10 poprawek)**: przegląd bloku PL (którego wcześniej nie
  audytowałem — traktowany jako źródło). Naprawione: cudzysłowy «» → polskie „ " w start.*
  (spadek po SPEC-002, gdy start.* siedziały w bloku es); anglicyzmy „Setup"→„Gotowe",
  „Tap"→„Tapnij"; „dobijasz punkty" → „zaliczasz punkty" (×3 — „dobić" w padlu = smecz,
  dwuznaczne); „na iPhone" → „na iPhonie"; „Z dwóch danych… log punktów" → „Wszystko z danych…
  logu punktów"; „poziom / level" → „poziom (level)"; „pokazuje Cię dziś kontra Ciebie" →
  „zestawia Cię dziś z Tobą". Walidator + node --check zielone.
- **#mecz: realna karta meczu zamiast makiety `.mcard`** (zasada handoffu): fałszywa
  HTML-owa makieta karty meczu (Match Effort ring, punkty×tętno SVG) zastąpiona realnym
  zrzutem `SingleMatchSummaryView` — WYGRANA 2-1, przebieg setów, kluczowe momenty (szczyt
  tętna 171), koszt meczu (WYSIŁEK), strefy tętna. Możliwe dzięki dodaniu pełnego timeline
  (HR+punkty+kroki) do seed-meczu w padelwatch-pro. Usunięto 15 kluczy `mock.m_*`, dodano `mecz.card_alt`.
- **Native-review 7 tłumaczeń (107 poprawek)**: przegląd każdego bloku językowego przez
  natywnego copywritera vs polski oryginał. Naprawione kalki, nienaturalne kolokacje, błędy
  terminologii i AI-slop. Najczęstsze: terminologia padlowa „liczyć"→„segnare/anotar/вести
  рахунок" (es/it), spójność „Round/тур"→„Turno/раунд" (it/ru/uk), kolizja „karta meczu vs
  mapa" (de „Match-Matrix", ru/uk „картка матча"), cudzysłowy per-locale (« » es/it/ru/uk/pt,
  „ " de, " " en), błędne tagi kroków (pt/ru „Konfiguracja"→„Gracze/Urządzenie"), „apostas"→
  „tensão" (pt), „Linse/лінза"→„Ansicht/вкладка" (de/uk), „П/П"→„В/П" (ru). Parzystość 302×8
  zachowana, składnia i walidator zielone.
- **#ja pokazuje „Jak gram" (Impact Rating), nie Aktywność**: batch11 `06-stats` wyszedł
  identyczny z `09-activity` (oba = zakładka Aktywność) → #ja duplikowało #aktywnosc i gubiło
  Impact Rating/archetyp. Zrzut przełączony na segment „Jak gram" (IMPACT RATING 0/100, ARCHETYP
  Wszechstronny, MAPA WYNIK×WYSIŁEK).
- **Screeny 1.9.0 zgodne z realną produkcją** (feedback Remiego): seed kumulował kilkanaście
  wystartowanych turniejów („NA ŻYWO" ×kilkanaście na Home) → przez to brakowało action cards
  i ekrany nie odpowiadały appce. Zregenerowane z czystego stanu (1 aktywny turniej „Klub Wisła"):
  01-home = greeting + JAK GRAM + 1 turniej + action cards (Pojedynczy mecz / Gram w turnieju),
  wymuszony dark mode. Podmienione 01/02/03/05/06/08/09.
- **Realny watch-home 1.9.0** (feedback Remiego): stary `watch-home.png` pokazywał niebieski przycisk
  „History", którego w produkcji nie ma — ekran główny zegarka 1.9.0 to żółty „▶ Play" + ciemna
  „History" (żółty tekst), tylko żółty + czarny. Zregenerowane ze świeżego builda `PadelMatchProWatch`
  na watch-sim. Hero-watch wrócił na `watch-home` (poprzedni swap na `watch-scoring` był z błędnego
  odczytania „nie ma niebieskiego").

### Removed
- **Martwy CSS/JS fake-ekranów** (SPEC-003 domknięte): ~260 linii nieużywanych stylów
  (`.apscr`/`.ap`, `.tboard`, `.twatch`, `.jacard`(+`.ak`), `.tw-*`, `.wface`/watch ScoreView,
  `.shots2`, `.app-ic`) + martwy JS `watchAnim()`/`wflash()` (sterowały nieistniejącymi
  #pmy/#poni/#smy). Karuzela `.fl-*`, `.fenceboard`, `.mcard`, `.split*`, `.skb*` zostają.

### Changed
- **Cut-30% leadów — 11 akapitów odchudzonych w 8 językach** (feedback Remiego „czy nie
  za dużo tekstu"): najdłuższe leady/akapity skrócone o ~20-25% bez zmiany tezy i faktów
  (hero.lead 58→36 słów, twatch/mecz/tour/league/vs/ja/akt/watch.s2/s4). Usunięty filler
  i powtórzona teza booking↔Padelore. PL napisany ręcznie, 7 języków przez natywnych
  tłumaczy skróconej wersji. Struktura sekcji bez zmian (decyzja Remiego: tylko leady, bez scalania).
- **Logo → wordmark „Padel●re"** (żółta kulka zamiast „o", jak w appce 1.9.0) zamiast ikona+tekst.
- **Restyle landingu na design system appki 1.9.0** (SPEC-004): font Bricolage Grotesque
  + Nunito (numerale), hero grad ujednolicony do ball-yellow `--accent`. 7 ręcznie budowanych
  fake HTML-owych ekranów zastąpionych prawdziwymi zrzutami z produkcji 1.9.0 w ramkach iPhone
  (hero 01-home + watch-home, #turniej wizard + tournament, #liga standings, #ja stats, #mecz watch).
  Zrzuty 05/08/09 wygenerowane z padelwatch-pro ScreenshotTests (fix nawigacji do karty turnieju).
  Follow-up (oflagowane): fence = wierna tablica HTML, watch-tagging → watch-scoring, #aktywnosc → stats (interim).

### Fixed
- **i18n.js — hotfix składni** (SPEC-001): krzywe cudzysłowy `“ ”` użyte jako ograniczniki
  JS + nieescapowane wewnętrzne `"` psuły parsowanie → cała treść poniżej hero nie
  renderowała się w 8 językach na produkcji. Ograniczniki → proste `"`, wewnętrzne → `\"`.

### Added
- **Walidator parzystości i18n** `scripts/validate-i18n.mjs` (SPEC-003): bramka sprawdzająca
  składnię, komplet kluczy z HTML w 8 językach i identyczny zestaw kluczy (pl = źródło prawdy).

### Removed
- **Martwe klucze i18n** (SPEC-003): `mock.r_done/now/plan/live/saved` (tylko pl) i
  `watch.wface_set` (+ jego duplikaty z wmieszanym PL/ES w blokach es/it). 0 użyć w HTML.
  Efekt: pełna parzystość 302/302 we wszystkich 8 językach.

### Changed
- **Lokalizacja start.* + watch.s4_hint / watch.s3_alt** (SPEC-002): błędnie wrzucony
  8-językowy zrzut `start.*` (siedział w bloku `es`) rozłożony do właściwych bloków —
  naprawia hiszpański (był portugalski) i uzupełnia it/de/ru/uk/pt. Dopisano `watch.s4_hint`
  (6 języków) i `watch.s3_alt` (naprawa wmieszanych języków). Wszystkie 8 języków: komplet
  234 kluczy wymaganych przez HTML.
