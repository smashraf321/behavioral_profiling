#!/bin/bash

# This is a script for upload process to dropbox and firestore

COUNT=$(iwconfig 2>&1 | grep -q ESSID:off/any | wc -l)
WIFI_STAT=$(ping -q -c3 8.8.8.8 | awk '/received/ {print $4}')
NUPLDF=$(ls /home/pi/behavioral_profiling/Documents/logs/ | wc -l)

if [ $COUNT == "0" ] && [ $WIFI_STAT == "3" ] && [ $NUPLDF > "1" ]; then

		./Dropbox-Uploader/dropbox_uploader.sh upload /home/pi/behavioral_profiling/Documents/logs/*.csv /
		source /home/pi/firestore/bin/activate
		python3 firestore_parse_n_upload.py
		deactivate
		rm -f /home/pi/behavioral_profiling/Documents/logs/*.csv

fi
