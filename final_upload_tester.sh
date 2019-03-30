#!/bin/bash

# This is a script for upload process to dropbox and firestore

COUNT=$(iwconfig 2>&1 | grep -q ESSID:off/any | wc -l)
WIFI_STAT=$(ping -q -c3 8.8.8.8 | awk '/received/ {print $4}')
NUPLDF=$(ls /home/pi/behavioral_profiling/Documents/logs/ | wc -l)

if [[ "0" -eq "$COUNT" ]] && [[ "3" -eq "$WIFI_STAT"]] && [[ "0" -ne "$NUPLDF" ]]; then

		echo $HOME

fi
