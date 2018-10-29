# CS121 Linear regression
#
<<<<<<< HEAD
# Luis Buenaventura 438954
=======
# YOUR NAME
>>>>>>> 773dcd3fdb9e1695ebc8bfcf1f2696415922ed23

import numpy as np
from asserts import assert_Xy, assert_Xbeta

# because Guido van Rossum hates functional programming
# http://www.artima.com/weblogs/viewpost.jsp?thread=98196
from functools import reduce


#############################
#                           #
#  Our code: DO NOT MODIFY  #
#                           #
#############################


def prepend_ones_column(A):
    '''
    Add a ones column to the left side of an array

    Inputs: 
        A: a numpy array

    Output: a numpy array
    '''
    ones_col = np.ones((A.shape[0], 1))
    return np.hstack([ones_col, A])


def linear_regression(X, y):
    '''
    Compute linear regression. Finds model, beta, that minimizes
    X*beta - Y in a least squared sense.

    Accepts inputs with type array
    Returns beta, which is used only by apply_beta

    Examples
    --------
    >>> X = np.array([[5, 2], [3, 2], [6, 2.1], [7, 3]]) # predictors
    >>> y = np.array([5, 2, 6, 6]) # dependent
    >>> beta = linear_regression(X, y)  # compute the coefficients
    >>> beta
    array([ 1.20104895,  1.41083916, -1.6958042 ])
    >>> apply_beta(beta, X) # apply the function defined by beta
    array([ 4.86363636,  2.04195804,  6.1048951 ,  5.98951049])
    '''
    assert_Xy(X, y, fname='linear_regression')

    X_with_ones = prepend_ones_column(X)

    # Do actual computation
    beta = np.linalg.lstsq(X_with_ones, y)[0]

    return beta


def apply_beta(beta, X):
    '''
    Apply beta, the function generated by linear_regression, to the
    specified values

    Inputs:
        model: beta as returned by linear_regression
        Xs: 2D array of floats

    Returns:
        result of applying beta to the data, as an array.

        Given:
            beta = array([B0, B1, B2,...BK])
            Xs = array([[x11, x12, ..., x0K],
                        [x21, x22, ..., x1K],
                        ...
                        [xN1, xN2, ..., xNK]])

            result will be:
            array([B0+B1*x11+B2*x12+...+BK*x1K,
                   B0+B1*x21+B2*x22+...+BK*x2K,
                   ...
                   B0+B1*xN1+B2*xN2+...+BK*xNK])
    '''
    assert_Xbeta(X, beta, fname='apply_beta')

    # Add a column of ones
    X_incl_ones = prepend_ones_column(X)

    # Calculate X*beta
    yhat = np.dot(X_incl_ones, beta)
    return yhat


def read_file(filename):
    '''
    Read data from the specified file.  Split the lines and convert
    float strings into floats.  Assumes the first row contains labels
    for the columns.

    Inputs:
      filename: name of the file to be read

    Returns:
      (list of strings, 2D array)
    '''
    with open(filename) as f:
        labels = f.readline().strip().split(',')
        data = np.loadtxt(f, delimiter=',', dtype=np.float64)
        return labels, data


###############
#             #
#  Your code  #
#             #
###############


<<<<<<< HEAD
def data_selector(filename, predictor_var_indices, dependent_var_index):
    '''
    Read data from the specified file and breaks data down into independent,
    dependent, and label sets.

    Inputs:
      filename: name of the file to be read
      predictor_var_indices: index values of predictor variable_separator
      dependent_var_index: index of dependent variable

    Returns:
      arrays for labels, independent variables, and dependent variables
    '''
    labels, dataset = read_file(filename)
    pre_dataset = dataset[:, predictor_var_indices]
    result_dataset = dataset[:, dependent_var_index]

    return labels, pre_dataset, result_dataset


def variable_separator(pre_dataset):
    '''
    Breaks apart independent variable array into a list of arrays
    where each array represents one variable variable 

    Inputs:
      pre_dataset: independent variable array

    Returns:
      list of arrays
    ''' 
    separated_var = np.transpose(pre_dataset).tolist()
    
    return separated_var


def y_hat(pre_dataset, result_dataset):
    '''
    Calculates beta coefficients to then calculate y_har values to
    help calculate r_2
    Inputs:
      pre_dataset: independent variable array
      result_dataset: dependent variable array

    Returns:
      result of applying beta as an array
    ''' 
    beta = linear_regression(pre_dataset, result_dataset)
    y_hat = apply_beta(beta, pre_dataset)
    
    return y_hat


