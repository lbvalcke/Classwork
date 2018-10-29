import sys

# Skeleton code for problem https://uchicago.kattis.com/problems/quickbrownfox
#
# Make sure you read the problem before editing this code.
#
# You should focus only on implementing the solve() function.
# Do not modify any other code.

# This function takes one parameter: the phrase (as described in the problem statement)
#
# It must return a list of letters that are missing from the phrase (i.e., that 
# prevent the phrase from being a pangram, as described in the problem statement) 
# The missing letters should be reported in lower case and should be sorted 
# alphabetically.
#
# If the phrase is a pangram, just return an empty list.
def solve(phrase):
    # YOUR CODE HERE
    phrase_char = list(phrase)
    dup_char = []
    char_dict = {"a": 1, "b": 2,"c": 3,"d": 4,"e": 5,"f": 6,"g": 7,"h": 8,"i": 9,"j": 10,"k": 11,"l": 12,"m": 13,"n": 14,"o": 15,"p": 16,"q": 17,"r": 18,"s": 19,"t": 20,"u": 21,"v": 22,"w": 23,"x": 24,"y": 25,"z": 26}
    for i, char in enumerate(phrase_char):
        if char.lower() in char_dict.keys():
            if char in dup_char:
                pass
            else:     
                lc_char = char.lower()
                dup_char.append(lc_char)
                char_dict.pop(lc_char)


    missing = sorted(char_dict.keys())

    # Replace [] with the list of missing characters
    return missing


if __name__ == "__main__":
    ntests = int(sys.stdin.readline())

    for i in range(ntests):
        phrase = sys.stdin.readline().strip()
        missing = solve(phrase)

        if len(missing) == 0:
            print("pangram")
        else:
            print("missing", "".join(missing))
