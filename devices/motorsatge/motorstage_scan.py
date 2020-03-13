#
# ------------------------------------------------------------
# Copyright (c) All rights reserved
# SiLab, Institute of Physics, University of Bonn
# ------------------------------------------------------------
#
from basil.dut import Dut
import time
import numpy as np
import tables as tb
import csv
import logging
from tables import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import random
from matplotlib.backends.backend_pdf import PdfPages
from Tkinter import *

import os
rootdir = os.path.dirname(os.path.abspath(__file__))
dut = Dut('motorstage_Pyserial.yaml')
dut.init()
dut["Julabo"].restore_intial_positions()
# Auto-Referencing Option: With standard PI stages
dut["Julabo"]._write_command("FE2", address=1)
dut["Julabo"]._write_command("FE2", address=2)
dut["Julabo"]._write_command("FE2", address=3)

# Restore intial positions
dut["Julabo"].Read_Write("MR%d" % Limit, address=1)   # y Move to the Border (In-Out)
dut["Julabo"].Read_Write("MR%d" % Limit, address=2)   # z Move to the Border (Up-Down)
dut["Julabo"].Read_Write("MR%d" % -Limit, address=3)   # x Move to the Border (Left-Right)
# Check Stages
#dut["Julabo"].Read_Write("MR 500000", address=1)  # y
#dut["Julabo"].Read_Write("MA3000000", address=1)  # x   (Move to the Middle)

dut["Julabo"].GUI(root=Tk())  # x(in-out)
'''
Step1: Restore the intial position with Auto-Referencing Option: With standard PI stages
step2: show GUI to control the motor stage 
A: address=1
B: address=2
C: address=3

'''
