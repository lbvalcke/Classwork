import numpy as np
import sys

# import linear regression and apply beta from PA #5.
sys.path.append("../pa5")
from model import linear_regression

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

def var(y):
    # replace 0.0 with proper return value
<<<<<<< HEAD
    y_bar = np.mean(y)
    n = len(y)
    total_var = np.square(y - y_bar)
    sum_var = sum(total_var)
    var = sum_var / n
    return var
=======
    return 0.0
>>>>>>> 773dcd3fdb9e1695ebc8bfcf1f2696415922ed23


def task2(b):
    ### Replace 0.0 with code to extract the desired slice
    print("rows 0, 1, and 2.")
<<<<<<< HEAD
    print(b[[0, 1, 2],:])
    print()
    print("rows 0, 1, and 5")
    print(b[[0, 1, 5],:])
    print()
    print("columns 0, 1, and 2")
    print(b[:, [0, 1, 2]])
    print()
    print("columns 0, 1, and 3")
    print(b[:, [0, 1, 3]])
    print()
    print("columns 0, 1, and 2 from rows 2 and 3.")
    print(b[[2, 3],:][:,[0, 1, 2]])
=======
    print(0.0)
    print()
    print("rows 0, 1, and 5")
    print(0.0)
    print()
    print("columns 0, 1, and 2")
    print(0.0)
    print()
    print("columns 0, 1, and 3")
    print(0.0)
    print()
    print("columns 0, 1, and 2 from rows 2 and 3.")
    print(0.0)
>>>>>>> 773dcd3fdb9e1695ebc8bfcf1f2696415922ed23
    print()

def go():
    city_col_names, city_data = read_file("../pa5/data/city/training.csv")

    graffiti = city_data[:,0]
    garbage = city_data[:,3]

    print("Task 1")
    print("GRAFFITI:", var(graffiti))
    print("GARBAGE:", var(garbage))
    print()
    print()


    print("Task 2")
    b = (np.arange(24)**2).reshape(6,4)
    task2(b)


    print("Task 3")
    ### REPLACE 0.0 with appropriate call to linear regression
<<<<<<< HEAD
    print("Rodents, Garbage => Crime", linear_regression(city_data[:,[2, 3]], city_data[:,7]))
=======
    print("Rodents, Garbage => Crime", 0.0)
>>>>>>> 773dcd3fdb9e1695ebc8bfcf1f2696415922ed23
    print()
    print()


    print("Task 4")
    ### REPLACE 0.0 with appropriate call to linear regression
<<<<<<< HEAD
    print("Graffiti => Crime:", linear_regression(city_data[:,[0]], city_data[:,7]))
=======
    print("Graffiti => Crime:", 0.0)
>>>>>>> 773dcd3fdb9e1695ebc8bfcf1f2696415922ed23
    print()
    print()

if __name__ == "__main__":
    go()
