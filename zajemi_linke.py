import re
import requests
import os

STEVILO_STRANI = 122
vzorec_linka = r'<meta itemprop="mainEntityOfPage" content="https://www.nepremicnine.net/oglasi-prodaja/(?P<url_oglasa>.*)" />'
pot = os.path.join('zajeti_podatki', 'linki.txt')

def zajemi_stran(url):
    '''Funkcija, ki sprejme url naslov strani, stran pobere in pretvori v niz.'''
    try:
        vsebina_strani = requests.get(url)
    except requests.exceptions.ConnectionError:
        print('Prišlo je do napake pri povezovanju.')
        return None
    # nadaljujemo s kodo če ni prišlo do napake
    if vsebina_strani.status_code == requests.codes.ok:
        with open('url.html', 'w', encoding='utf-8') as f:
            f.write(vsebina_strani.text)
        return vsebina_strani.text
    print('Težave pri vsebini strani')
    return None

def zajemi_linke():
    '''Funkcija, ki s strani pobere linke do nepremičnin, ki jih kasneje uporabimo za pridobitev podatkov, in jih zapiše v datoteko.'''
    for stran in range(1, STEVILO_STRANI+1):  
        url = f'https://www.nepremicnine.net/oglasi-prodaja/slovenija/hisa/samostojna/{stran}/?s=1'
        vsebina = zajemi_stran(url)
        for link in re.findall(vzorec_linka, vsebina):
            with open(pot, 'a', encoding='utf-8') as f:
                print(link, file=f)
    return None

zajemi_linke()