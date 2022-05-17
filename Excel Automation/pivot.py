# import pandas as pd
# import numpy as np

# data = pd.read_csv('sales_data.csv', sep=";")
# print("There are {:,} transactions in the raw dataset.".format(len(data)))

# print("Start Processing ...")
# data['date'] = pd.to_datetime(data['date'])
# data['month'] = data['date'].dt.month
# data['year'] = data['date'].dt.year
# data['month-year'] = data[['month', 'year']].astype(str).apply(lambda t: t['month'].zfill(2) + '-' + t['year'], axis = 1)

# my_cols = [str(i).zfill(2) + '-' + str(j) for j in range(2013, 2018) for i in range(1, 13)]

# data_store = pd.pivot_table(data, values = 'sales', index = ['store', 'item'],
#                            columns = ['month-year'], aggfunc=np.sum).fillna(0)

# data_store.sort_values(['store', 'item'], ascending = [True, True], inplace = True)
# print("Processing is completed.")
# print("{:,} lines in your final report".format(len(data_store)))

# data_store = data_store[my_cols]

# print("Start saving report.")
# data_store.to_excel("sales_report.xlsx")
# print("Your report is saved.")

import pandas as pd
import numpy as np

# Import Dataframe
df = pd.read_csv('sales_data.csv', sep=";")
print("{:,} transactions in your raw data".format(len(df)))

# Format Date
print("Start Processing ...")
df['date'] = pd.to_datetime(df['date'])
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year
df['month-year'] = df[['month', 'year']].astype(str).apply(lambda t: t['month'].zfill(2) + '-' + t['year'], axis = 1)

# month year columns
my_cols = [str(i).zfill(2) + '-' + str(j) for j in range(2013, 2018) for i in range(1, 13)]

# pivot by store item
df_store = pd.pivot_table(df, values='sales', index=['store', 'item'],
                    columns=['month-year'], aggfunc=np.sum).fillna(0)

# sort by ascending order
df_store.sort_values(['store', 'item'], ascending = [True, True], inplace = True)
print("Processing is completed.")
print("{:,} lines in your final report".format(len(df_store)))

# reorder columns
df_store = df_store[my_cols]

# Final report
print("Start saving report.")
df_store.to_excel('sales_report.xlsx')
print("Your report is saved.")