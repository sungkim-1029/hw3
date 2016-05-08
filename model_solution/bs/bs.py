""" A subclass of a constraint problem to solve a 6x6 battleship puzzle """

from constraint import *
from collections import defaultdict
from sys import stdout

class BS(Problem):

    def __init__(self, size, colsums, rowsums, ships, hints, solver=BacktrackingSolver()):

        super(BS, self).__init__(solver=solver)

        self.hints = hints
        self.size = size
        self.colsums = colsums
        self.rowsums = rowsums
        self.ships = ships

        domain1 = [(col, row, 1, '*') for col in range(size) for row in range(size)]
        domain2 = [(col, row, 2, 'h') for col in range(size-1) for row in range(size)] + \
                  [(col, row, 2, 'v') for col in range(size) for row in range(size-1)]
        domain3 = [(col, row, 3, 'h') for col in range(size-2) for row in range(size)] + \
                  [(col, row, 3, 'v') for col in range(size) for row in range(size-2)]
        
        # add variables
        for ship_size, num in ships.items():
            for i in range(num):
                v = (ship_size, i)
                if ship_size == 1 and domain1:
                    self.addVariable(v, domain1)
                elif ship_size == 2 and domain2:
                    self.addVariable(v, domain2)
                elif ship_size ==3 and domain3:
                    self.addVariable(v, domain3)                    
        vars = self._variables.keys()
        
        # a ship cannot violate a hint
        for v in vars:
            self.addConstraint(lambda v: hints_ok(v, self.hints), [v])

        # ships can't overlap or touch
        for v1 in vars:
            for v2 in vars:
                if v1 < v2:
                    self.addConstraint(notouch, [v1,v2])

        # row constraints
        for row in range(size):
            self.addConstraint(RowSumConstraint(row, rowsums[row]))

        # column sum constraints
        for col in range(size):
            self.addConstraint(ColumnSumConstraint(col, colsums[col]))

    def __repr__(self):
        return "BS(%s, %s, %s, %s, %s)" % (self.size, self.colsums, self.rowsums, self.ships, self.hints)
        


def print_solution(problem, solution):
    """ Prints solution of problem """

    # print parameters
    print 'Problem:', problem
    print 'Solution:', solution

    if False and not solution:
        print 
        return

    # problem parameters
    size = problem.size
    rowsums = problem.rowsums
    colsums = problem.colsums

    if solution:
        # board maps ship cell positions to ship part strings
        board = defaultdict(lambda: ' ~ ')
        for ship in solution.values():
            for cell in ship_cells(ship):
                board[cell] = ' ' + ship_val(ship, cell) + ' '
    else:
        board = defaultdict(lambda: ' ? ')
        for cell,val in problem.hints.items():
            board[cell] = ' ' + val + ' '

    # print board
    stdout.write('\n')
    for row in range(size):
        for col in range(size):
            stdout.write(board[(col,row)])
        stdout.write(" %s\n" % rowsums[row])
    stdout.write(' ' + '  '.join(map(str, colsums))+'\n')
    print
    
def notouch(ship1, ship2):
    for (c1, r1) in ship_cells(ship1):
        for (c2, r2) in ship_cells(ship2):
            c_delta = abs(c1-c2)
            r_delta = abs(r1-r2)
            if (r_delta, c_delta) in [(0,1), (1,0), (0,0)]:
                return False
    return True

def hints_ok(ship, hints):
    for cell, val in hints.items():
        if cell in ship_cells(ship) and val != ship_val(ship, cell):
            return False
    return True

def ship_cells(ship):
    """ returns a list of cells occupied by a ship """
    col, row, size, orient = ship
    results = [(col, row)]
    for i in range(1,size):
        if orient == 'h':
            results.append((col+i, row))
        else:
            results.append((col, row+i))
    return results

def ship_val(ship, cell):
    """ returns None if cell is not in ship or a string to represent
        value of ship part at cell """
    cells = ship_cells(ship)
    col, row, size, orient = ship    
    if cell not in cells:
        return None
    elif size == 1:
        return '*'
    elif cell == cells[0]:
        return '<' if orient == 'h' else '^'
    elif cell == cells[-1]:
        return '>' if orient == 'h' else 'v'
    else:
        return '#'

def num_in_row(ship, row):
    """
    returns number of cells a ship has in a row
    """
    n = 0
    for (c,r) in ship_cells(ship):
        if r == row:
            n +=1
    return n

def num_in_col(ship, col):
    """
    returns number of cells a ship has in a column
    """
    n = 0
    for (c,r) in ship_cells(ship):
        if c == col:
            n +=1
    return n

class RowSumConstraint(Constraint):

    def __init__(self, row, rowsum):
        self._rowsum = rowsum
        self.row = row

    def preProcess(self, variables, domains, constraints, vconstraints):
        Constraint.preProcess(self, variables, domains, constraints, vconstraints)
        rowsum = self._rowsum
        for variable in variables:
            domain = domains[variable]
            for value in domain[:]:
                if num_in_row(value, self.row) > rowsum:
                    domain.remove(value)

    def __call__(self, variables, domains, assignments, forwardcheck=False):
        rowsum = self._rowsum
        sum = 0
        missing = False
        for variable in variables:
            if variable in assignments:
                sum += num_in_row(assignments[variable], self.row)
            else:
                missing = True
        if sum > rowsum:
            return False
        if forwardcheck and missing:
            for variable in variables:
                if variable not in assignments:
                    domain = domains[variable]
                    for value in domain[:]:
                        if sum+num_in_row(value, self.row) > rowsum:
                            domain.hideValue(value)
                    if not domain:
                        return False
        if missing:
            return sum <= rowsum
        else:
            return sum == rowsum
    

class ColumnSumConstraint(Constraint):

    def __init__(self, col, colsum):
        self._colsum = colsum
        self.col = col

    def preProcess(self, variables, domains, constraints, vconstraints):
        Constraint.preProcess(self, variables, domains, constraints, vconstraints)
        colsum = self._colsum
        for variable in variables:
            domain = domains[variable]
            for value in domain[:]:
                if num_in_col(value, self.col) > colsum:
                    domain.remove(value)

    def __call__(self, variables, domains, assignments, forwardcheck=False):
        colsum = self._colsum
        sum = 0
        missing = False
        for variable in variables:
            if variable in assignments:
                sum += num_in_col(assignments[variable], self.col)
            else:
                missing = True
        if sum > colsum:
            return False
        if forwardcheck and missing:
            for variable in variables:
                if variable not in assignments:
                    domain = domains[variable]
                    for value in domain[:]:
                        if sum+num_in_col(value, self.col) > colsum:
                            domain.hideValue(value)
                    if not domain:
                        return False
        if missing:
            return sum <= colsum
        else:
            return sum == colsum

# tests

def test1(problem):
    print_solution(problem, problem.getSolution())

def test():
    # run bs on some tests cases
    test1(BS(2, colsums=[1,1], rowsums=[1,1], ships={1:2, 2:0, 3:0}, hints={}))
    test1(BS(6, colsums=[1,0,4,0,3,2], rowsums=[4,0,2,1,2,1], ships={1:3, 2:2, 3:1}, hints={(2,2):'~'}))
    test1(BS(6,colsums=[3,1,0,3,0,3], rowsums=[1,1,2,1,1,4], ships={1:3, 2:2, 3:1}, hints={(1,5):'^'}))
    test1(BS(6, [2,2,0,3,1,2], [2,2,0,3,1,2], {1:3, 2:2, 3:1}, {(0,0):'<', (1,3):'~'}))
    


        
