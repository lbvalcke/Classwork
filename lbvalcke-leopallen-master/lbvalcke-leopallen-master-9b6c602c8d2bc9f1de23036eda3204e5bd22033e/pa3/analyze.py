# CS121: Analyzing Election Tweets
#  Author: Luis Buenaventura and Leo Allen (partners)
# Part 2
 
import argparse
import json
import string
import sys
from util import sort_count_pairs, grab_year_month, pretty_print_by_month
from basic_algorithms import find_top_k, find_min_count, find_frequent, make_k_list
 
##################### DO NOT MODIFY THIS CODE #####################
 
PUNCTUATION = '!"$%\'()*+,-./:;<=>?[\\]^_`{|}~' + u"\u2014" + u"\u2026"
 
STOP_WORDS_SHORT = set(["a", "an", "the", "this", "that", "of", "for", "or", "and", "on", "to", "be", "if", "we", "you", "in", "is", "at", "it", "rt", "mt"])
 
STOP_WORDS = {"basic":STOP_WORDS_SHORT,
              "hrc":set(["clinton", "hillary", "tim", "timothy", "kaine"]).union(STOP_WORDS_SHORT),
              "djt": set(["donald", "trump", "mike", "michael", "pence"]).union(STOP_WORDS_SHORT),
              "both": STOP_WORDS_SHORT.union(set(["clinton", "hillary", "donald", "trump", "tim", "timothy", "kaine", "mike", "michael", "pence"])),
              "none": set([])}
 
STOP_PREFIXES  = {"default": set(["@", "#", "http", "&amp"]),
                  "hashtags_only": set(["#"]),
                  "none": set([])}
 
HRC_STOP_WORDS = STOP_WORDS["hrc"]
DT_STOP_WORDS = STOP_WORDS["djt"]
BOTH_CAND_STOP_WORDS = STOP_WORDS["both"]
 
# Tweets are represented as dictionaries that has the same keys and
# values as the JSON returned by twitter's search interface.
 
#####################  MODIFY THIS CODE #####################
# general functions

def counter(tweets, entity_key, value_key):
    '''
    Creates a dictionary containing counts associated w/ tweet entities.
    Helper function.

    Inputs:
        tweets: list of tweet dictionaries filled with info to be searched
                through and counted
        entity_key: key variable: either hashtags, urls, or user_mentions - 
                    to be used as a key to access information stored in tweets
        value_key:  key variable: either text, url, or screen_name - denotes 
                    the type of information that tweets will be counted for
                    Acts as a key for the dictionary mapped to by an 
                    entity_type

    Outputs: 
        tweet_entities_dict: a dictionary with counts mapped to by each entity
                            of the type of interest
    '''
    
    # creates empty dictionary to store tweet values
    tweet_entities_dict = {}
    
    # evaluates every tweet in the list of tweets
    for tweet in tweets:
        # picks dictionary associated with entity of interest
        tweet_entities = tweet["entities"][entity_key]
        # pulls info from each tweet entity
        for tweet_entity in tweet_entities:
            # finds value associated with each entity for the value of interest
            tweet_value = tweet_entity[value_key]
            # converts string elements to lower case
            tweet_value = tweet_value.lower()
            # adds a count to entity in the dictionary of entities. If an 
            # entity is not found in the tweet_entities_dictionary it is added
            # and given a baseline value of 1 
            tweet_entities_dict[tweet_value] = tweet_entities_dict.get(tweet_value, 0) + 1

    return tweet_entities_dict


def tweet_value_finder(tweets, entity_key, value_key):
    '''
    Creates a list of tweet values in lower case for a given entity and value
    type. Helper function

    Inputs: 
        tweets: list of tweet dictionaries filled with info stored in
                dictionaries
        entity_key: denotes entity type of interest
        value_key: denotes value type of interest

    Outputs:
        tweet_value_list: list of tweet values 
    '''
    
    # initializes an empty list to store tweet values
    tweet_value_list = []
    
    # searches through every tweet in tweets for values
    for tweet in tweets:
        # picks dictionary associated with entity of interest
        tweet_entities = tweet["entities"][entity_key]
        # searches over each tweet entity
        for tweet_entity in tweet_entities:
            # extracts tweet value
            tweet_value = tweet_entity[value_key]
            # converts value to lowercase
            tweet_value = tweet_value.lower()
            # adds value to a list of tweets
            tweet_value_list.append(tweet_value)

    return tweet_value_list


