from matplotlib.backends.qt_compat import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvas
from PyQt5.QtCore    import *
from PyQt5.QtGui     import *
from PyQt5.QtWidgets import *
import os
from graphics_Utils import DataMonitoring , MenuWindow , LogWindow
from analysis import analysis_utils
import numpy as np
ipAddress = '192.168.1.254'
rootdir = os.path.dirname(os.path.abspath(__file__)) 
class Ui_ChildWindow(QWidget):  
    def __init__(self):
       super().__init__() 
       self.menu= MenuWindow.MenuBar()
       self._openingAngleCalculation = "The beam profile at a specific height"
       self_ipAddress =ipAddress
       conf = analysis_utils.open_yaml_file(file ="BeamSpot_cfg.yaml",directory ="/Users/ahmedqamesh/git /Xray_Irradiation_System_Bonn/")
       self.filterList = conf['Tests']['Filters']
       print(self.filterList)
       #print("the directory: %s"%  os.path.dirname("/Users/ahmedqamesh/git/MOPS_daq_cfg.yml"))
       #print("last modified: %s" % time.ctime(os.path.getmtime("MOPS_daq_cfg.yml")))
       #print("created: %s" % time.ctime(os.path.getctime("MOPS_daq_cfg.yml")))
    
       #self.menu._createStatusBar(self)
 
    def settingChannel(self, ChildWindow):
        ChildWindow.setObjectName("ChildWindow")
        ChildWindow.setWindowTitle("Motor stage settings")
        #ChildWindow.resize(568, 109) 
        ChildWindow.setGeometry(300, 300, 300, 200)            
        plotframe = QFrame(ChildWindow)
        plotframe.setStyleSheet("QWidget { background-color: #eeeeec; }")
        plotframe.setLineWidth(0.6)
        ChildWindow.setCentralWidget(plotframe)
        
        self.mainGroupBox = QGroupBox("Set channel")
        mainLayout = QGridLayout()
                
        #comboBox and label for channel
        chLabel = QLabel("Channel", ChildWindow)
        chLabel.setText("Select Channel Number")

        items = ["---","ch01","ch02","ch03"]
        chComboBox = QComboBox(ChildWindow)
        for item in items: chComboBox.addItem(item)
        chComboBox.activated[str].connect(self.set_channel)

#         chComboBox.currentTextChanged.connect(self.on_combobox_changed)
#         listwidgetLayout = QHBoxLayout()
#         chlistwidget = QListWidget()
#         chlistwidget.insertItem(0, "Ch1")
#         chlistwidget.insertItem(1, "Ch2")
#         chlistwidget.insertItem(2, "Ch3")
#         chlistwidget.clicked.connect(self.setaddress(ChildWindow))
#         chlistwidget.clicked.connect(self.setaddress(ChildWindow))
#         listwidgetLayout.addWidget(chlistwidget)
                  
         #comboBox  and label  for coordinates
        dimLabel = QLabel("Coordinate", ChildWindow)
        dimLabel.setText("Choose coordinate")
        
        items = ["---","x","y","z"]
        dimComboBox = QComboBox(ChildWindow)
        for item in items: dimComboBox.addItem(item)
        dimComboBox.activated[str].connect(self.set_dimention)
