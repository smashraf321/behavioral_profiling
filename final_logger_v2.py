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

def can_rx_task():
    while True:
        message = bus.recv()
        if message.arbitration_id == hf.PID_REPLY:
            q_CAN.put(message)

def gps_rx_task():
    # read GPS data
    while True:
        for new_data in gpsd_socket:
            if new_data:
                q_GPS.put(new_data)
                break
            else:
                continue

q_CAN = queue.Queue()
q_GPS = queue.Queue()
rx_can = Thread(target = can_rx_task)
rx_can.start()
rx_gps = Thread(target = gps_rx_task)
rx_gps.start()

timeStamp = ''
time_stamp = ''
total_time = 0.0
total_time_day = 0.0
total_time2 = 0.0
total_time1 = 0.0
time_interval = 0.0
rpm = 0
speed = 0
throttle = 0
distance = 0
distance_total = 0
time2 = 0
time1 = 0
vspeed2 = 0
vspeed1 = 0
curr_lat = 0
prev_lat = 0
curr_lon = 0
prev_lon = 0
curr_lat_temp = 0
curr_lon_temp = 0
first_time12 = True
logged_data_can = ''
logged_data_gps = ''

count = 0
msg_count = 0
#for timeout purposes
time_start = 0.0
time_curr = 0.0
time_elapsed = 0.0
#to see if we waited for at least a while before starting again
time_spent_at_stop = 0.0
time_start_at_stop = 0.0
#file_count = 0
outfile_can = 0
outfile_name = 0
file_name_can = ''
file_open = False

LOG_GPS = False
DEPOT_BEGIN = True
STARTED_FROM_DEPOT = False
STARTED_FROM_ROUTE = True
RETURN_TO_DEPOT = False
CIRCULATOR = True
FIRST_TIME_START = True
NEW_DATA_START_LOC = False
NEW_DATA_STOP_LOC = False

