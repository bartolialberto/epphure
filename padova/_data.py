# -*- coding: utf-8 -*-
"""Dati del sito "Un giorno a Padova" — sabato, 9:30 → 18:20.

Orari e prezzi raccolti il 22 settembre 2026 dalle fonti ufficiali
(padovamusei.it, unipd.it, kalata.it, santantonio.org, ortobotanico1545.it,
turismopadova.it, fsbusitalia.it, bacaropadovano.com). Da riverificare prima di partire.
"""

GIORNO = u"sabato"
ARRIVO = u"09:30"
RIENTRO = u"18:20"

# ----------------------------------------------------------------- i luoghi toccati
# id -> scheda del posto. Le due varianti li mettono in fila in ordini diversi.
PLACES = {
    "stazione": dict(nome="Stazione FS", lat=45.4167, lon=11.8797, card=False,
        distanze=[(u"Centro, Caffè Pedrocchi", u"1,3 km", u"20 min a piedi", u"tram SIR1, 3 fermate"),
                  (u"Basilica del Santo", u"2,3 km", u"30 min a piedi", u"tram SIR1 fino a <b>Santo</b>, 6 fermate, ~20 min in tutto"),
                  (u"Prato della Valle", u"2,5 km", u"32 min a piedi", u"tram SIR1, 7 fermate")],
        testo="Prima cosa: il <b>biglietto del tram</b>, alla biglietteria Busitalia in stazione o al distributore "
              "del piazzale. Poi venti minuti a piedi lungo Corso del Popolo, oppure tre fermate di tram fino a "
              "Ponti Romani. Si passa accanto agli Eremitani: la Cappella degli Scrovegni resta sulla sinistra."),
    "pedrocchi": dict(nome="Caffè Pedrocchi", lat=45.4077, lon=11.8766, card=False,
        testo="Il <b>caffè senza porte</b>, aperto giorno e notte per un secolo. Un caffè alla menta al banco, "
              "poi di sopra: il <b>Piano Nobile</b> di Jappelli è una sfilata di sale egizia, greca, etrusca, rinascimentale.",
        nota="Il Piano Nobile chiude alle 12:30 e riapre alle 15:30: di mattina non si può rimandare."),
    "bo": dict(nome="Palazzo del Bo", fonte=(u"Università di Padova", u"https://www.unipd.it/palazzo-bo-900-gio-ponti-informazioni-tariffe"), lat=45.4069, lon=11.8772, card=False,
        testo="La sede storica dell’Università. Il <b>Teatro Anatomico del 1594</b>, il più antico al mondo ancora in piedi, "
              "la cattedra di Galileo, l’Aula Magna, la statua di Elena Lucrezia Cornaro Piscopia — prima laureata della storia — "
              "e, nel fine settimana, anche l’ala razionalista di Gio Ponti.",
        nota="Di sabato il tour dura <b>75 minuti</b> e costa 12,00 € invece di 7,00: è il giro lungo, che aggiunge il Novecento. "
             "<b>Prenotazione obbligatoria.</b> Turni: 9:30, 10:30, 11:30 (EN), 12:30, 14:30 (EN), 15:30, 16:30 (EN), 17:30.",
        nota_ada="<b>Perché dopo pranzo:</b> nell’itinerario Ada si rientra dal Santo verso le 11:30, e i 75 minuti del giro non ci stanno prima delle 13. Il turno delle 11:30 è in inglese; quello delle 12:30 finirebbe alle 13:45, cioè tre quarti d’ora dopo il tavolo prenotato. Resta il turno delle <b>15:30</b>, che chiude la giornata con tutto il tempo per arrivare al Prato."),
    "ragione": dict(nome="Palazzo della Ragione", fonte=(u"Musei Civici di Padova", u"https://padovamusei.it/it/biglietti-orari-musei"), lat=45.4074, lon=11.8747, card=True,
        testo="Il <b>Salone</b>: 80 metri di sala pensile senza colonne, sotto una carena di nave rovesciata, "
              "e attorno 333 riquadri affrescati con il calendario astrologico di Pietro d’Abano. Sotto, le due piazze del mercato, "
              "che di sabato mattina sono nel pieno."),
    "signori": dict(nome="Piazza dei Signori", lat=45.4079, lon=11.8720, card=False,
        testo="La <b>Torre dell’Orologio</b> del 1344, con il quadrante astronomico che segna ore, fasi lunari e segni zodiacali "
              "— e che, per un errore diventato leggenda, la Bilancia non ce l’ha. Accanto, la Loggia del Consiglio."),
    "pranzo": dict(nome="Bacaro Padovano", fonte=(u"bacaropadovano.com", u"https://www.bacaropadovano.com/contatti/"), lat=45.40545, lon=11.87242, card=False, pasto=True,
        testo="Pranzo prenotato. Cicchetteria e cucina veneziana in Via San Gregorio Barbarigo, tre minuti dal Duomo "
              "e cinque da Piazza dei Signori.",
        nota="Di sabato serve a pranzo dalle 12:00 alle 15:30: l’orario delle 13 sta comodo."),
    "battistero": dict(nome="Duomo e Battistero", lat=45.4065, lon=11.8709, card=True,
        testo="Il pezzo forte della giornata. Il <b>Battistero</b> è interamente affrescato da <b>Giusto de’ Menabuoi</b> (1375-78): "
              "un Paradiso di centinaia di figure sotto la cupola. È il grande sostituto della Cappella degli Scrovegni, "
              "e quasi sempre lo si ha per sé. Il biglietto comprende il Museo Diocesano e il Salone dei Vescovi.",
        nota="Turni ogni mezz’ora dalle 10:00 alle 17:30, con audioguida. Di sabato c’è anche la visita guidata "
             "in italiano alle 10:45 e alle 14:45."),
    "santo": dict(nome="Basilica del Santo", fonte=(u"Basilica del Santo", u"https://www.santantonio.org/it/basilica/orari"), lat=45.4014, lon=11.8809, card=True,
        testo="La basilica è gratuita: cupole orientali, il Donatello dell’altare maggiore, la Cappella del Santo. "
              "Fuori, il <b>Gattamelata</b>, primo monumento equestre in bronzo del Rinascimento. "
              "Accanto, l’<b>Oratorio di San Giorgio</b> con gli affreschi di Altichiero e la Scoletta del Santo.",
        nota="Basilica gratuita. Il biglietto è per Oratorio, Scoletta e Museo Antoniano, che <b>chiudono alle 18</b>: "
             "è la scadenza più stretta del pomeriggio."),
    "orto": dict(nome="Orto Botanico", fonte=(u"ortobotanico1545.it", u"https://ortobotanico1545.it/visita/orari/"), lat=45.3994, lon=11.8802, card=False,
        testo="Il <b>più antico orto botanico universitario del mondo</b> ancora nella sua posizione originale, 1545, patrimonio UNESCO. "
              "La palma di Goethe è lì dal 1585.",
        nota="Da aprile a settembre chiude alle 19, ultimo ingresso 18:15."),
    "prato": dict(nome="Prato della Valle", fonte=None, lat=45.3986, lon=11.8770, card=False,
        testo="La <b>piazza più grande d’Italia</b>: un’isola ellittica in un canale, 78 statue in doppio anello. "
              "Di sabato c’è il mercato, che smonta nel pomeriggio e lascia la piazza libera proprio all’ora giusta.",
        nota="Dalla fermata <b>Prato della Valle</b> il tram riporta in stazione in una dozzina di minuti. "
             "A piedi sono 2,5 km, circa mezz’ora."),
}

