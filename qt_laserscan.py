import sys
import os
import random
import matplotlib
# Make sure that we are using QT5
matplotlib.use('Qt5Agg')
from PyQt5 import QtCore, QtWidgets

from numpy import arange
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np


progname = os.path.basename(sys.argv[0])

laserDistances = []
theta = []
sx = []
sy = []
axes1 = None
axes2 = None


class Window(FigureCanvas):

    def __init__(self, parent=None, width=20, height=3, dpi=100):
        global axes1
        global axes2

        fig = Figure(figsize=(width, height), dpi=dpi)
        #self.axes = fig.add_subplot(111)

        #self.axes.hold(False)
        axes1=fig.add_subplot(211)
        axes2=fig.add_subplot(212)
        #fig.clf()
        self.figure(laserDistances,theta,sx,sy, fig) 

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def figure(self,laserDistances,theta,sx,sy, fig):
        #fig.clf()
        pass

class LS(Window):
    global laserDistances
    global theta
    global sx
    global sy
    global fig
    global axes1
    global axes2

    def figure(self,laserDistances, theta, sx, sy,fig):
        #fig.clf()
        for i in range(len(laserDistances)):
                #fig.clf()
                axes1.plot(laserDistances[i],theta,'o')
                axes2.plot(sx[i],sy[i],'o')

class ApplicationWindow(QtWidgets.QMainWindow):

    global fig
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle('LaserScan')

        self.file_menu = QtWidgets.QMenu('&File', self)
        self.file_menu.addAction('&Quit', self.fileQuit,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        self.menuBar().addMenu(self.file_menu)

        self.main_widget = QtWidgets.QWidget(self)

        l = QtWidgets.QVBoxLayout(self.main_widget)
        sc = LS(self.main_widget, width=20, height=5, dpi=100)
        #fig.clf()
        l.addWidget(sc)

        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

    def fileQuit(self):
        self.close()

    def closeEvent(self, ce):
        self.fileQuit()

def run(laserDistance,angles,laserx,lasery):
    global laserDistances
    global theta
    global sx
    global sy

    laserDistances = laserDistance
    theta = angles
    sx = laserx
    sy = lasery
    qApp = QtWidgets.QApplication(sys.argv)

    passScan = Window()

    s = ApplicationWindow()
    s.setWindowTitle("%s" % progname)
    s.show()
    sys.exit(qApp.exec_())