def var(data): 
    '''
    Calculates the variance of a set as a sum of squares
    Inputs:
      data: array of numeric values

    Returns:
      float representing the variance of the array
    ''' 
    data_bar = np.mean(data)
    n = len(data)
    total_var = np.square(data - data_bar)
    sum_var = sum(total_var)
    var = sum_var / n
    
    return var


def var_hat(predicted, actual):
    '''
    Calculates the sum of squares between y_hat and the actual results
    Inputs:
      predicted: an array with y_hat values
      actual: the result_dataset array

    Returns:
      float representing the variance between the two arrays
    ''' 
    error = np.subtract(actual, predicted)
    error_sq = np.square(error)
    sum_error = sum(error_sq)
    n = len(predicted)
    var_hat = sum_error / n
    
    return var_hat


def r_sq(var, var_hat): 
    '''
    Calculates the r_2 by using the calculated variances
      var: variance of the result_dataset
      var_hat: the sum of squares between the y_hat values and the 
      result_dataset

    Returns:
      float representing the calculated r_2
    ''' 
    r_sq = 1 - var_hat / var
    
    return r_sq


def rsq_processing(array, result_dataset):
    '''
    Consolidates the functions used to calculate r_2
    Inputs:
      array: independent variables array
      result_dataset: the result_dataset array
      variance: variance of the result_dataset

    Returns:
      float representing r_2
    ''' 
    variance = var(result_dataset)
    predictions = y_hat(array, result_dataset)
    #calculates the variance of the y_hats
    array_var_hat = var_hat(predictions, result_dataset)
    r_square = r_sq(variance, array_var_hat)

    return r_square


def test_rsq(y_hat, result_dataset):
    '''
    Uses the y_hats from a trained regression model applied to the 
    test dataset to calculate r_square 

    Inputs:
      y_hat: y_hat values calculated by applying betas to test
      dataset
      result_dataset: the result_dataset array
      variance: variance of the result_dataset

    Returns:
      float representing r_2
    '''   
    variance = var(result_dataset)  
    #caculates variance of the test data set
    array_var_hat = var_hat(y_hat, result_dataset)
    r_square = r_sq(variance, array_var_hat)

    return r_square


def top_var(pre_dataset, result_dataset):
    '''
    Finds the r_2 the model created by using each individual 
    independent variable and returns the highest r_2 and index

    Inputs:
      y_hat: y_hat values calculated by applying betas to test
      dataset
      result_dataset: the result_dataset array
      variance: variance of the result_dataset

    Returns:
      float representing r_2
    '''
    #sets the highest r_2 counter to 0
    highest_rsq = 0
    #separates the array into a list of arrays
    var_sep_array = variable_separator(pre_dataset)
    
    for i, array in enumerate(var_sep_array): 
        array = np.array(array)
        #reshapes each 1-d array into a 2-d array
        array = np.reshape(array, (-1,1))
        r_square = rsq_processing(array, result_dataset)
        if r_square > highest_rsq:  
                    #keeps track of the highest r_2 and index
                    highest_rsq = r_square
                    highest_index = i
        else: 
            pass

    return (highest_index, highest_rsq)


def r_sq_table(pre_dataset, result_dataset):
    '''
    Calculates the r_sq of each independent variable
    and saves the tuple of label index and r_2 to a list
    Inputs:
      pre_dataset: independent variable array
      result_dataset: dependent variable array

    Returns:
      list of tuples with each tuple holding index and r_2
    '''    
    table = []
    var_sep_array = variable_separator(pre_dataset)
    
    #adds a tuple to the list for each variable with
    #the respective index and r_2 of the one variable regression
    for i, array in enumerate(var_sep_array): 
        array = np.array(array)
        array = np.reshape(array, (-1,1))
        r_square = rsq_processing(array, result_dataset)
        table_row = (i, r_square) 
        table.append(table_row)
    
    return table


def r_sq_all(pre_dataset, result_dataset):
    '''
    Finds the r_2 value of a regression model which uses all of 
    the independent variables
    Inputs:
      pre_dataset: independent variable array
      result_dataset: dependent variable array

    Returns:
      float representing r_2 of the regression model
    '''

    r_square = rsq_processing(pre_dataset, result_dataset)
            
    return r_square


