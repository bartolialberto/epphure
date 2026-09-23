# -*- coding: utf-8 -*-
"""Le quattro pagine del sito."""
import io, os, re
from _build import page, nav, write, build_map, MAP_CSS, VW, VH, eur, extra_markers, NUM
from _data import (PLACES, VARIANTI, VARIANTE_A, VARIANTE_B, VARIANTE_ADA, ORDINE_MAPPA, RIGHE_TAPPA,
                   PRIMA,
                   CARD_SITI, ALTRI_LUOGHI, CARD_PREZZO, TRASPORTI, GIORNO, ARRIVO, RIENTRO,
                   TRAM_FERMATE)

CARD_N = 28.0
BIGLIETTO_CORSA = 1.70


def num(costo):
    if not costo:
        return 0.0
    m = re.match(r'^(\d+),(\d+)', costo)
    return float("%s.%s" % (m.group(1), m.group(2))) if m else 0.0


def conti(v):
    """(voci singoli, totale singoli, voci con card, totale con card)"""
    singoli, concard = [], [(u"Padova Urbs picta Card 48 ore", CARD_N)]
    visti = set()
    for pid, _o, _d, costo in v['tappe']:
        c = num(costo)
        if c and pid not in visti:
            visti.add(pid)
            singoli.append((PLACES[pid]['nome'], c))
            if not PLACES[pid]['card']:
                concard.append((PLACES[pid]['nome'], c))
    singoli.append((u"Trasporto urbano, due corse", 2 * BIGLIETTO_CORSA))
    concard.append((u"Trasporto urbano", 0.0))
    return singoli, sum(c for _, c in singoli), concard, sum(c for _, c in concard)


FOOT = u"""  <footer>
    <p><b>Orari e prezzi raccolti il 22 settembre 2026</b> dai siti ufficiali. Ogni riga delle due tabelle
    porta il link alla fonte da cui viene il dato, cos&igrave; potete controllare voi;
    dove la fonte manca l&rsquo;ho scritto invece di inventarla.</p>
    <p>Due visite di questa giornata &mdash; <b>Palazzo del Bo</b> e il <b>Battistero</b> &mdash; vogliono la prenotazione.
    La Cappella degli Scrovegni non fa parte del programma per vostra scelta: resta nella tabella della card
    perch&eacute; &egrave; la voce che ne determina il prezzo.</p>
  </footer>"""

