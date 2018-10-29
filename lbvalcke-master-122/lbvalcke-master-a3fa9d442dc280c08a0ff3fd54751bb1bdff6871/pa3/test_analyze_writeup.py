# CS121: Analyzing Election Tweets
# 
# Test code for tweet analysis algorithms
#

import json
import pytest
import os
import sys

# Handle the fact that the grading code may not
# be in the same directory as analyze.py
sys.path.append(os.getcwd())

from analyze import find_top_k_entities, find_min_count_entities, find_frequent_entities
from analyze import find_top_k_ngrams, find_min_count_ngrams, find_frequent_ngrams
from analyze import find_top_k_ngrams_by_month, STOP_PREFIXES, STOP_WORDS
from util import sort_count_pairs

# Get the test files from the same directory as
# this file.
BASE_DIR = os.path.dirname(__file__)
TEST_DATA_DIR = os.path.join(BASE_DIR, "test_data")

######### Utilities #########

def is_sequence(arg):
    '''
    From stackoverflow.com/questions/1835018/python-check-if-an-object-is-a-list-or-tuple-but-not-string
    '''
    return (not hasattr(arg, "strip") and
            hasattr(arg, "__getitem__") or
            hasattr(arg, "__iter__"))

def check_type(l):
    '''
    Does l have the format: list-like value with tuples of length 2 as
    elements?
    '''
    if not is_sequence(l):
        return False
    for item in l:
        if not isinstance(item, tuple) or len(item) != 2:
            return False

    return True

######### Helpers #########

task_to_fn = {"task1":find_top_k_entities,
              "task2":find_min_count_entities,
              "task3":find_frequent_entities,
              "task4":find_top_k_ngrams,
              "task5":find_min_count_ngrams,
              "task6":find_frequent_ngrams,
              "task7":find_top_k_ngrams_by_month}


def get_expected(test_description):
    '''
    Get the expected value from the file and convert convert inner
    lists to tuples.  Why? Because JSON does not support tuples.
    '''

    try:
        expected = json.load(open(test_description["expected_filename"]))    
    except OSError as e:
        return None

    if test_description["task"] in ["task1", "task2", "task3"]:
        for i in range(len(expected)):
            expected[i] = tuple(expected[i])
    elif test_description["task"] in ["task4", "task5", "task6"]:
        for i in range(len(expected)):
            expected[i] = (tuple(expected[i][0]), expected[i][1])
    else:
        assert test_description["task"] == "task7"
        for i in range(len(expected)):
            (year_month, topk) = expected[i]
            for j in range(len(topk)):
                (ngram, count) = topk[j]
                topk[j] = (tuple(ngram), count)
            expected[i] = (tuple(year_month), topk)

    return expected


def helper(test_description):
    task = test_description["task"]

    # load the tweets from the file
    try:
        tweet_filename = os.path.join(BASE_DIR, test_description["tweet_filename"])
        tweets = json.load(open(tweet_filename))
    except OSError as e:
        pytest.fail("{}".format(e))

    expected = get_expected(test_description)
    if expected == None:
        pytest.fail("Could not open expected result file:"+ test_description["expected_filename"] + ":")

    try:
        if task in ["task1", "task2", "task3"]:
            actual = task_to_fn[task](tweets, test_description["entity_type"], 
                                      test_description["value_key"], test_description["arg3"])
        else:
            assert task in ["task4", "task5", "task6", "task7"]
            stop_words = STOP_WORDS.get(test_description["stop_words_key"], set([]))
            stop_prefix = STOP_PREFIXES.get(test_description["stop_prefix_key"], set([]))
            actual = task_to_fn[task](tweets, test_description["n"], 
                                      stop_words, stop_prefix, 
                                      test_description["arg4"])
    except Exception as e:
        pytest.fail("{}".format(e))

    if not check_type(actual):
        s = "Actual result has the wrong type.  The correct type is list of pairs (that is, tuples of length 2)"
        pytest.fail(s)

    if actual != expected:
        if len(actual) != len(expected):
            s = "Length of actual result ({}) does not match the length of the expected result ({})"
            pytest.fail(s.format(len(actual), len(expected)))

        if sort_count_pairs(actual) == expected:
            pytest.fail("Actual result is not sorted properly.")

        for i in range(len(actual)):
            if actual[i] != expected[i]:
                s = "Actual result at index {} ({}) does not match expected result ({}) at index {}."
                pytest.fail(s.format(i, actual[i], expected[i], i))

    # Test succeeded if you get to here
    return



######### Generated test code #########

def test_task1_0():
    '''
    top-k entities example
    '''
    helper({'expected_filename': './data/test-task1-0-expected.json', 'task': 'task1', 'arg3': 3, 'tweet_filename': './data/hrc-feb.json', 'entity_type': 'hashtags', 'value_key': 'text'})

def test_task2_0():
    '''
    min count entities example
    '''
    helper({'expected_filename': './data/test-task2-0-expected.json', 'task': 'task2', 'arg3': 15, 'tweet_filename': './data/djt-feb.json', 'entity_type': 'hashtags', 'value_key': 'text'})

def test_task3_0():
    '''
    frequent entities example
    '''
    helper({'expected_filename': './data/test-task3-0-expected.json', 'task': 'task3', 'arg3': 3, 'tweet_filename': './data/hrc-feb.json', 'entity_type': 'hashtags', 'value_key': 'text'})

def test_task4_0():
    '''
    top k ngrams example
    '''
    helper({'expected_filename': './data/test-task4-0-expected.json', 'stop_words_key': 'hrc', 'task': 'task4', 'n': 2, 'tweet_filename': './data/hrc-feb.json', 'arg4': 3, 'stop_prefix_key': 'default'})

def test_task5_0():
    '''
    basic test
    '''
    helper({'expected_filename': './data/test-task5-0-expected.json', 'stop_words_key': 'djt', 'task': 'task5', 'n': 2, 'tweet_filename': './data/djt-feb.json', 'arg4': 30, 'stop_prefix_key': 'default'})

def test_task6_0():
    '''
    frequent ngrams example
    '''
    helper({'expected_filename': './data/test-task6-0-expected.json', 'stop_words_key': 'hrc', 'task': 'task6', 'n': 2, 'tweet_filename': './data/hrc-feb.json', 'arg4': 3, 'stop_prefix_key': 'default'})

def test_task7_0():
    '''
    top k by month example
    '''
    helper({'expected_filename': './data/test-task7-0-expected.json', 'stop_words_key': 'both', 'task': 'task7', 'n': 2, 'tweet_filename': './data/djt-all.json', 'arg4': 3, 'stop_prefix_key': 'default'})

