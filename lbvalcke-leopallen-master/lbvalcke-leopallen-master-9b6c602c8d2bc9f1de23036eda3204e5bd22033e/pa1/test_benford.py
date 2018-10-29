# CS121: Test code for Benford's Law assignment
#
# Anne Rogers
# June 2015, April 2016

import math
import pytest
import os
import sys

# Handle the fact that the grading code may not
# be in the same directory as benford.py
sys.path.append(os.getcwd())

from benford import *
from util import read_column_from_csv

# Get the name of the directory that holds the grading code.
BASE_DIR = os.path.dirname(__file__)

timeout=60


TEST_DATA_DIR=os.path.join(BASE_DIR, "data")

################## Extract leading digit of single value tests ##################

NUM_LD_TESTS = 6
LD_POINTS = 6
LD_POINTS_PER_TEST=LD_POINTS/NUM_LD_TESTS

def helper_extract_leading_digits(num_digits, amount, expected):
    leading_digits = extract_leading_digits(amount, num_digits)
    if leading_digits != expected:
        pytest.fail("Expected value ({:d}) and actual value ({:d}) do not match.".format(expected, leading_digits))

def test_extract_leading_digits_1():
    helper_extract_leading_digits(1, "$2.34", 2)

def test_extract_leading_digits_2():
    helper_extract_leading_digits(2, "$2.34", 23)

def test_extract_leading_digits_3():
    helper_extract_leading_digits(3, "$2.34", 234)

def test_extract_leading_digits_4():
    '''leading zero'''
    helper_extract_leading_digits(2, "$0.2034", 20)

def test_extract_leading_digits_5():
    '''floating point precision issues lead to the "wrong" answer'''
    helper_extract_leading_digits(3, "$2.01", 200)

def test_extract_leading_digits_6():
    '''
    A very slightly incorrect implementation (bad negation) passes all
    other tests except this edge case.  This test also catches the
    difference between log10(x) and log(x, 10).
    '''
    helper_extract_leading_digits(1, "$1000.00", 1)


################## Get leading digits range tests  ##################

NUM_GLDR_TESTS = 3
GLDR_POINTS = 3
GLDR_POINTS_PER_TEST=GLDR_POINTS/NUM_GLDR_TESTS

def helper_get_leading_digits_range(num_digits, expected_lb, expected_ub):
    (actual_lb, actual_ub) = get_leading_digits_range(num_digits)    
    if actual_lb != expected_lb:
        s = "Actual ({:}) and expected ({:}) lower bound do not match for {:d} number of leading digits."
        pytest.fail(s.format(actual_lb, expected_lb, num_digits))

    if actual_ub != expected_ub:
        s = "Actual ({:}) and expected ({:}) upper bound do not match for {:d} number of leading digits."
        pytest.fail(s.format(actual_ub, expected_ub, num_digits))

def test_get_leading_digits_range_1():
    helper_get_leading_digits_range(1, 1, 10)

def test_get_leading_digits_range_2():
    helper_get_leading_digits_range(2, 10, 100)

def test_get_leading_digits_range_3():
    helper_get_leading_digits_range(3, 100, 1000)
    

################## Floating point comparison helper ##################

# used in floating point equality tests
EPS = 0.0000001

def compare_actual_expected_from_file(actual, expected_filename):
    # get expected list of values from the file
    expected = []
    for x in read_column_from_csv(expected_filename, 0, True):
        expected.append(float(x))

    if not isinstance(actual, list):
        s = "Actual value returned from the function must be a list of floats."
        pytest.fail(s)

    if len(actual) > 0 and isinstance(actual[0], list):
        s = "Actual value returned from the function must be a list of floats, not a list containing a list."
        pytest.fail(s)

    if len(actual) != len(expected):
        s = "Length of expected ({0}) and actual results ({1}) do not match"
        pytest.fail(s.format(len(expected), len(actual)))

    for i in range(len(actual)):
        # stored and computed representations may not be identical
        if abs(expected[i] - actual[i]) > EPS:
            pytest.fail("actual and expected values do not match at element {0}".format(i))


################## Compute expected benford distribution tests ##################

NUM_EBD_TESTS = 2
EBD_POINTS = 6
EBD_POINTS_PER_TEST=EBD_POINTS/NUM_EBD_TESTS

