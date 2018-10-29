# CS122 W'17: Markov models and hash tables
# YOUR NAME HERE

import sys
import math
import Hash_Table

HASH_CELLS = 57

class Markov:

    def __init__(self,k,s):
        '''
        Construct a new k-order Markov model using the statistics of string "s"
        '''
        ### YOUR CODE HERE ###
        self.defval = 0
        self.s = s
        self.k = k
        self.alpha = len(set(s))
        self.k1 = k + 1
        self.n_table = self.create_hash(HASH_CELLS, self.defval, self.k, s)
        self.m_table = self.create_hash(HASH_CELLS, self.defval, self.k1, s)

    def create_hash(self, cells, defval, k, s):
        '''
        Initializes hash table for the specified number of k-grams.
        '''
        k_grams = self.gen_kgrams(k, s)
        k_hash = Hash_Table.Hash_Table(HASH_CELLS, defval)
        # Converts kgram list into hash table
        for gram in k_grams:
            val = k_hash.lookup(gram)
            if val == defval:
                k_hash.update(gram, 1)
            else: 
                k_hash.update(gram, val + 1)
        return k_hash

    def gen_kgrams(self, k, s):
        '''
        Generates the kgrams from a specified string.
        '''
        most_grams = [s[i-k:i] for i in range(k, len(s)+1)]
        missed_grams = []
        # Wraps around to find all possible kgrams
        for i in range(0,k-1):
            gram = s[-k+i+1:-1] + s[-1] + s[0:i+1]
            missed_grams.append(gram)
        return missed_grams + most_grams

    def log_probability(self, s):
        '''
        Get the log probability of string "s", given the statistics of
        character sequences modeled by this particular Markov model
        This probability is *not* normalized by the length of the string.
        '''
        ### YOUR CODE HERE ###
        log_prob = 0
        testing_k1grams = self.gen_kgrams(self.k1, s)
        # Finds probability of each k1_gram from the testing set
        for gram in testing_k1grams:
            m_value = self.m_table.lookup(gram)
            n_value = self.n_table.lookup(gram[:len(gram)-1])
            log_prob += math.log((m_value + 1) / (n_value + self.alpha))
        return log_prob



def identify_speaker(speech1, speech2, speech3, order):
    '''
    Given sample text from two speakers, and text from an unidentified speaker,
    return a tuple with the *normalized* log probabilities of each of the speakers
    uttering that text under a "order" order character-based Markov model,
    and a conclusion of which speaker uttered the unidentified text
    based on the two probabilities.
    '''
    ### YOUR CODE HERE ###
    speaker1 = Markov(order, speech1)
    prob1 = speaker1.log_probability(speech3) / len(speech3)
    speaker2 = Markov(order, speech2)
    prob2 = speaker2.log_probability(speech3) / len(speech3)
    # Creates conclusion
    if prob1 > prob2:
        conc = 'A'
    else: 
        conc = 'B'
    return (prob1, prob2, conc)


def print_results(res_tuple):
    '''
    Given a tuple from identify_speaker, print formatted results to the screen
    '''
    (likelihood1, likelihood2, conclusion) = res_tuple
    
    print("Speaker A: " + str(likelihood1))
    print("Speaker B: " + str(likelihood2))

    print("")

    print("Conclusion: Speaker " + conclusion + " is most likely")

if __name__=="__main__":
    num_args = len(sys.argv)

    if num_args != 5:
        print("usage: python3 " + sys.argv[0] + " <file name for speaker A> " +
              "<file name for speaker B>\n  <file name of text to identify> " +
              "<order>")
        sys.exit(0)
    
    with open(sys.argv[1], "rU") as file1:
        speech1 = file1.read()

    with open(sys.argv[2], "rU") as file2:
        speech2 = file2.read()

    with open(sys.argv[3], "rU") as file3:
        speech3 = file3.read()

    res_tuple = identify_speaker(speech1, speech2, speech3, int(sys.argv[4]))

    print_results(res_tuple)

