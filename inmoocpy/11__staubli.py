from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py 
ax=figure3D()
 
def draw():
    clean3D(ax,-2,2,-2,2,0,2)
    J = array([[0, 1, 0, 0, 0] , [0, 0, 1, 0,0] , [0, 0, 0, 1,0] , [1, 1, 1, 1,1]])
    plot3D(ax,J,"black",2)
    pause(0.01)
        
        
draw()    
pause(1)
        
