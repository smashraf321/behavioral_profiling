#!/bin/bash

# This is a script for automating the upload process

COUNT=$(iwconfig 2>&1 | grep ESSID:off/any | wc -l)
TRACKER=$(cat /home/pi/Documents/smart_car/tracker.txt | wc -l)
NUPLDF=$(ls /home/pi/Documents/smart_car/non_uploaded_logs | wc -l)

if [[ "0" -eq $COUNT ]] && [[ "1" -eq $TRACKER ]]
then
 kill -9 $(pidof python3)
 ./Dropbox-Uploader/dropbox_uploader.sh upload /home/pi/Documents/smart_car/*.log.csv / 
 echo 1 >> /home/pi/Documents/smart_car/tracker.txt;
 rm -f /home/pi/Documents/smart_car/*.log.csv

 if [[ "0" -ne $NUPLDF ]]
 then
  ./Dropbox-Uploader/dropbox_uploader.sh upload /home/pi/Documents/smart_car/non_uploaded_logs/*.log.csv /
  rm -f /home/pi/Documents/smart_car/non_uploaded_logs/*.log.csv
 fi
fi

