import sys
import os
import random
import matplotlib
# Make sure that we are using QT5
matplotlib.use('Qt5Agg')
from PyQt5 import QtCore, QtWidgets

from numpy import arange, sin, pi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import wave
import numpy as np


progname = os.path.basename(sys.argv[0])

global laserDistances
global theta
global sx
global sy

class Window(FigureCanvas):
    global laserDistances
    global theta
    global sx
    global sy

    def __init__(self, parent=None, width=20, height=3, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        self.axes.hold(False)

        self.figure(laserDistances,theta,sx,sy) 
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def figure(self,laserDistances,theta,sx,sy):
        pass


class Scanform(Window):
    global laserDistances
    global theta
    global sx
    global sy

    def figure(self,laserDistances,theta,sx,sy):
        for i in range(len(laserDistancess)):
            self.plt.clf()
            self.ax1.add_subbplot(211)
            self.ax1.plot(theta,laserDistances[i],'o')
            self.ax2.add_subbplot(212
            self.ax2.plot(sx[i],sy[i],'o')
            self.plt.draw()


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle('Audio')

        self.file_menu = QtWidgets.QMenu('&File', self)
        self.file_menu.addAction('&Quit', self.fileQuit,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        self.menuBar().addMenu(self.file_menu)

        self.main_widget = QtWidgets.QWidget(self)

        l = QtWidgets.QVBoxLayout(self.main_widget)
        sc = Waveform(self.main_widget, width=20, height=3, dpi=100)
        l.addWidget(sc)

        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)
        
        btn = QPushButton('Button', self)
        btn.setToolTip('This is a <b>QPushButton</b> widget')
        btn.resize(btn.sizeHint())
        btn.move(50, 50)         
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
    #passScan.variable = scanFileName
    #passScan.figure1(scanFileName)

    sw = ApplicationWindow()

    sw.setWindowTitle("%s" % progname)
    sw.show()
    sys.exit(qApp.exec_())