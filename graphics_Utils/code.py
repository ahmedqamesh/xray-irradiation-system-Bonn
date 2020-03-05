import sys
from matplotlib.backends.qt_compat import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvas
from PyQt5.QtCore    import *
from PyQt5.QtGui     import *
from PyQt5.QtWidgets import *
import pyqtgraph as pg
import numpy as np

class Slider(QWidget):
    def __init__(self, minimum, maximum, parent=None):
        super(Slider, self).__init__(parent=parent)
        groupBox = QGroupBox("Tube Voltage [V]")
        
        self.verticalLayout = QVBoxLayout(self)
        self.label = QLabel(self)
        self.verticalLayout.addWidget(self.label)
        
        self.horizontalLayout = QHBoxLayout()
        spacerItem = QSpacerItem(0, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        
        self.horizontalLayout.addItem(spacerItem)
        self.slider = QSlider(self)
        
        self.slider.setOrientation(Qt.Vertical)
        
        self.horizontalLayout.addWidget(self.slider)
        
        spacerItem1 = QSpacerItem(0, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        
        self.horizontalLayout.addItem(spacerItem1)
        
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.resize(self.sizeHint())
        
        self.minimum = minimum
        self.maximum = maximum
        self.slider.valueChanged.connect(self.setLabelValue)
        self.x = None
        self.setLabelValue(self.slider.value())

    def setLabelValue(self, value):
        self.x = self.minimum + (float(value) / (self.slider.maximum() - self.slider.minimum())) * (
        self.maximum - self.minimum)
        self.label.setText("{0:.4g}".format(self.x))
        
class MainWindow(QMainWindow):
    def __init__(self,parent=None):
        super(MainWindow, self).__init__(parent)   
        
    def doseCalculatorWindow(self):
        self.setObjectName("Dose Calculator")
        self.setWindowTitle("Dose Calculator")
        self.resize(700, 700) #w*h

        plotframe = QFrame(self)
        plotframe.setStyleSheet("QWidget { background-color: #eeeeec; }")
        plotframe.setLineWidth(0.6)
        self.setCentralWidget(plotframe)
        gridLayout = QGridLayout()
        gridLayout.addWidget(self.createExampleGroup(0, 0,"Tube Voltage [V]"), 0, 0)
        gridLayout.addWidget(self.createExampleGroup(0, 1, "Tube Current [A]"), 0, 1)
        gridLayout.addWidget(self.createExampleGroup(0, 2,"Height [cm]"), 0, 2)
        gridLayout.addWidget(self.createExampleGroup(0, 3, "Beam radius [cm]"), 0, 3)
        gridLayout.addWidget(self.createExampleGroup(0, 4, "Dose Rate [Mrad/hr]"), 0, 4)
        plotframe.setLayout(gridLayout)
        self.show()

    def createExampleGroup(self, row, column, Groupname):
        numSlider = row*2+column if row==0 else row*2+column+row
        groupBox = QGroupBox(Groupname) 
        self.verticalLayout = QVBoxLayout()
        #Define label
        self.label = QLabel(self)
        self.label.setObjectName(Groupname)
        
        #Define Slider
        sliders = ["Tube Voltage [V]","Tube Current [A]","Height [cm]","Beam radius [cm]","Dose Rate [Mrad/hr]" ]
        #for i in np.arange(lenn(sliders)):
        slider= QSlider(Qt.Vertical)
        name = "slider{}".format(numSlider)
        setattr(self, name, self.label) 
        slider.setObjectName(name) 
        slider.setRange(1, 2000000)
        slider.setFocusPolicy(Qt.StrongFocus)
        slider.setTickPosition(QSlider.TicksBothSides)
        slider.setTickInterval(200000)
        slider.setSingleStep(1)
        slider.valueChanged[int].connect(self.changevalue)
        #slider.valueChanged[int].connect(self.valueSpinBox.setValue)
        #Define tickbox
        box = QCheckBox("Fix",self)
        box.stateChanged.connect(self.clickBox)

        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QHBoxLayout()
        spacerItem = QSpacerItem(0, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        
        self.horizontalLayout.addWidget(slider)
        
        spacerItem1 = QSpacerItem(0, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.addWidget(box)
        #self.resize(self.sizeHint())
        groupBox.setLayout(self.verticalLayout)
        return groupBox

    def changevalue(self, value):
        sender = self.sender()
        label  = getattr(self, sender.objectName())
        label.setText("{:>9,}".format(value))
        print(value)

    def clickBox(self, state):

        if state == QtCore.Qt.Checked:
            print('Checked')
        else:
            print('Unchecked')
            
if __name__ == '__main__':
    qapp = QtWidgets.QApplication(sys.argv)
    app = MainWindow()
    app.doseCalculatorWindow()
    qapp.exec_()
    
    