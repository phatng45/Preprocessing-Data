"""This program fills in the missing values of specified attributes in a csv file.
The csv file should be comma-separated.
Depending whether the attribute is nominal or numeric, specific filling methods can be used.
If the attribute is nominal, the filling method is by the mode of the attribute.
If the attribute is numeric, user can select between the mean or the median of the attribute.
This program assumes that all data have equal weights of 1.

Command line: --in=[csv_path] --out=[output_path] --attributes=[attribute_indices] --num_method=[mean|median] | --help
    --in: Path to the input csv file for this program to check.
        For example: --in=a.csv, --in="a b c.csv"
    --out: Path to the output csv file after the data has been filled.
        If not specified, the default will be "output_fill_missing_values_" + input_file_name + ".csv".
        For example: --in=a.csv, --in="a b c.csv"
    --attributes: List of attribute indices to check, separated by comma, with no space inbetween.
        The "all" keyword can be used to specify all attributes detected as missing data.
        For example: --attributes=1,2,3,4 or --attributes=all
    --num_method: Specify the filling method for numeric attributes.
        By default, the filling method is "mean".
        For example: --num_method=mean or --num_method=median
    --help: See this documentation

Output:
    A csv file identical to the input csv with all the missing data filled.
"""

import sys
import os
import pandas as pd
from list_missing_cols import isNaN, list_missing_cols


def mean(data: 'list') -> 'float':
    """Calculate mean value of a numeric list, assuming all values have equal weights of 1.

    Args:
        data (list): Iterable numeric value list

    Returns:
        float: The mean value of the list
    """
    # If the data list is empty, mean is 0
    if len(data) == 0:
        return 0
    total: float = sum(data)
    return total / len(data)


def median(data: 'list') -> 'float':
    """Calculate median value of a numeric list, assuming all values have equal weights of 1.

    Args:
        data (list): Iterable numeric value list

    Returns:
        float: The median value of the list
    """
    # Sort the list in ascending order first
    data.sort()
    # If number of elements is odd, return the middle value
    size = len(data)
    # If the data list is empty, median is 0
    if size % 2 == 1:
        return data[int(size / 2)]
    else:
        # If the number of elements is even, return the average of 2 middle values, assuming it's 0-based index
        half = int(size / 2)
        return (data[half] + data[half - 1]) / float(2)


def modeNominal(data: 'list') -> 'str':
    """Get the mode value of a nominal list, assuming all values have equal weights of 1.

    Args:
        data (list): Iterable nominal value list

    Returns:
        str: The string value that has the most frequency in the list
    """
    counter = {}
    for value in data:
        count = counter.get(value, 0)
        if count == 0:
            counter.setdefault(value, 1)
        else:
            counter[value] += 1
    # If the data list is empty, we don't know the mode, just give "Unknown"
    if len(counter) == 0:
        return "Unknown"
    return max(counter, key=counter.get)


def fill_missing_values(data: 'pd.DataFrame', attrIndex: 'list', numeric_fill=mean) -> 'pd.DataFrame':
    """Fill the missing data in the data frame.
    If the data is nominal, it's filled with the mode of the attribute.
    If the data is numeric, it's filled with either mean or median of the attribute, specified by numeric_fill
    Specify the attributes to fill using a list of indices in attrIndex

    Returns:
        pandas.DataFrame: A copy of the original data frame, with filled data
    """
    # Iterate through each column in the specified attribute list
    for colIndex in attrIndex:
        # If the attribute is nominal, get the mode value of the column
        # By default, pandas read string values from csv as 'object' type
        filler = 0
        if data.dtypes[colIndex] == object:
            filler = modeNominal(
                [x for x in data.iloc[:, colIndex].tolist() if not isNaN(x)])
        else:
            # If the attribute is numeric, use the specified filling method from the parameter
            filler = numeric_fill(
                [x for x in data.iloc[:, colIndex].tolist() if not isNaN(x)])
        # Iterate through elements in the column, if an element is missing value, replace it with the filler
        for i in range(data.shape[0]):
            if isNaN(data.iloc[i, colIndex]):
                data.iat[i, colIndex] = filler
    return data


def main():
    args = sys.argv
    parse_error = "Invalid command line arguments. Please use \"--help\" flag to see the documentation."
    help_msg = """
This program fills in the missing values of specified attributes in a csv file.
The csv file should be comma-separated.
Depending whether the attribute is nominal or numeric, specific filling methods can be used.
If the attribute is nominal, the filling method is by the 'mode' of the attribute.
If the attribute is numeric, user can select between the 'mean' or the 'median' of the attribute.
This program assumes that all data have equal weights of 1.

Command line: --in=[csv_path] --out=[output_path] --attributes=[attribute_indices] --num_method=[mean|median] | --help
    --in: Path to the input csv file for this program to check.
        For example: --in=a.csv, --in="a b c.csv"
    --out: Path to the output csv file after the data has been filled.
        If not specified, the default will be "output.csv".
        For example: --out=a.csv, --out="a b c.csv"
    --attributes: List of attribute indices to check, separated by comma, with no space inbetween.
        The "all" keyword can be used to specify all attributes by default.
        For example: --attributes=1,2,3,4 or --attributes=all
    --num_method: Specify the filling method for numeric attributes.
        By default, the filling method is "mean".
        For example: --num_method=mean or --num_method=median
    --help: See this documentation

Output:
    A csv file identical to the input csv with all the missing data filled.
"""
    # Initialize a dictionary that specify the command line arguments
    spec = {
        "--in": str(),
        "--out": "hold",
        "--attributes": "all",
        "--num_method": mean,
        "--help": help_msg
    }

    # Parse the command line arguments
    if len(args) < 2 or len(args) > 5:
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
        elif (flag == "--in" and len(specVal) != 0) or (flag == "--out" and specVal != "hold") or (flag == "--attributes" and specVal == "all"):
            print("Can't use a flag twice. Please try again")
            return -1
        elif flag == "--help":
            print(specVal)
            return 0
        elif flag == "--in" or flag == "--out":
            if os.path.splitext(flagVal)[1] == ".csv":
                spec[flag] = flagVal
        elif flag == "--attributes":
            if flagVal != "all":
                try:
                    spec[flag] = [int(x)
                                  for x in flagVal.strip("\" ").split(",")]
                except ValueError:
                    print(
                        "Invalid attribute index values, please check the documentation using --help then try again.")
                    return -1
        elif flag == "--num_method":
            if flagVal == "median":
                spec[flag] = median
            elif flagVal != "mean":
                print(
                    "Invalid numeric filling method. See help with --help flag then try again.")
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

    # If attribute flag is specified as "all"
    if spec["--attributes"] == "all":
        spec["--attributes"] = [x[0]
                                for x in list_missing_cols(df.to_numpy().tolist(), df.columns.tolist())]

    # Fill in the missing values
    df = fill_missing_values(df, spec["--attributes"], spec["--num_method"])

    if spec["--out"] == "hold":
        spec["--out"] = "output_fill_missing_values_" + os.path.basename(spec["--in"])

    # Output the dataframe to csv
    df.to_csv(spec["--out"], index=False)

    return 0


if __name__ == "__main__":
    main()
