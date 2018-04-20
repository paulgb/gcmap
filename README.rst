Great Circle Maps for Python
============================

This is a Python rewrite of the code used to create the `Visualizing Facebook Friends <http://fbmap.bitaesthetics.com/>`__ visualization in 2010.

The original code was written in R and was built specifically around the Facebook dataset. This rewrite is as a Python module and is built to work on top of any dataset.

If you are looking to visualize a few (<10,000) coordinate pairs, `matplotlib <http://matplotlib.org/>`__ with `basemap <http://matplotlib.org/basemap/>`__ will be more flexible. The visualization
implemented by this module is useful when the data alone are sufficient to show the geography.

The algorithm uses a heuristic which attempts to visualize the *structure* of the pairs rather than their relative importance. In interpreting the results, you should not come to any conclusions about the relative importance of different coordinate pairs.

The `OpenFlights dataset <http://openflights.org/data.html>`__ visualized with ``gcmap`` (`source code <http://nbviewer.ipython.org/5851489>`__):

.. image:: https://raw.github.com/paulgb/gcmap/master/example.png

Installation
------------

Install ``gcmap`` using ``pip``::

    # pip install gcmap

Usage
-----

The module supplies two classes, ``GCMapper`` and ``Gradient``. ``GCMapper`` is the main class for rendering great-circle maps. ``Gradient`` is used when you would like to customize the color gradient
used to render the map.

``GCmapper``
------------

First, import GCMapper and instantiate it::

    >>> from gcmap import GCMapper
    >>> gcm = GCMapper()

The ``GCMapper()`` constructor can take a number of arguments:

* ``width`` the height of the output image
* ``height`` the width of the output image; defaults to half the width, which fits the world completely for the default projection (equidistant cylindrical)
* ``bgcol`` the background color as an (r, g, b) triple, eg. (255, 0, 0) for red
* ``cols`` a ``Gradient`` object or other function from a fraction an (r, g, b) triple
* ``proj`` the projection to use as a string, passed to pyproj. See `pyproj <http://pyproj.googlecode.com/svn/trunk/docs/pyproj-pysrc.html>`__ for a list of projections
* ``line_width`` the width of the lines draw, in pixels
* ``gc_resolution`` the number of straight line segments used to approximate each great-circle curve

Normally you would load the coordinate pairs from a file. For this example I'll simply code in the
data::

    >>> lons1 = [-79.4, -73.9, -122.4, -123.1, -0.1  ]
    >>> lats1 = [ 43.7,  40.7,   37.8,   49.2,  51.5 ]
    >>> lons2 = lons1[1:] + lons1[:1]    # this creates a cycle through the points
    >>> lats2 = lats1[1:] + lats1[:1]

The data can also be a numpy array.

Then, give the data to the ``GCMapper`` instance::

    >>> gcm.set_data(lons1, lats1, lons2, lats2)

Now, we can generate the image::

    >>> img = gcm.draw()

``img`` is just a Python Image Library Image object, which we can save in any supported
format::

    >>> img.save('output.png')

``Gradient``
------------

Gradients are instantiated with one parameter, a list of two or more gradient "stops". Stops
are RGB colors located at a fractional position along the gradient. The color at any point
on the gradient is a weighted blend of the stops nearest to that point in either direction.

For example, let's define a gradient from white to red to black::

    >>> from gcmap import Gradient
    >>> #             (stop,   red, green,  blue)
    >>> g = Gradient([(   0,   255,   255,   255),
    ...               ( 0.4,   255,     0,     0),
    ...               (   1,     0,     0,     0)])

Note that red the stop is at 0.4, or four tenths of the gradient.

The gradient ``g`` now acts as a function when it is called. When it is called with a
stop which was explicitly specified at construction, it returns the (r, g, b) triple
at that stop::

    >>> g(0)
    (255, 255, 255)
    >>> g(0.4)
    (255, 0, 0)
    >>> g(1)
    (0, 0, 0)

When ``g`` is called with fractions that are not stops, it blends the nearest stops in
either direction to create a new color::

    >>> g(0.1)
    (255, 191, 191)
    >>> g(0.2)
    (255, 127, 127)
    >>> g(0.3)
    (255, 63, 63)
    >>> g(0.5)
    (212, 0, 0)
    >>> g(0.6)
    (170, 0, 0)
    >>> g(0.7)
    (127, 0, 0)
    >>> g(0.8)
    (84, 0, 0)
    >>> g(0.9)
    (42, 0, 0)

License
-------
`zlib-style <http://www.gzip.org/zlib/zlib_license.html>`__ as follows:

Copyright (C) 2013 Paul Butler

This software is provided 'as-is', without any express or implied
warranty.  In no event will the authors be held liable for any damages
arising from the use of this software.

Permission is granted to anyone to use this software for any purpose,
including commercial applications, and to alter it and redistribute it
freely, subject to the following restrictions:

1. The origin of this software must not be misrepresented; you must not
claim that you wrote the original software. If you use this software
in a product, an acknowledgment in the product documentation would be
appreciated but is not required.
2. Altered source versions must be plainly marked as such, and must not be
misrepresented as being the original software.
3. This notice may not be removed or altered from any source distribution.
