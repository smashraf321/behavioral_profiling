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
curr_lon = 0
logged_data = ''

count = 0
#file_count = 0
outfile = 0
outfile_name = 0
file_open = False
file_name = ''

DEPOT_BEGIN = True
STARTED_FROM_DEPOT = False
RETURN_TO_DEPOT = False
NEW_DATA_START_LOC = False
NEW_DATA_STOP_LOC = False

# Main control starts
try:
    while True:
        for i in range(4):
            while(q.empty() == True):
                pass
            message = g.get()

            time2 = message.timestamp
            logged_data = '{0:d},{1:f},'.format(count,time2)

            if message.arbitration_id == hf.PID_REPLY and message.data[2] == hf.ENGINE_COOLANT_TEMP:
                temperature = message.data[3] - 40
            if message.arbitration_id == hf.PID_REPLY and message.data[2] == hf.ENGINE_RPM:
                rpm = round(((message.data[3]*256) + message.data[4])/4)
            if message.arbitration_id == hf.PID_REPLY and message.data[2] == hf.VEHICLE_SPEED:
                speed = message.data[3]
                vspeed2 = speed
            if message.arbitration_id == hf.PID_REPLY and message.data[2] == hf.THROTTLE:
                throttle = round((message.data[3]*100)/255)

        logged_data +=  '{0:d},{1:d},{2:d},{3:d},'.format(temperature,rpm,speed,throttle)

        #calculate distance
        distance += (vspeed2 + vspeed1)*(time2 - time1)/2
        vspeed1 = vspeed2
        time1 = time2

        logged_data += '{0:f},'.format(distance)

        # read GPS data
        for new_data in gpsd_socket:
            if new_data:
                data_stream.unpack(new_data)
                curr_lat = data_stream.TPV['lat']
                curr_lon = data_stream.TPV['lon']
                logged_data += str(curr_lat) + ',' + str(curr_lon) + ',' + str(data_stream.TPV['time'])
                break;
            else:
                continue

        if hf.geo_fence_depot(curr_lat,curr_lon):
            if DEPOT_BEGIN:
                os.system("sudo final_upload.sh")
                time.sleep(0.1)
                STARTED_FROM_DEPOT = True
            if RETURN_TO_DEPOT:
                if file_open:
                    outfile.close()
                file_open = False
                os.system("sudo final_upload.sh")
                time.sleep(0.1)
        else:
            RETURN_TO_DEPOT = True
            DEPOT_BEGIN = False
            if not STARTED_FROM_DEPOT:
                outfile_name = open('current_file.txt','r')
                filename = outfile_name.readline()
                outfile_name.close()
                outfile = open(filename,'w')
                file_open = True
            if hf.geo_fence_start(curr_lat,curr_lon,distance,speed):
                if not NEW_DATA_START_LOC:
                    if file_open:
                        outfile.close()
                    count = 0;
                    file_name = 'log_' + str(datetime.now()) + '.csv'
                    outfile_name = open('current_file.txt','w')
                    print(file_name,file = outfile_name)
                    outfile_name.close()
                    outfile = open(file_name,'w')
                    file_open = True
                    NEW_DATA_START_LOC = True
                    NEW_DATA_STOP_LOC = False
                    #file_count += 1
            if hf.geo_fence_stop(curr_lat,curr_lon,distance,speed):
                if not NEW_DATA_STOP_LOC:
                    if file_open:
                        outfile.close()
                    count = 0;
                    file_name = 'log' + str(datetime.now()) + '.csv'
                    outfile_name = open('current_file.txt','w')
                    print(file_name,file = outfile_name)
                    outfile_name.close()
                    outfile = open(file_name,'w')
                    file_open = True
                    NEW_DATA_START_LOC = False
                    NEW_DATA_STOP_LOC = True
                    #file_count += 1
        if file_open:
            print(logged_data,file = outfile)

        count += 1
        #print(logged_data)

except KeyboardInterrupt:
	#Catch keyboard interrupt
	GPIO.output(led,False)
    if file_open:
        outfile.close()
    # close CAN interface
	os.system("sudo /sbin/ip link set can0 down")
	print('\n\rKeyboard interrtupt')