# ----------------------------------------------------------------- le due varianti
# (id, ora, durata, costo)  — costo None = niente biglietto
VARIANTE_A = dict(
    id="a", titolo=u"Con Palazzo del Bo", sigla=u"A",
    sommario=u"Il Teatro Anatomico costa 75 minuti e 12,00 €, e si prende il posto dell’Orto Botanico. "
             u"Resta comunque tutto il resto, Battistero compreso.",
    tappe=[
        ("stazione",   "09:30", "20 min per il centro", None),
        ("pedrocchi",  "09:50", "35 min",               "4,00 €"),
        ("bo",         "10:30", "75 min",               "12,00 €"),
        ("ragione",    "11:50", "45 min",               "8,00 €"),
        ("signori",    "12:35", "20 min",               "Gratuito"),
        ("pranzo",     "13:00", "90 min",               None),
        ("battistero", "14:30", "60 min",               "15,00 €"),
        ("santo",      "15:50", "80 min",               "10,00 €"),
        ("prato",      "17:25", "25 min",               "Gratuito"),
        ("stazione",   "17:55", "tram, 12 min",         None),
    ])
VARIANTE_B = dict(
    id="b", titolo=u"Senza Palazzo del Bo", sigla=u"B",
    sommario=u"Senza l’università la giornata respira: il Battistero passa la mattina, e nel pomeriggio "
             u"entra l’Orto Botanico. Costa anche 2,00 € in meno.",
    tappe=[
        ("stazione",   "09:30", "20 min per il centro", None),
        ("pedrocchi",  "09:55", "30 min",               "4,00 €"),
        ("ragione",    "10:30", "50 min",               "8,00 €"),
        ("signori",    "11:25", "20 min",               "Gratuito"),
        ("battistero", "11:50", "55 min",               "15,00 €"),
        ("pranzo",     "13:00", "90 min",               None),
        ("santo",      "14:45", "90 min",               "10,00 €"),
        ("orto",       "16:15", "60 min",               "10,00 €"),
        ("prato",      "17:20", "30 min",               "Gratuito"),
        ("stazione",   "17:55", "tram, 12 min",         None),
    ])
