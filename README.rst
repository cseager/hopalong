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
    --cmax CMAX           max value of c
    --cmin CMIN           min value of c

Outputs
~~~~~~~

10 (or specified number of frames) png files titled hop000.png 
and one animated gif file titled hopalongs.gif


Sample output: ::

    $ python hopalong_plot.py -f 91

.. image:: https://raw.github.com/cseager/hopalong/master/example_output.gif
    :alt: example animated gif
