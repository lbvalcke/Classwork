import sys

# Skeleton code for problem https://uchicago.kattis.com/problems/permutationencryption
#
# Make sure you read the problem before editing this code.
#
# You should focus only on implementing the solve() function.
# Do not modify any other code.


def encrypt(message, permutations):
    """
    Parameters:
     - message: String. The message to encrypt.
     - permutations: List of integers. The integers that form the permutation.

    Returns: String. The encrypted message.
    """
    # Your code here.
    if len(permutations) > 1:
        rep_len = max(permutations)
        msg_list = list(message)

        if len(msg_list) % rep_len > 0:
            for i in range(rep_len - len(msg_list) % rep_len):
                msg_list.append(" ")
        
        div = len(msg_list) // rep_len

        str_groups = [[] for i in range(div)]
        enc_groups = [[] for i in range(div)]

        for i, char in enumerate(msg_list):
            list_index = i // rep_len
            str_groups[list_index].append(char)
            enc_groups[list_index].append(char)

        for i, group in enumerate(str_groups):
            for j, index in enumerate(permutations):
                enc_groups[i][j] = str_groups[i][index - 1] 

        enc_groups_flat = [val for sublist in enc_groups for val in sublist]
        message = ''.join(enc_groups_flat)
    
    # Replace "" with a suitable return value.
    return message


### The following code handles the input and output tasks for
### this problem.  Do not modify it!

if __name__ == "__main__":
    tokens = sys.stdin.readline().split()

    while int(tokens[0]) != 0:
        n = int(tokens[0])
        permutations = [int(x) for x in tokens[1:]]
        assert(len(permutations) == n)

        message = sys.stdin.readline().strip()
    
        print("'{}'".format(encrypt(message, permutations)))
        
        tokens = sys.stdin.readline().split()
    
