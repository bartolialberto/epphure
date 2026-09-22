# -*- coding: utf-8 -*-
"""Tutti i dati del sito "Un giorno a Padova" in un posto solo.

Orari e prezzi raccolti il 22 settembre 2026 dalle fonti ufficiali
(padovamusei.it, unipd.it, kalata.it, santantonio.org, ortobotanico1545.it,
turismopadova.it, bacaropadovano.com). Vanno riverificati prima di partire.
"""

# ----------------------------------------------------------------- l'itinerario
# n, ora, nome, coordinate, durata, cosa si fa, biglietto, avvertenza
ITINERARIO = [
    dict(n=1, ora="09:00", nome="Stazione FS", lat=45.4167, lon=11.8797, durata="20 min a piedi",
         testo="Si esce e si prende <b>Corso del Popolo</b>, che diventa Corso Garibaldi: un chilometro dritto fino al centro. "
               "Passa accanto agli Eremitani — la Cappella degli Scrovegni resta sulla sinistra, e la si saluta da fuori.",
         costo=None, card=False),
    dict(n=2, ora="09:20", nome="Caffè Pedrocchi", lat=45.4077, lon=11.8766, durata="45 min",
         testo="Il <b>caffè senza porte</b>, aperto giorno e notte per un secolo. Un caffè alla menta al banco, "
               "poi di sopra: il <b>Piano Nobile</b> di Jappelli è una sfilata di sale egizia, greca, etrusca, rinascimentale.",
         costo="4,00 €", card=False,
         nota="Il Piano Nobile apre alle 9:30: il quarto d’ora prima è esattamente quello del caffè."),
    dict(n=3, ora="10:15", nome="Palazzo del Bo", lat=45.4069, lon=11.8772, durata="45 min",
         testo="La sede storica dell’Università. Il <b>Teatro Anatomico del 1594</b>, il più antico al mondo ancora in piedi, "
               "la cattedra di Galileo, l’Aula Magna e la statua di Elena Lucrezia Cornaro Piscopia, prima laureata della storia.",
         costo="7,00 €", card=False,
         nota="Visita solo guidata, <b>prenotazione obbligatoria</b>. Il turno delle 10:30 è in italiano. Da lunedì a venerdì."),
    dict(n=4, ora="11:20", nome="Palazzo della Ragione", lat=45.4074, lon=11.8747, durata="55 min",
         testo="Il <b>Salone</b>: 80 metri di sala pensile senza colonne, sotto una carena di nave rovesciata, "
               "e attorno 333 riquadri affrescati con il calendario astrologico di Pietro d’Abano. Sotto, le due piazze del mercato.",
         costo="8,00 €", card=True),
    dict(n=5, ora="12:15", nome="Piazza dei Signori", lat=45.4079, lon=11.8720, durata="30 min",
         testo="La <b>Torre dell’Orologio</b> del 1344, con il quadrante astronomico che segna ore, fasi lunari e segni zodiacali "
               "— e che, per un errore diventato leggenda, la Bilancia non ce l’ha. Accanto, la Loggia del Consiglio.",
         costo="Gratuito", card=False),
    dict(n=6, ora="13:00", nome="Bacaro Padovano", lat=45.40545, lon=11.87242, durata="90 min",
         testo="Pranzo prenotato. Cicchetteria e cucina veneziana a due passi dal Duomo: dalla piazza si arriva in tre minuti.",
         costo="—", card=False, pasto=True,
         nota="A pranzo apre <b>solo venerdì, sabato e domenica</b>. Martedì chiuso tutto il giorno."),
    dict(n=7, ora="14:30", nome="Duomo e Battistero", lat=45.4065, lon=11.8709, durata="70 min",
         testo="Il pezzo forte della giornata. Il <b>Battistero</b> è interamente affrescato da <b>Giusto de’ Menabuoi</b> (1375-78): "
               "un Paradiso di centinaia di figure sotto la cupola. È il grande sostituto della Cappella degli Scrovegni, "
               "e quasi sempre lo si ha per sé. Il biglietto comprende il Museo Diocesano e il Salone dei Vescovi.",
         costo="15,00 €", card=True),
    dict(n=8, ora="15:45", nome="Basilica del Santo", lat=45.4014, lon=11.8809, durata="90 min",
         testo="La basilica è gratuita: cupole orientali, il Donatello dell’altare maggiore, la Cappella del Santo. "
               "Fuori, il <b>Gattamelata</b>, primo monumento equestre in bronzo del Rinascimento. "
               "Accanto, l’<b>Oratorio di San Giorgio</b> con gli affreschi di Altichiero e la Scoletta del Santo.",
         costo="10,00 €", card=True,
         nota="Basilica gratuita. Il biglietto è per Oratorio, Scoletta e Museo Antoniano, che chiudono alle 18."),
    dict(n=9, ora="17:15", nome="Orto Botanico", lat=45.3994, lon=11.8802, durata="60 min",
         testo="Il <b>più antico orto botanico universitario del mondo</b> ancora nella sua posizione originale, 1545, patrimonio UNESCO. "
               "La palma di Goethe è lì dal 1585.",
         costo="10,00 €", card=False,
         nota="Da aprile a settembre chiude alle 19, ultimo ingresso 18:15. Chiuso il lunedì."),
    dict(n=10, ora="18:15", nome="Prato della Valle", lat=45.3986, lon=11.8770, durata="30 min",
         testo="La <b>piazza più grande d’Italia</b>: un’isola ellittica in un canale, 78 statue in doppio anello, "
               "e la luce di fine giornata che è il momento giusto. Poi il tram dalla fermata Prato della Valle riporta in stazione in dieci minuti.",
         costo="Gratuito", card=False),
]

