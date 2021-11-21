"""
This program removes duplicate data in a csv file.
The csv file should be comma-separated.

Command line: [csv_path] | --help
    csv_path: Path to the csv file for this program to check.
        For example: a.csv, "a b c.csv"
    
    --help: See this documentation

Output:
    A csv file identical to the input csv with the duplicates removed.
    Output path is ''output_drop_duplicates_' + csv_path' and is not customizable.
"""

import csv
import os
import sys

arg = sys.argv

INPUTPATH = arg[1]

if INPUTPATH == "--help":
    print("""
This program removes duplicate data in a csv file.
The csv file should be comma-separated.

Command line: [csv_path] | --help
    csv_path: Path to the csv file for this program to check.
        For example: a.csv, "a b c.csv"
    
    --help: See this documentation

Output:
    A csv file identical to the input csv with the duplicates removed.
    Output path is ''output_drop_duplicates_' + csv_path' and is not customizable.
""")
    quit()

with open(INPUTPATH, newline='') as file:
    # cast csv file into list of list
    data = list(csv.reader(file))

# cast each instance (row) into tuple, then add it to set
# dict.fromkeys().keys() is a type of set that retains order
nondup = dict.fromkeys(list(map(tuple, data[1:]))).keys()
outputpath = 'output_drop_duplicates_' + os.path.basename(INPUTPATH)

with open(outputpath, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(data[0])
    writer.writerows(nondup)
    print('EXPORTED TO ' + outputpath)