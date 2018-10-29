# CS122: Linking restaurant records in Zagat and Fodor's list
# 
# Sandeep Malladi and Luis Buenaventura 
#
# CNET IDs sandeepm & lbvalcke


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import jellyfish
import util

def find_matches(mu, lambda_, outfile='./matches.csv', block_on=None):
    '''
    Completes the pa
    '''
    zagat_file = 'zagat.txt'
    fodor_file = 'fodors.txt'
    pairs_file = 'known_pairs.txt'    
    
    # clean text files to dataframes
    merged_matches, zagat_df, fodors_df = df_to_matches(zagat_file, 
                                                        fodor_file, 
                                                        pairs_file) 
    # unmatches - 1000 rows of randomly sampled pairs
    unmatches_df = get_unmatches_df(zagat_df, fodors_df)
    # get scores
    match_score_df, unmatch_score_df = match_unmatch_jw_scores(merged_matches, 
                                                              unmatches_df, 0)
    # get vector values (i.e. score -> category)
    vector_matches_df, vector_unmatches_df = get_vector_values(match_score_df, 
                                                                 unmatch_score_df)
    possible_vectors = gen_vectors(3)
    # calculate relative frequencies of vector ocurrences
    vectors_and_counts = calculate_relative_freq(vector_matches_df, vector_unmatches_df, 0)
    # 27 vectors split in to 3 groups based on mu and lambda_
    part_possible_df, part_match_df, part_unmatch_df = vector_partition(vectors_and_counts, 
                                                                                 mu, lambda_)

    # get all zagat - fodor pairs
    zagat_df['key'] = 1
    fodors_df['key'] = 1
    total_df = pd.merge(zagat_df, fodors_df, how='outer', on='key')
    del total_df['key']
    del total_df['zagat_index']
    del total_df['fodors_index']
    # rename columns to match 'unmatch_df' parameter in jw score calculating function
    total_df.columns = ['z_nameaddress', 'z_restaurant_name', 'z_address', 'z_city',
                           'f_nameaddress', 'f_restaurant_name', 'f_address', 'f_city']
    # get Jaro-Winkler scores ; only want total_match scores
    scored_total_df = match_unmatch_jw_scores(merged_matches, total_df, 1)
    # vector values for scored total match
    total_df_vectors = get_vector_values(pd.DataFrame(), scored_total_df, 1)
    # block on is either "address", "city", or "name"
    # only want vectors where corresponding component is equal to 2 (match)
    if block_on == "name":
        col = "vector_x"
        total_df_blocked = total_df_vectors.loc[total_df_vectors[col] == 2]
    elif block_on == "address":
        col = "vector_y"
        total_df_blocked = total_df_vectors.loc[total_df_vectors[col] == 2]
    elif block_on == "city":
        col = "vector_z"
        total_df_blocked = total_df_vectors.loc[total_df_vectors[col] == 2]
    else:
        total_df_blocked = total_df_vectors

    total_vector_counts_df = calculate_relative_freq(pd.DataFrame(), total_df_blocked, 1)
    # compare vectors to 3 partitions groups to determine counts by group
    # update counts in counts df
    final_counts_df = pd.DataFrame()
    final_counts_df["possible"] = 0
    final_counts_df["matches"] = 0
    final_counts_df["unmatches"] = 0
    # intiialize counts    
    final_possible_count = 0
    final_match_count = 0
    final_unmatch_count = 0
    # loop through total_counts_df to get partition counts
    for index, row in total_vector_counts_df.iterrows():
        if index in part_possible_df.index.tolist():
            final_possible_count += row["total_count"]
        elif index in part_match_df.index.tolist():
            final_match_count += row["total_count"]
        elif index in part_unmatch_df.index.tolist():
            final_unmatch_count += row["total_count"]
    # set partition count values
    final_counts_df.set_value(0, "possible", final_possible_count)
    final_counts_df.set_value(0, "unmatches", final_unmatch_count)
    final_counts_df.set_value(0, "matches", final_match_count)

    # build match df
    final_match_df = pd.DataFrame(columns=total_df_blocked.columns.tolist())
    for index, row in part_match_df.iterrows():
        data = total_df_blocked.loc[(total_df_blocked["vector_x"] == row["vector_x"]) &
                                    (total_df_blocked["vector_y"] == row["vector_y"]) &
                                    (total_df_blocked["vector_z"] == row["vector_z"])]
        final_match_df = final_match_df.append(data)
    # matches with zagat and fodors name addresses in to csv
    final_match_df = final_match_df[['z_nameaddress', 'f_nameaddress']]
    final_match_df.to_csv(outfile)

    return (final_counts_df["matches"][0], final_counts_df["possible"][0], final_counts_df["unmatches"][0])

