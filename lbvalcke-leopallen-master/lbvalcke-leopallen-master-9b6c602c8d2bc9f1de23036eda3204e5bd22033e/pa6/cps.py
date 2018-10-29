# CS121: Current Population Survey (CPS)
#
# Authors: Luis Buenaventura (lbvalcke, 438594) and Leo Allen (leopallen, 800165)  
# Functions for mining CPS data
 
import csv
import math
import numpy as np
import os
import pandas as pd
import sys
import tabulate
import pa6_helpers
 
# Constants
HID = "h_id"
AGE = "age"
GENDER = "gender"
RACE = "race"
ETHNIC = "ethnicity"
STATUS = "employment_status"
HRWKE = "hours_worked_per_week"
EARNWKE = "earnings_per_week"
 
FULLTIME_MIN_WORKHRS = 35
 
# CODE_TO_FILENAME: maps a code to the name for the corresponding code
# file
CODE_TO_FILENAME = {"gender_code":"data/gender_code.csv",
                    "employment_status_code": "data/employment_status_code.csv",
                    "ethnicity_code":"data/ethnic_code.csv",
                    "race_code":"data/race_code.csv"}
 
 
# VAR_TO_FILENAME: maps a variable-of-interest to the name for the
# corresponding code file
VAR_TO_FILENAME = {GENDER: CODE_TO_FILENAME["gender_code"],
                        STATUS: CODE_TO_FILENAME["employment_status_code"],
                        ETHNIC: CODE_TO_FILENAME["ethnicity_code"],
                        RACE: CODE_TO_FILENAME["race_code"]}
 
 
def read_codes(file_name):
    '''
    Reads the file_name passed into the function to retrieve the categories
    the codes associated with that file map to
   
    Inputs:
       file_name: the directory location of a code to category mapping

    Returns: 
        categories: an array of the categorical descriptors that the code 
        values map to.
    '''
    conversion_df = pd.read_csv(file_name)
    categories = conversion_df[conversion_df.columns[1]].values
 
    return categories
 
 
def build_morg_df(morg_filename):
    '''
    Construct a DF from the specified file. Resulting dataframe will
    use categorical descriptors rather than coded values.
   
    Inputs:
       morg_filename: (string) filename for the morg file.
 
    Returns: 
        morg_df: formatted pandas dataframe
    '''
    morg_df = pd.read_csv(morg_filename)
    # Keeps track of code categories that need to be changed
    categories_to_change = list(morg_df.columns.values)[2:6]
   
    # Maps the code categories to str categories one at a time
    for category in categories_to_change:
        conversion_file_name = CODE_TO_FILENAME[category]
        conversion = read_codes(conversion_file_name)
       
        # Subtracts 1 from ethnicity code to get the range to start at 0
        if category != "ethnicity_code":
            morg_df[category] = pd.Categorical.from_codes(morg_df[category] - 1
                                , conversion)
 
        else:
            morg_df[category] = morg_df[category].fillna(value = 0)
            morg_df[category] = pd.Categorical.from_codes(morg_df[category], conversion)
 
    # Renames the columns
    morg_df.columns = [HID, AGE, GENDER, RACE, ETHNIC, STATUS, HRWKE, EARNWKE]
 
    return morg_df
 
 
def get_fulltime(df):
    '''
    Cuts the dataframe to only include full-time workers
 
    Input:
       df: morg dataframe
 
    Returns: 
        full_time_df: morg dataframe with only the rows associated with full
        time workers
    '''
    full_time_df = df[(df.hours_worked_per_week >= 35)
                    & (df.employment_status == "Working")]
 
    return full_time_df
 
 
def cut_by_gender(df, gender):
    '''
    Cuts the dataframe to only include people of a certain gender
 
    Input:
       df: morg dataframe
       gender: string variable representing the gender of interst
 
    Returns: 
        full_time_gendered: morg dataframe with only people of a certain gender
    '''
    if gender != "All":
        full_time_gendered_df = df[df.gender == gender]
    else:
        full_time_gendered_df = df
 
    return full_time_gendered_df
 
 
def cut_by_race(df, race):
    '''
    Cuts the dataframe to only include people of a certain race
 
    Input:
        df: morg dataframe
        race: string variable representing the race of interest
 
    Returns: 
        full_time_raced_df: morg data frame with only people of a certain race
    '''
    if race != "All":
        if race != "Other":
            full_time_raced_df = df[df.race == race]
        elif race == "Other":
            full_time_raced_df = df[df.race not in valid_race_input]
    else:
        full_time_raced_df = df
 
    return full_time_raced_df
 
 
