import sys

# Skeleton code for problem https://uchicago.kattis.com/problems/securedoors
#
# Make sure you read the problem before editing this code.
#
# You should focus only on implementing the solve() function.
# Do not modify any other code.

# This function takes one parameter: A list of pairs. Each pair contains 
# two strings. The first one is either "entry" or "exit", and the second one
# is a name
#
# The function should not return anything. It should directly print
# the output as specified in the problem statement.
def solve(access_log):
    # Replace pass with your solution
    access_count = {}
    for access in access_log:
        if access[0] == "entry":
            if access[1] not in access_count or access_count[access[1]] == 0:
                access_count[access[1]] = access_count.get(access[1], 0) + 1
                print(str(access[1]) + " entered")
            elif access_count[access[1]] == 1:
                print(str(access[1]) + " entered" + " (ANOMALY)") 
        if access[0] == "exit":
            if access[1] not in access_count or access_count[access[1]] == 0:
                print(str(access[1]) + " exited" + " (ANOMALY)") 
            elif access_count[access[1]] == 1:
                access_count[access[1]] = access_count.get(access[1], 1) - 1
                print(str(access[1]) + " exited")


if __name__ == "__main__":
    tokens = sys.stdin.read().strip().split()

    n = int(tokens.pop(0))
    access_log = []
    for i in range(n):
        action = tokens.pop(0)
        name = tokens.pop(0)
        access_log.append( (action, name) )

    solve(access_log)
