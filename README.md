# Prodaja nepremičnin
Analiziral bom vnose nepremičnin na prodaj na spletnem portalu [nepremicnine.net](https://www.nepremicnine.net/oglasi-prodaja/)
## Zajeti podatki
Pri zajemanju podatkov se bom omejil na hiše zgrajene v Sloveniji, za vsako pa bom zajel:
- njen id
- vrsto (samostojna, vrstna itd.)
- lokacijo (regijo, upravno enoto, občino in kraj)
- ceno
- površino objekta in morebitnega zemljišča
- leto izgradnje in adaptacije

Podatke zajamemo tako, da poženemo datoteko *zajemi_strani.py*. Podatki so shranjeni v mapi zajeti_podatki, v datoteki *linki.txt* se nahajajo linki s katerih pobiramo podatke, datoteka *nepremicnine.txt* je pomožna pri izvajanju programa, v njej sproti preverjamo, če so zajeti podatki pravilni, prav tako spremljamo potek zajemanja, urejeni podatki so zapisani v datoteki *nepremicnine.csv*.
## Hipoteze
S pomočjo zajetih podatkov bom poskušal odgovoriti na naslednja vprašanja:
- Kako je cena nepremičnine odvisna od lokacije?
- Kako sta povezana lokacija in velikost objekta in zemljišča?
- V katerih krajih se prodaja največ nepremičnin?
- Kako je vrsta nepremičnine odvisna od lokacije?
- Kako je cena odvisna od leta izgradnje in adaptacije?
