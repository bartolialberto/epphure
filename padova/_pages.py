# -*- coding: utf-8 -*-
"""Le quattro pagine."""
import io, os
from _build import (page, nav, write, build_map, MAP_CSS, VW, VH, eur, extra_markers)
from _data import ITINERARIO, CARD_SITI, ALTRI_LUOGHI, CONTI, CARD_PREZZO

FOOT = u"""  <footer>
    <p><b>Orari e prezzi raccolti il 22 settembre 2026</b> dai siti ufficiali di Musei Civici di Padova,
    Universit&agrave; di Padova, Kalat&agrave;/Museo Diocesano, Basilica del Santo, Orto Botanico e Bacaro Padovano.
    Cambiano spesso: vanno riverificati prima di partire, e due visite di questo itinerario
    (Palazzo del Bo e il Battistero) <b>richiedono prenotazione</b>.</p>
    <p>La Cappella degli Scrovegni non fa parte del programma per vostra scelta. Resta nella tabella
    della card perch&eacute; &egrave; la voce che ne determina il prezzo.</p>
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
.sechead .cnt{margin-left:auto;font-size:12.5px;color:var(--ink-faint)}

.day{list-style:none;margin:0 0 38px;padding:0}
.stop{display:grid;grid-template-columns:62px 38px minmax(0,1fr);gap:0 14px;
  padding:18px 0 20px;border-bottom:1px solid var(--rule-soft)}
@media (max-width:560px){.stop{grid-template-columns:38px minmax(0,1fr)}
  .stop .ora{grid-column:2;margin-bottom:4px}}
.stop .ora{font-size:15px;font-weight:600;font-variant-numeric:tabular-nums;
  color:var(--ink);letter-spacing:.01em;padding-top:3px}
.stop .bullet{grid-row:1/span 5;display:flex;justify-content:center;position:relative}
@media (max-width:560px){.stop .bullet{grid-row:1/span 5;grid-column:1}}
.stop .bullet span{width:32px;height:32px;border-radius:50%;background:var(--c,var(--route));
  color:var(--marker-ring);display:flex;align-items:center;justify-content:center;
  font-size:14.5px;font-weight:600;font-variant-numeric:tabular-nums;z-index:1;margin-top:1px}
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
.stop p.nota{margin:9px 0 0;font-size:13.5px;color:var(--ink-faint);line-height:1.5;
  border-left:2px solid var(--rule);padding-left:11px;max-width:60ch}
.stop p.nota b{color:var(--ink-soft)}

.conti{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:0 0 20px}
@media (max-width:640px){.conti{grid-template-columns:1fr}}
.conto{background:var(--surface);border:1px solid var(--rule);border-radius:4px;padding:17px 19px}
.conto.win{border-color:var(--card);border-width:2px}
.conto h3{margin:0 0 3px;font-family:'Jost',sans-serif;font-size:12px;font-weight:700;
  letter-spacing:.14em;text-transform:uppercase;color:var(--ink-faint)}
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
  border-radius:0 3px 3px 0;margin:0 0 34px;font-size:14.5px;color:var(--ink-soft);line-height:1.55}
.verdetto b{color:var(--ink);font-weight:600}
"""


