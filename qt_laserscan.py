import sys
import os
import random
import matplotlib
import matplotlib.pyplot as plt
import time
import math
#rom scipy import spatial

# Make sure that we are using QT5
matplotlib.use('Qt5Agg')
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import Qt, QUrl, pyqtSignal, QFile, QIODevice
from PyQt5.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QPushButton,
QSizePolicy, QVBoxLayout, QWidget)
from PyQt5.QtGui import * #QPainter, QColor, QFont


from numpy import arange
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

progname = os.path.basename(sys.argv[0])

laserDistances = []
theta = []
sx = []
sy = []
fig = None
axes1 = None
axes2 = None
smth = None
cnt= 0
timer = None
line1 = None
line2 = None

c1 = []
c2 = []
firstclick = False
secondclick = False
oriz = []

class Window(FigureCanvas):

    def __init__(self, parent=None, width=20, height=6, dpi=100):
        global axes1,axes2
        global fig
        global smth,cnt

        smth = self

        fig = Figure(figsize=(width, height), dpi=dpi)

        axes1=fig.add_subplot(211)

        axes2=fig.add_subplot(212)


        self.figure(laserDistances,theta,sx,sy, fig) 

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def figure(self,laserDistances,theta,sx,sy, fig):
        pass

class LS(Window):
    global laserDistances
    global theta
    global sx,sy
    global fig
    global axes1,axes2
    global smth, cnt

    def figure(self,laserDistances, theta, sx, sy,fig):
        '''
        if(cnt<len(laserDistances)):
            axes1.clear()
            axes2.clear()
            axes1.plot(laserDistances[cnt],theta,'o')
            #axes1.hold()
            axes2.plot(sx[cnt],sy[cnt],'o')
            #axes2.hold()
            #smth.draw()
            cnt += 1
        '''


class ApplicationWindow(QtWidgets.QMainWindow):
    global laserDistances
    global theta
    global sx
    global sy
    global fig
    global axes1
    global axes2
    global smth, cnt

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        '''
        self.file_menu = QtWidgets.QMenu('&File', self)
        self.file_menu.addAction('&Quit', self.fileQuit,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        self.menuBar().addMenu(self.file_menu)
        '''

        self.main_widget = QtWidgets.QWidget(self)

        #l = QtWidgets.QVBoxLayout(self.main_widget)
        sc = LS(self.main_widget, width=20, height=6, dpi=100)
        #l.addWidget(sc)

        #Define buttons
        scanLayout = QHBoxLayout()
        scanLayout.addWidget(sc)

        playButton = QPushButton("Play")
        pauseButton = QPushButton("Pause")
        stopButton = QPushButton("Stop")
        annotationButton = QPushButton("Annotation")
        prevFrameButton = QPushButton("Previous")
        nextFrameButton = QPushButton("Next")

        classes = QComboBox()
        classes.addItem('Selections')
        classes.addItem('S1')
        classes.addItem('S2')
        classes.addItem('New')

        buttonLayout = QVBoxLayout()
        buttonLayout.addWidget(playButton)
        buttonLayout.addStretch(1)
        buttonLayout.addWidget(pauseButton)
        buttonLayout.addStretch(1)
        buttonLayout.addWidget(prevFrameButton)
        #buttonLayout.addStretch(1)
        buttonLayout.addWidget(nextFrameButton)
        buttonLayout.addStretch(1)
        buttonLayout.addWidget(stopButton)
        buttonLayout.addStretch(1)
        buttonLayout.addWidget(annotationButton)
        buttonLayout.setAlignment(Qt.AlignTop)


        classLayout = QVBoxLayout()
        classLayout.addWidget(classes)
        classLayout.setAlignment(Qt.AlignTop)

        layout = QHBoxLayout(self.main_widget)
        layout.addLayout(scanLayout)
        layout.addLayout(buttonLayout)
        layout.addLayout(classLayout)

        #Define Connections
        playButton.clicked.connect(self.bplay)
        pauseButton.clicked.connect(self.bpause)
        prevFrameButton.clicked.connect(self.bprevious)
        nextFrameButton.clicked.connect(self.bnext)
        stopButton.clicked.connect(self.bstop)
        annotationButton.clicked.connect(self.bannotation)

        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

    def bplay(self):
        ptime()

    def bpause(self):
        global timer
        timer.stop()

    def bprevious(self):
        global cnt
        global theta,laserDistances,sx,sy
        if (cnt>0):
            cnt = cnt-1
            axes1.clear()
            axes2.clear()
            axes1.plot(theta,laserDistances[cnt],'o')
            axes2.plot(sx[cnt],sy[cnt],'o')
            smth.draw()
        else:
            axes1.clear()
            axes2.clear()
            smth.draw()

    def bnext(self):
        global cnt,smth
        global theta,laserDistances,sx,sy
        if (cnt<len(laserDistances)):
            cnt = cnt+1
            print cnt
            axes1.clear()
            axes2.clear()
            axes1.plot(theta,laserDistances[cnt],'o')
            axes2.plot(sx[cnt],sy[cnt],'o')
            smth.draw()
        else:
            axes1.clear()
            axes2.clear()
            smth.draw()


    def bstop(self):
        global cnt,timer
        global axes1,axes2
        global smth
        cnt = 0
        timer.stop()
        axes1.clear()
        axes2.clear()
        smth.draw()

    def bannotation(self):
        fig.canvas.mpl_connect('button_press_event', self.onCLick)

    def onCLick(self,event):
        global c1,c2,c
        global firstclick,secondclick
        global axes1
        x = event.x
        y = event.y
        if event.button == 1:
            if firstclick == False:
                if event.inaxes is not None:
                    c1 = [event.xdata, event.ydata]
                    firstclick = True
            elif secondclick == False:
                if event.inaxes is not None:
                    c2 = [event.xdata, event.ydata]
                    secondclick = True
                    icon()
                    firstclick = False
                    secondclick = False


    def fileQuit(self):
        self.close()

    def closeEvent(self, ce):
        self.fileQuit()

