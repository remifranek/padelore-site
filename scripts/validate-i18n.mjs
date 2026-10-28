#!/usr/bin/env node
// Walidator parzystości i18n (SPEC-003). Uruchom: node scripts/validate-i18n.mjs
// Bramka: (a) i18n.js parsuje się, (b) każdy klucz z HTML istnieje we WSZYSTKICH blokach,
// (c) wszystkie bloki mają identyczny zestaw kluczy (źródło prawdy: pl).
// Exit 1 przy jakimkolwiek naruszeniu — nadaje się do pre-commit / Vercel build.
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const fail = [];

// (a) załaduj i18n.js
const g = {};
try {
  new Function("window", readFileSync(join(ROOT, "i18n.js"), "utf8"))(g);
} catch (e) {
  console.error("❌ i18n.js nie parsuje się:", e.message);
  process.exit(1);
}
const I = g.I18N;
if (!I) { console.error("❌ window.I18N nie zdefiniowane"); process.exit(1); }
const langs = Object.keys(I);

// (b) klucze wymagane przez HTML
const html = readFileSync(join(ROOT, "index.html"), "utf8");
const need = [...new Set(
  [...html.matchAll(/data-i18n(?:-html|-alt|-aria)?="([^"]+)"/g)].map((m) => m[1])
)];
for (const l of langs) {
  const miss = need.filter((k) => !(k in I[l]));
  if (miss.length) fail.push(`[${l}] brak ${miss.length} kluczy z HTML: ${miss.join(", ")}`);
}

// (c) parzystość zestawu kluczy (pl = źródło prawdy)
const ref = new Set(Object.keys(I.pl));
for (const l of langs) {
  const cur = new Set(Object.keys(I[l]));
  const missing = [...ref].filter((k) => !cur.has(k));
  const extra = [...cur].filter((k) => !ref.has(k));
  if (missing.length) fail.push(`[${l}] brak vs pl (${missing.length}): ${missing.join(", ")}`);
  if (extra.length) fail.push(`[${l}] nadmiar vs pl (${extra.length}): ${extra.join(", ")}`);
}

// (d) listy LANGS w skryptach stron = komplet bloków i18n.js. Do 2026-10-28 index.html i get-app.html
// miały 8 języków przy 11 blokach, więc ?lang=sv|fr|nl, zapamiętany wybór i język przeglądarki
// sv/fr/nl dawały wersję angielską, a walidator świecił na zielono.
for (const page of ["index.html", "get-app.html"]) {
  const src = readFileSync(join(ROOT, page), "utf8");
  const m = src.match(/var LANGS=\[([^\]]*)\]/);
  if (!m) { fail.push(`[${page}] brak tablicy LANGS`); continue; }
  const list = [...m[1].matchAll(/'([a-z]{2})'/g)].map((x) => x[1]);
  const miss = langs.filter((l) => !list.includes(l));
  const extra = list.filter((l) => !langs.includes(l));
  if (miss.length) fail.push(`[${page}] LANGS bez języków z i18n.js: ${miss.join(", ")}`);
  if (extra.length) fail.push(`[${page}] LANGS z językami spoza i18n.js: ${extra.join(", ")}`);
}

// raport
console.log(`Języki: ${langs.join(", ")} | klucze/HTML: ${need.length} | klucze/pl: ${ref.size}`);
if (fail.length) {
  console.error(`\n❌ WALIDACJA i18n — ${fail.length} problemów:`);
  fail.forEach((f) => console.error("  - " + f));
  process.exit(1);
}
console.log(`✅ WALIDACJA i18n: parsuje, komplet kluczy z HTML, parzystość ${langs.length} języków.`);
