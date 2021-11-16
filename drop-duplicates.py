import csv
import sys

arg = sys.argv

INPUTPATH = arg[1]

with open(INPUTPATH,newline='') as file:
    # cast csv file into list of list
    data = list(csv.reader(file))

# cast each instance (row) into tuple, then add it to set
# dict.fromkeys().keys() is a type of set that retains order
nondup = dict.fromkeys(list(map(tuple,data[1:]))).keys()

with open('output_drop_duplicates_' + INPUTPATH,'w',newline='') as file:
    writer = csv.writer(file)
    writer.writerow(data[0])
    writer.writerows(nondup)
    print('EXPORTED TO output_drop_duplicates_' + INPUTPATH)