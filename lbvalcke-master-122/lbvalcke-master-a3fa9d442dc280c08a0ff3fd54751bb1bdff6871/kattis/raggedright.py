import sys

# Skeleton code for problem https://uchicago.kattis.com/problems/raggedright
#
# Make sure you read the problem before editing this code.
#
# You should focus only on implementing the solve() function.
# Do not modify any other code.

def solve(lines):
    """
    Parameters:
     - lines: List of strings. Each string is a line of the paragraph.

    Returns: The raggedness score (as defined in the problem statement)
    """
    char_list = []
    # YOUR CODE HERE
    for line in lines:
        char = list(line)
        char_list.append(char)
    lengths = []
    for i, line in enumerate(char_list):
        line_len = len(char_list[i])
        lengths.append(line_len)
    max_len = max(lengths)
    raggedness = 0
    for length in lengths[:len(lengths) - 1]:
        raggedness += (length - max_len) ** 2

    # Replace 0 with your return value
    return raggedness


if __name__ == "__main__":
    lines = sys.stdin.readlines()

    lines = [x.strip() for x in lines]

    rv = solve(lines)
    assert isinstance(rv, int), "solve() must return an integer"

    print(rv)