def get_cleaned_df_from_file(text_file):
    '''
    given text file (like zagat or fodors), clean data and return
    original string in first column, restaurant name in second column,
    address in third column, city in fourth column
    
    Input:
        text_file - text file where each line is info 
                    for a different restaurant
    Returns:
        pandas dataframe
    '''
    st_list = ['\.', 'Sq.', 'Blvd.', 'W.', 'PCH', ' St.', 'Rd.', 'Center', 'Way', 'Plaza', 'Ave.', 'Sts.', 'Road']

    df = pd.read_csv(text_file, header = None, 
                     names = ["nameaddress"], 
                     dtype = {'nameaddress': str})

    # get name in column 0 and remainder of string in column 1
    df = df['nameaddress'].str.extract(r'^([^\d]*)(\d.*)$', expand=True)

    # insert original nameaddress string in leading column
    df.insert(0, 'nameaddress', df[0] + df[1])

    # address extract
    # need first assignment to zero to prevent errors with second assignment
    df[2] = 0
    df[2] = df[1].str.extract('^(.*(' + '|'.join(st_list) + r'))(.*?)$', expand=True) 
    
    # city extract (opposite of address extract
    df[3] = 0
    df[3] = df[1].str.extract('^(?:.*(?:' + '|'.join(st_list) + r'))(.*?)$', expand=True)
    
    # no longer need df[1] (it includes address and city)
    df.drop(1, axis = 1, inplace = True)
    df.columns = ['nameaddress', 'restaurant_name', 'address', 'city']
    
    df.fillna("String", inplace=True)
    
    # Hardcode df changes by file name
    if text_file == "zagat.txt":
        df.set_value(69,"address", '642 Broadway')
        df.set_value(69,"city", 'Chinatown')
        df.set_value(100,"address", '2450 Broadway')
        df.set_value(100,"city", 'New York City')
        df.set_value(117,"address", '2090 Broadway')
        df.set_value(117,"city", 'New York City')
        df.set_value(128,"address", '2199 Broadway')
        df.set_value(128,"city", 'New York City')
        df.set_value(150,"nameaddress", 'Oyster Bar lower level New York City')
        df.set_value(150,"restaurant_name", 'Oyster Bar')
        df.set_value(150,"address", 'lower level')
        df.set_value(150,"city", 'New York City')
        df.set_value(155,"address", '178 Broadway')
        df.set_value(155,"city", 'Brooklyn')
        df.set_value(159,"nameaddress", 'Rainbow Room 30 Rockefeller Plaza New York City')
        df.set_value(176,"nameaddress", 'Tavern on the Green Central Park West New York City')
        df.set_value(176,"restaurant_name", 'Tavern on the Green')
        df.set_value(176,"address", 'Central Park West')
        df.set_value(176,"city", 'New York City')
        df.set_value(277,"address", '220 Sandy Springs Circle')
        df.set_value(277,"city", 'Atlanta')
  
    if text_file == "fodors.txt":
        df.set_value(0,"address", '2930 Beverly Glen Circle')
        df.set_value(0, "city", 'Los Angeles')
        df.set_value(2,"address", '12224 Ventura Blvd.')
        df.set_value(2, "city", 'Studio City')
        df.set_value(29,"address", '8358 Sunset Blvd.')
        df.set_value(29, "city", 'West Hollywood')
        df.set_value(114, "address", '160 Central Park S')
        df.set_value(114, "city", 'New York')
        df.set_value(223, "address", '160 Central Park S')
        df.set_value(223, "city", 'New York')
        df.set_value(287, "address", '240 Central Park S')
        df.set_value(287, "city", 'New York')
        df.set_value(356, "nameaddress", 'Dante\'s Down the Hatch  Underground Underground Mall  Underground Atlanta Atlanta')
        df.set_value(356, "restaurant_name", 'Dante\'s Down the Hatch')
        df.set_value(356, "address", 'Underground Underground Mall')
        df.set_value(356, "city", 'Underground Atlanta Atlanta')
        df.set_value(371, "nameaddress", 'La Grotta at Ravinia Dunwoody Rd.  Holiday Inn/Crowne Plaza at Ravinia  Dunwoody Atlanta')
        df.set_value(371, "restaurant_name", 'La Grotta at Ravinia Dunwoody Rd.')
        df.set_value(371, "address", 'Holiday Inn/Crowne Plaza at Ravinia')
        df.set_value(371, "city", 'Dunwoody Atlanta')
        df.set_value(372, "nameaddress", 'Little Szechuan C Buford Hwy.  Northwoods Plaza  Doraville Atlanta')
        df.set_value(372, "restaurant_name", 'Little Szechuan')
        df.set_value(372, "address", 'C Buford Hwy.  Northwoods Plaza')
        df.set_value(372, "city", 'Doraville Atlanta')
        df.set_value(378, "nameaddress", 'Mi Spia Dunwoody Rd.  Park Place  across from Perimeter Mall  Dunwoody Atlanta')
        df.set_value(378, "restaurant_name", 'Mi Spia')
        df.set_value(378, "address", 'Dunwoody Rd.  Park Place  across from Perimeter Mall')
        df.set_value(378, "city", 'Dunwoody Atlanta')
        df.set_value(396, "nameaddress", 'Toulouse B Peachtree Rd. Atlanta')
        df.set_value(396, "address", 'Peachtree Rd.')
        df.set_value(396, "city", 'Atlanta')
        df.set_value(454, "address", '804 Northpoint')
        df.set_value(454, "city", 'San Francisco')
        df.set_value(456, "address", '732 Broadway')
        df.set_value(456, "city", 'San Francisco') 
        df.set_value(461, "nameaddress", 'Garden Court Market and New Montgomery Sts. San Francisco')
        df.set_value(461, "restaurant_name", 'Garden Court Market') 
        df.set_value(461, "address", 'Market and New Montgomery Sts.')
        df.set_value(461, "city", 'San Francisco')
        df.set_value(462, "nameaddress", 'Gaylord\'s Ghirardelli Sq. San Francisco ')
        df.set_value(462, "restaurant_name", 'Gaylord\'s')
        df.set_value(462, "address", 'Ghirardelli Sq.' )
        df.set_value(462, "city", 'San Francisco')
        df.set_value(464, "nameaddress", 'Greens Bldg. A Fort Mason San Francisco ')
        df.set_value(464, "restaurant_name", 'Greens')
        df.set_value(464, "address", 'Bldg. A Fort Mason')
        df.set_value(464, "city", 'San Francisco')
        df.set_value(470, "address", '430 Broadway')
        df.set_value(470, "city", 'San Francisco')
        df.set_value(491, "nameaddress", 'McCormick & Kuleto\'s Ghirardelli Sq. San Francisco')
        df.set_value(491, "restaurant_name", 'McCormick & Kuleto\'s')
        df.set_value(491, "address", 'Ghirardelli Sq.')
        df.set_value(491, "city", 'San Francisco')
        df.set_value(512, "address", '108 South Park')
        df.set_value(512, "city",  ' San Francisco')
        df.set_value(513, "address", 'Embarcadero 4')
        df.set_value(513, "city", 'San Francisco')
        df.set_value(514, "address",'150 Redwood Alley')
        df.set_value(514, "city", 'San Francisco')
        
    return df


