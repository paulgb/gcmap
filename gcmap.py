
import numpy as np
from pyproj import Geod, Proj
from PIL import Image
from aggdraw import Draw, Pen
import operator
from math import pi

from gradient import Gradient

default_cols = Gradient(((0, 0, 0, 0), (0.5, 0, 0, 255), (1, 255, 255, 255)))
default_bg = (0, 0, 0)

class GCMapper:
    def __init__(self, width=800,
            height=None, bgcol=default_bg,
            cols=default_cols, line_width=1, gc_resolution=100):
        '''
        Create an object for turning coordinate pairs into an image.

        Parameters
            height          the height of the resultant image
            width           the width of the resultant image
            bgcol           the background color of the image,
                            as an (r,g,b) triple
            cols            a function which takes one fractional
                            argument and returns a color (r,g,b) triple
            line_width      the width of lines drawn
            gc_resolution   the number of straight line segments
                            used to approximate each great-circle
                            curve

        Once the object is initialized, call set_data to add data.
        '''

        if height is None:
            height = width / 2

        self.height = height
        self.width = width
        self.bgcol = bgcol
        self.line_width = line_width
        self.gc_resolution = gc_resolution
        self.cols = cols
        self.geo = Geod(a=1)

    def set_data(self, lon1, lat1, lon2, lat2, count=None):
        '''
        Set the coordinate pairs to be drawn. The pairs are given
        as equal-length lists of longitudes and latitudes of each
        point in the pair, giving four lists total. A fifth list,
        count, optionally gives the frequency at which each pair
        occurred in the source data.

        Parameters:
            lon1        the longitudes of the source points
            lat1        the latitudes of the source points
            lon2        the longitudes of the destination points
            lat2        the latitudes of the destination points
            count       the frequency of each pair


        Once the data is set, call draw() to render the image.
        '''
        self.data = np.array((lon1, lat1, lon2, lat2)).T
        self.data_size = self.data.shape[0]

        # calculate great-circle distances between each coordinate
        # pair. This will be used for determining which order to
        # draw the lines in.
        _, _, dist = self.geo.inv(np.array(lon1),
                                  np.array(lat1),
                                  np.array(lon2),
                                  np.array(lat2))

        # if a frequency count is given, take it into account when
        # creating weights. Weights determine the coloring and
        # drawing order of each line.
        if count:
            self.weight = np.array(count) / dist
        else:
            self.weight = 1 / dist

        self.order = np.argsort(self.weight)

    def draw(self):
        '''
        Render the image
        '''

        img = Image.new('RGB', (self.width, self.height), self.bgcol)
        canvas = Draw(img)

        # create the projection. Here we use an equidistant cylindrical projection,
        # but others may work with tweaking of the parameters.
        proj = Proj(proj='eqc',
                a=self.width/(2*pi), # set the radius of the earth such that our
                                     # projections work
                x_0=self.width/2,    # center horizontally on the image
                y_0=self.height/2)   # center verticallly on the image

        # two branches below will use the same sequence of commands to
        # draw a great-circle on the map, so the common elements are wrapped
        # up into a locally defined function. Given a matrix of points and
        # a pen, draw the path through the points.
        def draw_(pts, pen):
            lons, lats = pts.T
            x, y = proj(lons, lats)
            y = self.height - y
            path = reduce(operator.add, zip(x, y))
            canvas.line(path, pen)

        # loop over every coordinate pair
        for i, (lon1, lat1, lon2, lat2, count) in enumerate(self.data[self.order]):
            # calculate the fraction of the paths already drawn, and use
            # it to create a pen of the appropriate color
            frac = i / float(self.data_size)
            pen = Pen(self.cols(frac), self.line_width)

            # find the intermediate coordinates along a line between the two 
            # coordinates
            pts = self.geo.npts(lon1, lat1, lon2, lat2, self.gc_resolution)
            pts = np.array(pts)

            # if the longitudinal distance between the two points (travelling
            # through the prime meridian) is more than 180 degrees, it's faster
            # to *not* travel through the prime meridian, so we have to special-
            # case the drawing of the lines.
            if abs(lon1 - lon2) >= 180:
                # find the index of the path where the line wraps around the image
                (cut_point,), = np.where(np.abs(np.diff(pts[:,0])) > 180)
                
                # draw the two resultant lines separately
                pts1 = pts[:cut_point,:]
                pts2 = pts[cut_point+1:,:]
                draw_(pts1, pen)
                draw_(pts2, pen)
            else:
                # the path does not wrap the image, so we can simply draw
                # it as-is
                draw_(pts, pen)
            
        canvas.flush()

        img.save('foo.png')