def preprocess_tweet(tweet, stop_words, stop_prefixes):
    '''
    Creates list of words from tweet with punctuation removed and with
    words with stop prefixes and stop words ignored 

    Inputs: 
        tweet: individual tweet dictionary
        stop_words: a set of strings to ignore
        stop_prefixes: a set of strings.  Words w/ a prefix that
           appears in this list should be ignored.
    Outputs:
        processed_tweet: list of tweet values 
    '''    
    
    # stores the stop_prefixes as a tuple
    stop_prefixes_tuple = tuple(stop_prefixes)
    # stores tweet text as a string in all in lower case 
    unprocessed_tweet = tweet["text"].lower()
    # stores each word in the tweet string as an individual element of a list
    undropped_words = unprocessed_tweet.split()
    # initializes an empty list to store words with removed punctuation
    no_punc_words = []
    # initializes empty list to store words after being processed
    processed_tweet = []

    for word in undropped_words:
        word_stripped = word.strip(PUNCTUATION)
        no_punc_words.append(word_stripped)

    for word_stripped in no_punc_words:
        if word_stripped.startswith(stop_prefixes_tuple) == False:
            if word_stripped != "":
                if word_stripped not in stop_words:
                    processed_tweet.append(word_stripped)

    return processed_tweet


def ngram_generator(tweets, n, stop_words, stop_prefixes):
    '''
    Generates a list of all possible n-grams from list of tweets 
  
    Inputs:
        tweets: a list of tweets
        n: integer
        stop_words: a set of strings to ignore
        stop_prefixes: a set of strings.  Words w/ a prefix that
          appears in this list should be ignored.
        k: integer
 
    Outputs:
        ngrams: a list of all the ngrams generated from the tweets 
    '''
  
    # creates list to hold ngram combinations
    ngrams = []
    
    # loops through tweets in list to preprocess text
    for tweet in tweets:
        preproc_words = preprocess_tweet(tweet, stop_words, stop_prefixes)
        #loops through words in tweet to create ngram
        for i, word in enumerate(preproc_words):
            # checks to see if there is space left in index to create ngram
            if i <= len(preproc_words) - n:
                # creates ngram
                ngram = (preproc_words[i:i + n])
                ngram = tuple(ngram)
                ngrams.append(ngram)
            else:
                pass 

    return ngrams


def ngram_counter(tweets, n, stop_words, stop_prefixes):
    '''
    Find n-grams and their associated counts.
   
    Inputs:
        tweets: a list of tweets
        n: integer
        stop_words: a set of strings to ignore
        stop_prefixes: a set of strings.  Words w/ a prefix that
          appears in this list should be ignored.
        min_count: integer
 
 
    Returns: list of key/value pairs sorted in non-increasing order
      by value.
    '''    
    
    # creates to list to hold ngrams and dict to count them
    ngram_dict = {}
    ngrams = []
    
    # loops through tweets in list to process text
    for tweet in tweets:
        preproc_words = preprocess_tweet(tweet, stop_words, stop_prefixes)
        # loops through words in tweet to create ngram
        for i, word in enumerate(preproc_words):
            # checks to see if there is space left in list index 
            # to create ngram
            if i <= len(preproc_words) - n:
                ngram = (preproc_words[i:i + n])
                ngram = tuple(ngram)
                ngram_dict[ngram] = ngram_dict.get(ngram, 0) + 1
            else:
                pass
    
    # converts dict to list and sorts
    ngram_list = ngram_dict.items()
    sorted_ngram_list = sort_count_pairs(ngram_list) 
    
    return sorted_ngram_list


