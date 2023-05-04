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
import matplotlib as mpl
import numpy as np
from matplotlib.figure import Figure
from graphics_Utils import DataMonitoring , MenuWindow ,LogWindow, childWindow
from analysis import analysis_utils , logger
# Third party modules
from logging.handlers import RotatingFileHandler
import coloredlogs as cl
import verboselogs
import logging
rootdir = os.path.dirname(os.path.abspath(__file__))
class MainWindow(QMainWindow):
    def __init__(self,parent=None , config =None , sourcemeter =None):
        super(MainWindow, self).__init__(parent)
        # Initialize logger
        verboselogs.install()
        self.logger = logging.getLogger(__name__)
        """:obj:`~logging.Logger`: Main logger for this class"""
        self.logger.setLevel(logging.DEBUG)

        # Read configurations from a file
        if config is None:
            conf = analysis_utils.open_yaml_file(file ="Xray_irradiation_conf.yaml",directory =rootdir[:-14])
        
        
        self.directory=rootdir[:-14]+"/graphics_Utils/test_files"
        self.test_directory = rootdir[:-14]+conf["Tests"]["test_directory"]
        # Initialize default arguments
        self.app_name = conf['Application']['name']
        
        #Devices
        self.sourcemeter= conf["Devices"]["sourcemeter"]["status"]
        self.motorstage= conf["Devices"]["motorstage"]["status"]
        channels = conf["Devices"]["motorstage"]["channels"]
        self.channel_x = channels[0]["x"]
        self.channel_y = channels[1]["y"]
        self.channel_z = channels[2]["z"]

        #Beamspot scan settings
        self.size_x=conf['Settings']['size_x']
        self.z=conf['Settings']['z']
        self.x_delay=conf['Settings']['x_delay']
        self.z_delay = conf['Settings']['z_delay']
        self.period = conf['Settings']['period']
        self.x=conf['Settings']['x']
        self.size_z=conf['Settings']['size_z']
        self.depth= conf['Settings']['depth'] 
        self.r = conf['Settings']['r'] 
        #Filters list
        self.__filtersList = conf['Tests']["filters"]
        self.__depthList = conf['Tests']["depth"]
        self.__currentList = conf['Tests']["current"]
        
        #Diodes list
        dictionary = dict(conf['Tests']['photodiodes'])
        self.__diodesList = list(dictionary.keys())
       
       #Get conversion factor 
        A_array =[dictionary[i] for i in ["A"] if i in dictionary]
        B_array =[dictionary[i] for i in ["B"] if i in dictionary]
        C_array =[dictionary[i] for i in ["C"] if i in dictionary]
        self.__A_factor  =   A_array[0]["factor"]
        self.__B_factor  =   B_array[0]["factor"]
        self.__C_factor  =   C_array[0]["factor"]
        # Get Info:
        self.__max_dose = conf['Info']["max_dose"]
        self.__max_current = conf['Info']["max_current"]
        self.__max_voltage = conf['Info']["max_voltage"]
        self.__max_radius= conf['Info']["max_radius"]
        self.__max_height = conf['Info']["max_height"]
       
    def Ui_ApplicationWindow(self):
        self.menu= MenuWindow.MenuBar(self)
        self.menu._createMenu(self)
        self.menu._createtoolbar(self)
        self.menu._createStatusBar(self)

        # call widgets
        self.createTopRightGroupBox()
        self.createBottomRightGroupBox()
        self.createMotorGroupBox()
        self.createProgressBar()

        # Creat a frame in the main menu for the gridlayout
        mainFrame = QFrame(self)
        mainFrame.setStyleSheet("QWidget { background-color: #eeeeec; }")
        mainFrame.setLineWidth(0.6)
        self.setCentralWidget(mainFrame)
        
        # SetLayout
        mainLayout = QGridLayout()
        mainLayout.addWidget(self.topRightGroupBox, 0, 0,1,2)
        mainLayout.addWidget(self.motorGroupBox , 1, 0)
        mainLayout.addWidget(self.bottomRightGroupBox ,1, 1)
        
        
        #mainLayout.addWidget(self.progressBar, 3, 0, 1, 2)
        
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
        Fig = DataMonitoring.MapMonitoringDynamicCanvas(r = self.r, period =self.period, depth = self.depth, dpi=100,x= self.x ,
                                                        z = self.z,  z_delay= self.z_delay, x_delay=self.x_delay, directory = self.directory)
        plotLayout.addStretch(1)
        plotLayout.addWidget(Fig)
        self.setCentralWidget(plotframe)
        plotframe.setLayout(plotLayout)
        self.topRightGroupBox.setLayout(plotLayout)

    def createBottomRightGroupBox(self):
        self.bottomRightGroupBox = QGroupBox("Scan controllers")
        plotframe = QFrame(self)
        
        plotframe.setStyleSheet("QWidget { background-color: #eeeeec; }")
        plotframe.setLineWidth(0.6)
        #list Joystick bottons
        h , w = 50 , 25
        field_joystick_in_button = QPushButton("")
        field_joystick_in_button.clicked.connect(self.joystick_in)
        field_joystick_in_button.setFixedWidth(w)
        field_joystick_in_button.setIcon(QIcon('graphics_Utils/icons/icon_in.jpg'))
        #field_joystick_in_button.setIconSize(QtCore.QSize(26,24))
        
        field_joystick_out_button = QPushButton("")
        field_joystick_out_button.clicked.connect(self.joystick_out)  
        field_joystick_out_button.setFixedWidth(w)
        field_joystick_out_button.setIcon(QIcon('graphics_Utils/icons/icon_out.jpg'))
        #field_joystick_out_button.setIconSize(QtCore.QSize(24,24))

        field_joystick_middle_button = QPushButton("")  
        field_joystick_middle_button.clicked.connect(self.joystick_middle_scan)
        field_joystick_middle_button.setFixedWidth(w)
        field_joystick_middle_button.setIcon(QIcon('graphics_Utils/icons/icon_start.png'))
        #field_joystick_middle_button.setIconSize(QtCore.QSize(24,24))

        field_joystick_right_button = QPushButton("")  
        field_joystick_right_button.clicked.connect(self.joystick_right)
        field_joystick_right_button.setFixedWidth(w)
        field_joystick_right_button.setIcon(QIcon('graphics_Utils/icons/icon_right.jpg'))
        #field_joystick_right_button.setIconSize(QtCore.QSize(24,24))
        
        
        field_joystick_left_button = QPushButton("")  
        field_joystick_left_button.clicked.connect(self.joystick_left)
        field_joystick_left_button.setFixedWidth(w)
        field_joystick_left_button.setIcon(QIcon('graphics_Utils/icons/icon_left.jpg'))
        #field_joystick_left_button.setIconSize(QtCore.QSize(24,24))
        
        # Up- down plots
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

        gridLayout = QGridLayout()
        gridLayout.addWidget(field_joystick_in_button,0,3)
        gridLayout.addWidget(field_joystick_left_button,1 ,2)
        gridLayout.addWidget(field_joystick_middle_button,1,3)
        gridLayout.addWidget(field_joystick_right_button,1,4)
        gridLayout.addWidget(field_joystick_out_button,2,3)
        gridLayout.addLayout(upDownLayout,0,6, 3,1)

        self.setCentralWidget(plotframe)
        plotframe.setLayout(gridLayout)
        self.bottomRightGroupBox.setLayout(gridLayout)    

        
    def createMotorGroupBox(self):
        self.motorGroupBox = QGroupBox("Scan settings")
        plotframe = QFrame(self)
        plotframe.setStyleSheet("QWidget { background-color: #eeeeec; }")
        plotframe.setLineWidth(0.6)
        
        table = QTableWidget(self)  # Create a table
        table.setColumnCount(3)     #Set three columns
        table.setRowCount(3)        # and one row
        # Set the table headers
        table.setHorizontalHeaderLabels([" ", "x", "z"])
        table.setEditTriggers( QAbstractItemView.NoEditTriggers)
        # Fill the first line
        table.setItem(0, 0, QTableWidgetItem("Matrix size [cm] :"))
        table.setItem(1, 0, QTableWidgetItem("Step   size [   ]:"))
        table.setItem(2, 0, QTableWidgetItem("Delay  time [sec]:"))
        
        table.item(0, 0).setBackground(QColor("gray"))
        table.item(1, 0).setBackground(QColor("gray"))
        table.item(2, 0).setBackground(QColor("gray"))
        
        table.setItem(0, 1, QTableWidgetItem(str(self.x)))
        table.setItem(0, 2, QTableWidgetItem(str(self.z)))

        table.setItem(1, 1, QTableWidgetItem(str(self.size_x)))
        table.setItem(1, 2, QTableWidgetItem(str(self.size_z)))

        table.setItem(2, 1, QTableWidgetItem(str(self.x_delay)))
        table.setItem(2, 2, QTableWidgetItem(str(self.z_delay)))
                        
        # Do the resize of the columns by content
        table.resizeColumnsToContents()
        table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        firstHBoxLayout = QHBoxLayout()
        firstLabel = QLabel("Matrix Size: ", self)
        firstLabel.setText("Matrix Size [cm]: ")
        labelValue = QLabel()
        labelValue.setText(str(self.z)+"x" +str(self.z))
        firstHBoxLayout.addWidget(firstLabel)
        firstHBoxLayout.addWidget(labelValue)
        
        montoSettings_button = QPushButton("Montor Settings")
        montoSettings_button.clicked.connect(self.openSettingsChildWindow)
        #MontoSettings_button.setFixedWidth(30)

        restore_button = QPushButton("Restore intial positions")
        restore_button.clicked.connect(self.openSettingsChildWindow)
        gridLayout = QGridLayout()
        gridLayout.addLayout(firstHBoxLayout, 0, 0)
        gridLayout.addWidget(table,1, 0)
        
        gridLayout.addWidget(montoSettings_button, 2, 0)
        gridLayout.addWidget(restore_button, 3, 0)
        
        self.setCentralWidget(plotframe)
        plotframe.setLayout(gridLayout)
        self.motorGroupBox.setLayout(gridLayout)
          
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
    def joystick_middle_scan(self):
        analysis_utils.BeamSpotScan().compute_move(size_x=self.size_x, z=self.z, z_delay = self.z_delay , x_delay=self.x_delay, x=self.x, size_z=self.size_z, sourcemeter=self.sourcemeter,motorstage = self.motorstage, directory=self.directory)
        
    def joystick_up(self):
        print("Up")
    def joystick_down(self):
        print("Down")

    def SettingsChildWindow(self, ChildWindow):
        ChildWindow.setObjectName("settingsChildWindow")
        ChildWindow.setWindowTitle("Motor settings")
        ChildWindow.resize(310, 600)  # w*h
        # Define a frame for that group
        plotframe = QFrame(ChildWindow)
        plotframe.setLineWidth(0.6)
        MainLayout = QGridLayout()
        FirstGroupBox = QGroupBox("")
        # comboBox and label for channel
        FirstGridLayout = QGridLayout() 
        #self.main.set_bytes(textboxValue[i])
        channelLabel = QLabel("Channel setup", ChildWindow)
        channelLabel.setText("Channel setup")
        channelitems = ["--","1","2","3"]
        dimitems = ["--","x","y","z"]
        channelComboBox = QComboBox(self)
        dimComboBox = QComboBox(self)
        for item in channelitems: channelComboBox.addItem(item)
        for item in dimitems: dimComboBox.addItem(item)
        channelComboBox.activated[str].connect(self.set_channel)
        dimComboBox.activated[str].connect(self.set_dimention)

        set_button = QPushButton("Set channel")
        set_button.setIcon(QIcon('graphics_Utils/icons/icon_true.png'))
        set_button.clicked.connect(self.set_all)

        FirstGridLayout.addWidget(channelLabel, 0, 0)
        FirstGridLayout.addWidget(channelComboBox, 0, 1)
        FirstGridLayout.addWidget(dimComboBox, 0, 2)        
        FirstGridLayout.addWidget(set_button, 0, 3)       
             
        FirstGroupBox.setLayout(FirstGridLayout) 
        
        SecondGroupBox = QGroupBox("Message Data")
        # comboBox and label for channel
        SecondGridLayout = QGridLayout()
        ByteList = ["Byte0 :", "Byte1 :", "Byte2 :", "Byte3 :", "Byte4 :", "Byte5 :", "Byte6 :", "Byte7 :"] 
        LabelByte = [ByteList[i] for i in np.arange(len(ByteList))]
        textbox = [ByteList[i] for i in np.arange(len(ByteList))]
        textboxValue = [ByteList[i] for i in np.arange(len(ByteList))]
        for i in np.arange(len(ByteList)):
            LabelByte[i] = QLabel(ByteList[i], ChildWindow)
            LabelByte[i].setText(ByteList[i])
            textbox[i] = QLineEdit("self.__bytes[i]", ChildWindow)
            textboxValue[i] = textbox[i].text()
            if i <= 3:
                SecondGridLayout.addWidget(LabelByte[i], i, 0)
                SecondGridLayout.addWidget(textbox[i], i, 1)
            else:
                SecondGridLayout.addWidget(LabelByte[i], i - 4, 4)
                SecondGridLayout.addWidget(textbox[i], i - 4, 5)
        #self.set_bytes(textboxValue)
        SecondGroupBox.setLayout(SecondGridLayout) 
        
        HBox = QHBoxLayout()
        send_button = QPushButton("Send")
        send_button.setIcon(QIcon('graphics_Utils/icons/icon_true.png'))

        close_button = QPushButton("close")
        close_button.setIcon(QIcon('graphics_Utils/icons/icon_close.jpg'))
        close_button.clicked.connect(ChildWindow.close)

        HBox.addWidget(send_button)
        HBox.addWidget(close_button)
                 
        MainLayout.addWidget(FirstGroupBox , 0, 0)
        MainLayout.addWidget(SecondGroupBox , 1, 0)
        MainLayout.addLayout(HBox , 2, 0)
        
        ChildWindow.setCentralWidget(plotframe)
        plotframe.setLayout(MainLayout) 
        QtCore.QMetaObject.connectSlotsByName(ChildWindow)
 
    def set_channel(self, x):
        self._channel = x 
    
    def set_dimention(self, x): 
        self._dim = x
    
    def set_all(self):
        dim = self.get_dimention()
        ch = self.get_channel()
        text = "channel %s will be set to  %s direction"%(ch,dim)
        print(text)
        #self.outLabel.setText(text)
        #self.outLabel.adjustSize()
        
    def openSettingsChildWindow(self):
        self.window = QMainWindow()
        #ui = childWindow.ChildWindow()
        self.SettingsChildWindow(self.window)
        #MainWindow.hide()
        self.window.show()
 
    def get_channel(self): 
        return self._channel 
    
    def get_dimention(self): 
        return self._dim
       
    def get_testDirectory(self):
        return self.test_directory
    
    def get_diodesList(self):
        return self.__diodesList
    
    def get_filtersList(self):
        return self.__filtersList
    
    def get_depthList(self):
        return self.__depthList
    
    def get_currentList(self):
        return self.__currentList
    
    def get_calibration_factor(self, diode = None):
        if diode =="A": factor = self.__A_factor
        if diode =="B": factor = self.__B_factor
        if diode =="C": factor = self.__C_factor
        return factor
    
    def get_Info(self, info):
        if info =="max_dose": value = self.__max_dose
        if info =="max_current": value = self.__max_current
        if info =="max_voltage": value = self.__max_voltage
        if info =="max_height": value = self.__max_height
        if info =="max_radius": value = self.__max_radius
        return value
            