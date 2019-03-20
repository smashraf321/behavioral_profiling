
import os
import csv
from google.cloud import firestore

files_path = '/home/pi/behavioral_profiling/Documents/logs/'

db = firestore.Client()

for curr_file in os.listdir(files_path):
    try:
        if curr_file.endswith('.csv'):
            print('csv file found')
            with open(files_path + curr_file,'r') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter = ',')
                for rows in csv_reader:
                    if len(rows[8]) == 1:
                        doc_name = '00000' + str(rows[8])
                    elif len(rows[8]) == 2:
                        doc_name = '0000' + str(rows[8])
                    elif len(rows[8]) == 3:
                        doc_name = '000' + str(rows[8])
                    elif len(rows[8]) == 4:
                        doc_name = '00' + str(rows[8])
                    elif len(rows[8]) == 5:
                        doc_name = '0' + str(rows[8])
                    else:
                        doc_name = str(rows[8])
                    doc_ref = db.collection(u'first_log_second_attempt').document(doc_name)
                    doc_ref.set({
                        u'Time_stamp': float(rows[0]),
                        u'Engine_Temperature': float(rows[1]),
                        u'RPM': float(rows[2]),
                        u'Speed': float(rows[3]),
                        u'Throttle': float(rows[4]),
                        u'GPS_time': rows[7],
                        u'Distance': float(rows[9])
                    })
                    if rows[5] != '0':
                        doc_ref.update({u'Lat': rows[5], u'Lon': rows[6]})
    except Exception as excptn:
        raise excptn
        print('No CSV files found')
