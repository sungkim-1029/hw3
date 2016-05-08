#! /usr/bin/python
# Tim Finin, http://umbc.edu/~finin/, finin@umbc.edu

# Test framework for HW3

import sys
import time
import signal
from operator import itemgetter

# import solvers from python_constraints
from constraint import BacktrackingSolver, RecursiveBacktrackingSolver, MinConflictsSolver

# load the CSP problems for magic squares and nqueens
from ms import MS
from nq import NQ

# support for a simple timeout mechanism
class TimeoutException(Exception): 
    pass 

def timeout(signum, frame):
    raise TimeoutException('Timed Out')

#SIGALRM is only usable on a unix platform
signal.signal(signal.SIGALRM, timeout)


# test a CSP problem
def tester(constraint_problem, sizes, max_time):
    """ show the time it takes to solve a constraint problem
        varying sizes using different solvers. """

    # dictionary of solutons by size
    solutions = {}
    
    solvers = [BacktrackingSolver, RecursiveBacktrackingSolver, MinConflictsSolver]

    # print table header line
    print "Size\t",
    for s in solvers:
        print "%s\t" % (s.__name__[0:7],),
    print

    # print results for each size
    for n in sizes:
        print "%s\t" % (n,),
        for s in solvers:
            start = time.time()
            try:
                # set the alarm for max_time seconds
                signal.alarm(max_time)
                solution =  constraint_problem(n, solver=s()).getSolution()
                # clear alarm since it didn't go off
                signal.alarm(0)
            except TimeoutException:
                solution = '?'
            elapsed = time.time() - start
            if solution == None:
                print "F:%.2f\t" % (elapsed,) ,
            elif solution == '?':
                print "?:%.2f\t" % (elapsed,) ,
            else:
                print "T:%.2f\t" % (elapsed,) ,
                solutions[n] =  solution
        print

    # print solutions found
    for n, sol in sorted(solutions.items(), key=itemgetter(1)):
        print "\nSize:", n, sol

if __name__ == "__main__":
    # default timeout in seconds
    timeout = 30
    if len(sys.argv) > 1:
        timeout = int(sys.argv[1])

    # test the magic squares problem
    print "\nMagic Squares"
    tester(MS, [3,4,5,6], timeout)

    # test the n queens problem
    print "\nQueens Squares"
    tester(NQ, [8,16,32,64,128,256,512], timeout)
         
