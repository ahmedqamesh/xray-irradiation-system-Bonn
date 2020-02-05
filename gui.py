import tkinter as tk
import tkinter.messagebox
from tkinter.font import Font
import time
import csv
from tables import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_pdf import PdfPages
import os.path
import numpy as np
import logging
import yaml
import tables as tb
from tqdm import tqdm
from scipy.optimize import curve_fit
from analysis import analysis
from analysis import logger
from analysis import utils
loglevel = logging.getLogger('GUI').getEffectiveLevel()
np.warnings.filterwarnings('ignore')
#!/usr/bin/env python
import sys
import os
import psutil
import subprocess
from PyQt5 import Qt
import pyqtgraph as pg
from pyqtgraph.dockarea import DockArea, Dock
try:
    import ConfigParser
except ImportError:  # pragma: no cover
    import configparser as ConfigParser  # renaming in python 3k
    

class GraphicalInterface(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        self.log = logger.setup_derived_logger('GUI')
        self.log.info('GUI initialized')
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

    def Application():
        print("<create the rest of your GUI here>")
        root.title("x-ray motorstage")
        root.geometry("450x230")
        lblInfo = Label(root, padx=8, font=Font(family='times', size=10), text="A", fg="Black")
        y1, y2, y3 = 30, 85, 140
        lblInfo.place(x=10, y=y1)
        e1 = DoubleVar()  # Relative Distance variable
        spinA = Spinbox(root, from_=-1073741824, to=1073741823, increment=1000, format="%0.2f",
                        textvariable=e1, width=10, font=Font(family='times', size=10))
        spinA.place(x=40, y=y1 - 5)

class OnlineMonitorApplication(pg.Qt.QtGui.QMainWindow):
    app_name = 'Online Monitor'

    def __init__(self, config_file, loglevel='INFO'):
        super(OnlineMonitorApplication, self).__init__()
        logger.setup_logging(loglevel)
        logging.debug("Initialize online monitor with configuration in %s", config_file)
        self.configuration = utils.parse_config_file(config_file, expect_receiver=True)
        self.setup_style()
        self.setup_widgets()
        self.receivers = self.start_receivers()

    def closeEvent(self, event):
        super(OnlineMonitorApplication, self).closeEvent(event)
        self.stop_receivers()
        set_window_geometry(self.geometry().getRect())

    def setup_style(self):
        self.setWindowTitle(self.app_name)
        stored_windows_geometry = self.get_window_geometry()
        if stored_windows_geometry:
            self.setGeometry(pg.Qt.QtCore.QRect(*stored_windows_geometry))
        # Fore/Background color
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')
        # Enable antialiasing for prettier plots
        pg.setConfigOptions(antialias=True)

    def start_receivers(self):
        receivers = []
        try:
            self.configuration['receiver']
        except KeyError:
            return receivers
        if self.configuration['receiver']:
            logging.info('Starting %d receivers', len(self.configuration['receiver']))
            for (receiver_name, receiver_settings) in self.configuration['receiver'].items():
                receiver_settings['name'] = receiver_name
                receiver = utils.load_receiver(receiver_settings['kind'], base_class_type=Receiver, *(), **receiver_settings)
                receiver.setup_widgets(self.tab_widget, name=receiver_name)
                receiver.start()
                receivers.append(receiver)
            return receivers

    def on_tab_changed(self, value):
        for index, actual_receiver in enumerate(self.receivers, start=1):  # First index is status tab widget
            actual_receiver.active(True if index == value else False)

    def stop_receivers(self):
        if self.receivers:
            logging.info('Stopping %d receivers', len(self.receivers))
            for receiver in self.receivers:
                receiver.shutdown()

    def setup_widgets(self):
        # Main window with Tab widget
        self.tab_widget = Qt.QTabWidget()
        self.setCentralWidget(self.tab_widget)
        self.setup_status_widget(self.tab_widget)
        self.tab_widget.currentChanged.connect(self.on_tab_changed)

    def setup_status_widget(self, parent):  # Visualizes the nodes + their connections + CPU usage
        # Status dock area showing setup
        dock_area = DockArea()
        parent.addTab(dock_area, 'Status')
        self.status_dock = Dock("Status")
        dock_area.addDock(self.status_dock)
        # GraphicsLayout to align graphics
        status_graphics_widget = pg.GraphicsLayoutWidget()
        status_graphics_widget.show()
        self.status_dock.addWidget(status_graphics_widget)
        try:
            self.configuration['receiver']
        except KeyError:
            return
        # Create nodes with links from configuration file for converter/receiver
        for receiver_index, (receiver_name, receiver_settings) in enumerate(self.configuration['receiver'].items()):
            # Add receiver info
            view = status_graphics_widget.addViewBox(row=receiver_index, col=5, lockAspect=True, enableMouse=False)
            text = pg.TextItem('Receiver\n%s' % receiver_name, border='b', fill=(0, 0, 255, 100), anchor=(0.5, 0.5), color=(0, 0, 0, 200))
            text.setPos(0.5, 0.5)
            view.addItem(text)
            # Add corresponding producer info
            try:
                if self.configuration['converter']:
                    try:
                        actual_converter = self.configuration['converter'][receiver_name]
                        view = status_graphics_widget.addViewBox(row=receiver_index, col=1, lockAspect=True, enableMouse=False)
                        text = pg.TextItem('Producer\n%s' % receiver_name, border='b', fill=(0, 0, 255, 100), anchor=(0.5, 0.5), color=(0, 0, 0, 200))
                        text.setPos(0.5, 0.5)
                        view.addItem(text)
                        view = status_graphics_widget.addViewBox(row=receiver_index, col=3, lockAspect=True, enableMouse=False)
                        text = pg.TextItem('Converter\n%s' % receiver_settings, border='b', fill=(0, 0, 255, 100), anchor=(0.5, 0.5), color=(0, 0, 0, 200))
                        text.setPos(0.5, 0.5)
                        view.addItem(text)
                    except KeyError:  # no converter for receiver
                        pass
            except KeyError:  # No converter defined in configruation
                pass


    def set_window_geometry(self, geometry):
        config = ConfigParser.SafeConfigParser()
        config.read(_file_name)
        try:
            config.add_section('OnlineMonitor')
        except ConfigParser.DuplicateSectionError:  # already existing
            pass
        config.set('OnlineMonitor', 'geometry', str(geometry)[1:-1])  # store new string representation
        with open(_file_name, 'w') as f:
            config.write(f)
    
    
    def get_window_geometry(self):
        config = ConfigParser.SafeConfigParser()
        config.read(_file_name)
        try:
            return ast.literal_eval(config.get('OnlineMonitor', 'geometry'))
        except ConfigParser.NoSectionError:
            return (100, 100, 1024, 768)  # std. settings
                        
def mainTk(): #run mianloop 
    root = tk.Tk()
    GraphicalInterface(root).pack(side="top", fill="both", expand=True)
    root.mainloop()

def mainQt():
    #args = utils.parse_arguments()
    #utils.setup_logging(args.log)
    app = Qt.QApplication(sys.argv)
    win = OnlineMonitorApplication("/Users/ahmedqamesh/git /Xray_Irradiation_System_Bonn/GUI/configuration.yaml")  # enter remote IP to connect to the other side listening
    win.show()
    sys.exit(app.exec_())
                
if __name__ == "__main__":
    #pass
    #mainTk()
    mainQt()