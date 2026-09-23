# -*- coding: utf-8 -*-
"""Genera le quattro pagine del sito "Un giorno a Padova"."""
import io, os, math, re
from _data import (PLACES, ORDINE_MAPPA, VARIANTI, CARD_SITI, ALTRI_LUOGHI,
                   CARD_PREZZO, TRAM_FERMATE)

HERE = os.path.dirname(os.path.abspath(__file__))

# =================================================================== proiezione
LON0, LON1, LAT0, LAT1 = 11.8640, 11.8900, 45.3955, 45.4190
VW = 1000.0
SX = VW / (LON1 - LON0)
SY = SX / math.cos(math.radians(45.407))
VH = int(round((LAT1 - LAT0) * SY))
px = lambda lo: (lo - LON0) * SX
py = lambda la: (LAT1 - la) * SY


def smooth(pts, closed=False):
    p = [(px(q[1]), py(q[0])) for q in pts]
    n = len(p)
    d = "M%.0f %.0f" % p[0]
    for i in range(n if closed else n - 1):
        p0, p1, p2, p3 = p[(i - 1) % n], p[i], p[(i + 1) % n], p[(i + 2) % n]
        if not closed:
            p0, p3 = p[max(i - 1, 0)], p[min(i + 2, n - 1)]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6.0, p1[1] + (p2[1] - p0[1]) / 6.0)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6.0, p2[1] - (p3[1] - p1[1]) / 6.0)
        d += "C%.0f %.0f,%.0f %.0f,%.0f %.0f" % (c1[0], c1[1], c2[0], c2[1], p2[0], p2[1])
    return d + ("Z" if closed else "")


def poly(pts):
    return "M" + "L".join("%.0f %.0f" % (px(q[1]), py(q[0])) for q in pts)


# =================================================================== geografia
# il centro storico di Padova e' un'isola: i canali lo girano tutto intorno
CANALE = [[45.4150, 11.8668], [45.4154, 11.8722], [45.4151, 11.8782], [45.4142, 11.8822],
          [45.4120, 11.8856], [45.4090, 11.8872], [45.4050, 11.8878], [45.4010, 11.8872],
          [45.3975, 11.8848], [45.3962, 11.8800], [45.3962, 11.8752], [45.3976, 11.8706],
          [45.4000, 11.8672], [45.4042, 11.8650], [45.4092, 11.8646], [45.4132, 11.8654]]
RAMI = [
    [[45.4195, 11.8618], [45.4172, 11.8632], [45.4155, 11.8656], [45.4150, 11.8668]],   # Bacchiglione da nord
    [[45.4120, 11.8856], [45.4128, 11.8890], [45.4132, 11.8920]],                       # Piovego verso est
    [[45.3962, 11.8752], [45.3948, 11.8712], [45.3938, 11.8670]],                       # verso sud-ovest
]
STRADE = [
    dict(w=8, p=[[45.4185, 11.8802], [45.4160, 11.8798], [45.4130, 11.8790], [45.4100, 11.8780],
                 [45.4086, 11.8772], [45.4078, 11.8768]]),                              # Corso del Popolo / Garibaldi
    dict(w=7, p=[[45.4078, 11.8768], [45.4072, 11.8757], [45.4058, 11.8742], [45.4040, 11.8738],
                 [45.4020, 11.8752], [45.4000, 11.8766], [45.3988, 11.8771]]),          # VIII Febbraio / Roma / Umberto I
    dict(w=6, p=[[45.4062, 11.8776], [45.4045, 11.8788], [45.4028, 11.8798], [45.4015, 11.8807]]),  # Via del Santo
    dict(w=5, p=[[45.4058, 11.8768], [45.4050, 11.8800], [45.4043, 11.8834]]),          # Via San Francesco
    dict(w=5, p=[[45.4079, 11.8720], [45.4098, 11.8712], [45.4118, 11.8702]]),  # Via Dante / San Fermo
    dict(w=5, p=[[45.4066, 11.8709], [45.4052, 11.8694], [45.4042, 11.8686]]),          # verso ovest
    dict(w=5, p=[[45.4090, 11.8788], [45.4084, 11.8820], [45.4079, 11.8846]]),          # Via Altinate
    dict(w=5, p=[[45.4074, 11.8747], [45.4077, 11.8735], [45.4079, 11.8720]]),          # le due piazze
    dict(w=5, p=[[45.3988, 11.8771], [45.3981, 11.8794], [45.3980, 11.8814]]),          # sotto il Prato
]
TRAM_TRACCIA = ([[45.4180, 11.8800]] + [[la, lo] for _n, la, lo in TRAM_FERMATE]
                + [[45.3946, 11.8780]])
