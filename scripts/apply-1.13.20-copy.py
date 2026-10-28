#!/usr/bin/env python3
"""Landing pod Padelore 1.13.20: podmiana wartości kluczy i18n w 11 językach.

Uruchom z katalogu repo: python3 scripts/apply-1.13.20-copy.py
Każdy klucz musi wystąpić w bloku języka dokładnie raz; inaczej skrypt nic nie zapisuje.
"""
import json, re, sys

T = {
 "share.note": {
  "pl": "Nie ma Padelore? Link otworzy stronę, która podpowie, skąd wziąć apkę. Po instalacji wystarczy otworzyć link jeszcze raz — mecz wpadnie do jego historii.",
  "en": "No Padelore? The link opens a page that points to the App Store. After installing, open the link again and the match lands in their history.",
  "es": "¿No tiene Padelore? El enlace abre una página que le dice de dónde bajar la app. Después de instalarla, basta con abrir el enlace otra vez y el partido entra en su historial.",
  "it": "Non ha Padelore? Il link apre una pagina che indica dove prendere l'app. Dopo l'installazione basta riaprire il link e la partita entra nella sua cronologia.",
  "de": "Kein Padelore? Der Link öffnet eine Seite, die zeigt, wo es die App gibt. Nach der Installation den Link noch einmal öffnen — dann landet das Match im Verlauf.",
  "ru": "Нет Padelore? Ссылка откроет страницу, которая подскажет, где взять приложение. После установки достаточно открыть ссылку ещё раз — матч попадёт в историю.",
  "uk": "Немає Padelore? Посилання відкриє сторінку, яка підкаже, де взяти застосунок. Після встановлення достатньо відкрити посилання ще раз — матч потрапить до історії.",
  "pt": "Não tens o Padelore? O link abre uma página que diz onde ir buscar a app. Depois de instalar, basta abrir o link outra vez e o jogo entra no histórico.",
  "sv": "Ingen Padelore? Länken öppnar en sida som visar var appen finns. Efter installationen räcker det att öppna länken igen, så hamnar matchen i historiken.",
  "fr": "Pas de Padelore ? Le lien ouvre une page qui indique où prendre l’appli. Une fois l’appli installée, il suffit de rouvrir le lien : le match arrive dans l’historique.",
  "nl": "Geen Padelore? De link opent een pagina die naar de App Store wijst. Na de installatie open je de link nog een keer en staat de match in de geschiedenis.",
 },
 "start.li1_html": {
  "pl": "<b>Z zegarka</b> — gdy grasz z kimś nowym albo nie chce Ci się wpisywać nazwisk. Imiona dopiszesz po meczu w Historii, opcją „Skład”. Do rankingu taki mecz się nie liczy.",
  "en": "<b>From the watch</b> — when you play someone new, or simply do not feel like typing names. Add the names after the match in History, under “Line-up”. Such a match does not count towards the ranking.",
  "es": "<b>Desde el reloj</b> — cuando juegas con alguien nuevo o no te apetece escribir nombres. Los nombres los añades después del partido en Historial, con «Alineación». Ese partido no cuenta para el ranking.",
  "it": "<b>Dall'orologio</b> — quando giochi con qualcuno di nuovo o non hai voglia di scrivere i nomi. I nomi li aggiungi dopo la partita in Cronologia, con «Formazione». Quella partita non conta per la classifica.",
  "de": "<b>Von der Uhr</b> — wenn du mit jemand Neuem spielst oder keine Lust hast, Namen einzutippen. Die Namen trägst du nach dem Match im Verlauf unter „Aufstellung“ nach. Für das Ranking zählt so ein Match nicht.",
  "ru": "<b>С часов</b> — когда играешь с кем-то новым или просто лень вбивать фамилии. Имена добавишь после матча в «Истории», через «Состав». В рейтинг такой матч не идёт.",
  "uk": "<b>З годинника</b> — коли граєш із кимось новим або просто ліньки вписувати прізвища. Імена допишеш після матчу в «Історії», через «Склад». До рейтингу такий матч не йде.",
  "pt": "<b>A partir do relógio</b> — quando jogas com alguém novo ou não te apetece escrever nomes. Os nomes acrescentas depois do jogo no Histórico, em «Formação». Esse jogo não conta para o ranking.",
  "sv": "<b>Från klockan</b> — när du spelar med någon ny eller inte orkar skriva in namn. Namnen lägger du till efter matchen i Historik, under ”Laguppställning”. En sådan match räknas inte till rankingen.",
  "fr": "<b>Depuis la montre</b> — quand tu joues avec quelqu’un de nouveau, ou que tu n’as pas envie de saisir des noms. Les noms, tu les ajoutes après le match dans l’Historique, via « Composition ». Ce match ne compte pas pour le classement.",
  "nl": "<b>Vanaf het horloge</b> — als je met iemand nieuws speelt of geen zin hebt om namen te typen. Namen voeg je na de match toe in Geschiedenis, via ‘Opstelling’. Zo’n match telt niet mee voor de ranking.",
 },
 "watch.s4_p": {
  "pl": "Każdy punkt z zegarka ląduje na telefonie jako wielka tablica „fence” — duże cyfry, MY/ONI, kto serwuje. Postaw telefon na kracie — wszyscy widzą wynik. Tablica pokazuje też, skąd biorą się punkty i jakie masz tętno.",
  "en": "Every tap from the watch lands on the phone as a big “fence” scoreboard — large digits, US/THEM, who's serving. Set the phone on the fence — everyone sees the score. The board also shows where the points come from and your heart rate.",
  "es": "Cada toque del reloj aparece en el teléfono como un gran tablero «valla» — cifras grandes, NOSOTROS/ELLOS, quién saca. Pon el teléfono en la valla y todos ven el partido. El tablero también muestra de dónde vienen los puntos y tu pulso.",
  "it": "Ogni punto dall'orologio compare sul telefono come un grande tabellone «Fence» — cifre grandi, NOI/LORO, chi serve. Appoggia il telefono alla recinzione: tutti vedono la partita. Il tabellone mostra anche da dove arrivano i punti e il tuo battito.",
  "de": "Jeder Punkt von der Watch erscheint auf dem Handy als große „Fence“-Anzeigetafel — große Ziffern, WIR/SIE, wer aufschlägt. Stell das Handy an den Zaun — alle sehen den Stand. Die Tafel zeigt auch, woher die Punkte kommen, und deinen Puls.",
  "ru": "Каждое очко с часов появляется на телефоне как большое табло «Fence» — крупные цифры, МЫ/ОНИ, кто подаёт. Поставь телефон на ограждение — все видят счёт. Табло показывает ещё, откуда берутся очки, и твой пульс.",
  "uk": "Кожне очко з годинника з’являється на телефоні великим табло «на огорожі» — великі цифри, МИ/ВОНИ, хто подає. Постав телефон на огорожу — усі бачать рахунок. Табло показує ще, звідки беруться очки, і твій пульс.",
  "pt": "Cada toque do relógio aparece no telemóvel como um grande marcador «na vedação» — números grandes, NÓS/ELES, quem serve. Pousa o telemóvel na vedação — todos veem o jogo. O marcador mostra também de onde vêm os pontos e a tua frequência cardíaca.",
  "sv": "Varje poäng från klockan landar på telefonen som en stor ”fence”-tavla — stora siffror, VI/DE, vem som servar. Ställ telefonen på gallret — alla ser ställningen. Tavlan visar också var poängen kommer ifrån och din puls.",
  "fr": "Chaque point tapé sur la montre arrive sur le téléphone en grand tableau « fence » — gros chiffres, NOUS/EUX, qui sert. Pose le téléphone sur le grillage — tout le monde voit le score. Le tableau montre aussi d’où viennent les points et ton rythme cardiaque.",
  "nl": "Elke tik op het horloge komt op de telefoon binnen als een groot ‘fence’-scorebord — grote cijfers, WIJ/ZIJ, wie serveert. Zet de telefoon aan het hek en iedereen ziet de stand. Het bord laat ook zien waar de punten vandaan komen en wat je hartslag doet.",
 },
 "tour.s2_li1": {
  "pl": "Rundy i korty układają się same. W Americano indywidualnym każdy gra z innym partnerem i rozgrywa podobną liczbę meczów.",
  "en": "Rounds and courts lay out by themselves. In individual Americano everyone gets a different partner and a similar number of matches.",
  "es": "Las rondas y pistas se organizan solas. En el Americano individual cada uno juega con un compañero distinto y un número parecido de partidos.",
  "it": "Turni e campi si organizzano da soli. Nell'Americano individuale ognuno cambia compagno e gioca un numero simile di partite.",
  "de": "Runden und Plätze werden automatisch angelegt. Im Americano „Einzeln“ spielt jeder mit wechselnden Partnern und ähnlich vielen Matches.",
  "ru": "Раунды и корты раскладываются автоматически. В индивидуальном Americano у каждого новый партнёр и примерно одинаковое число матчей.",
  "uk": "Раунди і корти розкладаються автоматично. В індивідуальному Americano кожен грає з іншим партнером і має приблизно однакову кількість матчів.",
  "pt": "Rondas e campos organizam-se automaticamente. No Americano individual cada um joga com um parceiro diferente e um número parecido de jogos.",
  "sv": "Rundor och banor läggs upp automatiskt. I individuell Americano får alla en ny partner och ungefär lika många matcher.",
  "fr": "Les tours et les terrains se placent automatiquement. En Americano individuel, chacun change de partenaire et joue à peu près autant de matchs.",
  "nl": "Rondes en banen worden vanzelf ingedeeld. Bij individuele Americano krijgt iedereen een andere partner en ongeveer evenveel matches.",
 },
 "tour.s2_li2": {
  "pl": "Zamkniętą rundę poprawisz, a w Mexicano rozstawienie przeliczy się samo.",
  "en": "A closed round can be corrected, and in Mexicano the pairings recalculate themselves.",
  "es": "Una ronda cerrada se puede corregir, y en Mexicano los emparejamientos se recalculan solos.",
  "it": "Un turno chiuso si può correggere, e nel Mexicano gli accoppiamenti si ricalcolano da soli.",
  "de": "Eine abgeschlossene Runde lässt sich korrigieren, im Mexicano berechnen sich die Paarungen dann neu.",
  "ru": "Закрытый раунд можно исправить, а в Mexicano пары пересчитаются сами.",
  "uk": "Закритий раунд можна виправити, а в Mexicano пари перерахуються самі.",
  "pt": "Uma ronda fechada pode ser corrigida, e no Mexicano os emparelhamentos recalculam-se sozinhos.",
  "sv": "En avslutad runda går att rätta, och i Mexicano räknas parningarna om av sig själva.",
  "fr": "Un tour clôturé se corrige, et en Mexicano les paires se recalculent toutes seules.",
  "nl": "Een afgesloten ronde kun je corrigeren, en bij Mexicano rekent de indeling zich vanzelf opnieuw uit.",
 },
 "tour.s2_li3": {
  "pl": "Tabela i statystyki aktualizują się same, a po turnieju wyślesz je grupie jako obrazy.",
  "en": "Table and stats update on their own, and after the tournament you send them to the group as images.",
  "es": "Tabla y estadísticas se actualizan solas, y al terminar el torneo las mandas al grupo como imágenes.",
  "it": "Classifica e statistiche si aggiornano da sole, e a fine torneo le mandi al gruppo come immagini.",
  "de": "Tabelle und Statistik aktualisieren sich von selbst, nach dem Turnier schickst du sie als Bilder in die Gruppe.",
  "ru": "Таблица и статистика обновляются сами, а после турнира отправишь их в группу картинками.",
  "uk": "Таблиця та статистика оновлюються самі, а після турніру надішлеш їх у групу картинками.",
  "pt": "Tabela e estatísticas atualizam-se sozinhas, e no fim do torneio envias tudo ao grupo em imagens.",
  "sv": "Tabell och statistik uppdateras av sig själva, och efter turneringen skickar du dem till gruppen som bilder.",
  "fr": "Le tableau et les stats se mettent à jour tout seuls, et après le tournoi tu les envoies au groupe en images.",
  "nl": "Tabel en statistieken lopen vanzelf mee, en na het toernooi stuur je ze als afbeeldingen naar de groep.",
 },
 "cta.p": {
  "pl": "Pobierz Padelore na iPhone, iPada i Apple Watch — działa obok Twojej apki do rezerwacji, nie zamiast niej.",
  "en": "Get Padelore for iPhone, iPad and Apple Watch — it works alongside your booking app, not instead of it.",
  "es": "Descarga Padelore para iPhone, iPad y Apple Watch — va con tu app de reservas, no en su lugar.",
  "it": "Scarica Padelore per iPhone, iPad e Apple Watch — sta accanto alla tua app di prenotazione, non la sostituisce.",
  "de": "Hol dir Padelore für iPhone, iPad und Apple Watch — es läuft neben deiner Buchungs-App, nicht an ihrer Stelle.",
  "ru": "Скачай Padelore для iPhone, iPad и Apple Watch — он работает рядом с твоим приложением для брони, а не вместо него.",
  "uk": "Завантаж Padelore для iPhone, iPad та Apple Watch — працює поряд із твоїм застосунком для броні, а не замість нього.",
  "pt": "Instala o Padelore no iPhone, no iPad e no Apple Watch — funciona ao lado da tua app de reservas, não em vez dela.",
  "sv": "Hämta Padelore till iPhone, iPad och Apple Watch — den funkar vid sidan av din bokningsapp, inte i stället för den.",
  "fr": "Prends Padelore sur iPhone, iPad et Apple Watch — ça tourne à côté de ton appli de réservation, pas à sa place.",
  "nl": "Haal Padelore voor iPhone, iPad en Apple Watch — hij werkt naast je boekingsapp, niet in plaats daarvan.",
 },
}

