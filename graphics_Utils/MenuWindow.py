import sys
import logging
loglevel = logging.getLogger('Analysis').getEffectiveLevel()
from analysis import logger
import matplotlib.pyplot as plt
from matplotlib.backends.qt_compat import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvas
from PyQt5.QtCore    import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from graphics_Utils import mainWindow , DataMonitoring , MenuWindow , childWindow , LogWindow
import numpy as np


class MenuBar(QWidget):  

    def __init__(self, parent=None):
        super(MenuBar, self).__init__(parent)
        self.mainwindow = QMainWindow()
        self.__diodesList = mainWindow.MainWindow().get_diodesList()
        self.__filtersList = mainWindow.MainWindow().get_filtersList()
        self.__depthList = mainWindow.MainWindow().get_depthList()
        self.__currentList = mainWindow.MainWindow().get_currentList()

    def _createMenu(self, mainwindow):
        menuBar = mainwindow.menuBar()
        menuBar.setNativeMenuBar(False)  # only for MacOS
        self._fileMenu(menuBar, mainwindow)
        self._viewMenu(menuBar, mainwindow)
        self._settingsMenu(menuBar, mainwindow)
        self._historyMenu(menuBar, mainwindow)
        self._helpMenu(menuBar, mainwindow)
        self.ui = childWindow.ChildWindow()
        
    def _createtoolbar(self, mainwindow):
        toolbar = mainwindow.addToolBar("tools")
        self._toolBar(toolbar, mainwindow)
        
    # 1. File menu
    def _fileMenu(self, menuBar, mainwindow):
               
        fileMenu = menuBar.addMenu('&File')

        new_action = QAction(QIcon('graphics_Utils/icons/icon_new.png'), '&New', mainwindow)
        new_action.setShortcut('Ctrl+N')
        new_action.setStatusTip('New start')
        new_action.triggered.connect(self.clicked)
        
        open_action = QAction(QIcon('graphics_Utils/icons/icon_open.png'), '&Open', mainwindow)
        open_action.setShortcut('Ctrl+O')
        open_action.setStatusTip('open session')  # show when move mouse to the icon
        open_action.triggered.connect(self.clicked)
        
        save_action = QAction(QIcon('graphics_Utils/icons/icon_save.png'), '&Save', mainwindow)
        save_action.setShortcut('Ctrl+S')
        save_action.setStatusTip('Save program')  # show when move mouse to the icon
        save_action.triggered.connect(self.clicked)
        
        close_action = QAction('&Close', mainwindow)
        close_action.setStatusTip('close session')  # show when move mouse to the icon
        close_action.triggered.connect(qApp.quit)
        
        exit_action = QAction(QIcon('graphics_Utils/icons/icon_exit.png'), '&Exit', mainwindow)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit program')
        exit_action.triggered.connect(qApp.quit)
        
        fileMenu.addAction(new_action)
        fileMenu.addAction(open_action)
        fileMenu.addAction(save_action)
        fileMenu.addAction(close_action)
        fileMenu.addSeparator()
        fileMenu.addAction(exit_action)
        
    # 2. View menu
    def _viewMenu(self, menuBar, mainwindow):
        viewMenu = menuBar.addMenu("&View")

        canSettings_action = QAction('&CAN Settings', mainwindow, checkable=True)
        canSettings_action.setStatusTip('CAN Settings')
        canSettings_action.setChecked(False)
        canSettings_action.triggered.connect(self.canSettingsChildWindow)
        
        canMessage_action = QAction('&CAN Message', mainwindow, checkable=True)
        canMessage_action.setStatusTip('CAN Message')
        canMessage_action.setChecked(False)
        canMessage_action.triggered.connect(self.toggleMenu)

        outWindow_action = QAction('&Output Window', mainwindow, checkable=True)
        outWindow_action.setStatusTip('Output Window')
        outWindow_action.setChecked(False)
        outWindow_action.triggered.connect(self.outputChildWindow)
                
        trend_action = QAction('&Data Trending', mainwindow, checkable=True)
        trend_action.setStatusTip('Data Trending')
        trend_action.setChecked(False)
        trend_action.triggered.connect(self.trendChildWindow)
        
        viewMenu.addAction(canSettings_action)
        viewMenu.addAction(canMessage_action)
        viewMenu.addAction(outWindow_action)
        viewMenu.addAction(trend_action)

     # 3. Test menu
    def _historyMenu(self, menuBar, mainwindow): 
        # history_menu = menuBar.addMenu("&History")
        test_menu = menuBar.addMenu("&Tests")
        
        angle__cone_action = QAction(QIcon('graphics_Utils/icons/icon_angle.png'), '&Opening Angle', mainwindow)        
        angle__cone_action.setStatusTip('Draw the cone shape of the opening angle')
        angle__cone_action.setChecked(True)
        angle__cone_action.triggered.connect(self.openingAngleConeChildMenu)
        test_menu.addAction(angle__cone_action) 

        angle_action = QAction(QIcon('graphics_Utils/icons/icon_angle.png'), '&BeamSpot radius vs height', mainwindow)        
        angle_action.setStatusTip('Get the estimated beam radius relative to the depth')
        angle_action.setChecked(True)
        angle_action.triggered.connect(self.openingAngleChildMenu)
        test_menu.addAction(angle_action) 
        
        diode_menu = test_menu.addMenu(QIcon('graphics_Utils/icons/icon_photodiode.png'), "&Photodiodes")

        diode_dosimetry_action = QAction(QIcon('graphics_Utils/icons/icon_linear.svg'), '&Photodiodes Dosimetry Calibration', mainwindow)        
        diode_dosimetry_action.setStatusTip('Photodiodes Dosimetry Calibration')
        diode_dosimetry_action.setChecked(True)
        diode_dosimetry_action.triggered.connect(self.photodiodesdosimetryChildMenu)
        
        diode_IV_action = QAction(QIcon('graphics_Utils/icons/icon_curve.png'), '&Photodiodes IV curve', mainwindow)        
        diode_IV_action.setStatusTip('Photodiodes IV curve')
        diode_IV_action.setChecked(True)
        diode_IV_action.triggered.connect(self.photodiodesIVChildMenu)
        
        diode_menu.addAction(diode_dosimetry_action) 
        diode_menu.addAction(diode_IV_action) 
        
        current_menu = test_menu.addMenu(QIcon('graphics_Utils/icons/icon_dose.png'), "&Absorbed dose vs. Tube Current")
        dose_action = []
        dose_filtersList = self.__filtersList
        for f in np.arange(0, len(dose_filtersList)):
            dose_action = QAction(dose_filtersList[f], mainwindow)        
            dose_action.setStatusTip('Get the calibration curves for each current'+dose_filtersList[f])
            dose_action.setChecked(True)
            dose_action.triggered.connect(self.doseChildMenu)
            current_menu.addAction(dose_action)
        
        voltage_menu = test_menu.addMenu(QIcon('graphics_Utils/icons/icon_dose.png'), "&Absorbed Dose vs. Tube Voltage")
        voltage_action = []
        voltage_filtersList = self.__filtersList
        for f in np.arange(0, len(voltage_filtersList)):
            voltage_action = QAction(voltage_filtersList[f], mainwindow)        
            voltage_action.setStatusTip('Get the calibration curves for each current' +voltage_filtersList[f])
            voltage_action.setChecked(True)
            voltage_action.triggered.connect(self.voltageChildMenu)
            voltage_menu.addAction(voltage_action)    
     
        depth_action = QAction(QIcon('graphics_Utils/icons/icon_inverse.png'), "&Absorbed dose vs. depth", mainwindow)        
        depth_action.setStatusTip('Get the dese rate at different depths')
        depth_action.setChecked(True)
        depth_action.triggered.connect(self.depthChildMenu)
        test_menu.addAction(depth_action) 


        spot_menu = test_menu.addMenu(QIcon('graphics_Utils/icons/icon_beamspot.png'), "&Beam Spot vs. depth")
        spot_action = []
        spot_filtersList = self.__filtersList
        for f in np.arange(0, len(spot_filtersList)):
            spot_action = QAction(dose_filtersList[f], mainwindow)        
            spot_action.setStatusTip('Get the beam spot at different depths' + dose_filtersList[f])
            spot_action.setChecked(True)
            spot_action.triggered.connect(self.beamspotChildMenu)
            spot_menu.addAction(spot_action)
        
     # 3. Settings menu
    def _settingsMenu(self, menuBar, mainwindow): 
        settings_menu = menuBar.addMenu("&Settings")
        settings_action = QAction(QIcon('graphics_Utils/icons/icon_settings.png'), '&Settings', mainwindow)        
        settings_action.setStatusTip('settings action')
        settings_action.setChecked(True)
        settings_action.triggered.connect(self.openWindow)
        settings_menu.addAction(settings_action)             
        
    # 4. Help menu
    def _helpMenu(self, menuBar, mainwindow):
        helpmenu = menuBar.addMenu("&Help")
 
        contents_action = QAction('&Contents', mainwindow)
        contents_action.setStatusTip("Contents")
        contents_action.triggered.connect(self.clicked)
              
        about_action = QAction('&About', mainwindow)
        about_action.setStatusTip("About")
        about_action.triggered.connect(self.about)
        
        helpmenu.addAction(contents_action)
        helpmenu.addAction(about_action)
    
    # make a toolbar         
    def _toolBar(self, toolbar, mainwindow):
        
        new_action = QAction(QIcon('graphics_Utils/icons/icon_new.png'), '&New', mainwindow)
        new_action.setShortcut('Ctrl+N')
        new_action.setStatusTip('New start')
        new_action.triggered.connect(self.clicked)
        
        open_action = QAction(QIcon('graphics_Utils/icons/icon_open.png'), '&Open', mainwindow)
        open_action.setShortcut('Ctrl+O')
        open_action.setStatusTip('open session')  # show when move mouse to the icon
        open_action.triggered.connect(self.clicked)
        
        save_action = QAction(QIcon('graphics_Utils/icons/icon_save.png'), '&Save', mainwindow)
        save_action.setShortcut('Ctrl+S')
        save_action.setStatusTip('Save program')  # show when move mouse to the icon
        save_action.triggered.connect(self.clicked)

        start_action = QAction(QIcon('graphics_Utils/icons/icon_start.png'), '&Start', mainwindow)
        start_action.setStatusTip('Start session')  # show when move mouse to the icon
        start_action.triggered.connect(self.clicked)

        pause_action = QAction(QIcon('graphics_Utils/icons/icon_pause.png'), '&Pause', mainwindow)
        pause_action.setStatusTip('Pause program')  # show when move mouse to the icon
        pause_action.triggered.connect(self.clicked)
                
        stop_action = QAction(QIcon('graphics_Utils/icons/icon_stop.png'), '&Stop', mainwindow)
        stop_action.setStatusTip('Stop program')  # show when move mouse to the icon
        stop_action.triggered.connect(self.clicked)
   
        toolbar.addAction(new_action)
        toolbar.addAction(open_action)
        toolbar.addAction(save_action)
        toolbar.addSeparator()
        toolbar.addAction(start_action)
        toolbar.addAction(pause_action)
        toolbar.addAction(stop_action)
                     
    def _createStatusBar(self, mainwindow):
        status = QStatusBar()
        status.showMessage("Ready")
        mainwindow.setStatusBar(status)

    # Functions to run
    def toggleMenu(self, state):
        if state:
            self.openWindow()
        else:
            pass

    def openingAngleConeChildMenu(self):
        self.ui.ChildMenu(ChildWindow=self.mainwindow ,
                                      firstitems=self.__filtersList,
                                      test_name="Opening Angle Test",
                                      dir="opening_angle/",
                                      name_prefix="opening_angle_",
                                      plot_prefix="opening_angle_cone")
        self.mainwindow.show()  
                 
    def openingAngleChildMenu(self):
        self.ui.ChildMenu(ChildWindow=self.mainwindow ,
                                      firstitems=self.__filtersList,
                                      test_name="BeamSpot radius vs height",
                                      dir="opening_angle/",
                                      name_prefix="opening_angle_",
                                      plot_prefix="opening_angle")
        self.mainwindow.show()  
    
    def depthChildMenu(self):
        self.ui.ChildMenu(ChildWindow=self.mainwindow ,
                                      firstitems=self.__filtersList,
                                      test_name="dose rate vs depth",
                                      dir="dose_depth/",
                                      name_prefix="dose_depth_",
                                      plot_prefix="dose_depth")
        self.mainwindow.show()          
        
    def beamspotChildMenu(self, state):
        action = self.sender()
        text = action.text()
        self.ui.ChildMenu(ChildWindow=self.mainwindow ,
                                      csv=None,
                                      firstitems=self.__depthList,
                                      test_name="beam spot vs depth",
                                      dir="beamspot/"+text+"/",
                                      name_prefix="beamspot_",
                                      plot_prefix="beamspot")
        self.mainwindow.show()   
            
    def photodiodesdosimetryChildMenu(self):
        self.ui.ChildMenu(ChildWindow=self.mainwindow ,
                                      firstitems=self.__diodesList,
                                      test_name="Photodiodes Dosimetry Calibration",
                                      dir="diode_calibration/",
                                      name_prefix="diode_calibration_",
                                      plot_prefix="diode_calibration")
        self.mainwindow.show()        

    def photodiodesIVChildMenu(self):
        self.ui.ChildMenu(ChildWindow=self.mainwindow ,
                                      firstitems=self.__diodesList,
                                      test_name="Photodiodes IV Curve",
                                      dir="diode_calibration/",
                                      name_prefix="IV_test_",
                                      plot_prefix="IV_test")
        self.mainwindow.show()       
           
    def doseChildMenu(self, state):
        action = self.sender()
        text = action.text()
        self.ui.ChildMenu(ChildWindow=self.mainwindow ,
                                      firstitems=self.__depthList,
                                      test_name="Absorbed Dose vs. Tube Current",
                                      dir="dose_current/" + text + "/",
                                      name_prefix="dose_current_",
                                      plot_prefix="dose_current")
        self.mainwindow.show()     
            
    def voltageChildMenu(self, state):
        action = self.sender()
        text = action.text()
        self.ui.ChildMenu(ChildWindow=self.mainwindow ,
                                      firstitems=self.__depthList,
                                      test_name="Absorbed Dose vs. Tube Voltage",
                                      dir="dose_voltage/" + text + "/",
                                      name_prefix="dose_voltage_",
                                      plot_prefix="dose_voltage")
        self.mainwindow.show()     
    
    def outputChildWindow(self, state):
        if state:
            self.ui.outputChildWindow(self.mainwindow)
            self.mainwindow.show()
        else:
           self.mainwindow.close()
    
    def trendChildWindow(self, state):
        if state:
            self.ui.trendChildWindow(self.mainwindow)
            self.mainwindow.show()
        else:
           self.mainwindow.close()
            
    def canSettingsChildWindow(self, state):
        if state:
            self.ui.canSettingsChildWindow(self.mainwindow)
            self.mainwindow.show()
        else:
           self.mainwindow.close()
           
    def about(self):
        text="text"
        QMessageBox.about(self, "About",text)

    def openWindow(self):
        self.ui.settingChannel(self.mainwindow)
        self.mainwindow.show()
        
    def clicked(self, q):
        print("is clicked")

        
if __name__ == "__main__":
    pass
                
