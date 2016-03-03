""" A subclass of a constraint problem to solve an n-queens problem of
    a given size with a given solver """

from constraint import *

class NQ(Problem):

    def __init__(self, n=8, solver=None):

        """N is the size of the board, solver is the CSP solver
           that will be used to sove the problem """

        # call the base class init method
        super(NQ, self).__init__(solver=solver)

        # set any NQ instance variables needed
        # define CSP variables with their domains
        # add CSP constraints 
        
