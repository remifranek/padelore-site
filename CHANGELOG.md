# Changelog — padelore-site

Format: [Keep a Changelog](https://keepachangelog.com). Wpisy wiążą się ze specami w `docs/specs/`.

## [Unreleased]

### Fixed
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
