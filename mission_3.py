import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'drivers-ddboat-v2'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'mission_1'))
import arduino_driver_v2 as arddrv
import imu9_driver_v2 as imudrv
import calibration as calib
import gps_driver_v2 as gpsdrv
import time as time
import numpy as np
import mission_2 as m2
from datetime import datetime

#initialisation du bateau
if __name__ == "__main__":
    ard = arddrv.ArduinoIO()
    gps = gpsdrv.GpsIO()
    gps.set_filter_speed("0")
    now = datetime.now()
    filename = "log_"+ now.strftime("%Y%m%d_%H%M%S")+".txt"
    file = open (filename, "w")


def spherique_a_plan(lx, ly):
    lx = lx
    ly = ly
    return np.array([ro*np.cos(ly)*(lx-lxm), ro*(ly-lym)])

#initialisation gps
lxm = 48.1991663*np.pi/180
lym = -3.0146494*np.pi/180  #inversion de signe parce que z vers le haut
lxa = 48.1996872*np.pi/180 #à modifier
lya = -3.0153766*np.pi/180
ro = 6347260
m = np.array([0,0])
a = spherique_a_plan(lxa, lya)

def temps():
    s = datetime.now()
    s=s.strftime("%Y%m%d_%H%M%S%f")
    h=int(s[9:11])
    m=int(s[11:13])
    sec=int(s[13:])*10e-7
    t=(h*60 +m)*60 +sec
    return t

        

def cvt_gll_ddmm_2_dd (st):
    ilat = st[0]
    ilon = st[2]
    olat = float(int(ilat/100))
    olon = float(int(ilon/100))
    olat_mm = (ilat%100)/60
    olon_mm = (ilon%100)/60
    olat += olat_mm
    olon += olon_mm
    if st[3] == "W":
        olon = -olon
    return olat,olon
        
def f_delta(psi, psi_chap):
    lst = [np.abs(psi-psi_chap-360), np.abs(psi-psi_chap), np.abs(psi-psi_chap +360)]
    i = lst.index(min(lst))
    delta = psi - psi_chap +360*(i-1)
    return delta
    
    
def definir_cap(a):
    gll_ok = False
    while not gll_ok :
        gll_ok, gll_data = gps.read_gll_non_blocking()
    lat, lon = cvt_gll_ddmm_2_dd(gll_data)
    txt = str(gll_data)+"\n"
    file.write(txt)

    #vecteur position p dans le plan
    p = spherique_a_plan(lat*np.pi/180, lon*np.pi/180)
    
    #vecteur direction d
    d = a-p
    norm_d = np.linalg.norm(d)

    
    #calcul du cap désiré
    psi_cap = -np.arctan2(d[1], d[0])
    
    cond = norm_d <= 5
    return psi_cap*180/np.pi, cond
    
    
def stop(t=0):
    ard.send_arduino_cmd_motor(0,0)
    time.sleep(t)

def depart():
    while True:
        a1 = calib.accel_corr()
        if a1[0] >= 8:
            break