def r_sq_pair(pre_dataset, result_dataset):
    '''
    Finds the r_2 value of pair of independent variables
    that lead to the highest r_2
    Inputs:
      pre_dataset: independent variable array
      result_dataset: dependent variable array

    Returns:
      tuple with the indexes of the best pair and the r_2 values
    '''    
    
    highest_rsq = 0
    var_sep_array = variable_separator(pre_dataset)
    
    #attempts to build regression models from all unique pairs
    #of variables and returns the highest r_2 found 
    for i, array_1 in enumerate(var_sep_array):
        for j, array_2 in enumerate(var_sep_array): 
            if i < j:
                array = np.column_stack((array_1, array_2))
                r_square = rsq_processing(array, result_dataset)
                
                if r_square > highest_rsq: 
                    highest_rsq = r_square 
                    highest_pair = (i, j)
            else: 
                pass
    
    return (highest_pair, highest_rsq)


def top_k_var(max_k, pre_dataset, result_dataset, threshold = 0):
    '''
    Finds the r_2 values created by incrementally adding additional variables
    to the regression model based on the variable which will increase r_2
    the most - where k is a bound on the number of variables in the model
    and threshold stops the calculation if the additional var does not add
    enough to r_2
    Inputs:
      max_k: the maximum number of variables allowed in the model
      pre_dataset: independent variable array
      result_dataset: dependent variable array
      threshold: the minimum incremental r_2 a variable needs to add
      to be added to the model

    Returns:
      k_tuple: the incremental label index of the the model and the associated r_2
      k_vars: the indexes of the variables in the regression model
    '''
    #finds the top var in the k = 1 case
    highest_index, highest_rsq = top_var(pre_dataset, result_dataset)
    #sets the initial r_2 difference to the r_2 of the top var regression model
    r_sq_diff = top_var(pre_dataset, result_dataset)[1]
    
    var_sep_array = variable_separator(pre_dataset)
    top_var_array = var_sep_array[highest_index]
    
    #keeps track of the indexes of the variables used
    k_vars = []
    #keeps track of the indexes and r_2 of the variables used
    k_tuple = []
    k_count = 0
    
    #assures that the incremental r_2 change is greater than the threshold
    #and assures that the loop is within the K variable boundary
    while r_sq_diff > threshold and k_count < max_k:
        k_vars.append(highest_index)

        k_tuple.append((highest_index, highest_rsq))

        k_count += 1    
        highest_index = 0
        #preserves the previous r_2 value to see if the incremental variable
        #adds more than the threshold
        highest_rsq_prev = highest_rsq
        
        #continues testing additional variables until 
        #at least one of the conditions in the loop occurs
        for i, next_array in enumerate(var_sep_array):
            if i not in k_vars:
                test_array = np.column_stack((top_var_array, next_array))
                r_square = rsq_processing(test_array, result_dataset)

                if r_square > highest_rsq:
                    highest_rsq = r_square
                    highest_index = i
        
        r_sq_diff = highest_rsq - highest_rsq_prev
        #defines the currect independent variable array with the incremental variables
        top_var_array = np.column_stack((top_var_array, var_sep_array[highest_index]))

    return k_tuple, k_vars


def r_2_test_data(max_k, train_pre_dataset, train_result_dataset, test_pre_dataset, test_result_dataset):
    '''
    Uses the top_k_var function to incrementally calculate top k variables to be used 
    for fitting the model. Fits the model according to the train array.
    Uses the resulting beta coefficients to the calculate y_hats and
    uses the y_hats to calculate the r_2 for model on the test result array.
    Inputs:
      max_k: the maximum number of variables allowed in the model
      train_pre_dataset: independent variable array from training set
      train_result_dataset: dependent variable array from training set
      test_pre_dataset: independent variable array from testing set
      test_result_dataset: dependent variable array from testing set

    Returns:
      list of tuples with the index of the added variable and the resulting r_2
    '''
    k_tuple, k_vars = top_k_var(max_k, train_pre_dataset, train_result_dataset)
    #defines the training array
    train_var_sep_array = variable_separator(train_pre_dataset)
    #defines the testing array 
    test_var_sep_array = variable_separator(test_pre_dataset)

    r_square_list = []

    start = k_vars[0]
    #reshapes the 1d arrays to 2d arrays
    train_relevant_array = train_var_sep_array[start]
    train_relevant_array_one = np.reshape(train_relevant_array, (-1,1))
    test_relevant_array = test_var_sep_array[start]
    test_relevant_array_one = np.reshape(test_relevant_array, (-1,1))
    
    #calculates the r_2 made by applying the trained regression on the
    #test dataset in the k = 1 case
    beta = linear_regression(train_relevant_array_one, train_result_dataset)
    y_hat = apply_beta(beta, test_relevant_array_one)
    r_square = test_rsq(y_hat, test_result_dataset)
    r_square_list.append((start, r_square))
    
    #calculates the subsequent r_2 in the N >= max_k > k > 1 cases
    if len(k_vars) > 1:
        for k in k_vars[1:]:
            train_relevant_array = np.column_stack((train_relevant_array, train_var_sep_array[k]))
            test_relevant_array = np.column_stack((test_relevant_array, test_var_sep_array[k]))

            beta = linear_regression(train_relevant_array, train_result_dataset)
            y_hat = apply_beta(beta, test_relevant_array)
            r_square = test_rsq(y_hat, test_result_dataset)
            r_square_list.append((k, r_square))

    return r_square_list, beta


