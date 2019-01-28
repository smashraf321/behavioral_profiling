#!/bin/bash

# First, can script starts during bootup keeps reading till bus reaches depot.
# This means we have time to take into account.
# Once the bus reaches depot, I stop the can script and upload to dropbox.
# I then increase the word count of my tracker.txt so i dont try to upload.
# I remove the log file from raspberry pi
# The can script should start reading again.
# This can be time based and tracker is reset to one.
# Now I keep logging can script again till I know trip is completed.
# I then try to upload again.
# so uploading and  is always time based
# python script start can also be time based

COUNT=$(iwconfig 2>&1 | grep ESSID | wc -l)
TRACKER=$(cat /home/pi/Documents/smart_car/tracker.txt | wc -l)

if [[ "1" -eq "$COUNT" ]] && [[ "1" -eq "$TRACKER" ]]; then

		kill -9 $(pidof python3)
		cd /home/pi/Dropbox-Uploader
		./dropbox_uploader.sh upload ../Documents/smart_car/*log.csv / 
		echo 1 >> /home/pi/Documents/smart_car/tracker.txt;
		rm -f /home/pi/Documents/smart_car/*.log.csv

fi

