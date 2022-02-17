# -*- coding: utf-8 -*-
"""
Created on Fri Feb 11 08:54:00 2022

@author: hungd
"""

import os
import sys

def addPaths():
    # Parent
    os.environ['PARENTDIR'] = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
    
    # Common Scripts
    sys.path.append('../commonScripts')
    
    # Basic User
    sys.path.append('../basicUser')
    
    # Advanced User
    sys.path.append('../advancedUser')
    
    # Contact Info
    sys.path.append('../contact')
