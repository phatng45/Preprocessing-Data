"""
This program solves a specified equation from the data in a csv file.
The csv file should be comma-separated.
The parameter must be in the correct order in order for this program to function normally.

Command line: [csv_path] [equation] | --help
    csv_path: Path to the csv file for this program to check.
        For example: a.csv, "a b c.csv"
    equation: The equation that needed to be solved.
        The variables must be columns' name.
        Random spacing are acceptable.
        For example: att1 + att2 -      att3*att4
    
    --help: See this documentation

Output:
    A csv file identical to the input csv with a new column in the end that stores the equation's result.
    Output path is ''output_solve_equation_' + csv_path' and is not customizable.
"""

import os
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

if INPUTPATH == "--help":
    print("""
This program solves a specified equation from the data in a csv file.
The csv file should be comma-separated.
The parameter must be in the correct order in order for this program to function normally.

Command line: [csv_path] [equation] | --help
    csv_path: Path to the csv file for this program to check.
        For example: a.csv, "a b c.csv"
    equation: The equation that needed to be solved.
        The variables must be columns' name.
        Random spacing are acceptable.
        For example: att1 + att2 -      att3*att4
    
    --help: See this documentation

Output:
    A csv file identical to the input csv with a new column in the end that stores the equation's result.
    Output path is ''output_solve_equation_' + csv_path' and is not customizable.
""")
    quit()

EQUATION = "".join(arg[2:]) # combine all remaining arguments to the equation

df = pd.read_csv(INPUTPATH) 
df.insert(len(df.columns), EQUATION, solve_equation(df,EQUATION))

outputpath = 'output_solve_equation_' + os.path.basename(INPUTPATH)
df.to_csv(outputpath, index = False)
print('EXPORTED TO ' + outputpath)