VARIANTE_ADA = dict(
    id="ada", titolo=u"Ada", sigla=u"★",
    sommario=u"Il Santo per primo, appena aprono i musei: è il momento in cui c’è meno gente. "
             u"Si va in tram direttamente lì, poi si risale in centro. Palazzo del Bo finisce <b>dopo pranzo</b>, "
             u"perché prima non ci sta (vedi la nota alla tappa).",
    tappe=[
        ("stazione",   "09:30", "tram, 20 min",         None),
        ("santo",      "09:50", "90 min",               "10,00 €"),
        ("pedrocchi",  "11:45", "40 min",               "4,00 €"),
        ("signori",    "12:35", "20 min",               "Gratuito"),
        ("pranzo",     "13:00", "90 min",               None),
        ("ragione",    "14:35", "45 min",               "8,00 €"),
        ("bo",         "15:30", "75 min",               "12,00 €"),
        ("prato",      "17:05", "30 min",               "Gratuito"),
        ("stazione",   "17:45", "tram, 12 min",         None),
    ])
VARIANTI = [VARIANTE_A, VARIANTE_B, VARIANTE_ADA]

# ordine di disegno del percorso sulla mappa (unione delle due varianti)
ORDINE_MAPPA = ["stazione", "pedrocchi", "bo", "ragione", "signori", "pranzo",
                "battistero", "santo", "orto", "prato"]

