import pandas as pd
import numpy as np

morg_filename="../pa6/data/morg_d07.csv"

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
