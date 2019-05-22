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

tx_file = 0
rx_file = 0

def can_rx_task():
    while True:
        message = bus.recv()
        if message.arbitration_id == hf.PID_REPLY:
            q_CAN.put(message)

def can_gps_task():
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
rx = Thread(target = can_rx_task)
rx.start()
tx = Thread(target = can_gps_task)
tx.start()

temperature = 0
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
logged_data = ''

count = 0
sp_count = 0
time_spent_at_stop = 0.0
time_start_at_stop = 0.0
#file_count = 0
outfile = 0
outfile_name = 0
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
    file_open = False
    while True:
        GPIO.output(led,True)
        # Send Throttle position request
        msg = can.Message(arbitration_id=hf.PID_REQUEST,data=[0x02,0x01,hf.THROTTLE,0x00,0x00,0x00,0x00,0x00],extended_id=False)
        bus.send(msg)
        while(q_CAN.empty() == True):
            pass
        message = q_CAN.get()
        if message.arbitration_id == hf.PID_REPLY and message.data[2] == hf.THROTTLE:
            throttle = round((message.data[3]*100)/255)
        # Send Engine RPM request
        msg = can.Message(arbitration_id=hf.PID_REQUEST,data=[0x02,0x01,hf.ENGINE_RPM,0x00,0x00,0x00,0x00,0x00],extended_id=False)
        bus.send(msg)
        while(q_CAN.empty() == True):
            pass
        message = q_CAN.get()
        if message.arbitration_id == hf.PID_REPLY and message.data[2] == hf.ENGINE_RPM:
            rpm = round(((message.data[3]*256) + message.data[4])/4)
        # Send Vehicle speed  request
        msg = can.Message(arbitration_id=hf.PID_REQUEST,data=[0x02,0x01,hf.VEHICLE_SPEED,0x00,0x00,0x00,0x00,0x00],extended_id=False)
        bus.send(msg)
        while(q_CAN.empty() == True):
            pass
        message = q_CAN.get()
        if message.arbitration_id == hf.PID_REPLY and message.data[2] == hf.VEHICLE_SPEED:
            speed_timeStamp = time.time()
            speed = message.data[3]
            vspeed2 = speed
            time2 = message.timestamp

        logged_data = '{0:f}, {0:f}, '.format(time2,speed_timeStamp)
        logged_data += '{0:d}, '.format(rpm) + '{0:d}, '.format(speed) + '{0:d}, '.format(throttle)

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

        # read GPS data
        if q_GPS.empty() == True:
            pass
        else:
            new_data = q_GPS.get()
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

        logged_data += str(curr_lat_temp) + ', ' + str(curr_lon_temp)

        logged_data += ', {0:f}, {1:f}'.format(distance_total,distance)

        print(logged_data)

except KeyboardInterrupt:
    #Catch keyboard interrupt
    GPIO.output(led,False)
    if file_open:
        outfile.close()
        tx_file.close()
        rx_file.close()
        # close CAN interface
    os.system("sudo /sbin/ip link set can0 down")
    print('\n\rKeyboard interrtupt')