# ----------------------------------------------------------------- tabella A: Padova Urbs picta Card
CARD_PREZZO = u"28,00 €"
CARD_SITI = [
    dict(nome="Cappella degli Scrovegni", lat=45.4118, lon=11.8795, dx=22, dy=-14,
         perche="Il ciclo di Giotto del 1305, il motivo per cui Padova è patrimonio UNESCO. "
                "<b>Escluso dal vostro programma</b> — resta qui perché è il cuore economico della card.",
         orari="09:00–19:00, tutti i giorni<em>ingresso ogni 15 minuti su prenotazione</em>",
         prezzo="15,00 €<em>ridotto 11,00 €; comprende Musei Civici e Palazzo Zuckermann</em>",
         escluso=True),
    dict(nome="Battistero della Cattedrale", lat=45.4064, lon=11.8707,
         perche="Il <b>ciclo di Giusto de’ Menabuoi</b>, 1375-78: la vera alternativa a Giotto, e senza folla. "
                "Tappa n. 7 dell’itinerario.",
         orari="Mar–dom 10:00–17:30, lunedì 14:00–17:30<em>turni ogni mezz’ora, con audioguida</em>",
         prezzo="15,00 €<em>ridotto 12,00 €; comprende Museo Diocesano e Salone dei Vescovi</em>"),
    dict(nome="Palazzo della Ragione", lat=45.4074, lon=11.8747,
         perche="Il Salone e il calendario astrologico affrescato. Tappa n. 4 dell’itinerario.",
         orari="09:00–19:00<em>chiuso il lunedì non festivo</em>",
         prezzo="8,00 €<em>ridotto 6,00 €</em>"),
    dict(nome="Oratorio di San Giorgio", lat=45.4012, lon=11.8802, dx=-30, dy=22,
         perche="Altichiero e Jacopo Avanzi, 1379-84: una cappella dipinta da cima a fondo, accanto alla Basilica. "
                "Parte della tappa n. 8.",
         orari="Mar–dom 09:00–13:00 e 14:00–18:00<em>chiuso il lunedì</em>",
         prezzo="10,00 €<em>ridotto 7,00 €; biglietto unico con Scoletta e Museo Antoniano</em>"),
    dict(nome="Basilica del Santo", lat=45.4014, lon=11.8809,
         perche="Le cappelle affrescate da Giusto de’ Menabuoi e Altichiero dentro la basilica. "
                "L’ingresso in chiesa è comunque libero. Tappa n. 8.",
         orari="06:20–19:00 (estate fino alle 19:45)<em>aperta tutti i giorni</em>",
         prezzo="Gratuito<em>la card non serve per entrare in basilica</em>"),
    dict(nome="Chiesa degli Eremitani", lat=45.4110, lon=11.8786, dx=-32, dy=20,
         perche="Quel che resta del <b>Mantegna</b> della Cappella Ovetari, distrutta dalle bombe nel 1944 e ricomposta.",
         orari="Lun–ven 08:15–12:15 e 16:00–18:00, festivi ridotto<em>orari legati alle funzioni</em>",
         prezzo="Gratuito"),
    dict(nome="Oratorio di San Michele", lat=45.4059, lon=11.8695,
         perche="Gli affreschi di Jacopo da Verona, 1397. Piccolo, defilato, quasi sempre vuoto.",
         orari="Mar–ven 10:00–13:00, sab–dom anche pomeriggio<em>chiuso il lunedì</em>",
         prezzo="4,00 €<em>ridotto 3,50 €</em>"),
    dict(nome="Cappella della Reggia Carrarese", lat=45.4085, lon=11.8732,
         perche="La cappella privata dei signori di Padova, affrescata da Guariento: il ciclo meno noto degli otto.",
         orari="Apertura limitata<em>verificare: spesso solo su prenotazione o in giorni stabiliti</em>",
         prezzo="Ingresso su prenotazione"),
]

