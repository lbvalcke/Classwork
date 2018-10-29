# CS121: Benford's Law

import csv

def read_column_from_csv(filename, col_num, remove_header):
    '''
    Extract values the values in the specified column from the specific csv file.

    Input: 
        filename: string with the name of a CSV file 
        col_num: the number of the desired column (0 based)

    Returns:
        list of strings, or None if the file cannot be opened.
    '''
    with open(filename, "rU") as f:
        reader = csv.reader(f)

        rv = []

        header = next(reader)

        if not remove_header:
            rv = [header]

        for row in reader:
            rv.append(row[col_num])
        return rv

    # will only get here if the open failed.
    return None