def helper_test_compute_expected_benford_dist(num_digits):
    actual = compute_expected_benford_dist(num_digits)
    expected_filename = os.path.join(TEST_DATA_DIR, "expected_benford_dist_{0}_output.txt".format(num_digits))
    compare_actual_expected_from_file(actual, expected_filename)

def test_compute_expected_benford_dist_1():
    helper_test_compute_expected_benford_dist(1)

def test_compute_expected_benford_dist_2():
    helper_test_compute_expected_benford_dist(2)


################## Compute benford distribution tests ##################

NUM_CBD_TESTS = 7
CBD_POINTS = 9
CBD_POINTS_PER_TEST=CBD_POINTS/NUM_CBD_TESTS

def helper_test_compute_benford_dist(prefix, col, num_digits):
    input_filename = prefix + "input.csv"
    amounts = read_column_from_csv(input_filename, col, True)
    expected_filename = prefix + "computed_benford_dist_{0}_output.txt".format(num_digits)
    amounts_copy = amounts[:]
    actual = compute_benford_dist(amounts, num_digits)
    compare_actual_expected_from_file(actual, expected_filename)
    if amounts != amounts_copy:
        pytest.fail("Do not change the list that is passed to your function!")


def test_compute_benford_dist_1():
    '''Simple example from assignment description.'''
    helper_test_compute_benford_dist(os.path.join(TEST_DATA_DIR, "simple_"), 0, 1)

def test_compute_benford_dist_2():
    '''Amount example from assignment description.'''
    helper_test_compute_benford_dist(os.path.join(TEST_DATA_DIR, "amounts_"), 0, 1)

def test_compute_benford_dist_3():
    helper_test_compute_benford_dist(os.path.join(TEST_DATA_DIR, "amounts_"), 0, 2)

def test_compute_benford_dist_4():
    helper_test_compute_benford_dist(os.path.join(TEST_DATA_DIR, "payments_50_"), 2, 1)

def test_compute_benford_dist_5():
    helper_test_compute_benford_dist(os.path.join(TEST_DATA_DIR, "payments_50_"), 2, 2)

def test_compute_benford_dist_6():
    helper_test_compute_benford_dist(os.path.join(TEST_DATA_DIR, "payments_50000_"), 2, 1)

def test_compute_benford_dist_7():
    helper_test_compute_benford_dist(os.path.join(TEST_DATA_DIR, "payments_50000_"), 2, 2)


################## Compute benford MAD tests ##################


NUM_MAD_TESTS = 7.0
MAD_POINTS = 6
MAD_POINTS_PER_TEST=MAD_POINTS/NUM_MAD_TESTS


def helper_test_compute_benford_MAD(prefix, col, num_digits):
    input_filename = prefix + "input.csv"
    amounts = read_column_from_csv(input_filename, col, True)
    amounts_copy = amounts[:]
    actual = compute_benford_MAD(amounts, num_digits)
    if amounts != amounts_copy:
        pytest.fail("Do not change the list that is passed to your function!")

    expected_filename = prefix + "computed_benford_mad_{0}_output.txt".format(num_digits)
    compare_actual_expected_from_file([actual], expected_filename)

def test_compute_benford_MAD_1():
    helper_test_compute_benford_MAD(os.path.join(TEST_DATA_DIR, "simple_"), 0, 1)

def test_compute_benford_MAD_2():
    helper_test_compute_benford_MAD(os.path.join(TEST_DATA_DIR, "amounts_"), 0, 1)

def test_compute_benford_MAD_3():
    helper_test_compute_benford_MAD(os.path.join(TEST_DATA_DIR, "amounts_"), 0, 2)

def test_compute_benford_MAD_4():
    helper_test_compute_benford_MAD(os.path.join(TEST_DATA_DIR, "payments_50_"), 2, 1)

def test_compute_benford_MAD_5():
    helper_test_compute_benford_MAD(os.path.join(TEST_DATA_DIR, "payments_50_"), 2, 2)

def test_compute_benford_MAD_6():
    helper_test_compute_benford_MAD(os.path.join(TEST_DATA_DIR, "payments_50000_"), 2, 1)

def test_compute_benford_MAD_7():
    helper_test_compute_benford_MAD(os.path.join(TEST_DATA_DIR, "payments_50000_"), 2, 2)



