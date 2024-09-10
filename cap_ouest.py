import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'drivers-ddboat-v2'))
import arduino_driver_v2 as arddrv
import imu9_driver_v2 as imudrv
import calibration as calib
import time as time
import numpy as np
ard = arddrv.ArduinoIO()

spdleft = 0
spdright = 0
ard.send_arduino_cmd_motor(spdleft, spdright) 
A_acc = np.array([[-380.07135576, -103.41488277, -185.57594292],
 [  29.10295617, -393.93476045,   40.11213048],
 [-203.97553517,   76.04485219,  375.73904179]] )
b_acc = np.array([-154.5,  -10.5,  -83. ])
A_mag = np.array([[-67.46851739,  -2.206411,   -37.06675841],
 [  4.29870475, -50.41805237,   2.68919986],
 [-29.69015204,  -0.85771692,  64.91296854]] )
b_mag = np.array([-2050.,   2037.5,  1185.5])




def suivi_cap(psi_cap, t):
    offset = 140
    k=1
    for i in range (t*2):
        phi, theta, psi_chap = calib.angles_euler(A_acc, b_acc, A_mag, b_mag)
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
        time.sleep(0.5)
        
        
def f_delta(psi, psi_chap):
    lst = [np.abs(psi-psi_chap-360), np.abs(psi-psi_chap), np.abs(psi-psi_chap +360)]
    i = lst.index(min(lst))
    delta = psi - psi_chap +360*(i-1)
    return delta


def stop(t=0):
    ard.send_arduino_cmd_motor(0,0)
    time.sleep(t)

def depart():
    imu = imudrv.Imu9IO()
    while True:
        xaccel, yaccel, zaccel = imu.read_accel_raw()
        X_acc = np.array([xaccel, yaccel, zaccel]).T
        a1 = np.linalg.inv(A_acc)@(X_acc + b_acc)
        if a1[0] >= 8:
            break
        time.sleep(0.5)
        
    
# depart()
# stop(2)
# suivi_cap(45, 30)
# stop(30)
# suivi_cap(-135, 30)
# stop()

suivi_cap(-135, 7)
