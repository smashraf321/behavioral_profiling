#!/bin/bash

COUNT=$(iwconfig 2>&1 | grep ESSID | wc -l)
TRACKER=$(cat /home/pi/Documents/smart_car/tracker.txt | wc -l)

if [[ "1" -eq "$COUNT" ]]; then

	if [[ "1" -eq "$TRACKER" ]]; then

		kill -9 $(pidof python3)
		./home/pi/Dropbox-Uploader/dropbox_uploader.sh upload ../Documents/smart_car/*log.csv / 
		echo 1 >> /home/pi/Documents/smart_car/tracker.txt;
		rm -f /home/pi/Documents/smart_car/*.log.csv
	fi
fi

