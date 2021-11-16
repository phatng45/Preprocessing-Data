import pandas as pd
import sys


def isNaN(value) -> bool:
    return value != value


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
PERCENTAGE = float(arg[2])

df = pd.read_csv(INPUTPATH)
n = len(df)

for col in df:
    if missing(df[col], PERCENTAGE, n):
        df.drop(col, axis=1, inplace=True)

outputpath = 'output_missing_rows_' + INPUTPATH
df.to_csv(outputpath, index=False)
print('EXPORTED TO ' + outputpath)