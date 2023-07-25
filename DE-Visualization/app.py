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


app = Flask(__name__, static_folder = "/Users/bryang229/Desktop/ode site/Static")


W = 1
g = 1
r = 1

@app.route('/update', methods = ['POST'])
def update():
    g_ = request.form['g']
    W_ = request.form['W']
    r_ = request.form['r']
    
    if not g_:
        flash('g is needed')
    elif not W_:
        flash('W is needed')
    elif not r_:
        flash('r is needed')

    else:
        global g, W, r
        g = int(g_)
        W = int(W_)
        r = int(r_)


    return redirect('/')

@app.route('/')
@app.route('/matplot', methods = ['GET', "POST"])
def mpl():
    global g, W, r

    r_ = get_val(r, 0, 2, 100)
    g_ = get_val(g, .01, 1, 100)
    W_ = get_val(W, 0, .9, 100)

    return render_template('index.html', PageTitle = "Matplotlib",gv = g_, Wv = W_, rv = r_, g=g,W=W,r=r )

@app.route('/plot.png')
def plot_png():
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_figure():
    global r, g, W

    r_ = get_val(r, 0, 2, 100)
    g_ = get_val(g, .01, 1, 100)
    W_ = get_val(W, 0, .9, 100)

    fig, ax = plt.subplots(figsize=(6,4))
    fig.patch.set_facecolor('#E8E5DA')

    z = genDiff(np.array([0+0j] * 8), np.linspace(0,100,500), 0, [-1, W_, g_, -1, r_])

    ax.scatter(z[:,0].real, z[:,0].imag)
    plt.title("Plot of the first function of the first set of equations")

    return fig


if (__name__ == "__main__"):
    app.debug = True
    app.run(port = 2500)