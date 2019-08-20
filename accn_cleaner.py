import csv

LAP_NUM = 6

file_n = []
file_n.append('log_LAPS_2019_07_14_15_35_54.csv')
file_n.append('log_LAPS_2019_07_14_15_53_38.csv')
file_n.append('log_LAPS_2019_07_14_16_10_42.csv')
file_n.append('log_LAPS_2019_07_14_16_27_53.csv')
file_n.append('log_LAPS_2019_07_14_16_45_15.csv')
file_n.append('log_LAPS_2019_07_14_17_21_23.csv')
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
field_names.append('lat')
field_names.append('lon')
field_names.append('tot_dist')
field_names.append('dist_intrvl')
field_names.append('dist_lap')

INIT_SCAN = True
FIRST_TIME = True
accn = 0.0
jerk = 0.0
prev_accn = 0.0
time = 0.0
distance_half_sec = 0.0
prev_dist = 0.0
curr_dist = 0.0

with open(file_name,'r') as csv_file:
    csv_reader = csv.DictReader(csv_file, fieldnames = field_names, delimiter = ',')
    with open(w_file_name, mode='w') as lap_file:
        csv_writer = csv.writer(lap_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for rows in csv_reader:
            if INIT_SCAN and float(rows['accn']) != 0.0:
                INIT_SCAN = False
            if INIT_SCAN:
                if float(rows['tim_lap']) >= time + 0.5:
                    accn = float(rows['accn'])
                    time = float(rows['tim_lap'])
                    curr_dist = float(rows['dist_lap'])
                    distance_half_sec = curr_dist - prev_dist
                    if prev_accn * accn <= 0:
                        jerk = 0.0
                    else:
                        jerk = accn - prev_accn
                    csv_writer.writerow([rows['idx'],rows['t_stmp'],rows['tot_time'],rows['tim_lap'],rows['tim_intvl'],rows['thrtl'],rows['rpm'],rows['spd'],accn,jerk,rows['lat'],rows['lon'],rows['tot_dist'],rows['dist_intrvl'],distance_half_sec,rows['dist_lap']])
                    prev_dist = curr_dist
                    prev_accn = accn
                else:
                    # continue
                    accn = 'n/a'
                    distance_half_sec = 'n/a'
                    jerk = 'n/a'
                    csv_writer.writerow([rows['idx'],rows['t_stmp'],rows['tot_time'],rows['tim_lap'],rows['tim_intvl'],rows['thrtl'],rows['rpm'],rows['spd'],accn,jerk,rows['lat'],rows['lon'],rows['tot_dist'],rows['dist_intrvl'],distance_half_sec,rows['dist_lap']])
            else:
                if float(rows['tim_lap']) >= time + 0.5 or FIRST_TIME:
                    FIRST_TIME = False
                    accn = float(rows['accn'])
                    time = float(rows['tim_lap'])
                    curr_dist = float(rows['dist_lap'])
                    distance_half_sec = curr_dist - prev_dist
                    if prev_accn * accn <= 0:
                        jerk = 0.0
                    else:
                        jerk = accn - prev_accn
                    csv_writer.writerow([rows['idx'],rows['t_stmp'],rows['tot_time'],rows['tim_lap'],rows['tim_intvl'],rows['thrtl'],rows['rpm'],rows['spd'],accn,jerk,rows['lat'],rows['lon'],rows['tot_dist'],rows['dist_intrvl'],distance_half_sec,rows['dist_lap']])
                    prev_dist = curr_dist
                    prev_accn = accn
                else:
                    # continue
                    accn = 'n/a'
                    distance_half_sec = 'n/a'
                    jerk = 'n/a'
                    csv_writer.writerow([rows['idx'],rows['t_stmp'],rows['tot_time'],rows['tim_lap'],rows['tim_intvl'],rows['thrtl'],rows['rpm'],rows['spd'],accn,jerk,rows['lat'],rows['lon'],rows['tot_dist'],rows['dist_intrvl'],distance_half_sec,rows['dist_lap']])
