
from __future__ import annotations
from typing import *
import sys
import os
from matplotlib.backends.qt_compat import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvas
from PyQt5.QtCore    import *
from PyQt5.QtGui     import *
from PyQt5.QtWidgets import *
from pathlib import Path

# from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib as mpl
import numpy as np
from matplotlib.figure import Figure
from graphics_Utils import DataMonitoring , utils , ChildWindow

from analysis import analysis_utils

class ApplicationWindow(QtWidgets.QMainWindow):
    app_name = 'Online Monitor'
    size_x=1
    z=20
    x_Delay=5
    z_Delay = 5
    period = 1000
    x=20
    size_z=1
    sourcemeter =False
    depth = 3
    def __init__(self, parent=None,depth=depth,  size_x=size_x,period=period, z=z, z_Delay=z_Delay, x_Delay=x_Delay, x=x, size_z=size_z, sourcemeter=sourcemeter):
        #ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) # This is your Project Root
        super(ApplicationWindow, self).__init__(parent)
        root = analysis_utils.get_project_root()
        directory= str(root)+"/graphics_Utils/test_files"
        self.size_x=size_x
        self.z=z
        self.x_Delay=x_Delay
        self.z_Delay = z_Delay
        self.period = period
        self.x=x
        self.size_z=size_z
        self.sourcemeter=sourcemeter
        self.directory=directory
        self.depth= depth
        self.originalPalette = QApplication.palette()
        utils._createMenu(self)
        # utils._createToolBar(self)
        utils._createStatusBar(self)
        
        # 1. Window settings
        utils._setup_style(self) 
        
        # call widgets
        self.createTopLeftTabGroupBox()
        self.createTopRightGroupBox()
        self.createBottomRightGroupBox()
        self.createBottomLeftGroupBox()
        self.createProgressBar()

        # Creat a frame in the main menu for the gridlayout
        mainFrame = QFrame(self)
        mainFrame.setStyleSheet("QWidget { background-color: #eeeeec; }")
        mainFrame.setLineWidth(0.6)
        self.setCentralWidget(mainFrame)
        
        # SetLayout
        mainLayout = QGridLayout()
        mainLayout.addWidget(self.topLeftTabGroupBox, 1, 0)
        mainLayout.addWidget(self.topRightGroupBox, 1, 1)
        mainLayout.addWidget(self.bottomLeftGroupBox, 2, 0)
        mainLayout.addWidget(self.bottomRightGroupBox , 2, 1)
        mainLayout.addWidget(self.progressBar, 3, 0, 1, 2)
        
        mainFrame.setLayout(mainLayout)
        # 3. Show
        self.show()
        return

    def createTopRightGroupBox(self):
        # Define a group for the whole wedgit
        self.topRightGroupBox = QGroupBox("Data Monitoring")
        # Define a frame for the figure
        plotframe = QFrame(self)
        plotframe.setStyleSheet("QWidget { background-color: #eeeeec; }")
        plotframe.setLineWidth(0.6)
        # Define a layout
        plotLayout = QVBoxLayout()
        # add the figure to the layout
        Fig = DataMonitoring.MapMonitoringDynamicCanvas(width=5, height=5, period =self.period, depth = self.depth, dpi=100,x= self.x ,
                                                        z = self.z,  z_Delay= self.z_Delay, x_Delay=self.x_Delay, directory = self.directory)
        plotLayout.addStretch(1)
        plotLayout.addWidget(Fig)
        self.setCentralWidget(plotframe)
        plotframe.setLayout(plotLayout)
        self.topRightGroupBox.setLayout(plotLayout)

    def createTopLeftTabGroupBox(self):
        # Define a group for the whole wedgit
        self.topLeftTabGroupBox = QGroupBox("Data Monitoring (2)")
        # Define a frame for the figure
        plotframe = QFrame(self)
        plotframe.setStyleSheet("QWidget { background-color: #eeeeec; }")
        plotframe.setLineWidth(0.6)
        # Define a layout
        plotLayout = QVBoxLayout()
        # add the figure to the layout
        # myFig = DataMonitoring.DataMonitoringCanvas(x_len=200, y_range=[0, 100], interval=1)
        Fig = DataMonitoring.LiveMonitoringData()
        plotLayout.addStretch(1)
        plotLayout.addWidget(Fig)
        self.setCentralWidget(plotframe)
        plotframe.setLayout(plotLayout)
        self.topLeftTabGroupBox.setLayout(plotLayout)
    
    def scan_click(self):
        print('Start scanning')
        analysis_utils.compute_move(size_x=self.size_x, z=self.z, z_Delay = self.z_Delay , x_Delay=self.x_Delay, x=self.x, size_z=self.size_z, sourcemeter=self.sourcemeter, directory=self.directory)
        
    def createBottomRightGroupBox(self):
        self.bottomRightGroupBox = QGroupBox("Scan controllers")
        plotframe = QFrame(self)
        plotframe.setStyleSheet("QWidget { background-color: #eeeeec; }")
        plotframe.setLineWidth(0.6)
        #list Joystick bottons
        field_joystick_in_button = QPushButton("")
        field_joystick_in_button.clicked.connect(self.joystick_in)
        field_joystick_in_button.setFixedWidth(24)
        field_joystick_in_button.setIcon(QIcon('graphics_Utils/icons/icon_in.jpg'))
        #field_joystick_in_button.setIconSize(QtCore.QSize(26,24))
        
        field_joystick_out_button = QPushButton("")
        field_joystick_out_button.clicked.connect(self.joystick_out)  
        field_joystick_out_button.setFixedWidth(24)
        field_joystick_out_button.setIcon(QIcon('graphics_Utils/icons/icon_out.jpg'))
        #field_joystick_out_button.setIconSize(QtCore.QSize(24,24))

        field_joystick_middle_button = QPushButton("")  
        field_joystick_middle_button.clicked.connect(self.joystick_middle)
        field_joystick_middle_button.setFixedWidth(24)
        field_joystick_middle_button.setIcon(QIcon('graphics_Utils/icons/icon_run.png'))
        #field_joystick_middle_button.setIconSize(QtCore.QSize(24,24))

        field_joystick_right_button = QPushButton("")  
        field_joystick_right_button.clicked.connect(self.joystick_right)
        field_joystick_right_button.setFixedWidth(24)
        field_joystick_right_button.setIcon(QIcon('graphics_Utils/icons/icon_right.jpg'))
        #field_joystick_right_button.setIconSize(QtCore.QSize(24,24))
        
        
        field_joystick_left_button = QPushButton("")  
        field_joystick_left_button.clicked.connect(self.joystick_left)
        field_joystick_left_button.setFixedWidth(24)
        field_joystick_left_button.setIcon(QIcon('graphics_Utils/icons/icon_left.jpg'))
        #field_joystick_left_button.setIconSize(QtCore.QSize(24,24))
        
        # Up- down plots
        h , w = 30 , 25
        upDownLayout = QVBoxLayout()
        field_joystick_up_button = QPushButton("")  
        field_joystick_up_button.clicked.connect(self.joystick_up)
        field_joystick_up_button.setFixedWidth(w)
        field_joystick_up_button.setFixedHeight(h)
        field_joystick_up_button.setIcon(QIcon('graphics_Utils/icons/icon_up.png'))
        
        
        
        field_joystick_down_button = QPushButton("")  
        field_joystick_down_button.clicked.connect(self.joystick_down)
        field_joystick_down_button.setFixedWidth(w)
        field_joystick_down_button.setFixedHeight(h)
        field_joystick_down_button.setIcon(QIcon('graphics_Utils/icons/icon_down.png'))
        
        upDownLayout.addWidget(field_joystick_up_button)
        upDownLayout.addWidget(field_joystick_down_button)
        
        
        MontoSettings_button = QPushButton("MontoSettings")
        MontoSettings_button.clicked.connect(self.openWindow)
        #MontoSettings_button.setFixedWidth(30)

        btn2 = QPushButton("btn2")
        btn2.clicked.connect(self.openWindow)
        
        gridLayout = QGridLayout()
        gridLayout.addWidget(field_joystick_in_button,0,3)
        gridLayout.addWidget(field_joystick_left_button,1 ,2)
        gridLayout.addWidget(field_joystick_middle_button,1,3)
        gridLayout.addWidget(field_joystick_right_button,1,4)
        gridLayout.addWidget(field_joystick_out_button,2,3)
        gridLayout.addLayout(upDownLayout,0,6, 3,1)
        
        
        #up-down buttons

        gridLayout.addWidget(MontoSettings_button, 3, 0)
        gridLayout.addWidget(btn2, 4, 0)
        
        self.setCentralWidget(plotframe)
        plotframe.setLayout(gridLayout)
        self.bottomRightGroupBox.setLayout(gridLayout)    

    def createBottomLeftGroupBox(self):
        self.bottomLeftGroupBox = QGroupBox("Group 3")
        self.bottomLeftGroupBox.setCheckable(True)
        self.bottomLeftGroupBox.setChecked(True)

        lineEdit = QLineEdit('s3cRe7')
        lineEdit.setEchoMode(QLineEdit.Password)

        spinBox = QSpinBox(self.bottomLeftGroupBox)
        spinBox.setValue(50)

        dateTimeEdit = QDateTimeEdit(self.bottomLeftGroupBox)
        dateTimeEdit.setDateTime(QDateTime.currentDateTime())

        slider = QSlider(Qt.Horizontal, self.bottomLeftGroupBox)
        slider.setValue(40)

        scrollBar = QScrollBar(Qt.Horizontal, self.bottomLeftGroupBox)
        scrollBar.setValue(60)

        dial = QDial(self.bottomLeftGroupBox)
        dial.setValue(30)
        dial.setNotchesVisible(True)

        layout = QGridLayout()
        layout.addWidget(lineEdit, 0, 0, 1, 2)
        layout.addWidget(spinBox, 1, 0, 1, 2)
        layout.addWidget(dateTimeEdit, 2, 0, 1, 2)
        layout.addWidget(slider, 3, 0)
        layout.addWidget(scrollBar, 4, 0)
        layout.addWidget(dial, 3, 1, 2, 1)
        layout.setRowStretch(5, 1)
        self.bottomLeftGroupBox.setLayout(layout)

    def createProgressBar(self):
        self.progressBar = QProgressBar()
        self.progressBar.setRange(0, 10000)
        self.progressBar.setValue(0)

        timer = QTimer(self)
        timer.timeout.connect(self.advanceProgressBar)
        timer.start(1000)

    def advanceProgressBar(self):
        curVal = self.progressBar.value()
        
        maxVal = self.progressBar.maximum()
        self.progressBar.setValue(curVal + (maxVal - curVal) / 100)
        
    def joystick_in(self):
        print("In")
    def joystick_out(self):
        print("Out")
    def joystick_right(self):
        print("Right")
    def joystick_left(self):
        print("Left")
    def joystick_middle(self):
        print("middle")
    def joystick_up(self):
        print("Up")
    def joystick_down(self):
        print("Down")
                
    def openWindow(self):
        self.window = QMainWindow()
        self.ui = ChildWindow.Ui_ChildWindow()
        self.ui.settingChannel(self.window)
        #MainWindow.hide()
        self.window.show()


if __name__ == "__main__":
    qapp = QtWidgets.QApplication(sys.argv)
    app = ApplicationWindow()
    qapp.exec_()