# ----------------------------------------------------------------- trasporto urbano
TRASPORTI = dict(
    biglietti=[
        (u"Biglietto ordinario urbano", u"1,70 €", u"zona arancio TU1, vale 90 minuti su bus e tram"),
        (u"Biglietto giornaliero", u"4,70 €", u"conviene solo da tre corse in su"),
        (u"Padova Urbs picta Card", u"compreso", u"i mezzi Busitalia sono inclusi nel prezzo della card"),
    ],
    dove=[
        (u"Biglietteria Busitalia in stazione", u"sabato e domenica 7:30–20:00, feriali 6:20–20:00",
         u"È l’opzione naturale: siete lì alle 9:30 ed è già aperta."),
        (u"Distributori automatici alle fermate del tram", u"sempre",
         u"Ce ne sono dodici, fra cui <b>Piazzale Stazione FS</b> e <b>Prato della Valle</b>: "
         u"le due fermate che userete."),
        (u"Tabaccai, edicole, bar", u"orari dei negozi",
         u"La rete più capillare, ma di sabato pomeriggio molti chiudono."),
        (u"Contactless a bordo", u"sempre",
         u"Si appoggia la carta al validatore e si paga 1,70 €. Niente code, niente app da installare: "
         u"per una giornata è il modo più semplice."),
        (u"App Busitalia Veneto, Trenitalia, DropTicket", u"sempre",
         u"Comodo se avete già una delle tre installate."),
    ],
    come=[
        (u"Contactless, il modo più rapido",
         u"Si appoggia la carta di credito o il telefono al <b>validatore giallo</b> appena saliti, "
         u"e si pagano 1,70 €. Non serve comprare nulla prima né installare niente. "
         u"Ogni persona deve appoggiare la propria carta: una carta sola non vale per due."),
        (u"Biglietto di carta",
         u"Va <b>obliterato a bordo</b> nella macchinetta appena saliti. Un biglietto non timbrato vale come "
         u"non averlo, ed è la multa più comune che prendono i turisti."),
        (u"App",
         u"Si compra e si <b>attiva prima di salire</b>: l’attivazione fa partire i 90 minuti."),
        (u"Quanto dura",
         u"<b>90 minuti dalla validazione</b>, con cambi liberi fra bus e tram. Per la vostra giornata "
         u"la corsa del mattino sarà scaduta da un pezzo quando tornate: servono due validazioni distinte."),
    ],
    consiglio=u"Per questa giornata servono <b>due corse</b>: stazione &rarr; centro la mattina, "
              u"Prato della Valle &rarr; stazione la sera. Sono <b>3,40 € a testa</b>, quindi il giornaliero da 4,70 € "
              u"non conviene. Se prendete la Padova Card, i mezzi sono già dentro e non comprate nulla. "
              u"La mattina si può anche andare a piedi in venti minuti: la corsa che serve davvero è quella del ritorno.",
)

# ----------------------------------------------------------------- tram SIR1
# fermate in centro, nell'ordine della linea (posizioni schematiche)
TRAM_FERMATE = [("Stazione FS", 45.4167, 11.8797), ("Trieste", 45.4133, 11.8791),
                ("Eremitani", 45.4110, 11.8781), ("Ponti Romani", 45.4085, 11.8772),
                ("Tito Livio", 45.4048, 11.8740), ("Santo", 45.4028, 11.8762),
                ("Prato della Valle", 45.3990, 11.8772), ("Santa Croce", 45.3960, 11.8778)]

