# -*- coding: utf-8 -*-
"""
Created on Fri Feb 11 08:54:00 2022

@author: hungd
"""

#%% Imports

import os
import pandas as pd
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QWidget, QTableWidgetItem
from registry import loadFromRegistry
from registry import saveToRegistry
from fileDialog import fileDialogBox
from advancedUserFunctions import advancedUserDummyFunction

#%% For Testing 

inputCSV = r'C:\Users\hungd\Documents\Work\AR54\ARISE\code\testFiles\testInput.csv'

#%% Main

class AdvancedUser(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uiFile = os.path.join(os.environ['PARENTDIR'], 'advancedUser/advancedUser.ui')
        uic.loadUi(uiFile, self)
        
        # Define Variables
        self.df = None
        self.df_col = None
        
        # Set Line Edit Values from Registry
        self.initiateValues()
        
        # Connect Line Edits
        self.connectLineEdits()
        
        # Connect Buttons
        self.connectButtons()
        
        # Create Dirs
        createDirs()
        
    # Set Line Edit Values and create initial plots
    def initiateValues(self):
        # Get registry
        registry, _ = loadFromRegistry()
        
        # Populate line edit fields
        self.lineEdit_inputCSV.setText(registry.get('advancedUser.inputCSV', 'testInput.csv'))  # inputCSV
        self.lineEdit_uniqueID.setText(registry.get('advancedUser.uniqueID', '10'))  # inputCSV
        
    # Save line edits to registry every time it changes
    def connectLineEdits(self):
        self.lineEdit_inputCSV.textChanged.connect(lambda: saveToRegistry('advancedUser.inputCSV', self.lineEdit_inputCSV.text()))  # inputCSV
        self.lineEdit_uniqueID.textChanged.connect(lambda: saveToRegistry('advancedUser.uniqueID', self.lineEdit_uniqueID.text()))  # uniqueID date

    # Def Buttons connected
    def connectButtons(self):
        self.pushButton_inputCSV.clicked.connect(self.selectFile)
        self.pushButton_getColNames.clicked.connect(self.getColNames)
        self.pushButton_getSimRows.clicked.connect(self.getSimRows)
        self.pushButton_exportResults.clicked.connect(self.exportResults)
        
    # Select Constituents File
    def selectFile(self):
        filepath = os.path.split(self.lineEdit_inputCSV.text())[0]
        filename = fileDialogBox(initialdir=filepath, title="Select Input CSV file", filetypes="*.csv")
        self.lineEdit_inputCSV.setText(filename)
        
    # Get Column names
    def getColNames(self):
        # Input CSV
        inputCSV = self.lineEdit_inputCSV.text()
        
        # Get column names from CSV
        self.colNames = pd.read_csv(inputCSV, nrows=1).columns.tolist()
        
        # Fill in column names
        self.fillColumnsTable()
        
        # Fill in check boxes
        self.insertCheckBoxes()
                        
    # Fill in Columns Table
    def fillColumnsTable(self):
        # Clear table
        self.tableWidget_col.setRowCount(1)  # Bring down to only header row for buy
        
        # Set number of rows
        newRowCount = len(self.colNames) + 1
        self.tableWidget_col.setRowCount(newRowCount) 
        
        # Fill values for Column Table
        for i in range(len(self.colNames)):
            self.tableWidget_col.setItem(i+1, 0, QTableWidgetItem(self.colNames[i]))
            
    # Insert Check boxes in columns table
    def insertCheckBoxes(self):
        for i in range(1, len(self.colNames)+1):
            for j in range(1, 4):
                chkBoxItem = QTableWidgetItem()
                chkBoxItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                chkBoxItem.setCheckState(QtCore.Qt.Checked)
                
                # Set Check State to 0 if checked
                if ((j == 1 and self.checkBox_include.checkState() == 0) or
                    (j == 2 and self.checkBox_weigh.checkState() == 0) or 
                    (j == 3 and self.checkBox_impute.checkState() == 0)):
                    chkBoxItem.setCheckState(QtCore.Qt.Unchecked)
                    
                self.tableWidget_col.setItem(i, j, chkBoxItem) 
                
    # Create df columns capturing checkbox state
    def createColumnsDf(self):
        # Include checkboxes
        includeStatus = []
        for i in range(1, len(self.colNames)+1):
            includeStatus.append(self.tableWidget_col.item(i, 1).checkState())
            
        # weigh checkboxes
        weighStatus = []
        for i in range(1, len(self.colNames)+1):
            weighStatus.append(self.tableWidget_col.item(i, 2).checkState())
            
        # impute checkboxes
        imputeStatus = []
        for i in range(1, len(self.colNames)+1):
            imputeStatus.append(self.tableWidget_col.item(i, 3).checkState())
            
        # Create col df
        df_col = pd.DataFrame({'Name': self.colNames,
                               'Include': includeStatus,
                               'Weigh More': weighStatus,
                               'Impute': imputeStatus})
        self.df_col = df_col
            
    # Get Similar Rows
    def getSimRows(self):
        # Create df col table
        self.createColumnsDf()
        
        # Define Variables
        inputCSV = self.lineEdit_inputCSV.text()       # Input CSV
        uniqueID = int(self.lineEdit_uniqueID.text())  # Unique ID
        numRec = int(self.comboBox.currentText())      # Number of Recommendations
        df_col = self.df_col                           # Define column entries
        
        # Run advanced User Dummy Function
        self.df = advancedUserDummyFunction(inputCSV, uniqueID, numRec, df_col)
        
        # Write Results to Table
        self.writeDfsToTables()
    
    # Write Results to Table
    def writeDfsToTables(self):
        # Define Variables
        df = self.df
        keepColumns = list(df.columns)
        
        # Clear table
        self.tableWidget.setRowCount(1)  # Bring down to only header row for buy
        self.tableWidget.setColumnCount(len(keepColumns))  # Set Column Count
        
        # Rename Columns in Similarity table to only the ones we care about
        for j in range(len(keepColumns)):
            self.tableWidget.setItem(0, j, QTableWidgetItem(keepColumns[j]))
        
        # Set number of rows
        newRowCount = max(len(df), 20)  # At least 20 rows looks good
        self.tableWidget.setRowCount(newRowCount)    
        
        # Fill values for Similarity table
        for i in range(df.shape[0]):
            for j in range(df.shape[1]):
                self.tableWidget.setItem(i+1, j, QTableWidgetItem(str(df.iloc[i,j])))
                
    # Export Results
    def exportResults(self):
        self.df.to_csv(r'..\results\advancedUserResults.csv', index=False)
        print('Results Exported')
        print(r'Location: \results\advancedUserResults.csv')
        
#%% Create Results Folder

def createDirs():
    # Paths
    output = r"..\results"
    
    # Results
    if not os.path.exists(output):
        os.makedirs(output)
                
                