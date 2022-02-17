# -*- coding: utf-8 -*-
"""
Created on Fri Dec 17 16:31:15 2021

@author: hungd
"""

#%% Imports

import os
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget

#%% Main

class Contact(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uiFile = os.path.join(os.environ['PARENTDIR'], 'contact/contact.ui')
        uic.loadUi(uiFile, self)