def cut_by_ethnicity(df, ethnicity):
    '''
    Cuts the dataframe to only include people of a certain ethnicity
 
    Input:
        df: morg dataframe
        ethnicity: string variable represeting the ethnicity of interest
 
    Returns: 
        final_cut_df: a morg data frame with only people of a certain ethnicity
    '''
    if ethnicity != "All":
        if ethnicity == "Non-Hispanic":
            final_cut_df = df[df.ethnicity == ethnicity]
        elif ethnicity == "Hispanic":
            final_cut_df = df[df.ethnicity != "Non-Hispanic"]
    else:
        final_cut_df = df
 
    return final_cut_df
 
 
def calculate_weekly_earnings_stats_for_fulltime_workers(df, gender, race, ethnicity):
    '''
    Calculate statistics for different subsets of a dataframe.
 
    Inputs:
        df: morg dataframe
        gender: "Male", "Female", or "All"
        race: specific race from a small set, "All", or "Other",
            where "Other" means not in the specified small set
        ethnicity: "Hispanic", "Non-Hispanic", or "All"
 
    Returns: 
        (mean, median, min, max) for the rows that match the filter.
    '''
    full_time_df = get_fulltime(df)
    valid_gender_input = ["Male", "Female", "All"]
    valid_race_input = ["WhiteOnly", "BlackOnly", "AmericanIndian/AlaskanNativeOnly", "AsianOnly", "Hawaiian/PacificIslanderOnly", "Other", "All"]
    valid_ethnicity_input = ["Hispanic", "Non-Hispanic", "All"]
 
    # Retuns (0, 0, 0, 0) for invalid input
    if gender not in valid_gender_input:
        return (0, 0, 0, 0)
    if race not in valid_race_input:
        return (0, 0, 0, 0)
    if ethnicity not in valid_ethnicity_input:
        return (0, 0, 0, 0)
 
    # Cuts by gender signifier
    full_time_gendered_df = cut_by_gender(full_time_df, gender)
 
    # Cuts by race signifier
    full_time_raced_df = cut_by_race(full_time_gendered_df, race)
 
    # Cuts by ethnicity signifier
    final_cut_df = cut_by_ethnicity(full_time_raced_df, ethnicity)
 
    if final_cut_df.empty:
        return (0, 0, 0, 0)
 
    mean = final_cut_df.earnings_per_week.mean()
    median = final_cut_df.earnings_per_week.median()
    min_amt = final_cut_df.earnings_per_week.min()
    max_amt = final_cut_df.earnings_per_week.max()
 
    return (mean, median, min_amt, max_amt)
 
 
 
def create_histogram(df, var_of_interest, num_buckets, min_val, max_val):
    '''
    Compute the number of full time workers who fall into each bucket
    for a specified number of buckets and variable of interest.
 
    Inputs:
        df: morg dataframe
        var_of_interest: one of EARNWKE, AGE, HWKE
        num_buckets: the number of buckets to use.
        min_val: minimal value (lower bound) for the histogram (inclusive)
        max_val: maximum value (lower bound) for the histogram (non-inclusive).
 
    Returns:
        counts: a list of integers where ith element is the number of full
        time workers who fall into the ith bucket.
 
        empty list if num_buckets <= 0 or max_val <= min_val
    '''
    full_time_df = get_fulltime(df)
    # Defines the relevant bins
    bins = np.linspace(min_val, max_val, num = num_buckets, endpoint = False)
    bins = np.append(bins, max_val)
   
    # Tags each row with its applicable bin for the var of interest
    binned_groups = pd.cut(full_time_df[var_of_interest],
                            bins = bins,
                            include_lowest = True,
                            right = False)
   
    # Counts the bin occurrences
    counts = pd.value_counts(binned_groups.values, sort = False)
    counts = counts.tolist()
 
    return counts
 
 
