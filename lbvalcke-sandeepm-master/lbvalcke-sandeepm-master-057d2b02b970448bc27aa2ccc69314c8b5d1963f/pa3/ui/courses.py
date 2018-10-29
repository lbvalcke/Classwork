### CS122, Winter 2017: Course search engine: search
###
### Sandeep Malladi & Luis Buenaventura

from math import radians, cos, sin, asin, sqrt
import sqlite3
import json
import re
import os


# Use this filename for the database
DATA_DIR = os.path.dirname(__file__)
DATABASE_FILENAME = os.path.join(DATA_DIR, 'course-info.db')


def find_courses(ui_args_dict):
    '''
    Takes a dictionary containing search criteria and returns courses
    that match the criteria.  The dictionary will contain some of the
    following fields:

      - dept a string
      - day is array with variable number of elements  
           -> ["'MWF'", "'TR'", etc.]
      - time_start is an integer in the range 0-2359
      - time_end is an integer an integer in the range 0-2359
      - enroll is an integer
      - walking_time is an integer
      - building ia string
      - terms is a string: "quantum plato"]

    Returns a pair: list of attribute names in order and a list
    containing query results.
    '''
    if not ui_args_dict:
        return ([], [])
    # connection and cursor to database
    connection = sqlite3.connect(DATABASE_FILENAME)
    connection.create_function("walk_time", 4, compute_time_between)
    db_cursor = connection.cursor()
    # get query and args for cursor
    (query, args) = get_query_and_args_from_dict(ui_args_dict)
    table = db_cursor.execute(query, args)
    # attribute list in order
    attributes = get_header(db_cursor)
    # table to list of results
    results = table.fetchall()
    connection.close()

    # replace with a list of the attribute names in order and a list
    # of query results.
    return (attributes, results)


