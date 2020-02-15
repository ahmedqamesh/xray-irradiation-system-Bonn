from matplotlib.backends.qt_compat import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvas as FigureCanvas

import matplotlib.pyplot as plt
import random
from PyQt5.QtCore    import *
from PyQt5.QtGui     import *
from PyQt5.QtWidgets import *
import os
from graphics_Utils import DataMonitoring , MenuWindow , LogWindow
from analysis import analysis_utils,  plottingCalibration, analysis
import numpy as np
from matplotlib.figure import Figure
import time
ipAddress = '192.168.1.254'
rootdir = os.path.dirname(os.path.abspath(__file__)) 

class Ui_ChildWindow(QWidget):  
    def __init__(self):
       super().__init__() 
       self.menu= MenuWindow.MenuBar()
       self.__openingAngleFilter = "With_Filter"
       self_ipAddress =ipAddress
       conf = analysis_utils.open_yaml_file(file ="BeamSpot_cfg.yaml",directory ="/Users/ahmedqamesh/git/Xray_Irradiation_System_Bonn/")
       self.__filterList = conf['Tests']['Filters']
       self.test_directory = rootdir[:-14]+conf['Tests']['test_directory']
       self.plotting =plottingCalibration.PlottingCalibration()
       #self.menu._createStatusBar(self)
     
    
    def outputChildWindow(self, ChildWindow):
        ChildWindow.setObjectName("OutputWindow")
        ChildWindow.setWindowTitle("Output Window")
        ChildWindow.resize(600, 600) #w*h
        logframe = QFrame(ChildWindow)
        logframe.setLineWidth(0.6)
        ChildWindow.setCentralWidget(logframe)
        self.WindowGroupBox = QGroupBox("")
        logEdit= LogWindow.LoggerDialog()
        logLayout = QVBoxLayout()
        logLayout.addWidget(logEdit)
        self.WindowGroupBox.setLayout(logLayout)
        logframe.setLayout(logLayout) 
        
    def trendChildWindow(self, ChildWindow):
        ChildWindow.setObjectName("OutputWindow")
        ChildWindow.setWindowTitle("Output Window")
        ChildWindow.resize(500, 500) #w*h
        logframe = QFrame(ChildWindow)
        logframe.setLineWidth(0.6)
        ChildWindow.setCentralWidget(logframe)
        self.WindowGroupBox = QGroupBox("")
        Fig = DataMonitoring.LiveMonitoringData()
        plotLayout = QVBoxLayout()
        plotLayout.addStretch(1)
        plotLayout.addWidget(Fig)
        self.WindowGroupBox.setLayout(plotLayout)
        logframe.setLayout(plotLayout) 
        
    def openingAngleChildMenu(self, ChildWindow):
        test_name = "Opening Angle Test"
        self.opening_angle_directory = self.test_directory+"opening_angle/"
        ChildWindow.setObjectName(test_name)
        ChildWindow.setWindowTitle(test_name)
        ChildWindow.resize(310, 600) #w*h
        MainLayout = QGridLayout()
        #Define a frame for that group
        plotframe = QFrame(ChildWindow)
        plotframe.setLineWidth(0.6)
        ChildWindow.setCentralWidget(plotframe)
        #Define First Group
        self.FirstGroupBox= QGroupBox("")
        FirstGridLayout =  QGridLayout()
        #comboBox and label for channel
        firstHBoxLayout = QHBoxLayout()
        firstLabel = QLabel("Test Type: ", ChildWindow)
        firstLabel.setText("Test Type: ")
        firstitems = ["-----------","With_Filter","Without_Filter"]
        firstComboBox = QComboBox(ChildWindow)
        for item in firstitems: firstComboBox.addItem(item)
        firstComboBox.activated[str].connect(self.set_openingAngleFilter)
        self.openSubFilterGroupMenu()
        def _SubFilterGroupMenu():
            FirstGridLayout.removeWidget(self.SubFilterGroupBox)
            self.SubFilterGroupBox.deleteLater()
            self.SubFilterGroupBox = None
            self.openSubFilterGroupMenu(ChildWindow = ChildWindow, x = self.__openingAngleFilter)
            FirstGridLayout.addWidget(self.SubFilterGroupBox,1,0)   
            
        firstComboBox.activated[str].connect(_SubFilterGroupMenu)
        firstHBoxLayout.addWidget(firstLabel)
        firstHBoxLayout.addWidget(firstComboBox)
               
        FirstGridLayout.addLayout(firstHBoxLayout,0,0)
        self.FirstGroupBox.setLayout(FirstGridLayout)
        MainLayout.addWidget(self.FirstGroupBox, 0, 0)
        plotframe.setLayout(MainLayout) 
        self.menu._createStatusBar(ChildWindow)
        QtCore.QMetaObject.connectSlotsByName(ChildWindow)  
        
    def openSubFilterGroupMenu(self, ChildWindow = None, x= "-----------"):
        self.SubFilterGroupBox= QGroupBox("")
       
        #self.canvas = FigureCanvas(self.figure)
        test_name = "Opening Angle Test"
        SubSecondGridLayout =  QGridLayout()
        firstLabel= QLabel("firstLabel", ChildWindow)
        secondLabel = QLabel("secondLabel", ChildWindow)
        thirdLabel = QLabel("thirdLabel", ChildWindow)
        forthLabel = QLabel("secondLabel", ChildWindow)
        fifthLabel = QLabel("thirdLabel", ChildWindow)
        firstGroupBox= QGroupBox("Test Info:")
        
        if (x == "Without_Filter"): 
            test = "Without_filter"
            test_dir = self.opening_angle_directory+"without_filter/"
            test_file = test_dir+"opening_angle_without_filter.csv" 
            test_date =time.ctime(os.path.getmtime(test_file))
            test_modify = time.ctime(os.path.getctime(test_file))
            secondLabel.setText("Test Directory:")
            secondtextbox = QLineEdit(test_dir)
            secondTextBoxValue = secondtextbox.text()
            
            thirdLabel.setText("Test Date:")
            thirdtextbox = QLineEdit(test_date)
            thirdTextBoxValue = thirdtextbox.text()
        
            forthLabel.setText("Last Modified:")
            forthtextbox = QLineEdit(test_modify)
            forthTextBoxValue = forthtextbox.text()
            #self.plotting_menu()
            fifthLabel.setText("Results:")
            Fig = DataMonitoring.PlottingWindowCanvas()#self.plotting_menu()
            #Fig = self.plotting.opening_angle(Directory=Directory, tests=[test])
            SubSecondGridLayout.addWidget(secondLabel,0,0)
            SubSecondGridLayout.addWidget(secondtextbox,0,1)  

            SubSecondGridLayout.addWidget(thirdLabel,1,0)
            SubSecondGridLayout.addWidget(thirdtextbox,1,1)
            
            SubSecondGridLayout.addWidget(forthLabel,2,0)
            SubSecondGridLayout.addWidget(forthtextbox,2,1)
            
            SubSecondGridLayout.addWidget(fifthLabel,3,0)
            SubSecondGridLayout.addWidget(Fig,3,0, 10,3)
            
        if (x == "With_Filter"):
            test_dir = self.opening_angle_directory
            test_file = test_dir+"Al/"+"opening_angle_Al.csv" 
            test_date =time.ctime(os.path.getmtime(test_file))
            test_modify = time.ctime(os.path.getctime(test_file))
            firstLabel.setText("Filter Material:")
            filterListItems = self.__filterList
            firstComboBox = QComboBox(ChildWindow)
            for item in filterListItems: firstComboBox.addItem(item)
            firstComboBox.activated[str].connect(self.set_openingAngleFilter)
            secondLabel.setText("Test Directory:")
            secondtextbox = QLineEdit(test_dir)
            secondTextBoxValue = secondtextbox.text()
            
            thirdLabel.setText("Test Date:")
            thirdtextbox = QLineEdit(test_date)
            thirdTextBoxValue = thirdtextbox.text()
        
            forthLabel.setText("Last Modified:")
            forthtextbox = QLineEdit(test_modify)
            forthTextBoxValue = forthtextbox.text()
            
            fifthLabel.setText("Results:")
            Fig = DataMonitoring.LiveMonitoringData()
            SubSecondGridLayout.addWidget(firstLabel,0,0)
            SubSecondGridLayout.addWidget(firstComboBox,0,1)
            
            SubSecondGridLayout.addWidget(secondLabel,1,0)
            SubSecondGridLayout.addWidget(secondtextbox,1,1)  

            SubSecondGridLayout.addWidget(thirdLabel,2,0)
            SubSecondGridLayout.addWidget(thirdtextbox,2,1)
            
            SubSecondGridLayout.addWidget(forthLabel,3,0)
            SubSecondGridLayout.addWidget(forthtextbox,3,1)
            
            SubSecondGridLayout.addWidget(fifthLabel,4,0)
            #SubSecondGridLayout.addWidget(self.canvas,5,0, 10,5)
                                  
        else: 
            firstLabel.setText("")
            firsttextbox = QLineEdit(ipAddress,ChildWindow)
            textboxValue = firsttextbox.text()
            secondLabel.setText("")
            thirdLabel.setText("") 
        self.SubFilterGroupBox.setLayout(SubSecondGridLayout)

    def plotting_menu(self):
        fig = Figure()
        self.canvas = FigureCanvas(fig)
        #FigureCanvas.__init__(self, fig)
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        data = [random.random() for i in range(10)]
        ax.plot(data, '*-')
        self.canvas.draw()
         
    def set_filter(self, x): 
        self._filter = x 
        
    def set_openingAngleFilter(self, x): 
        self.__openingAngleFilter = x 
    
    def set_self_ipAddress(self,x):
        # x = self.firsttextbox.text()
        self.self_ipAddress =x
        
        
    def set_label(self, text):
        self.outLabel.setText(text)

    def set_click(self):
        dim = self.get_dimention()
        ch = self.get_channel()
        text = "%s will be set to  %s direction"%(ch,dim)
        print(text)
        
    # setter method 
    def set_channel(self, x): 
        self._channel = x 
    
    def set_dimention(self, x): 
        self._dim = x
        dim = self.get_dimention()
        ch = self.get_channel()
        text = "%s will be set to  %s direction"%(ch,dim)
        self.outLabel.setText(text)
        self.outLabel.adjustSize()
        
    # getter methods
    def get_openingAngleFilter(self):
        return self.__openingAngleFilter
    
    def get_filter(self): 
        return self._filter
        
    def set_openingAngleCalculation(self): 
        self.mainWindow.set_interface(self._openingAngleCalculation)
        return self._openingAngleCalculation 
    
    def get_self_ipAddress(self):
        return self_ipAddress
    
    def get_channel(self): 
        return self._channel 
    
    def get_dimention(self): 
        return self._dim

    def clicked(self,q):
        print("is clicked")
                

        

if __name__ == "__main__":
    pass

