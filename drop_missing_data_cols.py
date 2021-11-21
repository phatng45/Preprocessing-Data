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
import csv
import sys

def isNaN(value) -> bool:
    """
    Refer to list_missing_cols.py
    """
    return value != value or value is None or value == ''


def missing(line: list, PERCENTAGE: float, n: int) -> bool:
    """
    This function returns a boolean that indicates 
    whether the current row/col has more missing data 
    than the specified percentage.
    """

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

with open(INPUTPATH, newline='') as file:
    # cast csv file into list of list
    data = list(csv.reader(file))

# get the number of rows
n = len(data[1:])

# init removal list
waitingForRemoval = []

for j in range(len(data[0])):
    # get the current column
    col = [data[i][j] for i in range(n)]

    # if the current column is counted as missing
    if missing(col, PERCENTAGE, n):

        # append that column to removal list
        waitingForRemoval.append(j)

# remove elements using list comprehension
data = [[row[coli] 
        for coli in range(len(row)) 
        if coli not in waitingForRemoval] 
        for row in data]

outputpath = 'output_drop_missing_data_cols_' + os.path.basename(INPUTPATH)

with open(outputpath, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data)
    print('EXPORTED TO ' + outputpath)