#         dimlistwidget = QListWidget()
#         dimlistwidget.insertItem(0, "x")
#         dimlistwidget.insertItem(1, "y")
#         dimlistwidget.insertItem(2, "z")
#         dimlistwidget.clicked.connect(self.setaddress)
#         listwidgetLayout.addWidget(dimlistwidget)
#         
#         Set_button = QPushButton("Set")
#         listwidgetLayout.addWidget(Set_button)
#         Set_button.clicked.connect(self.setaddress) 
#         childLayout.addLayout(listwidgetLayout)
          
        self.outLabel = QLabel("channel settings",ChildWindow)
        self.outLabel.setStyleSheet("background-color: white; border: 2px inset black;")# min-height: 200px;")
        
        set_button = QPushButton("Set")
        set_button.clicked.connect(self.set_click)
        
        close_button = QPushButton("close")
        close_button.clicked.connect(ChildWindow.close)

        gridLayout = QGridLayout()
        gridLayout.addWidget(chLabel,0,0)
        gridLayout.addWidget(chComboBox,1,0)
        
        gridLayout.addWidget(dimLabel,2,0)
        gridLayout.addWidget(dimComboBox,3,0)
        
        
        gridLayout.addWidget(self.outLabel,4,0)
        gridLayout.addWidget(set_button,4,1)    
        self.mainGroupBox.setLayout(gridLayout) 

        mainLayout.addWidget(self.mainGroupBox, 0, 0)

        plotframe.setLayout(mainLayout) 

        self.menu._createStatusBar(ChildWindow)
        QtCore.QMetaObject.connectSlotsByName(ChildWindow)     
    
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
        test_dir = "/../../"
        test_date ="1/1/2001"
        ChildWindow.setObjectName(test_name)
        ChildWindow.setWindowTitle(test_name)
        ChildWindow.resize(310, 600) #w*h
        MainLayout = QGridLayout()
        #Define a frame for that group
        plotframe = QFrame(ChildWindow)
        plotframe.setLineWidth(0.6)
        ChildWindow.setCentralWidget(plotframe)
        
        #Define First Group
        self.FirstGroupBox= QGroupBox("Test Info:")
        FirstGridLayout =  QGridLayout()
        #comboBox and label for channel
        firstHBoxLayout = QHBoxLayout(ChildWindow)
        firstLabel = QLabel("Test Type: ", ChildWindow)
        firstLabel.setText("Test Type: ")
        firstitems = ["With filter",
                  "Without Filter"]
        firstComboBox = QComboBox(ChildWindow)
        for item in firstitems: firstComboBox.addItem(item)
        firstComboBox.activated[str].connect(self.set_openingAngleCalculation)
        
        
    #    firstTextbox = QLineEdit(test_name, ChildWindow)
    #    firstTextboxValue = firstTextbox.text()
        firstHBoxLayout.addWidget(firstLabel)
        firstHBoxLayout.addWidget(firstComboBox)        
        
        #comboBox and label for channel
        secondHBoxLayout = QHBoxLayout(ChildWindow)
        secondLabel = QLabel("Data Directory: ", ChildWindow)
        firstLabel.setText("Data Directory: ")
        secondTextbox = QLineEdit(test_dir, ChildWindow)
        secondTextboxValue = secondTextbox.text()
        secondHBoxLayout.addWidget(secondLabel)
        secondHBoxLayout.addWidget(secondTextbox)   
        
        #comboBox and label for channel
        thirdHBoxLayout = QHBoxLayout(ChildWindow)
        thirdLabel = QLabel("Test Date   :", ChildWindow)
        thirdLabel.setText("Test Date   :")
        thirdTextbox = QLineEdit(test_date, ChildWindow)
        thirdTextboxValue = thirdTextbox.text()
        thirdHBoxLayout.addWidget(thirdLabel)
        thirdHBoxLayout.addWidget(thirdTextbox)  
        
        Fig = DataMonitoring.LiveMonitoringData()
                         
        FirstGridLayout.addLayout(firstHBoxLayout,0,0)
        FirstGridLayout.addLayout(secondHBoxLayout,1,0)
        FirstGridLayout.addLayout(thirdHBoxLayout,2,0)
        FirstGridLayout.addWidget(Fig,3,0)
        self.FirstGroupBox.setLayout(FirstGridLayout)
        #Define the second group
        self.SecondGroupBox= QGroupBox("Beam profile size vs height")
        SecondGridLayout =  QGridLayout()        
        #comboBox and label for channel
        calculationsLayout = QHBoxLayout()
        caLabel = QLabel("Calculations :", ChildWindow)
        caLabel.setText("Calculations  :")
        
        calculationitems = ["-----------------------------------------------",
                          "The beam profile at a specific height",
                          "The height for a specific beam profile"]
        calculationsComboBox = QComboBox(ChildWindow)
        for item in calculationitems: calculationsComboBox.addItem(item)
        calculationsComboBox.activated[str].connect(self.set_openingAngleCalculation)
        
        calculationsLayout.addWidget(caLabel)
        calculationsLayout.addWidget(calculationsComboBox)
        SecondGridLayout.addLayout(calculationsLayout,0,0)
        #Another group will be here for Bus parameters
        #self.BusParametersGroupBox(interface =self._openingAngleCalculation)
        self.SecondGroupBox.setLayout(SecondGridLayout)
        
        MainLayout.addWidget(self.FirstGroupBox, 0, 0)
        MainLayout.addWidget(self.SecondGroupBox, 1, 0)
        plotframe.setLayout(MainLayout) 

        self.menu._createStatusBar(ChildWindow)
        QtCore.QMetaObject.connectSlotsByName(ChildWindow)        
        
                        
    def ChildMenu(self, ChildWindow):
        test_name = "Opening Angle Test"
        test_dir = "/../../"
        test_date ="1/1/2001"
        ChildWindow.setObjectName(test_name)
        ChildWindow.setWindowTitle(test_name)
        ChildWindow.resize(310, 600) #w*h
        MainLayout = QGridLayout()
        #Define a frame for that group
        plotframe = QFrame(ChildWindow)
        plotframe.setLineWidth(0.6)
        ChildWindow.setCentralWidget(plotframe)
        
        #Define First Group
        self.FirstGroupBox= QGroupBox("Test Info:")
        FirstGridLayout =  QGridLayout()
        #comboBox and label for channel
        firstHBoxLayout = QHBoxLayout(ChildWindow)
        firstLabel = QLabel("Test Name: ", ChildWindow)
        firstLabel.setText("Test Name: ")
        firstTextbox = QLineEdit(test_name, ChildWindow)
        firstTextboxValue = firstTextbox.text()
        firstHBoxLayout.addWidget(firstLabel)
        firstHBoxLayout.addWidget(firstTextbox)        
        
        #comboBox and label for channel
        secondHBoxLayout = QHBoxLayout(ChildWindow)
        secondLabel = QLabel("Data Directory: ", ChildWindow)
        firstLabel.setText("Data Directory: ")
        secondTextbox = QLineEdit(test_dir, ChildWindow)
        secondTextboxValue = secondTextbox.text()
        secondHBoxLayout.addWidget(secondLabel)
        secondHBoxLayout.addWidget(secondTextbox)   
        
        #comboBox and label for channel
        thirdHBoxLayout = QHBoxLayout(ChildWindow)
        thirdLabel = QLabel("Test Date   :", ChildWindow)
        thirdLabel.setText("Test Date   :")
        thirdTextbox = QLineEdit(test_date, ChildWindow)
        thirdTextboxValue = thirdTextbox.text()
        thirdHBoxLayout.addWidget(thirdLabel)
        thirdHBoxLayout.addWidget(thirdTextbox)  
        
        Fig = DataMonitoring.LiveMonitoringData()
                         
        FirstGridLayout.addLayout(firstHBoxLayout,0,0)
        FirstGridLayout.addLayout(secondHBoxLayout,1,0)
        FirstGridLayout.addLayout(thirdHBoxLayout,2,0)
        FirstGridLayout.addWidget(Fig,3,0)
        self.FirstGroupBox.setLayout(FirstGridLayout)
        
        #Define the second group
        self.SecondGroupBox= QGroupBox("Bus Configuration")
        SecondGridLayout =  QGridLayout()        
        #comboBox and label for channel
        chLabel = QLabel("CAN Channel:", ChildWindow)
        chLabel.setText("CAN Channel:")
        controllerLayout = QHBoxLayout()
        interfaceitems = ["----","Kvaser","AnaGate","Others"]
        interfaceComboBox = QComboBox(ChildWindow)
        for item in interfaceitems: interfaceComboBox.addItem(item)
        interfaceComboBox.activated[str].connect(self.openSubFilterMenu)
        
        controllerLayout.addWidget(interfaceComboBox)
        
        #Another group will be here for Bus parameters
        #self.BusParametersGroupBox(interface =self._openingAngleCalculation)
        
        modeLabel = QLabel("CAN Mode:", ChildWindow)
        modeLabel.setText("CAN Mode:")
        modeitems = ["CAN"]
        modeComboBox = QComboBox(ChildWindow)
        for item in modeitems: modeComboBox.addItem(item)
        modeComboBox.activated[str].connect(self.clicked)

        #FirstButton
        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(ChildWindow.close)

        HGridLayout =  QGridLayout()  
        set_button = QPushButton("Set in all")
        set_button.setIcon(QIcon('graphics_Utils/icons/icon_true.png'))
        set_button.clicked.connect(self.clicked)
        
        h , w = 50 , 25
        connectButton = QPushButton("")
        connectButton.clicked.connect(self.get_openingAngleCalculation)  
        connectButton.setFixedWidth(w)
        connectButton.setIcon(QIcon('graphics_Utils/icons/icon_disconnect.jpg'))
        icon = QIcon()
        icon.addPixmap(QPixmap('graphics_Utils/icons/icon_disconnect.jpg'),  QIcon.Normal, QIcon.Off)
        icon.addPixmap(QPixmap('graphics_Utils/icons/icon_connect.jpg'), QIcon.Normal,  QIcon.On)
        connectButton.setIcon(icon)
        connectButton.setCheckable(True)
        
        
        setLabel = QLabel("Set same bit rate in all CAN controllers", ChildWindow)
        setLabel.setText("Set same bit rate in all CAN controllers")
        
        HGridLayout.addWidget(set_button,0,0)
        HGridLayout.addWidget(connectButton,0,1) 
        HGridLayout.addWidget(setLabel,0,2)
        
        self.SecondGroupBox.setLayout(SecondGridLayout)
        SecondGridLayout.addWidget(chLabel,0,0)
        SecondGridLayout.addLayout(controllerLayout,1,0)
        SecondGridLayout.addWidget(modeLabel,2,0)
        SecondGridLayout.addWidget(modeComboBox,3,0)
        
        def _interfaceParameters():
            interface = self._openingAngleCalculation
            
            SecondGridLayout.removeWidget(self.SubSecondGroupBox)
            self.SubSecondGroupBox.deleteLater()
            self.SubSecondGroupBox = None              
            self.BusParametersGroupBox(interface = interface)
            SecondGridLayout.addWidget(self.SubSecondGroupBox,4,0)        
        
        SecondGridLayout.addLayout(HGridLayout,5,0)
        interfaceComboBox.activated[str].connect(_interfaceParameters)

        MainLayout.addWidget(self.FirstGroupBox, 0, 0)
        MainLayout.addWidget(self.SecondGroupBox, 1, 0)
        plotframe.setLayout(MainLayout) 

        self.menu._createStatusBar(ChildWindow)
        QtCore.QMetaObject.connectSlotsByName(ChildWindow)        
        

    def openSubFilterMenu(self, interface ="AnaGate"):
        #Define subGroup
        self.SubFilterBox= QGroupBox("Bus Parameters")
        SubSecondGridLayout =  QGridLayout()
        firstLabel= QLabel("firstLabel", self)
        secondLabel = QLabel("secondLabel", self)
        thirdLabel = QLabel("thirdLabel", self)
        firstComboBox = QComboBox(self)
        if (interface == "Cu"):
            firstLabel.setText("Bus Speed:")
            firstItems = ["1000 kbit/s, 75.0%","500 kbit/s, 75.0%","250 kbit/s, 75.0%"," 125 kbit/s, 75.0%","100 kbit/s, 75.0%","83.333 kbit/s, 75.0%","62.500 kbit/s, 75.0%","50 kbit/s, 75.0%","33.333 kbit/s, 75.0%" ]
            for item in firstItems: firstComboBox.addItem(item)
            firstComboBox.activated[str].connect(self.clicked)
            secondLabel.setText("SJW:")
            secondItems = ["1","2","3","4"]
            secondComboBox = QComboBox(self)
            for item in secondItems: secondComboBox.addItem(item)
            secondComboBox.activated[str].connect(self.clicked)
            thirdLabel.setText("Bit Timing:")
            SubSecondGridLayout.addWidget(firstComboBox,0,1)
        if (interface == "AnaGate"):
            firstLabel.setText("IP address")
            self.firsttextbox = QLineEdit(ipAddress,self)
            textboxValue = self.firsttextbox.text()
            secondLabel.setText("SJW:")
            secondItems = ["1","2","3","4"]
            secondComboBox = QComboBox(self)
            for item in secondItems: secondComboBox.addItem(item)
            secondComboBox.activated[str].connect(self.clicked)
            thirdLabel.setText("Bit Timing:")
            SubSecondGridLayout.addWidget(firsttextbox,0,1)
            
        if (interface == "Al"):        
            firstLabel.setText("Speed:")
            firstItems = [""]
            firstComboBox = QComboBox(self)
            for item in firstItems: firstComboBox.addItem(item)
            firstComboBox.activated[str].connect(self.clicked)
            secondLabel.setText("SJW:")
            seconditems = [""]
            secondComboBox = QComboBox(self)
            for item in seconditems: secondComboBox.addItem(item)
            secondComboBox.activated[str].connect(self.clicked)
            thirdLabel.setText("Bit Timing:")
            SubSecondGridLayout.addWidget(firstComboBox,0,1)
            
        SubSecondGridLayout.addWidget(firstLabel,0,0)
        SubSecondGridLayout.addWidget(secondLabel,1,0)
        SubSecondGridLayout.addWidget(secondComboBox,1,1)
        SubSecondGridLayout.addWidget(thirdLabel,2,0)
        self.SubFilterBox.setLayout(SubSecondGridLayout)


    def set_filter(self, x): 
        self._filter = x 
        
    def set_openingAngleCalculation(self, x): 
        self._openingAngleCalculation = x 
    
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
    def get_filter(self): 
        return self._filter
        
    def get_openingAngleCalculation(self): 
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

