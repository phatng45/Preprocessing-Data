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

outputpath = 'output_feature_scaling_' + ATTRIBUTE + '_' + INPUTPATH
df.to_csv(outputpath, index = False)
print('EXPORTED TO ' + outputpath)