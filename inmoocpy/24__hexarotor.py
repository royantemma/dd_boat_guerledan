from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py
ax=figure3D()
m,g,b,d,l=10,9.81,2,1,1
I=array([[10,0,0],[0,10,0],[0,0,20]])
dt = 0.05

def draw_hexarotor3D(ax,p,R,α,col):
    lz=5*l
    Ca=hstack((circle3H(0.3*lz),[[0.3*lz,-0.3*lz],[0,0],[0,0],[1,1]])) # the disc + the blades
    Ca=expwH([0,pi/2,0])@Ca
    T = tran3H(p[0,0],p[1,0],p[2,0]) @ ToH(R)
    for i in range(0,N):
        Ci = T @ tran3H(*(lz * Q[:,i])) @ ToH(rotuv([[1],[0],[0]],D[:,i])) @ eulerH(α[i,0],0,0)@Ca
        draw3H(ax, Ci, col[i], True, -1)
    M = T @ add1([[lz,-lz,0,0, 0],[0,0,0,lz,-lz],[0,0,0,0,0]])
    draw3H(ax,M,'grey',True,-1)

def draw_platform(ax,p,R):
    lz=5*l
    Ca=circle3H(0.3*lz)
    Ca=expwH([0,pi/2,0])@Ca
    T = tran3H(p[0,0],p[1,0],p[2,0]) @ ToH(R)
    for i in range(0,N-2):
        Ci = T @ tran3H(*(lz * Q[:, i])) @ ToH(rotuv([[1],[0],[0]],D[:,i])) @ Ca
        draw3H(ax, Ci, 'black', True, -1)
    M = T @ add1([[lz,-lz,-lz, lz,lz],[lz,lz,-lz,-lz,lz],[0,0,0,0,0]])
    draw3H(ax,M,'grey',True,-1)


def clock_hexa(p,R,vr,wr,f):
    return p,R,vr,wr


def pd(t):  return  array([[sin(0.3*t)], [cos(0.4*t)], [-10+0.1*sin(0.3*t)]])
def Rd(t):  return  expw([sin(t),cos(2*t),t])

Q=array([[0,-l, 0, l,l/2, 0],[l, 0,-l, 0,  0,l/2], [0, 0, 0, 0,  0, 0]])  #positions of the rotors, all blades have the same pitch
D=array([[1,0,0,0,1,0],[0,0,0,0,0,1],[0,1,1,1,0,0]])  #orientation of the forces
N=D.shape[1]


p = array([[10], [0], [-20]])  #x,y,z (front,right,down)
R = eulermat(0.2,0.3,0.4)
vr = array([[0], [0], [0]])
wr = array([[0], [0], [0]])
α=zeros((N,1))


for t in arange(0,10,dt):
    f = 0.1*array([[1],[1],[1],[1],[1],[1]])
    p, R, vr, wr = clock_hexa(p, R, vr, wr, f)
    clean3D(ax, -20, 20, -20, 20, 0, 25)
    draw_hexarotor3D(ax, p, R, α, ['green','black','red','blue','orange','brown'])
    draw_platform(ax, pd(t), Rd(t))
    α = α + dt * 30 * f
    pause(0.001)
pause(1)


