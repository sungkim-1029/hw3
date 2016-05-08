""" A subclass of a constraint problem to find a magic square for a
    nxn grid and sum n*(n*n+1)/2. """

from constraint import *

class MS(Problem):

    def __init__(self, n=3, solver=None):

        super(MS, self).__init__(solver=solver)

        # compute default magic sum if none is given
        magic_sum = n * (n*n + 1) / 2
        
        vars = range(n*n)
        self.addVariables(vars, range(1, n*n+1))

        # all numbers in the square must be different
        self.addConstraint(AllDifferentConstraint())
        # diagonal down sums to magic_sum
        self.addConstraint(ExactSumConstraint(magic_sum), [row*(n+1) for row in range(n)])
        # diagonal up sums to magic_sum
        self.addConstraint(ExactSumConstraint(magic_sum), [row*(n-1)+n-1 for row in range(n)])
        # rows must sum to magic_sum
        for row in range(n):
            self.addConstraint(ExactSumConstraint(magic_sum), [row*n+i for i in range(n)])
        for col in range(n):
            self.addConstraint(ExactSumConstraint(magic_sum), [col+n*i for i in range(n)])