def build_index():
    stops = []
    for s in ITINERARIO:
        pills = [u'<span class="pill">%s</span>' % s['durata']]
        if s.get('costo'):
            c = s['costo']
            cls = 'free' if c in (u'Gratuito', u'—') else 'price'
            pills.append(u'<span class="pill %s">%s</span>' % (cls, c))
        if s['card']:
            pills.append(u'<span class="pill incard">Nella card</span>')
        col = ' style="--c:var(--food)"' if s.get('pasto') else ''
        stops.append(
            u'    <li class="stop">\n'
            u'      <span class="ora">%s</span>\n'
            u'      <span class="bullet"%s><span>%d</span></span>\n'
            u'      <h3>%s</h3>\n'
            u'      <span class="meta">%s</span>\n'
            u'      <p class="testo">%s</p>\n'
            u'      %s\n    </li>'
            % (s['ora'], col, s['n'], s['nome'], u''.join(pills), s['testo'],
               (u'<p class="nota">%s</p>' % s['nota']) if s.get('nota') else u''))

    def conto(titolo, righe, sub, win=False):
        tot = sum(v for _, v in righe)
        li = u''.join(u'<li><span>%s</span><span>%s</span></li>' % (n, eur(v)) for n, v in righe)
        return (u'    <div class="conto%s"><h3>%s</h3><p class="kicker" style="margin:0;letter-spacing:.02em;'
                u'text-transform:none;font-size:13px;color:var(--ink-soft);font-weight:400">%s</p>'
                u'<ul>%s</ul><div class="tot"><b>Totale</b><em>%s</em></div></div>'
                % (u' win' if win else u'', titolo, sub, li, eur(tot)))

    tot_s = sum(v for _, v in CONTI['singoli'])
    tot_c = sum(v for _, v in CONTI['con_card'])
    body = u"""%(nav)s

  <header class="masthead">
    <p class="eyebrow">Arrivo 9:00 &middot; pranzo 13:00 &middot; senza Scrovegni</p>
    <h1>Un giorno a <em>Padova</em></h1>
    <p class="standfirst">Dieci tappe fra la stazione e il Prato della Valle, costruite attorno ai due orari fissi
    della giornata: il treno delle nove e il tavolo delle tredici. Senza la Cappella degli Scrovegni &mdash;
    al suo posto, il <b>Battistero del Duomo</b>, che ha un ciclo di affreschi altrettanto grande e quasi nessuna coda.</p>
    <ul class="legend">
      <li style="--c:var(--route)"><i class="bar"></i>Il percorso a piedi</li>
      <li style="--c:var(--card)"><i class="dia"></i>Nella Padova Card</li>
      <li style="--c:var(--other)"><i></i>Altri luoghi</li>
      <li style="--c:var(--food)"><i></i>Il pranzo</li>
    </ul>
  </header>

  <a class="mapcard" href="mappa.html">
    <div>
      <p class="kicker">La mappa</p>
      <h2>Il percorso disegnato sulla citt&agrave;</h2>
      <p>Le dieci tappe proiettate dalle coordinate reali, il tracciato a piedi che le unisce, i canali che chiudono
      il centro ad anello e la linea del tram per tornare in stazione.</p>
      <span class="go">Apri la mappa &rarr;</span>
    </div>
    <div class="thumb">%(mini)s</div>
  </a>

  <div class="cardrow">
    <a class="linkcard" href="padova-card.html">
      <p class="kicker">Padova Card</p>
      <h2>Gli otto siti della card</h2>
      <p>I cicli affrescati del Trecento, patrimonio UNESCO: cosa sono, quando aprono e quanto costerebbero uno per uno.</p>
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

  <div class="sechead"><h2>La giornata</h2><span class="cnt">10 tappe &middot; circa 5 km a piedi</span></div>
  <ol class="day">
%(stops)s
  </ol>

  <div class="sechead"><h2>Conviene la Padova Card?</h2><span class="cnt">solo per questa giornata</span></div>
  <div class="conti" style="margin-top:18px">
%(conto_a)s
%(conto_b)s
  </div>
  <p class="verdetto"><b>Quasi in pari: %(diff)s di differenza.</b> La <b>Padova Urbs picta Card</b> costa %(cardp)s per 48 ore
  e vive di rendita sulla Cappella degli Scrovegni, che voi non fate. Senza quella, il margine si assottiglia.
  Conviene comprarla se aggiungete anche solo <b>un altro sito della card</b> &mdash; l&rsquo;Oratorio di San Michele,
  la Chiesa degli Eremitani, i Musei Civici &mdash; oppure se contate di usare il <b>tram</b>, che &egrave; compreso nel prezzo
  e vi riporta in stazione dal Prato della Valle.</p>

%(foot)s""" % dict(nav=nav("index.html"), mini=build_map(interactive=False, mini=True),
                   stops=u'\n'.join(stops),
                   conto_a=conto(u"Biglietti singoli", CONTI['singoli'], u"pagando ogni ingresso dell’itinerario"),
                   conto_b=conto(u"Con la card", CONTI['con_card'], u"la card copre Ragione, Battistero e Oratorio", win=(tot_c < tot_s)),
                   diff=eur(abs(tot_s - tot_c)), cardp=CARD_PREZZO, foot=FOOT)

    return page(u"Un giorno a Padova",
                u"Itinerario di un giorno nel centro di Padova senza la Cappella degli Scrovegni, con mappa, orari e prezzi.",
                INDEX_CSS, u'<div class="wrap">\n' + body + u'\n</div>', maxw="960px")