# =========================================================== 1. la giornata
INDEX_CSS = u"""
.mapcard{display:grid;grid-template-columns:minmax(0,1fr) 190px;gap:22px;align-items:center;
  background:var(--surface);border:1px solid var(--rule);border-radius:4px;padding:20px 22px;
  margin-bottom:12px;text-decoration:none;color:inherit;box-shadow:var(--shadow);
  transition:border-color .15s,transform .15s}
.mapcard:hover{border-color:var(--ink-faint);transform:translateY(-1px)}
.mapcard:focus-visible{outline:2px solid var(--card);outline-offset:3px}
@media (max-width:620px){.mapcard{grid-template-columns:1fr;gap:16px}
  .mapcard .thumb{order:-1;max-width:170px;margin-inline:auto}}
.mapcard .thumb{line-height:0;border-radius:3px;overflow:hidden;border:1px solid var(--rule)}
.mapcard .thumb svg{display:block;width:100%;height:auto}
.cardrow{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:0 0 36px}
@media (max-width:700px){.cardrow{grid-template-columns:1fr}}
.linkcard{display:flex;flex-direction:column;background:var(--surface);border:1px solid var(--rule);
  border-radius:4px;padding:18px 20px;text-decoration:none;color:inherit;box-shadow:var(--shadow);
  transition:border-color .15s,transform .15s}
.linkcard:hover{border-color:var(--ink-faint);transform:translateY(-1px)}
.linkcard:focus-visible{outline:2px solid var(--card);outline-offset:3px}
.kicker{font-size:11.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--ink-faint);
  font-weight:700;margin:0 0 7px}
.mapcard h2,.linkcard h2{margin:0;font-family:'EB Garamond',Garamond,serif;font-weight:600;
  font-size:26px;line-height:1.1;letter-spacing:-.005em}
.linkcard h2{font-size:23px}
.mapcard p,.linkcard p{margin:9px 0 0;font-size:14.5px;color:var(--ink-soft);line-height:1.45}
.linkcard p{flex:1}
.marks{display:flex;gap:7px;margin-top:15px;align-self:flex-start}
.marks i{width:19px;height:19px;border-radius:50%;background:var(--c);display:block;flex:none}
.marks i.dia{border-radius:0;width:21px;height:21px;clip-path:polygon(50% 0%,100% 50%,50% 100%,0% 50%)}
.go{margin-top:12px;align-self:flex-start;font-size:13.5px;font-weight:600;
  color:var(--route);letter-spacing:.02em}

.sechead{display:flex;align-items:baseline;gap:12px;padding-bottom:9px;
  border-bottom:2px solid var(--ink);margin:0 0 4px}
.sechead h2{margin:0;font-family:'Jost',sans-serif;font-size:12.5px;font-weight:700;
  letter-spacing:.15em;text-transform:uppercase}
.sechead .cnt{margin-left:auto;font-size:12.5px;color:var(--ink-faint);text-align:right}

/* --- lo scambio fra i due itinerari --- */
.switch{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:22px 0 26px}
@media (max-width:860px){.switch{grid-template-columns:1fr}}
.switch button{display:block;text-align:left;font-family:inherit;cursor:pointer;
  background:var(--surface);border:1px solid var(--rule);border-radius:4px;padding:15px 17px;
  color:inherit;transition:border-color .15s,background .15s}
.switch button:hover{border-color:var(--ink-faint)}
.switch button:focus-visible{outline:2px solid var(--route);outline-offset:3px}
.switch button[aria-pressed="true"]{border-color:var(--route);border-width:2px;padding:14px 16px;
  background:var(--surface-2)}
.switch .sig{display:inline-flex;align-items:center;justify-content:center;width:26px;height:26px;
  border-radius:50%;background:var(--ink-faint);color:var(--marker-ring);font-size:13px;
  font-weight:700;margin-right:9px;vertical-align:-6px}
.switch button[aria-pressed="true"] .sig{background:var(--route)}
.switch .tit{font-family:'EB Garamond',Garamond,serif;font-size:22px;font-weight:600;line-height:1.1}
.switch .det{margin:9px 0 0;font-size:13.5px;color:var(--ink-soft);line-height:1.45}
.switch .cost{margin:9px 0 0;font-size:12.5px;color:var(--ink-faint);font-variant-numeric:tabular-nums}
.switch .cost b{color:var(--ink);font-weight:600}

.introtab{margin:12px 0 14px;font-size:13.5px;color:var(--ink-faint)}
.tablebox{overflow-x:auto;border:1px solid var(--rule);border-radius:4px;background:var(--surface);
  box-shadow:var(--shadow);margin:0 0 34px}
.tablebox table{width:100%;border-collapse:collapse;min-width:1080px}
.tablebox thead th{background:var(--surface-2);text-align:left;font-size:11px;font-weight:700;
  letter-spacing:.14em;text-transform:uppercase;color:var(--ink-faint);
  padding:12px 14px;border-bottom:2px solid var(--ink)}
.tablebox td{padding:16px 14px;border-bottom:1px solid var(--rule-soft);vertical-align:top}
.tablebox tbody tr:last-child td{border-bottom:0}
.tablebox tbody tr:hover{background:var(--surface-2)}
.tablebox tr.seguito td{border-top:0;padding-top:0}
.tablebox tr.seguito .c-ora{border-left:2px solid var(--rule-soft)}
.tablebox tr.partenza,.tablebox tr.chiusura{background:var(--surface-2)}
.c-ora{width:86px;min-width:80px}
.c-ora .ora{display:block;font-size:15px;font-weight:600;font-variant-numeric:tabular-nums}
.c-ora .tappa{display:inline-flex;align-items:center;justify-content:center;width:23px;height:23px;
  border-radius:50%;background:var(--c,var(--route));color:var(--marker-ring);
  font-size:11.5px;font-weight:700;margin-top:7px}
.c-ora .dur{display:block;margin-top:6px;font-size:11.5px;color:var(--ink-faint)}
.quando{display:block;margin-top:9px;padding-left:11px;border-left:2px solid var(--rule);
  font-size:12.5px;color:var(--ink-faint);line-height:1.5}
.quando b{color:var(--ink-soft)}
.stop{display:grid;grid-template-columns:62px 38px minmax(0,1fr);gap:0 14px;
  padding:18px 0 20px;border-bottom:1px solid var(--rule-soft)}
.stop > *{grid-column:3}
.stop .ora{grid-column:1;grid-row:1;font-size:15px;font-weight:600;
  font-variant-numeric:tabular-nums;color:var(--ink);letter-spacing:.01em;padding-top:3px}
.stop .bullet{grid-column:2;grid-row:1/span 8;display:flex;justify-content:center;position:relative}
@media (max-width:620px){
  .stop{grid-template-columns:38px minmax(0,1fr)}
  .stop > *{grid-column:2}
  .stop .ora{grid-column:2;grid-row:1;padding-top:0;margin-bottom:5px}
  .stop .bullet{grid-column:1;grid-row:1/span 8}
}
.stop .bullet span{width:32px;height:32px;border-radius:50%;background:var(--c,var(--route));
  color:var(--marker-ring);display:flex;align-items:center;justify-content:center;
  font-size:14.5px;font-weight:600;font-variant-numeric:tabular-nums;z-index:1;margin-top:1px}
.stop.ritorno .bullet span{background:var(--surface);color:var(--ink-faint);
  border:2px dashed var(--rule);font-size:13px}
.stop .bullet::after{content:"";position:absolute;top:34px;bottom:-22px;width:2px;
  background:var(--rule);left:50%;transform:translateX(-50%)}
.stop:last-child .bullet::after{display:none}
.stop h3{margin:0;font-family:'EB Garamond',Garamond,serif;font-weight:600;
  font-size:23px;line-height:1.15;letter-spacing:-.005em}
.stop .meta{display:flex;flex-wrap:wrap;gap:7px;align-items:center;margin-top:7px}
.pill{font-size:11.5px;font-weight:600;letter-spacing:.07em;text-transform:uppercase;
  border:1px solid var(--rule);border-radius:3px;padding:2px 8px;color:var(--ink-soft)}
.pill.price{border-color:var(--route);color:var(--route)}
.pill.free{border-color:var(--other);color:var(--other)}
.pill.incard{border-color:var(--card);color:var(--card)}
.stop p.testo{margin:10px 0 0;font-size:15px;color:var(--ink-soft);line-height:1.55;max-width:62ch}
.stop p.nota{margin:11px 0 0;font-size:13.5px;color:var(--ink-faint);line-height:1.5;
  border-left:2px solid var(--rule);padding-left:12px;max-width:62ch}
.stop p.nota + p.nota{margin-top:8px}
.stop p.nota b{color:var(--ink-soft)}

.c-nome{width:16%;min-width:150px;font-family:'EB Garamond',Garamond,serif;
  font-weight:600;font-size:19px;line-height:1.16}
.c-perche{width:28%;min-width:240px;font-size:14px;color:var(--ink-soft);line-height:1.5}
.c-perche b{color:var(--ink);font-weight:600}
.c-orari{width:22%;min-width:195px;font-size:13.5px;color:var(--ink-soft);line-height:1.45}
.c-prezzo{width:14%;min-width:140px;font-size:15.5px;font-weight:600;font-variant-numeric:tabular-nums}
.c-fonte{width:12%;min-width:130px;font-size:13px}
.c-fonte a{display:block;color:var(--card);text-underline-offset:3px}
.c-fonte a.wiki{margin-top:6px;color:var(--ink-faint);font-size:12.5px}
.c-fonte a:hover{color:var(--ink)}
.c-fonte .none{display:inline-block;font-size:10.5px;font-weight:700;letter-spacing:.08em;
  text-transform:uppercase;color:var(--ink-faint);border:1px solid var(--rule);
  border-radius:3px;padding:2px 7px;line-height:1.5}
.c-fonte .why{display:block;margin-top:6px;font-size:12px;color:var(--ink-faint);line-height:1.4}
.c-orari em,.c-prezzo em{display:block;font-style:normal;font-weight:400;font-size:12.5px;
  color:var(--ink-faint);margin-top:5px;line-height:1.45}
@media (max-width:1040px){
  .tablebox{overflow-x:visible;border:0;border-radius:0;background:transparent;box-shadow:none}
  .tablebox table{min-width:0}
  .tablebox thead{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}
  .tablebox tbody tr{display:block;background:var(--surface);border:1px solid var(--rule);
    border-radius:4px;padding:16px 17px;margin-bottom:12px;box-shadow:var(--shadow)}
  .tablebox tbody tr.seguito{margin-top:-8px;border-top-left-radius:0;border-top-right-radius:0}
  .tablebox tbody tr:hover{background:var(--surface)}
  .tablebox td{display:block;width:auto!important;min-width:0!important;padding:0;border:0!important}
  .tablebox .c-ora{margin-bottom:9px}
  .tablebox .c-ora .ora,.tablebox .c-ora .tappa,.tablebox .c-ora .dur{display:inline-flex;
    vertical-align:middle;margin:0 9px 0 0}
  .c-perche,.c-orari,.c-prezzo,.c-fonte{margin-top:12px}
  .c-perche::before,.c-orari::before,.c-prezzo::before,.c-fonte::before{content:attr(data-l);
    display:block;font-size:10px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;
    color:var(--ink-faint);margin-bottom:4px}
}
.conti{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:18px 0 20px}
@media (max-width:640px){.conti{grid-template-columns:1fr}}
.conto{background:var(--surface);border:1px solid var(--rule);border-radius:4px;padding:17px 19px}
.conto.win{border-color:var(--card);border-width:2px;padding:16px 18px}
.conto h3{margin:0 0 3px;font-family:'Jost',sans-serif;font-size:12px;font-weight:700;
  letter-spacing:.14em;text-transform:uppercase;color:var(--ink-faint)}
.conto .sub{margin:0;font-size:13px;color:var(--ink-soft)}
.conto ul{list-style:none;margin:12px 0 0;padding:0}
.conto li{display:flex;justify-content:space-between;gap:12px;font-size:14px;
  padding:5px 0;border-bottom:1px solid var(--rule-soft);color:var(--ink-soft)}
.conto li span:last-child{font-variant-numeric:tabular-nums;white-space:nowrap;color:var(--ink)}
.conto .tot{display:flex;justify-content:space-between;align-items:baseline;gap:12px;
  margin-top:12px;padding-top:11px;border-top:2px solid var(--ink)}
.conto .tot b{font-family:'Jost',sans-serif;font-size:12px;font-weight:700;
  letter-spacing:.14em;text-transform:uppercase;color:var(--ink-faint)}
.conto .tot em{font-style:normal;font-family:'EB Garamond',Garamond,serif;
  font-size:30px;font-weight:600;font-variant-numeric:tabular-nums}
.verdetto{border-left:3px solid var(--card);background:var(--surface-2);padding:14px 17px;
  border-radius:0 3px 3px 0;margin:0 0 38px;font-size:14.5px;color:var(--ink-soft);line-height:1.55}
.verdetto b{color:var(--ink);font-weight:600}

/* --- trasporto urbano --- */
.tickets{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:18px 0 22px}
@media (max-width:640px){.tickets{grid-template-columns:1fr}}
.tick{background:var(--surface);border:1px solid var(--rule);border-radius:4px;padding:15px 17px}
.tick .lab{font-size:11px;letter-spacing:.13em;text-transform:uppercase;font-weight:700;
  color:var(--ink-faint);margin:0}
.tick .val{margin:6px 0 0;font-family:'EB Garamond',Garamond,serif;font-size:27px;
  font-weight:600;font-variant-numeric:tabular-nums;line-height:1}
.tick .det{margin:6px 0 0;font-size:12.5px;color:var(--ink-soft);line-height:1.4}
.dove{list-style:none;margin:0 0 20px;padding:0}
.dove li{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:2px 14px;
  padding:13px 2px;border-bottom:1px solid var(--rule-soft)}
.dove .n{font-size:15px;font-weight:600;color:var(--ink)}
.dove .q{font-size:12.5px;color:var(--ink-faint);font-variant-numeric:tabular-nums;text-align:right;white-space:nowrap}
@media (max-width:560px){.dove li{grid-template-columns:1fr}.dove .q{text-align:left}}
.dove .d{grid-column:1/-1;margin:5px 0 0;font-size:13.5px;color:var(--ink-soft);line-height:1.5}
.dove .d b{color:var(--ink)}
"""


