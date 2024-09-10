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
from datetime import datetime

#initialisation du bateau
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
lxa = 48.1996457*np.pi/180 #à modifier
lya = -3.0152944*np.pi/180
ro = 6347260
m = np.array([0,0])
a = spherique_a_plan(lxa, lya)

def suivi_cap(a):
    global file
    offset = 140
    k=1
    cond = False
    while cond == False:
        #calcul vitesse des moteurs
        psi_cap, c = definir_cap(a)
        cond = c
        phi, theta, psi_chap = calib.angles_euler()
        psi_chap = psi_chap%360 
        delta = f_delta(psi_cap, psi_chap)
        if np.abs(delta)>45:
            offset = 20
        else :
            offset = 140
        if delta >0:
            spdright = min(delta*k+ offset, 255)
            spdleft = offset
        else :
            spdright = offset
            spdleft = min(offset - delta*k, 255)
        
        ard.send_arduino_cmd_motor(spdleft, spdright)
        

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
        
        
def mission_2(): 
    depart()
    stop(2)
    suivi_cap(a)
    suivi_cap(m)
    stop()


mission_2()
    

file.close()
