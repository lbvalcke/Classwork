import sys

# Skeleton code for problem https://uchicago.kattis.com/problems/blackfriday
#
# Make sure you read the problem before editing this code.
#
# You should focus only on implementing the solve() function.
# Do not modify any other code.


def solve(rolls):
    """
    Parameters:
     - rolls: List of integers. The outcome of each participant's die roll.

    Returns: Integer, or None.
             The index of the participat that has the highest unique outcome.
             If no such participant exists, return None.
    """

    # Your code here.
    unique_dict = {}
    unique_list = []
    remove_list = []
    for i, roll in enumerate(rolls):
        if roll not in unique_dict:
            if roll not in remove_list:
                unique_dict[roll]  = i + 1
                unique_list.append(roll)
        elif roll in unique_dict:
            remove_list.append(roll) 
            unique_dict.pop(roll)
            unique_list.remove(roll)
    unique_list = sorted(unique_list)
    if unique_list != []:
        return unique_dict[unique_list[-1]]
    else:
        return None


### The following code handles the input and output tasks for
### this problem.  Do not modify it!

if __name__ == "__main__":
    tokens = sys.stdin.read().split()

    n = int(tokens.pop(0))
    rolls = [int(tokens.pop(0)) for i in range(n)]

    rv = solve(rolls)
    if rv is None:
        print("none")
    else:
        print(rv)