RIGA_PER_NOME = {}
for _lista in (CARD_SITI, ALTRI_LUOGHI):
    for _r in _lista:
        RIGA_PER_NOME[_r['nome']] = _r


def tabella_itinerario(v):
    """Le stesse righe delle due tabelle di riferimento, nell'ordine dell'itinerario."""
    out, visti = [], set()
    for pid, ora, durata, costo in v['tappe']:
        pl = PLACES[pid]
        ritorno = pid in visti
        visti.add(pid)
        n = NUM[pid][v['id']]
        col = 'var(--food)' if pl.get('pasto') else 'var(--route)'

        if ritorno:
            out.append(
                u'        <tr class="chiusura">\n'
                u'          <td class="c-ora"><span class="ora">%s</span></td>\n'
                u'          <td class="c-nome">Ritorno in stazione</td>\n'
                u'          <td class="c-perche" colspan="4">Dalla fermata <b>Prato della Valle</b> il tram SIR1 '
                u'riporta al piazzale della stazione in una dozzina di minuti: si arriva verso le <b>18:10</b>, '
                u'con dieci minuti di margine. A piedi sono 2,5 km e mezz\u2019ora.</td>\n'
                u'        </tr>' % ora)
            continue

        righe = [RIGA_PER_NOME[nm] for nm in RIGHE_TAPPA.get(pid, []) if nm in RIGA_PER_NOME]
        if not righe:      # la stazione non ha una riga di tabella
            out.append(
                u'        <tr class="partenza">\n'
                u'          <td class="c-ora"><span class="ora">%s</span>'
                u'<span class="tappa" style="--c:%s">%d</span></td>\n'
                u'          <td class="c-nome">%s</td>\n'
                u'          <td class="c-perche" colspan="4">%s</td>\n'
                u'        </tr>' % (ora, col, n, pl['nome'], pl['testo']))
            continue

        for k, r in enumerate(righe):
            perche = r['perche']
            if k == 0:
                extra = []
                if pl.get('nota'):
                    extra.append(pl['nota'])
                if v['id'] == 'ada' and pl.get('nota_ada'):
                    extra.append(pl['nota_ada'])
                for e in extra:
                    perche += u'<span class="quando">%s</span>' % e
            prima = (u'<span class="ora">%s</span><span class="tappa" style="--c:%s">%d</span>'
                     u'<span class="dur">%s</span>' % (ora, col, n, durata)) if k == 0 else u''
            out.append(
                u'        <tr%s>\n'
                u'          <td class="c-ora">%s</td>\n'
                u'          <td class="c-nome">%s</td>\n'
                u'          <td class="c-perche" data-l="Perch&eacute; conta">%s</td>\n'
                u'          <td class="c-orari" data-l="Orari e chiusura">%s</td>\n'
                u'          <td class="c-prezzo" data-l="Prezzo senza card">%s</td>\n'
                u'          <td class="c-fonte" data-l="Fonte">%s</td>\n'
                u'        </tr>' % (u' class="seguito"' if k else u'', prima, r['nome'],
                                    perche, r['orari'], r['prezzo'], cella_fonte(r)))
    return (u'    <div class="tablebox"><table>\n'
            u'      <thead><tr><th>Ora</th><th>Nome</th><th>Perch&eacute; conta</th>'
            u'<th>Orari e giorno di chiusura</th><th>Prezzo senza card</th><th>Fonte</th></tr></thead>\n'
            u'      <tbody>\n%s\n      </tbody>\n    </table></div>' % u'\n'.join(out))


