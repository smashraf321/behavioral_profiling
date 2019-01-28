#!/bin/bash

# This is a script for final upload process

COUNT=$(iwconfig 2>&1 | grep ESSID:off/any | wc -l)
NUPLDF=$(ls /home/pi/Documents/smart_car/non_uploaded_logs/ | wc -l)

if [[ "0" -eq $COUNT ]] && [[ "0" -ne $NUPLDF ]]; then

		./Dropbox-Uploader/dropbox_uploader.sh upload /home/pi/Documents/smart_car/non_uploaded_logs/*.log.csv /
		rm -f /home/pi/Documents/smart_car/non_uploaded_logs/*.log.csv

fi

