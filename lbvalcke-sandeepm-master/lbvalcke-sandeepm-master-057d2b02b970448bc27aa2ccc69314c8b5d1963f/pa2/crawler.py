# CS122: Course Search Engine Part 1
#
# Authors: Sandeep Malladi, Luis Buenaventura
#
#
# PA2

import re
import util
import bs4
import queue
import json
import sys
import csv
import string

INDEX_IGNORE = set(['a',  'also',  'an',  'and',  'are', 'as',  'at',  'be',
                    'but',  'by',  'course',  'for',  'from',  'how', 'i',
                    'ii',  'iii',  'in',  'include',  'is',  'not',  'of',
                    'on',  'or',  's',  'sequence',  'so',  'social',  'students',
                    'such',  'that',  'the',  'their',  'this',  'through',  'to',
                    'topics',  'units', 'we', 'were', 'which', 'will', 'with', 'yet'])


### YOUR FUNCTIONS HERE


### Helper Functions ###

def get_soup_from_url(url):
    '''
    Input:
        url - absolute url
    Returns:
        BeautifulSoup object corresponding to url
    '''
    request = util.get_request(url)
    if request == None:
        return None
    text = util.read_request(request)
    soup = bs4.BeautifulSoup(text, "html5lib")

    return soup


####### Crawler Functions #######

def get_clean_urls(url, limiting_domain):
    '''
    Given a soup for a webpage, create and return a list of all 
    'a' tag urls in that soup that have been cleaned (absolute urls only)
    and 'ok' to follow

    Inputs:
        url - absolute url 
        limiting_domain - domain name
        used_links - list of links already visited
    Outputs:
        list of absolute urls
    '''
    soup = get_soup_from_url(url)
    all_a_tags = soup.find_all("a")
    # get urls (i.e. if tag has 'href' attribute)
    clean_urls = []
    for tag in all_a_tags:
        if tag.has_attr('href'):
            absolute = util.convert_if_relative_url(url, tag['href'])
            if not util.is_url_ok_to_follow(absolute, limiting_domain):
                continue
            util.remove_fragment(absolute)
            # protocol field reversion
            temp_request = util.get_request(absolute)
            if temp_request == None:
                continue
            reverted_url = util.get_request_url(temp_request)
            # is url ok to follow based on specification in PA2
            if util.is_url_ok_to_follow(reverted_url, limiting_domain):
                clean_urls.append(reverted_url)
    # remove duplicates
    final_url_list = []
    for link in clean_urls:
        if link not in final_url_list:
            final_url_list.append(link)

    return final_url_list


def get_course_tuples(starting_url, limiting_domain, num_max_links, dictionary):
    '''
    using a queue, create a FIFO ordered list of absolute urls to follow.
    As each url is processed by the queue, create a list of tuples with course
    codes as the key (not exceeding the number of urls specified)

    Inputs:
        starting_url - absolute url
        limiting_domain - domain name
        num_max_links - integer
    Outputs:
        list of tuples
    '''
    initial_urls = get_clean_urls(starting_url, limiting_domain)
    captured_links = []
    code_tuples = []
    link_count = len(initial_urls)

    # check if max_links exceeded
    if link_count >= num_max_links:
        for url in initial_urls[:num_max_links]:
            code_tuples += get_course_codes(url, dictionary)
        return code_tuples

    # create the queue   
    else: 
        url_queue = queue.Queue()
        for link in initial_urls:
            if link not in captured_links:
                captured_links.append(link)
                url_queue.put(link)

    # track traversed links
    final_links = []
    # update queue in FIFO order
    while (url_queue.empty() == False):
        if link_count >= num_max_links:
            return code_tuples

        next_link = url_queue.get()
        final_links.append(next_link)
        
        print(next_link)
        code_tuples += get_course_codes(next_link, dictionary)
        
        for link in get_clean_urls(next_link, limiting_domain):
            if link not in captured_links:
                captured_links.append(link)
                url_queue.put(link)
        link_count = len(final_links)
    
    return code_tuples


####### Indexing functions #######

