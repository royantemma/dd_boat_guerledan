# MIT License

# Copyright (c) [2022] [Luc Jaulin]

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from roblib import * # https://www.ensta-bretagne.fr/jaulin/roblib.py
i=0

def draw_arrow_pv(f,p,v,col='blue'):  # p is the origin  of the vector v
    u = array([[1], [0], [0]])
    w=angle3d(u,v)
    A=(norm(v)/norm(u))*expw(w)
    draw_arrow(f, A, p, col, d=1)

def moveAc(A,c,x,y,z):
    return (c + A @ array([[x], [y], [z]])).flatten()

def draw_cube0(f,x1,x2,y1,y2,z1,z2,col,d=1) :
    draw_cube(f, eye(3), array([[0],[0],[0]]), x1, x2, y1, y2, z1, z2, col,d)

def move_write_v(F,A,c,x1,y1,z1):
    a1,a2,a3=moveAc(A,c,x1,y1,z1)
    F.write("v %.4f %.4f %.4f \n" % (a1,a2,a3))

def draw_cube(F,A,c,x1,x2,y1,y2,z1,z2,col,d=1) :
    draw_slab(F, A, c, x1, y1, z1, x1, y2, z1, x1, y2, z2, x1, y1, z2, col, d) #x1
    draw_slab(F, A, c, x2, y1, z1, x2, y2, z1, x2, y2, z2, x2, y1, z2, col, d) #x2
    draw_slab(F, A, c, x1, y1, z1, x2, y1, z1, x2, y1, z2, x1, y1, z2, col, d) #y1
    draw_slab(F, A, c, x1, y2, z1, x2, y2, z1, x2, y2, z2, x1, y2, z2, col, d) #y2
    draw_slab(F, A, c, x1, y1, z1, x2, y1, z1, x2, y2, z1, x1, y2, z1, col, d) #z1
    draw_slab(F, A, c, x1, y1, z2, x2, y1, z2, x2, y2, z2, x1, y2, z2, col, d) #z2

def draw_car(F,A,c,col,d=1) :
    y1,y2=-0.8,0.8
    x1,x2,x3,x4,x5=-1,0,1,1.5,3
    z1,z2,z3,z4=0,0.5,1,2
    draw_slab(F, A, c, x1, y1, z1, x2, y1, z4, x3, y1, z4, x4, y1, z3, col, d)
    draw_slab(F, A, c, x1, y1, z1, x4, y1, z3, x5, y1, z2, x5, y1, z1, col, d)
    draw_slab(F, A, c, x1, y2, z1, x2, y2, z4, x3, y2, z4, x4, y2, z3, col, d)
    draw_slab(F, A, c, x1, y2, z1, x4, y2, z3, x5, y2, z2, x5, y2, z1, col, d)
    draw_slab(F, A, c, x1, y1, z1, x1, y2, z1, x2, y2, z4, x2, y1, z4, col, d)
    draw_slab(F, A, c, x2, y1, z4, x2, y2, z4, x3, y2, z4, x3, y1, z4, col, d)
    draw_slab(F, A, c, x3, y1, z4, x3, y2, z4, x4, y2, z3, x4, y1, z3, 'blue', 0.5)
    draw_slab(F, A, c, x4, y1, z3, x4, y2, z3, x5, y2, z2, x5, y1, z2, col, d)
    draw_slab(F, A, c, x5, y1, z2, x5, y2, z2, x5, y2, z1, x5, y1, z1, col, d)


def setcolor(f,col,d=1):
    if col=='black':
        f.write("newmtl black \n")
        f.write("Kd 0.00000 0. 0. \n" )
        f.write("d %.4f \n" % (d))
        f.write("usemtl black \n")
    if col=='red':
        f.write("newmtl red \n")
        f.write("Kd 0.900000 0.1 0.1 \n" )
        f.write("d %.4f \n" % (d))
        f.write("usemtl red \n")
    if col=='orange':
        f.write("newmtl orange\n")
        f.write("Kd 1 0.5 0.0 \n" )
        f.write("d %.4f \n" % (d))
        f.write("usemtl orange\n")
    if col=='yellow':
        f.write("newmtl yellow\n")
        f.write("Kd 1 1 0.0 \n" )
        f.write("d %.4f \n" % (d))
        f.write("usemtl yellow\n")
    if col=='green':
        f.write("newmtl green \n")
        f.write("Kd 0.0 0.9 0.0 \n" )
        f.write("d %.4f \n" % (d))
        f.write("usemtl green \n")
    if col=='cyan':
        f.write("newmtl blue \n")
        f.write("Kd 0 1 1 \n" )
        f.write("d %.4f \n" % (d))
        f.write("usemtl blue \n")
    if col=='blue':
        f.write("newmtl blue \n")
        f.write("Kd 0 0 1 \n" )
        f.write("d %.4f \n" % (d))
        f.write("usemtl blue \n")
    if col=='bluetranslent':
        f.write("newmtl transluent\n")
        f.write("Kd 0 0.0 1.0 \n" )
        f.write("d %.4f \n" % (d))
        f.write("usemtl transluent\n")

