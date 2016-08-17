import sys
import os
import random
import matplotlib
import matplotlib.pyplot as plt
import time
import math
import csv
import ast
#rom scipy import spatial

# Make sure that we are using QT5
matplotlib.use('Qt5Agg')
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import Qt, QUrl, pyqtSignal, QFile, QIODevice
from PyQt5.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QPushButton,
QSizePolicy, QVBoxLayout, QWidget)

from numpy import arange
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

progname = os.path.basename(sys.argv[0])

#Arxikopoihsh global timwn
#Pinakes apo rosbag
sx = []
sy = []
#Arxikopoihsh metritwn
cnt = 0
timer = None
#Arxikopoihsh grafikwn parastasewn
ax = None
fig = None
fw = None
scan_widget = None
objx = []
objy = []
s1 = []
s2 = []
#Arxikopoihsh annotation
annotating = False
firstclick = False
secondclick = False
thirdclick = False
c1 = []
c2 = []
colorName = None
txt = None
annot = []
curr_ptr = []
data = None

class Window(FigureCanvas):

    def __init__(self, parent=None, width=10, height=3, dpi=100):

        global fw,fig,ax,bag_file,data

        fw = self

        fig = Figure(figsize=(width, height), dpi=dpi)

        #axes1=fig.add_subplot(211)
        #axes2=fig.add_subplot(212)
        ax = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def icon(self):
        pass

class LS(Window):

    def ptime(self):

        global timer

        timer.timeout.connect(self.icon)
        timer.start(0.0000976562732)

    def icon(self):

        global cnt,ax,annot, fw, colorName,timer, samex, samey, listofpointsx, listofpointsy,annotID,bbstart,bbend

        if(cnt<len(annot)):
            ax.clear()
            ax.axis('equal')
            ax.plot(annot[cnt].samex,annot[cnt].samey,'bo')
            if not annot[cnt].listofpointsx == []:
                ax.plot(annot[cnt].listofpointsx,annot[cnt].listofpointsy,'ro')
            fw.draw()
            cnt += 1
        if (cnt == len(annot)):
            cnt=0
            timer.stop()
            ax.clear()
            fw.draw()

    def rect(self):

        global cnt, ax, c1, c2, fw, cnt, firstclick, secondclick

        if(cnt<len(annot)):
            ax.axis('equal')
            #if len(c1)>0:
            if secondclick:
                ax.plot([c1[0],c2[0]],[c1[1],c1[1]],'r')
                ax.plot([c2[0],c2[0]],[c1[1],c2[1]],'r')
                ax.plot([c2[0],c1[0]],[c2[1],c2[1]],'r')
                ax.plot([c1[0],c1[0]],[c2[1],c1[1]],'r')
            fw.draw()


    def training(self):

        global colorName,sx,sy,c1,c2,cnt,objx,objy,s1,s2,fw, ax, curr_ptr,annot,txt

        ax.clear()
        for i in range(len(annot[cnt].samex)):
            if ((annot[cnt].samex[i] >= c1[0]) and (annot[cnt].samex[i] <= c2[0]) and ((annot[cnt].samey[i] >= c2[1]) and (annot[cnt].samey[i] <= c1[1]))):
                if (txt == 'Person1'):
                    ax.plot(annot[cnt].samex[i],annot[cnt].samey[i],colorName)
                elif (txt == 'Person2'):
                    ax.plot(annot[cnt].samex[i],annot[cnt].samey[i],colorName)
                curr_ptr.append(i)
                objx.append(annot[cnt].samex[i])
                objy.append(annot[cnt].samey[i])
            else:
                ax.plot(annot[cnt].samex[i],annot[cnt].samey[i],'bo')
        '''
        for i in range(len(annot[cnt].samex)):
            if ((annot[cnt].samex[i] >= c1[0]) and (annot[cnt].samex[i] <= c2[0]) and ((annot[cnt].samey[i] >= c2[1]) and (annot[cnt].samey[i] <= c1[1]))):
                ax.plot(annot[cnt].samex[i],annot[cnt].samey[i],colorName)
                curr_ptr.append(i)
                objx.append(annot[cnt].samex[i])
                objy.append(annot[cnt].samey[i])
            else:
                ax.plot(annot[cnt].samex[i],annot[cnt].samey[i],'bo')
        '''
        fw.draw()

