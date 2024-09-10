from sympy import sin, cos, Matrix, simplify,symbols,pi,hessian,lambdify

a1,a2,q1, q2,dq1,dq2,w1,w2,w3 = symbols("a1 a2 q1 q2 dq1 dq2 w1 w2 w3")
r1=(a1+a2*cos(q2))*cos(q1)
r2=(a1+a2*cos(q2))*sin(q1)
r3=-a2*sin(q2)
r = Matrix([r1, r2, r3])
q = Matrix([q1, q2])
J=r.jacobian(q)
print('J=',J)


from view3dlib import *

with open("car.obj", 'w') as F:    # visualize with https://3dviewer.net/
    draw_torus0(F,10,4,'green',1)
    draw_car(F, 0.4 * eye(3), array([[0],[0],[3]]), 'red')