def ptime():
    global timer

    timer.timeout.connect(icon)
    timer.start(0.0000976562732)


def run(laserDistance,angles,laserx,lasery):
    global laserDistances
    global theta
    global sx,sy
    global smth,cnt,timer

    timer = QtCore.QTimer(None)
    laserDistances = laserDistance
    theta = angles
    sx = laserx
    sy = lasery
    qApp = QtWidgets.QApplication(sys.argv)

    passScan = Window()

    s = ApplicationWindow()
    s.setWindowTitle('Laser Scan')
    #s.setWindowTitle("%s" % progname)
    s.show()
    sys.exit(qApp.exec_())


def icon():
    global laserDistances
    global theta
    global sx
    global sy
    global fig
    global axes1
    global axes2
    global smth, cnt
    global oriz,ka9et

    #for i in range(len(laserDistances)):
    if(cnt<len(laserDistances)):
        axes1.clear()
        axes2.clear()
        axes1.plot(theta,laserDistances[cnt],'o')
        axes2.plot(sx[cnt],sy[cnt],'o')
        axes2.axis('equal')
        if len(c1)>0:
            axes2.plot([c1[0],c2[0]],[c1[1],c1[1]],'r')
            axes2.plot([c2[0],c2[0]],[c1[1],c2[1]],'r')
            axes2.plot([c2[0],c1[0]],[c2[1],c2[1]],'r')
            axes2.plot([c1[0],c1[0]],[c2[1],c1[1]],'r')
            pos = cnt
            i=c1[0]
            while (i<c2[0]):
                #oriz.append(sx[i])
                #oriz = [sx[i],sy[i]]
                #distance,index = spatial.KDTree(sy).query(c1)
                if ((sy[pos]<c1[1]) and (sy[pos]>c2[1])):
                    axes2.plot(sx[index],sy[index],'r')
                    smth.draw()
                i=i+1
                pos=pos+1
        smth.draw()
        cnt += 1