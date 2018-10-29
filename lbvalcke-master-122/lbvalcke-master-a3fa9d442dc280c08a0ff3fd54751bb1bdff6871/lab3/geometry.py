# CS121 Lab 3: Functions

import math

# Your distance function goes here 
def dist(x1, y1, x2, y2):
    '''
    Real valued distance function  f(x1,y1,x2,y2) == ((x1-x2)**2 + (y1-y2)**2)**0.5

    Inputs:
        x1: float
        y1: float
        x2: float
        y2: float

    Return: float
    '''
    x_range = x1 - x2
    y_range = y1 - y2 
    x_sq = x_range ** 2
    y_sq = y_range ** 2
    distance = math.sqrt(x_sq + y_sq)

    return distance

# Your perimeter function goes here 
def perimeter(x1, y1, x2, y2, x3, y3):
    '''
    Real valued perimeter function  f(x1,y1,x2,y2,x3,y3) == sum of distances

    Inputs:
        x1: float
        y1: float
        x2: float
        y2: float
        x3: float
        y3: float

    Return: float
    '''
    p1 = dist(x1, y1, x2, y2)
    p2 = dist(x2, y2, x3, y3)
    p3 = dist(x1, y1, x3, y3)
    peri = p1 + p2 + p3

    return peri

def go():
    '''
    Write a small amount of code to verify that your functions work

    Verify that the distance between the points (0, 1) and (1, 0) is
    close to math.sqrt(2)

    After that is done, verify that the triangle 
    with vertices at (0, 0), (0, 1), (1, 0) has 
    a perimeter 2 + math.sqrt(2)
    '''

    # replace the pass with code that calls your functions
    # and prints the results
    x1 = 0
    y1 = 1
    x2 = 1
    y2 = 0
    x3 = 0
    y3 = 0

    result = perimeter(x1,y1,x2,y2,x3,y3)
    print(result)


if __name__ == "__main__":
    go()
    
                

