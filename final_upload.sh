#!/bin/bash

# This is a script for upload process to dropbox and firestore

COUNT=$(iwconfig 2>&1 | grep ESSID:off/any | wc -l)
NUPLDF=$(ls /home/pi/behavioral_profiling/Documents/logs/ | wc -l)

if [[ "0" -eq $COUNT ]] && [[ "0" -ne $NUPLDF ]]; then

		./Dropbox-Uploader/dropbox_uploader.sh upload /home/pi/behavioral_profiling/Documents/logs/*.csv /
		source /home/pi/firestore/bin/activate
		python3 firestore_parse_n_upload.py
		deactivate
		rm -f /home/pi/behavioral_profiling/Documents/logs/*.csv

fi
