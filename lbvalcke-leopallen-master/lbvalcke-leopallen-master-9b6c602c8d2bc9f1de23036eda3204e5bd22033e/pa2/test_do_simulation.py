# CS121: Schelling Model of Housing Segregation
#
# Test code for do_simulation
#

import os
import sys

timeout = 60

# Handle the fact that the grading code may not
# be in the same directory as schelling.py
sys.path.append(os.getcwd())

# Get the test files from the same directory as
# this file.
BASE_DIR = os.path.dirname(__file__)


from schelling import do_simulation
import pytest
import utility


def count_homeowners(grid):
    num_homeowners = 0
    for row in grid:
        for home in row:
            if home != "O":
                num_homeowners += 1
    return num_homeowners


def helper(input_filename, expected_filename, R, threshold,
           max_num_steps, expected_num_steps):
    '''
    Do one simulation with the specified parameters (R, threshold,
    max_num_steps) starting from the specified input file.  Match
    actual grid generated with the expected grid and match expected
    steps and actual steps.
    '''

    input_filename = os.path.join(BASE_DIR, input_filename)
    actual_grid = utility.read_grid(input_filename)
    actual_num_steps = do_simulation(actual_grid, R, threshold, max_num_steps)
    actual_num_homeowners = count_homeowners(actual_grid)

    expected_filename = os.path.join(BASE_DIR, expected_filename)
    expected_grid = utility.read_grid(expected_filename)
    expected_num_homeowners = count_homeowners(expected_grid)

    if actual_num_homeowners != expected_num_homeowners:
        if actual_num_homeowners <= expected_num_homeowners:
            s = "Homeowners are fleeing the city!\n"
        else:
            s = "City is gaining homeowners.\n"
        s += "    Actual number of homeowners: {:d}\n".format(actual_num_homeowners)
        s += "    Expected number of homeowners: {:d}\n".format(expected_num_homeowners)
        pytest.fail(s)

    mismatch = utility.find_mismatch(actual_grid, expected_grid)
    if mismatch:
        s = "actual and expected grid values do not match at location ({:d}, {:d})\n"
        s = s.format(mismatch[0], mismatch[1])

        actual = actual_grid[mismatch[0]][mismatch[1]]
        expected = expected_grid[mismatch[0]][mismatch[1]]
        s += "    got {}, expected {}".format(actual, expected)
        pytest.fail(s)

    # check steps only when expected steps >= 0
    if expected_num_steps >= 0 and actual_num_steps != expected_num_steps:
        s = "actual and expected values number of steps do not match\n"
        s = s + "    got {:d}, expected {:d}".format(actual_num_steps, expected_num_steps)
        pytest.fail(s)

def test_0():
    # Check stopping condition #1
    helper("tests/sample-grid.txt", "tests/sample-grid-1-51-0-final.txt", 1, 0.51, 0, 0)

def test_1():
    # All homeowners statisfied at the start. Check stopping condition #2
    helper("tests/sample-grid.txt", "tests/sample-grid-1-49-2-final.txt", 1, 0.49, 2, 1)

def test_2():
    # Check sample grid after 1 simulation step
    helper("tests/sample-grid.txt", "tests/sample-grid-1-51-1-final.txt", 1, 0.51, 1, 1)

def test_3():
    # Check sample grid after 2 simulation steps
    helper("tests/sample-grid.txt", "tests/sample-grid-1-51-2-final.txt", 1, 0.51, 2, 2)

def test_4():
    # Check sample grid after 3 simulation steps
    helper("tests/sample-grid.txt", "tests/sample-grid-1-51-3-final.txt", 1, 0.51, 3, 3)

def test_5():
    # Check sample grid after 4 simulations steps
    helper("tests/sample-grid.txt", "tests/sample-grid-1-51-4-final.txt", 1, 0.51, 4, 4)

def test_6():
    # Check stopping condition #2
    helper("tests/sample-grid.txt", "tests/sample-grid-1-51-5-final.txt", 1, 0.51, 5, 4)

def test_7():
    # Check case where possible new location is in the homeowner's current neighborhood
    helper("tests/grid-lone-blue-sea-of-red-2.txt", "tests/grid-lone-blue-sea-of-red-2-1-40-2-final.txt", 1, 0.4, 2, 1)

def test_8():
    # Check sample grid with R of 2
    helper("tests/sample-grid.txt", "tests/sample-grid-2-51-7-final.txt", 2, 0.51, 7, 7)

def test_9():
    # Check stopping condition #2
    helper("tests/sample-grid.txt", "tests/sample-grid-2-51-8-final.txt", 2, 0.51, 8, 7)

def test_10():
    # Check sample grid with R of 3
    helper("tests/sample-grid.txt", "tests/sample-grid-3-51-5-final.txt", 3, 0.51, 5, 5)

@pytest.mark.large
def test_11():
    # Check efficiency using large grid with R of 3
    helper("tests/grid-150-40-40.txt", "tests/grid-150-40-40-3-51-100-final.txt", 3, 0.51, 100, 41)

