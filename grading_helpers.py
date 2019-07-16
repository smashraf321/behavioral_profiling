#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 10:14:51 2019

@author: ashraf
"""

field_names = []
field_names.append('index')
field_names.append('time_stamp')
field_names.append('total_trips_time')
field_names.append('time_during_lap')
field_names.append('time_interval')
field_names.append('throttle')
field_names.append('rpm')
field_names.append('speed')
field_names.append('acceleration')
field_names.append('latitude')
field_names.append('longitude')
field_names.append('total_trips_distance')
field_names.append('distance_interval')
field_names.append('distance_in_lap')

number_of_ips = 12

ip_type = {
        0:['stop',11.838300,-0.215907,3,5,7,7,0,0,0,0],
        1:['signal',11.838300,-0.215907,1,10,0,10,15,1,1.2,5],
        2:['straight',12.205306,-0.199665,1,10,0,0,25,1,0,0],
        3:['stop',11.210319,-0.258248,2,7,10,10,0,0,0,0],
        4:['signal',11.838300,-0.215907,1,5,0,7,10,1,1.2,5],
        5:['stop',11.838300,-0.215907,2,5,7,7,0,0,0,0],
        6:['signal',11.838300,-0.215907,1,5,0,7,10,1,1.2,5],
        7:['signal',11.838300,-0.215907,1,5,0,7,10,1,1.2,5],
        8:['signal',11.838300,-0.215907,1,5,0,5,10,1,1.2,5],
        9:['signal',11.838300,-0.215907,1,5,0,5,10,1,1.2,5],
        10:['signal',11.838300,-0.215907,1,5,0,5,10,1,1.2,5],
        11:['signal',11.838300,-0.215907,1,5,0,5,10,1,1.2,5]
        }

ip_distances = []
ip_distances.append((70.0,150.0))
ip_distances.append((1800.0,2200.0))
ip_distances.append((2300.0,2550.0))# this is for linear stretch
ip_distances.append((4200.0,4375.0))
ip_distances.append((4500.0,4650.0))
ip_distances.append((4980.0,5100.0))
ip_distances.append((5150.0,5400.0))
ip_distances.append((7000.0,7250.0))
ip_distances.append((9100.0,9350.0))
ip_distances.append((9700.0,9950.0))
ip_distances.append((10200.0,10400.0))
ip_distances.append((10425.0,10600.0))

speed_limits = []
speed_limits.append((70.0,110.0,40))
speed_limits.append((111.0,150.0,75))
speed_limits.append((1800.0,2020.0,60))
speed_limits.append((2020.0,2200.0,55))
speed_limits.append((2300.0,2550.0,70))
speed_limits.append((4200.0,4310.0,60))
speed_limits.append((4311.0,4375.0,60))
speed_limits.append((4500.0,4650.0,55))
speed_limits.append((4980.0,5055.0,35))
speed_limits.append((4056.0,5100.0,40))
speed_limits.append((5150.0,5400.0,70))
speed_limits.append((7000.0,7250.0,70))
speed_limits.append((9100.0,9350.0,70))
speed_limits.append((9700.0,9950.0,70))
speed_limits.append((10200.0,10400.0,70))
speed_limits.append((10425.0,10600.0,70))

ip_stop_positions = []
ip_stop_positions.append((90.0,110.0))
ip_stop_positions.append((1995.0,2020.0))
ip_stop_positions.append((4290.0,4310.0))
ip_stop_positions.append((4595.0,4610.0))
ip_stop_positions.append((5033.0,5055.0))
ip_stop_positions.append((5215.0,5235.0))
ip_stop_positions.append((7090.0,7130.0))
ip_stop_positions.append((9180.0,9215.0))
ip_stop_positions.append((9795.0,9820.0))
ip_stop_positions.append((10315.0,10350.0))
ip_stop_positions.append((10500.0,10520.0))

stops_trip_weight = 15
signals_trip_weight = 15
straights_trip_weight = 10
