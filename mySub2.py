#!/usr/bin/python
'''
Programma per controllo stato sottotitoli in Subspedia
ver. 1.0 (28/01/17)
By Zirconet - 28-01-2017
'''

import os, sys
import urllib
import requests
from bs4 import BeautifulSoup

def StatoTrad():   
    url = "http://www.subspedia.tv/traduzioni.php"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "lxml")
    g_data = soup.find_all("div", {"class": "itemListaSerie"})

    path = '/mnt/usb/0tv/'
    control = '___'
    subdirectories =  os.listdir(path)

    for item in subdirectories:
        dirname = item
        vecchiadir= path+dirname
        seriedacercare = dirname

        if dirname.find(control) >0:
            cc = dirname.find(control)
            seriedacercare = dirname[:cc-1]

        for item in g_data:
            
            imgs = item('img', alt=seriedacercare)
            txt = item.find('span').text
            if imgs:
                if txt[4:9] == 'revis':
                    nuovadir = path+seriedacercare+' ___in rev '+txt[17:22]+' (Suspedia)'
                    os.rename((vecchiadir),(nuovadir))
                    print seriedacercare+' in revisione'
                if txt[4:9] == 'tradu':
                    nuovadir = path+seriedacercare+' ___in trad '+txt[17:23]+' (Suspedia)'
                    os.rename((vecchiadir),(nuovadir))
                    print seriedacercare+' in traduzione'        
        
    print '--> ricercato stato sottotitoli' 
 	        
             



