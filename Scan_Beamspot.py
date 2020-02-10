#
# ------------------------------------------------------------
# Copyright (c) All rights reserved
# SiLab, Institute of Physics, University of Bonn
# ------------------------------------------------------------
#
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
from analysis import analysis_utils

if __name__ == '__main__':
    directory="/Users/ahmedqamesh/git /Xray_Irradiation_System_Bonn/graphics_Utils/test_files"
    size_x=1
    z=20
    x_Delay=2
    z_Delay= 2
    x=20
    size_z=1
    sourcemeter =False
    depth = 3
    s = analysis_utils.compute_move(size_x=size_x, z=z,z_Delay=z_Delay, x_Delay=x_Delay, x=x, size_z=size_z,
                                     sourcemeter=sourcemeter, directory=directory)