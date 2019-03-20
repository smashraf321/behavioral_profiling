#!/usr/bin/python

import time
from datetime import datetime
from gps3 import gps3

# configure Gps
gpsd_socket = gps3.GPSDSocket()
data_stream = gps3.DataStream()
gpsd_socket.connect()
gpsd_socket.watch()

time.sleep(0.1)

curr_lat = 0
prev_lat = 0
curr_lon = 0
prev_lon = 0
logged_data = ''

try:
    while True:
        # read GPS data
        for new_data in gpsd_socket:
            if new_data:
                data_stream.unpack(new_data)
                curr_lat = data_stream.TPV['lat']
                if curr_lat == 'n/a':
                    curr_lat = 0;
                curr_lon = data_stream.TPV['lon']
                if curr_lon == 'n/a':
                    curr_lon = 0;
                curr_lat_temp = curr_lat
                curr_lon_temp = curr_lon
                if prev_lat == curr_lat and prev_lon == curr_lon:
                    curr_lat_temp = 0
                    curr_lon_temp = 0
                else:
                    prev_lat = curr_lat
                    prev_lon = curr_lon
                logged_data += str(curr_lat_temp) + ',' + str(curr_lon_temp) + ',' + str(data_stream.TPV['time'] + ',')
                break
            else:
                continue
        print(logged_data)

except KeyboardInterrupt:
    #Catch keyboard interrupt
    print('\n\rKeyboard interrtupt')