class ApplicationWindow(QtWidgets.QMainWindow):

    def __init__(self):

        global scan_widget

        QtWidgets.QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.main_widget = QtWidgets.QWidget(self)

        scan_widget = LS(self.main_widget)

        #Define buttons
        scanLayout = QHBoxLayout() 
        scanLayout.addWidget(scan_widget)

        playButton = QPushButton("Play")
        pauseButton = QPushButton("Pause")
        prevFrameButton = QPushButton("Previous")
        nextFrameButton = QPushButton("Next")
        stopButton = QPushButton("Stop")
        annotationButton = QPushButton("Annotation")
        saveButton = QPushButton("Save")

        classes = QComboBox()
        classes.addItem('Classes')
        classes.addItem('Person1')
        classes.addItem('Person2')
        classes.addItem('Other')

        buttonLayout = QVBoxLayout()
        buttonLayout.addWidget(playButton)
        buttonLayout.addWidget(pauseButton)
        buttonLayout.addWidget(prevFrameButton)
        buttonLayout.addWidget(nextFrameButton)
        buttonLayout.addWidget(stopButton)
        buttonLayout.addStretch(1)
        buttonLayout.addWidget(annotationButton)
        buttonLayout.addWidget(saveButton)
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
        saveButton.clicked.connect(self.bsave)
        classes.activated[str].connect(self.chooseClass)

        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)


    def bplay(self):
        global scan_widget
        scan_widget.ptime()

    def bpause(self):
        global timer
        timer.stop()

    def bprevious(self):
        global cnt,ax,fw,annot,colorName,annot
        if (cnt>0):
            cnt = cnt-1
            ax.clear()
            ax.axis('equal')
            ax.plot(annot[cnt].samex,annot[cnt].samey, 'bo')
            if not annot[cnt].listofpointsx == []:
                ax.plot(annot[cnt].listofpointsx,annot[cnt].listofpointsy,colorName)
            fw.draw()
        else:
            ax.clear()
            fw.draw()

    def bnext(self):
        global cnt,ax,fw,colorName, annot
        if (cnt<len(annot)):
            cnt = cnt+1
            ax.clear()
            ax.axis('equal')
            ax.plot(annot[cnt].samex,annot[cnt].samey,'bo')
            if not annot[cnt].listofpointsx == []:
                ax.plot(annot[cnt].listofpointsx,annot[cnt].listofpointsy,colorName)
            fw.draw()
        else:
            ax.clear()
            fw.draw()

    def bstop(self):
        global cnt,timer,ax,fw
        cnt=0
        timer.stop()
        ax.clear()
        fw.draw()

    def bannotation(self):
        global annotating
        annotating = True
        fig.canvas.mpl_connect('button_press_event', self.onCLick)

    def onCLick(self,event):

        global c1,c2,ax,firstclick,secondclick,thirdclick,scan_widget,annotating, annot, cnt, listofpointsx, listofpointsy,fw

        if annotating:
            x = event.x
            y = event.y
            if event.button == 1:
                if firstclick == False:
                    if event.inaxes is not None:
                        c1 = [event.xdata,event.ydata]
                        firstclick = True
                elif secondclick == False:
                    if event.inaxes is not None:
                        c2 = [event.xdata,event.ydata]
                        if (c2[0]<c1[0]):
                            temp_c = c2
                            c2 = c1
                            c1 = temp_c
                        secondclick = True
                        scan_widget.rect()
                elif ((not thirdclick) and (secondclick)):
                    if event.inaxes is not None:
                        ax.clear()
                        ax.plot(annot[cnt].samex,annot[cnt].samey, 'bo')
                        fw.draw()
                        firstclick = False
                        secondclick = False

    '''
    1. Na krataei clickstart kai clickend
    2. Na antistixizei ID1, ID2,...
    3. Na zwgrafizei ola auta ta ID kai meta ta upoloipa simeia
    '''

    def chooseClass(self, text):
        global colorName,txt,scan_widget
        txt=text
        if text == 'Selections':
            print 'Please, choose class'
        elif text == 'Person1':
            colorName = 'go'
        elif text == 'Person2':
            colorName = 'ro'
        elif text == 'Other':
            colorName = 'bo'
        scan_widget.training()

    def bsave(self):
        global annotating, cnt,  c1, c2, objx, objy, txt, curr_ptr, annot, bag_file,data

        annotating = False

        '''
        prepei na apo9ikevw kai to xrwma pou antistoixei se ka9e ID
        '''

        annot[cnt].bbstart.append(c1)
        annot[cnt].bbend.append(c2)
        annot[cnt].annotID.append(txt)
        annot[cnt].listofpointsx.append(objx)
        annot[cnt].listofpointsy.append(objy)
        annot[cnt].samex = [x for x in annot[cnt].samex if x not in annot[cnt].listofpointsx]
        annot[cnt].samey = [y for y in annot[cnt].samey if y not in annot[cnt].listofpointsy]

        filename = bag_file.replace(".bag","_laser.csv")
        with open(filename, 'w') as data:
            write = csv.writer(data)
            for row in annot:
                row_ = [row.bbstart, row.bbend, row.samex, row.samey, row.listofpointsx, row.listofpointsy, row.annotID]
                write.writerow(row_)
            data.close()


