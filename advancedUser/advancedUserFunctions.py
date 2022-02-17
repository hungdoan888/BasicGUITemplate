# -*- coding: utf-8 -*-
"""
Created on Fri Feb 11 08:54:00 2022

@author: hungd
"""

#%% Libraries

import pandas as pd

#%% For Testing

# inputCSV = r'C:\Users\hungd\Documents\Work\AR54\ARISE\testFiles\testInput.csv'
# uniqueID = 5
# numRec = 10

#%% Advanced User Function

def advancedUserDummyFunction(inputCSV, uniqueID, numRec, df_col):
    
    # Print columns df
    print('--- Columns ---')
    print(df_col)
    print('\n')
    
    # Read CSV
    df = pd.read_csv(inputCSV)
    
    # Get Row to put on top
    df_uniqueID = df[df['uniqueID'] == uniqueID]
    
    # Drop uniqueID row from df
    df = df.drop(df.index[df['uniqueID'] == uniqueID])
    
    # Drop df to only numRec Rows
    df = df.iloc[:numRec]
    
    # Concatenate
    df = pd.concat([df_uniqueID, df]).reset_index(drop=True)
    
    # Define columns to keep
    keepColumns = list(df_col['Name'][df_col['Include'] == 2])  # 2 = True, 0 = False
    df = df[keepColumns]
    return df