def blocco_conti(v):
    sing, tot_s, card, tot_c = conti(v)

    def box(titolo, sub, righe, tot, win=False):
        li = u''.join(u'<li><span>%s</span><span>%s</span></li>'
                      % (n, u'compreso' if c == 0 else eur(c)) for n, c in righe)
        return (u'      <div class="conto%s"><h3>%s</h3><p class="sub">%s</p><ul>%s</ul>'
                u'<div class="tot"><b>Totale</b><em>%s</em></div></div>'
                % (u' win' if win else u'', titolo, sub, li, eur(tot)))
    return (u'    <div class="conti">\n%s\n%s\n    </div>'
            % (box(u"Biglietti singoli", u"pagando ogni ingresso, più il tram", sing, tot_s),
               box(u"Con la Padova Card", u"la card copre Ragione, Battistero, Oratorio e i mezzi",
                   card, tot_c, win=tot_c < tot_s)),
            tot_s, tot_c)


def verdetto(v):
    _s, ts, _c, tc = conti(v)
    d = ts - tc
    if d > 0:
        return (u'    <p class="verdetto"><b>Con la card risparmiate %s.</b> Non tanto per gli ingressi '
                u'&mdash; senza gli Scrovegni il margine sarebbe sottile &mdash; quanto perch&eacute; la card '
                u'comprende <b>i mezzi</b>, e la corsa di ritorno vi serve davvero. Conviene ancora di pi&ugrave; '
                u'se ci aggiungete un altro sito compreso: l&rsquo;Oratorio di San Michele, la Chiesa degli '
                u'Eremitani, i Musei Civici.</p>' % eur(d))
    return (u'    <p class="verdetto" style="border-left-color:var(--route)"><b>Qui la card non conviene: '
            u'costereste %s in pi&ugrave;.</b> Questo itinerario tocca un solo sito compreso nella card oltre '
            u'al Santo, e spende invece parecchio fuori card (Palazzo del Bo, il Pedrocchi). '
            u'Con la card tornereste in pari solo aggiungendo due o tre visite comprese &mdash; il Battistero '
            u'da solo ne vale 15,00 &euro;.</p>' % eur(-d))