def draw_slab0(f,x1, y1, z1, x2, y2, z2, x3, y3, z3, x4, y4, z4,col,d=1) :
    draw_slab(f, eye(3), array([[0],[0],[0]]), x1, y1, z1, x2, y2, z2, x3, y3, z3, x4, y4, z4, col,d)


def draw_slab(F,A,c,x1, y1, z1, x2, y2, z2, x3, y3, z3, x4, y4, z4,col,d=1.0) :
    draw_triangle(F,A,c,x1, y1, z1, x2, y2, z2, x3, y3, z3,col,d)
    draw_triangle(F,A,c,x1, y1, z1, x3, y3, z3, x4, y4, z4,col,d)

def draw_triangle(F,A,c,x1, y1, z1, x2, y2, z2, x3, y3, z3,color,d=1) :
    global i
    setcolor(F,color,d)
    move_write_v(F, A, c, x1, y1, z1)
    move_write_v(F, A, c, x2, y2, z2)
    move_write_v(F, A, c, x3, y3, z3)
    F.write("f %d %d %d \n" % (1+i,2+i,3+i))
    i=i+3


def draw_arrow0(F,col,d=1) :
    draw_arrow(F, eye(3), array([[0],[0],[0]]),col,1)

def draw_arrow(F,A,c,col,d=1) :
    F.write("# draw_arrow \n")
    e=0.02
    draw_cube(F,A,c, 0,1, 0,e,0,e, col,d)
    a=0.05
    draw_triangle(F,A,c, 1,  a, -a, 1,  a, a, 1+4*a, 0, 0,  col,d)
    draw_triangle(F,A,c, 1,  a, -a, 1, -a, -a, 1+4*a, 0, 0, col,d)
    draw_triangle(F,A,c, 1,  -a,  a, 1,  -a, -a, 1+4*a, 0, 0, col,d)
    draw_triangle(F,A,c, 1,  a,  a, 1,  -a,  a, 1+4*a, 0, 0, col,d)



def draw_axis(f,e=0.01,L=10) :
    f.write("# draw_axis \n")
    draw_arrow0(f, 'red')
    draw_arrow_pv(f,array([[0],[0],[0]]),array([[0],[1],[0]]), 'green')
    draw_arrow_pv(f, array([[0],[0],[0]]),array([[0],[0],[1]]), 'blue')
    draw_cube0(f, 0,L, 0,e,0,e, 'red')
    draw_cube0(f, 0,e, 0,L,0,e, 'green')
    draw_cube0(f, 0,e, 0,e,0,L, 'blue')


def draw_torus0(F,ra,rb,col,d=1) :
    draw_torus(F,eye(3),array([[0],[0],[0]]),ra,rb,col,d)

def draw_surface(F,f,A,c,amin,da,amax,bmin,db,bmax,col,d) :
    for a in arange(amin, amax, da):
        for b in arange(bmin, bmax, db):
            draw_slab0(F, *moveAc(A,c,*f(a,b)), *moveAc(A,c,*f(a+da,b)), *moveAc(A,c,*f(a+da,b+db)), *moveAc(A,c,*f(a,b+db)),col,d)

def draw_sphere(F,A,c,col,d) :
    def f(a, b): return latlong2cart(1,b,a).flatten()
    draw_surface(F, f, A, c, -pi/2, pi/20, pi/2, 0, pi/20, 2*pi, col, d)



def draw_torus(F,A,c,ra,rb,col,d) :
    def f(a,b):
        R=expw(a*array([[0], [0], [1]]))
        v=array([[ra+rb*cos(b)], [0], [rb*sin(b)]])
        return R@v.flatten()
    draw_surface(F,f,A,c,0,pi/20,2*pi,0,pi/20,2*pi,col,d)


def draw_cylinder0(F,col,d=1) :
    draw_cylinder(F,eye(3),zeros((3,1)),col,d)

def draw_cylinder(F,A,c,col,d) :
    def f(a,b):
        R=expw(a*array([[0], [0], [1]]))
        v=array([[1], [0], [b]])
        return R@v.flatten()
    draw_surface(F,f,A,c,0,pi/10,2*pi,-1,0.1,1,col,d)



if __name__ == "__main__":

    print('main program to test the view3Dlib.py')
    with open("test.obj", 'w') as F: # Visualisation on https://3dviewer.net/
        F.write("g traj\n")
        print('fini')
        #draw_cube0(F,1, 2, 3, 4, 5,6,"blue",1)
        '''
        dt = 0.1
        for t in arange(0, 5, dt):
            draw_cube0(F,3+sin(t), 3+sin(t) + 2 * dt, cos(t), cos(t) + 2 * dt, sin(2 * t), sin(2 * t) + 2 * dt,"blue")
            
        '''
        A=array([[1,0,0],[0,2,0],[0,0,0.5]])

        #draw_sphere(F, A, array([[0],[0],[0]]), 'green',0.8)
        #draw_cylinder(F,eye(3), array([[0],[2],[0]]), 'red', 0.5)
        draw_car(F, eye(3), array([[0],[0],[0]]),'red',1)
        draw_cube0(F,-30, 30, -30, 30, -10,-0.1,"cyan",1)
        #draw_torus0(F, 10, 1, 'green', 1)

        #draw_axis(F)


