from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py

def draw_wheel(R,I,wr,colorwheel="black"):
    clean3D(ax,-3,3,-3,3,-1,5)
    w=R@wr
    L=R@I@wr # angular momentum
    draw_arrow3D(ax,0,0,2,0.02*L[0,0],0.02*L[1,0],0.02*L[2,0],"red")
    draw_arrow3D(ax,0,0,2,0.1*w[0,0],0.1*w[1,0],0.1*w[2,0],"green") # spin vector
    l2,l3=sqrt(abs(I[2,2]-I30+0.1)),sqrt(abs((I[1,1]-I20+0.1)))
    M=tran3H(0,0,2)@ToH(R)@wheel3H(r)
    draw3H(ax,M,colorwheel,True,1)
    def draw_masses(l2,l3,col):
        p=array([[0],[0],[2]])+R@array([[0],[l2],[l3]])
        ax.scatter(*p,color=col)
    draw_masses(l2,0,'green')
    draw_masses(-l2,0,'green')
    draw_masses(0, l3,'black')
    draw_masses(0,-l3,'black')
    pause(0.001)

def f(x,u):
    w1,w2,w3,I2,I3=x[0,0],x[1,0],x[2,0],x[3,0],x[4,0]
    I1=I2+I3
    u1,u2=u[0,0],u[1,0]
    dw1=-((I3-I2)/I1)*w2*w3-w1*(u1+u2)/I1
    dw2=-w3*w1-w2*u1/I2
    dw3= w1*w2-w3*u2/I3
    dI2=u1
    dI3=u2
    return array([[dw1],[dw2],[dw3],[dI2],[dI3]])

ax=figure3D()
dt=0.002
r=1
m=10
R=eye(3)
w=array([[10],[4],[1]])
wr=R.T@w
I20,I30=1/4*m*r**2,1/4*m*r**2
x=array([[wr[0,0]],[wr[1,0]],[wr[2,0]],[I20],[I30]])

for t in arange(0,1,dt):
    I2,I3=x[3,0],x[4,0]
    I1=I2+I3
    I=diag([I1,I2,I3])
    wr=array([[x[0,0]],[x[1,0]],[x[2,0]]])
    draw_wheel(R,I,wr)
    u=array([[0],[0]])
    R=R@expw(dt*wr)
    x=x+dt*f(x+(dt/2)*f(x,u),u)


pause(100)