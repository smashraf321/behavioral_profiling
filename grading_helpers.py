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

segment_type = {
        0 :['start'],
        1 :['straight'],
        2 :['stop'],
        3 :['straight'],
        4 :['signal'],
        5 :['straight'],
        6 :['stop'],
        7 :['straight'],
        8 :['signal'],
        9 :['straight'],
        10:['turn'],
        11:['straight'],
        12:['turn'],
        13:['straight'],
        14:['stop'],
        15:['straight'],
        16:['signal'],
        17:['straight'],
        18:['signal'],
        19:['straight'],
        20:['signal'],
        21:['straight'],
        22:['signal'],
        23:['straight'],
        24:['signal'],
        25:['signal'],
        26:['straight'],
        27:['roundabout'],
        28:['straight',1],
        29:['roundabout',11.838300,-0.215907,1,5,0,5,10,1,1.2,5],
        30:['straight',1],
        31:['roundabout',11.838300,-0.215907,1,5,0,5,10,1,1.2,5],
        32:['straight',1],
        33:['turn',11.838300,-0.215907,1,5,0,5,10,1,1.2,5],
        34:['straight',1]
        }

segment_limits = []
ip_distances.append((0.0,20.0))
ip_distances.append((20.0,70.0))#1
ip_distances.append((70.0,150.0))
ip_distances.append((150.0,1800))#3
ip_distances.append((1800.0,2200.0))
ip_distances.append((2200.0,4200.0))#5
ip_distances.append((4200.0,4375.0))
ip_distances.append((4375.0,4500.0))#7
ip_distances.append((4500.0,4670.0))
ip_distances.append((4670.0,4700.0))#9
ip_distances.append((4700.0,4820.0))
ip_distances.append((4820.0,4880.0))#11
ip_distances.append((4880.0,4950.0))
ip_distances.append((4950.0,4980.0))#13
ip_distances.append((4980.0,5100.0))
ip_distances.append((5100.0,5150.0))#15
ip_distances.append((5150.0,5400.0))
ip_distances.append((5400.0,7000.0))#17
ip_distances.append((7000.0,7250.0))
ip_distances.append((7250.0,9100.0))#19
ip_distances.append((9100.0,9350.0))
ip_distances.append((9350.0,9700.0))#21
ip_distances.append((9700.0,9950.0))
ip_distances.append((9950.0,10200.0))#23
ip_distances.append((10200.0,10430.0))
ip_distances.append((10430.0,10600.0))
ip_distances.append((10600.0,10950.0))#26
ip_distances.append((10950.0,11075.0))
ip_distances.append((11075.0,11375.0))#28
ip_distances.append((11375.0,11510.0))
ip_distances.append((11510.0,11830.0))#30
ip_distances.append((11830.0,11960.0))
ip_distances.append((11960.0,12020.0))#32
ip_distances.append((12020.0,12100.0))
ip_distances.append((12100.0,12750.0))#34


stop_positions = []
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

zone_limits = []
zone_limits.append([(0.0,20.0)])

speed_limits = []
speed_limits.append([(40.0,Aaccn,Baccn,Adccn,Bdccn,JT),(40.0,Aaccn,Baccn,Adccn,Bdccn,JT),(40.0,Aaccn,Baccn,Adccn,Bdccn,JT)])
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

stops_trip_weight = 15
signals_trip_weight = 15
straights_trip_weight = 10
