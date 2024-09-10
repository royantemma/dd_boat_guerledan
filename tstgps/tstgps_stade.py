import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'drivers-ddboat-v2'))

import gps_driver_v2 as gpsdrv
gps = gpsdrv.GpsIO()
gps.set_filter_speed("0")

file = open ("data_stade.txt", "w")
cnt = 0
while True :
    gll_ok, gll_data = gps.read_gll_non_blocking()
    if gll_ok :
        cnt += 1
        txt = str(gll_data)+"\n"
        file.write(txt)
        if cnt == 200 :
            break

file.close()