# ----------------------------------------------------------------- tabella A: Padova Urbs picta Card
CARD_PREZZO = u"28,00 €"
CARD_SITI = [
    dict(nome="Cappella degli Scrovegni", fonte=(u"Musei Civici di Padova", u"https://padovamusei.it/it/biglietti-orari-musei"), lat=45.4118, lon=11.8795, dx=22, dy=-14,
         perche="Il ciclo di Giotto del 1305, il motivo per cui Padova è patrimonio UNESCO. "
                "<b>Escluso dal vostro programma</b> — resta qui perché è la voce che determina il prezzo della card.",
         orari="09:00–19:00, tutti i giorni<em>ingresso ogni 15 minuti su prenotazione</em>",
         prezzo="15,00 €<em>ridotto 11,00 €; comprende Musei Civici e Palazzo Zuckermann</em>",
         escluso=True),
    dict(nome="Battistero della Cattedrale", fonte=(u"Kalatà / Museo Diocesano", u"https://kalata.it/esperienza/battistero-padova/"), lat=45.4064, lon=11.8707, tappa="battistero",
         perche="Il <b>ciclo di Giusto de’ Menabuoi</b>, 1375-78: la vera alternativa a Giotto, e senza folla.",
         orari="Sab e dom 10:00–17:30 · mar–gio 10:00–17:30 · lun 14:00–17:30"
               "<em>turni ogni mezz’ora con audioguida; sabato visita guidata in italiano alle 10:45 e 14:45</em>",
         prezzo="15,00 €<em>ridotto 12,00 €; comprende Museo Diocesano e Salone dei Vescovi</em>"),
    dict(nome="Palazzo della Ragione", fonte=(u"Musei Civici di Padova", u"https://padovamusei.it/it/biglietti-orari-musei"), lat=45.4074, lon=11.8747, tappa="ragione",
         perche="Il Salone e il calendario astrologico affrescato, sopra le due piazze del mercato.",
         orari="09:00–19:00<em>chiuso il lunedì non festivo — il sabato è aperto</em>",
         prezzo="8,00 €<em>ridotto 6,00 €</em>"),
    dict(nome="Oratorio di San Giorgio", fonte=(u"Basilica del Santo", u"https://www.santantonio.org/it/content/orario-e-biglietto-unico-i-siti-museali-del-complesso-antoniano"), lat=45.4012, lon=11.8802, dx=-30, dy=22, tappa="santo",
         perche="Altichiero e Jacopo Avanzi, 1379-84: una cappella dipinta da cima a fondo, accanto alla Basilica.",
         orari="Mar–dom 09:00–13:00 e 14:00–18:00<em>chiuso il lunedì</em>",
         prezzo="10,00 €<em>ridotto 7,00 €; biglietto unico con Scoletta e Museo Antoniano</em>"),
    dict(nome="Basilica del Santo", fonte=(u"Basilica del Santo", u"https://www.santantonio.org/it/basilica/orari"), lat=45.4014, lon=11.8809, tappa="santo",
         perche="Le cappelle affrescate da Giusto de’ Menabuoi e Altichiero dentro la basilica. "
                "L’ingresso in chiesa è comunque libero.",
         orari="06:20–19:00 (estate fino alle 19:45)<em>aperta tutti i giorni</em>",
         prezzo="Gratuito<em>la card non serve per entrare in basilica</em>"),
    dict(nome="Chiesa degli Eremitani", fonte=None, lat=45.4110, lon=11.8786, dx=-32, dy=20,
         perche="Quel che resta del <b>Mantegna</b> della Cappella Ovetari, distrutta dalle bombe nel 1944 e ricomposta.",
         orari="Lun–ven 08:15–12:15 e 16:00–18:00, festivi ridotto<em>orari legati alle funzioni</em>",
         prezzo="Gratuito"),
    dict(nome="Oratorio di San Michele", fonte=(u"Musei Civici di Padova", u"https://padovamusei.it/it/biglietti-orari-musei"), lat=45.4059, lon=11.8695,
         perche="Gli affreschi di Jacopo da Verona, 1397. Piccolo, defilato, quasi sempre vuoto. "
                "Se avanza mezz’ora, è a due passi dal Duomo.",
         orari="Sab e dom mattina e pomeriggio · mar–ven 10:00–13:00<em>chiuso il lunedì</em>",
         prezzo="4,00 €<em>ridotto 3,50 €</em>"),
    dict(nome="Cappella della Reggia Carrarese", fonte=(u"turismopadova.it", u"https://www.turismopadova.it/accoglienza-in-citta/urbspictacard/"), lat=45.4085, lon=11.8732,
         perche="La cappella privata dei signori di Padova, affrescata da Guariento: il ciclo meno noto degli otto.",
         orari="Apertura limitata<em>verificare: spesso solo su prenotazione o in giorni stabiliti</em>",
         prezzo="Ingresso su prenotazione"),
]

