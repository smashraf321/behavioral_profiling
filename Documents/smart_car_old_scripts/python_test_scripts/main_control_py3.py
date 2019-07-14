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
            q.put(message)

def can_tx_task():
    while True:
        GPIO.output(led,True)
        # Send Engine coolant temperature request
        msg = can.Message(arbitration_id=hf.PID_REQUEST,data=[0x02,0x01,hf.ENGINE_COOLANT_TEMP,0x00,0x00,0x00,0x00,0x00],extended_id=False)
        bus.send(msg)
        time.sleep(0.05)
        # Send Engine RPM request
        msg = can.Message(arbitration_id=hf.PID_REQUEST,data=[0x02,0x01,hf.ENGINE_RPM,0x00,0x00,0x00,0x00,0x00],extended_id=False)
        bus.send(msg)
        time.sleep(0.05)
        # Send Vehicle speed  request
        msg = can.Message(arbitration_id=hf.PID_REQUEST,data=[0x02,0x01,hf.VEHICLE_SPEED,0x00,0x00,0x00,0x00,0x00],extended_id=False)
        bus.send(msg)
        time.sleep(0.05)
        # Send Throttle position request
        msg = can.Message(arbitration_id=hf.PID_REQUEST,data=[0x02,0x01,hf.THROTTLE,0x00,0x00,0x00,0x00,0x00],extended_id=False)
        bus.send(msg)
        time.sleep(0.05)
        # End transmission
        GPIO.output(led,False)
        time.sleep(0.1)

q = queue.Queue()
rx = Thread(target = can_rx_task)
rx.start()
tx = Thread(target = can_tx_task)
tx.start()

temperature = 0
rpm = 0
speed = 0
throttle = 0
distance = 0
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
#file_count = 0
outfile = 0
outfile_name = 0
file_open = False
file_name = ''

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
        for i in range(4):
            while(q.empty() == True):
                pass
            message = q.get()

            time2 = message.timestamp
            logged_data = '{0:f},'.format(time2)

            if message.arbitration_id == hf.PID_REPLY and message.data[2] == hf.ENGINE_COOLANT_TEMP:
                temperature = message.data[3] - 40
            if message.arbitration_id == hf.PID_REPLY and message.data[2] == hf.ENGINE_RPM:
                rpm = round(((message.data[3]*256) + message.data[4])/4)
            if message.arbitration_id == hf.PID_REPLY and message.data[2] == hf.VEHICLE_SPEED:
                speed = message.data[3]
                vspeed2 = speed
            if message.arbitration_id == hf.PID_REPLY and message.data[2] == hf.THROTTLE:
                throttle = round((message.data[3]*100)/255)

        logged_data += '{0:d},{1:d},{2:d},{3:d},'.format(temperature,rpm,speed,throttle)

        # calculate distance
        if first_time12:
            time1 = time2
            vspeed1 = vspeed2
            first_time12 = False
        # convert speed from km/h to m/s
        vspeed1 = vspeed1 * 5 / 18
        vspeed2 = vspeed2 * 5 / 18
        distance += (vspeed2 + vspeed1)*(time2 - time1)/2
        vspeed1 = vspeed2
        time1 = time2

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

        if hf.if_in_depot(float(curr_lat),float(curr_lon)) or sp_count < 5:
            if DEPOT_BEGIN:
                os.system("./final_upload.sh")
                print('In depot (hopefully), gonna exit soon')
                time.sleep(0.1)
                STARTED_FROM_DEPOT = True
            if RETURN_TO_DEPOT:
                if file_open:
                    outfile.close()
                file_open = False
                os.system("./final_upload.sh")
                print('Returned to depot')
                # remove last logged file as not on route
                if file_open:
                    outfile_name = open('current_file.txt','r')
                    filename = outfile_name.readline()
                    outfile_name.close()
                    to_be_removed = "rm -f " + filename.rstrip()
                    os.system(to_be_removed)
                os.system("rm -f current_file.txt")
                time.sleep(0.1)
                STARTED_FROM_DEPOT = True
        else:
            print('On Road...')
            RETURN_TO_DEPOT = True
            DEPOT_BEGIN = False
            print(hf.geo_fence_start(float(curr_lat),float(curr_lon),distance,speed,FIRST_TIME_START,CIRCULATOR))
            if hf.geo_fence_start(float(curr_lat),float(curr_lon),distance,speed,FIRST_TIME_START,CIRCULATOR):
                if not NEW_DATA_START_LOC:
                    if file_open:
                        outfile.close()
                        print('Closed previous file')
                    # recaliberate count n distance
                    count = 0;
                    distance = 0
                    file_name = 'Documents/logs/log_' + str(datetime.now()) + '.csv'
                    # save file name
                    outfile_name = open('current_file.txt','w+')
                    print(file_name,file = outfile_name)
                    outfile_name.close()
                    # write to a new file
                    outfile = open(file_name,'w+')
                    print('Logging to file')
                    # set flags
                    file_open = True
                    NEW_DATA_START_LOC = True
                    FIRST_TIME_START = False
                    #file_count += 1
            else:
                NEW_DATA_START_LOC = False
            if not CIRCULATOR:
                if hf.geo_fence_stop(float(curr_lat),float(curr_lon),distance,speed):
                    if not NEW_DATA_STOP_LOC:
                        if file_open:
                            outfile.close()
                            print('Closed previous file')
                        # recaliberate count n distance
                        count = 0;
                        distance = 0
                        file_name = 'Documents/logs/log_' + str(datetime.now()) + '.csv'
                        # save file name
                        outfile_name = open('current_file.txt','w+')
                        print(file_name,file = outfile_name)
                        outfile_name.close()
                        # write to a new file
                        outfile = open(file_name,'w+')
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

        logged_data += '{0:d},{1:f}'.format(count,distance)
        if file_open:
            print(logged_data,file = outfile)

        count += 1
        if sp_count < 5:
            sp_count += 1
        print(logged_data)

except KeyboardInterrupt:
    #Catch keyboard interrupt
    GPIO.output(led,False)
    if file_open:
        outfile.close()
        # close CAN interface
    os.system("sudo /sbin/ip link set can0 down")
    print('\n\rKeyboard interrtupt')