ETICHETTE = [dict(t="EREMITANI", lat=45.4136, lon=11.8830, s=19),
             dict(t="CENTRO STORICO", lat=45.4100, lon=11.8688, s=19),
             dict(t="IL SANTO", lat=45.4000, lon=11.8840, s=18),
             dict(t="PORTELLO", lat=45.4082, lon=11.8862, s=16)]

# un tracciato per ciascun itinerario: cambiando itinerario cambia la linea rossa
_CENTRO   = [[45.4092, 11.8776], [45.4077, 11.8766]]                       # Corso Garibaldi -> Pedrocchi
_DA_STAZ  = [[45.4167, 11.8797], [45.4140, 11.8792], [45.4112, 11.8786]] + _CENTRO
_PIAZZE   = [[45.4073, 11.8760], [45.4074, 11.8747], [45.4077, 11.8735], [45.4079, 11.8720]]
_AL_DUOMO = [[45.4070, 11.8716], [45.4062, 11.8719], [45.40545, 11.87242], [45.4060, 11.8715], [45.4065, 11.8709]]
_AL_SANTO = [[45.4058, 11.8722], [45.4050, 11.8740], [45.4040, 11.8760], [45.4030, 11.8785], [45.4014, 11.8809]]
_AL_PRATO = [[45.4005, 11.8806], [45.3994, 11.8802], [45.3988, 11.8786], [45.3986, 11.8770]]

PERCORSI = {
    "a":   _DA_STAZ + [[45.4069, 11.8772]] + _PIAZZE + _AL_DUOMO + _AL_SANTO + [[45.4005, 11.8806]] + _AL_PRATO[1:],
    "b":   _DA_STAZ + _PIAZZE + _AL_DUOMO + _AL_SANTO + _AL_PRATO,
    # Ada: in tram fino al Santo, poi si risale in centro nell'ordine delle tappe
    # Santo -> Pedrocchi -> Signori -> pranzo -> Ragione -> Bo -> Prato
    "ada": [[45.4014, 11.8809], [45.4030, 11.8785], [45.4045, 11.8764], [45.4058, 11.8768],
            [45.4077, 11.8766],
            [45.4077, 11.8752], [45.4079, 11.8735], [45.4079, 11.8720],
            [45.4070, 11.8716], [45.4062, 11.8719], [45.40545, 11.87242],
            [45.4063, 11.8733], [45.4071, 11.8743], [45.4074, 11.8747],
            [45.4073, 11.8760], [45.4069, 11.8772],
            [45.4058, 11.8766], [45.4042, 11.8752], [45.4020, 11.8760],
            [45.4000, 11.8766], [45.3986, 11.8770]],
}

# =================================================================== stile
TOK = """  --ground:#EDEEE9; --surface:#F9F9F4; --surface-2:#F2F2EB;
  --land:#E5DFD3; --land-hi:#DBD4C5; --water:#93AEC6; --water-deep:#84A1BC;
  --road:#FCFBF6; --road-case:#CDC7B8;
  --ink:#22231E; --ink-soft:#66675D; --ink-faint:#93948A;
  --rule:#D5D3C6; --rule-soft:#E3E1D6;
  --route:#AF3A2D; --card:#2F5C93; --other:#6B8A3C; --food:#7B4B8A; --tram:#CE8F16; --bar:#1F7A7A;
  --marker-ring:#F9F9F4;
  --shadow:0 1px 2px rgba(34,35,30,.07), 0 6px 18px rgba(34,35,30,.06);"""
TOK_DARK = """  --ground:#16181A; --surface:#1D2022; --surface-2:#232729;
  --land:#2B2C27; --land-hi:#34352E; --water:#1B3142; --water-deep:#152838;
  --road:#494C44; --road-case:#212420;
  --ink:#E9E7DE; --ink-soft:#A2A398; --ink-faint:#787A70;
  --rule:#343836; --rule-soft:#282B2A;
  --route:#E2725E; --card:#7BABDA; --other:#A3C06C; --food:#C691D6; --tram:#E6B64B; --bar:#5FC3BE;
  --marker-ring:#16181A;
  --shadow:0 1px 2px rgba(0,0,0,.4), 0 6px 18px rgba(0,0,0,.35);"""

