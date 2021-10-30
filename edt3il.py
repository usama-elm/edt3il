from bs4 import BeautifulSoup
import numpy as np
import re as re
from datetime import datetime
import csv


# import math as m
import requests
#Recuperation de la page web
url = "http://eleves.groupe3il.fr/edt_eleves/00_index.php?idGroupe=I2+Groupe+1.xml"
req = requests.get(url)
soup = BeautifulSoup(req.text, "html.parser")
trait = soup.body
#On traite les infos, on prends tous les strings (stripped ou traités) et on les mets dans un array
var = []
for string in trait.stripped_strings:
    if(string=="Horaire"):
        var.append("Eliminer")
    else:
        var.append(string)
#On fait un 2eme traitement, et on élimine toutes les données inutiles qui appartienent au navbar ou autre
#On coupe en semaine, 1 
num=np.isin(var,"Eliminer")
lanum=[]
for i in range(len(num)):
    if num[i]==True:
        lanum.append(i)
lanum.append(len(var))
      
neovar=[]
for i in range(len(lanum)-1):
    neovar.append(var[lanum[i]+7:lanum[i+1]-1])


bt=-1
count=-1
letr=np.zeros((200,6),dtype=object)
jours=["Lundi","Mardi","Mercredi","Jeudi","Vendredi"]
for e in neovar:
    for i in range(len(e)):
        if e[i] in jours:
            bt+=1
            count=-1
        print(bt,count)
        print(e[i])
        count+=1
        letr[bt][count]=e[i]

for i in range(len(letr)):
    if letr[i][5]!=0:
        if "h" in letr[i][5]:
            letr[i][4]=letr[i][5]
            letr[i][5]=0
    if letr[i][3]!=0:     
        if "h" in letr[i][3]:
            letr[i][4]=letr[i][3]
            letr[i][3]=0
    if letr[i][2]!=0:
        if "h" in letr[i][2]:
            letr[i][4]=letr[i][2]
            letr[i][2]=0

        
for i in range(len(letr)-1):
    letr[i][2]=letr[i+1][2]
    letr[i+1][2]=0
    
    letr[i][3]=letr[i+1][3]
    letr[i+1][3]=0
    
    
aeli=[] #liste de trucs a eliminer
for i in range(len(letr)):
    if (letr[i][2]==0) and (letr[i-1][2]==0) and (letr[i][3]==0) and (letr[i][4]!=0):
        letr[i-1][4]=letr[i][4]
        letr[i][4]=0

for i in range(len(letr)):
    if letr[i][2]==0:
        aeli.append(i)

nletr = np.delete(letr,aeli,axis=0) #tu ne peux l'appliquer qu'une fois, ça marche pas dans une boucle

for i in range(len(nletr)):
    nletr[i][4]=nletr[i][4].replace('h',':')
            
temp = []
mot= ""
for i in range(len(nletr)):
    if "2021" not in nletr[i][1]:
        nletr[i][1]=nletr[i][1]+"/2021"
        
    temp=re.split("[ |-]+", nletr[i][4]) 
    if len(temp)>3:
        for j in range(len(temp)-2):
            mot+=temp[j+2]+" "
        temp=temp[:2]
        nletr[i][2]=mot
        nletr[i][4]=temp[0]
        nletr[i][5]=temp[1]
        temp=[]
        mot=''        
    elif len(temp)<2:
        nletr[i][4]=temp[0]
        nletr[i][5]="19h00"
    else:
        nletr[i][4],nletr[i][5]=temp
d=""
h=""
for i in range(len(nletr)):
    d=datetime.strptime(nletr[i][1], "%d/%m/%Y")
    nletr[i][1]=d.strftime("%d/%m/%Y")
    h=datetime.strptime(nletr[i][4], "%H:%M")
    nletr[i][4]=h.strftime("%I:%M %p")
    h=datetime.strptime(nletr[i][5], "%H:%M")
    nletr[i][5]=h.strftime("%I:%M %p")
    h=""
    nletr[i][0]="FALSE"
    
titre=['Subject','Start Date','Start Time','End Date','End Time','All Day Event','Description','Location']
nletr=nletr.transpose()
nletr=np.vstack([nletr,np.empty((1,len(nletr[0])),dtype=object)])
nletr=np.vstack([nletr,np.empty((1,len(nletr[0])),dtype=object)])

nletr[[0,2,4]]=nletr[[2,4,0]]
nletr[[3,4,5,6]]=nletr[[6,5,4,3]]

nletr=nletr.transpose()

with open('export.csv', 'w', encoding='UTF8', newline='') as f:
    writer=csv.writer(f)
    writer.writerow(titre)
    for elm in nletr:
        writer.writerow(elm)
