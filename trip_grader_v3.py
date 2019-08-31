#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 08:35:57 2019

@author: ashraf
"""

import grading_helpers as gh
import events_grader_v3 as eg
import csv
import sys

# lap number for choosing corresponding file
LAP_NUM = 6

SAVE_SEGMENT_SCORES = False

file_extension = '.csv'
#f_name = 'Documents/logs/lap_' + str(LAP_NUM)
f_name = 'C:\\Users\\DELL\\PycharmProjects\\behavioral_profiling\\Documents\\logs\\lap_' + str(LAP_NUM)
f_segment_name = 'C:\\Users\\DELL\\PycharmProjects\\behavioral_profiling\\Documents\\graphs\\lap_' + str(LAP_NUM)
file_name = f_name + file_extension

START_DIST = 0
END_DIST = 1

GRADING_DISTANCES = [(0,12750)]
grading_segment_counter = 0

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
regular_weight = 1
regular_distance = 0.0
special_weight = 2
special_distance = 0.0
segment_weight = 0.0
segment_score = 0.0
weighted_segment_score = 0.0
segment_scores = 0.0
total_weight = 0.0

best_segments = []
best_segment_score = 0
worst_segments = []
worst_segment_score = 100

if SAVE_SEGMENT_SCORES:
    segment_file = open(f_segment_name + '_' + '_segments.csv','w+')
    print('segment#,segment score,importance weight,distance weight, segment weight',file = segment_file)

segment_scores_n_weights = ''

"""
segment counter starts from zero and is incremented after every segment is over and graded
"""
try:
    with open(file_name,'r') as csv_file:
        csv_reader = csv.DictReader(csv_file, fieldnames = gh.field_names, delimiter = ',')
        print('Lap num: '+ str(LAP_NUM))
        for rows in csv_reader:
            # if dist travelled as per csv file is more than the segment counter end limit
            # denotes end of segment. So grade it based on segment type
            if float(rows['distance_in_lap']) >= gh.segment_limits[segment_counter][END_DIST]:
                if speeds:
                    if gh.segment_type[segment_counter] == 'straight':
                        REGULAR = True
                        segment_score = eg.regular_grading(speeds, accelerations, jerks, distance_intervals, segment_distances, total_segment_distance, segment_counter, LAP_NUM)
                        regular_distance += total_segment_distance
                        segment_weight = regular_weight * total_segment_distance
                        weighted_segment_score = segment_score * segment_weight
                        total_weight += segment_weight
                        segment_scores += weighted_segment_score

                        if SAVE_SEGMENT_SCORES:
                            segment_scores_n_weights = str(segment_counter) + ','
                            segment_scores_n_weights += str(segment_score) + ',' + str(regular_weight) + ',' + str(total_segment_distance) + ',' + str(segment_weight)
                            print(segment_scores_n_weights, file = segment_file)

                    else:
                        SPECIAL = True
                        segment_score = eg.special_grading(speeds, accelerations, jerks, distance_intervals, segment_distances, total_segment_distance, segment_counter, LAP_NUM)
                        special_distance += total_segment_distance
                        segment_weight = special_weight * total_segment_distance
                        weighted_segment_score = segment_score * segment_weight
                        total_weight += segment_weight
                        segment_scores += weighted_segment_score

                        if SAVE_SEGMENT_SCORES:
                            segment_scores_n_weights = str(segment_counter) + ','
                            segment_scores_n_weights += str(segment_score) + ',' + str(special_weight) + ',' + str(total_segment_distance) + ',' + str(segment_weight)
                            print(segment_scores_n_weights, file = segment_file)

                # reset required variables
                total_trip_distance += total_segment_distance
                speeds = []
                accelerations = []
                jerks = []
                distance_intervals = []
                segment_distances = []
                total_segment_distance = 0.0

                # for calculating the best and worst segment scores in this lap
                # results are printed at the end of the file parsing
                if segment_score > best_segment_score:
                    best_segments = [segment_counter]
                    best_segment_score = segment_score
                elif segment_score == best_segment_score:
                    best_segments.append(segment_counter)
                else:
                    pass
                if segment_score < worst_segment_score:
                    worst_segments = [segment_counter]
                    worst_segment_score = segment_score
                elif segment_score == worst_segment_score:
                    worst_segments.append(segment_counter)
                else:
                    pass
                # increment segment counter
                segment_counter += 1
            #if gh.segment_limits[segment_counter][START_DIST] <= float(rows['distance_in_lap']) < gh.segment_limits[segment_counter][END_DIST]:
            # if its not above segment end limit and acc. data is available,
            # append required raw data to their respective list
            if float(rows['distance_in_lap']) >= GRADING_DISTANCES[grading_segment_counter][END_DIST]:
                grading_segment_counter += 1
                if grading_segment_counter == len(GRADING_DISTANCES):
                    grading_segment_counter -= 1
            if rows['acceleration'] != 'n/a' and GRADING_DISTANCES[grading_segment_counter][START_DIST] <= float(rows['distance_in_lap']) < GRADING_DISTANCES[grading_segment_counter][END_DIST]:
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
                segment_score = eg.regular_grading(speeds, accelerations, jerks, distance_intervals, segment_distances, total_segment_distance, segment_counter, LAP_NUM)
                regular_distance += total_segment_distance
                segment_weight = regular_weight * total_segment_distance
                weighted_segment_score = segment_score * segment_weight
                total_weight += segment_weight
                segment_scores += weighted_segment_score

                if SAVE_SEGMENT_SCORES:
                    segment_scores_n_weights = str(segment_counter) + ','
                    segment_scores_n_weights += str(segment_score) + ',' + str(regular_weight) + ',' + str(total_segment_distance) + ',' + str(segment_weight)
                    print(segment_scores_n_weights, file = segment_file)

            else:
                SPECIAL = True
                segment_score = eg.special_grading(speeds, accelerations, jerks, distance_intervals, segment_distances, total_segment_distance, segment_counter, LAP_NUM)
                special_distance += total_segment_distance
                segment_weight = special_weight * total_segment_distance
                weighted_segment_score = segment_score * segment_weight
                total_weight += segment_weight
                segment_scores += weighted_segment_score

                if SAVE_SEGMENT_SCORES:
                    segment_scores_n_weights = str(segment_counter) + ','
                    segment_scores_n_weights += str(segment_score) + ',' + str(special_weight) + ',' + str(total_segment_distance) + ',' + str(segment_weight)
                    print(segment_scores_n_weights, file = segment_file)

            total_trip_distance += total_segment_distance

            #reset required variables
            speeds = []
            accelerations = []
            jerks = []
            distance_intervals = []
            segment_distances = []
            return_values = []
            total_segment_distance = 0.0

            #calculating worst and best segment scores
            if segment_score > best_segment_score:
                best_segments = [segment_counter]
                best_segment_score = segment_score
            if segment_score == best_segment_score:
                best_segments.append(segment_counter)
            if segment_score < worst_segment_score:
                worst_segments = [segment_counter]
                worst_segment_score = segment_score
            if segment_score == worst_segment_score:
                worst_segments.append(segment_counter)

        if SAVE_SEGMENT_SCORES:
            segment_file.close()

        print('Lap ' + str(LAP_NUM) + ' Report:')
        print('regular distance = ' + str(regular_distance) + ', special distance = ' + str(special_distance) + ', total distance = ' + str(total_trip_distance))
        print('total_weight = ' + str(total_weight) + ', segment_scores = ' + str(segment_scores))
        print('best segments = ' + str(best_segments) + ', best segment score = ' + str(best_segment_score))
        print('worst segments = ' + str(worst_segments) + ', worst segment score = ' + str(worst_segment_score))

        # producing final trip score
        final_trip_score = segment_scores / total_weight

        print('Final trip score is ' + str(final_trip_score) + ' out of 100')

except Exception as e:
    print('Something went wrong :(')
    print(sys.exc_value)
