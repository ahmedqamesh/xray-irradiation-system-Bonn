import sys
from matplotlib.backends.qt_compat import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvas
from PyQt5.QtCore    import *
from PyQt5.QtGui     import *
from PyQt5.QtWidgets import *
import pyqtgraph as pg
import numpy as np
import os
from analysis import fitEquations as f
from analysis import analysis_utils
rootdir = os.path.dirname(os.path.abspath(__file__))

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
        

    def doseCalculatorWindow(self):
        self.setObjectName("Dose Calculator")
        self.setWindowTitle("Dose Calculator")
        self.resize(1200, 700)  # w*h
        
        self.voltage_slider , voltage_Group= self.createSliderGroup(i=0, limit = self.__max_voltage)
        self.current_slider , current_Group = self.createSliderGroup(i=1, limit =self.__max_current)
        self.height_slider , height_Group = self.createSliderGroup(i=2, limit = self.__max_height)
        self.radius_slider , radius_Group = self.createSliderGroup(i=3, limit = self.__max_radius)
        self.dose_slider , dose_Group = self.createSliderGroup(i=4, limit =  self.__max_dose)
        
        VBox = QVBoxLayout()
        firstHBoxLayout = QHBoxLayout()
        firstLabel = QLabel("Test Type: ")
        firstLabel.setText("                            Test Type: ")
        
        firstComboBox = QComboBox()
        for item in self.__filtersList: firstComboBox.addItem(item)
        firstComboBox.activated[str].connect(self.set_filterItem)
        firstHBoxLayout.addWidget(firstLabel)
        firstHBoxLayout.addWidget(firstComboBox)
        self.win = pg.GraphicsWindow(title="Basic plotting examples")
        self.p6 = self.win.addPlot(title="My Plot")
        self.curve = self.p6.plot(pen='r')
        self.update_plot()
        
        VBox.addLayout(firstHBoxLayout)
        VBox.addWidget(self.win)

        mainFrame = QFrame(self)
        mainFrame.setStyleSheet("QWidget { background-color: #eeeeec; }")
        mainFrame.setLineWidth(0.6)
        self.setCentralWidget(mainFrame)
        mainLayout = QGridLayout()

        self.voltage_slider.valueChanged.connect(self.changevalue)
        self.voltage_slider.valueChanged.connect(self.update_plot)
        
        self.current_slider.valueChanged.connect(self.changevalue)
        self.current_slider.valueChanged.connect(self.update_plot)
        
        self.height_slider.valueChanged.connect(self.changevalue)
        self.height_slider.valueChanged.connect(self.update_plot)
        
        self.radius_slider.valueChanged.connect(self.changevalue)
        self.radius_slider.valueChanged.connect(self.update_plot)

        self.dose_slider.valueChanged.connect(self.changevalue)
        self.dose_slider.valueChanged.connect(self.update_plot)
                
        mainLayout.addWidget(voltage_Group, 0, 0)
        mainLayout.addWidget(current_Group, 0, 1)
        mainLayout.addWidget(height_Group, 0, 2)
        mainLayout.addWidget(radius_Group, 0, 3)
        mainLayout.addWidget(dose_Group, 0, 4)
        mainLayout.addLayout(VBox,0,5)
        mainFrame.setLayout(mainLayout)
        self.show()

    def createSliderGroup(self, i=0, limit=20, range = [1,2,3]):
        sliders = ["Tube voltage", "Tube current", "Height", "Beam radius", "Dose rate" ]
        groupBox= QGroupBox(sliders[i]) 
        frame = QFrame(self)
        frame.setStyleSheet("QWidget { background-color: #eeeeec; }")
        frame.setLineWidth(0.9)
        self.verticalLayout = QVBoxLayout()
        # Define label
        self.label = QLabel(self)
        # Define Slider
        slider = QSlider(Qt.Vertical)
        name = "{}".format(i)
        setattr(self, name, self.label) 
        slider.setObjectName(name) 
        slider.setRange(0, limit)
        slider.setFocusPolicy(Qt.StrongFocus)
        slider.setTickPosition(QSlider.TicksBothSides)

        # Define tickbox
        box = QCheckBox("Fix", self)
        box.stateChanged.connect(self.clickBox)

        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QHBoxLayout()
        spacerItem = QSpacerItem(0, 10, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        
        self.horizontalLayout.addWidget(slider)
        
        spacerItem1 = QSpacerItem(0, 10, QSizePolicy.Expanding, QSizePolicy.Minimum)
        
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.addWidget(box)
        
        self.setCentralWidget(frame)
        frame.setLayout(self.verticalLayout)
        groupBox.setLayout(self.verticalLayout)
        return slider , groupBox

    def changevalue(self, value):
        sliders_units = [" [kV]", " [mA]", " [cm]", " [cm]", " [Mrad/hr]"]
        sender = self.sender()
        i = int(sender.objectName())
        label = getattr(self, sender.objectName())
        label.setText("{:>10,}".format(value)+sliders_units[i])
        if i == 0:
            dV = f.dose_voltage(voltage = value, filter = "without", depth ="8cm")
            self.set_dose(dV)  
        if i == 1:
            dC = f.dose_current(current = value, filter = "without", depth ="3cm",voltage = "40kV")
            self.set_dose(dC)
        if i == 2:
            dD = f.dose_depth(depth = value, filter = "without")
            r = f.opening_angle(depth = value)
            print(dD, r)
        if i == 3:
            height = f.opening_angle(radius = value)
            print(height)     
        if i == 4:
            current = f.dose_current(dose = value, filter = "without", depth ="3cm", voltage = "40kV")
            self.set_current(current)
        
    def clickBox(self, state):
        if state == QtCore.Qt.Checked:
            print('Checked')
        else:
            print('Unchecked')
    
    def update_plot(self):
        a = self.voltage_slider.value()
        b = self.current_slider.value()
        c = self.height_slider.value()
        d = self.radius_slider.value()
        x = np.linspace(0, 10, 100)
        data = a + np.cos(x + c * np.pi / 180) * np.exp(-b * x) * d
        self.curve.setData(data)
    
    def set_filterItem(self, x): 
        self.__filterItem = x 

    def set_voltage(self,x):
        self.__voltage = x
        self.voltage_slider.setValue(x)
        
    def set_current(self,x):
        self.__current = x
        self.current_slider.setValue(x)

    def set_dose(self,x):
        self.__dose = x
        #self.dose_slider.setValue(x)
        
    def set_height(self,x):
        self.__height = x
    
    def set_radius(self,x):
        self.__radius = x 

    def get_filterItem(self): 
        return self.__filterItem
        
    def get_voltage(self):
        return self.__voltage 

    def get_current(self):
        return self.__current 

    def get_dose(self):
        return self.__dose  
    
    def get_height(self):
        return self.__height
     
    def get_radius(self):
        return self.__radius
                   
if __name__ == '__main__':
    qapp = QtWidgets.QApplication(sys.argv)
    app = MainWindow()
    app.doseCalculatorWindow()
    qapp.exec_()
    
