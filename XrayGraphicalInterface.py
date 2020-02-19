from __future__ import annotations
import sys
from matplotlib.backends.qt_compat import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvas
from PyQt5.QtCore    import *
from PyQt5.QtGui     import *
from PyQt5.QtWidgets import *
from pathlib import Path
import matplotlib as mpl
import numpy as np
from matplotlib.figure import Figure
from graphics_Utils import mainWindow

if __name__ == "__main__":
    qapp = QtWidgets.QApplication(sys.argv)
    app = mainWindow.MainWindow()
    app.Ui_ApplicationWindow()
    qapp.exec_()