""" A subclass of a constraint problem to solve a 6x6 battleship puzzle """

from constraint import *

class BS(Problem):

    def __init__(self, size, colsums, rowsums, ships, hints, solver=BacktrackingSolver()):

        super(BS, self).__init__(solver=solver)

        self.hints = hints

        places1 = [(col, row, 1, '*') for col in range(size) for row in range(size)]
        places2 = [(col, row, 2, 'h') for col in range(size-1) for row in range(size)] + \
                  [(col, row, 2, 'v') for col in range(size) for row in range(size-1)]
        places3 = [(col, row, 3, 'h') for col in range(size-2) for row in range(size)] + \
                  [(col, row, 3, 'v') for col in range(size) for row in range(size-2)]
        
        vars = []
        # add variables
        for ship_size, num in ships.items():
            for i in range(num):
                v = (ship_size, i)
                vars.append(v)
                if ship_size == 1 and places1:
                    self.addVariable(v, places1)
                elif ship_size == 2 and places2:
                    self.addVariable(v, places2)
                elif ship_size ==3 and places3:
                    self.addVariable(v, places3)                    

        # a ship cannot violate a hint
        for v in vars:
            self.addConstraint(lambda v: hints_ok(v, self.hints), [v])

        # ships can't overlap or touch
        for v1 in vars:
            for v2 in vars:
                if v1 < v2:
                    self.addConstraint(lambda x,y: notouch(x,y), [v1,v2])

        # row constraints
        for row in range(size):
            self.addConstraint(RowSumConstraint(row, rowsums[row]))

        # column sum constraints
        for col in range(size):
            self.addConstraint(ColumnSumConstraint(col, colsums[col]))
        

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
        if cell in ship_cells(ship) and val != shipval(ship, cell):
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

def shipval(ship, cell):
    """ returns None if cell is not in ship or
        value of ship part at cell """
    cells = ship_cells(ship)
    col, row, size, orient = ship    
    if cell not in cells:
        return None
    elif size == 1:
        return '*'
    elif cell == cells[0]:
        return '<' if orient == 'h' else 'v'
    elif cell == cells[-1]:
        return '>' if orient == 'h' else '^'
    else:
        return '#'

def num_in_row(ship, row):
    """
    returns number of cells a ship has in a row
    """
    n = 0
    #print ship, ship_cells(ship)
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
                #print variable, assignments                
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
                #print variable, assignments
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
    
        
p1 = BS(2, colsums=[1,1], rowsums=[1,1], ships={1:2, 2:0, 3:0}, hints={})
p2 = BS(6, colsums=[1,0,4,0,3,2], rowsums=[4,0,2,1,2,1], ships={1:3, 2:2, 3:1}, hints={(3,3):'~'})
