# -*- coding: utf-8 -*-
"""
Created on Fri Feb 11 08:54:00 2022

@author: hungd
"""

#%% Imports

import os
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QTableWidgetItem
from registry import loadFromRegistry
from registry import saveToRegistry
from fileDialog import fileDialogBox
from basicUserFunctions import basicUserDummyFunction

#%% Main

class BasicUser(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uiFile = os.path.join(os.environ['PARENTDIR'], 'basicUser/basicUser.ui')
        uic.loadUi(uiFile, self)
    
        # Set Line Edit Values from Registry
        self.initiateValues()
        
        # Connect Line Edits
        self.connectLineEdits()
        
        # Connect Buttons
        self.connectButtons()
        
    # Set Line Edit Values and create initial plots
    def initiateValues(self):
        # Get registry
        registry, _ = loadFromRegistry()
        
        # Populate line edit fields
        self.lineEdit_inputCSV.setText(registry.get('basicUser.inputCSV', 'testInput.csv'))  # inputCSV
        self.lineEdit_uniqueID.setText(registry.get('basicUser.uniqueID', '10'))  # inputCSV
        
    # Save line edits to registry every time it changes
    def connectLineEdits(self):
        self.lineEdit_inputCSV.textChanged.connect(lambda: saveToRegistry('basicUser.inputCSV', self.lineEdit_inputCSV.text()))  # inputCSV
        self.lineEdit_uniqueID.textChanged.connect(lambda: saveToRegistry('basicUser.uniqueID', self.lineEdit_uniqueID.text()))  # uniqueID date

    # Def Buttons connected
    def connectButtons(self):
        self.pushButton_inputCSV.clicked.connect(self.selectFile)
        self.pushButton_getSimRows.clicked.connect(self.getSimRows)
        self.pushButton_exportResults.clicked.connect(self.exportResults)
        
    # Select Constituents File
    def selectFile(self):
        filepath = os.path.split(self.lineEdit_inputCSV.text())[0]
        filename = fileDialogBox(initialdir=filepath, title="Select Input CSV file", filetypes="*.csv")
        self.lineEdit_inputCSV.setText(filename)

    # Export Results
    def getSimRows(self):
        inputCSV = self.lineEdit_inputCSV.text()       # Input CSV
        uniqueID = int(self.lineEdit_uniqueID.text())  # Unique ID
        numRec = int(self.comboBox.currentText())      # Number of Recommendations
        
        # Run Basic User Dummy Function
        self.df = basicUserDummyFunction(inputCSV, uniqueID, numRec)
        
        # Write Results to Table
        self.writeDfsToTables()
    
    # Write Results to Table
    def writeDfsToTables(self):
        df = self.df
        keepColumns = list(df.columns)
        
        # Clear table
        self.tableWidget.setRowCount(1)  # Bring down to only header row for buy
        self.tableWidget.setColumnCount(len(keepColumns))  # Set Column Count
        
        # Set number of rows
        newRowCount = max(len(df), 20)  # At least 20 rows looks good
        self.tableWidget.setRowCount(newRowCount)    
        
        # Rename Columns in Similarity table to only the ones we care about
        for j in range(len(keepColumns)):
            self.tableWidget.setItem(0, j, QTableWidgetItem(keepColumns[j]))
        
        # Fill values for buy table
        for i in range(df.shape[0]):
            for j in range(df.shape[1]):
                self.tableWidget.setItem(i+1, j, QTableWidgetItem(str(df.iloc[i,j])))
                
    # Export Results
    def exportResults(self):
        self.df.to_csv(r'..\results\basicUserResults.csv', index=False)
        print('Results Exported')
        print(r'Location: \results\basicUserResults.csv')
        
#%% Create Results Folder

def createDirs():
    # Paths
    output = r"..\results"
    
    # Results
    if not os.path.exists(output):
        os.makedirs(output)
                