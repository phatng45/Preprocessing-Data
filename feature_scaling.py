"""
This program normalizes/standardizes a column in a csv file.
The csv file should be comma-separated.
The parameter must be in the correct order in order for this program to function normally.

Command line: [csv_path] [attribute] [include] | --help
    csv_path: Path to the csv file for this program to check.
        For example: a.csv, "a b c.csv"
    attribute: The attribute that need to be normalized/standardized
        For example: att1
    include: The needed method for output, including:
        zscore: Standardize the column using Z Score method.
        minmaxscale: Normalize the column using Min-Max Scaling method
        all: both
    
    --help: See this documentation

Output:
    A csv file where the first column store the original value, the next column(s) store the value after being normalized/standardized.
    Output path is ''output_feature_scaling_' + csv_path' and is not customizable.
"""

import os
import pandas as pd 
import sys

def minmax(a: list) -> list:  
    """
    This function returns a list of values that 
    have been normalized.
    """
    Min = min(a)
    Max = max(a)
    
    # min-max scaling (Normalization)
    return [(x - Min) / (Max - Min) for x in a]

########################################################
def zscore(a: list) -> list:
    """
    This function returns a list of values that 
    have been standardized.
    """
    mean = sum(a) / len(a)
    
    # population standard deviation (do lech chuan)
    sum_temp = 0
    # a for loop is utilized instead of list comprehension to conserve memory
    for i in a:
        sum_temp += (i - mean) ** 2

    pstdev = (sum_temp / len(a)) ** (1 / 2)
    
    # z scores normalization (Standardization)
    return [(x - mean) / pstdev for x in a]

######################################################## MAIN
arg = sys.argv

INPUTPATH = arg[1]

if INPUTPATH == "--help":
    print("""
This program normalizes/standardizes a column in a csv file.
The csv file should be comma-separated.
The parameter must be in the correct order in order for this program to function normally.

Command line: [csv_path] [attribute] [include] | --help
    csv_path: Path to the csv file for this program to check.
        For example: a.csv, "a b c.csv"
    attribute: The attribute that need to be normalized/standardized
        For example: att1
    include: The needed method for output, including:
        zscore: Standardize the column using Z Score method.
        minmaxscale: Normalize the column using Min-Max Scaling method
        all: both
    
    --help: See this documentation

Output:
    A csv file where the first column store the original value, the next column(s) store the value after being normalized/standardized.
    Output path is ''output_feature_scaling_' + csv_path' and is not customizable.
""")
    quit()

ATTRIBUTE = arg[2]
INCLUDE = arg[3]

column = list(pd.read_csv(INPUTPATH)[ATTRIBUTE])
colNames = [ATTRIBUTE]
result = zip()
    
# handling INCLUDE option
    
if INCLUDE == 'all':
    colNames.extend(['Min-max Scaling', 'Z-Score'])
    result = zip(column, minmax(column), zscore(column))
    
elif INCLUDE == 'zscore':
    colNames.append('Z-Score')
    result = zip(column, zscore(column))
    
elif INCLUDE == 'minmaxscale':    
    colNames.append('Min-max Scaling')
    result = zip(column, minmax(column))
    
else:
    print("INVALID CONSTRUCTION.\n CLOSING PROGRAM..")
    quit()

# create a new DataFrame that stores the results
df = pd.DataFrame(result,columns = colNames)

outputpath = 'output_feature_scaling_' + ATTRIBUTE + '_' + os.path.basename(INPUTPATH)
df.to_csv(outputpath, index = False)
print('EXPORTED TO ' + outputpath)