def format_task1(data_name, labels, pre_dataset, result_dataset):
    '''
    Applies r_sq_table to calculate the r_2 of each independent variable for task 1a
    and applies r_sq_all to calculate r_2 of all the independent variables together
    Inputs: 
      data_name: the name of the dataset (e.g. "city")
      labels: the labels of each column of the dataset
      pre_dataset: the array of independent variables
      result_dataset: the array of the dependent variable

    Returns:
      Prints the results for task 1
    '''
    table = r_sq_table(pre_dataset, result_dataset)
    rsq_allvar = r_sq_all(pre_dataset, result_dataset)
    #task 1a
    #formats the list on a line by line basis while printing lines
    print(str(data_name) + " Task 1a:")
    for row in table:
        print(str(labels[row[0]]) + ": " + str(round(row[1], 2)))
    
    #merges all the labels together in preparation of task 1b
    all_labels = str(labels[0])
    for label in labels[1:len(labels) - 1]:
        all_labels = all_labels + ", " + str(label)

    #task 1b
    #prints the merged labels along with the r_2 for the regression with all ind var
    print('\n')
    print('\n')
    print(str(data_name) + " Task 1b:")
    print(all_labels + " R2:" + str(round(rsq_allvar, 2)))  


def format_task2(data_name, labels, pre_dataset, result_dataset):
    '''
    Applies r_sq_pair to calculate the r_2 of the best independent variable pair for task 2
    Inputs: 
      data_name: the name of the dataset (e.g. "city")
      labels: the labels of each column of the dataset
      pre_dataset: the array of independent variables
      result_dataset: the array of the dependent variable

    Returns:
      Prints the results for task 2
    '''
    best_pair = r_sq_pair(pre_dataset, result_dataset)
    
    #task 2
    #formats the results of the best pair
    print('\n')
    print('\n')
    print(str(data_name) + " Task 2:")
    print(str(labels[best_pair[0][0]]) + ", " + str(labels[best_pair[0][1]]) + " R2:" + str(round(best_pair[1], 2))) 


def format_task3(data_name, max_k, threshold1, threshold2, labels, pre_dataset, result_dataset):
    '''
    Uses format_task3a and format_task3b to print the results for task 3
    Inputs: 
      data_name: the name of the dataset (e.g. "city")
      max_k: the max k number of variables
      threshold1: the first threshold used for task 3b
      threshold2: the second threshold used for task 3b
      labels: the labels of each column of the dataset
      pre_dataset: the array of independent variables
      result_dataset: the array of the dependent variable

    Returns:
      Prints the results for task 2
    '''
    format_task3a(data_name, max_k, labels, pre_dataset, result_dataset)
    format_task3b(data_name, max_k, threshold1, threshold2, labels, pre_dataset, result_dataset)    


def format_task3a(data_name, max_k, labels, pre_dataset, result_dataset):
    '''
    Uses top_k_var with no thresholds to create a table of 1 <= K <= N variables with the incremental
    variable added and the associated r_2 
    Inputs: 
      data_name: the name of the dataset (e.g. "city")
      max_k: the max k number of variables
      labels: the labels of each column of the dataset
      pre_dataset: the array of independent variables
      result_dataset: the array of the dependent variable

    Returns:
      Prints the results for task 3a
    '''
    k_tuple, k_vars = top_k_var(max_k, pre_dataset, result_dataset, threshold = 0)
    
    #formats and prints the tuples on a tuple by tuple basis from the list for task 3a
    label_tuple = []
    print('\n')
    print('\n')
    print(str(data_name) + " Task 3a:")
    for pair in k_tuple:
        if label_tuple == []:
            label_tuple.append((str(labels[pair[0]]), round(pair[1], 2)))
            print(str(label_tuple[0][0]) + " R2:" + str(label_tuple[0][1]))
        else:
            label_tuple.append((str(label_tuple[len(label_tuple) - 1][0]) + ", " + str(labels[pair[0]]), round(pair[1], 2)))
            print(str(label_tuple[len(label_tuple) - 1][0]) + " R2:" + str(label_tuple[len(label_tuple) - 1][1]))

            
