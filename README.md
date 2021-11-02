# Edt3il
![code asmy](https://img.shields.io/badge/script-usama-orange) ![pypi](https://img.shields.io/pypi/v/csv-ical.svg)  ![python versions](https://img.shields.io/pypi/pyversions/csv-ical.svg)

Un petit script qui exporte l'EDT de 3IL vers un fichier lisible par Google Calendar et iCalendar

# Utilisation
Quand on execute le script edt3il.py il demande le groupe de I2 ou si on est un autre groupe on met le lien de l'EDT. Puis il traite et crée 2 fichiers CSV et ICS pour les calendriers.
Sur Google Calendar on peut utiliser CSV et sur Outlook et iCalendar on peut utiliser ICS.
Voici un [tutoriel de quoi en faire avec ce csv pour Google Calendar](https://support.google.com/calendar/answer/37118?hl=fr#zippy=%2Ccr%C3%A9er-ou-modifier-un-fichier-csv)

Si vous avez des problèmes ou autre n'hesitez pas à ouvrir un ticket.

Il faut Python 3 et il faut installer par [pip](https://pypi.org/project/pip/)
Si pip ou la commande Python ne marche pas sur Windows, [il faut ajouter Python au PATH](https://technochouette.istocks.club/comment-ajouter-python-a-la-variable-windows-path-wiki-utile/2020-10-14/)
Les dependances python:
- numpy
- csv
- re
- datetime
- BeautifulSoup 4
- csv-ical

La commande pour installer les dependances:
`pip install numpy regex datetime beautifulsoup4 csv-ical`
