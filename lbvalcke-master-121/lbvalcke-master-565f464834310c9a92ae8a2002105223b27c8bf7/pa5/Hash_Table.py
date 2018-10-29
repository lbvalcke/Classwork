# CS122 W'17: Markov models and hash tables
# Luis Buenaventura Valcke (lbvalcke)


TOO_FULL = 0.5
GROWTH_RATIO = 2


class Hash_Table:

    def __init__(self,cells,defval):
        '''
        Construct a bnew hash table with a fixed number of cells equal to the
        parameter "cells", and which yields the value defval upon a lookup to a
        key that has not previously been inserted
        '''
        ### YOUR CODE HERE ###
        self.cells = cells
        self.defval = defval 
        self.hash_table = [[] for i in range(cells)]
        self.entries = 0 

    def hash_f(self, key):
        '''
        Calculates hash index for string
        '''
        hash_num = 0 
        for i, char in enumerate(key):
            hash_num += 37**(len(key) - i - 1) * ord(char)
        hash_num = hash_num % self.cells
        return hash_num    

    def update_hash(self, hash_num):
        '''
        Checks if following index following current hash num 
        is in the hash table
        '''
        if hash_num + 1 == self.cells:
            new_hash_num = 0
        else: 
            new_hash_num = hash_num + 1 
        return new_hash_num        

    def lookup(self,key):
        '''
        Retrieve the value associated with the specified key in the hash table,
        or return the default value if it has not previously been inserted.
        '''
        ### YOUR CODE HERE ###
        hash_num = self.hash_f(key)
        # Checks to see if the position is empty
        if self.hash_table[hash_num] != []:
            if key == self.hash_table[hash_num][0]: 
                return self.hash_table[hash_num][1]
            else: 
                new_hash_num = self.update_hash(hash_num)
                # Linear Probing
                while  new_hash_num != hash_num:
                    # Finds empty slot
                    if self.hash_table[new_hash_num] == []:
                        break
                    elif key == self.hash_table[new_hash_num][0]: 
                        return self.hash_table[new_hash_num][1]
                    else: 
                        new_hash_num = self.update_hash(new_hash_num)
        # Returns default value if key is not found
        return self.defval

    def update(self,key,val):
        '''
        Change the value associated with key "key" to value "val".
        If "key" is not currently present in the hash table, insert it with
        value "val".
        '''
        ### YOUR CODE HERE ###
        hash_num = self.hash_f(key)
        # Checks to see if key is in hash table
        if self.lookup(key) != self.defval:
            if key == self.hash_table[hash_num][0]:
                self.hash_table[hash_num] = (key, val)
            
            else:
                # Linear probing
                new_hash_num = self.update_hash(hash_num)
                while  new_hash_num != hash_num:
                    # Finds key
                    if key == self.hash_table[new_hash_num][0]: 
                        self.hash_table[new_hash_num] = (key, val)
                        break
                    else: 
                        new_hash_num = self.update_hash(new_hash_num)

        else:
            # Checks to see if there is room for the key in the table
            if self.entries + 1 <= self.cells * TOO_FULL:
                if self.hash_table[hash_num] != []:
                    # Linear probing
                    new_hash_num = self.update_hash(hash_num)
                    while  new_hash_num != hash_num:
                        # Empty slot
                        if self.hash_table[new_hash_num] == []: 
                            self.hash_table[new_hash_num] = (key, val)
                            break
                        else: 
                            new_hash_num = self.update_hash(new_hash_num)

                else:  
                    self.hash_table[hash_num] = (key, val)               
            # Rehashes if table is too full
            else:
                self.rehash(self.cells * GROWTH_RATIO)
                self.update(key, val)
            self.entries += 1

    def rehash(self, new_cells):
        '''
        Rehash table if size limit is reached. 
        '''
        old_hash = self.hash_table
        self.entries = 0
        self.cells = new_cells
        self.hash_table = [[] for i in range(new_cells)]
        for pair in old_hash:
            if pair != []:
                self.update(pair[0], pair[1])

