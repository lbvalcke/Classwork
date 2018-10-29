# CS121: Analyzing Election Tweets
# Author: Luis Buenaventura and Leo Allen (partners)
# Part 1


from util import sort_count_pairs

def make_k_list(items):
    '''
    returns a list of counts for each item in items

    Inputs:
        items: list of items to be counted

    Returns:
        k_list: list of counts for each item in list as a list of tuples
    '''
  
    #initializes an empty dictionary
    k_dict = {}
    #creates keys with binned counts, the keys are the items from the list
    for item in items:
        k_dict[item] = k_dict.get(item, 0) + 1
    #converts dictionary to list of tuples
    k_list = k_dict.items()
    k_list_sorted = sort_count_pairs(k_list)

    return k_list_sorted


def find_top_k(items, k):
    '''
    Find the K most frequently occuring items

    Inputs:
        items: a list of items
        k: integer 

    Returns: sorted list of K tuples

    '''
  
    #calls function to make a list of counts for each item
    k_list_sorted = make_k_list(items)
    #sorts k_list by number of counts in decending order
    #cuts off sorted list to only the top k entries in the list
    top_k = k_list_sorted[:k]

    return top_k


def find_min_count(items, min_count):
    '''
    Find the items that occur at least min_count times

    Inputs:
        items: a list of items    
        min)count: integer
        
    Returns: sorted list of tuples
    '''
  
    #calls function to make a list of counts for each item
    k_list_sorted = make_k_list(items)
    ##cuts off each value in k_list under min_count
    k_list_min_sorted = [x for x in k_list_sorted if x[1] >= min_count]

    return k_list_min_sorted


def find_frequent(items, k):
    '''
    Find items where the number of times the item occurs is at least
    fraction * len(items).

    Input: 
        items: list of items
        k: integer

    Returns: sorted list of tuples
    '''
  
    # initializes empty dictionary for processing
    D = {}
  
    # loops over each item in the list
    for I in items:
        # checks to see if item isn't in list and if there are less 
        # than k-1 counters and adds it to list with value 1 if so
        if I not in D and len(D) < k - 1:
            D[I] = 0
            D[I] += 1
        # checks to see if item isn't in list and if there are more
        # than k-1 counters and reduces all items in list by 1 and drops 
        # items valued at 0
        elif I not in D and len(D) >= k - 1:
            D = {key: D[key] - 1 for key in D}
            D = {key: D[key] for key in D if D[key] >= 1}
        # adds 1 if item is in list
        else: 
            D[I] += 1
  
    # turns dictionary into list
    list_frequent = D.items()
    # sorts list
    list_freq_sorted = sort_count_pairs(list_frequent)
     
    # YOUR CODE HERE
    # REPLACE RETURN VALUE WITH AN APPROPRIATE VALUE
    return list_freq_sorted
