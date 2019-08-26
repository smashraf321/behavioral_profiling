#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 08:37:06 2019

@author: ashraf
"""

import grading_helpers as gh
import math
#import matplotlib.pyplot as plt

DEBUG = False
PLOT = False

START_DIST = 0
END_DIST = 1

STOP_SIGN = 1

# index for each threshold present in zone_thresholds list
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

# raw value of speed is obtained in km/h from csv. To convert them into m/s
CONV_FACTOR = 5/18


# straight segments follow a 2 degree polynomial regression. X is speed and A,B,C are coefficients.
def get_poly_threshold(A, B, C, X):
    return (A*X*X + B*X + C)


# special segments tend to follow an exponential regression
def get_exp_threshold(A, B, X):
    return (A * pow(math.e, X * B))


# for plotting graphs for each point in a segment. Also saves it by appending lap num and segment num
def plot_graphs(speeds, speed_limits, accns, accn_limits, dccn_limits, jerks, jerk_limits_positive, jerk_limits_negative
                ,segment_dist, segment_counter, LAP_NUM):
    # f_name = 'Documents/graphs/lap_' + str(LAP_NUM)
    f_name = 'C:\\Users\\DELL\\PycharmProjects\\behavioral_profiling\\Documents\\graphs\\lap_' + str(LAP_NUM)
    # for converting raw data to m/s^2
    speeds = [s*CONV_FACTOR for s in speeds]
    accns = [a*CONV_FACTOR for a in accns]
    jerks = [j*CONV_FACTOR for j in jerks]

    plt.figure()
    plt.plot(segment_dist,speed_limits,label='Speed Limit',c='r',linestyle='-', marker='.', lw=1.0)
    plt.plot(segment_dist,speeds, label='Actual speed', c='g', linestyle='-', marker='.', lw=1.0)
    plt.xlabel('Distance(m)')
    plt.ylabel('Speed(m/s)')
    # helps keep the legend box above the plot
    plt.legend(bbox_to_anchor=(0, 1.02, 1, 0.2), loc="lower left",
               mode="expand", borderaxespad=0, ncol=2)
    #plt.show()
    plt.savefig(f_name + '_' + str(segment_counter) + '_speed' + '.png')
    plt.close()

    plt.figure()
    plt.plot(segment_dist, accn_limits, label='Accn Thresholds', c='r', linestyle='-', marker ='.', lw=1.0)
    plt.plot(segment_dist, dccn_limits, label='Dccn Thresholds', c='r', linestyle='-', marker ='.', lw=1.0)
    plt.plot(segment_dist, accns, label='Actual Accn', c='g', linestyle='-', marker='.', lw=1.0)
    plt.xlabel('Distance(m)')
    plt.ylabel('Acceleration(m/s^2)')
    # helps keep the legend box above the plot
    plt.legend(bbox_to_anchor=(0, 1.02, 1, 0.2), loc="lower left",
               mode="expand", borderaxespad=0, ncol=3)
    # plt.show()
    plt.savefig(f_name + '_' + str(segment_counter) + '_accn' + '.png')
    plt.close()

    plt.figure()
    plt.plot(segment_dist, jerk_limits_positive, label='Jerk +ve Thresholds', c='r', linestyle='-', marker='.', lw=1.0)
    plt.plot(segment_dist, jerk_limits_negative, label='Jerk -ve Thresholds', c='r', linestyle='-', marker='.', lw=1.0)
    plt.plot(segment_dist, jerks, label='Actual Jerks', c='g', linestyle='-', marker='.', lw=1.0)
    plt.xlabel('Distance(m)')
    plt.ylabel('Jerk(m/s^3)')
    # helps keep the legend box above the plot
    plt.legend(bbox_to_anchor=(0, 1.02, 1, 0.2), loc="lower left",
               mode="expand", borderaxespad=0, ncol=3)
    # plt.show()
    plt.savefig(f_name + '_' + str(segment_counter) + '_jerk' + '.png')
    plt.close()


def regular_grading(speeds, accelerations, jerks, distance_intervals, segment_distances, total_segment_distance, segment_counter, LAP_NUM):
    segment_score = 0.0
    # no of points observed in this segment
    num_values = len(speeds)
    zone_counter = 0
    speed_score = 0.0
    accn_score = 0.0
    jerk_score = 0.0
    point_score = 0.0

    # For Plotting purposes
    speed_limits = []
    accn_limits = []
    dccn_limits = []
    jerk_limits_positive = []
    jerk_limits_negative = []

    for i in range(num_values):
        speed_weight = 100
        accn_weight = 0
        jerk_weight = 0

        # increments the zone counter within a segment if above zone limit
        while segment_distances[i] >= gh.zone_limits[segment_counter][zone_counter][END_DIST]:
            zone_counter += 1

        # Speed score calculations
        speed_limit = gh.zone_thresholds[segment_counter][zone_counter][SPEED_LIMIT]
        speed_limits.append(speed_limit*CONV_FACTOR)

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
        accn_limit = get_poly_threshold(accn_a, accn_b, accn_c, speeds[i])
        accn_limits.append(accn_limit*CONV_FACTOR)
        dccn_limit = get_poly_threshold(dccn_a, dccn_b, dccn_c, speeds[i])
        dccn_limits.append(dccn_limit*-1*CONV_FACTOR)

        # if acceleration value is > 0, its a positive acceleration aka just acceleration
        if accelerations[i] > 0:
            accn_weight = 50
            speed_weight = 50
            if accelerations[i] > accn_limit:
                accn_score = (1 - ((accelerations[i] - accn_limit)/accn_limit)) * 100
            else:
                accn_score = 100

        # if acceleration value is less than 0, its a deceleration
        if accelerations[i] < 0:
            # if no jerk, weights are given 50 each to accn score and speed limit score for a point
            accn_weight = 50
            speed_weight = 50
            if abs(accelerations[i]) > dccn_limit:
                accn_score = (1 - ((abs(accelerations[i]) - dccn_limit)/dccn_limit)) * 100
            else:
                accn_score = 100

        # Jerk score calculation
        jerk_limit = gh.zone_thresholds[segment_counter][zone_counter][JERK_LIMIT_REG]
        jerk_limits_positive.append(jerk_limit*CONV_FACTOR)
        jerk_limits_negative.append(-1*jerk_limit*CONV_FACTOR)
        if jerks[i] != 0:
            #if jerk present, weights are distributed 33% each
            jerk_weight = 33
            accn_weight = 34
            speed_weight = 33
            if abs(jerks[i]) > jerk_limit:
                jerk_score = (1 - ((abs(jerks[i]) - jerk_limit)/jerk_limit)) * 100
            else:
                jerk_score = 100

        # Final point calculation. print calls for debugging are commented if not needed.
        point_score = (speed_score * (speed_weight / 100)) + (accn_score * (accn_weight / 100)) + (jerk_score * (jerk_weight / 100))
        if DEBUG:
            print('speed = ' + str(speeds[i]) + ', accn = ' + str(accelerations[i]) + ', jerk = ' + str(jerks[i]))
            print('speed weight = ' + str(speed_weight) + ', accn weight = ' + str(accn_weight) + ', jerk weight = ' + str(jerk_weight))
            print('speed score = ' + str(speed_score) + ', accn score = ' + str(accn_score) + ', jerk score = ' + str(jerk_score))
            print('point score = ' + str(point_score))
            print(' ')

        segment_score += point_score * distance_intervals[i]
    # Segment score calculation
    segment_score = segment_score / total_segment_distance
    print('regular segment score = ' + str(segment_score))
    print(' ')

    # plot the graph for this segment
    if PLOT:
        plot_graphs(speeds,speed_limits,accelerations,accn_limits,dccn_limits,jerks,jerk_limits_positive,
                    jerk_limits_negative, segment_distances, segment_counter, LAP_NUM)

    if segment_score < 0:
        segment_score = 0.0
    return segment_score


def special_grading(speeds, accelerations, jerks, distance_intervals, segment_distances, total_segment_distance, segment_counter, LAP_NUM):
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

    # For Plotting purposes
    speed_limits = []
    accn_limits = []
    dccn_limits = []
    jerk_limits_positive = []
    jerk_limits_negative = []

    for i in range(num_values):
        speed_weight = 100
        accn_weight = 0
        jerk_weight = 0
        while segment_distances[i] >= gh.zone_limits[segment_counter][zone_counter][END_DIST]:
            zone_counter += 1
        # Speed score calculations
        speed_limit = gh.zone_thresholds[segment_counter][zone_counter][SPEED_LIMIT]
        speed_limits.append(speed_limit*CONV_FACTOR)
        if speeds[i] > speed_limit:
            speed_score = (1 - ((speeds[i] - speed_limit)/speed_limit)) * 100
        else:
            speed_score = 100
        # Accns score calculation
        accn_a = gh.zone_thresholds[segment_counter][zone_counter][EXP_ACCN_A]
        accn_b = gh.zone_thresholds[segment_counter][zone_counter][EXP_ACCN_B]
        dccn_a = gh.zone_thresholds[segment_counter][zone_counter][EXP_DCCN_A]
        dccn_b = gh.zone_thresholds[segment_counter][zone_counter][EXP_DCCN_B]
        accn_limit = get_exp_threshold(accn_a, accn_b, speeds[i])
        accn_limits.append(accn_limit*CONV_FACTOR)
        dccn_limit = get_exp_threshold(dccn_a, dccn_b, speeds[i])
        dccn_limits.append(dccn_limit*-1*CONV_FACTOR)
        if accelerations[i] > 0:
            accn_weight = 50
            speed_weight = 50
            if accelerations[i] > accn_limit:
                accn_score = (1 - ((accelerations[i] - accn_limit)/accn_limit)) * 100
            else:
                accn_score = 100
        if accelerations[i] < 0:
            accn_weight = 50
            speed_weight = 50
            if abs(accelerations[i]) > dccn_limit:
                accn_score = (1 - ((abs(accelerations[i]) - dccn_limit)/dccn_limit)) * 100
            else:
                accn_score = 100
        # Jerk score calculation
        jerk_limit = gh.zone_thresholds[segment_counter][zone_counter][JERK_LIMIT_SP]
        jerk_limits_positive.append(jerk_limit*CONV_FACTOR)
        jerk_limits_negative.append(-1*jerk_limit*CONV_FACTOR)
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

        if DEBUG:
            print('speed = ' + str(speeds[i]) + ', accn = ' + str(accelerations[i]) + ', jerk = ' + str(jerks[i]))
            print('speed weight = ' + str(speed_weight) + ', accn weight = ' + str(accn_weight) + ', jerk weight = ' + str(jerk_weight))
            print('speed score = ' + str(speed_score) + ', accn score = ' + str(accn_score) + ', jerk score = ' + str(jerk_score))
            print('point score = ' + str(point_score))
            print(' ')

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

    if PLOT:
        plot_graphs(speeds,speed_limits,accelerations,accn_limits,dccn_limits,jerks,jerk_limits_positive,
                    jerk_limits_negative, segment_distances, segment_counter, LAP_NUM)

    if segment_score < 0:
        segment_score = 0.0
    return segment_score
