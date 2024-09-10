import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'drivers-ddboat-v2'))
import imu9_driver_v2 as imudrv
import time as time
import numpy as np          

imu = imudrv.Imu9IO()
xmag, ymag, zmag = imu.read_mag_raw()
xaccel, yaccel, zaccel = imu.read_accel_raw()
xgyro, ygyro, zgyro = imu.read_gyro_raw()


def rotuv(u,v): #returns rotation with minimal angle  such that  v=R*u
    u=np.array(u).reshape(3,1)
    v=np.array(v).reshape(3,1)
    u=(1/np.linalg.norm(u))*u
    v=(1/np.linalg.norm(v))*v
    c=(u.T)@v
    A=v@u.T-u@v.T
    return np.eye(3,3)+A+(1/(1+c))*A@A


def calibration_mag ():
    print("Nord")
    time.sleep(6)
    print("allez chop chop")
    xmag, ymag, zmag = imu.read_mag_raw()
    xn = np.array([xmag, ymag, zmag])
    time.sleep(3)
    print("Sud à l'envers")
    time.sleep(6)
    print("allez chop chop")
    xmag, ymag, zmag = imu.read_mag_raw()
    xs = np.array([xmag, ymag, zmag])
    time.sleep(3)
    print("Ouest")
    time.sleep(6)
    print("allez chop chop")
    xmag, ymag, zmag = imu.read_mag_raw()
    xw = np.array([xmag, ymag, zmag])
    time.sleep(3)
    print("up, z au nord")
    time.sleep(6)
    print("allez chop chop")
    xmag, ymag, zmag = imu.read_mag_raw()
    xu = np.array([xmag, ymag, zmag])
    print("calcul en cours, féliciations, veuillez patienter <3")

    #calcul du biais
    b = -0.5*(xn+xs)

    #calcul de la matrice A
    beta = 46
    I = 64/360*2*np.pi
    Y = np.array([ [beta*np.cos(I), 0, -beta*np.sin(I)],
                 [0, -beta*np.cos(I), 0],
                 [-beta*np.sin(I), -beta*np.sin(I), beta*np.cos(I)]])
    X = np.array([xn+b, xw+b, xu+b]).T
    A = X@np.linalg.inv(Y)

    print("voilà c'était rapide")
    print(A, b.T)


def calibration_acc():
    print("x vers le haut")
    time.sleep(10)
    print("allez prends tes mesures loustic")
    xaccel, yaccel, zaccel = imu.read_accel_raw()
    xx = np.array([xaccel, yaccel, zaccel])
    time.sleep(1)
    print("y vers le haut")
    time.sleep(10)
    print("allez prends tes mesures loustic")
    xaccel, yaccel, zaccel = imu.read_accel_raw()
    xy = np.array([xaccel, yaccel, zaccel])
    time.sleep(1)
    print("z vers le haut")
    time.sleep(10)
    print("allez prends tes mesures loustic")
    xaccel, yaccel, zaccel = imu.read_accel_raw()
    xz = np.array([xaccel, yaccel, zaccel])
    time.sleep(1)
    print("z vers le bas")
    time.sleep(10)
    print("allez prends tes mesures loustic")
    xaccel, yaccel, zaccel = imu.read_accel_raw()
    xmz = np.array([xaccel, yaccel, zaccel])
    print("calcul des trucs bisous <3")

    
    #calcul du biais
    b = -0.5*(xz+xmz)

    #calcul de la matrice A
    beta = 9.81
    X = np.array([xx+b, xy+b, xz+b]).T
    A = 1/beta*X

    print("fini :)")
    print(A, b.T)


def angles_euler(A_acc, b_acc, A_mag, b_mag):
    xaccel, yaccel, zaccel = imu.read_accel_raw()
    xmag, ymag, zmag = imu.read_mag_raw()

    #accélération corrigée & normalisée
    X_acc = np.array([xaccel, yaccel, zaccel]).T
    a1 = np.linalg.inv(A_acc)@(X_acc + b_acc)
    a1 = a1/np.linalg.norm(a1)
    
    X_mag = np.array([xmag, ymag, zmag]).T
    y1 = np.linalg.inv(A_mag)@(X_mag + b_mag)
    y1 = y1/np.linalg.norm(y1)

    
    #calcul de l'angle de gîte
    v1 = np.array([0,1,0])
    phi_chap = np.arcsin(v1@a1)

    #calcul de l'assiette
    v2 = np.array([1,0,0])
    theta_chap = - np.arcsin(v2@a1)

    #calcul du cap
    v0 = np.array([0,0,1]).T
    R = rotuv(a1, v0)
    yh = R@y1
    psi_chap = -np.arctan2(yh[1], yh[0])

    return phi_chap*180/np.pi, theta_chap*180/np.pi, psi_chap*180/np.pi


def erreur(psi_d, psi_chap):
    return psi_d - psi_chap
    


def test_magnetisme():
    A_mag = np.array([[-67.46851739,  -2.206411,   -37.06675841],
 [  4.29870475, -50.41805237,   2.68919986],
 [-29.69015204,  -0.85771692,  64.91296854]] )
    b_mag = np.array([-2050.,   2037.5,  1185.5])

    xmag, ymag, zmag = imu.read_mag_raw()
    X_mag = np.array([xmag, ymag, zmag]).T
    y1 = np.linalg.inv(A_mag)@(X_mag + b_mag)
    print(np.linalg.inv(A_mag)@X_mag)
    print(b_mag)
    y1 = y1/np.linalg.norm(y1)
    print(y1*180/np.pi)

def test_accelero():
    A_acc = np.array([[-380.07135576, -103.41488277, -185.57594292],
 [  29.10295617, -393.93476045,   40.11213048],
 [-203.97553517,   76.04485219,  375.73904179]] )
    b_acc = np.array([-154.5,  -10.5,  -83. ])

    xaccel, yaccel, zaccel = imu.read_accel_raw()

    #accélération corrigée & normalisée
    X_acc = np.array([xaccel, yaccel, zaccel]).T
    a1 = np.linalg.inv(A_acc)@(X_acc + b_acc)
    a1 = a1/np.linalg.norm(a1)
    print(a1*9.81)


#valeurs des différentes matrices après calibration
A_acc = np.array([[-380.07135576, -103.41488277, -185.57594292],
 [  29.10295617, -393.93476045,   40.11213048],
 [-203.97553517,   76.04485219,  375.73904179]] )
b_acc = np.array([-154.5,  -10.5,  -83. ])
A_mag = np.array([[-67.46851739,  -2.206411,   -37.06675841],
 [  4.29870475, -50.41805237,   2.68919986],
 [-29.69015204,  -0.85771692,  64.91296854]] )
b_mag = np.array([-2050.,   2037.5,  1185.5])




#angles_euler(A_acc, b_acc, A_mag, b_mag)

