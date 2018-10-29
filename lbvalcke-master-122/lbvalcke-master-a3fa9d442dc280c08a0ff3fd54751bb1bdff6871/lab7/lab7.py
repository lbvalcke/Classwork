import pandas as pd
import numpy as np

morg_filename = "../pa6/data/morg_d07.csv"

#TASK 1
morg_df = pd.read_csv(morg_filename, index_col = 0)

#TASK 2
age_only = morg_df['age']

#TASK 3
specific_id = morg_df[morg_df.index == '1_2_2']

#TASK 4
first_four = morg_df[0:4]

#TASK 5
more_thirytfive = morg_df[morg_df.hours_worked_per_week >= 35]

ethnic_categories = ['Non-Hispanic', 'Mexican', 'PuertoRican', 
                     'Cuban', 'Dominican',
                     'Salvadoran', 'CentralAmericanExcludingSalvadoran', 
                     'SouthAmerican',  'OtherSpanish']

status_categories = ['Working',
                     'With a job but not at work',
                     'Layoff',
                     'Looking',
                     'Others1',
                     'Unable to work or disabled',
                     'Others2']

### convert ethnicity from code to categorical
morg_df["ethnicity_code"] = morg_df["ethnicity_code"].fillna(0)
morg_df["ethnicity_code"] = pd.Categorical.from_codes(morg_df["ethnicity_code"], ethnic_categories)
morg_df.rename(columns={"ethnicity_code":"ethnicity"}, inplace=True)

### add age bins
boundaries = range(16, 89, 8)
morg_df["age_bin"] = pd.cut(morg_df["age"], 
                            bins=boundaries,
                            labels=range(len(boundaries)-1),
                            include_lowest=True, right=False)

#TASK 6
morg_df["employment_status_code"] = morg_df["employment_status_code"] - 1 
morg_df["employment_status_code"] = pd.Categorical.from_codes(morg_df["employment_status_code"], status_categories)
morg_df.rename(columns={"employment_status_code":"employment_status"}, inplace=True)

#TASK 7
not_working = morg_df[morg_df.employment_status != 'Working']

#TASK 8
workin = morg_df[(morg_df.employment_status == 'Working') & (morg_df.hours_worked_per_week >= 35)]

#TASK 9
boundaries = range(0, 99, 9)
morg_df["hours_bin"] = pd.cut(morg_df["hours_worked_per_week"], 
                                   bins = boundaries, 
                                   labels = range(len(boundaries) - 1), 
                                   include_lowest = True, 
                                   right = True)

#TASK 10
morg_df["hours_bin"].value_counts().sort_index()

morg_df.groupby("hours_bin").size().sort_index
