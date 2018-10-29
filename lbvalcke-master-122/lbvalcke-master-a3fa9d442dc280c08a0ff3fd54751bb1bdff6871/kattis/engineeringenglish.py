import sys

# Skeleton code for problem https://uchicago.kattis.com/problems/engineeringenglish
#
# Make sure you read the problem before editing this code.
#
# You should focus only on implementing the solve() function.
# Do not modify any other code.

# This function takes a single parameter: a list of strings, each corresponding
# to a line of input. You must return a list of strings where the strings
# have been converted as described in the problem statement.
def solve(lines):
    # YOUR CODE HERE
    eng_dict = {}
    duplicates = []
    split_lines = [line.split() for line in lines]

    words = [word for line in split_lines for word in line]

    lc_words = [word.lower() for word in  words] 

    for i, lines in enumerate(split_lines):
        for j, word in enumerate(lines):
            lc_word = word.lower()
            index = (i, j)
            eng_dict[lc_word] = eng_dict.setdefault(lc_word, [])
            eng_dict[lc_word].append(index)

    for word in eng_dict: 
        if len(eng_dict[word]) > 1: 
            duplicates.append(eng_dict[word][1:len(eng_dict[word])])

    for duplicate in duplicates:
        if len(duplicate) > 1:
            for i, index in enumerate(duplicate):
                split_lines[duplicate[i][0]][duplicate[i][1]] = "."
        if len(duplicate) == 1:
            split_lines[duplicate[0][0]][duplicate[0][1]] = "."

    new_lines = [' '.join(line) for line in split_lines] 
    # Replace [] with the list of processed strings
    
    return new_lines


if __name__ == "__main__":
    lines = [s.strip() for s in sys.stdin.readlines()]

    print("\n".join(solve(lines)))