# =========================================================== 2. la mappa
MAPPA_CSS = MAP_CSS + u"""
.cols{display:grid;grid-template-columns:minmax(0,1.05fr) minmax(0,1fr);gap:34px;align-items:start}
@media (max-width:920px){.cols{grid-template-columns:1fr;gap:26px}}
.mapcol{position:sticky;top:calc(env(safe-area-inset-top,0px) + 14px)}
@media (max-width:920px){.mapcol{position:static}}
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
"""


def build_mappa():
    items = []
    for s in ITINERARIO:
        col = ' style="--c:var(--food)"' if s.get('pasto') else ''
        extra = u' &middot; %s' % s['costo'] if s.get('costo') else u''
        items.append(u'      <li class="item" data-n="%d" tabindex="0"%s><span class="n">%d</span>'
                     u'<h3>%s</h3><p class="ora"><b>%s</b> &middot; %s%s</p></li>'
                     % (s['n'], col, s['n'], s['nome'], s['ora'], s['durata'], extra))
    body = u"""%(nav)s

  <header class="masthead">
    <p class="eyebrow">Mappa &middot; 10 tappe &middot; circa 5 km</p>
    <h1>Il percorso a <em>piedi</em></h1>
    <p class="standfirst">Tutti i segnaposto sono proiettati dalle coordinate reali, quindi le distanze fra loro sono corrette.
    Canali, strade e tracciato del tram sono schematici.</p>
    <ul class="legend">
      <li style="--c:var(--route)"><i class="bar"></i>Percorso a piedi</li>
      <li style="--c:var(--route)"><i></i>Tappa dell&rsquo;itinerario</li>
      <li style="--c:var(--card)"><i class="dia"></i>Sito della Padova Card</li>
      <li style="--c:var(--other)"><i></i>Altro luogo</li>
      <li style="--c:var(--tram)"><i class="bar"></i>Tram SIR1</li>
    </ul>
  </header>

  <div class="cols">
    <div class="mapcol">
      <div class="mapframe"><svg class="map" id="svg" viewBox="0 0 %(vw)d %(vh)d" role="img"
        aria-label="Mappa schematica del centro di Padova con il percorso della giornata">%(svg)s</svg></div>
      <p class="mapnote">Il cerchio azzurro attorno a una tappa vuol dire che &egrave; compresa nella Padova Card.
      Il tratto viola &egrave; il pranzo. Passa il dito o il mouse sui pallini del tram per leggere il nome della fermata.</p>
    </div>
    <div>
      <div class="sechead" style="display:flex;align-items:baseline;gap:12px;padding-bottom:9px;border-bottom:2px solid var(--ink);margin:0 0 4px">
        <h2 style="margin:0;font-family:'Jost',sans-serif;font-size:12.5px;font-weight:700;letter-spacing:.15em;text-transform:uppercase">La giornata</h2>
        <span style="margin-left:auto;font-size:12.5px;color:var(--ink-faint)">09:00 &rarr; 18:45</span>
      </div>
      <ul class="items">
%(items)s
      </ul>
    </div>
  </div>

%(foot)s

<script>
(function(){
  "use strict";
  var markers=document.querySelectorAll('.marker'), items=document.querySelectorAll('.item'), active=null;
  function setActive(n,scroll){
    active = (active===n) ? null : n;
    markers.forEach(function(m){m.classList.toggle('on', +m.dataset.n===active);});
    items.forEach(function(i){i.classList.toggle('on', +i.dataset.n===active);});
    if(active!==null && scroll){
      var el=document.querySelector('.item[data-n="'+active+'"]');
      if(el) el.scrollIntoView({block:'nearest',behavior:'smooth'});
    }
  }
  function wire(el,scroll){
    el.addEventListener('click',function(){setActive(+el.dataset.n,scroll);});
    el.addEventListener('keydown',function(e){
      if(e.key==='Enter'||e.key===' '){e.preventDefault();setActive(+el.dataset.n,scroll);}
    });
  }
  markers.forEach(function(m){wire(m,true);});
  items.forEach(function(i){wire(i,false);});
})();
</script>""" % dict(nav=nav("mappa.html"), svg=build_map(), vw=VW, vh=VH,
                    items=u'\n'.join(items), foot=FOOT)
    return page(u"Mappa di un giorno a Padova",
                u"Il percorso a piedi di una giornata a Padova, disegnato sulle coordinate reali.",
                MAPPA_CSS, u'<div class="wrap">\n' + body + u'\n</div>', maxw="1280px")


