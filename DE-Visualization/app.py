from flask import render_template, Flask, request, url_for, redirect, Response, flash

import pandas as pd
import numpy as np
from odepy import genDiff, get_val
import matplotlib.pyplot as plt
import matplotlib 
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
matplotlib.use('Agg')

import io


app = Flask(__name__, static_folder = "/Users/bryang229/Desktop/DE-Visualization/DE-Visualization/Static")


W = 1
g = 1
r = 1
w = 99
G = 99
func_i = 0
tspan = [0, 100]
steps = 1000


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
        global g, W, r, w, G, func_i, tspan, steps
        g = int(g_)
        W = int(W_)
        r = int(r_)
        w = int(w_)
        G = int(G_)
        func_i = int(func_i_)
        steps_ = int(steps_)
        steps_ = 100 if steps_ < 100 else steps_
        steps_ = 10000 if steps_ > 10000 else steps_
        steps = steps_
        tspan = [float(tmin_), float(tmax_)]


    return redirect('/')

@app.route('/')
@app.route('/matplot', methods = ['GET', "POST"])
def mpl():
    global g, W, r, w, G, func_i, tspan, steps

    r_ = get_val(r, 0, 2, 100)
    g_ = get_val(g, .01, 1, 100)
    W_ = get_val(W, 0, .9, 100)
    w_ = get_val(w, 0, 1, 100)
    G_ = get_val(G, 0, 1,100)

    return render_template('index.html', PageTitle = "Matplotlib",gv = g_, Wv = W_, rv = r_, wv = w_, Gv=G_ , G=G, w=w,g=g,W=W,r=r, func_i=func_i, tmin=tspan[0], tmax=tspan[1], steps = steps)

@app.route('/plot.png')
def plot_png():
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_figure():
    global r, g, W, w, G, func_i, tspan, steps

    r_ = get_val(r, 0, 2, 100)
    g_ = get_val(g, .01, 1, 100)
    W_ = get_val(W, 0, .9, 100)
    w_ = get_val(w, 0, 1, 100)
    G_ = get_val(G, 0, 1,100)

    fig, ax = plt.subplots(figsize=(6,4))
    fig.patch.set_facecolor('#E8E5DA')

    z = genDiff(np.array([0+0j] * 8), np.linspace(tspan[0],tspan[1],steps), [w_, W_, g_, G_, r_])

    ax.scatter(z[:,func_i].real, z[:,func_i].imag, c= np.linspace(.1,1,len(z[:,func_i].real)))
    plt.title("Plot of the first function of the first set of equations")

    return fig


if (__name__ == "__main__"):
    app.debug = True
    app.run(port = 2500)