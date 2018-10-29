#!/usr/bin/python3

import sys

# Skeleton code for problem https://uchicago.kattis.com/problems/uchicago.shortmanhattan
#
# Make sure you read the problem before editing this code.
#
# You should focus only on implementing the find_paths() function.  Do not
# modify any other code.

# This function takes four parameters: x0, y0, x1, y1 (as defined
# in the problem statement)
#
# The function must return a list of all the shortest paths from (x0,y0) to
# (x1, y1). For example:
#
#    find_paths(0,0,1,1) would return [["right", "up"], ["up", "right"]]
#    find_paths(1,1,0,0) would return [["left", "down"], ["down", "left"]]
#
# Note: The order of the paths is not important. e.g., the first call could
#       return [["up", "right"], ["right", "up"]] and it would also be correct.
#
# Note (2): If there are no shortest paths (because you're finding the path from
#           one point to itself, the function must return [[]] (i.e., a list with
#           just one path: the empty path.
def find_paths(x0,y0,x1,y1):
    # your code goes here

    x_len = x0 - x1 
    y_len = y0 - y1

    if x_len == 0 and y_len == 0:
        return [[]]
    else: 
        if x_len == 0:            
            if y_len > 0:
                return [["down"] + path for path in find_paths(x0, y0-1, x1, y1)]  
            else: 
                return [["up"] + path for path in find_paths(x0, y0+1, x1, y1)]
        elif y_len == 0:
            if x_len > 0:
                return [["left"] + path for path in find_paths(x0-1, y0, x1, y1)]
            else: 
                return [["right"] + path for path in find_paths(x0+1, y0, x1, y1)]
        else:
            if y_len > 0:
                y_dir = [["down"] + path for path in find_paths(x0, y0-1, x1, y1)]
            else: 
                y_dir = [["up"] + path for path in find_paths(x0, y0+1, x1, y1)]

            if x_len > 0:
                x_dir = [["left"] + path for path in find_paths(x0-1, y0, x1, y1)]
            else: 
                x_dir = [["right"] + path for path in find_paths(x0+1, y0, x1, y1)]
            return x_dir + y_dir

### The following code handles the input and output tasks for
### this problem.  Do not modify it!

if __name__ == "__main__":
    x0, y0, x1, y1 = sys.stdin.read().split()

    paths = find_paths(int(x0), int(y0), int(x1), int(y1))

    if len(paths) == 1 and len(paths[0]) == 0:
        print("NONE")
    else:
        for p in paths:
            print(" ".join(p))

    