# =========================================================== 3-4. le due tabelle
TAB_CSS = u"""
.tablebox{overflow-x:auto;border:1px solid var(--rule);border-radius:4px;
  background:var(--surface);box-shadow:var(--shadow)}
table{width:100%;border-collapse:collapse;min-width:900px}
thead th{background:var(--surface-2);text-align:left;font-size:11px;font-weight:700;
  letter-spacing:.14em;text-transform:uppercase;color:var(--ink-faint);
  padding:13px 16px;border-bottom:2px solid var(--ink)}
td{padding:17px 16px;border-bottom:1px solid var(--rule-soft);vertical-align:top}
tbody tr:last-child td{border-bottom:0}
tbody tr:hover{background:var(--surface-2)}
tbody tr.off{opacity:.55}
.c-nome{width:20%;min-width:175px;font-family:'EB Garamond',Garamond,serif;
  font-weight:600;font-size:20px;line-height:1.16}
.c-nome .tappa{display:inline-flex;align-items:center;justify-content:center;
  width:23px;height:23px;border-radius:50%;background:var(--c,var(--route));color:var(--marker-ring);
  font-family:'Jost',sans-serif;font-size:11.5px;font-weight:700;vertical-align:3px;margin-right:7px}
.c-nome .skip{display:inline-block;margin-top:6px;font-family:'Jost',sans-serif;font-size:10px;
  font-weight:700;letter-spacing:.09em;text-transform:uppercase;color:var(--ink-faint);
  border:1px solid var(--rule);border-radius:3px;padding:2px 7px}
.c-perche{width:34%;min-width:270px;font-size:14px;color:var(--ink-soft);line-height:1.5}
.c-perche b{color:var(--ink);font-weight:600}
.c-orari{width:26%;min-width:215px;font-size:13.5px;color:var(--ink-soft);line-height:1.45}
.c-prezzo{width:20%;min-width:165px;font-size:16px;font-weight:600;
  font-variant-numeric:tabular-nums;letter-spacing:-.01em}
.c-orari em,.c-prezzo em{display:block;font-style:normal;font-weight:400;font-size:12.5px;
  letter-spacing:0;color:var(--ink-faint);margin-top:5px;line-height:1.45}
@media (max-width:880px){
  .tablebox{overflow-x:visible;border:0;border-radius:0;background:transparent;box-shadow:none}
  table{min-width:0}
  thead{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}
  tbody tr{display:block;background:var(--surface);border:1px solid var(--rule);border-radius:4px;
    padding:16px 17px;margin-bottom:12px;box-shadow:var(--shadow)}
  tbody tr:hover{background:var(--surface)}
  td{display:block;width:auto!important;min-width:0!important;padding:0;border:0}
  .c-perche,.c-orari,.c-prezzo{margin-top:12px}
  .c-perche::before,.c-orari::before,.c-prezzo::before{content:attr(data-l);display:block;
    font-family:'Jost',sans-serif;font-size:10px;font-weight:700;letter-spacing:.14em;
    text-transform:uppercase;color:var(--ink-faint);margin-bottom:4px}
}
.secnote{margin:16px 0 0;font-size:13px;line-height:1.55;color:var(--ink-faint);max-width:76ch}
.secnote b{color:var(--ink-soft);font-weight:600}
"""

TAPPA = {}
for _s in ITINERARIO:
    TAPPA[_s['nome']] = _s['n']
from _build import ALIAS


def rows(data, colore):
    out = []
    for s in data:
        n = TAPPA.get(ALIAS.get(s['nome'], s['nome']))
        col = 'var(--food)' if s.get('tipo') == 'pasto' else colore
        badge = (u'<span class="tappa" style="--c:%s">%d</span>' % (col, n)) if n else u''
        skip = u'<br><span class="skip">Fuori programma</span>' if s.get('escluso') else u''
        out.append(
            u'        <tr%s>\n'
            u'          <td class="c-nome">%s%s%s</td>\n'
            u'          <td class="c-perche" data-l="Perch&eacute; conta">%s</td>\n'
            u'          <td class="c-orari" data-l="Orari e chiusura">%s</td>\n'
            u'          <td class="c-prezzo" data-l="Prezzo senza card">%s</td>\n'
            u'        </tr>' % (u' class="off"' if s.get('escluso') else u'',
                                badge, s['nome'], skip, s['perche'], s['orari'], s['prezzo']))
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
        <tr><th>Nome</th><th>Perch&eacute; conta</th><th>Orari e giorno di chiusura</th><th>Prezzo senza card</th></tr>
      </thead>
      <tbody>
