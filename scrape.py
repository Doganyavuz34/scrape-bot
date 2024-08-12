# -*- coding: utf-8 -*-
"""
Created on Tue May 14 15:19:44 2024

@author: Fujitsu
"""

import pandas as pd
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import telegram
import time as t

urunler = pd.read_excel("urun_listesi.xlsx")
base_url = "https://www.amazon.com.tr/dp/"

cookies = {
    'session-id': '258-4571020-0927405',
    'i18n-prefs': 'TRY',
    'ubid-acbtr': '259-5040866-4995800',
    'csm-hit': 'tb:E2R8KF07ATPYXYQNYXXN+b-5FWREBKE4E4WCYBHAZZA|1715690585275&t:1715690585275&adb:adblk_no',
    'session-token': '"ilGAeG1eI4MluQxCFibuwA6/F18AVqeM5Ndw3Ejkj4UCL98g7hgcuodsi0rcWw0mlBpFeJN3njlYsLlZZpVVeLTTrAkmcKyQT1e6Xxl8s5Mi7B6WGH/A3i/ZKK59CZ0o4Zs0hDxeboOeGArt/XzyBqbn2Y7dhCEcafoogM2D8Rt600ZNb4+FwM4ku7uL7dYTL4uRG/nyKKczficmaEm0r1kqwv6BrtyFBj3NtXvMplts9R1qp4d2xd9FYuwPqghiXlwTEcT8LbUo5LB2Pyo5uy8pAgIXMqL0KKODiw5MpK4WIPAiFxHKUOiHg9qzTDYDE9YHYlPexPSduS4VtDCiFgsp1tqvma9FkpKpNUW983o="',
    'session-id-time': '2082758401l',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'tr-TR,tr;q=0.9',
    'cache-control': 'max-age=0',
    # 'cookie': 'session-id=258-4571020-0927405; i18n-prefs=TRY; ubid-acbtr=259-5040866-4995800; csm-hit=tb:E2R8KF07ATPYXYQNYXXN+b-5FWREBKE4E4WCYBHAZZA|1715690585275&t:1715690585275&adb:adblk_no; session-token="ilGAeG1eI4MluQxCFibuwA6/F18AVqeM5Ndw3Ejkj4UCL98g7hgcuodsi0rcWw0mlBpFeJN3njlYsLlZZpVVeLTTrAkmcKyQT1e6Xxl8s5Mi7B6WGH/A3i/ZKK59CZ0o4Zs0hDxeboOeGArt/XzyBqbn2Y7dhCEcafoogM2D8Rt600ZNb4+FwM4ku7uL7dYTL4uRG/nyKKczficmaEm0r1kqwv6BrtyFBj3NtXvMplts9R1qp4d2xd9FYuwPqghiXlwTEcT8LbUo5LB2Pyo5uy8pAgIXMqL0KKODiw5MpK4WIPAiFxHKUOiHg9qzTDYDE9YHYlPexPSduS4VtDCiFgsp1tqvma9FkpKpNUW983o="; session-id-time=2082758401l',
    'device-memory': '8',
    'downlink': '9.25',
    'dpr': '1.5',
    'ect': '4g',
    'priority': 'u=0, i',
    'rtt': '100',
    'sec-ch-device-memory': '8',
    'sec-ch-dpr': '1.5',
    'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-ch-ua-platform-version': '"10.0.0"',
    'sec-ch-viewport-width': '231',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'viewport-width': '231',
}

class TELEGRAM():
    def send_message(msg, urun_foto):
        user_id = 6801076365 # USER ID DEĞİŞTİR!
        BOT_TOKEN = "6678794985:AAHXKmbZOMZ8bP0m6s8TBCepui162sA6l60" # BOT TOKEN DEĞİŞTİR!
        bot = telegram.Bot(token = BOT_TOKEN)
        
        bot.sendPhoto(chat_id=user_id, caption=msg, 
                      parse_mode = telegram.ParseMode.HTML,
                      photo=urun_foto)
        
    
    def prepare_message(urun_adi, urun_foto, urun_fiyati, hedef_fiyat, urun_link):
        msg = "\n<b><a href='" + urun_link + "'>"  + urun_adi + "</a></b>\n\n"
        msg += "Hedef Fiyat: " + str(hedef_fiyat) + "\n"
        msg += "Güncel Fiyat: " + str(urun_fiyati) + "\n"
        indirim_orani = "%" + str(round(100 - ((urun_fiyati * 100)/hedef_fiyat), 2))
        msg += "İndirim Oranı: " + indirim_orani
        TELEGRAM.send_message(msg, urun_foto)

while True:
    for row in urunler.iterrows():
        idx = row[0]
        urun_kodu = row[1]["URUN_KODU"]
        hedef_fiyat = row[1]["HEDEF_FIYAT"]
        response = requests.get(base_url + urun_kodu, cookies=cookies, headers=headers)
        if(response.status_code == 200):
            # İstek başarılı
            source = BeautifulSoup(response.content, "html.parser")
            fiyat_kutusu = source.find("div", attrs={"class":"a-box-group"})
            urun_fiyati = fiyat_kutusu.find("span", attrs={"class":"a-offscreen"}).text
            urun_fiyati = float(urun_fiyati.split("TL")[0].replace(".","").replace(",","."))
            urun_adi = source.find("span", attrs={"id":"productTitle"}).text.strip()
            urun_foto = source.find("img", attrs={"data-a-image-name": "landingImage"})["src"]
            urun_link = base_url + urun_kodu
            if(urun_fiyati < hedef_fiyat):
                # Telegram Mesajı Gönder...
                TELEGRAM.prepare_message(urun_adi, urun_foto, urun_fiyati, hedef_fiyat, urun_link)
                urunler.at[idx, "HEDEF_FIYAT"] = urun_fiyati
                zaman = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
                print(zaman + " " + "Mesaj gönderildi...")
            else:
                zaman = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
                print(zaman + " " + urun_kodu + " -> " + "Ürün fiyatı hedef fiyatın üstünde")
        else:
            # İstek Başarısız.
            zaman = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
            print(zaman + " " + str(response.status_code))
        t.sleep(2)
    
    
    
    
    
    
    
    
    
    
    
    