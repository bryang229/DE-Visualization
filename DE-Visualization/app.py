from flask import render_template, Flask, request, url_for, redirect, Response, flash

from http import cookies as Cookie
import pandas as pd
import numpy as np
from odepy import genDiff, get_val, genSessionId, CoefHolder
import matplotlib.pyplot as plt
import matplotlib 
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
matplotlib.use('Agg')

import io

app = Flask(__name__, static_folder = "/Users/bryang229/Desktop/DE-Visualization/DE-Visualization/Static")
userCookie = Cookie.SimpleCookie()
sessionId = genSessionId()

zHolder = CoefHolder()

userCookie['session'] = sessionId
# W = .1
# g = 1.0
# r = .01
# w = 1
# G = .1
# func_i = 0
# tspan = [0, 100]
# steps = 1000


userCookie['W'] = .1
userCookie['g'] = .01
userCookie['r'] = .01
userCookie['w'] = 1
userCookie['G'] = 1
userCookie['func_i'] = 0
userCookie['tmin'] = 0
userCookie['tmax'] = 100
userCookie['steps'] = 1000

def loadCookies():
    global userCookie
    temp = [float(userCookie['g'].value), float(userCookie['W'].value),
            float(userCookie['r'].value), float(userCookie['w'].value),
            float(userCookie['G'].value), int(userCookie['func_i'].value),
            int(userCookie['tmin'].value), int(userCookie['tmax'].value),
            int(userCookie['steps'].value)]
    return temp



@app.route('/update', methods = ['POST'])
def update():
    g_ = request.form['g']
    W_ = request.form['W']
    r_ = request.form['r']
    w_ = request.form['w']
    G_ = request.form['G']
    func_i_ = request.form['func_i']
    steps_ = request.form['trang']
    tmin_ = request.form['tmin']
    tmax_ = request.form['tmax']
    
    if not g_:
        flash('g is needed')
    elif not W_:
        flash('W is needed')
    elif not r_:
        flash('r is needed')
    elif not w_:
        flash('w is needed')
    elif not G_:
        flash('G is needed')
    elif not func_i_:
        flash("Function index needed")
    elif not steps_:
        flash("Please add time range")
    elif not tmin_:
        flash("Min time needed")
    elif not tmax_:
        flash("Max time needed")
    elif float(tmax_) < float(tmin_):
        flash('Make sure the max is greater than the min')
    else:
        
        global userCookie
        userCookie['g'] = float(g_)
        userCookie['W'] = float(W_)
        userCookie['r'] = float(r_)
        userCookie['w'] = float(w_)
        userCookie['G'] = float(G_)
        userCookie['func_i'] = int(func_i_)
        steps_ = int(steps_)
        steps_ = 100 if steps_ < 100 else steps_
        steps_ = 10000 if steps_ > 10000 else steps_
        userCookie['steps'] = steps_
        userCookie['tmin'] = int(tmin_)
        userCookie['tmax'] = int(tmax_)


    return redirect('/')

@app.route('/')
@app.route('/matplot', methods = ['GET', "POST"])
def mpl():
    g, W, r, w, G, func_i, tmin, tmax, steps = loadCookies()

    return render_template('index.html', PageTitle = "Matplotlib", G=G, w=w,g=g,W=W,r=r, func_i=func_i, tmin=tmin, tmax=tmax, steps = steps)

@app.route('/plot.png')
def plot_png():
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/plot_rt.png')
def plot_png_rt():
    fig = create_figure_rt()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/plot_it.png')
def plot_png_it():
    fig = create_figure_it()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_figure():
    g, W, r, w, G, func_i, tmin, tmax, steps = loadCookies()

    fig, ax = plt.subplots(nrows = 3, figsize=(6,6))
    fig.patch.set_facecolor('#E8E5DA')

    z = genDiff(np.array([0+0j] * 16), np.linspace(tmin,tmax,steps), [w, W, g, G, r])

    ax[0].scatter(z[:,func_i].real, z[:,func_i].imag, c= np.linspace(.1,1,len(z[:,func_i].real)))
    ax[0].set_title("Complex plane")
    ax[1].plot(np.linspace(tmin, tmax, steps), z[:,func_i].real)
    ax[1].set_title("Real vs time")
    ax[2].plot(np.linspace(tmin, tmax, steps), z[:,func_i].imag)
    ax[2].set_title("Imaginary vs time")
    fig.tight_layout(pad = 2.0)
    return fig


if (__name__ == "__main__"):
    app.debug = True
    app.run(port = 2500)