def build_index():
    blocchi, switch = [], []
    for v in VARIANTI:
        tl = tabella_itinerario(v)
        conti_html, tot_s, tot_c = blocco_conti(v)
        ntappe = len(set(p for p, _, _, _ in v['tappe']))
        switch.append(
            u'    <button type="button" class="sw" data-v="%s" aria-pressed="%s" aria-controls="var-%s">'
            u'<span class="sig">%s</span><span class="tit">%s</span>'
            u'<span class="det">%s</span>'
            u'<span class="cost">Biglietti <b>%s</b> &nbsp;·&nbsp; con la card <b>%s</b></span></button>'
            % (v['id'], 'true' if v['id'] == PRIMA else 'false', v['id'], v['sigla'], v['titolo'],
               v['sommario'], eur(tot_s), eur(tot_c)))
        blocchi.append(
            u'  <section class="variante" id="var-%s"%s>\n'
            u'    <div class="sechead"><h2>Itinerario %s &middot; %s</h2>'
            u'<span class="cnt">%d tappe &middot; %s &rarr; %s</span></div>\n'
            u'    <p class="introtab">Le stesse righe delle due tabelle di riferimento, '
            u'nell\u2019ordine di questo itinerario.</p>\n'
            u'%s\n'
            u'    <div class="sechead"><h2>Quanto costa</h2><span class="cnt">a testa, ingressi e tram</span></div>\n'
            u'%s\n%s\n  </section>'
            % (v['id'], u'' if v['id'] == PRIMA else u' hidden', v['sigla'], v['titolo'],
               ntappe, ARRIVO, RIENTRO, tl, conti_html, verdetto(v)))

    _, tot_sa, tot_ca = blocco_conti(VARIANTE_A)
    risparmio = eur(tot_sa - tot_ca)

    tick = u''.join(u'      <div class="tick"><p class="lab">%s</p><p class="val">%s</p><p class="det">%s</p></div>\n'
                    % (n, p, d) for n, p, d in TRASPORTI['biglietti'])
    dove = u''.join(u'      <li><span class="n">%s</span><span class="q">%s</span><p class="d">%s</p></li>\n'
                    % (n, q, d) for n, q, d in TRASPORTI['dove'])
    come = u''.join(u'      <li><span class="n">%s</span><p class="d">%s</p></li>\n'
                    % (n, d) for n, d in TRASPORTI['come'])
    dist = u''.join(u'      <li><span class="n">%s</span><span class="q">%s</span>'
                    u'<p class="d">%s &nbsp;&middot;&nbsp; %s</p></li>\n'
                    % (dove_, km, piedi, mezzi)
                    for dove_, km, piedi, mezzi in PLACES['stazione']['distanze'])

    body = u"""%(nav)s

  <header class="masthead">
    <p class="eyebrow">%(giorno)s &middot; arrivo %(arrivo)s &middot; rientro %(rientro)s &middot; senza Scrovegni</p>
    <h1>Un giorno a <em>Padova</em></h1>
    <p class="standfirst">Tre giornate possibili fra la stazione e il Prato della Valle, incastrate fra i tre orari fissi
    della giornata: il treno delle 9:30, il tavolo delle 13:00 e il treno di ritorno delle 18:20.
    Senza la Cappella degli Scrovegni &mdash; al suo posto il <b>Battistero del Duomo</b>, che ha un ciclo di
    affreschi altrettanto grande e quasi nessuna coda.</p>
    <ul class="legend">
      <li style="--c:var(--route)"><i class="bar"></i>Il percorso a piedi</li>
      <li style="--c:var(--card)"><i class="dia"></i>Nella Padova Card</li>
      <li style="--c:var(--other)"><i></i>Altri luoghi</li>
      <li style="--c:var(--food)"><i></i>Il pranzo</li>
    </ul>
  </header>

  <a class="mapcard" href="../">
    <div>
      <p class="kicker">La mappa</p>
      <h2>La mappa dei tre percorsi</h2>
      <p>Sta nella home del sito, sotto le foto: i tracciati proiettati dalle coordinate reali, i canali che
      chiudono il centro ad anello, i due bar e la linea del tram SIR1 dalla stazione alla fermata Santo.</p>
      <span class="go">Vai alla mappa &rarr;</span>
    </div>
    <div class="thumb">%(mini)s</div>
  </a>

  <div class="cardrow">
    <a class="linkcard" href="padova-card.html">
      <p class="kicker">Padova Card</p>
      <h2>Gli otto siti della card</h2>
      <p>I cicli affrescati del Trecento, patrimonio UNESCO: cosa sono, quando aprono, quanto costerebbero
      uno per uno e da dove viene ogni dato.</p>
      <span class="marks" aria-hidden="true"><i class="dia" style="--c:var(--card)"></i><i class="dia" style="--c:var(--card)"></i><i class="dia" style="--c:var(--card)"></i><i class="dia" style="--c:var(--card)"></i></span>
      <span class="go">Apri la tabella &rarr;</span>
    </a>
    <a class="linkcard" href="altri-luoghi.html">
      <p class="kicker">Altri luoghi</p>
      <h2>Fuori dalla card</h2>
      <p>Palazzo del Bo, l&rsquo;Orto Botanico, il Prato della Valle, il Pedrocchi e il tavolo prenotato del Bacaro Padovano.</p>
      <span class="marks" aria-hidden="true"><i style="--c:var(--other)"></i><i style="--c:var(--other)"></i><i style="--c:var(--other)"></i><i style="--c:var(--food)"></i></span>
      <span class="go">Apri la tabella &rarr;</span>
    </a>
  </div>

  <div class="sechead"><h2>Tre itinerari</h2><span class="cnt">cambiano ordine, orari e conto</span></div>
  <div class="switch">
%(switch)s
  </div>

%(blocchi)s

  <div class="sechead"><h2>Dalla stazione</h2><span class="cnt">a piedi o in tram</span></div>
  <ul class="dove" style="margin-bottom:26px">
%(dist)s  </ul>

  <div class="sechead"><h2>Biglietti del bus e del tram</h2><span class="cnt">Busitalia Veneto, zona urbana</span></div>
  <div class="tickets">
%(tick)s  </div>
  <div class="sechead" style="border-bottom-width:1px"><h2 style="font-size:11.5px;color:var(--ink-faint)">Dove si comprano</h2></div>
  <ul class="dove">
%(dove)s  </ul>
  <div class="sechead" style="border-bottom-width:1px"><h2 style="font-size:11.5px;color:var(--ink-faint)">Come si usano</h2></div>
  <ul class="dove">
%(come)s  </ul>
  <p class="verdetto" style="border-left-color:var(--tram)">%(consiglio)s</p>

%(foot)s

<script>
(function(){
  "use strict";
  var btns=document.querySelectorAll('.switch .sw');
  btns.forEach(function(b){
    b.addEventListener('click',function(){
      btns.forEach(function(o){
        var on = o===b;
        o.setAttribute('aria-pressed', String(on));
        document.getElementById('var-'+o.dataset.v).hidden = !on;
      });
      document.querySelector('.switch').scrollIntoView({block:'start',behavior:'smooth'});
    });
  });
})();
</script>""" % dict(nav=nav("giornata"), giorno=GIORNO.capitalize(), arrivo=ARRIVO, rientro=RIENTRO,
                    mini=build_map(interactive=False, mini=True),
                    switch=u'\n'.join(switch), blocchi=u'\n\n'.join(blocchi), risp=risparmio,
                    tick=tick, dove=dove, come=come, dist=dist,
                    consiglio=TRASPORTI['consiglio'], foot=FOOT)

    return page(u"Un giorno a Padova",
                u"Due itinerari di un giorno nel centro di Padova, sabato 9:30-18:20, senza la Cappella degli Scrovegni.",
                INDEX_CSS, u'<div class="wrap">\n' + body + u'\n</div>', maxw="960px")