# ----------------------------------------------------------------- tabella B: fuori card
ALTRI_LUOGHI = [
    dict(nome="Brutal", fonte=(u"OpenStreetMap", u"https://www.openstreetmap.org/?mlat=45.40742&mlon=11.87398#map=19/45.40742/11.87398"),
         lat=45.4074182, lon=11.8739796, dx=-14, dy=28, tipo="bar",
         perche="Cocktail bar in <b>Piazza dei Signori</b>, sotto la Torre dell’Orologio: è esattamente dove passa "
                "l’itinerario a metà mattina, e il posto giusto per la sosta prima di pranzo.",
         orari="Verificare sul posto o sui social del locale<em>orario non reperito da fonte ufficiale</em>",
         prezzo="—<em>Piazza dei Signori 2</em>"),
    dict(nome="All’Ombra della Piazza", fonte=(u"OpenStreetMap", u"https://www.openstreetmap.org/?mlat=45.40816&mlon=11.87504#map=19/45.40816/11.87504"),
         lat=45.4081590, lon=11.8750373, dx=18, dy=-14, tipo="bar",
         perche="In <b>Via Pietro d’Abano</b>, il vicolo fra Piazza della Frutta e Piazza dei Signori: due passi "
                "da Palazzo della Ragione, utile per lo spritz appena usciti dal Salone.",
         orari="Verificare sul posto o sui social del locale<em>orario non reperito da fonte ufficiale</em>",
         prezzo="—<em>Via Pietro d’Abano 16</em>"),
    dict(nome="Bacaro Padovano", fonte=(u"bacaropadovano.com", u"https://www.bacaropadovano.com/contatti/"), lat=45.40545, lon=11.87242, tipo="pasto", tappa="pranzo",
         perche="<b>Il pranzo prenotato.</b> Cicchetteria e cucina veneziana in Via San Gregorio Barbarigo, "
                "tre minuti dal Duomo e cinque da Piazza dei Signori.",
         orari="Ven e sab 12:00–15:30 e 19:00–24:00 · dom 12:00–15:30 · lun, mer, gio solo cena"
               "<em>chiuso il martedì; a pranzo apre solo ven, sab e dom</em>",
         prezzo="—<em>Via San Gregorio Barbarigo 3, tel. 049 8762777</em>"),
    dict(nome="Palazzo del Bo", fonte=(u"Università di Padova", u"https://www.unipd.it/palazzo-bo-900-gio-ponti-informazioni-tariffe"), lat=45.4069, lon=11.8772, tappa="bo",
         perche="Il <b>Teatro Anatomico del 1594</b>, il più antico conservato al mondo, la cattedra di Galileo e l’Aula Magna. "
                "Di sabato il giro è quello lungo e aggiunge l’ala novecentesca di Gio Ponti.",
         orari="<b>Sab, dom e festivi:</b> 9:30, 10:30, 11:30 (EN), 12:30, 14:30 (EN), 15:30, 16:30 (EN), 17:30 — 75 min<br>"
               "<b>Lun–ven:</b> 10:30, 11:30 (EN), 12:30, 15:30, 16:30 (EN), 17:30 — 45 min"
               "<em>prenotazione obbligatoria; chiuso 24, 25 e 31 dicembre e 1º gennaio</em>",
         prezzo="12,00 € il sabato<em>7,00 € nei giorni feriali; ridotti da 8,00 a 3,00 €</em>"),
    dict(nome="Caffè Pedrocchi — Piano Nobile", fonte=(u"Comune di Padova", u"https://padovaper.comune.padova.it/servizi/cultura-e-turismo/piano-nobile-dello-stabilimento-pedrocchi"), lat=45.4077, lon=11.8766, tappa="pedrocchi",
         perche="Le sale di Jappelli sopra il caffè, con il Museo del Risorgimento. Il modo giusto di cominciare la giornata.",
         orari="09:30–12:30 e 15:30–18:00<em>chiuso il lunedì non festivo — il sabato è aperto</em>",
         prezzo="4,00 €<em>ridotto 2,50 €; comprende il Museo del Risorgimento</em>"),
    dict(nome="Orto Botanico", fonte=(u"ortobotanico1545.it", u"https://ortobotanico1545.it/visita/orari/"), lat=45.3994, lon=11.8802, tappa="orto",
         perche="Il più antico orto botanico universitario del mondo ancora al suo posto, 1545, patrimonio UNESCO dal 1997. "
                "Nell’itinerario <b>B</b>, quello senza il Bo.",
         orari="Apr–set 10:00–19:00 · ott 10:00–18:00 · nov–mar 10:00–17:00"
               "<em>chiuso il lunedì; ultimo ingresso 45 minuti prima</em>",
         prezzo="10,00 €<em>8,00 € over 65; 6,00 € ridotto giovani</em>"),
    dict(nome="Prato della Valle", fonte=None, lat=45.3986, lon=11.8770, tappa="prato",
         perche="La piazza più grande d’Italia: isola ellittica, canale anulare, 78 statue. Di sabato c’è il mercato.",
         orari="Sempre accessibile<em>mercato il sabato, smonta nel pomeriggio</em>",
         prezzo="Gratuito"),
    dict(nome="Piazza dei Signori e Torre dell’Orologio", fonte=None, lat=45.4079, lon=11.8720, tappa="signori",
         perche="Il quadrante astronomico del 1344 e la Loggia del Consiglio.",
         orari="Piazza sempre accessibile<em>la torre si visita solo su prenotazione</em>",
         prezzo="Gratuito<em>salita alla torre a pagamento, su prenotazione</em>"),
    dict(nome="Duomo di Padova", fonte=None, lat=45.4065, lon=11.8711, tappa="battistero",
         perche="La cattedrale su progetto rimaneggiato di Michelangelo, austera e mai finita in facciata. "
                "È il portone accanto al Battistero.",
         orari="Lun–sab 07:30–12:00 e 15:45–19:30 · dom 07:45–13:00 e 15:45–20:30",
         prezzo="Gratuito"),
    dict(nome="Basilica di Santa Giustina", fonte=None, lat=45.3983, lon=11.8798,
         perche="Otto cupole affacciate sul Prato della Valle, il <b>Martirio di Santa Giustina</b> di Veronese "
                "e il pozzo dei martiri. Cinque minuti dal Prato, se avanza tempo prima del tram.",
         orari="Lun–sab 07:30–12:00 e 15:00–20:00 · dom 06:30–13:00 e 15:00–20:00",
         prezzo="Gratuito"),
    dict(nome="Musei Civici agli Eremitani", fonte=(u"Musei Civici di Padova", u"https://padovamusei.it/it/biglietti-orari-musei"), lat=45.4114, lon=11.8797, dx=-24, dy=16,
         perche="Archeologia e pinacoteca: Giotto, Bellini, Tiziano, Tiepolo. Si entra dallo stesso cortile della Cappella.",
         orari="09:00–19:00, tutti i giorni",
         prezzo="11,00 €<em>ridotto 9,00 €; 15,00 € con la Cappella degli Scrovegni</em>"),
    dict(nome="Palazzo Zuckermann", fonte=(u"Musei Civici di Padova", u"https://padovamusei.it/it/biglietti-orari-musei"), lat=45.4121, lon=11.8789,
         perche="Arti applicate e la collezione Bottacin di monete e medaglie, in un palazzo primo Novecento.",
         orari="Mar–dom 10:00–19:00<em>chiuso il lunedì</em>",
         prezzo="11,00 €<em>stesso biglietto dei Musei Civici</em>"),
    dict(nome="Loggia e Odeo Cornaro", fonte=(u"Musei Civici di Padova", u"https://padovamusei.it/it/biglietti-orari-musei"), lat=45.4037, lon=11.8827,
         perche="Il teatro privato rinascimentale di Alvise Cornaro, dove nacque il teatro del Ruzante. "
                "Poco visitato e a dieci minuti dal Santo.",
         orari="Sab e dom mattina e pomeriggio · mar–ven 10:00–13:00<em>chiuso il lunedì</em>",
         prezzo="5,00 €<em>ridotto 4,00 €</em>"),
    dict(nome="MUSME — Museo di Storia della Medicina", fonte=(u"musme.it", u"https://www.musme.it/pianifica-la-visita/"), lat=45.4042, lon=11.8797,
         perche="Museo interattivo nell’antico ospedale di San Francesco, dove la medicina padovana ha davvero cominciato.",
         orari="Sab e dom 09:30–19:00 · mar–ven 14:30–19:00<em>chiuso il lunedì</em>",
         prezzo="Circa 10,00 €<em>tariffa non verificata: controllare su musme.it/biglietteria</em>"),
]
