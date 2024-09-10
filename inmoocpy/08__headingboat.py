from roblib import *

def draw_boat(p,R,col,y,a):
    draw_boat3D(ax,p,R,col,1)
    draw_arrow3D(ax,*p,*(2*y),"magenta")
    draw_arrow3D(ax,*p,*(2*a),"black")


xmin,xmax,ymin,ymax,zmin,zmax=-10,10,-10,10,0,20
ax=axis3D(xmin,xmax,ymin,ymax,zmin,zmax)

a0=array([[0],[0],[1]])
I=1.15

y0=array([[cos(I)],[0],[-sin(I)]])
draw_boat([0,0,10],eye(3,3),'blue',y0,a0)

draw_axis3D(ax,0,0,0,2*eye(3,3))



pause(10)


