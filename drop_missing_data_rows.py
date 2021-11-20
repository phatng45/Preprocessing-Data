"""
This program removes the rows that have more missing values than a specified percentage in a csv file.
The csv file should be comma-separated.

Command line: --in=[input_path] --out=[output_path] --percent=[integer] | --help
    --in: Path to the input csv file for this program to check.
        For example: --in=a.csv, --in="a b c.csv"
    --out: Path to the output csv file after the missing rows have been removed.
        For example: --out=a.csv, --out="a b c.csv"
        If not specified, the default will be "output_drop_missing_data_rows_" + input_file_name + ".csv".
    --percent: The percentage for the number of columns with missing data that is required for a row to be removed.
        Must be an integer in the range [0,100].
        If --percent=0 the program will remove any row with at least a missing column.
        If --percent=100 the program will only remove rows that don't contain any data
    --help: See this documentation

Output:
    A csv file with data from the input file that has the rows missing a percentage of columns removed.
"""

import sys
import os
import pandas as pd
from list_missing_cols import list_missing_cols


def drop_missing_rows(data: 'list[list]', percent: int) -> 'list[list]':
    """Remove rows with number of missing datas exceeds the percentage.

    Returns:
        list[list]: 2D list of the data table after removing the missing rows.
    """
    if len(data) == 0:
        return None
    columnNum = len(data[0])
    result = []
    for row in data:
        # Get number of missing data columns in a row
        missingNum = len(list_missing_cols([row], None))
        missingPercent = (float(missingNum) / columnNum) * 100
        if missingPercent >= percent and percent != 0:
            continue
        elif missingPercent > 0 and percent == 0:
            continue
        else:
            result.append(row)
    return result


def main():
    args = sys.argv
    parse_error = "Invalid command line arguments. Please use \"--help\" flag to see the documentation."
    help_msg = """
This program removes the rows that have more missing values than a specified percentage in a csv file.
The csv file should be comma-separated.

Command line: --in=[input_path] --out=[output_path] --percent=[integer] | --help
    --in: Path to the input csv file for this program to check.
        For example: --in=a.csv, --in="a b c.csv"
    --out: Path to the output csv file after the missing rows have been removed.
        For example: --out=a.csv, --out="a b c.csv"
        If not specified, the default will be "output_drop_missing_data_rows_" + input_file_name + ".csv".
    --percent: The percentage for the number of columns with missing data that is required for a row to be removed.
        Must be an integer in the range [0,100].
        If --percent=0 the program will remove any row with at least a missing column.
        If --percent=100 the program will only remove rows that don't contain any data.
        The default value is 0.
    --help: See this documentation

Output:
    A csv file with data from the input file that has the rows missing a percentage of columns removed.
"""
    # Initialize a dictionary that specify the command line arguments
    spec = {
        "--in": str(),
        "--out": "hold",
        "--percent": 0,
        "--help": help_msg
    }

    # Parse the command line arguments
    if len(args) < 2 or len(args) > 4:
        print(parse_error)
        return -1
    for arg in args[1:]:
        # For each argument in the argument list
        # If the argument is missing the flag starter "--", it's invalid
        if not arg.startswith("--"):
            print(parse_error)
            return -1
        # Split the argument into flag name and flag value
        splitted = arg.split("=")
        flag = splitted[0]
        flagVal: str = ""
        if len(splitted) == 2:
            flagVal = splitted[1]
        # Handle the flag
        # If the flag name is invalid
        specVal = spec.get(flag, None)
        if specVal is None:
            print(parse_error)
            return -1
        # If the flag has already been used
        elif (flag == "--in" and len(specVal) != 0) or (flag == "--out" and specVal != "hold"):
            print("Can't use a flag twice. Please try again")
            return -1
        elif flag == "--help":
            print(specVal)
            return 0
        elif flag == "--in" or flag == "--out":
            if os.path.splitext(flagVal)[1] == ".csv":
                spec[flag] = flagVal
        elif flag == "--percent":
            try:
                spec[flag] = int(flagVal)
                if spec[flag] < 0 or spec[flag] > 100:
                    print("The percentage value must be in range [0,100].")
                    return -1
            except ValueError:
                print(
                    "Invalid percentage values, please check the documentation using --help then try again.")
                return -1
        else:
            print(parse_error)
            return -1

    # Read input csv
    if not os.path.exists(spec["--in"]):
        print("Invalid input file path. Please try again")
        return -1

    # Read the data file and separate it into data and headers
    df = pd.read_csv(spec["--in"])

    # Fill in the missing values
    df = pd.DataFrame(drop_missing_rows(df.to_numpy().tolist(), spec["--percent"]), columns=df.columns)

    if spec["--out"] == "hold":
        spec["--out"] = "output_drop_missing_data_rows_" + os.path.basename(spec["--in"])

    # Output the dataframe to csv
    df.to_csv(spec["--out"], index=False)

    return 0


if __name__ == "__main__":
    main()
