#!/usr/bin/python

# Skeleton code for problem https://uchicago.kattis.com/problems/uchicagoplacement.palindrome
#
# Make sure you read the problem before editing this code.
#
# You should focus only on implementing the is_palindrome function.
# Do not modify any other code.

import sys

def is_palindrome(s):
    # This function takes a string and returns True if the
    # string is a palindrome (and False otherwise)
    if len(s) == 1:
    	return True
    elif len(s) == 2:
    	if s[0] == s[1]:
    		return True
    	else:
    		return False
    else:
    	if s[0] == s[-1]:
    		return is_palindrome(s[1:len(s) - 1])
    	else:
    		return False


### The following code handles the input and output tasks for
### this problem.  Do not modify it!

if __name__ == "__main__":
    s = sys.stdin.read().strip()

    if is_palindrome(s):
        print("PALINDROME")
    else:
        print("NOT PALINDROME")

