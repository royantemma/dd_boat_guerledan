from view3dlib import * # https://www.ensta-bretagne.fr/jaulin/view3dlib.py

with open("euler_field.obj", 'w') as F: # Visualisation on https://3dviewer.net/
    draw_sphere(F, eye(3), array([[0], [0], [0]]), 'green',0.7)
    draw_axis(F,0.05,5)


