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
        phi, theta, psi_chap = calib.angles_euler()
        psi_chap = psi_chap%360
        delta = f_delta(psi_cap, psi_chap)
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
        ard.send_arduino_cmd_motor(spdleft, spdright)
        time.sleep(0.1)


def definir_cap_2(a,b):
    #vecteur direction d
    d = b-a
    norm_d = np.linalg.norm(d)
    
    #calcul du cap désiré
    psi_cap = -np.arctan2(d[1], d[0])
    
    return psi_cap*180/np.pi


def suivi_waypoints(lst):
    verif_gps()
    for i in range(len(lst)-1):
        print("coords :",lst[i], lst[i+1])
        a, b, = lst[i], lst[i+1]
        psi_d = definir_cap_2(a, b)
        suivi_ligne(a, b, psi_d)
    

  

def suivi_ligne(a,b, psi_d):
    # print("psi d", psi_d)
    cond = True
    offset = 120
    psi_e = 0
    #k = np.pi/180*75
    if b[0] == sax:
        offset = 120
    t0 = time.time()    
    while cond :
        #calcul vitesse des moteurs
        gll_ok, gll_data = gps.read_gll_non_blocking()
        if gll_ok :
            psi_e, c = erreur(a, b,gll_data)
            cond = c
        phi, theta, psi_chap = calib.angles_euler()
        psi_chap = psi_chap%360

        #calcul nouvel angle désiré
        psi_cap = psi_d + 0.7*psi_e
        # print("erreur cap :",psi_e)
        # print("psi_chap :", psi_chap)
        delta = f_delta(psi_cap, psi_chap)
        
        if np.abs(delta)>30:
            k=3
        else :
            k=2
        
        if delta >0:
            spdright = min(offset + delta*k, 255)
            spdleft = max(0, offset - delta*k)
        else :
            spdleft = min(offset - delta*k, 255)
            spdright = max(0, offset + delta*k)
        ard.send_arduino_cmd_motor(spdleft, spdright)
        # if b[0] == sax*3:
        #     t = time.time()-t0
        #     cond = cond and (t<120)
        #     print("2min")
        while True:
            if (time.time()-t0)>0.1:
                break
        t0=time.time()
        
    stop_brusque()
        
        
def stop_brusque():
    ard.send_arduino_cmd_motor(-255, -255)
    time.sleep(2)
    stop()

def test_stop():
    ard.send_arduino_cmd_motor(190, 190)
    time.sleep(5)
    stop_brusque()
    
        
        
def erreur(a, b, gll_data):
    lat, lon = cvt_gll_ddmm_2_dd(gll_data)
    txt = str(gll_data)+"\n"
    file.write(txt)

    #vecteur position p dans le plan
    p = spherique_a_plan(lat*np.pi/180, lon*np.pi/180)
    # print("coordonnées gps p", lat, lon)
    # stop(20)
    n = (b-a)/np.linalg.norm(b-a)

    #calcul erreur
    e = n[0]*(p[1]-a[1]) - n[1]*(p[0]-a[0])
    print("distance au point :", np.linalg.norm(e))
    psi_e = 0.5*180*np.tanh(e/5)/np.pi

    cond = (np.linalg.norm(b-p)>5)
    return psi_e, cond
    
    

def suivi_cap_trajectoire():
    offset = 200
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
    print("position :", lat, lon)
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
    suivi_cap_fixe(a)
    suivi_cap_trajectoire()
    #suivi_cap_fixe(m)
    stop()

        
def mission_2(): 
    # depart()
    stop(2)
    suivi_cap_fixe(a)
    #suivi_cap_fixe(m)
    stop()



def mission_4():
    #depart()
    stop(2)
    lst = [m,amer, amer_b, amer_c, amer_b, amer,m, amer, amer_b, amer_c, amer_b, amer, m]
    #lst = [m, amer, m]
    suivi_waypoints(lst)
    stop()


    
def mission_5():
    suivi_waypoints([m, amer_b])
    stop()
    while True :
        t = temps()
        if t >(11*60 + 26)*60:
            break
   
    suivi_waypoints([amer_b, amer_c])
    stop()
    while True :
        t = temps()
        if t >(11*60 + 29)*60:
            break
    
    
    


def retour():
    #depart()
    stop()
    lst = [amer,m]
    suivi_waypoints(lst)
    stop()

    
if __name__ == "__main__":
    #initialisation gps
    lxm =48.19922833333*np.pi/180
    lym = -3.014735*np.pi/180  #inversion de signe parce que z vers le haut
    # lxm = 48.19922666666666*np.pi/180
    # lym = -3.0146383333333335*np.pi/180
    lxa = 48.1995699*np.pi/180 #à modifier
    lya = -3.0153416*np.pi/180
    # lxb = 48.2006278*np.pi/180
    # lyb = -3.0167036*np.pi/180
    # lxc = 48.20194444444*np.pi/180
    # lyc = -3.01472222222*np.pi/180
    lxc = 48.199984*np.pi/180
    lyc = -3.015493*np.pi/180
    lxb =48.200134*np.pi/180
    lyb = -3.015532*np.pi/180
    
    ro = 6347260
    m = np.array([0,0])
    amer = spherique_a_plan(lxa, lya)
    sax = amer[0]
    amer_b = spherique_a_plan(lxb, lyb)
    amer_c = spherique_a_plan(lxc, lyc)
    #variables
    A=12 #amplitude
    t0= 12*3600 #à définir : temps initial
    T=210 #période
    N=15 #nombre de bateaux
    delta_i = T*8/N
    kv = 1 #coefficient pour la vitesse

    #suivi_cap_fixe(m)
    #mission_4()

    #test_stop()
    #mission_5()
    #suivi_cap_fixe(amer)
    retour()
    stop_brusque()
    stop()
    file.close()



    
