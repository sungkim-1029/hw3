""" A subclass of a constraint problem to solve a 6x6 battleship puzzle """

from constraint import *

class BS(Problem):

    def __init__(self, size, columns, rows, ships, hints, solver=None):

        super(BS, self).__init__(solver=solver)
        
        # add variables
        vars = [(col, row) for col in range(size) for row in range(size)]
        domain = ['up', 'down', 'left', 'right']
        self.addVariables(vars, domain)

        # record hints, overwriting previous domain to a single value
        for var, val in hints:
            self.addVariable(var, [val])

        # add constraints
        
