from view3dlib import * # https://www.ensta-bretagne.fr/jaulin/view3dlib.py

x1,x2,x3,x4=0,0,0,0
ax=init_figure(-40,50,-5,90)
draw_tank(array([[x1],[x2],[x3]]),'darkblue',0.6)

pause(1)

r=20
with open("car.obj", 'w') as F: # Visualisation on https://3dviewer.net/
    draw_axis(F,0.05,r+2)
    draw_sphere(F,r*eye(3),zeros((3,1)),'cyan',0.3)
    draw_car(F, eye(3), array([[0], [0], [r]]), 'red', 1)

