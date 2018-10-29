# CS121: Schelling Model of Housing Segregation
# 

# Automatically added to test code for is_satisfied.

# Handle the fact that the test code may not be in the same directory
# as schelling.py

import os
import sys

sys.path.append(os.getcwd())

import schelling
import pytest
import utility

def helper_test_is_satisfied(filename, R, location, threshold, expected):
    '''
    Check result of calling is_satisfied on the specified location with
    in an R-neighborhood with the specified threshold.

    Inputs:
        filename: (string) name of the input grid file
        R: (integer) neighborhood parameter
        location: (pair of integers) location in the grid to be tested
        threshold: (float) satisfaction threshold
        expected: (boolean) expected result.
    '''
    grid = utility.read_grid(filename)

    actual = schelling.is_satisfied(grid, R, threshold, location)
    if actual != expected:
        s = "Actual value ({}) is not equal to the expected value ({}).\n"
        s = s + "    @ location {} with R={:d} and threshold={:.2f}.\n"
        pytest.fail(s.format(actual, expected, location, R, threshold))


# Generated code



def test_0():
    # Check boundary neighborhood:top left corner.
    helper_test_is_satisfied("tests/sample-grid.txt", 1, (0, 0), 0.8233333333333334, True)

def test_1():
    # Check boundary neighborhood:top left corner.
    helper_test_is_satisfied("tests/sample-grid.txt", 1, (0, 0), 0.8433333333333334, False)

def test_2():
    # Check boundary neighborhood: top left corner.
    helper_test_is_satisfied("tests/sample-grid.txt", 2, (0, 0), 0.6566666666666666, True)

def test_3():
    # Check boundary neighborhood: top left corner.
    helper_test_is_satisfied("tests/sample-grid.txt", 2, (0, 0), 0.6766666666666666, False)

def test_4():
    # Check boundary neighborhood: top right corner.
    helper_test_is_satisfied("tests/sample-grid.txt", 1, (0, 4), 0.6566666666666666, True)

def test_5():
    # Check boundary neighborhood: top right corner.
    helper_test_is_satisfied("tests/sample-grid.txt", 1, (0, 4), 0.6766666666666666, False)

def test_6():
    # Check boundary neighborhood: top right corner.
    helper_test_is_satisfied("tests/sample-grid.txt", 2, (0, 4), 0.5733333333333334, True)

def test_7():
    # Check boundary neighborhood: top right corner.
    helper_test_is_satisfied("tests/sample-grid.txt", 2, (0, 4), 0.5933333333333334, False)

def test_8():
    # Check boundary neighborhood: lower left corner.
    helper_test_is_satisfied("tests/sample-grid.txt", 1, (4, 0), 0.49, True)

def test_9():
    # Check boundary neighborhood: lower left corner.
    helper_test_is_satisfied("tests/sample-grid.txt", 1, (4, 0), 0.51, False)

def test_10():
    # Check boundary neighborhood: lower left corner.
    helper_test_is_satisfied("tests/sample-grid.txt", 2, (4, 0), 0.5733333333333334, True)

def test_11():
    # Check boundary neighborhood: lower left corner.
    helper_test_is_satisfied("tests/sample-grid.txt", 2, (4, 0), 0.5933333333333334, False)

def test_12():
    # Check neighborhood that is complete when R is 1.
    helper_test_is_satisfied("tests/sample-grid.txt", 1, (1, 1), 0.49, True)

def test_13():
    # Check neighborhood that is complete when R is 1.
    helper_test_is_satisfied("tests/sample-grid.txt", 1, (1, 1), 0.51, False)

def test_14():
    # Check neighborhood that is not complete when R is 2.
    helper_test_is_satisfied("tests/sample-grid.txt", 2, (1, 1), 0.4445454545454545, True)

def test_15():
    # Check neighborhood that is not complete when R is 2.
    helper_test_is_satisfied("tests/sample-grid.txt", 2, (1, 1), 0.46454545454545454, False)

def test_16():
    # Check interior neighborhood with location that has no neighbors.
    helper_test_is_satisfied("tests/grid-no-neighbors.txt", 1, (2, 2), 0.59, True)

def test_17():
    # Check interior neighborhood with location that has no neighbors.
    helper_test_is_satisfied("tests/grid-no-neighbors.txt", 1, (2, 2), 0.61, False)

def test_18():
    # Check interior neighborhood with a location that has no neighbors.
    helper_test_is_satisfied("tests/grid-no-neighbors.txt", 2, (2, 2), 0.6438461538461538, True)

def test_19():
    # Check interior neighborhood with a location that has no neighbors.
    helper_test_is_satisfied("tests/grid-no-neighbors.txt", 2, (2, 2), 0.6638461538461539, False)

def test_20():
    # Check boundary neighborhood (lower right corner) with location that has no neighbors.
    helper_test_is_satisfied("tests/grid-no-neighbors.txt", 1, (4, 4), 0.6566666666666666, True)

def test_21():
    # Check boundary neighborhood (lower right corner) with location that has no neighbors.
    helper_test_is_satisfied("tests/grid-no-neighbors.txt", 1, (4, 4), 0.6766666666666666, False)

def test_22():
    # Check boundary neighborhood (lower right corner) with location that has a few neighbors.
    helper_test_is_satisfied("tests/grid-no-neighbors.txt", 2, (4, 4), 0.4066666666666667, True)

def test_23():
    # Check boundary neighborhood (lower right corner) with location that has a few neighbors.
    helper_test_is_satisfied("tests/grid-no-neighbors.txt", 2, (4, 4), 0.4266666666666667, False)

def test_24():
    # Check one blue homeowner in an all red neighborhood.
    helper_test_is_satisfied("tests/grid-lone-blue-sea-of-red.txt", 1, (3, 3), 0.19, True)

def test_25():
    # Check one blue homeowner in an all red neighborhood.
    helper_test_is_satisfied("tests/grid-lone-blue-sea-of-red.txt", 1, (3, 3), 0.21000000000000002, False)

def test_26():
    # Check one blue homeowner in an all red boundary neighborhood.
    helper_test_is_satisfied("tests/grid-lone-blue-sea-of-red.txt", 2, (3, 3), 0.08090909090909092, True)

def test_27():
    # Check one blue homeowner in an all red boundary neighborhood.
    helper_test_is_satisfied("tests/grid-lone-blue-sea-of-red.txt", 2, (3, 3), 0.1009090909090909, False)

def test_28():
    # R is 3.
    helper_test_is_satisfied("tests/sample-grid.txt", 3, (2, 2), 0.5138095238095238, True)

def test_29():
    # R is 3.
    helper_test_is_satisfied("tests/sample-grid.txt", 3, (2, 2), 0.5338095238095238, False)

