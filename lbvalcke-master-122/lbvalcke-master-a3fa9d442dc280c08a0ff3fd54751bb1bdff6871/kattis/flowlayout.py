import sys

# Skeleton code for problem https://uchicago.kattis.com/problems/flowlayout
#
# Make sure you read the problem before editing this code.
#
# You should focus only on implementing the solve() function.
# Do not modify any other code.

# This function takes two parameters:
#
#  - max_width: The maximum width of the window
#  - rectangles: A list of pairs. Each pair contains two integers:
#                the width and height of a rectangle
#
# You must return the width and height of the resulting window.
def solve(max_width, rectangles):
    # YOUR CODE HERE
    width = 0
    height_index = 0 
    dimension = []
    for i, rectangle in enumerate(rectangles):
        if rectangle[0] <= max_width:    
            if dimension == []:
                dimension = [rectangle[0], rectangle[1]]
                width = rectangle[0]
                height_index = i
            elif dimension[0] + rectangle[0] <= max_width:
                dimension[0] = dimension[0] + rectangle[0]
                if dimension[0] > width:
                    width = dimension[0]
                if rectangle[1] - rectangles[height_index][1] > 0:
                    dimension[1] += rectangle[1] - rectangles[height_index][1]
                    height_index = i
            elif dimension[0] + rectangle[0] > max_width:
                dimension = [rectangle[0], rectangle[1] + dimension[1]]
                height_index = i 
                if dimension[0] > width:
                    width = dimension[0]                

    # Replace 0, 0 with the width and height of the resulting window.
    return width, dimension[1]


if __name__ == "__main__":
    tokens = sys.stdin.read().strip().split()

    width = int(tokens.pop(0))
    while width != 0:
        rectangles = []
        rwidth = int(tokens.pop(0))
        rheight = int(tokens.pop(0))
        while rwidth != -1 and rheight != -1:
            rectangles.append( (rwidth, rheight) )
            rwidth = int(tokens.pop(0))
            rheight = int(tokens.pop(0))
            
        w, h = solve(width, rectangles)
        print("{} x {}".format(w, h))

        width = int(tokens.pop(0))
