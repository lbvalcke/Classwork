import math
import pylab
import numpy


def sinc(x):
    if x != 0:
        return math.sin(x) / x
    else:
        return 1


def plot_sinc():
    # Compute Xs using range or numpy.arange
    # Compute Ys using a loop
    # Call plot
    # Call show
    # remove the next line
<<<<<<< HEAD
   X = list(range(-10, 11))
   Y = []
   for n in X:
       y = sinc(n)
       Y.append(y)
   pylab.plot(X, Y)
   pylab.show(pylab.plot(X, Y))
   pass

def plot_sinc_2(step):
    # Compute Xs using range or numpy.arange
    # Compute Ys using a loop
    # Call plot
    # Call show
    # remove the next line
   X = list(numpy.arange(-10, 10.1, step))
   Y = []
   for n in X:
       y = sinc(n)
       Y.append(y)
   pylab.plot(X, Y)
   pylab.show(pylab.plot(X, Y))
   pass
=======
    pass
>>>>>>> 79ace3309267f29e028e155209d8a072a85de3ad
