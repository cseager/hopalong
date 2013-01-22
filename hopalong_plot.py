#!/usr/bin/python
# Filename: hopalong_plot.py

import os, sys
import argparse
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable    
import PIL
import images2gif  #http://code.google.com/p/visvis/source/browse/#hg/vvmovie

NUMPOINTS = 10000 # number of points in each hopalong attractor plot frame
axislim = [-10, 10] # boundaries of the chart


class Hopalong():
    def __init__(self, aa, bb, cc, frames):
        self.abc = zip(aa, bb, cc)
        self.frames = frames
        self.min = np.min(self.abc)
        self.max = np.max(self.abc)
        self.set_cmap()
        self.set_axisbg()
        
    def set_cmap(self, cmap='jet'):
        self.COLORS = plt.get_cmap(cmap)(np.linspace(0, 1, NUMPOINTS))
    
    def set_axisbg(self, axisbg='white'):
        self.axisbg = axisbg

    # hopalong attractor algorithm
    # http://www.fraktalwelt.de/myhome/simpiter2.htm
    def get_points(self, i, num_points):
        a, b, c = self.abc[i]
        points = np.zeros((num_points, 2))
        x, y = points[0]
        for i in range(1, num_points):
            points[i] = [y - np.sign(x) * pow((np.abs(b*x - c)), 0.5), a - x]
            x, y = points[i]
        return [points.T[0], points.T[1]]
 
    # dynamically set plot text labels showing a,b,c values
    # all magic numbers specific to the layout of the chart below
    def axtext(self, axX, x, y, label):
        scale_range = self.max - self.min + 0.2
        char_width = 0.0175 * scale_range
        flip_threshold = self.max - char_width * 18
        if x < flip_threshold: 
            # put the label on the right of the bar
            location = char_width + x
            text = label + " = " + str(x)
        else:
            # put the label left of the bar so it doesn't go outside the chart
            location = x - char_width*(len(str(x)) + 3)
            text = str(x) + " = " + label
        axX.text(location, y, text)

      
    # outputs a single frame of a hopalong animation to the current directory
    def get_plot(self, i):
        points = self.get_points(i, NUMPOINTS)
        a, b, c = self.abc[i]
        fig = plt.figure()
        ax = fig.add_subplot(111, axisbg=self.axisbg)
        ax.scatter(points[0], points[1], c=self.COLORS, s=1, edgecolors='none')
        ax.set_xlim(axislim)
        ax.set_ylim(axislim)
        divider = make_axes_locatable(ax)
        axX = divider.append_axes("top", 0.5, 0.5, True)
        axX.scatter([a,b,c], [0,1,2], c='.75', s=5000, marker='|', linewidths=3)
        axX.set_xlim([self.min - 0.1, self.max + 0.1])
        axX.set_ylim([-0.8, 2.8])
        self.axtext(axX, a, -0.4, "a")
        self.axtext(axX, b, 0.6, "b")
        self.axtext(axX, c, 1.6, "c")
        plt.setp(axX.get_yticklabels(), visible=False)
        plt.setp(axX,yticks=[])
        return fig
        


# assign min and max of a, b, c from the parsed arguments list
# it's fine if min > max, it will just change the order of the final gif 
def get_range(parameter, default):
    try:
        pmin = parameter[0][0]
        if len(parameter[0]) > 1:
            pmax = parameter[0][1]
        else: 
            pmax = pmin
    except: 
        pmin, pmax = default
    return pmin, pmax


def run_hopalong(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--frames", dest='frames', 
                        type=int, default=10,
                        help="number of frames to save")
    parser.add_argument("-cmap", dest='cmap', default='Paired',
                        help="color map for the plot")
    parser.add_argument("-axisbg", default="black", help="background color for the plot")

    # TODO: change this group to arguments that can take 1-2 values.
    #       write custom action class to implement logic. 
    #       currently more than 2 arguments are ignored. 
    #       see http://docs.python.org/2/library/argparse.html#action
    parser.add_argument("-a", dest='a', type=float, nargs='+', action='append',
                        help="magnitude or range of a")
    parser.add_argument("-b", dest='b', type=float, nargs='+', action='append',
                        help="magnitude or range of b")
    parser.add_argument("-c", dest='c', type=float, nargs='+', action='append',
                        help="magnitude or range of c")


    args = parser.parse_args()

    # number of frames in animation
    frames = args.frames
   
    # default values provided here 
    amin, amax = get_range(args.a, (0.5, 0.5))
    bmin, bmax = get_range(args.b, (-0.6, -0.6))
    cmin, cmax = get_range(args.c, (0.0, 0.9))

    # a, b, c are the parameters to vary the hopalong attractor graph in each frame
    # aa, bb, cc are arrays of floats between -1 and 1, one element for each frame
    aa = np.linspace(amin, amax, frames)
    bb = np.linspace(bmin, bmax, frames)
    cc = np.linspace(cmin, cmax, frames)
    
    hopalong_orbit = Hopalong(aa, bb, cc, frames)
    hopalong_orbit.set_cmap(args.cmap)
    hopalong_orbit.set_axisbg(args.axisbg)

    # save the frames in the current directory
    for i in range(frames):
        fig = hopalong_orbit.get_plot(i)
        name = 'hop' + ('%03d' % i) + '.png'
        fig.savefig(name)
        
    # convert the png frames into animated gif
    f = sorted([i for i in os.listdir('.') if '.png' in i])
    images = [PIL.Image.open(i) for i in f]
    tofile = "hopalongs.gif"
    rate = 15.0 / frames
    rate = .2 if rate < .2 else rate
    images2gif.writeGif(tofile, images, duration=rate)


if __name__ == '__main__':
    run_hopalong(sys.argv)

