from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py
ax=figure3D()
pos = array([[0, 0, -5]]).T
R = eye(3, 3)
v = 0.1
α=0 #angles for the blade
u=array([[2],[0],[0],[0]]) 
dt=0.1
t=0          
w=1 
for t in arange(0,2,dt):
    clean3D(ax,-15,15,-15,15,-15,5)
    draw_riptide3D(ax, pos, R, u, α)
    α=α+dt*u[0,0]
pause(1)

