from gps3 import gps3
import time
import os

#Gps config
gpsd_socket = gps3.GPSDSocket()
data_stream = gps3.DataStream()
gpsd_socket.connect()
gpsd_socket.watch()

def dayofweek(d, m, y):
    t = [ 0, 3, 2, 5, 0, 3,
          5, 1, 4, 6, 2, 4 ]
    y -= m < 3
    return (( y + int(y / 4) - int(y / 100)+ int(y / 400) + t[m - 1] + d) % 7)

# Driver Code
#day = dayofweek(30, 8, 2010)
#print(day) 

days = {1:'Mon',2:'Tue',3:'Wed',4:'Thu',5:'Fri'}
flag = 1
while flag:

    for new_data in gpsd_socket:
        if new_data:
            data_stream.unpack(new_data)
            #logData = ',' + 'gps:' + str(data_stream.TPV['lat']) + ',' + str(data_stream.TPV['lon']) + ',' + str(data_stream.TPV['time'])
            date = str(data_stream.TPV['time'])
            if 'n/a' not in date:

             cal =date.strip().split('T')
             date = str(cal[0])
             time = str(cal[1].split('.')[0])
             #cal = date[0:10].strip().split("-")[1]
             yy = int(date[0:4])
             mm = int(date[5:7])
             dd = int(date[8:10])
             print(date,time)
             setCal = " sudo date --set=\'TZ=\"AmericaChicago\" "
             setCal += date + ' ' + time +'\''

             try:
              os.system(setCal)
              flag = 0
             except:
              print('cannot set time')
              flag = 1
             #print (setCal)
            # print(dayofweek(dd,mm,yy))
             break #for loop
            else:
             print('No fix')
             continue
