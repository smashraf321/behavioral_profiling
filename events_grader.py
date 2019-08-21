#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 08:37:06 2019

@author: ashraf
"""

import grading_helpers as gh
import math

START_DIST = 0
END_DIST = 1

STOP_SIGN = 1

SPEED_LIMIT = 0
JERK_LIMIT_REG = 7
JERK_LIMIT_SP = 5
POLY_ACCN_A = 1
POLY_ACCN_B = 2
POLY_ACCN_C = 3
POLY_DCCN_A = 4
POLY_DCCN_B = 5
POLY_DCCN_C = 6
EXP_ACCN_A = 1
EXP_ACCN_B = 2
EXP_DCCN_A = 3
EXP_DCCN_B = 4

def get_poly_threshold(A, B, C, X):
    return (A*X*X + B*X + C)

def get_exp_threshold(A, B, X):
    return (A * pow(math.e, X * B))

def regular_grading(speeds, accelerations, jerks, distance_intervals, segment_distances, total_segment_distance, segment_counter):
    segment_score = 0.0
    num_values = len(speeds)
    zone_counter = 0
    speed_score = 0.0
    accn_score = 0.0
    jerk_score = 0.0
    point_score = 0.0

    for i in range(num_values):
        speed_weight = 100
        accn_weight = 0
        jerk_weight = 0
        if segment_distances[i] >= gh.zone_limits[segment_counter][zone_counter][END_DIST]:
            zone_counter += 1
        # Speed score calculations
        speed_limit = gh.zone_thresholds[segment_counter][zone_counter][SPEED_LIMIT]
        if speeds[i] > speed_limit:
            speed_score = (1 - ((speeds[i] - speed_limit)/speed_limit)) * 100
        else:
            speed_score = 100
        # Accns score calculation
        accn_a = gh.zone_thresholds[segment_counter][zone_counter][POLY_ACCN_A]
        accn_b = gh.zone_thresholds[segment_counter][zone_counter][POLY_ACCN_B]
        accn_c = gh.zone_thresholds[segment_counter][zone_counter][POLY_ACCN_C]
        dccn_a = gh.zone_thresholds[segment_counter][zone_counter][POLY_DCCN_A]
        dccn_b = gh.zone_thresholds[segment_counter][zone_counter][POLY_DCCN_B]
        dccn_c = gh.zone_thresholds[segment_counter][zone_counter][POLY_DCCN_C]
        if accelerations[i] > 0:
            accn_weight = 50
            speed_weight = 50
            accn_limit = get_poly_threshold(accn_a, accn_b, accn_c, speeds[i])
            if accelerations[i] > accn_limit:
                accn_score = (1 - ((accelerations[i] - accn_limit)/accn_limit)) * 100
            else:
                accn_score = 100
        if accelerations[i] < 0:
            accn_weight = 50
            speed_weight = 50
            accn_limit = get_poly_threshold(dccn_a, dccn_b, dccn_c, speeds[i])
            if abs(accelerations[i]) > accn_limit:
                accn_score = (1 - ((abs(accelerations[i]) - accn_limit)/accn_limit)) * 100
            else:
                accn_score = 100
        # Jerk score calculation
        jerk_limit = gh.zone_thresholds[segment_counter][zone_counter][JERK_LIMIT_REG]
        if jerks[i] != 0:
            jerk_weight = 33
            accn_weight = 34
            speed_weight = 33
            if abs(jerks[i]) > jerk_limit:
                jerk_score = (1 - ((abs(jerks[i]) - jerk_limit)/jerk_limit)) * 100
            else:
                jerk_score = 100
        # Final point calculation
        point_score = (speed_score * (speed_weight / 100)) + (accn_score * (accn_weight / 100)) + (jerk_score * (jerk_weight / 100))
        # print('speed = ' + str(speeds[i]) + ', accn = ' + str(accelerations[i]) + ', jerk = ' + str(jerks[i]))
        # print('speed weight = ' + str(speed_weight) + ', accn weight = ' + str(accn_weight) + ', jerk weight = ' + str(jerk_weight))
        # print('speed score = ' + str(speed_score) + ', accn score = ' + str(accn_score) + ', jerk score = ' + str(jerk_score))
        # print('point score = ' + str(point_score))
        # print(' ')
        segment_score += point_score * distance_intervals[i]
    # Segment score calculation
    segment_score = segment_score / total_segment_distance
    print('regular segment score = ' + str(segment_score))
    print(' ')
    if segment_score < 0:
        segment_score = 0.0
    return segment_score

def special_grading(speeds, accelerations, jerks, distance_intervals, segment_distances, total_segment_distance, segment_counter):
    segment_score = 0.0
    complete_stop_score = 0.0
    hesitation_score = 0.0
    segment_weight = 33
    complete_stop_weight = 34
    hesitation_weight = 33

    num_values = len(speeds)
    zone_counter = 0
    speed_score = 0.0
    accn_score = 0.0
    jerk_score = 0.0
    point_score = 0.0

    min_speed = 1000
    STOP_SPEED = 3
    num_hesitation = 0
    NEGATIVE_ONGOING = False
    POSITIVE_ONGOING = False

    for i in range(num_values):
        speed_weight = 100
        accn_weight = 0
        jerk_weight = 0
        if segment_distances[i] >= gh.zone_limits[segment_counter][zone_counter][END_DIST]:
            zone_counter += 1
        # Speed score calculations
        speed_limit = gh.zone_thresholds[segment_counter][zone_counter][SPEED_LIMIT]
        if speeds[i] > speed_limit:
            speed_score = (1 - ((speeds[i] - speed_limit)/speed_limit)) * 100
        else:
            speed_score = 100
        # Accns score calculation
        accn_a = gh.zone_thresholds[segment_counter][zone_counter][EXP_ACCN_A]
        accn_b = gh.zone_thresholds[segment_counter][zone_counter][EXP_ACCN_B]
        dccn_a = gh.zone_thresholds[segment_counter][zone_counter][EXP_DCCN_A]
        dccn_b = gh.zone_thresholds[segment_counter][zone_counter][EXP_DCCN_B]
        if accelerations[i] > 0:
            accn_weight = 50
            speed_weight = 50
            accn_limit = get_exp_threshold(accn_a, accn_b, speeds[i])
            if accelerations[i] > accn_limit:
                accn_score = (1 - ((accelerations[i] - accn_limit)/accn_limit)) * 100
            else:
                accn_score = 100
        if accelerations[i] < 0:
            accn_weight = 50
            speed_weight = 50
            accn_limit = get_exp_threshold(dccn_a, dccn_b, speeds[i])
            if abs(accelerations[i]) > accn_limit:
                accn_score = (1 - ((abs(accelerations[i]) - accn_limit)/accn_limit)) * 100
            else:
                accn_score = 100
        # Jerk score calculation
        jerk_limit = gh.zone_thresholds[segment_counter][zone_counter][JERK_LIMIT_SP]
        if jerks[i] != 0:
            jerk_weight = 33
            accn_weight = 34
            speed_weight = 33
            if abs(jerks[i]) > jerk_limit:
                jerk_score = (1 - ((abs(jerks[i]) - jerk_limit)/jerk_limit)) * 100
            else:
                jerk_score = 100
        # Catch lowest speed in stop sign zone and hesitation check
        if zone_counter == STOP_SIGN and gh.segment_type[segment_counter] == 'stop':
            # stop sign speed check
            if speeds[i] < min_speed:
                min_speed = speeds[i]
            # hesitation check
            if accelerations[i] < 0.0:
                NEGATIVE_ONGOING = True
                POSITIVE_ONGOING = False
            elif accelerations[i] > 0.0 and NEGATIVE_ONGOING and not POSITIVE_ONGOING:
                num_hesitation += 1
                POSITIVE_ONGOING = True
            else:
                pass
        # Final point calculation
        point_score = (speed_score * (speed_weight / 100)) + (accn_score * (accn_weight / 100)) + (jerk_score * (jerk_weight / 100))
        # print('speed = ' + str(speeds[i]) + ', accn = ' + str(accelerations[i]) + ', jerk = ' + str(jerks[i]))
        # print('speed weight = ' + str(speed_weight) + ', accn weight = ' + str(accn_weight) + ', jerk weight = ' + str(jerk_weight))
        # print('speed score = ' + str(speed_score) + ', accn score = ' + str(accn_score) + ', jerk score = ' + str(jerk_score))
        # print('point score = ' + str(point_score))
        # print(' ')
        segment_score += point_score * distance_intervals[i]
    # Segment score calculation
    segment_score = segment_score / total_segment_distance
    if gh.segment_type[segment_counter] == 'stop':
        # Complete stop score calculation
        if min_speed <= STOP_SPEED:
            complete_stop_score = 100
        else:
            complete_stop_score = 100 - pow(min_speed - STOP_SPEED, 3)
        # Hesitation score calculation
        if num_hesitation > 1:
            hesitation_score = 100 - pow(num_hesitation - 1, 3)
        else:
            hesitation_score = 100
        segment_score = (segment_score * (segment_weight / 100)) + (complete_stop_score * (complete_stop_weight / 100)) + (hesitation_score * (hesitation_weight / 100))
    print('special segment score = ' + str(segment_score))
    print(' ')
    if segment_score < 0:
        segment_score = 0.0
    return segment_score
