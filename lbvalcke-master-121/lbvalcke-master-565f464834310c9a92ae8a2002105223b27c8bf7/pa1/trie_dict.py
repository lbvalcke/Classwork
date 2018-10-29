# CS122: Auto-completing keyboard using Tries
#
# usage: python trie_dict.py <dictionary filename>
#
# Luis Buenaventura Valcke (cnetid: lbvalcke)

import os
import sys
from sys import exit
import tty
import termios
import fcntl
import string

import trie_shell

def create_trie_node():
    '''
    Creates an empty trie node with count set at zero and final to false.
    '''
    return {'count': 0, 'final': False}


def add_word(word, trie):
    '''
    Recursively either creates nodes for each letter in then inputted word
    or adds to the counts of letter if they already exist. 

    Inputs: 
        word: the string to be inserted letter by letter into the trie
        trie: the trie to be filled out
    Returns: trie with the added word.
    '''
    # Automatically adds 1 to the tree to reflect the addition of each
    # successive letter
    trie['count'] += 1
    # Checks to see if the letter exists in that level of the trie
    trie[word[0]] = trie.get(word[0], create_trie_node())
    
    # Adds the next letter of the word to the next level of the trie
    if len(word) > 1:
        return add_word(word[1:], trie[word[0]])
    
    # Adds the finishing conditions at the end of the word
    else:
        trie[word[0]]['count'] += 1
        trie[word[0]]['final'] = True
        return trie


def is_word(word, trie):
    '''
    Runs through the letters of the inputted prefix to see if its
    successive letters are present in the trie. If any of the letters are
    not, it returns False. Otherwise, True. It allows for an empty string.

    Inputs:
        word: the string to be checked against the trie
        trie: trie to be used to check string 
    Returns: Boolean value.
    '''
    # Checks to see if the first letter is in the tree
    if len(word) > 0 and word[0] not in trie:
        return False
    
    # If the first letter is in the tree it checks the next
    elif len(word) > 1 and word[0] in trie: 
        return is_word(word[1:], trie[word[0]])
    
    else:
            return True

def suffix_trie(word, trie):
    '''
    Checks to see if the inputted prefix fits into the trie and returns the
    the trie nodes below the inputted prefix. 

    Inputs:
        word: string to be used to jump down the trie.
        trie: trie to be used.
    Returns: part of the original trie. 
    '''
    # Climbs down trie using the letters of a prefix string
    if is_word(word, trie):
        if len(word) > 0:
            for letter in word:
                trie = trie[letter]
        return trie
    
    else: 
        return []

def num_completions(word, trie):
    '''
    Uses the inputted prefix to jump to the relevant part of the tree
    and then checks the count to return the possible number of completions.

    Inputs:
        word: string of the prefix
        trie: the trie of interest.
    Returns: numeric value for number of completions 
    '''
    # Jumps to relevant node and checks the count
    suff_trie = suffix_trie(word, trie)
    if suff_trie == []:
        return 0
    else:
        return suff_trie['count']


def get_completions(word, trie):
    '''
    Prepares the trie to find the relevant completions to the inputted prefix.
    Passes the trie to get_list() and then returns the list of completions.
    Inputs: 
        word: string of the prefix
        trie: the trie of interest
    Returns: list of strings corresponding to completions
    '''
    # Prepares trie and gets list
    suff_trie = suffix_trie(word, trie)
    if suff_trie == []:
        return []
    else:
        return get_list(suff_trie)


def get_list(trie):
    '''
    Recursively gathers the possible completions to a trie.
    Checks to see if a node is a leaf and if so returns a list
    holding an empty string. If it is not, it checks to see if the
    node corresponds to a complete node and adds an empty string if so.
    If not, it goes through the possible letters connecting to a node
    and concatenates them. This is done until a base case is reached.

    Inputs:
        trie: the trie used to gather completions
    Returns: list of strings corresponding to completions
    '''
    words = []
    # Base case
    if trie['count'] == 1 and trie['final'] == True:
        return ['']
    else: 
        # Checks to see if node is a completion
        if trie['count'] > 1 and trie['final'] == True:
            words.append('')
        # Checks following nodes
        for key in trie.keys():
            if len(key) == 1: 
                for word in get_list(trie[key]):
                    words.append(key + word)
        return words



if __name__ == "__main__":
    trie_shell.go("trie_dict")
