#!/usr/bin/python
'''
Programma per scarico sottotitoli da Subspedia
ver. 1.5 (28/01/17)
By Zirconet - 07-01-2017
'''
import mySub2
import mySub3
import mySub4
import zipfile
import subprocess
import time
import os, sys
import urllib
import requests
from bs4 import BeautifulSoup

url = "http://www.subspedia.tv/index.php"
r = requests.get(url)
soup = BeautifulSoup(r.content, "lxml")
g_data = soup.find_all("table", {"class": "subHomeContainer"})
control ='___'

path = '/mnt/usb/0tv/'
subdirectories =  os.listdir(path)

t = time.localtime()
timestamp = time.strftime('%d-%b-%Y %H:%M', t)
log = timestamp+' starting mySub\n'
out_file=open("/var/log/mySub.log", "a")
out_file.write(log)
out_file.close() 

for item in subdirectories:
    seriedacercare = item
    dirname = seriedacercare

    if seriedacercare.find(control) >0:
	cc = seriedacercare.find(control)
	seriedacercare = seriedacercare[:cc]

    f = open('/mnt/usb/except','r')
    xxx = [x for x in f.readlines()]  
    f.close()
    for x in xxx:
     eccept = x.split(";")
     if eccept[0] == seriedacercare:
        seriedacercare = eccept[1]
   
    print seriedacercare 
    aList = []

    for item in g_data:
        links = item.contents[1].find_all("a", text=seriedacercare)
	
        for link in links:
                xxx = item.contents[3].find_all("a", href=True)
                for link in xxx:
                        trovo = link["href"]
                        aList.append(trovo);
	        
                str0 = aList [0]
                str1 = str0.replace('javascript:downloadSub("', '')
                str2 = str1.replace(');','')
                str = str2.replace('"','')
                data = str.split(',')

		filename = data[0].split('/')
                nomefile = path+dirname+'/'+filename[1]
		print nomefile
                
                sito = "http://www.subspedia.tv/scaricaSub.php?path="
                url = sito+data[0]+'&serie='+data[1]+'&stagione='+data[2]+'&numero='+data[3]

                myfile = urllib.URLopener()
                myfile.retrieve(url, nomefile)
		
		vecchiadir= path+dirname
		nuovadir = path+"0_subbed "+dirname
		nuovonomefile = nuovadir+'/'+filename[1]
		xzip = nuovonomefile[-3:]

		os.rename((vecchiadir),(nuovadir))
		
		if xzip == 'zip':
			print 'deflating zip file'
			zip = zipfile.ZipFile(nuovonomefile)
			zip.extractall(nuovadir)
			os.remove(nuovonomefile)

		messaggio = "Trovato nuovo sottotitolo per "+seriedacercare
		subprocess.Popen(["/mnt/usb/telegram.sh", messaggio]) 

mySub2.StatoTrad()
mySub3.TraduttoriAnonimi()
mySub4.StatoTradAnonimi()

