import csv
import queue

LAP_NUM = 6

file_n = []
file_n.append('lap_1_1.csv')
file_n.append('lap_2_1.csv')
file_n.append('lap_3_1.csv')
file_n.append('lap_4_1.csv')
file_n.append('lap_5_1.csv')
file_n.append('lap_6_1.csv')
file_name = 'Documents/logs/' + file_n[LAP_NUM - 1]

w_file_n = []
w_file_n.append('lap_1.csv')
w_file_n.append('lap_2.csv')
w_file_n.append('lap_3.csv')
w_file_n.append('lap_4.csv')
w_file_n.append('lap_5.csv')
w_file_n.append('lap_6.csv')
w_file_name = 'Documents/logs/' + w_file_n[LAP_NUM - 1]

field_names = []
field_names.append('idx')
field_names.append('t_stmp')
field_names.append('tot_time')
field_names.append('tim_lap')
field_names.append('tim_intvl')
field_names.append('thrtl')
field_names.append('rpm')
field_names.append('spd')
field_names.append('accn')
field_names.append('jerk')
field_names.append('lat')
field_names.append('lon')
field_names.append('tot_dist')
field_names.append('dist_intrvl')
field_names.append('grad_dist')
field_names.append('dist_lap')

gps_q = queue.Queue()
curr_time = 0.0
gps_lat = 0.0
gps_lon = 0.0
TIME_LAG = 2
gps_values = 0
WRITTEN = True

with open(file_name,'r') as csv_file:
    csv_reader = csv.DictReader(csv_file, fieldnames = field_names, delimiter = ',')
    with open(w_file_name, mode='w') as lap_file:
        csv_writer = csv.writer(lap_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for rows in csv_reader:
            if float(rows['lat']) and float(rows['lon']):
                curr_time = float(rows['tim_lap'])
                gps_lat = float(rows['lat'])
                gps_lon = float(rows['lon'])
                gps_q.put((gps_lat,gps_lon,curr_time))
            if not gps_q.empty() and WRITTEN:
                gps_values = gps_q.get()
            if gps_values:
                if float(rows['tim_lap']) >= TIME_LAG + gps_values[2]:
                    csv_writer.writerow([rows['idx'],rows['t_stmp'],rows['tot_time'],rows['tim_lap'],rows['tim_intvl'],rows['thrtl'],rows['rpm'],rows['spd'],rows['accn'],rows['jerk'],gps_values[0],gps_values[1],rows['tot_dist'],rows['dist_intrvl'],rows['grad_dist'],rows['dist_lap']])
                    WRITTEN = True
                    gps_values = 0
                else:
                    csv_writer.writerow([rows['idx'],rows['t_stmp'],rows['tot_time'],rows['tim_lap'],rows['tim_intvl'],rows['thrtl'],rows['rpm'],rows['spd'],rows['accn'],rows['jerk'],0,0,rows['tot_dist'],rows['dist_intrvl'],rows['grad_dist'],rows['dist_lap']])
                    WRITTEN = False
            else:
                csv_writer.writerow([rows['idx'],rows['t_stmp'],rows['tot_time'],rows['tim_lap'],rows['tim_intvl'],rows['thrtl'],rows['rpm'],rows['spd'],rows['accn'],rows['jerk'],0,0,rows['tot_dist'],rows['dist_intrvl'],rows['grad_dist'],rows['dist_lap']])
