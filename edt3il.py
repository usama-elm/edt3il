######################################################################
##                  NECESSARY DEPENDANCIES                          ##
##                  OR ELSE IT WONT                                 ##
##                  WORK                                            ##
##                  @kaiser-mousu IN GITHUB                         ##
######################################################################
from bs4 import BeautifulSoup
import numpy as np
import re as re
from datetime import datetime
import csv
import math as m
import requests
import exportICS

#Création du lien en fonction du groupe I2
lienBase = "https://eleves.groupe3il.fr/edt_eleves/00_index.php?idGroupe="
groupe=input("C'est quoi ton groupe (1, 2, 3, 4, 5+FA, 6+FA) ou autre?: ")
if groupe.upper()=="AUTRE":
    groupe=input("Met le lien de l'EDT à exporter sous le format \nhttps://eleves.groupe3il.fr/edt_eleves/00_index.php?idGroupe=ERIS1+Groupe+1+FE.xml qui correspond a ton groupe ")
url=lienBase+"I2+Groupe+"+groupe+".xml"

#Récuperation du lien et parsing html
req = requests.get(url)
soup = BeautifulSoup(req.text, "html.parser")
traitementBase = soup.body
#On traite les infos, on prends tous les strings (stripped ou traités) et on les mets dans un array
listeNonParsee = []
for string in traitementBase.stripped_strings:
    if(string=="Horaire"):
        listeNonParsee.append("Eliminer")
    else:
        listeNonParsee.append(string)
        
#On fait un 2eme traitement, et on élimine toutes les données inutiles qui appartienent au navbar ou autre
#On coupe par semaine
#D'abord je cree une matrice booleene qui met true aux positions ou il faut trancher par semaine
matriceBoolene=np.isin(listeNonParsee,"Eliminer")
positions=[]
for i in range(len(matriceBoolene)):
    if matriceBoolene[i]==True:
        positions.append(i)
positions.append(len(matriceBoolene))
#Puis on met sur chaque ligne une semaine, remplie des matieres (avec les differentes données)
semaines=[]
for i in range(len(positions)-1):
    semaines.append(listeNonParsee[positions[i]+7:positions[i+1]-1])

#Cette partie est nottament reserve pour le traitement et mise en case des diffeents elements
# D'abord je crée les differents compteurs position et la matrice pure, composée d'elements vides de taille semaines*5(les jours)*6(matieres qu'on avec un surplus au cas ou)
positionI=-1
positionJ=-1
edtPur=np.zeros((m.floor(len(positions)*5*6),6),dtype=object)
jours=["Lundi","Mardi","Mercredi","Jeudi","Vendredi"] #J'ai remarqué que dans la structure ca commence toujours par le jour donc je l'utilise comme delimiteur de chaque ligne
for semaine in semaines:
    for i in range(len(semaine)):
        if semaine[i] in jours: 
            positionI+=1
            positionJ=-1 #Si c'est un des jours, on avance de ligne et on remet la position a la base
        positionJ+=1
        edtPur[positionI][positionJ]=semaine[i]

#Des fois les horaires sont dans des colonnes differentes car ils ont pas mis un standard pour communiquer les infos (merci pour le coup de me donner plus de taf)
#donc je cherche s'il y a un h contenu dans la case des salles (comme 10h30) et je le met a sa bonne case
for i in range(len(edtPur)):
    if edtPur[i][5]!=0:
        if "h" in edtPur[i][5]:
            edtPur[i][4]=edtPur[i][5]
            edtPur[i][5]=0
    if edtPur[i][3]!=0:     
        if "h" in edtPur[i][3]:
            edtPur[i][4]=edtPur[i][3]
            edtPur[i][3]=0
    if edtPur[i][2]!=0:
        if "h" in edtPur[i][2]:
            edtPur[i][4]=edtPur[i][2]
            edtPur[i][2]=0

#Je ne sais pourquoi, mais il y a un decalage dans les salles et horaires par rapport aux sujets, donc je decale vers le haut de 1
for i in range(len(edtPur)-1):
    edtPur[i][2]=edtPur[i+1][2]
    edtPur[i+1][2]=0
    
    edtPur[i][3]=edtPur[i+1][3]
    edtPur[i+1][3]=0
    
