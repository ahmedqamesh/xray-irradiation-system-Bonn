#!/usr/bin/env python
from __future__ import annotations
from typing import *

from analysis import plotting_Calibration
from graphics import plotCanvas
import matplotlib
matplotlib.use("Agg")
from matplotlib import pyplot as plt   
import matplotlib as mpl 
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDateTime, Qt, QTimer, pyqtSlot
import sys
import random
import numpy as np
import pyqtgraph as pg
import time
from IPython import display


        
class MainApplication(QMainWindow):
    
    def __init__(self, parent=None):
        super(MainApplication, self).__init__(parent)
        self.originalPalette = QApplication.palette()
        #main window features
        #MainWindow = QtWidgets.QMainWindow()
        #MainWindow.setObjectName("MainWindow")
        #MainWindow.resize(800, 600)
        self.setWindowTitle("QMainWindow")
        #self.changeStyle('Windows')
        self._createMenu()
        #self._createToolBar()
        #self._createStatusBar()
        
        styleComboBox = QComboBox()
        styleComboBox.addItems(QStyleFactory.keys())
        styleLabel = QLabel("&Style:")
        styleLabel.setBuddy(styleComboBox)

        self.useStylePaletteCheckBox = QCheckBox("&Use style's standard palette")
        self.useStylePaletteCheckBox.setChecked(True)
        disableWidgetsCheckBox = QCheckBox("&Disable widgets")

        self.createTopLeftGroupBox()
        self.createTopRightGroupBox()
        self.createBottomLeftTabWidget()
        self.createBottomRightGroupBox()
        self.createProgressBar()

        styleComboBox.activated[str].connect(self.changeStyle)
        self.useStylePaletteCheckBox.toggled.connect(self.changePalette)
        
        disableWidgetsCheckBox.toggled.connect(self.topLeftGroupBox.setDisabled)
        disableWidgetsCheckBox.toggled.connect(self.topRightGroupBox.setDisabled)
        disableWidgetsCheckBox.toggled.connect(self.bottomLeftTabWidget.setDisabled)
        disableWidgetsCheckBox.toggled.connect(self.bottomRightGroupBox.setDisabled)
        
        topLayout = QHBoxLayout() 
        topLayout.addWidget(styleLabel)
        topLayout.addWidget(styleComboBox)
        topLayout.addStretch(1)
        topLayout.addWidget(self.useStylePaletteCheckBox)
        topLayout.addWidget(disableWidgetsCheckBox)

        mainLayout = QGridLayout()
        mainLayout.addLayout(topLayout, 0, 0, 1, 2)
        mainLayout.addWidget(self.topLeftGroupBox, 1, 0)
        mainLayout.addWidget(self.topRightGroupBox, 1, 1)
        mainLayout.addWidget(self.bottomLeftTabWidget, 2, 0)
        mainLayout.addWidget(self.bottomRightGroupBox, 2, 1)
        mainLayout.addWidget(self.progressBar, 3, 0, 1, 2)
        mainLayout.setRowStretch(1, 1)
        mainLayout.setRowStretch(2, 1)
        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(1, 1)
        
        centralWidget.setLayout(mainLayout)


    def _createMenu(self):