LANGS = ["pl","en","es","it","de","ru","uk","pt","sv","fr","nl"]
src = open("i18n.js", encoding="utf-8").read()
lines = src.split("\n")
starts = {}
for i, l in enumerate(lines):
    m = re.match(r"^([a-z]{2}): \{$", l)
    if m: starts[m.group(1)] = i
assert sorted(starts) == sorted(LANGS), starts
order = sorted(starts.items(), key=lambda x: x[1])
ranges = {lang: (s, order[n+1][1] if n+1 < len(order) else len(lines)) for n, (lang, s) in enumerate(order)}

errors = []
for key, per in T.items():
    assert sorted(per) == sorted(LANGS), key
    for lang in LANGS:
        a, b = ranges[lang]
        pat = re.compile(r'^(\s*)"' + re.escape(key) + r'"\s*:\s*".*",?\s*$')
        hits = [i for i in range(a, b) if pat.match(lines[i])]
        if len(hits) != 1:
            errors.append(f"{lang}/{key}: {len(hits)} trafień"); continue
        i = hits[0]
        indent = pat.match(lines[i]).group(1)
        comma = "," if lines[i].rstrip().endswith(",") else ""
        lines[i] = f'{indent}"{key}": {json.dumps(per[lang], ensure_ascii=False)}{comma}'
if errors:
    print("BŁĄD, nic nie zapisano:\n" + "\n".join(errors)); sys.exit(1)
open("i18n.js", "w", encoding="utf-8").write("\n".join(lines))
print(f"OK: {len(T)} kluczy × {len(LANGS)} języków")
