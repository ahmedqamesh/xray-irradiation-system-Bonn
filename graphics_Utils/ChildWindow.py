from matplotlib.backends.qt_compat import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvas
from PyQt5.QtCore import QDateTime, Qt, QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from graphics_Utils import DataMonitoring , MapMonitoring , utils , ChildWindow
class Ui_ChildWindow(object):  
    def setupUi(self, ChildWindow):
        ChildWindow.setObjectName("ChildWindow")
        #ChildWindow.resize(568, 109) 
        ChildWindow.setGeometry(300, 300, 300, 200)
        centralwidget = QWidget(ChildWindow)
        centralwidget.setObjectName("centralwidget")
        
        ChildWindow.setCentralWidget(centralwidget)        
        childLayout = QVBoxLayout(centralwidget)
        #childLayout.addStretch(1)
        #comboBoxLayout = QHBoxLayout()
        listwidgetLayout = QHBoxLayout()
        #comboBox for channel
        #chlabel = QLabel("Channel", ChildWindow)
        #chlabel.setText("Channel")
#         chlabel.move(30, 50)
#         chComboBox = QComboBox(ChildWindow)
#         chComboBox.addItem("Ch1")
#         chComboBox.addItem("Ch2")
#         chComboBox.addItem("Ch3")
#         chComboBox.move(50, 100)
#         chComboBox.activated[str].connect(self.setaddress)    
#         listwidgetLayout.addWidget(chComboBox)
        chlistwidget = QListWidget()
        chlistwidget.insertItem(0, "Ch1")
        chlistwidget.insertItem(1, "Ch2")
        chlistwidget.insertItem(2, "Ch3")
        chlistwidget.clicked.connect(self.setaddress(ChildWindow))
        chlistwidget.clicked.connect(self.setaddress(ChildWindow))
        listwidgetLayout.addWidget(chlistwidget)
                  
         #comboBox for coordinates
        #dimlabel = QLabel("Coordinate", ChildWindow)
        #dimlabel.setText("Coordinate")
        
        #dimlabel.move(110, 50)
        #dimComboBox = QComboBox(ChildWindow)
        #dimComboBox.addItem("x")
        #dimComboBox.addItem("y")
        #dimComboBox.addItem("z")
        #dimComboBox.move(100, 200)
        #dimComboBox.activated[str].connect(self.setaddress)
        dimlistwidget = QListWidget()
        dimlistwidget.insertItem(0, "x")
        dimlistwidget.insertItem(1, "y")
        dimlistwidget.insertItem(2, "z")
        dimlistwidget.clicked.connect(self.setaddress)
        
        listwidgetLayout.addWidget(dimlistwidget)
        
        Set_button = QPushButton("Set")
        listwidgetLayout.addWidget(Set_button)
        Set_button.clicked.connect(self.setaddress) 
        
        
        childLayout.addLayout(listwidgetLayout)
        
        ok_button = QPushButton("Ok")
        #ok_button.clicked.connect(self.onNext)
        
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(ChildWindow.close)
        
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(ok_button)
        buttonLayout.addWidget(cancel_button)      
        childLayout.addLayout(buttonLayout)
                
        #ChildWindow.setLayout(buttonLayout)

        self.statusbar = QtWidgets.QStatusBar(ChildWindow)
        self.statusbar.setObjectName("statusbar")
        ChildWindow.setStatusBar(self.statusbar)
        ChildWindow.setWindowTitle("Motor stage settings")
        QtCore.QMetaObject.connectSlotsByName(ChildWindow)
    
    def setaddress(self, text):
        #print(text)
        #ChildWindow.lbl.setText(text)
        #ChildWindow.lbl.adjustSize()  
        item = dimlistwidget.currentItem()
        print(item.text())
   
    
    
if __name__ == "__main__":
    pass

