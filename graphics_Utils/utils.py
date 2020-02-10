import sys
import logging
loglevel = logging.getLogger('Analysis').getEffectiveLevel()
from analysis import logger
import matplotlib.pyplot as plt
from PyQt5.QtCore import QDateTime, Qt, QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *

def _createMenu(self):
    menuBar = self.menuBar()
    menuBar.setNativeMenuBar(False) #only for MacOS

    file_menu = menuBar.addMenu('&File')
    
    exit_action = QAction(QIcon('graphics_Utils/icons/icon_exit.png'), '&Exit', self)
    exit_action.setShortcut('Ctrl+Q')
    exit_action.setStatusTip('Exit program')
    exit_action.triggered.connect(qApp.quit)
    
    save_action = QAction(QIcon('graphics_Utils/icons/icon_save.png'), '&Save', self)
    save_action.setShortcut('Ctrl+S')
    save_action.setStatusTip('Save program') # show when move mouse to the icon

    file_menu.addAction(save_action)
    file_menu.addAction(exit_action)
    
    menu = menuBar.addMenu("&Menu")
    menu.addAction('&Exit',fileQuit)
    
    #Settings menu
    settings_menu = menuBar.addMenu("&settings")
    
    click_action = QAction(QIcon('graphics_Utils/icons/icon_settings.png'), '&Motorstage Settings', self)        
    click_action.setShortcut('Ctrl+N')
    click_action.setStatusTip('settings action')
    click_action.triggered.connect(clickMethod)
    
    settings_menu.addAction(click_action)
    
    # Help menu
    help_menu = menuBar.addMenu("&Help")
    help_menu.addAction('&About', about)

def _createToolBar(self):
    self.toolbar = self.addToolBar("tools")
    exit_action = QAction(QIcon('graphics_Utils/icons/icon_exit.png'), '&Exit', self)
    exit_action.setShortcut('Ctrl+Q')
    exit_action.setStatusTip('Exit program')  # show when move mouse to the icon
    exit_action.triggered.connect(qApp.quit)
    self.toolbar.addAction(exit_action)
    
    
def _createStatusBar(self):
    status = QStatusBar()
    status.showMessage("I'm the Status Bar")
    self.setStatusBar(status)
    
def fileQuit(self):
    self.close()

def closeEvent(self, ce):
    self.fileQuit()

def about():
    QMessageBox.about( "About",
    """embedding_in_qt5.py example
    Copyright 2015 BoxControL
    This program is a simple example of a Qt5 application embedding matplotlib
    canvases. It is base on example from matplolib documentation, and initially was
    developed from Florent Rougon and Darren Dale.
    http://matplotlib.org/examples/user_interfaces/embedding_in_qt4.html
    It may be used and modified with no restriction; raw copies as well as
    modified versions may be distributed without limitation.""")
    

def clickMethod(self):
    self.window = ChildWindow()
    self.window.switch_window.connect(self.show_window_two)
    self.window.show()
    
    childLayout = QVBoxLayout()
    btnNext = QPushButton("Next")
    #btnNext.clicked.connect(self.onNext)
    btnPrevious = QPushButton("Previous")
    #btnPrevious.clicked.connect(self.onPrevious)
    
    btnLayout = QHBoxLayout()
    btnLayout.addWidget(btnPrevious)
    btnLayout.addWidget(btnNext)               
    childLayout.addLayout(btnLayout)
    self.setLayout(childLayout)
    #lay.show()
    
def _setup_style(self):
    self.setWindowTitle(self.app_name)
    #self.setGeometry(300, 300, 800, 400)
    self.resize(800, 600)


            