# Task 1
def find_top_k_entities(tweets, entity_key, value_key, k):
    '''
    Find the K most frequently occuring entitites
 
    Inputs:
        tweets: a list of tweets
        entity_key: a string ("hashtags", "user_mentions", etc)
        value_key: string (appropriate value depends on the entity type)
        k: integer
 
    Returns: list of entity, count pairs sorted in non-decreasing order by count.
 
    '''
  
    # Calls counter function to count occurances of entities of a given type
    # found in tweets and store as a dictionary
    tweet_entities_dict = counter(tweets, entity_key, value_key)
    # Converts this dictionary to a list of tuples
    tweet_entities_list = tweet_entities_dict.items()
    # Sorts this list in decending order by calling sort_count_pairs function
    tweet_entities_list_sorted = sort_count_pairs(tweet_entities_list)
    # Chops off all but the K most occuring values from the list of entities
    tweet_entities_list_sorted = tweet_entities_list_sorted[:k]
    
    return tweet_entities_list_sorted
 
 
# Task 2
def find_min_count_entities(tweets, entity_key, value_key, min_count):
    '''
    Find the entitites that occur at least min_count times.
 
    Inputs:
        tweets: a list of tweets
        entity_key: a string ("hashtags", "user_mentions", etc)
        value_key: string (appropriate value depends on the entity type)
        min_count: integer
 
    Returns: list of entity, count pairs sorted in non-decreasing order by count.
    '''
   
    # calls counter function to count entity occurences in the tweets, stores
    # counts as a dictionary
    tweet_entities_dict = counter(tweets, entity_key, value_key)
    # converts this dictionary of counts to a list
    tweet_entities_list = tweet_entities_dict.items()
    # cuts out all entity values with counts below the specified min. threshold
    tweet_entities_list_min = [x for x in tweet_entities_list if x[1] >= min_count]
    # sorts list of values of count >= mincounts in decending order
    tweet_entities_list_sorted = sort_count_pairs(tweet_entities_list_min)
     
    return tweet_entities_list_sorted
 
 
# Task 3
def find_frequent_entities(tweets, entity_key, value_key, k):
    '''
    Find entities where the number of times the specific entity occurs
    is at least fraction * the number of entities in across the tweets.
 
    Input:
        tweets: a list of tweets
        entity_key: a string ("hashtags", "user_mentions", etc)
        value_key: string (appropriate value depends on the entity type)
        k: integer
 
    Returns: list of entity, count pairs sorted in non-decreasing order by count.
    '''
   
    # creates empty list to store relevant values from tweets
    tweet_freq = {}
    # generates a list of tweet values to be analyzed by calling
    # tweet_value_finder function
    tweet_values = tweet_value_finder(tweets, entity_key, value_key)
    
    # loops over each tweet value in tweet_values
    for tweet_value in tweet_values:
        # if a value is not stored in tweet_freq dictionary, and the dict.
        # is not longer than the specified length, frequencty count for
        # the value is increased by one
        if tweet_value not in tweet_freq and len(tweet_freq) < k - 1:
            tweet_freq[tweet_value] = 0
            tweet_freq[tweet_value] += 1 
        # if a tweet value is not found in tweet_freq and the dictionary's
        # length meets/exceeds k-1, all counts in tweet_freq are decreased
        # and gets rid of phrases (keys) which map to 0 after the decrease
        elif tweet_value not in tweet_freq and len(tweet_freq) >= k - 1:
            tweet_freq = {key: tweet_freq[key] - 1 for key in tweet_freq}
            tweet_freq = {key: tweet_freq[key] for key in tweet_freq if tweet_freq[key] >= 1}
        # if a tweet entity is found in tweet_freq and the length condition is
        # not exceeded, the count for the value in question is increased by 1
        else: 
            tweet_freq[tweet_value] += 1
   
    # converts the tweet_freq dictionary to a sortable list
    tweet_frequent = tweet_freq.items()
    # sorts the tweet_freq list in decending order by counts
    tweet_freq_sorted = sort_count_pairs(tweet_frequent)
    
    return tweet_freq_sorted
 
 
