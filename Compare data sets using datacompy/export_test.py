# importing the requests library 
import requests 
# importing csv module 
import csv 
from io import StringIO
import pandas as pd
import datacompy
import json

# csv file name 
filename = "something.csv"

# initializing the titles and rows list 
fields = [] 
rows = [] 

# api 
_id = "id"
env = "base url"
status = "status"

# api-endpoint 
URL = "url endpoint with string formatting"

PARAMS = {'status': status} 
# sending get request and saving the response as response object 
r = requests.get(url = URL,params = PARAMS).json()
total_pages = int(r['data']['meta']['total_pages'])
print(r['data']['meta']['total_pages'])

# results will be appended to this list
all_time_entries = []

# loop through all pages and return JSON object
for page in range(1, total_pages+1):
    page = page
    limit = 10
    # defining a params dict for the parameters to be sent to the API 
    PARAMS = {'page':page,'limit':limit, 'status': status} 
    # hit url for paginated data        
    response = requests.get(url=URL,params = PARAMS).json()   
    # get dictionary data from response and appned to the list by iterating
    for data_dict in response['object1']['object2']:
        all_time_entries.append(data_dict) 
    page += 1
# prettify JSON
data = json.dumps(all_time_entries, sort_keys=True, indent=4)
#print(data)

print("\n.................Printing Data Start from Csv file......................\n\n")
# reading csv file 
with open(filename, 'r') as csvfile: 
    # creating a csv reader object 
    csvreader = csv.reader(csvfile) 
    # extracting field names through first row 
    fields = next(csvreader) 
    # extracting each data row one by one 
    for row in csvreader: 
        rows.append(row) 
    # get total number of rows 
    print("Total no. of rows: %d"%(csvreader.line_num)) 
# printing the field names 
print('Field names are:' + ', '.join(field for field in fields)) 
#  printing first 5 rows 
print('\nFirst 5 rows are:\n') 
for row in rows[:5]: 
    # parsing each column of a row 
    for col in row: 
        print("%10s"%col), 
    print('\n') 
print("\n.................Printing Data End from Quest Csv file......................\n\n")

# adding two datasets in pandas dataframe 
df1 = pd.DataFrame(all_time_entries)
df2 = pd.read_csv(filename)

print(df1.head())
print(df2.head())

# compare
compare = datacompy.Compare(
    df1,
    df2,
    #join_columns=['column_name'], #You can also specify a list of columns
    #on_index = True,
    join_columns='column_name',
    abs_tol=0, #Optional, defaults to 0
    rel_tol=0, #Optional, defaults to 0
    df1_name='api_name', #Optional, defaults to 'df1'
    df2_name='Csv_data_name' #Optional, defaults to 'df2'
    )

# result boolean
print("DataComPy Result: ",compare.matches(ignore_extra_columns=True))
# This method prints out a human-readable report summarizing and sampling differences
print(compare.report())

print("\n.................Printing Start Unique Rows for df1(APi)......................\n\n")
# print unique rows df1
print(compare.df1_unq_rows)
print("\n.................Printing End Unique Rows for df1(APi)......................\n\n")

print("\n.................Printing Start Unique Rows for df2(Csv)......................\n\n")
# print unique rows df2
print(compare.df2_unq_rows)
print("\n.................Printing End Unique Rows for df2(Csv)......................\n\n")

print("\n.................Printing Start Unique Columns for df1(APi)......................\n\n")
# print unique columns df1
print(compare.df1_unq_columns())
print("\n.................Printing End Unique Columns for df1(APi)......................\n\n")

print("\n.................Printing Start Unique Columns for df2(Csv)......................\n\n")
# print unique columns df2
print(compare.df2_unq_columns())
print("\n.................Printing End Unique Columns for df2(Csv)......................\n\n")

