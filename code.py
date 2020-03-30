import sys
from matplotlib.backends.qt_compat import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvas

from matplotlib.figure import Figure
from matplotlib.widgets import Slider

from PyQt5.QtCore    import *
from PyQt5.QtGui     import *
from PyQt5.QtWidgets import *
import matplotlib.pyplot as plt
import pyqtgraph as pg
import numpy as np
import os
from IPython.display import clear_output
from scipy.optimize import curve_fit
from analysis import fitEquations as f
from analysis import analysis_utils
rootdir = os.path.dirname(os.path.abspath(__file__))

class BeamMonitoring(FigureCanvas):
    """A canvas that updates itself every second with a new plot."""
    def __init__(self, parent=None):
        self.fig = Figure(edgecolor = "black",linewidth ="2.5")#, facecolor="#e1ddbf")
        self.axes = self.fig.add_subplot(111)
        FigureCanvas.__init__(self, self.fig )
        #FigureCanvas.setSizePolicy(self,QSizePolicy.Expanding,QSizePolicy.Expanding),FigureCanvas.updateGeometry(self)
        self.axes.set_xlabel(r'Diameter (d) [cm]', size = 10)
        self.axes.set_ylabel(r'Height from the the collimator holder(h) [cm]', size = 10) 
        self.axes.grid(True)
        self.axes.invert_yaxis()
        self.axes.set_xlim(-6,6)
        plt.tight_layout()                 
        self.axes.set_title('Diameter covered by beam spot', fontsize=12)

    def update_figure(self,x,y,h,r,filter,color):
        #self.axes.invert_yaxis()
        self.axes.set_xlabel(r'Diameter (d) [cm]', size = 10)
        self.axes.set_ylabel(r'Height from the the collimator holder(h) [cm]', size = 10) 
        self.axes.grid(True)
        self.axes.set_xlim(-6,6)
        self.axes.set_title('Diameter covered by beam spot [%s filter]'%filter, fontsize=12)
        self.axes.plot(x, y, color=color)
        self.axes.text(0.95, 0.90, "Height = %.2f cm\n radius = %.2f cm"%(h,r),
               horizontalalignment='right', verticalalignment='top', transform=self.axes.transAxes,
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.7))
        
        self.draw()
                   
class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)   
        conf = analysis_utils.open_yaml_file(file="Xray_irradiation_conf.yaml", directory=rootdir[:])
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
                
    def doseCalculatorWindow(self):
        self.setObjectName("Dose Calculator")
        self.setWindowTitle("Dose Calculator")
        self.resize(600, 700)  # w*h
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
        
        self.fig = BeamMonitoring()
        HLayout.addWidget(self.height_slider)
        HLayout.addWidget(self.fig)
        stop_button = QPushButton("close")
        stop_button.setIcon(QIcon('graphics_Utils/icons/icon_close.png' ))
        stop_button.clicked.connect(self.close)  
        
        mainFrame = QFrame(self)
        mainFrame.setStyleSheet("QWidget { background-color: #eeeeec; }")
        mainFrame.setLineWidth(0.6)
        self.setCentralWidget(mainFrame)
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
        self.show()

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

        self.setCentralWidget(frame)
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
                   
if __name__ == '__main__':
    qapp = QtWidgets.QApplication(sys.argv)
    app = MainWindow()
    app.doseCalculatorWindow()
    qapp.exec_()
    