# Task 4
def find_top_k_ngrams(tweets, n, stop_words, stop_prefixes, k):
    '''
    Find k most frequently occurring n-grams or
    if k < 0, count occurrences of all n-grams
   
    Inputs:
        tweets: a list of tweets
        n: integer
        stop_words: a set of strings to ignore
        stop_prefixes: a set of strings.  Words w/ a prefix that
          appears in this list should be ignored.
        k: integer
 
    Returns: list of key/value pairs sorted in non-increasing order
      by value.
    '''
  
    #calls counter function and cuts off list based on chosen index k
    counted_ngrams = ngram_counter(tweets, n, stop_words, stop_prefixes)
    top_k_ngrams = counted_ngrams[:k] 
    
    return top_k_ngrams
 
 
# Task 5
def find_min_count_ngrams(tweets, n, stop_words, stop_prefixes, min_count):
    '''
    Find n-grams that occur at least min_count times.
   
    Inputs:
        tweets: a list of tweets
        n: integer
        stop_words: a set of strings to ignore
        stop_prefixes: a set of strings.  Words w/ a prefix that
          appears in this list should be ignored.
        min_count: integer
 
 
    Returns: list of key/value pairs sorted in non-increasing order
      by value.
    '''
    
    # calls counter function
    counted_ngrams = ngram_counter(tweets, n, stop_words, stop_prefixes)
    
    # finds first ngram in sorted list less than min_count
    for i, count in enumerate(counted_ngrams):
        if counted_ngrams[i][1] < min_count:
            index = i
            break
    
    # cuts off sorted list at identified index
    min_count_ngrams = counted_ngrams[:index]

    return min_count_ngrams

 
# Task 6
def find_frequent_ngrams(tweets, n, stop_words, stop_prefixes, k):
    '''
    Find frequently occurring n-grams
 
    Inputs:
        tweets: a list of tweets
        n: integer
        stop_words: a set of strings to ignore
        stop_prefixes: a set of strings.  Words w/ a prefix that
          appears in this list should be ignored.
        k: integer
 
    Returns: list of key/value pairs sorted in non-increasing order
      by value.
    '''
    
    # calls generator function to generate possible ngrams 
    ngrams = ngram_generator(tweets, n, stop_words, stop_prefixes)
    
    # initializes empty dictionary for processing
    freq_ngrams = {}
    # loops over each item in the list
    for ngram in ngrams:
        # checks to see if item isn't in list and if there are less 
        # than k-1 counters and adds it to list with value 1 if so
        if ngram not in freq_ngrams and len(freq_ngrams) < k - 1:
            freq_ngrams[ngram] = 0
            freq_ngrams[ngram] += 1
        # checks to see if item isn't in list and if there are more
        # than k-1 counters and reduces all items in list by 1 and drops 
        # items valued at 0
        elif ngram not in freq_ngrams and len(freq_ngrams) >= k - 1:
            freq_ngrams = {key: freq_ngrams[key] - 1 for key in freq_ngrams}
            freq_ngrams = {key: freq_ngrams[key] for key in freq_ngrams if freq_ngrams[key] >= 1}
        # adds 1 if item is in list
        else: 
            freq_ngrams[ngram] += 1
    # turns dictionary into list
    freq_ngram_list = freq_ngrams.items()
    # sorts list
    freq_ngram_list_sorted = sort_count_pairs(freq_ngram_list)
     
    return freq_ngram_list_sorted
 
 
# Task 7
 
