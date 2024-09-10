from roblib import * # available at https://www.ensta-bretagne.fr/jaulin/roblib.py

def draw(R,wr):
    M=tran3H(0,0,3)@ToH(R)@diag([a,b,c,1])@tran3H(-0.5,-0.5,-0.5)@cube3H()
    M2=tran3H(0,0,3)@ToH(R)@diag([a,b,c,1])@tran3H(-0.5,-0.5,-0.5)@diag([1,0.01,1,1])@cube3H()
    w=R@wr
    draw_arrow3D(ax,0,0,3+a/2,*w,"magenta")
    draw_axis3D(ax,0,0,0,eye(3,3))
    draw3H(ax,M,'blue',True)
    draw3H(ax,M2,'red',True)

a,b,c,m=0.4,1,3,1
I=(m/12)*array([[b**2+c**2,0,0],[0,a**2+c**2,0],[0,0,a**2+b**2]])

ax=plt.figure().add_subplot(111,projection='3d')

wr=array([[0],[1],[0]])
R=eye(3)

clean3D(ax,-3,3,-3,3,0,6)
draw(R,wr)

pause(10)