BASE_CSS = u"""
*{box-sizing:border-box}
body{margin:0;background:var(--ground);color:var(--ink);
  font-family:'Jost',system-ui,-apple-system,'Segoe UI',sans-serif;
  font-size:16px;line-height:1.55;-webkit-font-smoothing:antialiased}
img{max-width:100%%}
[hidden]{display:none!important}
a{color:inherit}
.wrap{max-width:%(maxw)s;margin:0 auto;padding-inline:20px;padding-block:24px 60px}

.sitenav{display:flex;flex-wrap:wrap;align-items:center;gap:9px;font-size:13px;letter-spacing:.03em;margin-bottom:20px}
.sitenav a{color:var(--ink-soft);text-decoration:none;border-bottom:1px solid transparent;padding-bottom:2px}
.sitenav a:hover{color:var(--ink);border-bottom-color:var(--rule)}
.sitenav a[aria-current]{color:var(--ink);font-weight:600}
.sitenav a:focus-visible{outline:2px solid var(--card);outline-offset:3px;border-radius:2px}
.sitenav .sep{color:var(--ink-faint)}

.masthead{border-bottom:1px solid var(--rule);padding-bottom:20px;margin-bottom:26px}
.eyebrow{font-size:12px;letter-spacing:.17em;text-transform:uppercase;color:var(--ink-faint);
  font-weight:600;margin:0 0 10px}
h1{font-family:'EB Garamond',Garamond,'Times New Roman',serif;font-weight:600;
  font-size:clamp(38px,7vw,60px);line-height:1.0;margin:0;letter-spacing:-.012em;text-wrap:balance}
h1 em{font-style:italic;color:var(--route)}
.standfirst{margin:14px 0 0;max-width:64ch;color:var(--ink-soft);font-size:16.5px}
.standfirst a{color:var(--ink);text-underline-offset:3px}

.legend{display:flex;flex-wrap:wrap;gap:7px;margin:18px 0 0;padding:0;list-style:none}
.legend li{display:inline-flex;align-items:center;gap:8px;border:1px solid var(--rule);
  background:var(--surface);border-radius:999px;padding:5px 13px 5px 10px;
  font-size:13px;color:var(--ink-soft)}
.legend i{width:11px;height:11px;border-radius:50%%;background:var(--c);flex:none}
.legend i.dia{border-radius:0;width:13px;height:13px;clip-path:polygon(50%% 0%%,100%% 50%%,50%% 100%%,0%% 50%%)}
.legend i.bar{width:20px;height:4px;border-radius:2px}

footer{margin-top:40px;padding-top:18px;border-top:1px solid var(--rule);
  font-size:13px;color:var(--ink-faint);max-width:80ch}
footer p{margin:0 0 8px}
footer a{color:var(--ink-soft)}
footer b{color:var(--ink-soft)}
@media (prefers-reduced-motion: reduce){*{transition:none!important}}
"""

NAV_PAGES = [("home", u"EPPHURE · la mappa"), ("giornata", u"La giornata"),
             ("card", u"Padova Card"), ("altri", u"Altri luoghi")]
HREF = {
    "root":   {"home": "./", "giornata": "padova/", "card": "padova/padova-card.html", "altri": "padova/altri-luoghi.html"},
    "padova": {"home": "../", "giornata": "./", "card": "padova-card.html", "altri": "altri-luoghi.html"},
}


def nav(cur, dove="padova"):
    out = []
    for key, label in NAV_PAGES:
        cu = ' aria-current="page"' if key == cur else ''
        out.append(u'    <a href="%s"%s>%s</a>' % (HREF[dove][key], cu, label))
    sep = u'\n    <span class="sep">/</span>\n'
    return u'  <nav class="sitenav">\n' + sep.join(out) + u'\n  </nav>'


def page(title, desc, css, body, maxw="900px"):
    return u"""<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>%(title)s</title>
<meta name="description" content="%(desc)s">
<meta property="og:title" content="%(title)s">
<meta property="og:description" content="%(desc)s">
<meta property="og:type" content="website">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,500;0,600;1,500&family=Jost:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap">
<style>
:root{
  color-scheme: light dark;
  padding-top: env(safe-area-inset-top, 0px);
  padding-bottom: env(safe-area-inset-bottom, 0px);
%(tok)s
}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){
%(tokd)s
}}
:root[data-theme="dark"]{
%(tokd)s
}
%(base)s
%(css)s
</style>
</head>
<body>
%(body)s
</body>
</html>
""" % dict(title=title, desc=desc, tok=TOK, tokd=TOK_DARK,
           base=BASE_CSS % dict(maxw=maxw), css=css, body=body)


def write(name, text):
    io.open(os.path.join(HERE, name) if not name.startswith('..') else os.path.abspath(os.path.join(HERE, name)), 'w', encoding='utf-8', newline='\n').write(text)
    return len(text.encode('utf-8')) / 1024.0


