import numpy as np
from odeintw import odeintw as ode
import matplotlib.pyplot as plt

g = .1  # Search || [0 - .9]
G = 1.0 # FIX
w = 1.0 # FIX 
W = .9  # Search || [.01 - 1]
r = .1  # Search || [0, .01, .05, ... 2]

def model(z, t, w,W,g,G,r):
        gG2 = (g*G/2)
        tanr = np.tanh(r)        

        dYdt = np.array([( 1j*w - 1j*W - g + z[0] + z[2]) * z[0] + (gG2)
        ,(-1j*w - 1j*W - g - z[0] - z[2]) * z[1] + 2 * (z[1] + z[3]) * z[0] - z[4] - z[6]
        ,( 1j*w - 1j*W - g + z[0] + z[2]) * z[2]
        ,(-1j*w - 1j*W - g - z[0] - z[2]) * z[3] + 2 * (z[1] + z[3]) * z[2] - z[5] - z[7] - (gG2) * tanr * np.exp(-2*g*t) * np.exp(-2j*W*t)
        ,(-2*g - 2j*W + z[0]) * z[4] + z[0] * z[6] + (gG2) * z[1]
        ,(-2*g - 2j*W + z[0]) * z[5] + z[0] + z[7] + (gG2) * tanr * np.exp(-2*g*t -2j*W*t) * z[0]
        ,(-2*g - 2j*W + z[2]) * z[6] + z[2] * z[4] + (gG2) * z[3]
        ,(-2*g - 2j*W + z[2]) * z[7] + z[2] * z[5] + (gG2) * tanr * np.exp(-2*g*t -2j*W*t) * z[2]
        ,(-2*g + z[0]) * z[8] + z[0] * z[10] - (gG2) * tanr * np.exp(-2*g*t -2j*W*t) * z[1]
        ,(-2*g + z[2]) * z[9] + z[0] * z[11] - (gG2) * tanr * tanr * z[0]
        ,(-2*g + z[2]) * z[10] + z[2] * z[8] - (gG2) * tanr * np.exp(-2*g*t -2j*W*t) * z[3]
        ,(-2*g + z[2]) * z[11] + z[2] * z[9] - (gG2) * tanr * tanr * z[2]
        ,( 1j*w + 1j*W - g + z[0] + z[2]) * z[12] - (gG2)*tanr*np.exp(-2*g*t)*np.exp(2j*W*t)
        ,(-1j*w + 1j*W - g - z[0] - z[2]) * z[13] + 2 * (z[1] + z[3]) * z[12] - z[8] - z[10]
        ,( 1j*w + 1j*W - g - z[0] + z[2]) * z[14]
        ,(-1j*w + 1j*W - g - z[0] - z[2]) * z[15] + 2 * (z[1] + z[3]) * z[14] - z[9] - z[11] + gG2 * tanr * tanr
        ])
       
        return dYdt

def genDiff(init_conds, tspan, params = [-1] * 5): 
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

def genSessionId():
    sesStr = ""
    for i in range(1, 30):
        sesStr += str(np.random.randint(0, np.random.randint(10, 20 * i)))
    return sesStr

class CoefHolder:
    def __init__(self):
          self.userCookies = {}
    
    def updateCookieList(self, userCookie, z_list):
        self.userCookies[userCookie] = z_list
    
    def getUserCookieData(self, userCookie):
        if userCookie in self.userCookies:
            return self.userCookies[userCookie]
        return 0