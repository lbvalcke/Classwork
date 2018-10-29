#!/usr/bin/python

import sys

# Skeleton code for problem https://uchicago.kattis.com/problems/uchicago.mpcs.minesweeper
#
# Make sure you read the problem before editing this code.
#
# You should focus only on implementing the solve() function.  Do not
# modify any other code.

# This function takes a one parameter: a list of lists of integers
# (representing a matrix, i.e., the minefield).  A 1 means that 
# the spot contains a mine and a zero indicates that it
# does not.  You must return a list of lists of integers representing
# a field of the same dimensions, but where each spot
# should contain either -1, meaning that the spot holds a mine, or a
# value that is >= 0, which is a count of the number of mines in
# adjacent spots.

def solve(field):
    # Your code here
    y_list = list(range(len(field)))
    x_list = list(range(len(field[1])))
    mine_dict = {}
    neighbor_dict = {}
    neighbor_list = []
    neighbors_list = []
    
    for i, x in enumerate(x_list):
        for j, y in enumerate(y_list):
            location = (x_list[i], y_list[j])
            if field[j][i] == 1:
                mine_dict[location] = "X"
            else:    
                mine_dict[location] = field[j][i]
    
    for i, x in enumerate(x_list):
        for j, y in enumerate(y_list):
            location = (x_list[i], y_list[j])
            neighbor_dict[location] = 0

    for i, x in enumerate(x_list):
        for j, y in enumerate(y_list):
            location = (x_list[i], y_list[j])
            neighbor_list = [(x_list[i] + 1, y_list[j]), (x_list[i] - 1, y_list[j]), (x_list[i], y_list[j] + 1), (x_list[i], y_list[j] - 1), (x_list[i] + 1, y_list[j] + 1), (x_list[i] -1, y_list[j] - 1)]
            neighbor_list = [x for x in neighbor_list if x[0] >= 0 and x[1] >= 0]
            neighbors_list.append(neighbor_list)    
    
    for i, x in enumerate(x_list):
        for j, y in enumerate(y_list):
            location = (x_list[i], y_list[j])
            neighbor_dict[location] = neighbors_list[x_list[i]][y_list[i]]
    print(neighbor_dict)

    mines = 0

    for key in mine_dict: 
        mines = 0
        print(key)
        if mine_dict[key] == 0:
            for neighbor in neighbor_dict[key]:
                if mine_dict[neighbor] != "X":
                    pass
                elif mine_dict[neighbor] == "X":
                    mines += 1
            if mines == 0:
                mine_dict[key] = "-"
            if mines > 0:
                mine_dict[key] = str(mines)
    


    print(mine_dict)
    # Replace [] with a list of lists representing the solved minefield
    return []

def result_to_str(field):
    result_str = ""
    for row in field:
        s = ""
        for v in row:
            if v == -1:
                s += "X"
            elif v == 0:
                s += "-"
            else:
                s += str(v)
        result_str += s + "\n"

    return result_str

if __name__ == "__main__":
    tokens = sys.stdin.read().strip().split()

    x = int(tokens.pop(0))
    y = int(tokens.pop(0))

    field = []

    for i in range(x):
        row = []
        for j in range(y):
            row.append(int(tokens.pop(0)))
        field.append(row)

    result = solve(field)
    print(result_to_str(result))

          
