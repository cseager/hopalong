hopalong_plot.py
================

This program creates a gif animation of the hopalong attractor. 

Dependencies
------------

images2gif.py module found at 
http://code.google.com/p/visvis/source/browse/#hg/vvmovie

Further information on the hopalong algorithm: 
http://www.fraktalwelt.de/myhome/simpiter2.htm


Sample Output
-------------

Inputs
~~~~~~

Command line arguments: ::

    -f, --frames          integer, number of frames to save
    -cmap                 color map for the plot
    -a                    magnitude or range of a
    -b                    magnitude or range of b
    -c                    magnitude or range of c

Outputs
~~~~~~~

10 (or specified number of frames) png files titled hop000.png 
and one animated gif file titled hopalongs.gif


Sample output: ::

    $ python hopalong_plot.py -f 91

.. image:: https://raw.github.com/cseager/hopalong/master/example_output.gif
    :alt: example animated gif

The following example with args has 13 frames, holds ``a`` constant at -1.0, 
range of ``b`` from -1.9 to 0.0, range of ``c`` from 1.5 to 0.3, and uses the 
matplotlib color map ``winter``: ::

    $ python hopalong_plot.py -f 13 -a -1 -b -1.9 0 -c 1.5 .3 -cmap winter
    
.. image:: https://raw.github.com/cseager/hopalong/master/example2.gif
    :alt: example animated gif