def get_clean_matches_df(text_file = "known_pairs.txt"):
    '''
    process text in known_pairs.txt to create a cleaned datafram

    Input:
        text_file - a text file, particularly the known pairs text file

    Output:
        pandas dataframe with two columns
    '''
    df = pd.read_csv(text_file, names = ["initial_text"], 
                     error_bad_lines = False)
    
    # need two more rows to complete cleaning, one temp and one clean
    df["temp"] = 0
    df["cleaned"] = 0
    
    # get NaN for rows that have pertinent information in a temporary column
    df["temp"] = df["initial_text"].str.extract(r'^(.*?)(\#)(?:.*?)$', 
                                                expand=True)
    
    # populate "cleaned" with info in "temp", but fill NaNs...
    # with "initial_text" --> left with empty rows or match info strings
    df["cleaned"] = df["temp"].fillna(df["initial_text"])
    
    # no longer need initial_text or temp column
    df.drop("initial_text", inplace = True, axis = 1)
    df.drop("temp", inplace = True, axis = 1)

    # some matches extend in to 3 rows, move partial row in to the one above it
    for index, row in df.iterrows():
        x = len(row["cleaned"].split())
        if x <= 4 and x >= 1 and index > 1:
            temp = df.loc[index - 1]["cleaned"].split() + row["cleaned"].split()
            df.loc[index - 1]["cleaned"] = ' '.join(temp)
            df.loc[index]["cleaned"] = ''

     # remove empty rows by replacing them with nan, then using dropna
    df["cleaned"].replace('', np.nan, inplace = True)
    df.dropna(subset = ['cleaned'], inplace = True)

    # create new df with each row representing a matched pair
    # zagat in one column and fodors in the other. 
    # code from http://stackoverflow.com/questions/36181622
    final_df = pd.DataFrame({'zagat':df['cleaned'].iloc[::2].values, 
                             'fodors':df['cleaned'].iloc[1::2].values})
    
    final_df["fodors"][46] = "Caf&eacute;  Ritz-Carlton  Buckhead,3434 Peachtree Rd. Atlanta Georgia"
    final_df["zagat"][46] = 'Ritz-Carlton Cafe (Buckhead) 3434 Peachtree Rd. NE Atlanta'
    
    return final_df


