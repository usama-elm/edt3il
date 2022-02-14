from datetime import datetime, timedelta
from csv_ical import Convert

def importerICS(name=''):
    convert = Convert()
    csv_file_location = 'exports/'+name+'Export.csv'
    ical_file_location = 'exports/'+name+'Export.ics'
    csv_configs = {
        'HEADER_ROWS_TO_SKIP': 1,
        'CSV_NAME': 0,
        'CSV_START_DATE': 2,
        'CSV_END_DATE': 3,
        'CSV_DESCRIPTION': 5,
        'CSV_LOCATION': 6,
        }

    convert.read_csv(csv_file_location, csv_configs)
    i = 0
    while i < len(convert.csv_data):
        row = convert.csv_data[i]
        start_date = row[1] + '-'+row[csv_configs['CSV_START_DATE']]
        try:
            row[csv_configs['CSV_START_DATE']] = datetime.strptime(start_date, '%d/%m/%Y-%I:%M %p')
            row[csv_configs['CSV_END_DATE']] = row[csv_configs['CSV_START_DATE']]+timedelta(minutes=90)
            i += 1
        except ValueError:
            convert.csv_data.pop(i)
            print("error",i)

    convert.make_ical(csv_configs)
    convert.save_ical(ical_file_location)