#Il y a bcp de lignes vides,et des informations sur 2 lignes (horaire sur une ligne, matiere et salle dans celle d'apres), donc je cherche a les fusionner avec un tes
# si la matiere de cette ligne et celle d'avant est vide mais qu'il y a un horaire est une salle dans celle d'avant je fusionne
# en regle generale c'est les EPP ou autres conferences
positionsEliminer=[] #liste de trucs a eliminer
for i in range(len(edtPur)):
    if (edtPur[i][2]==0) and (edtPur[i-1][2]==0) and (edtPur[i][3]==0) and (edtPur[i][4]!=0):
        edtPur[i-1][4]=edtPur[i][4]
        edtPur[i][4]=0
#On prends les lignes vides (sans matiere) et on les elimine
for i in range(len(edtPur)):
    if edtPur[i][2]==0:
        positionsEliminer.append(i)
edtTraite = np.delete(edtPur,positionsEliminer,axis=0) #tu ne peux l'appliquer qu'une fois, ça marche pas dans une boucle

#CSV et ICS sont des standards americains, donc ils utilisent : a la place de h, donc on remplace
for i in range(len(edtTraite)):
    edtTraite[i][4]=edtTraite[i][4].replace('h',':')

#Des fois les heures sont EPP donc il y a plus d'info que l'heure donc il faut decouper l'heure de la matiere
temp = []
mot= ""
for i in range(len(edtTraite)):
    if "2022" not in edtTraite[i][1] in edtTraite[i][1]:
        edtTraite[i][1]=edtTraite[i][1]+"/2022"
    temp=re.split("[ |-]+", edtTraite[i][4]) #On split utilisant REGEX
    if len(temp)>2: 
        for j in range(len(temp)-2):
            mot+=temp[j+2]+" "
        temp=temp[:2]
        edtTraite[i][2]=mot
        edtTraite[i][4]=temp[0]
        edtTraite[i][5]=temp[1] #Si le mot est plus grand que 2, il y a que les indices 0 et 1 qui contiennent l'heure, le reste c'est des mots donc matiere
        temp=[]
        mot=''                  #On les remet a 0 
    elif len(temp)<2:
        edtTraite[i][4]=temp[0]
        edtTraite[i][5]=None    #S'il y a pas d'horaire de fin google ajoute automatiquement 1h donc EPP ou autre
    else:
        edtTraite[i][4],edtTraite[i][5]=temp
#Traitement des heures et dates pour standardiser vers ICS et CSV
d=""
h=""
for i in range(len(edtTraite)):
    d=datetime.strptime(edtTraite[i][1], "%d/%m/%Y")
    edtTraite[i][1]=d.strftime("%d/%m/%Y")
    try:
        h=datetime.strptime(edtTraite[i][4], "%H:%M")
        edtTraite[i][4]=h.strftime("%I:%M %p")
    except:
        edtTraite[i][4]=None
    try:
        h=datetime.strptime(edtTraite[i][5], "%H:%M")
        edtTraite[i][5]=h.strftime("%I:%M %p")
    except:
        edtTraite[i][5]=None
    h=""
    edtTraite[i][0]="FALSE"         #Il faut une colonne FALSE pour ALL-DAY-EVENT donc on transforme
    edtTraite[i][2]=edtTraite[i][2]+" en "+str(edtTraite[i][3]) #On ajoute la salle a la matiere pour plus de visibilité
    
    
    
titre=['Subject','Start Date','Start Time','End Date','End Time','All Day Event','Description','Location'] #Premiere colonne du CSV
#La on transpose, on bouge les lignes dans le bon ordre, on ajoute certaines colonnes vides et on reconvertis en colonnes
edtTraite=edtTraite.transpose()
edtTraite=np.vstack([edtTraite,np.empty((1,len(edtTraite[0])),dtype=object)])
edtTraite=np.vstack([edtTraite,np.empty((1,len(edtTraite[0])),dtype=object)])
edtTraite[[0,2,4]]=edtTraite[[2,4,0]]
edtTraite[[3,4,5,6]]=edtTraite[[6,5,4,3]]
edtTraite=edtTraite.transpose()

#Ecriture du CSV
with open('export.csv', 'w', encoding='UTF8', newline='') as f:
    writer=csv.writer(f)
    writer.writerow(titre)
    for element in edtTraite:
        writer.writerow(element)

exportICS.importerICS() #Execute le script CSV>ICS