def df_to_matches(zagat_file, fodor_file, pairs_file):
    '''
    Inputs:
        zagat_file - text file string
        fodor_file - text file string
        pairs_file - text file string

    Output:
        3 cleaned and formatted pandas dataframes - matches, zagat, and fodors
    '''
    #Create zagat_df and add index column
    zagat_df = get_cleaned_df_from_file(zagat_file)
    zagat_df['zagat_index'] = zagat_df.index

    #Create fodors_df and add index column
    fodors_df = get_cleaned_df_from_file(fodor_file)
    fodors_df['fodors_index'] = fodors_df.index
    
    #Create matches_df
    matches_df = get_clean_matches_df(pairs_file)

    merged_matches = pd.merge(matches_df, zagat_df, how='left', left_on='zagat', right_on = 'nameaddress')


    merged_matches = pd.merge(merged_matches, fodors_df, how='left', left_on='fodors', right_on = 'nameaddress')

    zagat_hardcode = [1, 15, 17, 19, 26, 34, 46]
    correct_zagat = [107, 81, 308, 256, 159, 68, 267]
    fodors_hardcode = [8, 10, 15, 16, 21, 23, 26, 34, 35, 40, 44, 46]
    correct_fodors = [370, 363, 71, 380, 66, 209, 276, 58, 321, 361, 243, 347]
    zagat_columns = ["nameaddress_x","restaurant_name_x","address_x","city_x", "zagat_index"]
    fodors_columns = ["nameaddress_y","restaurant_name_y","address_y","city_y", "fodors_index"]
    
    merged_matches[["zagat_index", "fodors_index"]] = merged_matches[["zagat_index", "fodors_index"]].fillna(0)
    merged_matches = merged_matches.fillna("String")

    for index, row in merged_matches.iterrows():
        if index in zagat_hardcode:
            zagat_index = correct_zagat.pop(0)
            merged_matches.set_value(index, "nameaddress_x", zagat_df.loc[zagat_index, "nameaddress"])
            merged_matches.set_value(index, "restaurant_name_x", zagat_df.loc[zagat_index, "restaurant_name"])
            merged_matches.set_value(index, "address_x", zagat_df.loc[zagat_index, "address"])
            merged_matches.set_value(index, "city_x", zagat_df.loc[zagat_index, "city"])
            merged_matches.set_value(index, "zagat_index", zagat_df.loc[zagat_index, "zagat_index"])
        if index in fodors_hardcode:
            fodors_index = correct_fodors.pop(0)
            merged_matches.set_value(index, "nameaddress_y", fodors_df.loc[fodors_index, "nameaddress"])
            merged_matches.set_value(index, "restaurant_name_y", fodors_df.loc[fodors_index, "restaurant_name"])
            merged_matches.set_value(index, "address_y", fodors_df.loc[fodors_index, "address"])
            merged_matches.set_value(index, "city_y", fodors_df.loc[fodors_index, "city"])
            merged_matches.set_value(index, "fodors_index", fodors_df.loc[fodors_index, "fodors_index"])

    
    merged_matches[["zagat_index", "fodors_index"]] = merged_matches[["zagat_index", "fodors_index"]].astype(int)
    merged_matches.drop(["zagat", "fodors"], axis=1, inplace=1)

    return merged_matches, zagat_df, fodors_df


