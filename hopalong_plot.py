#!/usr/bin/python
# Filename: hopalong_plot.py

import os, sys
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable    
import PIL
import images2gif  #http://code.google.com/p/visvis/source/browse/#hg/vvmovie

NUMPOINTS = 10000 # number of points in each hopalong attractor plot frame
# this is for individual point colors in the charts
COLORS = np.linspace(0, 1, NUMPOINTS) 
axislim = [-10, 10] # boundaries of the chart

# hopalong attractor algorithm
# http://www.fraktalwelt.de/myhome/simpiter2.htm
def hopalong(a, b, c, n=1000):
    arr = np.zeros((n, 2))
    x, y = arr[0]
    for i in range(1, n):
        arr[i] = [y - np.sign(x) * pow((np.abs(b*x - c)), 0.5), a - x]
        x, y = arr[i]
    return [arr.T[0], arr.T[1]]
 

# dynamically set plot text labels showing a,b,c values
# all magic numbers specific to the layout of the chart below
def axtext(axX, abc, y, abcstr):
    if abc < 0.4: 
        axX.text(0.03 + abc, y, abcstr + " = " + str(abc))
    else:
        axX.text(abc - 0.035*len(str(abc)) - 0.15, y, str(abc) + " = " + abcstr)


# outputs a single frame of a hopalong animation to the current directory
def hopalong_iteration(a, b, c, i):
    p = hopalong(a, b, c, NUMPOINTS)
    fig, ax = plt.subplots()
    ax.scatter(p[0], p[1], c=COLORS, s=1, edgecolors='none')
    ax.set_xlim(axislim)
    ax.set_ylim(axislim)
    divider = make_axes_locatable(ax)
    axX = divider.append_axes("top", 0.5, 0.5, True)
    axX.scatter([a,b,c], [0,1,2], c='.75', s=5000, marker='|', linewidths=3)
    axX.set_xlim([-1, 1])
    axX.set_ylim([-0.8, 2.8])
    axtext(axX, a, -0.4, "a")
    axtext(axX, b, 0.6, "b")
    axtext(axX, c, 1.6, "c")
    plt.setp(axX.get_yticklabels(), visible=False)
    plt.setp(axX,yticks=[])
    name = 'hop' + ('%03d' % i) + '.png'
    fig.savefig(name)

def run_hopalong(argv):
	# number of frames in animation
	if len(argv) == 2:
		n = int(argv[1])
	else:
		n = 10

	# TODO: expand functionality to vary a and b as well
	# a, b, c are the parameters to vary the hopalong attractor graph in each frame
	# aa, bb, cc are arrays of floats between -1 and 1, one element for each frame
	aa, bb, cc = 0.5*np.ones(n), -0.6*np.ones(n), np.linspace(0, 0.9, n)

	# animated set of charts
	for i in range(n):
		hopalong_iteration(aa[i], bb[i], cc[i], i)

	f = sorted([i for i in os.listdir('.') if '.png' in i])
	images = [PIL.Image.open(i) for i in f]
	tofile = "hopalongs.gif"
	images2gif.writeGif(tofile, images, duration=.2)


if __name__ == '__main__':
	run_hopalong(sys.argv)

