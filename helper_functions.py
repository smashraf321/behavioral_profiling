import subprocess

# PIDs selector variables
ENGINE_COOLANT_TEMP = 0x05
ENGINE_RPM = 0x0C
VEHICLE_SPEED = 0x0D
MAF_SENSOR = 0x10
O2_VOLTAGE = 0x14
THROTTLE = 0x11

PID_REQUEST = 0x7DF
PID_REPLY = 0x7E8

# set GEOFencing bounds
DEPOT_LAT_NORTH = 42.02994532
DEPOT_LAT_SOUTH = 42.02994530
DEPOT_LONG_EAST = -93.65335383
DEPOT_LONG_WEST = -93.65335385

START_LAT_NORTH = 42.02994552
START_LAT_SOUTH = 42.02994550
START_LONG_EAST = -93.65335373
START_LONG_WEST = -93.65335375

STOP_LAT_NORTH = 42.02994562
STOP_LAT_SOUTH = 42.02994560
STOP_LONG_EAST = -93.65335393
STOP_LONG_WEST = -93.65335395

DIST_DEPOT = 1
DIST_DEPOT_MAX = 2.2
DIST_DEPOT_MIN = 2

DIST_START_MIN1 = 3.3
DIST_START_MAX1 = 3.4
DIST_START_MIN2REGL = 10.2
DIST_START_MAX2REGL = 10.3
DIST_START_MIN2CIRC = 25.2
DIST_START_MAX2CIRC = 25.3

DIST_STOP_MIN = 15.4
DIST_STOP_MAX = 15.5

# csv file properties
NUM_COLS = 7

def geo_fence_depot(lat,lon):
    return lat < DEPOT_LAT_NORTH and lat > DEPOT_LAT_SOUTH and lon < DEPOT_LONG_EAST and lon > DEPOT_LONG_WEST

def geo_fence_start(lat,lon,dist,spd,start_first_time,circulator):
    geofence =  lat < START_LAT_NORTH and lat > START_LAT_SOUTH and lon < START_LONG_EAST and lon > START_LONG_WEST
    if start_first_time:
        dist_check = dist > DIST_START_MIN1 and dist < DIST_START_MAX1 and spd == 0
    else:
        if circulator:
            dist_check = dist > DIST_START_MIN2CIRC and dist < DIST_START_MAX2CIRC and spd == 0
        else:
            dist_check = dist > DIST_START_MIN2REGL and dist < DIST_START_MAX2REGL and spd == 0
    return geofence or dist_check

def geo_fence_stop(lat,lon,dist,spd):
    geofence = lat < STOP_LAT_NORTH and lat > STOP_LAT_SOUTH and lon < STOP_LONG_EAST and lon > STOP_LONG_WEST
    dist_check = dist > DIST_STOP_MIN and dist < DIST_STOP_MAX and spd == 0
    return geofence or dist_check

def wifi_present():
    result = subprocess.check_output(
    'iwconfig 2>&1 | grep ESSID:off/any | wc -l',
    stderr = subprocess.STDOUT,
    shell = True)
    return int(result.strip())

def if_in_depot(lat,lon):
    return geo_fence_depot(lat,lon) or wifi_present()

def previous_distance(filename):
    # read from end of file
    f = open(filename,'rb')
    f.seek(-2,2)
    dis = 0
    comma_counter = 0
    while comma_counter != (NUM_COLS - 1):
        # for noting distance column value
        curr_char = 0
        while curr_char != b',':
            curr_char = f.read(1)
            if curr_char == b',':
                dis = f.readline()
            f.seek(-2,1)
        # for seeing current row has correct number of columns or not
        curr_char = 0
        comma_counter = 0
        while curr_char != b'\n':
            curr_char = f.read(1)
            if curr_char == b',':
                comma_counter += 1
            f.seek(-2,1)
    f.close()
    return float(dis)
