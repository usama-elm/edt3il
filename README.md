# edt3il
Un petit script qui exporte l'EDT de 3IL vers un fichier lisible par Google Calendar et iCalendar

# utilisation

Il y a tout en haut, une variable url, a la place tu mets l'url qui correspond a ton groupe puis tu executes le script qui te donnera un fichier .csv (pour Google calendar).
Voici un [tutoriel de quoi en faire avec ce csv](https://support.google.com/calendar/answer/37118?hl=fr#zippy=%2Ccr%C3%A9er-ou-modifier-un-fichier-csv)

Puis pour iCalendar il faut executer d'abord le premier script edt3il.py qui crée un fichier .csv puis le deuxieme script exportICS qui crée le .ics a importer (ça j'ai pas essayé mais vous devez trouver des tutos en ligne).

Là c'est très brut, le code est un peu mauvais et la manière pas correcte mais le code fait son taf et exporte bien l'EDT ^-^