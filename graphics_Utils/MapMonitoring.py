
import sys
import random
import matplotlib
# matplotlib.use("Qt5Agg")
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from numpy import arange, sin, pi
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from mpl_toolkits.axes_grid1.colorbar import colorbar
from matplotlib.patches import Circle
import numpy as np
import tables as tb
import csv
import time
import logging
import os
from tables import *
import pandas as pd
from analysis import analysis_utils
class MapMonitoringDynamicCanvas(FigureCanvas):
    """A canvas that updates itself every second with a new plot."""
    def __init__(self, parent=None, width=5, height=4, dpi=100 ,period=None, depth = None, z=None, x=None, z_Delay= None, x_Delay=None,size_x =None, size_z = None, directory=None):
        self.directory = directory
        self.size_x=size_x
        self.z=z
        self.x_Delay=x_Delay
        self. z_Delay = z_Delay
        self.x=x
        self.size_z=size_z
        self.depth = depth
        self.period = period
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.compute_initial_figure(z=self.z, x=self.x)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.initiate_timer(period=self.period)
           
    def initiate_timer(self,period=None):    
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(period)
        
    def compute_initial_figure(self,z=None, x=None, directory= None):
        cmap = plt.cm.get_cmap('tab20c')
        beamspot = np.zeros(shape=(z, x), dtype=np.float64)
        analysis_utils.save_to_h5(data=beamspot, outname='beamspot_Live.h5', directory=self.directory)
        im = self.axes.imshow(beamspot, aspect='auto', origin='upper', cmap=cmap)  
        self.plot_style(im=im , cmap=cmap, z=self.z, x=self.x)
    
    def update_figure(self): 
        beamspot = analysis_utils.open_h5_file(outname='beamspot_Live.h5', directory=self.directory)
        cmap = plt.cm.get_cmap('tab20c')
        
        im = self.axes.imshow(beamspot, aspect='auto', origin='upper', cmap=cmap)
        self.draw()
    
    def plot_style(self, z=None, x=None, depth=None, im=None, cmap=plt.cm.get_cmap('viridis', 5)):
        mid_z = z / 2
        mid_x = x / 2
        r = 3
        self.axes.set_title("Beam profile", fontsize=12, y=1.7, x=-0.6)
        #self.axes.set_xlabel('x [mm]')
        #self.axes.set_ylabel('z[mm]')
        circle = plt.Circle((mid_z, mid_x), r, color='red', fill=False)
        self.axes.add_artist(circle)
        self.axes.axhline(y=mid_z, linewidth=0.6, color='#d62728', linestyle='dashed')
        self.axes.axvline(x=mid_x, linewidth=0.6, color='#d62728', linestyle='dashed')
    
if __name__ == '__main__':
    pass
