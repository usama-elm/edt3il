# Edt3il
![code asmy](https://img.shields.io/badge/script-usama-orange) ![pypi](https://img.shields.io/pypi/v/csv-ical.svg)  ![python versions](https://img.shields.io/pypi/pyversions/csv-ical.svg)
A little bit of explanation in here. My school, has a [website](https://eleves.groupe3il.fr/edt_eleves/00_index.php) that shows our school calendar. The problem is that for some reason they dont have an export function. Back in 2020 I just developped a quick but tedious script to extract the webpage and then transform it into csv/ical format so it can be imported into normal calendars.


# Use of the script
When the script ``python3 edt3il.py`` is executed it asks for what level (I1, I2, I3) and the group. It takes the website and outputs a csv.

Here is a tutorial to import a csv manually into [Google Calendar](https://support.google.com/calendar/answer/37118?hl=fr#zippy=%2Ccr%C3%A9er-ou-modifier-un-fichier-csv)

If any issues, open a ticket.

Python 3 and [pip](https://pypi.org/project/pip/) needed.
The dependencies ``numpy csv re datetime beautifulsoup4 csv-ical``

The command to install dependencies : 
`pip install numpy regex datetime beautifulsoup4 csv-ical`

To keep it continually running you can run a CRON job in Linux/MacOS by using ``crontab``