def get_unmatches_df(zagat_df, fodors_df):
    '''
    create and return a dataframe of two columns - one with 1000 random zagat
    restaurants and one with 1000 random fodors restaurants

    Input:
        zagat_df - text file string
        fodors_df - text file string

    Output:
        pandas dataframe - unmatches_df with 1000 rows and 8 columns
    '''

    # get random sample from zagat and reset index from zero for join
    z_unmatch_df = zagat_df.sample(1000, replace = True)
    z_unmatch_df = z_unmatch_df.reset_index(drop = True)
    z_unmatch_df.drop("zagat_index", axis=1, inplace=1)

    # get random sample from fodors and reset index from zero
    f_unmatch_df = fodors_df.sample(1000, replace = True)
    f_unmatch_df = f_unmatch_df.reset_index(drop = True)
    f_unmatch_df.drop("fodors_index", axis=1, inplace=1)

    
    # Renaming columns 
    z_unmatch_df.columns = ['z_nameaddress', 'z_restaurant_name', 'z_address', 'z_city']
    f_unmatch_df.columns = ['f_nameaddress', 'f_restaurant_name', 'f_address', 'f_city']
    
    # Join randomized-sample zagat and fodors dfs on index
    unmatch_df = z_unmatch_df.join(f_unmatch_df, how = 'left')

    return unmatch_df


def match_unmatch_jw_scores(match_df, unmatch_df, plot=0):
    '''
    given match and unmatch dataframes, calculate Jaro-Winkler scores for 
    restaurant names, addresses, and cities between zagat and fodor items.
    Then, create and save histograms of the JW scores to a pdf
    '''
    # Produce JW scores for unmatches
    # for general use JW score calculation
    for index, row in unmatch_df.iterrows():
        if not row.isnull().values.any():
            name_score = jellyfish.jaro_winkler(row["z_restaurant_name"], row["f_restaurant_name"])
            address_score = jellyfish.jaro_winkler(row["z_address"], row["f_address"])
            city_score = jellyfish.jaro_winkler(row["z_city"], row["f_city"])
            unmatch_df.set_value(index, "jw_restaurant_names", name_score)
            unmatch_df.set_value(index, "jw_address", address_score)
            unmatch_df.set_value(index, "jw_city", city_score)     

    if plot == 0:
        # Produce JW scores for matches
        for index, row in match_df.iterrows():
            if not row.isnull().values.any():
                name_score = jellyfish.jaro_winkler(row["restaurant_name_x"], row["restaurant_name_y"])
                address_score = jellyfish.jaro_winkler(row["address_x"], row["address_y"])
                city_score = jellyfish.jaro_winkler(row["city_x"], row["city_y"])
                match_df.set_value(index, "jw_restaurant_names", name_score)
                match_df.set_value(index, "jw_address", address_score)
                match_df.set_value(index, "jw_city", city_score)   

        # Drop plot if exists
        plt.clf()
        # Create plots
        plt.figure(1)
        # Names
        plt.subplot(321)
        plt.hist(match_df["jw_restaurant_names"])   
        plt.title("Names from Matches", fontsize=12)
        plt.xlabel('Jaro-Winkler Score', fontsize=8)
        plt.ylabel('Frequency', fontsize=8)
        plt.subplot(322)
        plt.hist(unmatch_df["jw_restaurant_names"])   
        plt.title("Names from Unmatches", fontsize=12)
        plt.xlabel('Jaro-Winkler Score', fontsize=8)
        plt.ylabel('Frequency', fontsize=8)
        # Addresses
        plt.subplot(323)
        plt.hist(match_df["jw_address"])   
        plt.title("Addresses from matches", fontsize=12)
        plt.xlabel('Jaro-Winkler Score', fontsize=8)
        plt.ylabel('Frequency', fontsize=8)
        plt.subplot(324)
        plt.hist(unmatch_df["jw_address"])   
        plt.title("Addresses from unmatches", fontsize=12)
        plt.xlabel('Jaro-Winkler Score', fontsize=8)
        plt.ylabel('Frequency', fontsize=8)
        # City
        plt.subplot(325)
        plt.hist(match_df["jw_city"])   
        plt.title("Cities from matches", fontsize=12)
        plt.xlabel('Jaro-Winkler Score', fontsize=8)
        plt.ylabel('Frequency', fontsize=8) 
        plt.subplot(326)
        plt.hist(unmatch_df["jw_city"])   
        plt.title("Cities from unmatches", fontsize=12)
        plt.xlabel('Jaro-Winkler Score', fontsize=8)
        plt.ylabel('Frequency', fontsize=8)     

        # Format and save to file
        plt.tight_layout()
        plt.savefig('histograms.pdf')

        return match_df, unmatch_df

    else:
        return unmatch_df