# ----------------------------------------------------------------- tabella B: fuori card
ALTRI_LUOGHI = [
    dict(nome="Bacaro Padovano", lat=45.40545, lon=11.87242, tipo="pasto",
         perche="<b>Il pranzo prenotato</b>, tappa n. 6. Cicchetteria e cucina veneziana in Via San Gregorio Barbarigo, "
                "tre minuti dal Duomo e cinque da Piazza dei Signori.",
         orari="Ven e sab 12:00–15:30 e 19:00–24:00 · dom 12:00–15:30 · lun, mer, gio solo cena"
               "<em>chiuso il martedì; a pranzo apre solo ven, sab e dom</em>",
         prezzo="—<em>Via San Gregorio Barbarigo 3, tel. 049 8762777</em>"),
    dict(nome="Palazzo del Bo", lat=45.4069, lon=11.8772,
         perche="Il <b>Teatro Anatomico del 1594</b>, il più antico conservato al mondo, la cattedra di Galileo e l’Aula Magna. "
                "Tappa n. 3. Nel fine settimana il giro cambia e include l’ala di Gio Ponti.",
         orari="Giro storico lun–ven: 10:30, 11:30 (EN), 12:30, 15:30, 16:30 (EN), 17:30<em>45 minuti, "
               "prenotazione obbligatoria; sab e dom tour “Gio Ponti”</em>",
         prezzo="7,00 €<em>3,00 € per 13-25 anni; 5,00 € over 65</em>"),
    dict(nome="Caffè Pedrocchi — Piano Nobile", lat=45.4077, lon=11.8766,
         perche="Le sale di Jappelli sopra il caffè, con il Museo del Risorgimento. Tappa n. 2, "
                "e il modo giusto di cominciare la giornata.",
         orari="09:30–12:30 e 15:30–18:00<em>chiuso il lunedì non festivo</em>",
         prezzo="4,00 €<em>ridotto 2,50 €; comprende il Museo del Risorgimento</em>"),
    dict(nome="Orto Botanico", lat=45.3994, lon=11.8802,
         perche="Il più antico orto botanico universitario del mondo ancora al suo posto, 1545, patrimonio UNESCO dal 1997. "
                "Tappa n. 9.",
         orari="Apr–set 10:00–19:00 · ott 10:00–18:00 · nov–mar 10:00–17:00"
               "<em>chiuso il lunedì; ultimo ingresso 45 minuti prima</em>",
         prezzo="10,00 €<em>8,00 € over 65; 6,00 € ridotto giovani</em>"),
    dict(nome="Prato della Valle", lat=45.3986, lon=11.8770,
         perche="La piazza più grande d’Italia: isola ellittica, canale anulare, 78 statue. Tappa n. 10, al tramonto.",
         orari="Sempre accessibile<em>il sabato ospita il mercato</em>",
         prezzo="Gratuito"),
    dict(nome="Piazza dei Signori e Torre dell’Orologio", lat=45.4079, lon=11.8720,
         perche="Il quadrante astronomico del 1344 e la Loggia del Consiglio. Tappa n. 5.",
         orari="Piazza sempre accessibile<em>la torre si visita solo su prenotazione</em>",
         prezzo="Gratuito<em>salita alla torre a pagamento, su prenotazione</em>"),
    dict(nome="Duomo di Padova", lat=45.4065, lon=11.8711,
         perche="La cattedrale su progetto rimaneggiato di Michelangelo, austera e mai finita in facciata. "
                "È il portone accanto al Battistero, tappa n. 7.",
         orari="Lun–sab 07:30–12:00 e 15:45–19:30 · dom 07:45–13:00 e 15:45–20:30",
         prezzo="Gratuito"),
    dict(nome="Basilica di Santa Giustina", lat=45.3983, lon=11.8798,
         perche="Otto cupole affacciate sul Prato della Valle, il <b>Martirio di Santa Giustina</b> di Veronese "
                "e il pozzo dei martiri. Cinque minuti dalla tappa n. 10.",
         orari="Lun–sab 07:30–12:00 e 15:00–20:00 · dom 06:30–13:00 e 15:00–20:00",
         prezzo="Gratuito"),
    dict(nome="Musei Civici agli Eremitani", lat=45.4114, lon=11.8797, dx=-24, dy=16,
         perche="Archeologia e pinacoteca: Giotto, Bellini, Tiziano, Tiepolo. Si entra dallo stesso cortile della Cappella.",
         orari="09:00–19:00, tutti i giorni",
         prezzo="11,00 €<em>ridotto 9,00 €; 15,00 € con la Cappella degli Scrovegni</em>"),
    dict(nome="Palazzo Zuckermann", lat=45.4121, lon=11.8789,
         perche="Arti applicate e la collezione Bottacin di monete e medaglie, in un palazzo primo Novecento.",
         orari="Mar–dom 10:00–19:00<em>chiuso il lunedì</em>",
         prezzo="11,00 €<em>stesso biglietto dei Musei Civici</em>"),
    dict(nome="Loggia e Odeo Cornaro", lat=45.4037, lon=11.8827,
         perche="Il teatro privato rinascimentale di Alvise Cornaro, dove nacque il teatro del Ruzante. "
                "Poco visitato e a dieci minuti dal Santo.",
         orari="Mar–ven 10:00–13:00, sab e dom anche pomeriggio<em>chiuso il lunedì</em>",
         prezzo="5,00 €<em>ridotto 4,00 €</em>"),
    dict(nome="MUSME — Museo di Storia della Medicina", lat=45.4042, lon=11.8797,
         perche="Museo interattivo nell’antico ospedale di San Francesco, dove la medicina padovana ha davvero cominciato.",
         orari="Mar–ven 14:30–19:00 · sab e dom 09:30–19:00<em>chiuso il lunedì</em>",
         prezzo="10,00 €<em>ridotto 8,00 €</em>"),
]

# ----------------------------------------------------------------- il conto
CONTI = dict(
    singoli=[("Caffè Pedrocchi, Piano Nobile", 4), ("Palazzo del Bo", 7),
             ("Palazzo della Ragione", 8), ("Battistero della Cattedrale", 15),
             ("Oratorio di San Giorgio e Scoletta", 10), ("Orto Botanico", 10)],
    con_card=[("Padova Urbs picta Card 48 ore", 28), ("Caffè Pedrocchi, Piano Nobile", 4),
              ("Palazzo del Bo", 7), ("Orto Botanico", 10)],
)
