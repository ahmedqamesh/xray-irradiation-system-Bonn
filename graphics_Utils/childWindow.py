from matplotlib.backends.qt_compat import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvas as FigureCanvas
import matplotlib.pyplot as plt
import random
from PyQt5.QtCore    import *
from PyQt5.QtGui     import *
from PyQt5.QtWidgets import *
import os
from analysis import analysis_utils,  plottingCalibration, analysis
from analysis import fitEquations as f
from graphics_Utils import mainWindow , DataMonitoring , MenuWindow , LogWindow , plottingCanvas
import numpy as np
from matplotlib.figure import Figure
from IPython.display import clear_output
from scipy.optimize import curve_fit
import time
rootdir = os.path.dirname(os.path.abspath(__file__)) 
class ChildWindow(QWidget):  
    def __init__(self, parent = None):
       super(ChildWindow,self).__init__(parent)
       self.test_directory = mainWindow.MainWindow().get_testDirectory()
       conf = analysis_utils.open_yaml_file(file="Xray_irradiation_conf.yaml", directory=rootdir[:-15])
       self.__max_dose = conf['Info']["max_dose"]
       self.__max_current = conf['Info']["max_current"]
       self.__max_voltage = conf['Info']["max_voltage"]
       self.__max_radius = conf['Info']["max_radius"]
       self.__max_height = conf['Info']["max_height"]
       self.__voltage_range = conf['Info']["voltage_range"]
        
       self.__filtersList = conf['Tests']["filters"]
       self.__depthList = conf['Tests']["depth"]
       self.__currentList = conf['Tests']["current"]
       self.__voltageList = conf['Tests']["voltage"]
       self.__voltage = 0
       self.__current = 0
       self.__filterItem = 0
       self.__height   = 0       
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
        ChildWindow.setObjectName("Dose Calculator")
        ChildWindow.setWindowTitle("Dose Calculator")
        ChildWindow.resize(600, 700)  # w*h
        font = QFont('Open Sans',20, QFont.Bold)
        style = "background-color: black;""color: #00ff00;""border: 2px solid red;"
        
        tubeLabel = QLabel("Tube parameters: ")
        tubeLabel.setText("Tube parameters: ")
        tubeLabel.setFont(QFont("Times", 12, QFont.Bold))
        
        self.currentLabel = QLabel("Current: ")
        self.currentLabel.setText("      Current [mA] ")
        
        voltageLabel = QLabel("Voltage: ")
        voltageLabel.setText("      Voltage [kV]    ") 
                
        self.tubeCurrentComboBox = QComboBox()
        for item in self.__currentList: self.tubeCurrentComboBox.addItem(item)
        self.tubeCurrentComboBox.activated[str].connect(self.set_current)
        
        self.tubeCurrentDial = QDial()
        self.tubeCurrentDial.setMinimum(0);
        self.tubeCurrentDial.setMaximum(self.__max_current);
        self.tubeCurrentDial.setNotchesVisible(True)
        self.tubeCurrentDial.valueChanged.connect(self.change_dose)
        
        self.tubeVoltageComboBox = QComboBox()
        for item in self.__voltageList: self.tubeVoltageComboBox.addItem(item)
        self.tubeVoltageComboBox.activated[str].connect(self.set_voltage)
        
        depthLabel = QLabel("Depth: ")
        depthLabel.setText("           Depth [cm] ")
        
        self.depthComboBox = QComboBox()
        for item in self.__depthList : self.depthComboBox.addItem(item)
        self.depthComboBox.activated[str].connect(self.set_height)
        
        filterLabel = QLabel("Filter: ")
        filterLabel.setText("     Filter")

        self.filterComboBox = QComboBox()
        for item in self.__filtersList: self.filterComboBox.addItem(item)
        self.filterComboBox.activated[str].connect(self.set_filterItem)
        
        
        line = QFrame()
        line.setGeometry(QRect(320, 150, 118, 3))
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        
        testLabel = QLabel("Beam Spot Size: ")
        testLabel.setText("Beam Spot Size: ")
        testLabel.setFont(QFont("Times", 12, QFont.Bold))
                
        labelLayout  = QVBoxLayout()         
        self.doseDepthLabel = QLabel("        ")
        self.doseDepthLabel.setFont(font)
        self.doseDepthLabel.setStyleSheet(style)
        labelLayout.addWidget(self.doseDepthLabel)
        
        refresh_button = QPushButton("")
        refresh_button.setIcon(QIcon('graphics_Utils/icons/icon_reset.png' ))
        refresh_button.clicked.connect(self.change_dose)  
        
        # Define label
        VLayout = QVBoxLayout()
        doseDepthLabel = QLabel("")
        doseDepthLabel.setText("  Dose rate [50mA /40kV]")
        self.doseLabel = QLabel("        ")
        self.doseLabel.setFont(font)
        self.doseLabel.setStyleSheet(style)

        self.label = QLabel(self)
        HLayout = QHBoxLayout()
        self.height_slider , height_Group = self.createSliderGroup(i=2, limit = self.__max_height)
        self.height_slider.valueChanged.connect(self.update_plot)
        
        self.fig = DataMonitoring.BeamMonitoring()
        HLayout.addWidget(self.height_slider)
        HLayout.addWidget(self.fig)
        stop_button = QPushButton("close")
        stop_button.setIcon(QIcon('graphics_Utils/icons/icon_close.png' ))
        stop_button.clicked.connect(ChildWindow.close)  
        
        mainFrame = QFrame(self)
        mainFrame.setStyleSheet("QWidget { background-color: #eeeeec; }")
        mainFrame.setLineWidth(0.6)
        ChildWindow.setCentralWidget(mainFrame)
        mainLayout = QGridLayout()
        mainLayout.addWidget(tubeLabel, 0, 0)
        mainLayout.addLayout(labelLayout,0,2)#, 1, 5,2,1)
        mainLayout.addWidget(refresh_button,0,3)
        mainLayout.addWidget(self.currentLabel, 1, 0)
        mainLayout.addWidget(voltageLabel, 1, 1)
        mainLayout.addWidget(depthLabel,1, 2)
        mainLayout.addWidget(filterLabel,1, 3)
        mainLayout.addWidget(self.tubeCurrentDial, 2, 0)
        mainLayout.addWidget(self.tubeVoltageComboBox, 2, 1)
        mainLayout.addWidget(self.depthComboBox,2, 2)
        mainLayout.addWidget(self.filterComboBox,2,3)
        mainLayout.addWidget(line,3, 0, 2, 6)
        mainLayout.addWidget(testLabel,5,0)
        mainLayout.addWidget(doseDepthLabel,6,2)
        mainLayout.addWidget(self.doseLabel,7,2)
        
        mainLayout.addLayout(HLayout,8, 0,1,4)
        mainLayout.addWidget(stop_button,10,3)
        mainFrame.setLayout(mainLayout)
                
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

    def createSliderGroup(self, i=0, limit=20, range = [1,2,3]):
        self.sliders = ["Tube voltage", "Tube current", "Height:", "  Beam radius", "Dose rate" ]
        groupBox= QGroupBox()#sliders[i]) 
        frame = QFrame(self)
        frame.setStyleSheet("background-color: w;")
        frame.setLineWidth(0.9)
        self.verticalLayout = QVBoxLayout()
        # Define Slider
        slider = QSlider(Qt.Vertical)
        name = "{}".format(i)
        setattr(self, name, self.label) 
        slider.setObjectName(name) 
        slider.setRange(0, limit)
        slider.setFocusPolicy(Qt.StrongFocus)
        slider.setTickPosition(QSlider.TicksBothSides)
        slider.setInvertedAppearance(True)
        
        self.horizontalLayout = QHBoxLayout()
        spacerItem1 = QSpacerItem(0, 5, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.horizontalLayout.addWidget(slider)
        spacerItem2 = QSpacerItem(0, 5, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        #self.setCentralWidget(frame)
        frame.setLayout(self.horizontalLayout)
        groupBox.setLayout(self.horizontalLayout)
        return slider , groupBox

    def changevalue(self, value):
        sender = self.sender()
        i = int(sender.objectName())
        label = getattr(self, sender.objectName())
        if i == 0:
            dV = f.dose_voltage(V = value, filter = "without", depth ="8cm")
            print(dV)        
        if i == 1:
            dC = f.dose_current(I = value, filter = "without", depth ="3cm",voltage = "40kV")
            print(dC)    
        if i == 2:
            dD = f.dose_depth(depth = value, filter = self.get_filterItem(), current =self.get_current(),voltage = self.get_voltage())
            r = f.opening_angle(depth = value,filter= self.get_filterItem())
            self.doseDepthLabel.setText(str(dD)[0:5]+"  Mrad/hr")
        if i == 3:
            height = f.opening_angle(r = value)
            print(height)     
        if i == 4:
            current = f.dose_current(d = value, filter = "without", depth ="3cm", voltage = "40kV")
            print(current)
    
    def change_dose(self,value):
        self.set_current(float(value))
        self.currentLabel.setText("    "+str(self.get_current()) + "[mA] ")
        dC = f.dose_current(I = self.get_current(), filter = self.get_filterItem(), depth =self.get_height(),voltage = self.get_voltage())
        self.doseDepthLabel.setText(str(dC)[0:5]+"  Mrad/hr")
                            
    def update_plot(self):
        # Plot a cone represents the beam spot radius
        h = self.height_slider.value()
        dD = f.dose_depth(depth = h, filter = "without", current ="50mA",voltage = "40kV")
        self.doseLabel.setText(str(dD)[0:5]+"  Mrad/hr")
        h_space = np.linspace(0, h, 20)
        r_space = f.opening_angle(depth = h_space,filter= self.get_filterItem())
        r = f.opening_angle(depth = h,filter= self.get_filterItem())
        self.fig.axes.cla()
        col_row = plt.cm.BuPu(np.linspace(0.3, 0.9, len(r_space)))
        for i in range(len(r_space)):
            x, y = np.linspace(-r_space[i], r_space[i], 2), [h_space[i] for _ in np.arange(2)]
            self.fig.update_figure(x, y,h,r,self.get_filterItem(), col_row[-i])
            self.fig.axes.invert_yaxis()
            
    def set_filterItem(self, x): 
        self.__filterItem = x 

    def set_voltage(self,x):
        self.__voltage = x

    def set_current(self,x):
        self.__current = x

    def set_dose(self,x):
        self.__dose = x
    
    def set_height(self,x):
        self.__height = x
    
    def set_radius(self,x):
        self.__radius = x 

    def get_filterItem(self): 
        if self.__filterItem !=0:
            return self.__filterItem
        else:
            return str(self.filterComboBox.currentText())

    def get_voltage(self):
        if self.__voltage !=0:
            return self.__voltage
        else:
            return str(self.tubeVoltageComboBox.currentText())
        
    def get_current(self):
        if self.__current !=0:
            return self.__current 
        else:
            return float(self.tubeCurrentDial.value())
        
    def get_dose(self):
        return self.__dose  
    
    def get_height(self):
        if self.__height !=0:
            return self.__height
        else:
            return str(self.depthComboBox.currentText())

    def get_radius(self):
        return self.__radius
    
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

