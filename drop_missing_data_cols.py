"""
This program removes the columns that have more missing values than a specified percentage in a csv file.
The csv file should be comma-separated.
The parameter must be in the correct order in order for this program to function normally.

Command line: [csv_path] [percentage] | --help
    csv_path: Path to the csv file for this program to check.
        For example: a.csv, "a b c.csv"
    percentage: The percentage that decides whether or not a column will be removed if it has less than this much data.
        The number must be in range of [0, 1]
        For example: 0.5
    
    --help: See this documentation

Output:
    A csv file identical to the input csv with the instances whose percentages of missing data exceed the specified percentage removed.
    Output path is ''output_drop_missing_data_cols_' + csv_path' and is not customizable.
"""
import os
import pandas as pd
import sys

def isNaN(value) -> bool:
    """
    Refer to list_missing_cols.py
    """
    return value != value or value is None

def missing(line, PERCENTAGE: float, n: int) -> bool:
    """
    This function returns a boolean that indicates 
    whether the current row/col has more missing data 
    than the specified percentage.
    """

    # line.count() returns the number of instances that
    # their value are not NaN.
    count = 0
    for e in line:
        if isNaN(e) == False:
            count += 1
    return (len(line) - count) / n > PERCENTAGE


######################################################## MAIN
arg = sys.argv

INPUTPATH = arg[1]

if INPUTPATH == "--help":
    print("""
This program removes the columns that have more missing values than a specified percentage in a csv file.
The csv file should be comma-separated.
The parameter must be in the correct order in order for this program to function normally.

Command line: [csv_path] [percentage] | --help
    csv_path: Path to the csv file for this program to check.
        For example: a.csv, "a b c.csv"
    percentage: The percentage that decides whether or not a column will be removed if it has less than this much data.
        The number must be in range of [0, 1]
        For example: 0.5
    
    --help: See this documentation

Output:
    A csv file identical to the input csv with the instances whose percentages of missing data exceed the specified percentage removed.
    Output path is ''output_drop_missing_data_cols_' + csv_path' and is not customizable.
""")
    quit()

PERCENTAGE = float(arg[2])

df = pd.read_csv(INPUTPATH)
n = len(df)
    
for col in df:
    if missing(df[col], PERCENTAGE, n):
        df.drop(col, axis=1, inplace=True)

outputpath = 'output_drop_missing_data_cols_' + os.path.basename(INPUTPATH)
df.to_csv(outputpath, index=False)
print('EXPORTED TO ' + outputpath)