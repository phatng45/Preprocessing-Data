"""This program counts the number of rows with missing data from a csv file.
The csv file should be comma-separated.

Command line: [csv_path] | --help
    csv_path: Path to the csv file for this program to check
    --help: See this documentation

Output:
    The number of rows with missing data
"""

import sys
import os
import pandas as pd
from list_missing_cols import isNaN


def count_missing_rows(data: 'list[list]') -> 'int':
    # Result is the number of rows containing missing data
    result = 0

    # Iterate through each row
    for row_index in range(len(data)):
        # Iterate through each column in row
        for col_index in range(len(data[0])):
            if isNaN(data[row_index][col_index]):
                result += 1
                break

    return result


def main():
    args = sys.argv
    filepath = args[1]

    # Print the documentation of this file if the user ask for help
    if filepath == "--help":
        print("""
This program counts the number of rows with missing data from a csv file.
The csv file should be comma-separated.

Command line: [csv_path] | --help
    csv_path: Path to the csv file for this program to check
    --help: See this documentation

Output:
    The number of rows with missing data
""")
        return 0

    # If the file path does not exist
    if not os.path.exists(filepath):
        print("Invalid file path: " + filepath + " - Please try again")
        return -1
    df = pd.read_csv(filepath)

    # Convert data frame to matrix (2D list)
    mat = df.to_numpy().tolist()

    # Print the result to the console
    print("The number of rows with missing data is:", count_missing_rows(mat))

    return 0


if __name__ == "__main__":
    main()