def eur(n):
    return (u"%d,00 €" % n) if n == int(n) else (u"%.2f €" % n).replace(".", ",")


# =================================================================== la mappa (SVG)
def numeri():
    """id del luogo -> {'a': n|None, 'b': n|None}. La stazione conta una volta sola."""
    out = dict((k, {}) for k in PLACES)
    for v in VARIANTI:
        n = 0
        visti = set()
        for pid, _ora, _dur, _cost in v['tappe']:
            if pid in visti:
                continue
            visti.add(pid)
            n += 1
            out[pid][v['id']] = n
    for k in out:
        out[k].setdefault('a', None)
        out[k].setdefault('b', None)
    return out


NUM = numeri()


def extra_markers():
    """I luoghi delle due tabelle che non sono gia' tappe dell'itinerario."""
    out = []
    for s in CARD_SITI:
        if not s.get('tappa'):
            out.append((s, 'card'))
    for s in ALTRI_LUOGHI:
        if not s.get('tappa'):
            out.append((s, 'other'))
    return out


def build_map(interactive=True, mini=False):
    g = []
    g.append('<rect width="%d" height="%d" fill="var(--land)"/>' % (VW, VH))
    # l'anello dei canali chiude il centro storico: dentro e' un'isola
    g.append('<path d="%s" fill="var(--land-hi)"/>' % smooth(CANALE, True))
    g.append('<path d="%s" fill="none" stroke="var(--water)" stroke-width="15" stroke-linejoin="round"/>' % smooth(CANALE, True))
    for r in RAMI:
        g.append('<path d="%s" fill="none" stroke="var(--water)" stroke-width="15" stroke-linecap="round"/>' % smooth(r))
    if not mini:
        for st in STRADE:
            g.append('<path d="%s" fill="none" stroke="var(--road-case)" stroke-width="%d" stroke-linecap="round" stroke-linejoin="round" opacity=".5"/>' % (smooth(st['p']), st['w'] + 3))
        for st in STRADE:
            g.append('<path d="%s" fill="none" stroke="var(--road)" stroke-width="%d" stroke-linecap="round" stroke-linejoin="round"/>' % (smooth(st['p']), st['w']))
        g.append('<g id="tram"><path d="%s" fill="none" stroke="var(--marker-ring)" stroke-width="11" stroke-linecap="round" opacity=".6"/>' % poly(TRAM_TRACCIA))
        g.append('<path d="%s" fill="none" stroke="var(--tram)" stroke-width="5" stroke-linecap="round" stroke-dasharray="1 11" stroke-linejoin="round"/>' % poly(TRAM_TRACCIA))
        for nm, la, lo in TRAM_FERMATE:
            g.append('<circle cx="%.0f" cy="%.0f" r="5.5" fill="var(--marker-ring)" stroke="var(--tram)" stroke-width="2.6"><title>%s — tram SIR1</title></circle>' % (px(lo), py(la), nm))
        g.append('</g>')
        for e in ETICHETTE:
            g.append('<text class="maplabel" x="%.0f" y="%.0f" font-size="%d">%s</text>' % (px(e['lon']), py(e['lat']), e['s'], e['t']))
    # un tracciato per itinerario: la pagina ne mostra uno per volta
    for vid, pts in PERCORSI.items():
        vis = '' if (vid == 'a' or mini) else ' hidden="hidden"'
        op = ' opacity=".5"' if (mini and vid != 'a') else ''
        g.append('<g class="rt" data-v="%s"%s%s>' % (vid, vis, op))
        g.append('<path d="%s" fill="none" stroke="var(--marker-ring)" stroke-width="%d" stroke-linecap="round" stroke-linejoin="round" opacity=".75"/>'
                 % (smooth(pts), 16 if not mini else 20))
        g.append('<path class="routeline" d="%s" fill="none" stroke="var(--route)" stroke-width="%d" stroke-linecap="round" stroke-linejoin="round"/>'
                 % (smooth(pts), 8 if not mini else 12))
        g.append('</g>')
        if mini:
            break
    # gli altri luoghi
    if not mini:
        for s, kind in extra_markers():
            x, y = px(s['lon']) + s.get('dx', 0), py(s['lat']) + s.get('dy', 0)
            col = 'var(--card)' if kind == 'card' else 'var(--other)'
            op = ' opacity=".45"' if s.get('escluso') else ''
            if s.get('tipo') == 'bar':
                col = 'var(--bar)'
                shape = '<rect x="%.0f" y="%.0f" width="23" height="23" rx="5" fill="%s" stroke="var(--marker-ring)" stroke-width="3"%s/>' % (x - 11.5, y - 11.5, col, op)
            elif kind == 'card':
                shape = '<path d="M0 -14 L14 0 L0 14 L-14 0 Z" transform="translate(%.0f,%.0f)" fill="%s" stroke="var(--marker-ring)" stroke-width="3"%s/>' % (x, y, col, op)
            else:
                shape = '<circle cx="%.0f" cy="%.0f" r="12" fill="%s" stroke="var(--marker-ring)" stroke-width="3"%s/>' % (x, y, col, op)
            g.append('<g class="small">%s<title>%s</title></g>' % (shape, s['nome']))
    # le tappe
    for pid in ORDINE_MAPPA:
        pl = PLACES[pid]
        na, nb = NUM[pid]['a'], NUM[pid]['b']
        x, y = px(pl['lon']), py(pl['lat'])
        fill = 'var(--food)' if pl.get('pasto') else 'var(--route)'
        r = 21 if not mini else 26
        ring = ('<circle cx="%.0f" cy="%.0f" r="%.0f" fill="none" stroke="var(--card)" stroke-width="3"/>' % (x, y, r + 5)) if pl['card'] else ''
        prima = na or nb or NUM[pid].get('ada')
        num = '' if mini else '<text class="num" x="%.0f" y="%.0f">%s</text>' % (x, y, prima or '')
        if interactive:
            tag = ('g class="marker" data-p="%s" data-a="%s" data-b="%s" data-ada="%s" '
                   'tabindex="0" role="button" aria-label="%s"'
                   % (pid, na or '', nb or '', NUM[pid].get('ada') or '', pl['nome']))
        else:
            tag = 'g'
        g.append('<%s>%s<circle class="halo" cx="%.0f" cy="%.0f" r="%.0f"/>'
                 '<circle class="pin" cx="%.0f" cy="%.0f" r="%.0f" fill="%s"/>%s</g>'
                 % (tag, ring, x, y, r + 14, x, y, r, fill, num))
    if not mini:
        sbw = (250.0 / (111320 * math.cos(math.radians(45.407)))) * SX
        sx, sy = 36, VH - 40
        g.append('<g opacity=".85"><line x1="%d" y1="%d" x2="%.0f" y2="%d" stroke="var(--ink-soft)" stroke-width="3"/>'
                 '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="var(--ink-soft)" stroke-width="3"/>'
                 '<line x1="%.0f" y1="%d" x2="%.0f" y2="%d" stroke="var(--ink-soft)" stroke-width="3"/>'
                 '<text class="scaletxt" x="%d" y="%d">250 m</text></g>'
                 % (sx, sy, sx + sbw, sy, sx, sy - 7, sx, sy + 7, sx + sbw, sy - 7, sx + sbw, sy + 7, sx, sy - 13))
        g.append('<g opacity=".7" transform="translate(%d,%d)"><path d="M0 -24 L7.5 9 L0 2.5 L-7.5 9 Z" fill="var(--ink-soft)"/>'
                 '<text class="scaletxt" x="0" y="26" text-anchor="middle">N</text></g>' % (VW - 46, VH - 50))
    return ''.join(g)


