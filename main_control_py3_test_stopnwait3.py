#!/usr/bin/python3

import helper_functions as hf
import RPi.GPIO as GPIO
import can
import time
import os
import queue
from threading import Thread
from datetime import datetime
from gps3 import gps3

# initial Raspi setup for CAN Shield interfacing
led = 22
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(led,GPIO.OUT)
GPIO.output(led,True)

# configure Gps
gpsd_socket = gps3.GPSDSocket()
data_stream = gps3.DataStream()
gpsd_socket.connect()
gpsd_socket.watch()

# Bring up can0 interface at 500kbps
os.system("sudo /sbin/ip link set can0 up type can bitrate 500000")
time.sleep(0.1)

try:
    bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
except OSError:
    print('Cannot find PiCAN board.')
    GPIO.output(led,False)
    exit()

temperature = 0
rpm = 0
speed = 0
throttle = 0
distance = 0
distance_total = 0
rpi_speed_epoch_time = 0
time2 = 0
time1 = 0
vspeed2 = 0
vspeed1 = 0
curr_lat = 0
prev_lat = 0
curr_lon = 0
prev_lon = 0
first_time12 = True
logged_data = ''

count = 0
sp_count = 0
time_spent_at_stop = 0.0
time_start_at_stop = 0.0
#file_count = 0
outfile = 0
outfile_name = 0
############################################################
file_open = False
############################################################
file_name = ''

DEPOT_BEGIN = True
STARTED_FROM_DEPOT = False # what is the purpose of this flag?
STARTED_FROM_ROUTE = True
RETURN_TO_DEPOT = False
CIRCULATOR = True
FIRST_TIME_START = True
NEW_DATA_START_LOC = False
NEW_DATA_STOP_LOC = False

# Main control starts
try:
    while True:

        # read GPS data
        for new_data in gpsd_socket:
            #print('received GPS')
            if new_data:
                #print('recieved valid GPS data')
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
                GPIO.output(led,True)
                # Send Engine RPM request
                msg = can.Message(arbitration_id=hf.PID_REQUEST,data=[0x02,0x01,hf.ENGINE_RPM,0x00,0x00,0x00,0x00,0x00],extended_id=False)
                bus.send(msg)
                rpm_timeStamptx = datetime.now().strftime('%H:%M:%S.%f')
                #print('sent RPM mesg')
                #time.sleep(0.01)
                # waiting for RPM
                #print('waiting for rpm')
                rpm_not_rx = True
                while rpm_not_rx:
                    print('waiting for rpm')
                    message = bus.recv()
                    print(str(message))
                    if message.arbitration_id == hf.PID_REPLY and message.data[2] == hf.ENGINE_RPM:
                        rpm_timeStamp = datetime.now().strftime('%H:%M:%S.%f')
                        rpm = round(((message.data[3]*256) + message.data[4])/4)
                        rpm_not_rx = False
                        time.sleep(0.01)
                        print('rpm recieved')

                # Send Vehicle speed  request
                msg = can.Message(arbitration_id=hf.PID_REQUEST,data=[0x02,0x01,hf.VEHICLE_SPEED,0x00,0x00,0x00,0x00,0x00],extended_id=False)
                bus.send(msg)
                speed_timeStamptx = datetime.now().strftime('%H:%M:%S.%f')
                #print('sent Speed mesg')
                #time.sleep(0.01)
                # waiting for Speed
                #print('waiting for speed')
                speed_not_rx = True
                while speed_not_rx:
                    print('waiting for speed')
                    message = bus.recv()
                    print(str(message))
                    if message.arbitration_id == hf.PID_REPLY and message.data[2] == hf.VEHICLE_SPEED:
                        rpi_time = time.time()
                        speed_timeStamp = datetime.now().strftime('%H:%M:%S.%f')
                        speed = message.data[3]
                        vspeed2 = speed
                        time2 = message.timestamp
                        speed_not_rx = False
                        time.sleep(0.01)
                        print('speed recieved')

                # Send Throttle position request
                msg = can.Message(arbitration_id=hf.PID_REQUEST,data=[0x02,0x01,hf.THROTTLE,0x00,0x00,0x00,0x00,0x00],extended_id=False)
                bus.send(msg)
                throttle_timeStamptx = datetime.now().strftime('%H:%M:%S.%f')
                #print('sent throttle mesg')
                #time.sleep(0.01)
                # waiting for throttle
                #print('waiting for throttle')
                throttle_not_rx = True
                while throttle_not_rx:
                    print('waiting for throttle')
                    message = bus.recv()
                    print(str(message))
                    if message.arbitration_id == hf.PID_REPLY and message.data[2] == hf.THROTTLE:
                        throttle_timeStamp = datetime.now().strftime('%H:%M:%S.%f')
                        throttle = round((message.data[3]*100)/255)
                        throttle_not_rx = False
                        time.sleep(0.01)
                        print('throttle recieved')

                # End transmission
                GPIO.output(led,False)

                #time.sleep(0.2)

                logged_data = rpm_timeStamptx + ', ' + rpm_timeStamp + ', {0:d}, '.format(rpm) + speed_timeStamptx  + ', ' + speed_timeStamp + ', {0:f}, '.format(time2) + '{0:f}, '.format(rpi_time)  + '{0:d}, '.format(speed) + throttle_timeStamptx + ', ' + throttle_timeStamp + ', {0:d}, '.format(throttle)

                # calculate distance
                if first_time12:
                    time1 = time2
                    vspeed1 = vspeed2
                    first_time12 = False
                # convert speed from km/h to m/s
                vspeed1 = vspeed1 * 5 / 18
                vspeed2 = vspeed2 * 5 / 18
                distance += (vspeed2 + vspeed1)*(time2 - time1)/2
                distance_total += (vspeed2 + vspeed1)*(time2 - time1)/2
                vspeed1 = vspeed2
                time1 = time2
                logged_data += str(curr_lat_temp) + ', ' + str(curr_lon_temp) + ', ' + str(data_stream.TPV['time'] + ', ') + datetime.now().strftime('%H:%M:%S.%f')
                break
            else:
                continue

        logged_data += ', {0:d}, {1:f}, {2:f}'.format(count,distance_total,distance)

        if not file_open:
            file_name = 'Documents/logs/log_DOJ_stopnwait3_' + str(datetime.now()) + '.csv'
            outfile = open(file_name,'w+')
            print('Logging data timestamps...')
            file_open = True
        if file_open:
            print(logged_data,file = outfile)

        count += 1
        #print(logged_data)

except KeyboardInterrupt:
    #Catch keyboard interrupt
    GPIO.output(led,False)
    #if file_open:
        #outfile.close()
        # close CAN interface
    os.system("sudo /sbin/ip link set can0 down")
    print('\n\rKeyboard interrtupt')
