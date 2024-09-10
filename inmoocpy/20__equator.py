from roblib import *    
ρE,dψE,dt = 10,0.2,0.05
p,R3 = array([[10],[0],[5]]), eulermat(pi/3,pi/3,pi/3)
ax=figure3D()
clean3D(ax,-1.5*ρE,1.5*ρE,-1.5*ρE,1.5*ρE,-ρE,ρE);     
draw_axis3D(ax,0,0,0,3*eye(3,3))
draw_earth3D(ax,ρE,eye(3,3),'gray')
draw_robot3D(ax,p,R3,'blue',0.3)   
pause(10)