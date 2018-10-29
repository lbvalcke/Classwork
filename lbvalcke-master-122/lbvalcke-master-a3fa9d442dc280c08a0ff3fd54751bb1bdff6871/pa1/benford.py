# CS121: Benford's Law
#
# Luis Buenaventura Valcke

# Functions for evaluating data using Benford's Law.

import math
import os.path
import pylab as plt
import sys
import util

def extract_leading_digits(dollar_amount, num_digits):
    '''
    Given a dollar amount as a string and a number of digits, extract
    the specified number of leading digits

    Inputs:
        dollar_amount: string
        num_digits: the number of leading digits to extract from the
            amount.

    Returns:
        integer
    '''
    # Returns portion of string that represents amount
    str_amount = dollar_amount[1:]
    
    # Returns float from string
    num_amount = float(str_amount)
    
    # Returns leading digits
    return math.trunc(10 ** (-1 * math.floor(math.log10(num_amount)) + num_digits - 1) * num_amount)


def get_leading_digits_range(num_digits):
    '''
    Given a number of leading digits, returns the range of values
    for that number of leading digits

    Inputs:
        num_digits: the number of leading digits
    
    Returns:
       tuple
    '''
    # Lower bound and upper bound calculation
    lbound = 10 ** (num_digits - 1)
    ubound = 10 ** (num_digits)
    
    # Replace (0, 0) with an appropriate return value
    return (lbound, ubound)


def compute_expected_benford_dist(num_digits):
    '''
    Given a number of leading digits, returns the expected distribution
    for each value within the range of values for that number 
    of leading digits

    Inputs:
        num_digits: the number of leading digits
    
    Returns:
        list with expected distribution for each value within the 
            leading digit range   
    '''

    # Returns leading digit range
    digits_range = get_leading_digits_range(num_digits)
    
    # Creates empty list to populate with distribution proportions
    prop_list = []
    
    # Calculates expected proportions and appends them to list
    for n in range(min(digits_range) - 1, max(digits_range) - 1): 
        proportion = math.log10(1 + 1 / (n + 1))  
        prop_list.append(proportion)
    
    # Returns complete list
    return prop_list


def compute_benford_dist(dollar_amounts, num_digits):
    '''
    Given a list of dollar amounts and a number of digits,
    returns the benford distribution of the list
    
    Inputs:
        dollar_amounts: the list of dollar amounts used
            used to calculate benford distribution
        num_digits: the number of leading digits
    
    Returns:
        list with actual distribution for each value within the 
            leading digit range
    '''
    # Returns leading digit range
    digits_range = get_leading_digits_range(num_digits)
    
    # Extracts the values from the tuple
    max_range = max(digits_range)
    min_range = min(digits_range)
    
    # Finds length of list
    length_amounts = len(dollar_amounts)
    
    # Creates zero-valued list with length of the max value of digit range
    benford_list = [0] * max_range
    
    # Adds leading digit occurences to list
    for i in dollar_amounts:
        digit = extract_leading_digits(i, num_digits)
        benford_list[digit] = benford_list[digit] + 1
    
    # Cuts list down to relevant range
    benford_list = benford_list[min_range:max_range]
    
    # Divides every value by length
    benford_list[:] = [x / length_amounts for x in benford_list]
    
    # Returns benford distribution
    return benford_list


def compute_benford_MAD(dollar_amounts, num_digits):
    '''
    Given a list of dollar amounts and a number of digits,
    returns the MAD of the benford distribution of the list
    
    Inputs:
        dollar_amounts: the list of dollar amounts used
            used to calculate benford distribution
        num_digits: the number of leading digits
    
    Returns:
        the mean absolute difference (MAD) of the expected distribution
            and the actual distribution for the given data set
    '''

    # Creates empty list for MAD values
    MAD_list = [] 
    
    # Extracts leading digit range
    digits_range = get_leading_digits_range(num_digits)
    
    # Extracts min and max values from tuple
    max_range = max(digits_range)
    min_range = min(digits_range)
    
    # Calculates the range
    benford_range = max(digits_range) - min(digits_range)
    
    # Calculates actual and expected distribution to get MAD
    expected_dist = compute_benford_dist(dollar_amounts, num_digits)
    actual_dist = compute_expected_benford_dist(num_digits)
    for i, j in zip(expected_dist, actual_dist):
        ind_MAD = abs(i - j)
        MAD_list.append(ind_MAD)
    
    # Divides values by range of distribution
    MAD_list[:] = [x / benford_range for x in MAD_list]
    
    # Sums every value
    MAD = sum(MAD_list)
    
    # Returns total MAD value
    return MAD


################ Do not change the code below this line ################

def plot_benford_dist(dollar_amounts, num_digits):
    '''
    Plot the actual and expected benford distributions

    Inputs:
        dollar_amounts: a non-empty list of positive dollar amounts as
            strings
        num_digits: number of leading digits
    '''
    # The assert statement below will cause the program to fail with the error:
    #    num_digits must be greater than zero...
    # if num_digits less than or equal to zero.   It will have no
    # effect, if num_digits is greater than zero.

    assert num_digits > 0, \
        "num_digits must be greater than zero {:d}".format(num_digits)

    n = len(dollar_amounts)

    # The assert statement below will fail with the error:
    #    "dollar_amounts must be a non-empty list"
    # if dollar_amounts is an empty list.
    assert n > 0, \
        "dollar_amounts must be a non-empty list"

    # compute range of leading digits
    (lb, ub) = get_leading_digits_range(num_digits)
    digits = range(lb,ub)

    # start a new figure
    f = plt.figure()

    # plot expected distribution
    expected = compute_expected_benford_dist(num_digits)
    plt.scatter(digits, expected, color="red", zorder=1)

    # plot actual distribution
    actual = compute_benford_dist(dollar_amounts, num_digits)
    plt.bar(digits, actual, align="center", color="blue", zorder=0)

    # set hash marks for x axis.
    plt.xticks(range(lb, ub, lb))

    # compute limits for the y axis
    max_val = max(max(expected), max(actual))
    y_ub = max_val * 1.1
    plt.ylim(0,y_ub)

    # add labels
    plt.title("Actual (blue) and expected (red) Benford distributions")
    if num_digits ==1: 
        plt.xlabel("Leading digit")
    else:
        plt.xlabel("Leading digits")
    plt.ylabel("Proportion")

    # show the plot
    plt.show()


def go():
    usage = "usage: python benford.py <input filename> <column number>  <num digits>"
    if len(sys.argv) != 4:
        print(usage)
    else:
        input_filename = sys.argv[1]
        if not os.path.isfile(input_filename):
            print(usage)
            print("error: file not found: {}".format(input_filename))
            return

        # convert column number argument to an integer
        try:
            col_num = int(sys.argv[2])
        except ValueError:
            s = "error: column number must be an integer: {}"
            print(usage)
            print(s.format(sys.argv[2]))
            return

        data = util.read_column_from_csv(input_filename, col_num, True)

        # convert number of digits argument to an integer
        try:
            num_digits = int(sys.argv[3])
        except ValueError:
            s = "error: number of digits must be an integer: {}".format(sys.argv[3])
            print(usage)
            print(s.format(sys.argv[3]))
            return

        plot_benford_dist(data, num_digits)

        # print only four digits after the decimal point
        print("MAD: {:.4}".format(compute_benford_MAD(data, num_digits)))

if __name__=="__main__":
    go()
