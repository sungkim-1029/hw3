""" A subclass of a constraint problem to solve an n-queens problem of
    a given size with a given solver """

from constraint import *

class NQ(Problem):

    def __init__(self, size=8, solver=None):
        super(NQ, self).__init__(solver=solver)

        self.addVariables(range(size), range(size))
        for c1 in range(size):
            for c2 in range(c1+1,size):
                self.addConstraint(lambda row1, row2, col1=c1, col2=c2:
                                abs(row1-row2) != abs(col1-col2) and row1 != row2,
                                (c1, c2))
