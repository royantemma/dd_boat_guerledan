from view3dlib import * # https://www.ensta-bretagne.fr/jaulin/view3dlib.py

def f(x):
    x1,x2,x3=x.flatten()
    return array([[-x2*x3],[x1*x3],[-x2-0.5*x3]])


with open("pendule.obj", 'w') as F: # Visualisation on https://3dviewer.net/
    draw_axis(F,0.05,5)
    wmax,dw=6,0.3
    draw_cylinder(F,diag([1,1,wmax]),zeros((3,1)),'green',0.8)
    for θ in arange(0,2*pi,pi/10):
        for w in arange(-wmax,wmax,dw):
            x=expw(θ * array([[0], [0], [1]])) @ array([[1], [0], [w]])
            draw_arrow_pv(F, x, 0.3/(norm(f(x))+1)*f(x), 'red')

