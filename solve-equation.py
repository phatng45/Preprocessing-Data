import pandas as pd
import sys

def solve_equation(df, EQUATION):
    """
    This function solves the equation on columns from the User's input 
    using eval().
    """

    # find all the attributes that involved in the function
    atts = [att for att in list(df.columns) if att in EQUATION]

    # init result list
    calc = []

    for i in range(len(df)):
        # the dictionary comprehension is applied to 
        # map each variable in the equation into its current row's value
        calc.append(eval(EQUATION, {att : df.loc[i, att] for att in atts}))

    return calc

######################################################## MAIN
arg = sys.argv

INPUTPATH = arg[1]
EQUATION = "".join(arg[2:]) # combine all remaining arguments to the equation

df = pd.read_csv(INPUTPATH) 
df.insert(len(df.columns), EQUATION, solve_equation(df,EQUATION))

outputpath = 'output_solve_equation_' + INPUTPATH
df.to_csv(outputpath, index = False)
print('EXPORTED TO ' + outputpath)