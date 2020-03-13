from matplotlib.backends.qt_compat import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvas as FigureCanvas
import matplotlib.pyplot as plt
import random
from PyQt5.QtCore    import *
from PyQt5.QtGui     import *
from PyQt5.QtWidgets import *
import os
from analysis import analysis_utils,  plottingCalibration, analysis
from graphics_Utils import mainWindow , DataMonitoring , MenuWindow , LogWindow , plottingCanvas
import numpy as np
from matplotlib.figure import Figure
import time
rootdir = os.path.dirname(os.path.abspath(__file__)) 
class ChildWindow(QWidget):  
    def __init__(self, parent = None):
       super(ChildWindow,self).__init__(parent)
       self.test_directory = mainWindow.MainWindow().get_testDirectory()
       
       #self.menu._createStatusBar(self)
    def OutputChildWindow(self, ChildWindow):
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

    def doseCalculatorWindow(self, ChildWindow):
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
        
    def ChildMenu(self, ChildWindow = None,csv = True, firstitems=None, test_name = "Opening Angle Test",dir="opening_angle/", Fig =None, plot_prefix = None, name_prefix = "None"):
        self._directory = self.test_directory+dir
        ChildWindow.setObjectName(test_name)
        ChildWindow.setWindowTitle(test_name)
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
        self.set_firstItem(firstitems[1])
        firstComboBox = QComboBox(ChildWindow)
        for item in firstitems: firstComboBox.addItem(item)
        firstItem = self.get_firstItem()
        def _SubFilterGroupMenu():
            ChildWindow.resize(700, 700) #w*h
            FirstGridLayout.removeWidget(self.SubFilterGroupBox)
            self.SubFilterGroupBox.deleteLater()
            self.SubFilterGroupBox = None
            firstItem = self.get_firstItem()
            test_dir = self._directory+firstItem+"/" 
            if csv is not None: 
                test_file = test_dir +name_prefix + firstItem +".csv" 
            else: 
                test_file = test_dir +name_prefix + firstItem +".h5"    
            self.openSubGroupMenu(ChildWindow = ChildWindow, firstItem = firstItem, test_file =test_file, test_dir = test_dir, plot_prefix= plot_prefix, name_prefix=name_prefix)
            FirstGridLayout.addWidget(self.SubFilterGroupBox,1,0)  

        firstComboBox.activated[str].connect(self.set_firstItem)
        self.openSubGroupMenu(firstItem = firstItem) 
        
        firstComboBox.activated[str].connect(_SubFilterGroupMenu)
        firstHBoxLayout.addWidget(firstLabel)
        firstHBoxLayout.addWidget(firstComboBox)
               
        FirstGridLayout.addLayout(firstHBoxLayout,0,0)
        self.FirstGroupBox.setLayout(FirstGridLayout)
        MainLayout.addWidget(self.FirstGroupBox, 0, 0)
        plotframe.setLayout(MainLayout) 
        QtCore.QMetaObject.connectSlotsByName(ChildWindow)  
        
    def openSubGroupMenu(self, ChildWindow = None, firstItem= None ,plot_prefix =None,  test_file = None, test_dir = None, name_prefix = "None"):
        self.SubFilterGroupBox= QGroupBox("")
        SubSecondGridLayout =  QGridLayout()
        firstLabel= QLabel("firstLabel", ChildWindow)
        secondLabel = QLabel("secondLabel", ChildWindow)
        thirdLabel = QLabel("thirdLabel", ChildWindow)
        forthLabel = QLabel("secondLabel", ChildWindow)
        fifthLabel = QLabel("thirdLabel", ChildWindow)
        firstGroupBox= QGroupBox("Test Info:")
        secondLabel.setText("Test Directory:")
        thirdLabel.setText("Test Date:")
        forthLabel.setText("Last Modified:")
        fifthLabel.setText("Results:")
        close_button = QPushButton("Close")
        close_button.setIcon(QIcon('graphics_Utils/icons/icon_true.png'))
        close_button.setStatusTip('close session') # show when move mouse to the icon
        
        if ChildWindow is not None:
            try: 
                test_date =time.ctime(os.path.getmtime(test_file))
                test_modify = time.ctime(os.path.getctime(test_file))
            except Exception:
                test_date =time.ctime(os.path.getmtime(test_dir))
                test_modify = time.ctime(os.path.getctime(test_dir))
            secondtextbox = QLineEdit(test_dir)
            secondTextBoxValue = secondtextbox.text()
            thirdtextbox = QLineEdit(test_date)
            thirdTextBoxValue = thirdtextbox.text()
            forthtextbox = QLineEdit(test_modify)
            forthTextBoxValue = forthtextbox.text()
            Fig =  plottingCanvas.PlottingCanvas(test_file=test_file, tests=[firstItem], plot_prefix = plot_prefix, name_prefix =name_prefix)
            close_button.clicked.connect(ChildWindow.close)        
            SubSecondGridLayout.addWidget(secondLabel,0,0)
            SubSecondGridLayout.addWidget(secondtextbox,0,1)  
            SubSecondGridLayout.addWidget(thirdLabel,1,0)
            SubSecondGridLayout.addWidget(thirdtextbox,1,1)
            
            SubSecondGridLayout.addWidget(forthLabel,2,0)
            SubSecondGridLayout.addWidget(forthtextbox,2,1)        
            SubSecondGridLayout.addWidget(fifthLabel,3,0)
            SubSecondGridLayout.addWidget(Fig,4,0, 4,0)
            SubSecondGridLayout.addWidget(close_button,25,5)
        self.SubFilterGroupBox.setLayout(SubSecondGridLayout)

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

    # setter method                    
    def set_filter(self, x): 
        self._filter = x 
        
    def set_firstItem(self, x): 
        self.__firstItem = x 
    
    def set_self_ipAddress(self,x):
        # x = self.firsttextbox.text()
        self.self_ipAddress =x
        
    def set_label(self, text):
        self.outLabel.setText(text)

   
    # getter methods
    def get_firstItem(self):
        return self.__firstItem
    
    def get_filter(self): 
        return self._filter
        
    def set_openingAngleCalculation(self): 
        self.mainWindow.set_interface(self._openingAngleCalculation)
        return self._openingAngleCalculation 

    def clicked(self,q):
        print("is clicked")

if __name__ == "__main__":
    pass

