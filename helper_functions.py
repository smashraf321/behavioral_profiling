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

# coordinates collection
DEPOT_LAT_N = [42.019205,41.997700]
DEPOT_LAT_S = [42.018049,41.997229]
DEPOT_LON_E = [-93.624976,-93.631859]
DEPOT_LON_W = [-93.626312,-93.633290]

START_LAT_N = [42.018726,42.001011,42.000144]
START_LAT_S = [42.017320,42.000320,41.999589]
START_LON_E = [-93.637696,-93.633085,-93.632878]
START_LON_W = [-93.639789,-93.634071,-93.633463]

HOMEE = 0
ISU_ALUMNI_CENTER = 0
RESEARCH_PARK = 1
RP_STOP_SIGN = 1
RP_NEW_LINK_GENETICS = 2

# set GEOFencing bounds
DEPOT_LAT_NORTH = DEPOT_LAT_N[ RESEARCH_PARK ]
DEPOT_LAT_SOUTH = DEPOT_LAT_S[ RESEARCH_PARK ]
DEPOT_LONG_EAST = DEPOT_LON_E[ RESEARCH_PARK ]
DEPOT_LONG_WEST = DEPOT_LON_W[ RESEARCH_PARK ]

START_LAT_NORTH = START_LAT_N[ RP_NEW_LINK_GENETICS ]
START_LAT_SOUTH = START_LAT_S[ RP_NEW_LINK_GENETICS ]
START_LONG_EAST = START_LON_E[ RP_NEW_LINK_GENETICS ]
START_LONG_WEST = START_LON_W[ RP_NEW_LINK_GENETICS ]

# not useful now since we're working with laps
STOP_LAT_NORTH = 42.02994562
STOP_LAT_SOUTH = 42.02994560
STOP_LONG_EAST = -93.65335393
STOP_LONG_WEST = -93.65335395

# not useful ATM
DIST_DEPOT_EXIT = 20
DIST_DEPOT_RETURN = 20000

DIST_START_MIN1 = 170
DIST_START_MAX1 = 190
DIST_START_MIN2REGL = 10200
DIST_START_MAX2REGL = 10300
DIST_START_MIN2CIRC = 24900
DIST_START_MAX2CIRC = 25000

DIST_STOP_MIN = 15.4
DIST_STOP_MAX = 15.5

# csv file properties
NUM_COLS = 11

def geo_fence_depot(lat,lon,dist):
    geofence = lat < DEPOT_LAT_NORTH and lat > DEPOT_LAT_SOUTH and lon < DEPOT_LONG_EAST and lon > DEPOT_LONG_WEST
    dist_check = dist < DIST_DEPOT_EXIT or dist > DIST_DEPOT_RETURN
    return geofence or dist_check

def geo_fence_start(lat,lon,dist,spd,start_first_time,circulator):
    geofence =  lat < START_LAT_NORTH and lat > START_LAT_SOUTH and lon < START_LONG_EAST and lon > START_LONG_WEST
    if start_first_time:
        dist_check = dist > DIST_START_MIN1 and dist < DIST_START_MAX1
    else:
        if circulator:
            dist_check = dist > DIST_START_MIN2CIRC and dist < DIST_START_MAX2CIRC
        else:
            dist_check = dist > DIST_START_MIN2REGL and dist < DIST_START_MAX2REGL
    return (geofence or dist_check) and spd == 0

def geo_fence_stop(lat,lon,dist,spd):
    geofence = lat < STOP_LAT_NORTH and lat > STOP_LAT_SOUTH and lon < STOP_LONG_EAST and lon > STOP_LONG_WEST
    dist_check = dist > DIST_STOP_MIN and dist < DIST_STOP_MAX
    return (geofence or dist_check) and spd == 0

def wifi_present():
    result = subprocess.check_output(
    'iwconfig 2>&1 | grep ESSID:off/any | wc -l',
    stderr = subprocess.STDOUT,
    shell = True)
    return int(result.strip())

def if_in_depot(lat,lon,dist):
    return geo_fence_depot(lat,lon,dist) #or wifi_present() == 0

def if_bus_on_track():
    result = subprocess.check_output(
    'ls | grep current_file.txt | wc -l',
    stderr = subprocess.STDOUT,
    shell = True)
    return int(result.strip())

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