%(rows)s
      </tbody>
    </table>
  </div>
  <p class="secnote">%(nota)s</p>

%(foot)s""" % dict(nav=nav(cur), occ=occhiello, h1=h1, sf=standfirst, leg=legenda,
                   rows=rows(data, colore), nota=nota, foot=FOOT)
    return page(titolo, desc, TAB_CSS, u'<div class="wrap">\n' + body + u'\n</div>', maxw="1280px")


def build_card():
    return tabella(
        u"Gli otto siti della Padova Card", u"Padova Urbs picta Card &middot; 8 siti &middot; %s" % CARD_PREZZO,
        u"La <em>card</em>",
        u"La <b>Padova Urbs picta Card</b> costa %s per 48 ore (35,00 &euro; per 72) e comprende gli otto cicli "
        u"affrescati del Trecento iscritti all&rsquo;UNESCO nel 2021, pi&ugrave; i mezzi pubblici Busitalia. "
        u"Il numero rosso indica le tappe del <a href=\"./\">vostro itinerario</a>." % CARD_PREZZO,
        u'<li style="--c:var(--card)"><i class="dia"></i>Compreso nella card</li>'
        u'<li style="--c:var(--route)"><i></i>Tappa dell&rsquo;itinerario</li>',
        CARD_SITI, 'var(--route)',
        u"<b>Attenzione al luned&igrave;:</b> Palazzo della Ragione, l&rsquo;Oratorio di San Giorgio e l&rsquo;Oratorio di San Michele "
        u"chiudono. <b>E al biglietto del Santo:</b> i 10,00 &euro; sono un biglietto unico per Oratorio, Scoletta e Museo "
        u"Antoniano, e non &egrave; del tutto chiaro quanto di quel cumulativo la card sostituisca &mdash; conviene chiederlo alla "
        u"biglietteria. La Cappella della Reggia Carrarese ha aperture irregolari: verificatela prima di contarci.",
        "padova-card.html",
        u"Gli otto siti compresi nella Padova Urbs picta Card, con orari, giorni di chiusura e prezzo dei biglietti singoli.")


def build_altri():
    return tabella(
        u"Altri luoghi di Padova", u"Fuori dalla card &middot; %d luoghi" % len(ALTRI_LUOGHI),
        u"Fuori dalla <em>card</em>",
        u"Quello che la Padova Urbs picta Card non copre e che vale comunque la giornata: l&rsquo;universit&agrave;, "
        u"l&rsquo;orto botanico, la piazza pi&ugrave; grande d&rsquo;Italia &mdash; e il tavolo prenotato per l&rsquo;una. "
        u"Il numero indica le tappe del <a href=\"./\">vostro itinerario</a>.",
        u'<li style="--c:var(--other)"><i></i>Fuori dalla card</li>'
        u'<li style="--c:var(--route)"><i></i>Tappa dell&rsquo;itinerario</li>'
        u'<li style="--c:var(--food)"><i></i>Il pranzo</li>',
        ALTRI_LUOGHI, 'var(--route)',
        u"<b>Il vincolo pi&ugrave; stretto della giornata &egrave; il ristorante:</b> il Bacaro Padovano serve a pranzo "
        u"<b>solo venerd&igrave;, sabato e domenica</b>. E il <b>Giro storico</b> di Palazzo del Bo, quello con il Teatro Anatomico, "
        u"si fa solo dal luned&igrave; al venerd&igrave;: nel fine settimana il tour &egrave; un altro. Le due condizioni si "
        u"incrociano in un giorno solo, il <b>venerd&igrave;</b>.",
        "altri-luoghi.html",
        u"Palazzo del Bo, Orto Botanico, Prato della Valle, Caff&egrave; Pedrocchi e altri luoghi di Padova fuori dalla card.")


if __name__ == '__main__':
    for name, fn in [("index.html", build_index), ("mappa.html", build_mappa),
                     ("padova-card.html", build_card), ("altri-luoghi.html", build_altri)]:
        kb = write(name, fn())
        print("%-20s %5.1f KB" % (name, kb))
    print("\nviewBox %d x %d" % (VW, VH))
