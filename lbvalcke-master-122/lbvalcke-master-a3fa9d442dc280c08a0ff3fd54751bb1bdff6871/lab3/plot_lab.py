# CS121 Lab 3: Functions

import math
import numpy
import pylab

def sinc(x):
    '''
    Real valued sinc function  f(x) == sin(x)/x

    Inputs:
        x: float

    Return: float
    '''
    # Make sure we don't divide by zero  
    if x != 0:
        return math.sin(x) / x
    else:
        # sin(0) / 0 == 1
        return 1.0

    
def plot_func(xs, ys, title, xlab, ylab):            
    # plot the figure
    pylab.figure()
    pylab.plot(xs,ys)
    pylab.title(title)
    pylab.xlabel(xlab)
    pylab.ylabel(ylab)
    pylab.show()


def plot_sinc(left_boundary, right_boundary, dx, title, xlab, ylab):
    '''
    Plot the sinc function from from left_boundary...right_boundary
    with increments of size dx.
    '''
    xs = numpy.arange(left_boundary, right_boundary, dx) 

    # apply the sinc function onto the xs list
    ys = []
    for x in xs:
        ys.append(sinc(x))
    plot_func(xs, ys, title, xlab, ylab)

def go():
    dx = .01
    left_boundary = -10
    right_boundary = 10 
    title = "Sinc Values"
    xlab = "Inputs"
    ylab = "Outputs"
    plot_sinc(left_boundary, right_boundary, dx, title, xlab, ylab)


if __name__ == "__main__":
    go()


def square(x):
    x_sq = x ** 2
    return x_sq


def plot_square(left_boundary, right_boundary, dx, title, xlab, ylab):
    '''
    Plot the x^2 function from from left_boundary...right_boundary
    with increments of size dx.
    '''
    xs = numpy.arange(left_boundary, right_boundary, dx) 

    # apply the sinc function onto the xs list
    ys = []
    for x in xs:
        ys.append(square(x))
    plot_func(xs, ys, title, xlab, ylab)


