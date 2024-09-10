from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py

def f(x):
    x=x.flatten()
    return (array([[1],[0],[2],[0] ]))

        
r=10
g = 9.81
dt=0.005;
x=array([[r],[0],[0],[0]])


ech=5
ax=init_figure(r-ech,r+ech,-ech,ech)
clear(ax)
draw_disk(ax,array([[0],[0]]),r,"grey")
for t in arange(0,1,dt) :
    x=x+dt*(0.25*f(x)+0.75*(f(x+dt*(2/3)*f(x)))) # Runge Kutta
    draw_disk(ax,array([[x[0,0]],[x[2,0]]]),0.04,"red")
pause(1)