class laserAnn:

    global c1,c2, objx,objy, s1,s2, txt

    def __init__(self, bbstart_=None, bbend_=None, samex_=None, samey_=None, listofpointsx_=None,listofpointsy_=None, annotID_=None): #TODO fix constructor parameters

        self.bbstart = []
        self.bbend = []
        self.samex = []
        self.samey = []
        self.listofpointsx = []
        self.listofpointsy = []
        self.annotID = []

        '''
        self.bbstart.append(c1)
        self.bbend.append(c2)
        self.listofpointsx.append(objx)
        self.listofpointsy.append(objy)
        self.annotID.append(txt)
        '''
        if bbstart_ == None:
            self.bbstart = []
        else:
            self.bbstart = bbstart_
        if bbend_ == None:
            self.bbend = []
        else:
            self.bbend = bbend_
        if samex_ == None:
            self.samex = []
        else:
            self.samex = samex_
        if samey_ == None:
            self.samey = []
        else:
            self.samey = samey_
        if listofpointsx_ == None:
            self.listofpointsx = []
        else:
            self.listofpointsx = listofpointsx_
        if listofpointsy_ == None:
            self.listofpointsy = []
        else:
            self.listofpointsy = listofpointsy_
        if annotID_ == None:
            self.annotID = []
        else:
            self.annotID = annotID_


def run(laserx,lasery,bagFile):

    global timer,scan_widget,annot,s1,s2,bag_file,colorName

    timer = QtCore.QTimer(None)

    bag_file = bagFile
    filename = bag_file.replace(".bag", "_laser.csv")
    if os.path.isfile(filename):
    #if False:
        with open(filename, 'rb') as data:
            if os.path.getsize(filename)>1:
                read = csv.reader(data)
                for row in read:
                    row[0] = row[0][2:-2]
                    row[1] = row[1][2:-2]
                    row[2] = row[2][2:-2]
                    row[3] = row[3][2:-2]
                    row[4] = row[4][2:-2]
                    row[5] = row[5][2:-2]
                    row[6] = row[6][2:-2]
                    row[0] = row[0].split(", ")
                    row[1] = row[1].split(", ")
                    row[2] = row[2].split(", ")
                    row[3] = row[3].split(", ")
                    row[4] = row[4].split(", ")
                    row[5] = row[5].split(", ")
                    row[6] = row[6].split(", ")

                    for i in range(0, len(row[0])):
                        if row[0][i] == "":
                            row[0] = []
                            break
                        '''
                        else:
                            row[0][i] = row[0][i]
                            #row[0][i] = float(row[0][i])
                        '''
                    for i in range(0, len(row[1])):
                        if row[1][i] == "":
                            row[1] = []
                            break
                        '''
                        else:
                            row[1][i] = float(row[1][i])
                        '''
                    for i in range(0, len(row[2])):
                        if row[2][i] == "":
                            row[2] = []
                            break
                        '''
                        else:
                            row[2][i] = float(row[2][i])
                        '''
                    for i in range(0, len(row[3])):
                        if row[3][i] == "":
                            row[3] = []
                            break
                        '''
                        else:
                            row[3][i] = float(row[3][i])
                        '''
                    for i in range(0, len(row[4])):
                        if row[4][i] == "":
                            row[4] = []
                            break
                        '''
                        else:
                            row[4][i] = float(row[4][i])
                        '''
                    for i in range(0, len(row[5])):
                        if row[5][i] == "":
                            row[5] = []
                            break
                        '''
                        else:
                            row[5][i] = float(row[5][i])
                        '''
                    for i in range(0, len(row[6])):
                        if row[6][i] == "":
                            row[6] = []
                            break
                        else:
                            row[6][i] = str(row[6][i])
                            if row[6] == 'Person1':
                                colorName = 'go'
                            elif row[6] == 'Person2':
                                colorName = 'ro'
                    '''
                    print row[0]
                    print row[1]
                    print row[2]
                    print row[3]
                    print row[4]
                    print row[5]
                    '''
                    #print row[6]

                    la = laserAnn(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
                    annot.append(la)
    else:
        for i in range(len(laserx)):
            s1 = laserx[i].tolist()
            s2 = lasery[i].tolist()
            la = laserAnn(samex_=s1,samey_=s2)
            annot.append(la)

    qApp = QtWidgets.QApplication(sys.argv)

    s = ApplicationWindow()

    s.show()

    sys.exit(qApp.exec_())