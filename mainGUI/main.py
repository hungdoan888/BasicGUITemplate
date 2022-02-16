# -*- coding: utf-8 -*-
"""
Created on Fri Feb 11 08:54:00 2022

@author: hungd
"""

#%% imports

from addPaths import addPaths
addPaths()
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from home import Home
from basicUser import BasicUser

#%% Main

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        
        # Home Page
        self.comboBox.addItem('Home')
        self.home = Home()
        self.stackedWidget.addWidget(self.home)

        # Basic User
        self.comboBox.addItem('Basic User')
        self.BasicUser = BasicUser()
        self.stackedWidget.addWidget(self.BasicUser)
        
        # Connect Combo Box
        self.comboBox.currentIndexChanged.connect(self.comboBoxChanged)
        
    def comboBoxChanged(self):
        print('\n---', self.comboBox.currentText(), '---\n')
        self.stackedWidget.setCurrentIndex(self.comboBox.currentIndex())

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()