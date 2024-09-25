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

def verif_gps():
    cond = False
    while cond == False:
        gll_data = gps.read_gll()
        if gll_data[1] != "0.0":
            print("gps ok : départ")
            cond = True
    

def suivi_cap_fixe(a):
    global file
    verif_gps()
    offset = 150
    k=2
    cond = False
    psi_cap = 45
    while cond == False:
        #calcul vitesse des moteurs
        gll_ok, gll_data = gps.read_gll_non_blocking()
        if gll_ok :
            psi_cap, c = definir_cap(a, gll_data)
            cond = c
        # print("cap")
        # print(psi_cap)
        phi, theta, psi_chap = calib.angles_euler()
        psi_chap = psi_chap%360
        # print(psi_chap)
        delta = f_delta(psi_cap, psi_chap)
        #print("delta d", delta)
        if np.abs(delta)>30:
            k=4
            offset = 80
        else :
            offset = 200
        if delta >0:
            spdright = min(delta*k+ offset, 255)
            spdleft = offset
        else :
            spdright = offset
            spdleft = min(offset - delta*k, 255)
        # print("speed left", spdleft)
        # print("speed right", spdright)
        ard.send_arduino_cmd_motor(spdleft, spdright)
        time.sleep(0.1)

def suivi_cap_trajectoire():
    offset = 80
    k=2
    t_dep = temps()
    t = 0
    while t < t_dep + 180:
        t= temps()
        #calcul vitesse des moteurs
        psi_cap, vd = suivi_trajectoire()
        phi, theta, psi_chap = calib.angles_euler()
        psi_chap = psi_chap%360
        delta = f_delta(psi_cap, psi_chap)
        print("vd :", vd)
        offset = min(140, vd*100)
        if delta >0:
            spdright = min(delta*k+ offset, 255)
            spdleft = offset
        else :
            spdright = offset
            spdleft = min(offset - delta*k, 255)
        #print("spd right, spd left :", spdright, spdleft)
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
    
    

def definir_cap(a, gll_data):
    lat, lon = cvt_gll_ddmm_2_dd(gll_data)
    # print("LAT, LON")
    # print(lat, lon)
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
    print("norme :", norm_d)
    return psi_cap*180/np.pi, cond

def lissajou(t):
    return A*np.sin(2*(t-t0+delta_i)/T*2*np.pi)+a[0],  A*np.sin((t-t0+delta_i)/T*2*np.pi)+a[1]

def d_lissajou(t):
    return A*4*np.pi/T*np.cos(2*(t-t0+delta_i)/T*2*np.pi),  A*2*np.pi/T*np.cos((t-t0+delta_i)/T*2*np.pi)


def direction(pd, d_pd):
    gll_ok = False
    while not gll_ok :
        gll_ok, gll_data = gps.read_gll_non_blocking()
    lat, lon = cvt_gll_ddmm_2_dd(gll_data)
    txt = str(gll_data)+"\n"
    file.write(txt)

    #vecteur position p dans le plan
    p = spherique_a_plan(lat*np.pi/180, lon*np.pi/180)
    
    #erreur
    e=pd-p
    print("norme lissajou ", np.linalg.norm(e))
    
    #direction
    d = kv*(e/np.linalg.norm(e))*np.tanh(np.linalg.norm(e)/5) + d_pd
    
    return d
    
def temps():
    s = datetime.now()
    s=s.strftime("%Y%m%d_%H%M%S%f")
    h=int(s[9:11])
    m=int(s[11:13])
    sec=int(s[13:])*10e-7
    t=(h*60 +m)*60 +sec
    return t
		

def stop(t=0):
    ard.send_arduino_cmd_motor(0,0)
    time.sleep(t)

def depart():
    while True:
        a1 = calib.accel_corr()
        if a1[0] >= 8:
            break

def suivi_trajectoire():
    t = temps()
    pd = lissajou(t)
    d_pd = d_lissajou(t)
    d = direction(pd, d_pd)
    
    #calcul du cap désiré
    psi_cap = -np.arctan2(d[1], d[0])
    vd = np.linalg.norm(d)
    return psi_cap, vd

    
def mission_3(): 
    #depart()
    stop(2)
    #suivi_cap_fixe(a)
    #suivi_cap_trajectoire()
    suivi_cap_fixe(m)
    stop()

        
def mission_2(): 
    depart()
    stop(2)
    suivi_cap_fixe(a)
    #suivi_cap_fixe(m)
    stop()



if __name__ == "__main__":
    #initialisation gps
    lxm = 48.1991663*np.pi/180
    lym = -3.0146494*np.pi/180  #inversion de signe parce que z vers le haut
    lxa = 48.1995699*np.pi/180 #à modifier
    lya = -3.0153416*np.pi/180
    ro = 6347260
    m = np.array([0,0])
    a = spherique_a_plan(lxa, lya)


    #variables
    A=12 #amplitude
    t0= 12*3600 #à définir : temps initial
    T=210 #période
    N=15 #nombre de bateaux
    delta_i = T*8/N
    kv = 1 #coefficient pour la vitesse


    mission_3()
    stop()
    file.close()



    
