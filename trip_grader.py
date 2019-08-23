#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 08:35:57 2019

@author: ashraf
"""

import grading_helpers as gh
import events_grader as eg
import csv
import sys

# lap number for choosing corresponding file
LAP_NUM = 4

file_extension = '.csv'
#f_name = 'Documents/logs/lap_' + str(LAP_NUM)
f_name = 'C:\\Users\\DELL\\PycharmProjects\\behavioral_profiling\\Documents\\logs\\lap_' + str(LAP_NUM)
file_name = f_name + file_extension

START_DIST = 0
END_DIST = 1

segment_counter = 0

speeds = []
accelerations = []
jerks = []
distance_intervals = []
segment_distances = []
total_segment_distance = 0.0
total_trip_distance = 0.0

REGULAR = False
SPECIAL = False
regular_weight = 0.0
regular_importance_weight = 100
regular_distance_weight = 0
regular_distance = 0.0
regular_score = 0.0
regular_scores = 0.0
special_weight = 0.0
special_importance_weight = 100
special_distance_weight = 0
special_distance = 0.0
special_score = 0.0
special_scores = 0.0

"""
segment counter starts from zero and is incremented after every segment is over and graded
"""
try:
    with open(file_name,'r') as csv_file:
        csv_reader = csv.DictReader(csv_file, fieldnames = gh.field_names, delimiter = ',')
        for rows in csv_reader:
            # if dist travelled as per csv file is more than the segment counter end limit
            # denotes end of segment. So grade it based on segment type
            if float(rows['distance_in_lap']) >= gh.segment_limits[segment_counter][END_DIST]:
                if gh.segment_type[segment_counter] == 'straight':
                    REGULAR = True
                    regular_score = eg.regular_grading(speeds, accelerations, jerks, distance_intervals, segment_distances, total_segment_distance, segment_counter, LAP_NUM)
                    regular_distance += total_segment_distance
                    regular_scores += regular_score * total_segment_distance
                else:
                    SPECIAL = True
                    special_score = eg.special_grading(speeds, accelerations, jerks, distance_intervals, segment_distances, total_segment_distance, segment_counter, LAP_NUM)
                    special_distance += total_segment_distance
                    special_scores += special_score * total_segment_distance

                # reset required variables
                total_trip_distance += total_segment_distance
                speeds = []
                accelerations = []
                jerks = []
                distance_intervals = []
                segment_distances = []
                total_segment_distance = 0.0
                # increment segment counter
                segment_counter += 1
            #if gh.segment_limits[segment_counter][START_DIST] <= float(rows['distance_in_lap']) < gh.segment_limits[segment_counter][END_DIST]:
            # if its not above segment end limit and acc. data is available,
            # append required raw data to their respective list
            if rows['acceleration'] != 'n/a':
                speeds.append(int(rows['speed']))
                accelerations.append(float(rows['acceleration']))
                jerks.append(float(rows['jerk']))
                distance_intervals.append(float(rows['grading_distance']))
                segment_distances.append(float(rows['distance_in_lap']))
                total_segment_distance += float(rows['grading_distance'])

        # After exiting from loop above, if any pending event (i.e. speeds [] not empty), grade accordingly as above
        if speeds:
            if gh.segment_type[segment_counter] == 'straight':
                REGULAR = True
                regular_score = eg.regular_grading(speeds, accelerations, jerks, distance_intervals, segment_distances, total_segment_distance, segment_counter, LAP_NUM)
                regular_distance += total_segment_distance
                regular_scores += regular_score * total_segment_distance
            else:
                SPECIAL = True
                special_score = eg.special_grading(speeds, accelerations, jerks, distance_intervals, segment_distances, total_segment_distance, segment_counter, LAP_NUM)
                special_distance += total_segment_distance
                special_scores += special_score * total_segment_distance

            total_trip_distance += total_segment_distance
            #reset required variables
            speeds = []
            accelerations = []
            jerks = []
            distance_intervals = []
            segment_distances = []
            return_values = []
            total_segment_distance = 0.0

        # if both Regular and Special zones were graded, set the weights for each as below to combine scores
        if REGULAR and SPECIAL:
            regular_importance_weight = 33
            special_importance_weight = 67

        regular_scores = regular_scores / regular_distance
        special_scores = special_scores / special_distance

        # calculating distance weight
        regular_distance_weight = ((regular_distance / total_trip_distance) * 100)
        special_distance_weight = ((special_distance / total_trip_distance) * 100)

        # total weight combined 50% each
        regular_weight = (regular_importance_weight * 0.5) + ((regular_distance_weight) * 0.5)
        special_weight = (special_importance_weight * 0.5) + ((special_distance_weight) * 0.5)

        print('regular distance = ' + str(regular_distance) + ', special distance = ' + str(special_distance) + ', total distance = ' + str(total_trip_distance))
        print('regular importance weight = ' + str(regular_importance_weight) + ', special_importance_weight = ' + str(special_importance_weight))
        print('regular distance weight = ' + str(regular_distance_weight) + ', special distance weight = ' + str(special_distance_weight))
        print('regular weight = ' + str(regular_weight) + ', special weight = ' + str(special_weight))
        print('regular score = ' + str(regular_scores) + ', special score = ' + str(special_scores))

        # producing final trip score
        final_trip_score = regular_scores * regular_weight / 100 + special_scores * special_weight / 100

        print('Final trip score is ' + str(final_trip_score) + ' out of 100')

except Exception as e:
    print('Something went wrong :(')

    print(sys.exc_value)
