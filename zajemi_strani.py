import re
import requests
import os
import csv

# Fukcije url_to_text, zapisi_csv in zapisi_v_csv so pobrane z repozitorija od predmeta Programiranje 1.

STEVILO_STRANI = 166
mapa = 'zajeti_podatki'
linki = 'linki.txt'
nepremicnine_txt = 'nepremicnine.txt'
nepremicnine_csv = 'nepremicnine.csv'
vzorec_linka = r'<meta itemprop="mainEntityOfPage" content="https://www.nepremicnine.net/oglasi-prodaja/(.*)" />'
vzorec_lastnosti = (
    r'<div class="more_info">Posredovanje: (.*?) '
    r'\| Vrsta: (.*?) '
    r'\| Regija: (?P<regija>.*?) '
    r'\| Upravna enota: (?P<upravna_enota>.*?) '
    r'\| Občina: (?P<obcina>.*?)'
    r'</div><div class="main-data">.*?'
    r'<div class="kratek" itemprop="description"><strong class="rdeca">(?P<kraj>.*?)</strong>, '
    r'((?P<povrsina>[\d,.]*) m2, )?.*?'
    r'((?P<vrsta_hise>.*?), )?.*?'
    r'l. (?P<leto>[0-9]{4}),.*?'
    r'( adaptiran[oa] l. (?P<adaptirana>[0-9]{1,4}),)?.*?'
    r'( (?P<zemljisce>[\d.,]*) m2 zemljišča,)?.*?'
    r'(.ena:(.*?)? (?P<cena>[\d,.]* EUR(/m2)?))?<'
)

def url_to_text(url):
    '''Funkcija, ki sprejme url naslov strani, stran pobere in pretvori v niz.'''
    try:
        vsebina_strani = requests.get(url)
    except requests.exceptions.ConnectionError:
        print('Prišlo je do napake pri povezovanju.')
        return None
    if vsebina_strani.status_code == requests.codes.ok:
        return vsebina_strani.text
    print('Težave pri vsebini strani')
    return None

def zajemi_linke(mapa, datoteka_z_linki):
    '''Funkcija, ki s strani pobere linke do nepremičnin, ki jih kasneje uporabimo za pridobitev podatkov, in jih zapiše v datoteko.'''
    os.makedirs(mapa, exist_ok=True)
    pot = os.path.join(mapa, datoteka_z_linki)
    if os.path.exists(pot): # če obstaja datoteka z linki jo izbrišemo; datoteko pri vsaki uporabi na novo ustvarimo, da se izognemo nedelujočim linkom
        os.remove(pot)
    for stran in range(1, STEVILO_STRANI+1):  
        url = f'https://www.nepremicnine.net/oglasi-prodaja/slovenija/hisa/{stran}/?s=1'
        vsebina = url_to_text(url)
        for link in re.findall(vzorec_linka, vsebina):
            with open(pot, 'a', encoding='utf-8') as f:
                print(link, file=f)
    return None

def poberi_podatke(mapa, datoteka_z_linki, datoteka_z_nepremicninami):
    '''Funkcija, ki iz spletnih strani, navedenih v datoteki z linki, pobere podatke, jih zapiše v pomožno datoteko in vrne seznam slovarjev s podatki.'''
    zajemi_linke(mapa, datoteka_z_linki)
    oglasi = []
    with open(os.path.join(mapa, datoteka_z_linki)) as f:
        for link in f:
            podatki_hise = {}
            text = url_to_text(f'https://www.nepremicnine.net/oglasi-prodaja/{link}')
            id_hise = re.findall(r'\d{7}', link)[0] # id hiše preberemo iz linka
            podatki_hise['id'] = id_hise
            lastnosti = re.search(vzorec_lastnosti, text, re.DOTALL)
            try:
                podatki_hise.update(lastnosti.groupdict())
            except:
                pass
            oglasi.append(podatki_hise)
            with open(os.path.join(mapa, datoteka_z_nepremicninami), 'a', encoding='utf-8') as dat: # ustvari pomozno datoteko, v kateri so zapisani slovarji s podatki o nepremičninah, z namenom preverjanja pravilnosti pobranih podatkov
                print(podatki_hise, file=dat)
    return oglasi

def zapisi_csv(glava, vrstice, mapa, datoteka_z_nepremicninami):
    pot = os.path.join(mapa, datoteka_z_nepremicninami)
    with open(pot, 'w', encoding='utf-8', newline='') as dat:
        writer = csv.DictWriter(dat, fieldnames=glava)
        writer.writeheader()
        for vrstica in vrstice:
            if vrstica['povrsina'] != None:
                vrstica['povrsina'] = float(vrstica['povrsina'].replace('.', '').replace(',', '.'))
            if vrstica['zemljisce'] != None:
                vrstica['zemljisce'] = float(vrstica['zemljisce'].replace('.', '').replace(',', '.'))
            if vrstica['cena'] != None:
                prebrana_cena = vrstica['cena']
                cena = float(prebrana_cena.split(',')[0].replace('.', ''))
                if '/m2' in prebrana_cena:
                    nova_cena = float(vrstica['povrsina'] * cena)
                    vrstica['cena'] = nova_cena
                else:
                    vrstica['cena'] = cena
            writer.writerow(vrstica)
    return None

def zapisi_v_csv(oglasi, mapa, datoteka_z_nepremicninami):
    assert oglasi and (all(j.keys() == oglasi[0].keys() for j in oglasi))
    zapisi_csv(oglasi[0].keys(), oglasi, mapa, datoteka_z_nepremicninami)

def main():
    podatki = poberi_podatke(mapa, linki, nepremicnine_txt)
    zapisi_v_csv(podatki, mapa, nepremicnine_csv)

main() 