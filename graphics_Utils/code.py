import sys
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
        
class Window(QWidget):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.setWindowTitle("PyQt5 Sliders")
        self.resize(425, 392)
        self.doseCalculatorWindow(ChildWindow=self)        
        
    def doseCalculatorWindow(self, ChildWindow):
        ChildWindow.setObjectName("Dose Calculator")
        ChildWindow.setWindowTitle("Output Window")
        ChildWindow.resize(700, 300) #w*h
        logframe = QFrame(self)
        logframe.setLineWidth(0.6)
        #ChildWindow.setCentralWidget(logframe)
        self.WindowGroupBox = QGroupBox("")
        gridLayout = QGridLayout()
        scrollWidget = QWidget()
        scrollWidget.setLayout(gridLayout)
        
        scrollArea = QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollArea.setWidget(scrollWidget)   
        self.WindowGroupBox.setLayout(gridLayout)
        logframe.setLayout(gridLayout)
        self.w1 = Slider(-10, 10)
        gridLayout.addWidget(self.w1,0,0)
        self.w2 = Slider(-1, 1)
        gridLayout.addWidget(self.w2,0,1)

        self.w3 = Slider(-10, 10)
        gridLayout.addWidget(self.w3,0,2)

        self.w4 = Slider(-10, 10)
        gridLayout.addWidget(self.w4,0,3)
        row = 0
       # gridLayout.addWidget(self.createExampleGroup(row, 0,"Tube Voltage [V]"), row, 0)
       # gridLayout.addWidget(self.createExampleGroup(row, 1, "Tube Current [A]"), row, 1)
       # gridLayout.addWidget(self.createExampleGroup(row, 2,"Height [cm]"), row, 2)
       # gridLayout.addWidget(self.createExampleGroup(row, 3, "Beam radius [cm]"), row, 3)
       # gridLayout.addWidget(self.createExampleGroup(row, 4, "Dose Rate [Mrad/hr]"), row, 4)
        

    def createExampleGroup(self, row, column, Groupname):
        numSlider = row*2+column if row==0 else row*2+column+row
        groupBox = QGroupBox(Groupname)
        self.label = QLabel()  
        #self.label.setObjectName("label{}".format(numSlider))

        slider = QSlider(Qt.Vertical)
        name = "slider{}".format(numSlider)
        slider.setObjectName(name) 
        setattr(self, name, self.label) 
        slider.setRange(1, 2000000)
        slider.setFocusPolicy(Qt.StrongFocus)
        slider.setTickPosition(QSlider.TicksBothSides)
        slider.setTickInterval(200000)
        slider.setSingleStep(0.1)
        slider.valueChanged[int].connect(self.changevalue)

        vbox = QVBoxLayout()
        vbox.addWidget(self.label)
        vbox.addWidget(slider)
        vbox.addStretch(1)
        groupBox.setLayout(vbox)
        return groupBox

    def changevalue(self, value):
        sender = self.sender()
        label  = getattr(self, sender.objectName())
        label.setText("{:>9,}".format(value))
        print(value)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    clock = Window()
    clock.show()
    sys.exit(app.exec_())