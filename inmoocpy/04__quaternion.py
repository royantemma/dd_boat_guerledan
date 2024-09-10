from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py

φ,θ,ψ=1,2,3 
R=eulermat(φ,θ,ψ)
v,R1 = eig(R)
t=trace(R)
print("t=",t)  

