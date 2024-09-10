from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py

def f(X,u):
    θ=X[2,0]
    u=u.flatten()
    u1,u2=list(u[0:2])
    return array([[u1*cos(θ)], [u1*sin(θ)],[u2]])    
    
    

dt= 0.01

ax=init_figure(-0.3,0.3,-0.3,0.3)


X=array([[0],[0],[1]])
for t in arange(0,1,dt):
    draw_tank(X,'darkblue',0.005,1)       
    u=array([[1],[1]])
    X=X+dt*f(X,u)

pause(1)
 




