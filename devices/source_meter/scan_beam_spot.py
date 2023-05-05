#
# ------------------------------------------------------------
# Copyright (c) All rights reserved
# SiLab, Institute of Physics, University of Bonn
# ------------------------------------------------------------
#
import time
import os
import numpy as np
import tables as tb
import csv
import sys
import logging
from tables import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import random
from matplotlib.backends.backend_pdf import PdfPages

# sudo chmod 666 /dev/ttyUSB0
rootdir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(rootdir[:-21])
from analysis import analysis_utils , logger
if __name__ == '__main__':
    
    directory = "/test_files"
    conf = analysis_utils.open_yaml_file(file="Xray_irradiation_conf.yaml", directory=rootdir[:-21])
    size_x = conf['Settings']['size_x']
    z = conf['Settings']['z']
    x_delay = conf['Settings']['x_delay']
    z_delay = conf['Settings']['z_delay']
    x = conf['Settings']['x']
    size_z = conf['Settings']['size_z']
    sourcemeter = conf["Devices"]["sourcemeter"]
    motorstage = conf["Devices"]["motorstage"]
    depth = conf['Settings']['depth'] 
    scan = analysis_utils.BeamSpotScan()
    s = scan.compute_move(size_x=size_x, z=z, z_delay=z_delay, x_delay=x_delay, x=x, size_z=size_z,
                                     sourcemeter=sourcemeter, motorstage=motorstage, directory=directory)