MAP_CSS = u"""
.mapframe{background:var(--land);border:1px solid var(--rule);border-radius:3px;
  overflow:hidden;box-shadow:var(--shadow);line-height:0}
svg.map{display:block;width:100%;height:auto;max-width:100%;touch-action:manipulation}
.marker{cursor:pointer}
.marker .halo{fill:var(--route);opacity:0;transition:opacity .18s}
.marker .pin{stroke:var(--marker-ring);stroke-width:3.5}
.marker .num{fill:var(--marker-ring);font-family:'Jost',sans-serif;font-weight:600;font-size:23px;
  text-anchor:middle;dominant-baseline:central;pointer-events:none}
.marker:hover .halo,.marker.on .halo{opacity:.22}
.marker:focus-visible{outline:none}
.marker:focus-visible .halo{opacity:.3}
.maplabel{fill:var(--ink-soft);font-family:'Jost',sans-serif;font-weight:600;
  font-size:19px;letter-spacing:.2em;text-anchor:middle;pointer-events:none;opacity:.55}
.scaletxt{fill:var(--ink-soft);font-family:'Jost',sans-serif;font-size:17px;font-weight:500;opacity:.8}
.mapnote{margin:11px 2px 0;font-size:12.5px;line-height:1.5;color:var(--ink-faint);max-width:58ch}
"""
