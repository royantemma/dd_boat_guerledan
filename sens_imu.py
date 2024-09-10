import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'drivers-ddboat-v2'))
import imu9_driver_v2 as imudrv
import time as time

print("ok")
imu = imudrv.Imu9IO()
xmax, ymax, zmax = imu.read_mag_raw()
xaccel, yaccel, zaccel = imu.read_accel_raw()
xgyro, ygyro, zgyro = imu.read_gyro_raw()


for i in range(50):
    xaccel, yaccel, zaccel = imu.read_accel_raw()
    print(xaccel, yaccel, zaccel)
    print("\n")
    time.sleep(1)

print("fini")
    
    
