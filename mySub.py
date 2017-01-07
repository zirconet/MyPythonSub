#!/usr/bin/python
'''
Programma per scarico sottotitoli da Subspedia
ver. 0.9
By Zirconet - 07-01-2017
'''

import os, sys
import urllib
import requests
from bs4 import BeautifulSoup

url = "http://www.subspedia.tv/index.php"
r = requests.get(url)
soup = BeautifulSoup(r.content, "lxml")
g_data = soup.find_all("table", {"class": "subHomeContainer"})

path = '/mnt/usb/0tv/'
subdirectories =  os.listdir(path)

for item in subdirectories:
    seriedacercare = item 
    print seriedacercare 
    aList = []
    for item in g_data:
        links = item.contents[1].find_all("a", text=seriedacercare)
	
        for link in links:
                xxx = item.contents[3].find_all("a", href=True)
                for link in xxx:
                        cazzo = link["href"]
                        aList.append(cazzo);
	        
                str0 = aList [0]
                str1 = str0.replace('javascript:downloadSub("', '')
                str2 = str1.replace(');','')
                str = str2.replace('"','')
                data = str.split(',')

		filename = data[0].split('/')
                nomefile = path+seriedacercare+'/'+filename[1]
		print nomefile
                
                sito = "http://www.subspedia.tv/scaricaSub.php?path="
                url = sito+data[0]+'&serie='+data[1]+'&stagione='+data[2]+'&numero='+data[3]

                myfile = urllib.URLopener()
                myfile.retrieve(url, nomefile)
		
		os.rename((path+seriedacercare),(path+"0subbed "+seriedacercare))



