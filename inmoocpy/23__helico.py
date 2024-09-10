from roblib import *
ax=figure3D()


m,g,l=10,9.81,2
ω1,ω2=100,100
β1,β4=0.02,0.002
β2,β3=β1/10,β1/10
δ1=β1/5
B=array([[β1*ω1**2,0,0,0],[0,β2*ω1**2,0,0],[0,0,β3*ω1**2,0],[-δ1*ω1**2,0,0,-β4*l*ω2**2]])
I=array([[10,0,0],[0,20,0],[0,0,20]])
dt = 0.01

def draw_helico3D(ax,p,R,α,l):
    Ca1=hstack((circle3H(0.7*l),[[0.7*l,-0.7*l],[0,0],[0,0],[1,1]])) # the disc + the blade
    Ca2=hstack((circle3H(0.2*l),[[0.2*l,-0.2*l],[0,0],[0,0],[1,1]])) # the disc + the blades
    T = tran3H(p[0,0],p[1,0],p[2,0]) @ ToH(R)
    C1= T @ tran3H(0,0,-l/4) @eulerH(0,0,-α[0,0])@Ca1
    C2= T @ tran3H(-l,0,0)@eulerH(pi/2,0,0) @eulerH(0,0,α[1,0])@Ca2
    M = T @ add1(array([[-l,0,0],[0,0,0],[0,0,-l/4]]))
    draw3H(ax,M,'black',True,-1)  #body
    draw3H(ax, C2, 'green', True,-1)
    draw3H(ax, C1, 'blue', True, -1)
    pause(0.001)

def clock_helico(p,R,vr,wr,u):
    τ=B@u
    p=p+dt*R@vr
    vr=vr+dt*(-adjoint(wr)@vr+inv(R)@array([[0],[0],[g]])+array([[0],[0],[-τ[0,0]/m]]))
    R=R@expw(dt*wr)
    wr=wr+dt*(inv(I)@(-adjoint(wr)@I@wr+τ[1:4].reshape(3,1)))
    return p,R,vr,wr

    

p = array([[0],[0],[-10]])
R = eulermat(0.4,0.2,0.4)
vr = array([[13], [0], [0]])
wr = array([[0], [0], [0]])
α=array([[0,0]]).T
for t in arange(0,1,dt):
    clean3D(ax, -20, 20, -20, 20, 0, 40)
    u=array([[0.4],[0],[0],[0]])
    p, R, vr, wr = clock_helico(p, R, vr, wr, u)
    draw_helico3D(ax,p,R,α,5*l)
    α = α + dt * 30 * array([[ω1],[ω2]])
pause(10)