def apply_df_conditions(age_range, var_of_interest, morg_df):
    '''
    Slices the morg dataframe such that the output includes only the entries 
    that are within the specified age range and are relevant to the variable
    of interest. 

    Inputs:
        age_range: (tuple of ints) (lower_bound, upper_bound)
        var_of_interest: string, one of "gender", "race", "ethnicity"
        morg_df: pandas dataframe - unsliced

    Outputs:
        total_var_df: pandas dataframe delimited by age and var_of_interest,
            includes everyone who's employment status is classified as "Looking", 
            "Working" or "Layoff"
        unemployed_var_df: pandas dataframe delimited by age and variable,
            includes only entries who's employment staus is classified as "Looking"
            or "Layoff" 
    '''
    # Applies age range and employment conditions to dataframe
    age_reduced_df = morg_df[(morg_df.age >= age_range[0])
                    & (morg_df.age <= age_range[1])]
    total_df = age_reduced_df[(age_reduced_df.employment_status == "Layoff")
                    | (age_reduced_df.employment_status == "Looking")
                    | (age_reduced_df.employment_status == "Working")]
    unemployed_df = total_df[(total_df.employment_status == "Layoff")
                    | (total_df.employment_status == "Looking")]
   
    # Limits set to variable of interest
    unemployed_var_df = unemployed_df[var_of_interest]
    total_var_df = total_df[var_of_interest]
 
    return total_var_df, unemployed_var_df
 
 
def calculate_proportions(total_var_df, unemployed_var_df, possible_values):
    '''
    Finds proportion of the subset of interest who are unemployed, stratified
    by the possible classifications indicated by the variable of interst in
    the calculate_unemployment_rate function. 

    Inputs:
        total_var_df: pandas dataframe with entries for the subset of interest
        unemployed_var_df: pandas dataframe with entries for the subset of
            interest who are unemployed.
        possible_values: array of possible stratifications that reflect the
            variable of interest. 

    Outputs:
        store_proportion: A list of the proportions of unemployed stratified by
        possible values of the variable of interest. 

    '''
    # For the possible values for the relevant variable
    # calculates the relevant unemployment rate
    store_proportion = []
    for value in possible_values:
       
        unemployed_count = unemployed_var_df[unemployed_var_df == value].shape[0]
        total_count = total_var_df[total_var_df == value].shape[0]
       
        if unemployed_count == 0 or total_count == 0:
            proportion = 0.0
        else:
            proportion = unemployed_count / total_count
       
        store_proportion.append(proportion)
 
    return store_proportion
 
 
def calculate_unemployment_rates(filenames, age_range, var_of_interest):
    '''
    Calculate the unemployment rate for participants in a given age range (inclusive)
    by values of the variable of interest.
 
    Inputs:
        filenames: (list of strings) list of morg filenames
        age_range: (tuple of ints) (lower_bound, upper_bound)
        var_of_interest: one of "gender", "race", "ethnicity"
 
    Returns: pandas dataframe
    '''
    # Initializes dictionary to hold unemployment rates
    d = {}
   
    # Checks that age range makes sense
    if age_range[0] > age_range[1]:
        return None
   
    # Defines the possible subgroups for the unemployment analysis
    file_name = VAR_TO_FILENAME[var_of_interest]
    possible_values = read_codes(file_name)
   
    for morg_filename in filenames:
       
        # Initializes list to store unemployment rate for the relevant year
        # Assures that the filename is just the filename
        manipulated_filename = os.path.basename(morg_filename)
        # Sets the year for the column
        # http://stackoverflow.com/questions/11339210/how-to-get-integer-values-from-a-string-in-python
        year = ''.join(num for num in manipulated_filename if num.isdigit())
        morg_df = build_morg_df(morg_filename)
       
        # Checks to make sure that the file is not empty
        if morg_df.empty:
            return None
            break
       
        total_var_df, unemployed_var_df = apply_df_conditions(age_range,
                                        var_of_interest,
                                        morg_df)
       
        store_proportion = calculate_proportions(total_var_df,
                                        unemployed_var_df,
                                        possible_values)
       
        # Stores unemployment rates in dictionary under the key
        # for the relevant year
        d[year] = store_proportion
 
    # Creates and sorts the dataframe so it matches the instructor's tables
    unemployment_df = pd.DataFrame(d, index = possible_values)
    unemployment_df = unemployment_df.reindex(unemployment_df.index.astype("str")).sort_index()
   
    # prints a fabulous table
    print(tabulate.tabulate(unemployment_df, unemployment_df.columns.values.tolist(),
                            "fancy_grid",
                            floatfmt=".2f"))
 
    return unemployment_df

    

    
    
