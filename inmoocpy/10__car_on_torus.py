from view3dlib import *

def draw_pose(x1,x2,x3):
    R1 = expm(x1 * adjoint(array([[0], [0], [1]])))
    R2 = expm(x2 * adjoint(array([[0], [1], [0]])))
    R3 = expm(x3 * adjoint(array([[1], [0], [0]])))
    r3 = r1 + r2 * cos(x2)
    v = array([[r3], [0], [r2 * sin(-x2)]])
    R=R1@R2@R3@ expm((pi/2)*adjoint(array([0,0,1])))@ expm((pi/2)*adjoint(array([1,0,0])))
    draw_car(F, 0.4 * R, R1@v, 'red', 1)

kmax,dt=1000,0.1
r1,r2=10,6
with open("car.obj", 'w') as F:
    draw_axis(F,0.05,r1+2)
    draw_torus0(F,r1,r2,'green',1)
    draw_pose(0, 0, 0)



