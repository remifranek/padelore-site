# Changelog — padelore-site

Format: [Keep a Changelog](https://keepachangelog.com). Wpisy wiążą się ze specami w `docs/specs/`.

## [Unreleased]

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
