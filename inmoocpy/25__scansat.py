from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py

def draw_sat(p, R, Rw):
    clear(ax)
    draw_disk(ax, array([[0], [0]]), 0.2, "blue", 1, 1)
    draw_tank(array([[p[0,0]],[p[1,0]],[logw(R)]]), 'darkblue',0.05)
    M = add1(0.2*array([[-1, 1, 0, 0 ,0 ],[0,  0, 0, 1,-1]]))
    plot2D(tran2H(p[0,0],p[1,0]) @ rot2H(logw(Rw)) @ M, 'red', 1)


ech=1.2
ax=init_figure(-ech,ech,-ech,ech)
p=array([[0],[1]])
R,Rw=eye(2,2),eye(2,2)

draw_sat(p,R,Rw)
pause(1)
