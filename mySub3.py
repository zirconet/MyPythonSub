#!/usr/bin/python
'''
Programma per controllo stato sottotitoli in Subspedia
ver. 1.0 (28/01/17)
By Zirconet - 28-01-2017
'''

import zipfile
import subprocess
import time
import os, sys
import urllib
import requests
from bs4 import BeautifulSoup

def TraduttoriAnonimi():
    
    url = "http://www.traduttorianonimi.it"
    pezzo1 = "http://www.traduttorianonimi.it/data/srt/"
    pezzo2 = "-traduttorianonimi.it.zip"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "lxml")
    g_data = soup.find_all("div", id="le_table_container")
    
    path = '/mnt/usb/0tv/' 
    subdirectories =  os.listdir(path)

    for item in subdirectories:
        parte = item[:8]
        primo = 'S00'
        secondo = '00'
        dirname = item
        dirdir = path+item
        nomefile = dirdir+'/'+'ciao.zip'
        nuovadir = path+"0_subbed "+dirname

        if parte == '0_subbed':
            seriedacercare = 'niente'
            
        if parte <> '0_subbed':
            seriedir = os.walk(dirdir).next()[1]
            accio = ''.join(seriedir)
            print accio
            srt = accio.find('S0')
            if srt < 0:
                break
            Listn = accio.split('.')
            nome = accio[:srt-1]
            nome = nome.replace('.','-')
            for x in Listn:
                if x.find('S0') == 0:
                    primo = x[2:3]
                    secondo = x[4:]
		    secondo = secondo.replace('E','')
                    numero = primo +'x'+secondo

            seriedacercare = item + ' - '+numero
            print "-------->>>>>>>>"+seriedacercare

            
        for item in g_data:
 
            for image in item.findAll("img", title=seriedacercare):
                if image:
                    url = pezzo1+nome+'-'+numero+pezzo2
                    print url
                    myfile = urllib.URLopener()
                    myfile.retrieve(url, nomefile)
                    print 'deflating zip file'
                    zip = zipfile.ZipFile(nomefile)
                    zip.extractall(dirdir)
                    os.remove(nomefile)
                    os.rename((dirdir),(nuovadir))
                    messaggio = "Trovato nuovo sottotitolo per "+seriedacercare
		    subprocess.Popen(["/mnt/usb/telegram.sh", messaggio]) 
            break