def get_vector_values(matches_df, unmatches_df, val=0):
    '''
    Input:
        matches_df and unmatches_df with Jaro-Winkler scores calculated
        val - int (if 0, return vector values for both dfs;
                   if 1, return vector values for second df in params)
    Output:
        parameter dataframes with x y z vector value columns
    '''
    # assign vectors to matches_df
    for index, row in matches_df.iterrows():
        x = util.get_jw_category(row["jw_restaurant_names"])
        y = util.get_jw_category(row["jw_address"])
        z = util.get_jw_category(row["jw_city"])
        matches_df.set_value(index, "vector_x", x)
        matches_df.set_value(index, "vector_y", y)
        matches_df.set_value(index, "vector_z", z)
    
    # assign vectors to unmatches_df
    for index, row in unmatches_df.iterrows():
        x = util.get_jw_category(row["jw_restaurant_names"])
        y = util.get_jw_category(row["jw_address"])
        z = util.get_jw_category(row["jw_city"])
        unmatches_df.set_value(index, "vector_x", x)
        unmatches_df.set_value(index, "vector_y", y)
        unmatches_df.set_value(index, "vector_z", z)

    # to make the function applicable for use on any scored dataframe
    # specify return conditions
    if val == 0:
        return matches_df, unmatches_df
    else:
        return unmatches_df



def gen_vectors(len_v):
    '''
    recursively create list of permutation lists of length len_v, where len_v is 
    an integer. permutations include integers 0 to len_v
    '''
    if len_v == 1:
        return [[0],[1],[2]]
    else:
        return [[y]+x for x in gen_vectors(len_v - 1) for y in range(0,3)]


def calculate_relative_freq(v_matches_df, v_unmatches_df, val=0):
    '''   
    given matches and unmatches dataframes with corresponding vector information,
    create and return a dataframe that shows possible vectors, their counts in matches
    and unmatches, and their relative frequencies

    Inputs:
        v_matches_df - pandas df
        v_unmatches_df - pandas df
        val - int 1 or 0 (if 0, add match and unmatch count, if 1 only count for second param)

    Output:
        pandas df
    '''
    # get possible vectors
    vector_list = gen_vectors(3)
    # build possible_vectors df
    x_list = [l[0] for l in vector_list] 
    y_list = [l[1] for l in vector_list] 
    z_list = [l[2] for l in vector_list]
    possible_vectors_df = pd.DataFrame({'vector_x' : x_list, 
                                        'vector_y' : y_list, 
                                        'vector_z' : z_list})
    if val == 0:
        for vector in vector_list:
            # calculate counts
            match_count = v_matches_df[(v_matches_df.vector_x == vector[0]) &
                                       (v_matches_df.vector_y == vector[1]) &
                                       (v_matches_df.vector_z == vector[2])].count(axis=0, numeric_only=True)
            unmatch_count = v_unmatches_df[(v_unmatches_df.vector_x == vector[0]) &
                                           (v_unmatches_df.vector_y == vector[1]) &
                                           (v_unmatches_df.vector_z == vector[2])].count(axis=0, numeric_only=True)
            # get index at which vector occurs                        
            idx = possible_vectors_df[(possible_vectors_df["vector_x"] == vector[0]) &
                                      (possible_vectors_df["vector_y"] == vector[1]) &
                                      (possible_vectors_df["vector_z"] == vector[2])].index.tolist()
            # set frequency counts
            possible_vectors_df.set_value(idx[0], "match_count", match_count[0])
            possible_vectors_df.set_value(idx[0], "unmatch_count", unmatch_count[0])
        
        # get/set relative frequency
        possible_vectors_df["prob_m"] = (possible_vectors_df["match_count"] / 
                                         possible_vectors_df["match_count"].sum())
        possible_vectors_df["prob_u"] = (possible_vectors_df["unmatch_count"] / 
                                         possible_vectors_df["unmatch_count"].sum())

    if val == 1:
        # only want to use second df param (specifically for counting total_df in top function)    
        for vector in vector_list:
            total_count = v_unmatches_df[(v_unmatches_df.vector_x == vector[0]) &
                                         (v_unmatches_df.vector_y == vector[1]) &
                                         (v_unmatches_df.vector_z == vector[2])].count(axis=0, numeric_only=True)        
            idx = possible_vectors_df[(possible_vectors_df["vector_x"] == vector[0]) &
                                      (possible_vectors_df["vector_y"] == vector[1]) &
                                      (possible_vectors_df["vector_z"] == vector[2])].index.tolist()

            possible_vectors_df.set_value(idx[0], "total_count", total_count[0])
        # no need for probabilities

    return possible_vectors_df



