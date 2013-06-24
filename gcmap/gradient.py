
import numpy as np

class Gradient:
    '''
    Simple multi-color gradient implementation.

    Specify the colors as a list of (start, red, green, blue)
    tuples where start is a fraction [0..1] indicating where
    each section of the gradient starts.

    The gradient object is initialized with a list of stops.
    Once initialized, the gradient object can be called like
    a function with one parameter, a fraction, to return colors.

    Uses linear color combinations. Outputs the color as a
    (red, green, blue) triple.

    >>> g = Gradient([(0, 0, 255, 0),
    ...               (0.5, 255, 255, 0),
    ...               (1, 255, 255, 255)])
    >>> g(0)
    (0, 255, 0)
    >>> g(0.5)
    (255, 255, 0)
    >>> g(1)
    (255, 255, 255)
    >>> g(0.3)
    (153, 255, 0)
    '''

    def __init__(self, colors):
        '''
        Create a gradient object.

        Parameters:
            colors      a list of (start, red, green, blue) tuples
                        where 0 <= start <= 1 is a fractional position
                        on the gradient and (red, green, blue) is the
                        color at that gradient (as integers out of 255)

        Returns a gradient object which can be called like a function.
        '''
        self.colors = np.matrix(colors)

    def __call__(self, frac):
        '''
        Compute the color value at a given fractional position on the
        gradient.

        Parameters:
            frac        the fraction along the gradient at which to
                        compute the color

        Returns a triple (red, green, blue) specifying the color at
        the given point on the gradient. red, green, and blue are
        integers on the same scale as the gradient was initialized with.
        '''
        # find the index of the gradient segment that the fraction
        # falls on
        for i in range(0, self.colors.shape[0]):
            if self.colors[i, 0] > frac:
                break
        # compute how far along the segment we are
        segment_frac = (frac - self.colors[i-1, 0]) / (self.colors[i,0] - self.colors[i-1,0])
        # create a 1x2 matrix to linearly blend the colors
        segment_blend = np.matrix([1-segment_frac, segment_frac])
        # compute the blended color
        color = segment_blend * self.colors[i-1:i+1, 1:4]
        return tuple(np.int32(np.array(color)[0]))
        
        