def find_top_k_ngrams_by_month(tweets, n, stop_words, stop_prefixes, k):
    '''                                                                                                            
    Find the top k ngrams for each month.
 
    Inputs:
        tweets: list of tweet dictionaries
        n: integer
        stop_words: a set of strings to ignore
        stop_prefixes: a set of strings.  Words w/ a prefix that
          appears in this list should be ignored.
        k: integer
 
    Returns: sorted list of pairs.  Each pair has the form:
        ((year,  month), (sorted top-k n-grams for that month with their counts))
    '''

    # initializes dict and lists to hold tweets, dates, and ngrams
    tweet_dict_by_date = {}
    top_k_n_grams_by_month = []
    list_of_tweet_dates = []
    
    # pulls date for each tweet
    for tweet in tweets:   
        tweet_date = grab_year_month(tweet["created_at"])
        #adds date key to dict if its not contained in it 
        #and also appends tweet to relevant date key 
        tweet_dict_by_date.setdefault(tweet_date, []).append(tweet)
        # adds tweet date to list 
        if tweet_date not in list_of_tweet_dates:
            list_of_tweet_dates.append(tweet_date)

    # sorts list of dates
    list_of_tweet_dates.sort()
    
    # finds top ngram for each month and year pair
    for tweet_date in list_of_tweet_dates:
        top_k = find_top_k_ngrams(tweet_dict_by_date[tweet_date], n, stop_words, stop_prefixes, k)
        tweet_date_tuple = (tweet_date, top_k)
        top_k_n_grams_by_month.append(tweet_date_tuple)

    return top_k_n_grams_by_month
 
 
def parse_args(args):
    '''                                                                                                                
    Parse the arguments                                                                                                
    '''
    parser = argparse.ArgumentParser(description='Analyze presidential candidate tweets .')
    parser.add_argument('-t', '--task', nargs=1, help="<task number>", type=int, default=[0])
    parser.add_argument('-k', '--k', nargs=1, help="value for k", type=int, default=[1])
    parser.add_argument('-c', '--min_count', nargs=1, help="min count value", type=int, default=[1])
    parser.add_argument('-n', '--n', nargs=1, help="number of words in an n-gram", type=int, default=[1])
    parser.add_argument('-e', '--entity_key', nargs=1, help="entity key for task 1", type=str, default=["hashtags"])
    parser.add_argument('file', nargs=1, help='name of JSON file with tweets')
 
    try:
        return parser.parse_args(args[1:])
    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(1)
 
def go(args):
    task = args.task
   
    task = task[0]
 
    if task <= 0 or task > 7:
        print("The task number needs to be a value between 1 and 7 inclusive.",
              file=sys.stderr)
        sys.exit(1)
       
    ek2vk = {"hashtags":"text",
             "urls":"url",
             "user_mentions":"screen_name"}
 
    if task in [1,2,3]:
        ek = args.entity_key=args.entity_key[0]
        if ek not in ek2vk:
            print("Entity type must be one of: hashtags, urls, or user_mentions",
                  file=sys.stderr)
            sys.exit(1)
        else:
            vk = ek2vk[ek]
 
    try:
        tweets = json.load(open(args.file[0]))
    except OSError as e:
        print(e, file=sys.stderr)
        sys.exit(1)
 
    if task == 1:
        print(find_top_k_entities(tweets, ek, vk, args.k[0]))
 
    elif task == 2:
        print(find_min_count_entities(tweets, ek, vk, args.min_count[0]))
 
    elif task == 3:
        print(find_frequent_entities(tweets, ek, vk, args.k[0]))
 
    elif task == 4:
        print(find_top_k_ngrams(tweets, args.n[0], BOTH_CAND_STOP_WORDS,
                                STOP_PREFIXES["default"], args.k[0]))
    elif task == 5:
        print(find_min_count_ngrams(tweets, args.n[0], BOTH_CAND_STOP_WORDS,
                                    STOP_PREFIXES["default"], args.min_count[0]))
    elif task == 6:
        print(find_frequent_ngrams(tweets, args.n[0], BOTH_CAND_STOP_WORDS,
                                   STOP_PREFIXES["default"], args.k[0]))
    elif task == 7:
        result = find_top_k_ngrams_by_month(tweets, args.n[0], BOTH_CAND_STOP_WORDS,
                                            STOP_PREFIXES["default"], args.k[0])
        pretty_print_by_month(result)
 
 
 
if __name__=="__main__":
    args = parse_args(sys.argv)
    go(args)