def format_task3b(data_name, max_k, threshold1, threshold2, labels, pre_dataset, result_dataset):
    '''
    Uses top_k_var with one of two threshold bounds to print the results for task 3b
    Inputs: 
      data_name: the name of the dataset (e.g. "city")
      max_k: the max k number of variables
      threshold1: the first threshold used for task 3b
      threshold2: the second threshold used for task 3b
      labels: the labels of each column of the dataset
      pre_dataset: the array of independent variables
      result_dataset: the array of the dependent variable

    Returns:
      Prints the results for task 3b
    '''
    #intializes the tuples for each threshold input for task 3b
    k_tuple_t1, k_vars_t1 = top_k_var(max_k, pre_dataset, result_dataset, threshold1)
    k_tuple_t2, k_vars_t2 = top_k_var(max_k, pre_dataset, result_dataset, threshold2)
    
    print('\n')
    print('\n')
    print(str(data_name) + " Task 3b:")

    label_tuple = []
    
    #prints the tuples on a tuple by tuple basis for threshold 1
    for pair in k_tuple_t1:
        if label_tuple == []:
            label_tuple.append((str(labels[pair[0]]), round(pair[1], 2)))
        else:
            label_tuple.append((str(label_tuple[len(label_tuple) - 1][0]) + ", " + str(labels[pair[0]]), round(pair[1], 2)))
    
    print("Threshold " + str(threshold1) + ": " + str(label_tuple[len(label_tuple) - 1][0]) + " R2:" + str(label_tuple[len(label_tuple) - 1][1]))

    label_tuple = []
    
    #prints the tuples on a tuple by tuple basis for threshold 2
    for pair in k_tuple_t2:
        if label_tuple == []:
            label_tuple.append((str(labels[pair[0]]), round(pair[1], 2)))
        else:
            label_tuple.append((str(label_tuple[len(label_tuple) - 1][0]) + ", " + str(labels[pair[0]]), round(pair[1], 2)))
    
    print("Threshold " + str(threshold2) + ": " + str(label_tuple[len(label_tuple) - 1][0]) + " R2:" + str(label_tuple[len(label_tuple) - 1][1]))


def format_task4(data_name, max_k, train_pre_dataset, train_result_dataset, test_pre_dataset, test_result_dataset, labels):
    '''
    Uses the top_k_var function to incrementally calculate top k variables to be used 
    for fitting the model. Fits the model according to the train array.
    Uses the resulting beta coefficients to the calculate y_hats and
    uses the y_hats to calculate the r_2 for model on the test result array.
    Does this for each 1 <= K <= N and prints a table with the associated variable names in the models
    Inputs:
      max_k: the maximum number of variables allowed in the model
      train_pre_dataset: independent variable array from training set
      train_result_dataset: dependent variable array from training set
      test_pre_dataset: independent variable array from testing set
      test_result_dataset: dependent variable array from testing set

    Returns:
      list of tuples with the index of the added variable and the resulting r_2
    '''
    #calls the function to product the list of tuples of incremental variables
    #from the test data set
    r_2_table = r_2_test_data(max_k, train_pre_dataset, train_result_dataset, test_pre_dataset, test_result_dataset)

    label_tuple = []

    print('\n')
    print('\n')
    print(str(data_name) + " Task 4:")
    
    #prints the tuple on a tuple by tuple basis
    for pair in r_2_table:
        if label_tuple == []:
            label_tuple.append((str(labels[pair[0]]), round(pair[1], 2)))
            print(str(label_tuple[0][0]) + " R2:" + str(label_tuple[0][1]))
        else:
            label_tuple.append((str(label_tuple[len(label_tuple) - 1][0]) + ", " + str(labels[pair[0]]), round(pair[1], 2)))
            print(str(label_tuple[len(label_tuple) - 1][0]) + " " + str(label_tuple[len(label_tuple) - 1][1]))
=======
>>>>>>> 773dcd3fdb9e1695ebc8bfcf1f2696415922ed23
