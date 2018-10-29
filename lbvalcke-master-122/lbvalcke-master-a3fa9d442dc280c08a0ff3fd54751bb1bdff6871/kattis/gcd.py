#!/usr/bin/python

# Skeleton code for problem https://uchicago.kattis.com/problems/uchicago.mpcs.gcd
#
# Make sure you read the problem before editing this code.
#
# You should focus only on implementing the gcd function.
# Do not modify any other code.

import sys

def gcd(a,b):
    # This function takes a pair of floats and returns their greatest
    # common denominator.
    if a == 0 or b == 0:
    	return 0
    elif a == b:
    	return a
    elif a > b:
    	return gcd(a - b, b)
    elif a < b:
    	return gcd(a, b - a)

### The following code handles the input and output tasks for
### this problem.  Do not modify it!

tokens = sys.stdin.read().split()

a = int(tokens[0])
b = int(tokens[1])

print(gcd(a, b))