#         menubar =QtWidgets.QMenuBar(self)
#         self.menu = menubar.addMenu("&Menu")
#         self.save_button = QtWidgets.QPushButton('Save')
#         self.clear_button = QtWidgets.QPushButton('Clear')
#         self.open_button = QtWidgets.QPushButton('Open')
#         self.menu.addAction('&Exit', self.close)
        
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        
    def _createToolBar(self):
        tools = QToolBar()
        self.addToolBar(tools)
        tools.addAction('Exit', self.close)

    def _createStatusBar(self):
        status = QStatusBar()
        status.showMessage("I'm the Status Bar")
        self.setStatusBar(status)
               
    def changeStyle(self, styleName):
        QApplication.setStyle(QStyleFactory.create(styleName))
        self.changePalette()

    def changePalette(self):
        if (self.useStylePaletteCheckBox.isChecked()):
            QApplication.setPalette(QApplication.style().standardPalette())
        else:
            QApplication.setPalette(self.originalPalette)

    def advanceProgressBar(self):
        curVal = self.progressBar.value()
        maxVal = self.progressBar.maximum()
        self.progressBar.setValue(curVal + (maxVal - curVal) / 100)

    def createTopLeftGroupBox(self):
        self.topLeftGroupBox = QGroupBox("Group 1")

        radioButton1 = QRadioButton("Radio button 1")
        radioButton2 = QRadioButton("Radio button 2")
        radioButton3 = QRadioButton("Radio button 3")
        radioButton1.setChecked(True)

        checkBox = QCheckBox("Tri-state check box")
        checkBox.setTristate(True)
        checkBox.setCheckState(Qt.PartiallyChecked)

        layout = QVBoxLayout()
        layout.addWidget(radioButton1)
        layout.addWidget(radioButton2)
        layout.addWidget(radioButton3)
        layout.addWidget(checkBox)
        layout.addStretch(1)
        self.topLeftGroupBox.setLayout(layout)    

    def createTopRightGroupBox(self):
        centralWidget = QtWidgets.QWidget(self)
        self.setCentralWidget(centralWidget)
        
        
        centralWidget.topRightGroupBox = QGroupBox("Power results")
        centralWidget.figure = plt.figure() # a figure instance to plot on
        width=5
        height=4
        dpi=100
        fig = Figure(figsize=(width, height), dpi=dpi)
        centralWidget.axes = fig.add_subplot(111)
        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot(centralWidget)  
        centralWidget.canvas = FigureCanvas(centralWidget.figure)
        centralWidget.toolbar = NavigationToolbar(self.canvas, self)
        centralWidget.button = QPushButton('Start Scan')
        centralWidget.button.clicked.connect(self.plot)

        # set the layout
        layout = QVBoxLayout()
        layout.addWidget(centralWidget.toolbar)
        layout.addWidget(centralWidget.canvas)
        layout.addWidget(centralWidget.button)
        centralWidget.setLayout(layout)        
        layout.addStretch(1)
        centralWidget.topRightGroupBox.setLayout(layout)
        
    def plot(self,centralWidget):
        # Initialize the board with starting positions
        def init_board(pos_list, my_board):
            for pos in pos_list:
                my_board[pos[0], pos[1]] = 1
            return my_board

        fig = plt.gcf()
        ax = centralWidget.figure.add_subplot(111)
        data = [random.random() for i in range(25)]       
        boardsize = 50        # board will be X by X where X = boardsize
        pad = 2               # padded border, do not change this!
        initial_cells = 1500  # this number of initial cells will be placed 
        # Get a list of random coordinates so that we can initialize 
        # board with randomly placed organisms
        pos_list = []
        for i in range(initial_cells):
                pos_list.append([random.randint(1, boardsize), random.randint(1, boardsize)])
        # Initialize the board
        my_board = np.zeros((boardsize+pad, boardsize+pad))
        my_board = init_board(pos_list, my_board)
        im = plt.imshow(my_board)
        centralWidget.canvas.draw()
        
        def animate(frame):
            im.set_data(update_board(my_board))
            return im,
        
         #This line creates the animation
        anim = animation.FuncAnimation(fig, animate, frames=200, interval=50)

    def beamspot(self,size_x=1, z=20, x_Delay=5, x=20,size_z=1,
             Directory=False , Mororstage= False, Sourcemeter=False, CurrentLimit=1.000000E-06):
        '''
        Assuming that the cabinet door is the -z
        1 mm is equivalent to 56.88888 step
        x : Number of movements to x direction 
        z: Number of movements inside the cabinet
        Size_x: size of the step in  mm x direction
        Size_z: size of the step in  mm z direction
        '''
        #def beamspot(size_x=5*57000, z=25, x_Delay=5*3, x=25,size_z=5*57000 51 scan
        #size_x = size_x*57000
        #size_z=size_z*57000
        if Sourcemeter:
            dut = Dut('Scanning_pyserial.yaml')
            dut.init()
            dut['sm'].write(":OUTP ON")
            #dut['sm'].write("*RST")
            #dut['sm'].write(":SOUR:VOLT:RANG 60")
            #dut['sm'].write('SENS:CURR:PROT ' + str(CurrentLimit))
            #print "The Protection Current limit is", dut['sm'].ask("SENS:CURR:PROT?")
            dut['sm'].write(":SOUR:FUNC VOLT")
            dut['sm'].write(':SOUR:VOLT 50')
        if Mororstage:
            dut = Dut('motorstage_Pyserial.yaml')
            dut.init()
        else:  print("Starting the random data mode")
        #ax = self.figure.add_subplot(111)
        def Move(step_z=False,size_x=size_x,size_z=size_z):
            if step_z % 2 == 0:
                a,b,c = 0,x,1
                print ("Even" , size_x,range(a,b,c))
            else:
                size_x = size_x*-1
                a,b,c = x-1,-1,-1
                print ("odd", size_x,range(a,b,c))    
            first_point = True
            for step_x in np.arange(a,b,c):
                if not first_point:
                    if Mororstage: dut["ms"].read_write("MR%d" % (size_x), address=3) # x 50000,100,50 = 4.5 cm left/right
                    else: print("nodevice mode")
                first_point = False
                time.sleep(x_Delay)
                if Sourcemeter:
                    val = dut['sm'].ask(":MEAS:CURR?")
                    current = val[15:-43]
                else:
                    current = random.randint(1, 101)
                    
                beamspot[step_z,step_x] = float(current)
                plt.imshow(beamspot, aspect='auto', origin='upper',  cmap=plt.get_cmap('tab20c'))
                self.canvas.draw()
                #plt.pause(0.05)
                print (beamspot[step_z,step_x],step_x,step_z)
            if Sourcemeter: dut["ms"].read_write("MR%d" % (-size_z), address=2)  # x# x 50000,100,50 = 4.5 cm in/out
            time.sleep(2*x_Delay)
        t0 = time.time()
        beamspot = np.zeros(shape=(z, x), dtype=np.float64)
        for step_z in range(z):
            Move(step_z=step_z)
        #plt.show()
        self.canvas.draw()
        file = Directory + "beamspot_randomcm_collimator.h5"
        with tb.open_file(file, "w") as out_file_h5:
            out_file_h5.create_array(out_file_h5.root, 'beamspot', beamspot, "beamspot")  
        print ("The beamspot file is saved as%s" %(file))
        t1 = time.time()
        print ("The time Estimated", t1 - t0)
        
    
    def createBottomLeftTabWidget(self):
        self.bottomLeftTabWidget = QTabWidget()
        self.bottomLeftTabWidget.setSizePolicy(QSizePolicy.Preferred,
                QSizePolicy.Ignored)

        tab1 = QWidget()
        tableWidget = QTableWidget(10, 10)

        tab1hbox = QHBoxLayout()
        tab1hbox.setContentsMargins(5, 5, 5, 5)
        tab1hbox.addWidget(tableWidget)
        tab1.setLayout(tab1hbox)

        tab2 = QWidget()
        textEdit = QTextEdit()

        textEdit.setPlainText("Twinkle, twinkle, little star,\n"
                              "How I wonder what you are.\n" 
                              "Up above the world so high,\n"
                              "Like a diamond in the sky.\n"
                              "Twinkle, twinkle, little star,\n" 
                              "How I wonder what you are!\n")

        tab2hbox = QHBoxLayout()
        tab2hbox.setContentsMargins(5, 5, 5, 5)
        tab2hbox.addWidget(textEdit)
        tab2.setLayout(tab2hbox)

        self.bottomLeftTabWidget.addTab(tab1, "&Table")
        self.bottomLeftTabWidget.addTab(tab2, "Text &Edit")

    def createBottomRightGroupBox(self):
        self.bottomRightGroupBox = QGroupBox("Group 3")
        self.bottomRightGroupBox.setCheckable(True)
        self.bottomRightGroupBox.setChecked(True)

        lineEdit = QLineEdit('s3cRe7')
        lineEdit.setEchoMode(QLineEdit.Password)

        spinBox = QSpinBox(self.bottomRightGroupBox)
        spinBox.setValue(50)

        dateTimeEdit = QDateTimeEdit(self.bottomRightGroupBox)
        dateTimeEdit.setDateTime(QDateTime.currentDateTime())

        slider = QSlider(Qt.Horizontal, self.bottomRightGroupBox)
        slider.setValue(40)

        scrollBar = QScrollBar(Qt.Horizontal, self.bottomRightGroupBox)
        scrollBar.setValue(60)

        dial = QDial(self.bottomRightGroupBox)
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
        self.bottomRightGroupBox.setLayout(layout)

    def createProgressBar(self):
        self.progressBar = QProgressBar()
        self.progressBar.setRange(0, 10000)
        self.progressBar.setValue(0)

        timer = QTimer(self)
        timer.timeout.connect(self.advanceProgressBar)
        timer.start(1000)
   
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    gallery = MainApplication()
    #window = Window()
    #window.show()
    #gapp = ApplicationWindow()
    #gapp.show()
    #app.exec_()
    sys.exit(app.exec_()) 


    