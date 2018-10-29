# CS121 Lab 3: Function


# Write functions are_any_true, add_lists, and add_one
def are_any_true(booleans):
    true_list = []
    for x in booleans: 
    	value = "FALSE"
    	if x == 1:
    		value = "TRUE"
    	true_list.append(value)
    return true_list


def add_lists(list1, list2):
    sum_list = []
    for x,y in zip(list1,list2):
    	sums = x + y
    	sum_list.append(sums)
    return sum_list


def add_one(list1):
	for i in range(len(list1)): 
		list1[i] = list1[i] + 1 
	return list1



def go():
    '''
    Write code to verify that your functions work as expected here.
    Try to think of a few good examples to test your work.
    '''

    # replace the pass with test code for your functions
    list1 = [1,2,3,4]
    list2 = [1,2,3,4]
    true = are_any_true(list1)
    addlists = add_lists(list1, list2)
    addone = add_one(list1)
    
    print(true)
    print(addlists)
    print(addone)


if __name__ == "__main__":
    go()

