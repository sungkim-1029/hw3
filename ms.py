""" A subclass of a constraint problem to find a magic square for a
    nxn grid and sum n*(n*n+1)/2. """

from constraint import *

class MS(Problem):

    def __init__(self, n=3, solver=None):

        """N is the size of the magic square, solver is the CSP solver
           that will be used to sove the problem """

        # call the base class init method
        super(MS, self).__init__(solver=solver)

        # set any MS instance variables needed
        # define CSP variables with their domains
        # add CSP constraints 
        

