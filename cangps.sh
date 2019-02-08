#!/bin/bash

# This is a script for logging can data

echo 1 > /home/pi/Documents/smart_car/tracker.txt
#python3 -u /home/pi/Documents/smart_car/cangps.py > /home/pi/Documents/smart_car/$(date +"%m.%d.%y_%H.%M.%S").log.csv
python3 -u /home/pi/Documents/smart_car/cangps.py | tee /home/pi/Documents/smart_car/$(date +"%m.%d.%y_%H.%M.%S").log.csv