def get_course_codes(url, dictionary, ignore=INDEX_IGNORE):
    '''
    for a given url, return a list of tuples that have the course code (found
    in dictionary parameter) and the acceptable words that correspond to it

    Inputs:
        url - absolute url
        dictionary - map of course titles to code
        ignore - list of strings

    Outputs:
        list of tuples
    '''
    soup = get_soup_from_url(url)
    divs = soup.find_all("div", class_="courseblock main")
    code_tuples = []
    # Maps course identifier to code
    for tag in divs:
        # Maps dependent on sequence or subsequence
        if util.find_sequence(tag) == []:
            course_identifier = get_course_identifier(tag)
            course_code = dictionary[course_identifier]
            course_words = get_course_words(tag, INDEX_IGNORE)
            code_tuples.append((course_code, course_words))
        else: 
            sequence = util.find_sequence(tag)
            for subsequence in sequence:
                course_identifier = get_course_identifier(subsequence)
                course_code = dictionary[course_identifier]
                course_words = get_course_words(subsequence, INDEX_IGNORE)
                code_tuples.append((course_code, course_words))
        
    return code_tuples


def get_course_identifier(tag):
    '''
    Input:
        tag - <div> tag with class_= "courseblock main"
    Output:
        string
   '''
    temp_id = tag.find_all("strong")[0].text.split()
    course_identifier = temp_id[0] + " " + temp_id[1][:5]
 
    return course_identifier
 
 
def get_course_words(tag, ignore):
    '''
    In a given <div> tag, return the words in the course title and course
    description that are not in the list of words to ignore
    Inputs:
        tag - <div> tag with class_= "courseblock main"
        ignore - list of words to ignore
    Ouput:
        list of strings
    '''
    # Pulls course title
    temp = tag.find_all("strong")[0].text.split()
    course_title = [temp[0]] + temp[2:(len(temp)-2)]
    
    # Pulls course description 
    temp_desc = tag.find_all("p", class_= "courseblockdesc")[0].text.split()
    course_desc = temp_desc[:len(temp_desc)-1]
 
    all_words = list(set(course_desc + course_title))
    final = []
    
    # Uses regex to clean strings
    for word in all_words:
        if word.isdigit() or word == '':
            continue
        fixed_word = re.sub(r'[^a-zA-Z ]', '', word).split()
        if fixed_word == [''] or fixed_word == []:
            continue
        final.append(fixed_word[0])

    fixed_final = [word.lower() for word in final if word.lower() 
                   not in ignore and len(word) > 1]
    return fixed_final



def tuples_to_csv(csv_file, word_tuples):
    '''
    turn a list of tuples that maps course codes to words and update/return
    a csv file

    Input:
        csv_file - csv formatted file 
        word_tuples - list of tuples
    Output:
        csv file (updated)
    '''
    with open(csv_file, 'w', newline='') as csvf:
        line_writer = csv.writer(csvf, delimiter = '|')
        for code_tuple in word_tuples:
            for word in code_tuple[1]:
                line_writer.writerow([code_tuple[0], word])
 
    return csvf


def go(num_pages_to_crawl, course_map_filename, index_filename):
    '''
    Crawl the college catalog and generates a CSV file with an index.

    Inputs:
        num_pages_to_crawl: the number of pages to process during the crawl
        course_map_filename: the name of a JSON file that contains the mapping
          course codes to course identifiers
        index_filename: the name for the CSV of the index.

    Outputs: 
        CSV file of the index index.
    '''

    starting_url = "http://www.classes.cs.uchicago.edu/archive/2015/winter/12200-1/new.collegecatalog.uchicago.edu/index.html"
    limiting_domain = "classes.cs.uchicago.edu"

    # Completes assignment
    dictionary = json.load(open(course_map_filename))
    word_tuples = get_course_tuples(starting_url, limiting_domain, num_pages_to_crawl, dictionary)
    
    return tuples_to_csv(index_filename, word_tuples)


if __name__ == "__main__":
    usage = "python3 crawl.py <number of pages to crawl>"
    args_len = len(sys.argv)
    course_map_filename = "course_map.json"
    index_filename = "catalog_index.csv"
    if args_len == 1:
        num_pages_to_crawl = 11
    elif args_len == 2:
        try:
            num_pages_to_crawl = int(sys.argv[1])
        except ValueError:
            print(usage)
            sys.exit(0)
    else:
        print(usage)    
        sys.exit(0)

    '''
    go(num_pages_to_crawl, course_map_filename, index_filename)
    '''
