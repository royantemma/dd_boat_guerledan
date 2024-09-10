from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py
             
     
ax=axis3D(-20,20,-20,20,0,40)
x = array([[0,0,5,15,0,1,0]]).T
u = array([[0,0,0.1]]).T
dt = 0.05
draw_robot3D(ax,x[0:3],eulermat(*x[4:7,0]),'blue',1)
draw_arrow3D(ax,2,2,1,2,2,2,"red")
draw_axis3D(ax,0,0,0,5*eye(3,3))
pause(5)

 
  
