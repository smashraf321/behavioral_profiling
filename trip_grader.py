#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 08:35:57 2019

@author: ashraf
"""

import grading_helpers as gh
import events_grader as eg
import csv

LAP_NUM = 2
file_n = []
file_n.append('log_LAPS_2019_07_14_15_35_54.csv')
file_n.append('log_LAPS_2019_07_14_15_53_38.csv')
file_n.append('log_LAPS_2019_07_14_16_10_42.csv')
file_n.append('log_LAPS_2019_07_14_16_27_53.csv')
file_n.append('log_LAPS_2019_07_14_16_45_15.csv')
file_n.append('log_LAPS_2019_07_14_17_21_23.csv')
file_name = 'Documents/logs/' + file_n[LAP_NUM - 1]

START_DIST = 0
END_DIST = 1
SPEED_LIM = 2

IP_TYPE = 0

IP_SCORE = 0
SL_COUNTER = 1
IP_SP_COUNTER = 2

ip_dist_counter = 0
speed_lim_counter = 0
ip_stop_pos_counter = 0

speeds = []
accelerations = []
distance_intervals = []
event_distances = []
total_event_distance = 0.0
return_values = []
stop_score = 0
signal_score = 0
straight_score = 0
stops_count = 0
signals_count = 0
straights_count = 0

try:
    with open(file_name,'r') as csv_file:
        csv_reader = csv.DictReader(csv_file, fieldnames = gh.field_names, delimiter = ',')
        for rows in csv_reader:
            if float(rows['distance_in_lap']) >= gh.ip_distances[ip_dist_counter][START_DIST] and float(rows['distance_in_lap']) <= gh.ip_distances[ip_dist_counter][END_DIST]:
                speeds.append(int(rows['speed']))
                accelerations.append(float(rows['acceleration']))
                distance_intervals.append(float(rows['distance_interval']))
                event_distances.append(float(rows['distance_in_lap']))
                total_event_distance += float(rows['distance_interval'])
            elif speeds:
                if gh.ip_type[ip_dist_counter][IP_TYPE] == 'stop':
                    return_values = eg.stop_grading(speeds, accelerations, distance_intervals, event_distances, total_event_distance, ip_dist_counter, speed_lim_counter, ip_stop_pos_counter)
                    stop_score += return_values[IP_SCORE]
                    stops_count += 1
                elif gh.ip_type[ip_dist_counter][IP_TYPE] == 'signal':
                    return_values = eg.signal_grading(speeds, accelerations, distance_intervals, event_distances, total_event_distance, ip_dist_counter, speed_lim_counter, ip_stop_pos_counter)
                    signal_score += return_values[IP_SCORE]
                    signals_count += 1
                elif gh.ip_type[ip_dist_counter][IP_TYPE] == 'straight':
                    return_values = eg.straight_grading(speeds, accelerations, distance_intervals, event_distances, total_event_distance, ip_dist_counter, speed_lim_counter, ip_stop_pos_counter)
                    straight_score += return_values[IP_SCORE]
                    straights_count += 1
                else:
                    pass
                # send all 3 counter values, make function return speedlim counters, stoppos counters n scores as list cuz they may change within an event
                # empty the lists, i.e sent information
                speeds = []
                accelerations = []
                distance_intervals = []
                event_distances = []
                total_event_distance = 0.0
                speed_lim_counter = return_values[SL_COUNTER]
                ip_stop_pos_counter = return_values[IP_SP_COUNTER]
                return_values = []
                # update ip_dist_counter, and unpack other counters from function return values
                ip_dist_counter += 1
                if ip_dist_counter == gh.number_of_ips:
                    break
            else:
                pass
        final_trip_score = (stop_score / (stops_count * 100)) * gh.stops_trip_weight + (signal_score / (signals_count * 100)) * gh.signals_trip_weight + (straight_score / (straights_count * 100)) * gh.straights_trip_weight
        print('Stop_scores are ' + str(stop_score) + ' out of ' + str(stops_count * 100))
        print('Signal_scores are ' + str(signal_score) + ' out of ' + str(signals_count * 100))
        print('Straight_scores are ' + str(straight_score) + ' out of ' + str(straights_count * 100))
        print('Final trip score is ' + str(final_trip_score) + ' out of 40')

except Exception:
    print('Something went wrong :(')