HOME_BODY = u"""%(nav)s

  <header class="masthead">
    <p class="eyebrow">Itinerari</p>
    <h1>EPPHURE</h1>
  </header>

  <div class="foto">
    <figure>
      <img src="img/panchina.jpg" alt="Quattro ragazzi seduti sulla spalliera di una panchina in un parco"
           width="640" height="640">
    </figure>
    <figure>
      <img src="img/mare.jpg" alt="Sei ragazzi in posa sulla riva di una spiaggia, con scogliera alle spalle"
           width="1600" height="1200">
    </figure>
  </div>

  <div class="sechead"><h2>Padova &middot; %(giorno)s</h2><span class="cnt">%(arrivo)s &rarr; %(rientro)s</span></div>
  <ul class="legend">
    <li style="--c:var(--route)"><i class="bar"></i>Percorso a piedi</li>
    <li style="--c:var(--route)"><i></i>Tappa</li>
    <li style="--c:var(--card)"><i class="dia"></i>Padova Card</li>
    <li style="--c:var(--other)"><i></i>Altro luogo</li>
    <li style="--c:var(--bar)"><i style="border-radius:3px"></i>Bar</li>
    <li style="--c:var(--tram)"><i class="bar"></i>Tram SIR1</li>
  </ul>

  <div class="cols" style="margin-top:24px">
    <div class="mapcol">
      <div class="mapframe"><svg class="map" id="svg" viewBox="0 0 %(vw)d %(vh)d" role="img"
        aria-label="Mappa schematica del centro di Padova con i tre itinerari della giornata">%(svg)s</svg></div>
      <p class="mapnote">Il cerchio azzurro attorno a una tappa vuol dire che &egrave; compresa nella Padova Card;
      il segnaposto viola &egrave; il pranzo, i quadratini verde-petrolio sono i due bar. La linea gialla tratteggiata
      &egrave; il <b>tram SIR1</b>, che dalla stazione arriva alla fermata <b>Santo</b> in sei fermate: passaci sopra
      per leggere i nomi.</p>
    </div>
    <div>
      <div class="vswitch">
%(vsw)s
      </div>
      <div class="sechead"><h2>La giornata</h2><span class="cnt">%(arrivo)s &rarr; %(rientro)s</span></div>
%(lists)s
      <a class="vai" href="padova/">
        <h2>Tutti i dettagli della giornata</h2>
        <p>Che cosa si vede a ogni tappa, quanto costa ciascun itinerario, dove e come si comprano i biglietti
        del tram, e le due tabelle con orari, prezzi e fonti.</p>
        <span class="go">Apri &rarr;</span>
      </a>
    </div>
  </div>

  <footer>Le pagine sono statiche e autosufficienti: nessun tracciamento, nessun cookie.</footer>

<script>
(function(){
  "use strict";
  var markers=document.querySelectorAll('.marker'), active=null;
  function setActive(p,scroll){
    active = (active===p) ? null : p;
    markers.forEach(function(m){m.classList.toggle('on', m.dataset.p===active);});
    document.querySelectorAll('.item').forEach(function(i){i.classList.toggle('on', i.dataset.p===active);});
    if(active && scroll){
      var el=document.querySelector('.items:not([hidden]) .item[data-p="'+active+'"]');
      if(el) el.scrollIntoView({block:'nearest',behavior:'smooth'});
    }
  }
  function applica(v){
    markers.forEach(function(m){
      var n=m.dataset[v];
      m.classList.toggle('off', !n);
      var t=m.querySelector('.num');
      if(t) t.textContent = n || '';
    });
    document.querySelectorAll('.rt').forEach(function(g){
      if(g.dataset.v===v){ g.removeAttribute('hidden'); } else { g.setAttribute('hidden','hidden'); }
    });
    document.querySelectorAll('.items').forEach(function(u){u.hidden = u.id!=='lista-'+v;});
    document.querySelectorAll('.vsw').forEach(function(b){b.setAttribute('aria-pressed', String(b.dataset.v===v));});
    active=null; setActive(null,false);
  }
  document.querySelectorAll('.vsw').forEach(function(b){
    b.addEventListener('click',function(){applica(b.dataset.v);});
  });
  function wire(el,scroll){
    el.addEventListener('click',function(){setActive(el.dataset.p,scroll);});
    el.addEventListener('keydown',function(e){
      if(e.key==='Enter'||e.key===' '){e.preventDefault();setActive(el.dataset.p,scroll);}
    });
  }
  markers.forEach(function(m){wire(m,true);});
  document.querySelectorAll('.item').forEach(function(i){wire(i,false);});
  applica('%(prima)s');
})();
</script>"""


# =========================================================== 2. la home: foto + mappa
HOME_CSS = MAP_CSS + u"""
.foto{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:0 0 34px;
  max-width:600px;align-items:start}
@media (max-width:520px){.foto{grid-template-columns:1fr;max-width:300px}}
.foto figure{margin:0;background:var(--surface);border:1px solid var(--rule);border-radius:4px;
  overflow:hidden;box-shadow:var(--shadow);line-height:0}
.foto figure{aspect-ratio:4/3;display:flex;align-items:center;justify-content:center}
.foto img{display:block;width:100%;height:100%;object-fit:contain}
.cols{display:grid;grid-template-columns:minmax(0,1.05fr) minmax(0,1fr);gap:34px;align-items:start}
@media (max-width:920px){.cols{grid-template-columns:1fr;gap:26px}}
.mapcol{position:sticky;top:calc(env(safe-area-inset-top,0px) + 14px)}
@media (max-width:920px){.mapcol{position:static}}
.marker.off{opacity:.18}
.vswitch{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin:0 0 18px}
.vswitch button{font-family:inherit;cursor:pointer;background:var(--surface);
  border:1px solid var(--rule);border-radius:4px;padding:11px 12px;color:inherit;text-align:left;
  transition:border-color .15s,background .15s}
.vswitch button:hover{border-color:var(--ink-faint)}
.vswitch button:focus-visible{outline:2px solid var(--route);outline-offset:3px}
.vswitch button[aria-pressed="true"]{border-color:var(--route);border-width:2px;padding:10px 11px;
  background:var(--surface-2)}
.vswitch .sig{display:inline-flex;align-items:center;justify-content:center;width:23px;height:23px;
  border-radius:50%;background:var(--ink-faint);color:var(--marker-ring);font-size:12px;
  font-weight:700;margin-right:7px;vertical-align:-5px}
.vswitch button[aria-pressed="true"] .sig{background:var(--route)}
.vswitch .t{font-size:13px;font-weight:500}
.items{list-style:none;margin:0;padding:0}
.item{display:grid;grid-template-columns:36px minmax(0,1fr);gap:0 13px;padding:13px 10px 13px 8px;
  border-bottom:1px solid var(--rule-soft);cursor:pointer;transition:background .15s;border-radius:2px}
.item:hover,.item.on{background:var(--surface-2)}
.item.on{box-shadow:inset 3px 0 0 var(--c,var(--route))}
.item:focus-visible{outline:2px solid var(--route);outline-offset:-2px}
.item .n{grid-row:1/span 3;width:30px;height:30px;border-radius:50%;background:var(--c,var(--route));
  color:var(--marker-ring);display:flex;align-items:center;justify-content:center;
  font-size:14px;font-weight:600;font-variant-numeric:tabular-nums;margin-top:2px}
.item h3{margin:0;font-family:'EB Garamond',Garamond,serif;font-weight:600;font-size:20px;line-height:1.18}
.item .ora{margin:3px 0 0;font-size:13px;color:var(--ink-faint);font-variant-numeric:tabular-nums}
.item .ora b{color:var(--ink-soft);font-weight:600}
.sechead{display:flex;align-items:baseline;gap:12px;padding-bottom:9px;
  border-bottom:2px solid var(--ink);margin:0 0 4px}
.sechead h2{margin:0;font-family:'Jost',sans-serif;font-size:12.5px;font-weight:700;
  letter-spacing:.15em;text-transform:uppercase}
.sechead .cnt{margin-left:auto;font-size:12.5px;color:var(--ink-faint)}
.vai{display:block;margin:26px 0 0;background:var(--surface);border:1px solid var(--rule);
  border-radius:4px;padding:18px 20px;text-decoration:none;color:inherit;box-shadow:var(--shadow);
  transition:border-color .15s,transform .15s}
.vai:hover{border-color:var(--ink-faint);transform:translateY(-1px)}
.vai:focus-visible{outline:2px solid var(--card);outline-offset:3px}
.vai h2{margin:0;font-family:'EB Garamond',Garamond,serif;font-weight:600;font-size:24px;line-height:1.1}
.vai p{margin:9px 0 0;font-size:14.5px;color:var(--ink-soft);line-height:1.45}
.vai .go{display:inline-block;margin-top:11px;font-size:13.5px;font-weight:600;color:var(--route)}
"""


