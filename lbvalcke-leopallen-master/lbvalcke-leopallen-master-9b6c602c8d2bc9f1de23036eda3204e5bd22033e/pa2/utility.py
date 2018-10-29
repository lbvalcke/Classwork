#  CS121:: Schelling Model of Housing Segregation
#
#  Utility code for managing grids.
#

import csv
import os
import sys
import schelling


def check_row(N, row, i):
    '''
    Check the format of ith row.

    Inputs:
        N: (int) the expected length of the row
        row: (list of strings) a row from the file
        i: (int) the row's line number in the file

    '''
    if len(row) != N:
        print("Format error in line {}: row is wrong length".format(i))
        sys.exit(0)
    if set(row) - set(("R", "B", "O")) != set():
        print("Format error in line {}: row has character other than R/B/O".format(i))
        sys.exit(0)


def read_grid(filename, strip_Us=True):
    '''
    Read a grid from a text file and return the corresponding
    in-memory representation.

    Inputs:
        filename: (string) the name of the grid file to read

    returns: (list of list of strings) the grid contained in file f.
    '''

    if not os.path.isfile(filename):
        print("Bad file name:" + filename)
        sys.exit(0)

    with open(filename) as f:
        reader = csv.reader(f, delimiter = " ")
        grid = []
        i = 0
        for row in reader:
            if i == 0 and len(row) == 1:
                # old format with N in the file
                continue
            if strip_Us:
                # remove indications of unsatisfied homeowners if necessary
                row = [(x[1:] if len(x) > 0 and x[0] == "U" else x).strip() for x in row]
            if i == 0:
                N = len(row)
            if not strip_Us:
                check_row(N, row, i)
            grid.append(row)
            i = i + 1

        if len(grid) == 0:
            print("File is empty")
            sys.exit(0)

        return grid


def is_grid(grid):
    '''
    Verify that grid is a list (length N) where each element is a list
    of length N.  For smaller grids, checks that the rows contain the
    values "R", "B", and "O"."

    Inputs:
        grid: a value

    returns: True, if the input has the correct form.

    '''
    MAX_SMALL_GRID = 20

    if not isinstance(grid, list):
        return False

    if len(grid) == 0:
        return False

    N = len(grid)
    if N <= MAX_SMALL_GRID:
        # do full check only for small grids
        for row in grid:
            if not isinstance(row, list) or len(row) != N:
                return False
            for home in row:
                if home not in ["R", "B", "O"]:
                    return False
    else:
        for row in grid:
            if not isinstance(row, list) or len(row) != N:
                return False

    return True


def print_grid(grid):
    '''
    Print a text representation of a grid.

    Inputs:
        grid: (list of lists of strings)
    '''
    print(len(grid))
    for row in grid:
        print(row)


def find_mismatch(grid0, grid1):
    '''
    Find the first location where two grids differ.

    Inputs:
        grid0, grid1: (lists of lists of strings) grids

    Returns: None if the grids are the same, a location (int, int), if the
    grids are not the same.
    '''

    assert is_grid(grid0) and is_grid(grid1), \
        "Grids are not lists of lists of strings."

    assert len(grid0) == len(grid1), \
        "Grids are not the same shape."

    assert len(grid0[0]) == len(grid1[0]), \
        "Grids are not the same shape."

    for i in range(len(grid0)):
        for j in range(len(grid0[0])):
            # strip unsatisfied indicator from values if necessary
            val0 = grid0[i][j] if "U" not in grid0[i][j] else grid0[i][j][1]
            val1 = grid1[i][j] if "U" not in grid1[i][j] else grid1[i][j][1]
            if val0 != val1:
                return (i, j)
    return None

