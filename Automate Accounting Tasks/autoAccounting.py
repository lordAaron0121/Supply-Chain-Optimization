import pandas as pd

# Functions
def clean(file_raw, month):
    # Open file and start from line 5
    df_raw = pd.read_excel(file_raw, header = 5)
    df_raw.head()

    # Remove first lines
    df_clean = df_raw.copy()
    df_clean = df_clean.iloc[4: ]

    # Fill NA with '-' (string)
    for col in df_raw.columns[0:2]:
        df_clean[col] = df_clean[col].fillna('-')
    
    # Fill NA with 0 (numeric)
    for col in df_raw.columns[2:]:
        df_clean[col] = df_clean[col].fillna(0).round(1)

    # Trim column values
    df_clean.columns = [str(t).strip() for t in df_clean.columns]

    return df_clean

def process_month(df_clean, month):
    # Type
    df_clean['Type'] = df_clean[['Renting', 'Investment']].apply(
        lambda t: 'Rent.' if t['Renting'] == 'X' else 'Invest.' if t['Investment'] == 'X' else 'Purch.', axis = 1)

    # Quantity
    dict_qty = dict(zip(['Rent.', 'Purch.', 'Invest.'], ['Rental Units', 'Purchasing Units', 'Invests. Units']))
    df_clean['Qty'] = df_clean.apply(lambda t: t[dict_qty[t['Type']]], axis = 1)

    # Unit Cost
    dict_cost = dict(zip(['Rent.', 'Purch.', 'Invest.'], ['Unit Rental Cost per month', 'Purchasing Unit Cost', 'Invests. Unit Cost']))
    df_clean['Unit Cost'] = df_clean.apply(lambda t: t[dict_cost[t['Type']]], axis = 1)

    # Report dataframe
    df_report = df_clean[df_clean.columns[-3:]].copy()
    df_report.columns = [month + '-' + str(i) for i in df_report.columns]

    # Add Month
    df_month = pd.DataFrame([pd.Series(['', 'May', ''])])
    df_month.columns = df_report.columns

    # Concat
    df_report = pd.concat([df_month, df_report], ignore_index = False)

    # Reset index
    df_report.reset_index(inplace = True)

    return df_report


#####################################################

# Examples of filenames in a dictionary
list_files = ['DC-JAN-2017.xlsx', 'DC-FEB-2017.xlsx', 'DC-MAR-2017.xlsx','DC-APR-2017.xlsx', 'DC-MAY-2017.xlsx', 'DC-JUN-2017.xlsx',
             'DC-JUL-2017.xlsx', 'DC-AUG-2017.xlsx', 'DC-SEP-2017.xlsx','DC-OCT-2017.xlsx', 'DC-NOV-2017.xlsx', 'DC-DEC-2017.xlsx']

zip_loop = zip(list_files, [i[3:6] for i in list_files])

# Final report dataframe
df_report = pd.DataFrame()

for file_raw, month in zip_loop:
    # Import and Clean data
    df_clean = clean(file_raw, month)

    # Build Monthly report
    df_month = process_month(df_clean, month)

    # Merge with previous Months report
    if df_report.empty:
        df_report = df_month
    else:
        df_report = df_report.merge(df_month, on = 'index')

# Save final report
df_report.to_excel('Final Report.xlsx')
