def f(x):
    '''
    Real valued square function  f(x) == x^2
    '''

    return x*x


<<<<<<< HEAD
def integrate(lb, ub, steps):
=======
def integrate():
>>>>>>> 79ace3309267f29e028e155209d8a072a85de3ad
    # Your code here
    # decide on the number of rectangles
    # compute the width of the rectangles
    # use a loop to compute the total area
    # return the value of totalArea
    # remove the next line
<<<<<<< HEAD
    totalArea = 0 
    width = (ub - lb)/steps
    for i in range(0, steps):
        upper_step = width * (i+1)
        lower_step = width * (i)
        upper_eval = upper_step ** 2
        lower_eval = lower_step ** 2
        avg_eval = (upper_eval + lower_eval)/2
        area = (avg_eval) * width
        totalArea = totalArea + area
        print(totalArea)
    
    return print(totalArea)
    pass
=======
    pass
>>>>>>> 79ace3309267f29e028e155209d8a072a85de3ad
