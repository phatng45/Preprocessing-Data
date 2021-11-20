"""This program lists out the columns that have missing data in a csv file.
The csv file should be comma-separated.

Command line: [csv_path] | --help
    csv_path: Path to the csv file for this program to check
    --help: See this documentation

Output:
    A list of columns that have missing data
"""

import sys
import os
import pandas as pd


def isNaN(value):
    """Function to check if a data cell is missing value

    Args:
        value: A data value or data cell in data frame

    Returns:
        True: If the value is NaN or none
        False: If the value is available
    """
    return value != value or value is None


def list_missing_cols(data: 'list[list]', colnames: 'list[str] | None') -> 'list[tuple]':
    """List out columns with missing data

    Returns:
        list[tuple]: A list of columns with missing data as tuples of (index, name)
    """
    # Result is a list of tuple of column index - column name
    result: list[tuple] = []

    # Iterate through each column
    for col_index in range(len(data[0])):
        # Iterate through each element in column
        for row_index in range(len(data)):
            if isNaN(data[row_index][col_index]):
                if colnames is not None:
                    result.append((col_index, colnames[col_index]))
                else:
                    result.append((col_index, ""))
                break

    return result


def main():
    args = sys.argv
    filepath = args[1]

    # Print the documentation of this file if the user ask for help
    if filepath == "--help":
        print("""
This program lists out the columns that have missing data in a csv file.
The csv file should be comma-separated.

Command line: [csv_path] | --help
    csv_path: Path to the csv file for this program to check
    --help: See this documentation

Output:
    A list of columns that have missing data
""")
        return 0

    # If the file path does not exist
    if not os.path.exists(filepath):
        print("Invalid file path: " + filepath + " - Please try again")
        return -1
    df = pd.read_csv(filepath)

    # Get column names and dataset sizes
    colnames = df.columns.tolist()
    mat = df.to_numpy().tolist()

    result = list_missing_cols(mat, colnames)

    # Print the result to the console
    if (len(result) == 0):
        print("No column has missing data!")
    else:
        print("Columns with missing data (index - name):")
        for col in result:
            print(col[0], '-', col[1])

    return 0


if __name__ == "__main__":
    main()
