import re

vzorec_lokacije = (
    r'<div class="more_info">Posredovanje: (.*?) '
    r'\| Vrsta: (.*?) '
    r'\| Regija: (?P<regija>.*?) '
    r'\| Upravna enota: (?P<upravna_enota>.*?) '
    r'\| Občina: (?P<obcina>.*?)'
    r'</div><div class="main-data">'
)

# <div class="more_info">Posredovanje: (.*?) \| Vrsta: (.*?) \| Regija: (?P<regija>.*?) \| Upravna enota: (?P<upravna_enota>.*?) \| Občina: (?P<obcina>.*?)</div><div class="main-data">

vzorec_lastnosti = (
    r'<div class="kratek" itemprop="description"><strong class="rdeca">(?P<kraj>.*?)</strong>, '
    r'(?P<povrsina>[\d,]*) m2, .*?'
    r'l. (?P<leto>[0-9]{4}),.*?'
    r'( adaptiran[oa] l. (?P<adaptirana>[0-9]{1,4}),)?.*?'
    r'( (?P<zemljisce>\d{0,3}\.?\d{0,3}) m2 zemljišča,)?.*?'
    r'Cena: (?P<cena>[\d,.]*) EUR</div>'
)

# <div class="kratek" itemprop="description"><strong class="rdeca">(?P<kraj>.*?)</strong>, (?P<povrsina>[\d,]*) m2, .*?l. (?P<leto>[0-9]{4}),.*?( adaptiran[oa] l. (?P<adaptirana>[0-9]{1,4}),)?.*?( (?P<zemljisce>\d{0,3}\.?\d{0,3}) m2 zemljišča,)?.*?Cena: (?P<cena>[\d,.]*) EUR</div>

vzorec_energijskega_razreda = r'Energ. razred:.*?<div class=".*?">(.*?)</div>'