def build_home():
    lists, vsw = [], []
    for v in VARIANTI:
        items, visti = [], set()
        for pid, ora, durata, costo in v['tappe']:
            if pid in visti:
                continue
            visti.add(pid)
            pl = PLACES[pid]
            col = ' style="--c:var(--food)"' if pl.get('pasto') else ''
            extra = u' &middot; %s' % costo if costo else u''
            items.append(u'        <li class="item" data-p="%s" tabindex="0"%s><span class="n">%d</span>'
                         u'<h3>%s</h3><p class="ora"><b>%s</b> &middot; %s%s</p></li>'
                         % (pid, col, NUM[pid][v['id']], pl['nome'], ora, durata, extra))
        lists.append(u'      <ul class="items" id="lista-%s"%s>\n%s\n      </ul>'
                     % (v['id'], u'' if v['id'] == PRIMA else u' hidden', u'\n'.join(items)))
        vsw.append(u'        <button type="button" class="vsw" data-v="%s" aria-pressed="%s">'
                   u'<span class="sig">%s</span><span class="t">%s</span></button>'
                   % (v['id'], 'true' if v['id'] == PRIMA else 'false', v['sigla'], v['titolo']))

    body = HOME_BODY % dict(nav=nav("home", "root"), svg=build_map(), vw=VW, vh=VH, giorno=GIORNO,
                            arrivo=ARRIVO, rientro=RIENTRO,
                            vsw=u'\n'.join(vsw), lists=u'\n'.join(lists), prima=PRIMA)
    return page(u"EPPHURE",
                u"Tre itinerari per un giorno a Padova, disegnati su una mappa del centro.",
                HOME_CSS, u'<div class="wrap">\n' + body + u'\n</div>', maxw="1280px")


# =========================================================== 3-4. le due tabelle
TAB_CSS = u"""
.tablebox{overflow-x:auto;border:1px solid var(--rule);border-radius:4px;
  background:var(--surface);box-shadow:var(--shadow)}
table{width:100%;border-collapse:collapse;min-width:1020px}
thead th{background:var(--surface-2);text-align:left;font-size:11px;font-weight:700;
  letter-spacing:.14em;text-transform:uppercase;color:var(--ink-faint);
  padding:13px 16px;border-bottom:2px solid var(--ink)}
td{padding:17px 16px;border-bottom:1px solid var(--rule-soft);vertical-align:top}
tbody tr:last-child td{border-bottom:0}
tbody tr:hover{background:var(--surface-2)}
tbody tr.off{opacity:.55}
.c-nome{width:18%;min-width:165px;font-family:'EB Garamond',Garamond,serif;
  font-weight:600;font-size:20px;line-height:1.16}
.c-nome .tappa{display:inline-flex;align-items:center;justify-content:center;
  width:23px;height:23px;border-radius:50%;background:var(--c,var(--route));color:var(--marker-ring);
  font-family:'Jost',sans-serif;font-size:11.5px;font-weight:700;vertical-align:3px;margin-right:7px}
.c-nome .skip{display:inline-block;margin-top:6px;font-family:'Jost',sans-serif;font-size:10px;
  font-weight:700;letter-spacing:.09em;text-transform:uppercase;color:var(--ink-faint);
  border:1px solid var(--rule);border-radius:3px;padding:2px 7px}
.c-perche{width:30%;min-width:250px;font-size:14px;color:var(--ink-soft);line-height:1.5}
.c-perche b{color:var(--ink);font-weight:600}
.c-orari{width:24%;min-width:205px;font-size:13.5px;color:var(--ink-soft);line-height:1.45}
.c-prezzo{width:16%;min-width:150px;font-size:16px;font-weight:600;
  font-variant-numeric:tabular-nums;letter-spacing:-.01em}
.c-fonte{width:12%;min-width:135px;font-size:13px}
.c-fonte a{color:var(--card);text-underline-offset:3px}
.c-fonte a:hover{color:var(--ink)}
.c-fonte .none{display:inline-block;font-size:10.5px;font-weight:700;letter-spacing:.08em;
  text-transform:uppercase;color:var(--ink-faint);border:1px solid var(--rule);
  border-radius:3px;padding:2px 7px;line-height:1.5}
.c-fonte .why{display:block;margin-top:6px;font-size:12px;color:var(--ink-faint);line-height:1.4}
.c-orari em,.c-prezzo em{display:block;font-style:normal;font-weight:400;font-size:12.5px;
  letter-spacing:0;color:var(--ink-faint);margin-top:5px;line-height:1.45}
@media (max-width:980px){
  .tablebox{overflow-x:visible;border:0;border-radius:0;background:transparent;box-shadow:none}
  table{min-width:0}
  thead{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}
  tbody tr{display:block;background:var(--surface);border:1px solid var(--rule);border-radius:4px;
    padding:16px 17px;margin-bottom:12px;box-shadow:var(--shadow)}
  tbody tr:hover{background:var(--surface)}
  td{display:block;width:auto!important;min-width:0!important;padding:0;border:0}
  .c-perche,.c-orari,.c-prezzo,.c-fonte{margin-top:12px}
  .c-perche::before,.c-orari::before,.c-prezzo::before,.c-fonte::before{content:attr(data-l);display:block;
    font-family:'Jost',sans-serif;font-size:10px;font-weight:700;letter-spacing:.14em;
    text-transform:uppercase;color:var(--ink-faint);margin-bottom:4px}
}
.secnote{margin:16px 0 0;font-size:13px;line-height:1.55;color:var(--ink-faint);max-width:78ch}
.secnote b{color:var(--ink-soft);font-weight:600}
"""


def cella_fonte(s):
    out = []
    f = s.get('fonte')
    if f:
        out.append(u'<a href="%s" target="_blank" rel="noopener">%s &nearr;</a>' % (f[1], f[0]))
    else:
        out.append(u'<span class="none">non verificata</span>'
                   u'<span class="why">Orari legati alle funzioni o al mercato: non ho trovato una fonte '
                   u'ufficiale da citare, prendeteli come indicativi.</span>')
    w = s.get('wiki')
    if w:
        out.append(u'<a class="wiki" href="%s" target="_blank" rel="noopener">Wikipedia &nearr;</a>' % w)
    return u''.join(out)


