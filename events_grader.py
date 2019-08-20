#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 08:37:06 2019

@author: ashraf
"""
# for zones check segment distances

import pandas as pd
import grading_helpers as gh

START_DIST = 0
END_DIST = 1

def regular_grading(speeds, accelerations, jerks, distance_intervals, segment_distances, total_segment_distance):
    segment_score = 0.0
    num_values = len(speeds)

    for i in range(num_values):
        

    if segment_score < 0:
        segment_score = 0.0
    return segment_score

def special_grading(speeds, accelerations, jerks, distance_intervals, segment_distances, total_segment_distance, segment_counter):
    segment_score = 0.0

    if segment_score < 0:
        segment_score = 0.0
    return segment_score

"""
    The code below here is obsolete
"""

# ALPHA = 1
# BETA = 2
# #C_K = 3
# W_ACDC = 3
# W_SL = 4
# W_CS = 5
# W_H = 6
# STD_THRESH = 7
# W_STD = 8
# CSGL_THRESH = 9
# W_CSGL = 10

def accn_thresh_f(speed,ip_dist_counter):
    return (gh.ip_type[ip_dist_counter][ALPHA] * pow(speed, gh.ip_type[ip_dist_counter][BETA]))

def stop_grading(speeds, accns, dist_intervals, tot_dists, tot_event_dist, ip_dist_counter, speed_lim_counter, ip_stop_pos_counter):
    print('This is the function for grading a stop sign')
#    ---using pandas---
#    spds_n_dist = {'speeds':speeds,'accns':accns,'tot_dists':tot_dists}
#    spds_n_dist = pd.DataFrame(spds_n_dist)
#    spds_n_dist = spds_n_dist.loc[(spds_n_dist['tot_dists'] >= gh.ip_stop_positions[ip_stop_pos_counter][START_DIST]) & (spds_n_dist['tot_dists'] <= gh.ip_stop_positions[ip_stop_pos_counter][END_DIST])]
#    print(spds_n_dist)

    ip_score = 100
    num_values = len(speeds)

    delta_accn_dccn = 0
    accn_dccn_weight = gh.ip_type[ip_dist_counter][W_ACDC]
    accn_dccn_penalty = 0
    accn_thresh = 0

    delta_speed_limit = 0
    speed_limit_weight = gh.ip_type[ip_dist_counter][W_SL]
    speed_limit_penalty = 0

    min_speed = 100
    delta_full_stop = 0
    full_stop_weight = gh.ip_type[ip_dist_counter][W_CS]
    full_stop_penalty = 0

    delta_hesitation = 0
    NEGATIVE_ONGOING = False
    POSITIVE_ONGOING = False
    hesitation_weight = gh.ip_type[ip_dist_counter][W_H]
    hesitation_penalty = 0

    for i in range(num_values):
        #accn/dccn penalty check n calculation
        if speeds[i] == 0:
            accn_thresh = 9.8
        else:
            accn_thresh = accn_thresh_f(speeds[i],ip_dist_counter)
        if accns[i] > accn_thresh:
            delta_accn_dccn = abs(accns[i]) - accn_thresh
            accn_dccn_penalty += delta_accn_dccn * accn_dccn_weight
        #speed limit adherence check n calculation
        if tot_dists[i] >= gh.speed_limits[speed_lim_counter][START_DIST] and tot_dists[i] <= gh.speed_limits[speed_lim_counter][END_DIST]:
            if speeds[i] > gh.speed_limits[speed_lim_counter][SPEED_LIM]:
                delta_speed_limit = speeds[i] - gh.speed_limits[speed_lim_counter][SPEED_LIM]
                delta_speed_limit *= dist_intervals[i]
                speed_limit_penalty += delta_speed_limit
        elif tot_dists[i] > gh.speed_limits[speed_lim_counter][END_DIST]:
            speed_lim_counter += 1
            if speed_lim_counter == len(gh.speed_limits):
                speed_lim_counter -= 1
        else:
            pass
        #complete stop n hesitation
        if tot_dists[i] >= gh.ip_stop_positions[ip_stop_pos_counter][START_DIST] and tot_dists[i] <= gh.ip_stop_positions[ip_stop_pos_counter][END_DIST]:
            #complete stop check
            if speeds[i] < min_speed:
                min_speed = speeds[i]
            #hesitation check
            if accns[i] < 0.0:
                NEGATIVE_ONGOING = True
                POSITIVE_ONGOING = False
            elif accns[i] > 0.0 and NEGATIVE_ONGOING and not POSITIVE_ONGOING:
                delta_hesitation += 1
                POSITIVE_ONGOING = True
            else:
                pass

    #speed limit penalty calculation
    speed_limit_penalty = speed_limit_penalty * speed_limit_weight / tot_event_dist

    #complete stop penalty calculation
    if min_speed == 0:
        delta_full_stop = min_speed
    else:
        delta_full_stop = min_speed - 3
    full_stop_penalty = delta_full_stop * full_stop_weight

    #hesitation penalty calculation
    if delta_hesitation > 1:
        hesitation_penalty = (delta_hesitation - 1) * hesitation_weight

    ip_score -= full_stop_penalty + accn_dccn_penalty + speed_limit_penalty + hesitation_penalty

    print('Full Stop penalty = ' + str(full_stop_penalty) + ' Speed at Stop = ' + str(delta_full_stop))
    print('Acceleration/Deceleration penalty = ' + str(accn_dccn_penalty))
    print('Speed limit penalty = ' + str(speed_limit_penalty))
    if delta_hesitation == 0:
        print('Hesitation penalty = ' + str(hesitation_penalty) + ' You hesitated ' + str(delta_hesitation) + ' times')
    else:
        print('Hesitation penalty = ' + str(hesitation_penalty) + ' You hesitated ' + str(delta_hesitation - 1) + ' times')
    print('Stop sign score = ' + str(ip_score) + ' out of 100')
    print('')

    ip_stop_pos_counter += 1

    return_values = []
    return_values.append(ip_score)
    return_values.append(speed_lim_counter)
    return_values.append(ip_stop_pos_counter)
    return return_values


def signal_grading(speeds, accns, dist_intervals, tot_dists, tot_event_dist, ip_dist_counter, speed_lim_counter, ip_stop_pos_counter):
    print('This is the function for grading a signal')
    ip_score = 100
    num_values = len(speeds)

    delta_accn_dccn = 0
    accn_dccn_weight = gh.ip_type[ip_dist_counter][W_ACDC]
    accn_dccn_penalty = 0
    accn_thresh = 0

    delta_speed_limit = 0
    speed_limit_weight = gh.ip_type[ip_dist_counter][W_SL]
    speed_limit_penalty = 0

    delta_hesitation = 0
    NEGATIVE_ONGOING = False
    POSITIVE_ONGOING = False
    hesitation_weight = gh.ip_type[ip_dist_counter][W_H]
    hesitation_penalty = 0

    min_speed = 100
    delta_std_deviation = 0
    std_deviation_thresh = gh.ip_type[ip_dist_counter][STD_THRESH]
    std_deviation_weight = gh.ip_type[ip_dist_counter][W_STD]
    std_deviation_penalty = 0

    max_accn = 0
    accn_speed = 0
    accn_thresh = 0
    delta_catching_signal = 0
    catching_signal_threshold = gh.ip_type[ip_dist_counter][CSGL_THRESH]
    catching_signal_weight = gh.ip_type[ip_dist_counter][W_CSGL]
    catching_signal_penalty = 0

    for i in range(num_values):
        #accn/dccn penalty check n calculation
        if speeds[i] == 0:
            accn_thresh = 9.8
        else:
            accn_thresh = accn_thresh_f(speeds[i],ip_dist_counter)
        if accns[i] > accn_thresh:
            delta_accn_dccn = abs(accns[i]) - accn_thresh
            accn_dccn_penalty += delta_accn_dccn * accn_dccn_weight
        #speed limit adherence check n calculation
        if tot_dists[i] >= gh.speed_limits[speed_lim_counter][START_DIST] and tot_dists[i] <= gh.speed_limits[speed_lim_counter][END_DIST]:
            if speeds[i] > gh.speed_limits[speed_lim_counter][SPEED_LIM]:
                delta_speed_limit = speeds[i] - gh.speed_limits[speed_lim_counter][SPEED_LIM]
                delta_speed_limit *= dist_intervals[i]
                speed_limit_penalty += delta_speed_limit
        elif tot_dists[i] > gh.speed_limits[speed_lim_counter][END_DIST]:
            speed_lim_counter += 1
            if speed_lim_counter == len(gh.speed_limits):
                speed_lim_counter -= 1
        else:
            pass
        #catching signal eligibility calculation
        if tot_dists[i]<= gh.ip_stop_positions[ip_stop_pos_counter][END_DIST]:
            if accns[i] > max_accn:
                max_accn = accns[i]
                accn_speed = speeds[i]
        #hesitation check if at slow speeds
        if tot_dists[i] >= gh.ip_stop_positions[ip_stop_pos_counter][START_DIST] and tot_dists[i] <= gh.ip_stop_positions[ip_stop_pos_counter][END_DIST] and speeds[i] < 15 :
            if accns[i] < 0.0:
                NEGATIVE_ONGOING = True
                POSITIVE_ONGOING = False
            elif accns[i] > 0.0 and NEGATIVE_ONGOING and not POSITIVE_ONGOING:
                delta_hesitation += 1
                POSITIVE_ONGOING = True
            else:
                pass
        #standard deviation eligibilty calculation
        elif tot_dists[i] >= gh.ip_stop_positions[ip_stop_pos_counter][START_DIST] and tot_dists[i] <= gh.ip_stop_positions[ip_stop_pos_counter][END_DIST]:
            if speeds[i] < min_speed:
                min_speed = speeds[i]
        else:
            pass

    #speed limit penalty calculation
    speed_limit_penalty = speed_limit_penalty * speed_limit_weight / tot_event_dist

    #hesitation penalty calculation
    if delta_hesitation > 1 and delta_hesitation < 4:
        hesitation_penalty = (delta_hesitation - 1) * hesitation_weight

    #standard deviation eligibilty check
    if min_speed > 30:
        spds_n_dist = pd.DataFrame(speeds)
        if float(spds_n_dist.std()) > std_deviation_thresh:
            delta_std_deviation = float(spds_n_dist.std()) - std_deviation_thresh
        std_deviation_penalty = delta_std_deviation * std_deviation_weight

    #catching signal eligibility check
    if min_speed > 30 and accn_speed > 30:
        accn_thresh = accn_thresh_f(accn_speed,ip_dist_counter)
        if max_accn > accn_thresh + catching_signal_threshold:
            delta_catching_signal = max_accn - accn_thresh
        catching_signal_penalty = delta_catching_signal * catching_signal_weight

    ip_score -= accn_dccn_penalty + speed_limit_penalty + hesitation_penalty + std_deviation_penalty + catching_signal_penalty

    print('Acceleration/Deceleration penalty = ' + str(accn_dccn_penalty))
    print('Speed limit penalty = ' + str(speed_limit_penalty))
    if delta_hesitation == 0:
        print('Hesitation penalty = ' + str(hesitation_penalty) + ' You hesitated ' + str(delta_hesitation) + ' times')
    else:
        print('Hesitation penalty = ' + str(hesitation_penalty) + ' You hesitated ' + str(delta_hesitation - 1) + ' times')
    print('Standard deviation penalty = ' + str(std_deviation_penalty))
    print('Catching Signal penalty = ' + str(catching_signal_penalty))
    print('Signal score = ' + str(ip_score) + ' out of 100')
    print('')

    ip_stop_pos_counter += 1

    return_values = []
    return_values.append(ip_score)
    return_values.append(speed_lim_counter)
    return_values.append(ip_stop_pos_counter)
    return return_values

def straight_grading(speeds, accns, dist_intervals, tot_dists, tot_event_dist, ip_dist_counter, speed_lim_counter, ip_stop_pos_counter):
    print('This is the function for grading a straight stretch')
    ip_score = 100
    num_values = len(speeds)

    delta_accn_dccn = 0
    accn_dccn_weight = gh.ip_type[ip_dist_counter][W_ACDC]
    accn_dccn_penalty = 0
    accn_thresh = 0

    delta_speed_limit = 0
    speed_limit_weight = gh.ip_type[ip_dist_counter][W_SL]
    speed_limit_penalty = 0

    delta_std_deviation = 0
    std_deviation_thresh = gh.ip_type[ip_dist_counter][STD_THRESH]
    std_deviation_weight = gh.ip_type[ip_dist_counter][W_STD]
    std_deviation_penalty = 0

    for i in range(num_values):
        #accn/dccn penalty check n calculation
        if speeds[i] == 0:
            accn_thresh = 9.8
        else:
            accn_thresh = accn_thresh_f(speeds[i],ip_dist_counter)
        if accns[i] > accn_thresh:
            delta_accn_dccn = abs(accns[i]) - accn_thresh
            accn_dccn_penalty += delta_accn_dccn * accn_dccn_weight
        #speed limit adherence check n calculation
        if tot_dists[i] >= gh.speed_limits[speed_lim_counter][START_DIST] and tot_dists[i] <= gh.speed_limits[speed_lim_counter][END_DIST]:
            if speeds[i] > gh.speed_limits[speed_lim_counter][SPEED_LIM]:
                delta_speed_limit = speeds[i] - gh.speed_limits[speed_lim_counter][SPEED_LIM]
                delta_speed_limit *= dist_intervals[i]
                speed_limit_penalty += delta_speed_limit
        elif tot_dists[i] > gh.speed_limits[speed_lim_counter][END_DIST]:
            speed_lim_counter += 1
            if speed_lim_counter == len(gh.speed_limits):
                speed_lim_counter -= 1
        else:
            pass

    #calculating standard deviation penalty
    #---using pandas---
    spds_n_dist = pd.DataFrame(speeds)
    if float(spds_n_dist.std()) > std_deviation_thresh:
        delta_std_deviation = float(spds_n_dist.std()) - std_deviation_thresh
    std_deviation_penalty = delta_std_deviation * std_deviation_weight

    #speed limit penalty calculation
    speed_limit_penalty = speed_limit_penalty * speed_limit_weight / tot_event_dist

    ip_score -= accn_dccn_penalty + speed_limit_penalty + std_deviation_penalty

    print('Acceleration/Deceleration penalty = ' + str(accn_dccn_penalty))
    print('Speed limit penalty = ' + str(speed_limit_penalty))
    print('Standard deviation penalty = ' + str(std_deviation_penalty))
    print('Straight score = ' + str(ip_score) + ' out of 100')
    print('')
    return_values = []
    return_values.append(ip_score)
    return_values.append(speed_lim_counter)
    return_values.append(ip_stop_pos_counter)
    return return_values
