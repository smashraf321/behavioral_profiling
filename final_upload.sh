#!/bin/bash

# This is a script for final upload process

COUNT=$(iwconfig 2>&1 | grep ESSID:off/any | wc -l)
NUPLDF=$(ls /home/pi/behavioral_profiling/Documents/logs/ | wc -l)

if [[ "0" -eq $COUNT ]] && [[ "0" -ne $NUPLDF ]]; then

		./Dropbox-Uploader/dropbox_uploader.sh upload /home/pi/behavioral_profiling/Documents/logs/*.csv /
		rm -f /home/pi/behavioral_profiling/Documents/logs/*.csv

fi
