import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'drivers-ddboat-v2'))
import arduino_driver_v2 as arddrv
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

def suivi_cap():
    psi_cap = 90
    for i in range (360):
        phi, theta, psi_chap = calib.angles_euler(A_acc, b_acc, A_mag, b_mag)
        delta = psi_cap-psi_chap
        print(psi_chap)
        if delta >0:
            spdright = delta+ 80
            spdleft = 80
        else :
            spdright = 80
            spdleft = 80-delta
        
        ard.send_arduino_cmd_motor(spdleft, spdright)
        time.sleep(0.5)
        
        
suivi_cap()
