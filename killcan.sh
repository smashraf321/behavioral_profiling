#!/bin/bash

if [[ "1" -eq $(pidof python3 | wc -l) ]]; then
	kill -9 $(pidof python3)
	mv /home/pi/Documents/smart_car/*.log.csv /home/pi/Documents/smart_car/non_uploaded_logs/
fi

if [[ "1" -eq $(pidof curl | wc -l) ]]; then
	mv /home/pi/Documents/smart_car/*.log.csv /home/pi/Documents/smart_car/non_uploaded_logs/
	kill -9 $(pidof curl)
fi