def get_query_and_args_from_dict(arg_dict):
    '''
    take a dictionary of arguments containing search criteria
    and return a tuple of the form (query, args) where query
    is a string and args is a list of arguments that replace
    the '?' in query string
    '''
    # list of query items
    params = arg_dict.keys()
    # non-unique lists of select terms, tables --> refined below
    select_nu = []
    tables_nu = []
    # unique list of join criteria
    joins = []
    # list of tuples of where statement strings and corresponding args
    where = []
    # get select terms and tables first
    # courses table in all queries, so it is not added during loop
    for param in params:
        if param in ["dept", "terms"]:
            # select
            select_nu.append(("courses.dept", 1))
            select_nu.append(("courses.course_num", 2))
            select_nu.append(("courses.title", 10))
        if param in ["day", "time_start", "time_end"]:
            # select
            select_nu.append(("courses.dept", 1))
            select_nu.append(("courses.course_num", 2))
            select_nu.append(("sections.section_num", 3))
            select_nu.append(("meeting_patterns.day", 4))
            select_nu.append(("meeting_patterns.time_start", 5))
            select_nu.append(("meeting_patterns.time_end", 6))
            # tables
            tables_nu.append("meeting_patterns")
            tables_nu.append("sections")
        if param in ["walking_time", "building"]:
            # select
            select_nu.append(("courses.dept", 1))
            select_nu.append(("courses.course_num", 2))
            select_nu.append(("sections.section_num", 3))
            select_nu.append(("meeting_patterns.day", 4))
            select_nu.append(("meeting_patterns.time_start", 5))
            select_nu.append(("meeting_patterns.time_end", 6))
            # need to have two gps tables, a & b, for walk time
            select_nu.append(("a.building_code ", 7))
            select_nu.append(("walk_time(b.lon, b.lat, a.lon, a.lat) AS walking_time ", 8))
            # tables
            tables_nu.append("meeting_patterns")
            tables_nu.append("sections")
            tables_nu.append("gps AS a")
        if param in ["enroll_lower", "enroll_upper"]:
            # select
            select_nu.append(("courses.dept", 1))
            select_nu.append(("courses.course_num", 2))
            select_nu.append(("sections.section_num", 3))
            select_nu.append(("meeting_patterns.day", 4))
            select_nu.append(("meeting_patterns.time_start", 5))
            select_nu.append(("meeting_patterns.time_end", 6))
            select_nu.append(("sections.enrollment", 9))
            # tables
            tables_nu.append("meeting_patterns")
            tables_nu.append("sections")
    # get unique query terms for output
    select_final_terms = [x[0] for x in sorted(list(set(select_nu)), key = lambda tup: tup[1])]
    # unique list of tables (other than courses table)
    tables_final = list(set(tables_nu))
    # based on tables, create ON criteria for joins
    # if gps in tables, sections MUST be in tables
    if "gps AS a" in tables_final:
        joins.append("sections.building_code = a.building_code")
    if "sections" in tables_final:
        joins.append("courses.course_id = sections.course_id")
    if "terms" in params:
        joins.append("courses.course_id = catalog_index.course_id")
        tables_final.append("catalog_index")
    # if meeting patterns in tables, sections MUST be in tables
    if "meeting_patterns" in tables_final:
        joins.append("sections.meeting_pattern_id = meeting_patterns.meeting_pattern_id")
    # specify where statements based on parameters, track args in tuple
    if "terms" in params:
        words = arg_dict["terms"].split()
        q_marks = ["?" for word in words]
        where.append(("catalog_index.word IN (" + ",".join(q_marks) + ")", words))
    if "dept" in params:
        where.append(("courses.dept = ?", arg_dict["dept"]))
    if "day" in params:
        days = arg_dict["day"]
        q_marks = ["?" for day in days]
        where.append(("meeting_patterns.day IN (" + ",".join(q_marks) + ")", days))
    if "time_start" in params:
        where.append(("meeting_patterns.time_start >= ?", arg_dict["time_start"]))
    if "time_end" in params:
        where.append(("meeting_patterns.time_end <= ?", arg_dict["time_end"]))
    if "enroll_lower" in params:
        where.append(("sections.enrollment >= ?", arg_dict["enroll_lower"]))
    if "enroll_upper" in params:
        where.append(("sections.enrollment <= ?", arg_dict["enroll_upper"]))
    if "walking_time" in params:
        where.append(("walking_time <= ?", arg_dict["walking_time"]))
    # build query
    query = []
    arg_list = []
    # Select / From
    query.append("SELECT ")
    query.append(", ".join(select_final_terms))
    query.append(" FROM courses ")
    # Joins
    if tables_final != []:
        if "sections" in tables_final:
            query.append("JOIN sections ")
        if "catalog_index" in tables_final:
            query.append("JOIN catalog_index ")
        if "meeting_patterns" in tables_final:
            query.append("JOIN meeting_patterns ")
        #if "gps" in tables_final:
        #    query.append("JOIN gps ")
        if "gps AS a" in tables_final:
            query.append("JOIN gps AS a ")
            query.append("JOIN (SELECT building_code, lon, lat FROM gps WHERE building_code = ?) AS b ")
            arg_list.append(arg_dict["building"])
    # ON statements
    if joins != []:
        query.append("ON ")
        query.append(" AND ".join(joins))
    # Where conditions
    query.append(" WHERE ")
    n = len(where)
    m = 0
    for tup in where:
        query.append(tup[0])
        m += 1
        if m < n:
            query.append(" AND ")
        if type(tup[1]) == list:
            for arg in tup[1]:
                arg_list.append(arg)
        else:
            arg_list.append(tup[1])
    if "terms" in params:
        if "sections" in tables_final:
            query.append(" GROUP BY sections.section_id HAVING COUNT(*) = ?")
            arg_list.append(len(arg_dict["terms"].split()))
        else:
            query.append(" GROUP BY courses.course_id HAVING COUNT(*) = ?")
            arg_list.append(len(arg_dict["terms"].split()))

    return ("".join(query), arg_list)


    


########### auxiliary functions #################
########### do not change this code #############

def compute_time_between(lon1, lat1, lon2, lat2):
    '''
    Converts the output of the haversine formula to walking time in minutes
    '''
    meters = haversine(lon1, lat1, lon2, lat2)

    #adjusted downwards to account for manhattan distance
    walk_speed_m_per_sec = 1.1 
    mins = meters / (walk_speed_m_per_sec * 60)

    return mins


def haversine(lon1, lat1, lon2, lat2):
    '''
    Calculate the circle distance between two points 
    on the earth (specified in decimal degrees)
    '''
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 

    # 6367 km is the radius of the Earth
    km = 6367 * c
    m = km * 1000
    return m 



def get_header(cursor):
    '''
    Given a cursor object, returns the appropriate header (column names)
    '''
    desc = cursor.description
    header = ()

    for i in desc:
        header = header + (clean_header(i[0]),)

    return list(header)


def clean_header(s):
    '''
    Removes table name from header
    '''
    for i in range(len(s)):
        if s[i] == ".":
            s = s[i+1:]
            break

    return s



########### some sample inputs #################

example_0 = {"time_start":930,
             "time_end":1500,
             "day":["MWF"]}

example_1 = {"building":"RY",
             "dept":"CMSC",
             "day":["MWF", "TR"],
             "time_start":1030,
             "time_end":1500,
             "enroll_lower":20,
             "terms":"computer science",
             "walking_time": 100}

