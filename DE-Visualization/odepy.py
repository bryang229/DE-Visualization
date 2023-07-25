import numpy as np
from odeintw import odeintw as ode
import matplotlib.pyplot as plt

g = .1  # Search || [0 - .9]
G = 1.0 # FIX
w = 1.0 # FIX 
W = .9  # Search || [.01 - 1]
r = .1  # Search || [0, .01, .05, ... 2]

def model(z, t, w,W,g,G,r):
        dYdt = np.array([( 1j*w - 1j*W - g + z[0] + z[2]) * z[0] + (g*G/2)
        ,(-1j*w - 1j*W - g - z[0] - z[2]) * z[1] + 2 * (z[1] + z[3]) * z[0] - z[4] - z[6]
        ,( 1j*w - 1j*W - g + z[0] + z[2]) * z[2]
        ,(-1j*w - 1j*W - g - z[0] - z[2]) * z[3] + 2 * (z[1] + z[3]) * z[2] - z[5] - z[7] - (g*G/2) * np.tanh(r) * np.exp(-2*g*t) * np.exp(-2j*W*t)
        ,(-2*g - 2j*W + z[0]) * z[4] + z[0] * z[6] + (g*G/2) * z[1]
        ,(-2*g - 2j*W + z[0]) * z[5] + z[0] + z[7] + (g*G/2) * np.tanh(r) * np.exp(-2*g*t -2j*W*t) * z[0]
        ,(-2*g - 2j*W + z[2]) * z[6] + z[2] * z[4] + (G*g/2) * z[3]
        ,(-2*g - 2j*W + z[2]) * z[7] + z[2] * z[5] + (g*G/2) * np.tanh(r) * np.exp(-2*g*t -2j*W*t) * z[2]])
       
        return dYdt

def genDiff(init_conds, tspan,func_i, params = [-1] * 5): 
    param = [.1, 1.0, 1.0, .9, .1]
    i = 0
    print('called')

    for para in params:
        if para != -1:
            param[i] = para 
        i += 1

    z = ode(model, init_conds, tspan, args = tuple(params))

    # plt.figure(1)

    # plt.scatter(z[:,func_i].real, z[:,func_i].imag)
    
    # fname = "research.png"
    
    # plt.savefig(fname = fname)
    # plt.clf()

    return z

def get_val(index, min, max, step):
    vals = np.linspace(min, max, step)
    return vals[index]