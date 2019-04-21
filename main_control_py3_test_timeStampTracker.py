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
    rx_file_open = False
    rx_file = 0
    counterr = 0
    rx_logs = '{0:d}'.format(counterr)
    while True:
        message = bus.recv()
        if message.arbitration_id == hf.PID_REPLY:
            q_CAN.put(message)
            rx_timeStamp = datetime.now().strftime('%H:%M:%S.%f')
            rx_logs += ', ' + rx_timeStamp
            counterr += 1

        if not rx_file_open:
            rx_file_name = 'Documents/logs/log_rx_' + str(datetime.now()) + '.csv'
            rx_file = open(rx_file_name,'w+')
            print('Logging Rx timestamps...')
            rx_file_open = True

        if counterr % 3 == 0 and counterr != 0:
            print(rx_logs,file = rx_file)
            rx_logs = '{0:d}'.format(counterr)


def can_tx_task():
    tx_file_open = False
    tx_file = 0
    while True:
        GPIO.output(led,True)
        # Send Engine RPM request
        msg = can.Message(arbitration_id=hf.PID_REQUEST,data=[0x02,0x01,hf.ENGINE_RPM,0x00,0x00,0x00,0x00,0x00],extended_id=False)
        bus.send(msg)
        rpm_timeStamp = datetime.now().strftime('%H:%M:%S.%f')
        time.sleep(0.05)
        # Send Vehicle speed  request
        msg = can.Message(arbitration_id=hf.PID_REQUEST,data=[0x02,0x01,hf.VEHICLE_SPEED,0x00,0x00,0x00,0x00,0x00],extended_id=False)
        bus.send(msg)
        speed_timeStamp = datetime.now().strftime('%H:%M:%S.%f')
        time.sleep(0.05)
        # Send Throttle position request
        msg = can.Message(arbitration_id=hf.PID_REQUEST,data=[0x02,0x01,hf.THROTTLE,0x00,0x00,0x00,0x00,0x00],extended_id=False)
        bus.send(msg)
        throttle_timeStamp = datetime.now().strftime('%H:%M:%S.%f')
        time.sleep(0.05)
        # End transmission
        GPIO.output(led,False)
        time.sleep(0.15)

        tx_logs = rpm_timeStamp + ', ' + speed_timeStamp  + ', ' + throttle_timeStamp
        if not tx_file_open:
            tx_file_name = 'Documents/logs/log_tx_' + str(datetime.now()) + '.csv'
            tx_file = open(tx_file_name,'w+')
            print('Logging Tx timestamps...')
            tx_file_open = True
        print(tx_logs,file = tx_file)

q_CAN = queue.Queue()
rx = Thread(target = can_rx_task)
rx.start()
tx = Thread(target = can_tx_task)
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
        for i in range(3):
            while(q_CAN.empty() == True):
                pass
            message = q_CAN.get()

            time2 = message.timestamp
            logged_data = '{0:f}, '.format(time2)

            if message.arbitration_id == hf.PID_REPLY and message.data[2] == hf.ENGINE_RPM:
                rpm = round(((message.data[3]*256) + message.data[4])/4)
                rpm_timeStamp = datetime.now().strftime('%H:%M:%S.%f')
            if message.arbitration_id == hf.PID_REPLY and message.data[2] == hf.VEHICLE_SPEED:
                speed = message.data[3]
                vspeed2 = speed
                speed_timeStamp = datetime.now().strftime('%H:%M:%S.%f')
            if message.arbitration_id == hf.PID_REPLY and message.data[2] == hf.THROTTLE:
                throttle = round((message.data[3]*100)/255)
                throttle_timeStamp = datetime.now().strftime('%H:%M:%S.%f')

        logged_data += '{0:d}, '.format(rpm) + rpm_timeStamp + ', ' + '{0:d}, '.format(speed) + speed_timeStamp  + ', ' + '{0:d},'.format(throttle) + throttle_timeStamp + ', '

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
                logged_data += str(curr_lat_temp) + ', ' + str(curr_lon_temp) + ', ' + str(data_stream.TPV['time'] + ', ') + datetime.now().strftime('%H:%M:%S.%f')
                break
            else:
                continue

        logged_data += ', {0:d}, {1:f}, {2:f}'.format(count,distance_total,distance)

        if not file_open:
            file_name = 'Documents/logs/log_DOJ_' + str(datetime.now()) + '.csv'
            outfile = open(file_name,'w+')
            print('Logging data timestamps...')

        print(logged_data,file = outfile)
        file_open = True
        print('...')

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
