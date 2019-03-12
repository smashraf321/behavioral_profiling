
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
                    doc_name = 'row_' + str(rows[8])
                    doc_ref = db.collection(u'first_log').document(doc_name)
                    doc_ref.set({
                        u'Time_stamp': rows[0],
                        u'Engine_Temperature': rows[1],
                        u'RPM': rows[2],
                        u'Speed': rows[3],
                        u'Throttle': rows[4],
                        u'GPS_time': rows[7],
                        u'Distance': rows[9]
                    })
                    if rows[5] != 0:
                        doc_ref.update({u'Lat': rows[5], u'Lon': rows[6]})
    except Exception as excptn:
        raise excptn
        print('No CSV files found')
