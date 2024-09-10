import numpy as np

def delta(psi, psi_chap):
    lst = [np.abs(psi-psi_chap-360), np.abs(psi-psi_chap), np.abs(psi-psi_chap +360)]
    i = lst.index(min(lst))
    delta = psi - psi_chap +360*(i-1)
    return delta



delta(180, -170)
delta(180, 170)
delta(0,10)
delta(360, 10)
delta(350, -10)
