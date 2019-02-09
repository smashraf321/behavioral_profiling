#!/usr/bin/python3

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

# PIDs selector variables
ENGINE_COOLANT_TEMP = 0x05
ENGINE_RPM = 0x0C
VEHICLE_SPEED = 0x0D
MAF_SENSOR = 0x10
O2_VOLTAGE = 0x14
THROTTLE = 0x11

PID_REQUEST = 0x7DF
PID_REPLY = 0x7E8

# set GEOFencing bounds
DEPOT_LAT_NORTH = 42.02994532
DEPOT_LAT_SOUTH = 42.02994530
DEPOT_LONG_EAST = -93.65335383
DEPOT_LONG_WEST = -93.65335385

START_LAT_NORTH = 42.02994552
START_LAT_SOUTH = 42.02994550
START_LONG_EAST = -93.65335373
START_LONG_WEST = -93.65335375

STOP_LAT_NORTH = 42.02994562
STOP_LAT_SOUTH = 42.02994560
STOP_LONG_EAST = -93.65335393
STOP_LONG_WEST = -93.65335395

DIST_START_MIN = 3.3
DIST_START_MAX = 3.4
DIST_STOP_MIN = 15.4
DIST_STOP_MAX = 15.5

# configure Gps
gpsd_socket = gps3.GPSDSocket()
data_stream = gps3.DataStream()
gpsd_socket.connect()
gpsd_socket.watch()

global outfile

# Bring up can0 interface at 500kbps
os.system("sudo /sbin/ip link set can0 up type can bitrate 500000")
time.sleep(0.1)

try:
    bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
except OSError:
    print('Cannot find PiCAN board.')
    GPIO.output(led,False)
    exit()

def geo_fence_depot(lat,lon):
    return lat < DEPOT_LAT_NORTH and lat > DEPOT_LAT_SOUTH and lon < DEPOT_LONG_EAST and lon > DEPOT_LONG_WEST

def geo_fence_start(lat,lon,dist,spd):
    geofence =  lat < START_LAT_NORTH and lat > START_LAT_SOUTH and lon < START_LONG_EAST and lon > START_LONG_WEST
    dist_check = dist > DIST_START_MIN and dist < DIST_START_MAX and spd == 0
    return geofence or dist_check

def geo_fence_stop(lat,lon,dist,spd):
    geofence = lat < STOP_LAT_NORTH and lat > STOP_LAT_SOUTH and lon < STOP_LONG_EAST and lon > STOP_LONG_WEST
    dist_check = dist > DIST_STOP_MIN and dist < DIST_STOP_MAX and spd == 0
    return geofence or dist_check

def can_rx_task():
    while True:
        message = bus.recv()
        if message.arbitration_id == PID_REPLY:
            q.put(message)

def can_tx_task():
    while True:
        GPIO.output(led,True)
        # Send Engine coolant temperature request
        msg = can.Message(arbitration_id=PID_REQUEST,data=[0x02,0x01,ENGINE_COOLANT_TEMP,0x00,0x00,0x00,0x00,0x00],extended_id=False)
        bus.send(msg)
        time.sleep(0.05)
        # Send Engine RPM request
		msg = can.Message(arbitration_id=PID_REQUEST,data=[0x02,0x01,ENGINE_RPM,0x00,0x00,0x00,0x00,0x00],extended_id=False)
		bus.send(msg)
		time.sleep(0.05)
        # Send Vehicle speed  request
		msg = can.Message(arbitration_id=PID_REQUEST,data=[0x02,0x01,VEHICLE_SPEED,0x00,0x00,0x00,0x00,0x00],extended_id=False)
		bus.send(msg)
		time.sleep(0.05)
        # Send Throttle position request
		msg = can.Message(arbitration_id=PID_REQUEST,data=[0x02,0x01,THROTTLE,0x00,0x00,0x00,0x00,0x00],extended_id=False)
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
file_count = 0
file_name = ''

DEPOT_BEGIN = 0

# Main control starts
try:
    while True:
        for i in range(4):
            while(q.empty() == True):
                pass
            message = g.get()

            time2 = message.timestamp
            logged_data = '{0:d},{1:f},'.format(count,time2)

            if message.arbitration_id == PID_REPLY and message.data[2] == ENGINE_COOLANT_TEMP:
                temperature = message.data[3] - 40
            if message.arbitration_id == PID_REPLY and message.data[2] == ENGINE_RPM:
                rpm = round(((message.data[3]*256) + message.data[4])/4)
            if message.arbitration_id == PID_REPLY and message.data[2] == VEHICLE_SPEED:
                speed = message.data[3]
                vspeed2 = speed
            if message.arbitration_id == PID_REPLY and message.data[2] == THROTTLE:
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

        if geo_fence_depot(curr_lat,curr_lon):
            if DEPOT_BEGIN == 0:
                os.system("sudo final_upload.sh")
                time.sleep(0.1)
            if RETURN_TO_DEPOT:
                outfile.close()
                file_open = False
                os.system("sudo final_upload.sh")
                time.sleep(0.1)
        else:
            if geo_fence_start(curr_lat,curr_lon,distance,speed):
                outfile.close()
                file_name = 'log' + str(file_count) + '.csv'
                outfile = open(file_name,'w')
                file_open = True
                file_count += 1
            if geo_fence_stop(curr_lat,curr_lon,distance,speed):
                outfile.close()
                file_name = 'log' + str(file_count) + '.csv'
                outfile = open(file_name,'w')
                file_open = True
                file_count += 1

        if file_open:
            print(logged_data,file = outfile)

        count += 1

except KeyboardInterrupt:
	#Catch keyboard interrupt
	GPIO.output(led,False)
    if file_open:
        outfile.close()
    # close CAN interface
	os.system("sudo /sbin/ip link set can0 down")
	print('\n\rKeyboard interrtupt')