# Main control starts
try:
    if hf.if_bus_on_track() == 0:
        STARTED_FROM_ROUTE = False
    while True:
        GPIO.output(led,True)

        while(msg_count != 3):
            msg_count = 0
            # Send Throttle position request
            msg = can.Message(arbitration_id=hf.PID_REQUEST,data=[0x02,0x01,hf.THROTTLE,0x00,0x00,0x00,0x00,0x00],extended_id=False)
            time_start = time.time()
            time_curr = time_start
            time_elapsed = 0.0
            bus.send(msg)
            while(q_CAN.empty() == True and time_elapsed <= 1.0):
                time_curr = time.time()
                time_elapsed = time_curr - time_start
            #check for timeout
            if time_elapsed > 1.0:
                continue
            message = q_CAN.get()
            if message.arbitration_id == hf.PID_REPLY and message.data[2] == hf.THROTTLE:
                throttle = round((message.data[3]*100)/255)
                msg_count += 1
            # Send Engine RPM request
            msg = can.Message(arbitration_id=hf.PID_REQUEST,data=[0x02,0x01,hf.ENGINE_RPM,0x00,0x00,0x00,0x00,0x00],extended_id=False)
            time_start = time.time()
            time_curr = time_start
            time_elapsed = 0.0
            bus.send(msg)
            while(q_CAN.empty() == True and time_elapsed <= 1.0):
                time_curr = time.time()
                time_elapsed = time_curr - time_start
            #check for timeout
            if time_elapsed > 1.0:
                continue
            message = q_CAN.get()
            if message.arbitration_id == hf.PID_REPLY and message.data[2] == hf.ENGINE_RPM:
                rpm = round(((message.data[3]*256) + message.data[4])/4)
                msg_count += 1
            # Send Vehicle speed  request
            msg = can.Message(arbitration_id=hf.PID_REQUEST,data=[0x02,0x01,hf.VEHICLE_SPEED,0x00,0x00,0x00,0x00,0x00],extended_id=False)
            time_start = time.time()
            time_curr = time_start
            time_elapsed = 0.0
            bus.send(msg)
            while(q_CAN.empty() == True and time_elapsed <= 1.0):
                time_curr = time.time()
                time_elapsed = time_curr - time_start
            #check for timeout
            if time_elapsed > 1.0:
                continue
            message = q_CAN.get()
            if message.arbitration_id == hf.PID_REPLY and message.data[2] == hf.VEHICLE_SPEED:
                time_stamp = datetime.now()
                timeStamp = time_stamp.strftime('%H:%M:%S.%f')
                vspeed2 = message.data[3]
                time2 = message.timestamp
                total_time2 = float(time_stamp.strftime('%H')) * 3600 + float(time_stamp.strftime('%M')) * 60 + float(time_stamp.strftime('%S.%f'))
                msg_count += 1

        # read GPS data if available
        msg_count = 0
        LOG_GPS = False
        logged_data_gps = '0,0'
        if q_GPS.empty() == False:
            time_stamp = datetime.now()
            timeStamp = time_stamp.strftime('%H:%M:%S.%f')
            total_time2 = float(time_stamp.strftime('%H')) * 3600 + float(time_stamp.strftime('%M')) * 60 + float(time_stamp.strftime('%S.%f'))
            new_data = q_GPS.get()
            data_stream.unpack(new_data)
            curr_lat = data_stream.TPV['lat']
            if curr_lat == 'n/a':
                curr_lat = 0;
            curr_lon = data_stream.TPV['lon']
            if curr_lon == 'n/a':
                curr_lon = 0;
            if prev_lat != curr_lat or prev_lon != curr_lon:
                logged_data_gps = str(curr_lat) + ',' + str(curr_lon)
                prev_lat = curr_lat
                prev_lon = curr_lon

        logged_data_can = str(count) + ',' + timeStamp + ','
        logged_data_can += '{0:f},'.format(rpm) + '{0:f},'.format(vspeed2) + '{0:f},'.format(throttle)
        logged_data_can += logged_data_gps

        # calculate distance
        if first_time12:
            time1 = time2
            vspeed1 = vspeed2
            total_time1 = total_time2
            first_time12 = False
        # convert speed from km/h to m/s
        vspeed1 = vspeed1 * 5 / 18
        vspeed2 = vspeed2 * 5 / 18
        distance += (vspeed2 + vspeed1)*(time2 - time1)/2
        distance_total += (vspeed2 + vspeed1)*(time2 - time1)/2
        vspeed1 = vspeed2
        time1 = time2
        time_interval = total_time2 - total_time1
        total_time += time_interval
        total_time_day += time_interval
        total_time1 = total_time2

        logged_data_can += ',{0:f},{1:f},{2:f},{3:f},{4:f}'.format(total_time_day,total_time,time_interval,distance_total,distance)
        if file_open:
            print(logged_data_can,file = outfile_can)

        # geofence logic begins
        if hf.if_in_depot(float(curr_lat),float(curr_lon),distance_total,RETURN_TO_DEPOT,vspeed2):
            if DEPOT_BEGIN:
                #os.system("./final_upload.sh")
                print('D')
                if not file_open:
                    file_name_can = 'Documents/logs/log_DOJ_' + datetime.now().strftime('%Y_%m_%d_%H_%M_%S') + '.csv'
                    # save file name
                    outfile_name = open('current_file.txt','w+')
                    print(file_name_can,file = outfile_name)
                    outfile_name.close()
                    # write to a new file
                    outfile_can = open(file_name_can,'w+')
                    print('Logging to first file')
                    file_open = True
                STARTED_FROM_DEPOT = True
            if RETURN_TO_DEPOT:
                if file_open:
                    outfile_can.close()
                file_open = False
                #os.system("./final_upload.sh")
                print('B2D')
                # remove last logged file as not on route
                if file_open:
                    outfile_name = open('current_file.txt','r')
                    filename = outfile_name.readline()
                    outfile_name.close()
                    to_be_renamed = "mv " + filename.rstrip() + " " + filename.rstrip() + ".b2d.csv"
                    os.system(to_be_renamed)
                os.system("rm -f current_file.txt")
                STARTED_FROM_DEPOT = True
        else:
            print('R')
            RETURN_TO_DEPOT = True
            DEPOT_BEGIN = False
            if hf.geo_fence_start(float(curr_lat),float(curr_lon),distance,vspeed2,FIRST_TIME_START,CIRCULATOR):
                if not NEW_DATA_START_LOC:
                    if file_open:
                        outfile_can.close()
                        print('Closed previous file')
                    # recaliberate count n distance
                    count = 0
                    distance = 0
                    total_time = 0
                    file_name_can = 'Documents/logs/log_LAPS_CAN_' + datetime.now().strftime('%Y_%m_%d_%H_%M_%S') + '.csv'
                    # save file name
                    outfile_name = open('current_file.txt','w+')
                    print(file_name_can,file = outfile_name)
                    outfile_name.close()
                    # write to a new file
                    outfile_can = open(file_name_can,'w+')
                    print('Logging to file')
                    # set flags
                    file_open = True
                    NEW_DATA_START_LOC = True
                    FIRST_TIME_START = False
                    #file_count += 1
            else:
                NEW_DATA_START_LOC = False
            if not CIRCULATOR:
                if hf.geo_fence_stop(float(curr_lat),float(curr_lon),distance,vspeed2):
                    if not NEW_DATA_STOP_LOC:
                        if file_open:
                            outfile_can.close()
                            print('Closed previous file')
                        # recaliberate count n distance
                        count = 0
                        distance = 0
                        total_time = 0
                        file_name_can = 'Documents/logs/log_LAPS_CAN_' + datetime.now().strftime('%Y_%m_%d_%H_%M_%S') + '.csv'
                        # save file name
                        outfile_name = open('current_file.txt','w+')
                        print(file_name_can,file = outfile_name)
                        outfile_name.close()
                        # write to a new file
                        outfile_can = open(file_name_can,'w+')
                        print('Logging to file')
                        # set flags
                        file_open = True
                        NEW_DATA_STOP_LOC = True
                        #file_count += 1
                else:
                    NEW_DATA_STOP_LOC = False
            if STARTED_FROM_ROUTE:
                # open the previous file
                outfile_name = open('current_file.txt','r')
                filename = outfile_name.readline()
                outfile_name.close()
                # get previous_distance
                distance = hf.previous_distance(filename.rstrip())
                outfile = open(filename.rstrip(),'a')
                file_open = True
                STARTED_FROM_ROUTE = False

        count += 1
        #print(logged_data_can)

except KeyboardInterrupt:
    #Catch keyboard interrupt
    GPIO.output(led,False)
    if file_open:
        outfile_can.close()
        # close CAN interface
    os.system("sudo /sbin/ip link set can0 down")
    print('\n\rKeyboard interrtupt')