def vector_partition(frequencies_df, mu, lambda_):
    '''
    Partitions 27 vectors based on mu and lambda and training data set. 
    Inputs:
        frequencies_df: pandas datafram
        mu: scalar parameter
        lamba: scalar parameter
    Output:
        Returns data frames with vector components of each type
    '''
    possible_vectors = []
    match_vectors = []
    unmatch_vectors = []

    frequencies_df["possible_vectors"] = np.where((frequencies_df.prob_m == 0) & 
                                                   (frequencies_df.prob_u == 0), 1, 0)
    
    # separate possible vectors in to own df
    possible_vectors_df = frequencies_df.loc[frequencies_df.possible_vectors == 1]
    frequencies_df = frequencies_df.loc[frequencies_df.possible_vectors != 1]

    # for remaining vectors, order and calculate necessary values
    frequencies_df["uw_0"] = np.where((frequencies_df.possible_vectors != 1) & 
                                                   (frequencies_df.prob_u == 0), 0, 1)
    frequencies_df["mw_uw"] = frequencies_df.prob_m / frequencies_df.prob_u
    frequencies_df["mw_uw"].fillna(0, inplace=True)

    # ordering
    # split frequencies in to two dfs, one where uw = 0 and one where uw = 1
    # order each dataframe correctly and then append back together
    uw_0_df = frequencies_df.loc[frequencies_df["uw_0"] == 0]
    uw_1_df = frequencies_df.loc[frequencies_df["uw_0"] == 1]
    uw_1_df.sort(columns="mw_uw", axis=0, ascending=False, inplace=True)
    frequencies_df = uw_0_df.append(uw_1_df)

    # get cumulative sums for uw descending and mw ascending
    frequencies_df["cumsum_uw"] = frequencies_df["prob_u"].cumsum(axis=0, skipna=True)
    frequencies_df["cumsum_mw"] = frequencies_df.iloc[::-1]["prob_m"].cumsum(axis=0, skipna=True)
    match_vectors_df = frequencies_df.loc[frequencies_df["cumsum_uw"] <= mu]
    frequencies_df = frequencies_df.loc[frequencies_df["cumsum_uw"] > mu]
    # separate match and unmatch vectors in to own dfs by respective cumsum value
    # then drop the values from frequencies df

    unmatch_vectors_df = frequencies_df.loc[frequencies_df["cumsum_mw"] <= lambda_]
    frequencies_df = frequencies_df.loc[frequencies_df["cumsum_mw"] > lambda_]

    possible_vectors_df = possible_vectors_df.append(frequencies_df, ignore_index=False, 
                                                     verify_integrity=True)

    return possible_vectors_df, match_vectors_df, unmatch_vectors_df


if __name__ == '__main__':

    num_m, num_p, num_u = find_matches(0.005, 0.005, './matches.csv', 
                                       block_on=None)

    print("Found {} matches, {} possible matches, and {} " 
              "unmatches with no blocking.".format(num_m, num_p, num_u))
