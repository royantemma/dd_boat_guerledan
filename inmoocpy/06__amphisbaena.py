
from roblib import *
ax=init_figure(-6,6,-6,6)

def draw_amphisbaena(θ):
    draw_tank([0,0,θ],'blue',0.5)
    draw_tank([0,0,pi+θ],'blue',0.5)

draw_amphisbaena(P)



pause(10)
