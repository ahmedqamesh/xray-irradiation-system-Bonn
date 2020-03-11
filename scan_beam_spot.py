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
import logging
from tables import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import random
from matplotlib.backends.backend_pdf import PdfPages
from analysis import analysis_utils , logger

if __name__ == '__main__':
    rootdir = os.path.dirname(os.path.abspath(__file__))
    directory= rootdir +"/test_files"
    conf = analysis_utils.open_yaml_file(file ="Xray_irradiation_conf.yaml",directory =rootdir)
    size_x=conf['Settings']['size_x']
    z=conf['Settings']['z']
    x_delay=conf['Settings']['x_delay']
    z_delay = conf['Settings']['z_delay']
    x=conf['Settings']['x']
    size_z=conf['Settings']['size_z']
    sourcemeter= True
    depth= conf['Settings']['depth'] 
    scan = analysis_utils.BeamSpotScan()
    s = scan.compute_move(size_x=size_x, z=z,z_delay=z_delay, x_delay=x_delay, x=x, size_z=size_z,
                                     sourcemeter=sourcemeter, directory=directory)