def rows(data, colore):
    out = []
    for s in data:
        pid = s.get('tappa')
        col = ('var(--food)' if s.get('tipo') == 'pasto'
               else 'var(--bar)' if s.get('tipo') == 'bar' else colore)
        badge = u''
        if pid:
            na, nb = NUM[pid]['a'], NUM[pid]['b']
            et = (u'%d' % na) if na else (u'%d' % nb)
            if na and nb and na != nb:
                et = u'%d/%d' % (na, nb)
            badge = u'<span class="tappa" style="--c:%s">%s</span>' % (col, et)
        skip = u'<br><span class="skip">Fuori programma</span>' if s.get('escluso') else u''
        out.append(
            u'        <tr%s>\n'
            u'          <td class="c-nome">%s%s%s</td>\n'
            u'          <td class="c-perche" data-l="Perch&eacute; conta">%s</td>\n'
            u'          <td class="c-orari" data-l="Orari e chiusura">%s</td>\n'
            u'          <td class="c-prezzo" data-l="Prezzo senza card">%s</td>\n'
            u'          <td class="c-fonte" data-l="Fonte">%s</td>\n'
            u'        </tr>' % (u' class="off"' if s.get('escluso') else u'',
                                badge, s['nome'], skip, s['perche'], s['orari'], s['prezzo'],
                                cella_fonte(s)))
    return u'\n'.join(out)


def tabella(titolo, occhiello, h1, standfirst, legenda, data, colore, nota, cur, desc):
    body = u"""%(nav)s

  <header class="masthead">
    <p class="eyebrow">%(occ)s</p>
    <h1>%(h1)s</h1>
    <p class="standfirst">%(sf)s</p>
    <ul class="legend">%(leg)s</ul>
  </header>

  <div class="tablebox">
    <table>
      <thead>
        <tr><th>Nome</th><th>Perch&eacute; conta</th><th>Orari e giorno di chiusura</th>
        <th>Prezzo senza card</th><th>Fonte</th></tr>
      </thead>
      <tbody>
%(rows)s
      </tbody>
    </table>
  </div>
  <p class="secnote">%(nota)s</p>

%(foot)s""" % dict(nav=nav(cur), occ=occhiello, h1=h1, sf=standfirst, leg=legenda,
                   rows=rows(data, colore), nota=nota, foot=FOOT)
    return page(titolo, desc, TAB_CSS, u'<div class="wrap">\n' + body + u'\n</div>', maxw="1380px")


def build_card():
    return tabella(
        u"Gli otto siti della Padova Card", u"Padova Urbs picta Card &middot; 8 siti &middot; %s" % CARD_PREZZO,
        u"La <em>card</em>",
        u"La <b>Padova Urbs picta Card</b> costa %s per 48 ore (35,00 &euro; per 72) e comprende gli otto cicli "
        u"affrescati del Trecento iscritti all&rsquo;UNESCO nel 2021, pi&ugrave; i mezzi pubblici Busitalia. "
        u"Il numero rosso indica le tappe del <a href=\"./\">vostro itinerario</a>: dove ne trovate due, "
        u"sono le posizioni nell&rsquo;itinerario A e nel B." % CARD_PREZZO,
        u'<li style="--c:var(--card)"><i class="dia"></i>Compreso nella card</li>'
        u'<li style="--c:var(--route)"><i></i>Tappa dell&rsquo;itinerario</li>',
        CARD_SITI, 'var(--route)',
        u"<b>Di sabato aprono tutti</b> tranne la Cappella della Reggia Carrarese, che ha aperture irregolari: "
        u"verificatela prima di contarci. Il luned&igrave; invece chiuderebbero Palazzo della Ragione e i due oratori. "
        u"<b>Sul biglietto del Santo:</b> i 10,00 &euro; sono un cumulativo per Oratorio, Scoletta e Museo Antoniano, "
        u"e non &egrave; del tutto chiaro quanto di quel cumulativo la card sostituisca &mdash; conviene chiederlo alla biglietteria.",
        "card",
        u"Gli otto siti compresi nella Padova Urbs picta Card, con orari, prezzi e la fonte di ogni dato.")


def build_altri():
    return tabella(
        u"Altri luoghi di Padova", u"Fuori dalla card &middot; %d luoghi" % len(ALTRI_LUOGHI),
        u"Fuori dalla <em>card</em>",
        u"Quello che la Padova Urbs picta Card non copre e che vale comunque la giornata: l&rsquo;universit&agrave;, "
        u"l&rsquo;orto botanico, la piazza pi&ugrave; grande d&rsquo;Italia &mdash; e il tavolo prenotato per l&rsquo;una. "
        u"Il numero indica le tappe del <a href=\"./\">vostro itinerario</a>.",
        u'<li style="--c:var(--other)"><i></i>Fuori dalla card</li>'
        u'<li style="--c:var(--route)"><i></i>Tappa dell&rsquo;itinerario</li>'
        u'<li style="--c:var(--food)"><i></i>Il pranzo</li>'
        u'<li style="--c:var(--bar)"><i style="border-radius:3px"></i>I due bar</li>',
        ALTRI_LUOGHI, 'var(--route)',
        u"<b>Palazzo del Bo di sabato costa di pi&ugrave; e dura di pi&ugrave;:</b> 12,00 &euro; e 75 minuti invece di "
        u"7,00 &euro; e 45, perch&eacute; nel fine settimana il giro &egrave; quello lungo che aggiunge l&rsquo;ala di Gio Ponti. "
        u"Il Teatro Anatomico e la cattedra di Galileo ci sono in entrambi. "
        u"<b>Il Bacaro Padovano</b> a pranzo apre solo venerd&igrave;, sabato e domenica: il vostro sabato va bene.",
        "altri",
        u"Palazzo del Bo, Orto Botanico, Prato della Valle e altri luoghi di Padova fuori dalla card.")


if __name__ == '__main__':
    lavori = [("../index.html", build_home), ("index.html", build_index),
              ("padova-card.html", build_card), ("altri-luoghi.html", build_altri)]
    for name, fn in lavori:
        print("%-20s %5.1f KB" % (name, write(name, fn())))
    vecchia = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mappa.html")
    if os.path.exists(vecchia):
        os.remove(vecchia)
        print("rimossa mappa.html: ora la mappa sta nella home")
    for v in VARIANTI:
        _s, ts, _c, tc = conti(v)
        print("Itinerario %-4s singoli %5.2f  |  con card %5.2f" % (v['sigla'], ts, tc))
