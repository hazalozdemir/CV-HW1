# -*- coding: utf-8 -*-
"""
Created on Sun Oct 21 18:06:50 2018

@author: hazal
"""

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, \
    QPushButton, QGroupBox, QAction, QFileDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from matplotlib.figure import Figure
from PyQt5 import QtWidgets, QtGui, QtCore
import matplotlib.pyplot as plt
import matplotlib.pyplot as plot
import numpy as np
from scipy import misc
import cv2

##########################################
## Do not forget to delete "return NotImplementedError"
## while implementing a function
########################################

class App(QMainWindow):
    def __init__(self):
        super(App, self).__init__()
       # return NotImplementedError


        self.title = 'Histogram Equalization'
        # You can define other things in here
        self.left = 70
        self.top = 70
        self.width = 640
        self.height = 400
        self.initUI()

    def openInputImage(self):
        # This function is called when the user clicks File->Input Image.
        
        #name = QFileDialog.getOpenFileName(self, 'Open Input')
       # file = open(name,'r')
       # name = 'C:\\Users\\hazal\\Desktop\\Myself\\Fall2018\\Computer Vision\\BLG453E_hw1\\BLG453E_hw1\\color1.png'
        #pixmap=QPixmap(name)
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        img = cv2.imread(fileName)
        print("img",img)
        self.label_image = QLabel(self)
     #   self.label_image.setGeometry(5,5,231,550)
        input_img = QImage(fileName)
     #   input_img = input_img.scaled(2/3*input_img.width,1*input_img.height)
     #   input_img = input_img.
        self.label_image.setPixmap(QPixmap.fromImage(input_img))
     #   self.label_image.adjustSize()
      #  self.resize(input_img.width(),input_img.height())
        vbox1 = QVBoxLayout()
        vbox1.addWidget(self.label_image)
       # vbox.setGeometry(15,15,31,50)
        self.groupbox1.setLayout(vbox1)
        self.calcHistogram(img)
        
        #PlotCanvas.plotHistogram(self,hist)
        
        #return NotImplementedError

    def openTargetImage(self):
        # This function is called when the user clicks File->Target Image.
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        self.label_image = QLabel(self)
        
        target_img = QImage(fileName)
        self.label_image.setPixmap(QPixmap.fromImage(target_img))
        vbox2 = QVBoxLayout()
        vbox2.addWidget(self.label_image)
        self.groupbox2.setLayout(vbox2)
        
        
        

    def initUI(self):
      #  return NotImplementedError
        # Write GUI initialization code
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        
        self.groupbox1 = QtWidgets.QGroupBox(self)
        self.groupbox1.setTitle('Input')
        self.groupbox1.setGeometry(QtCore.QRect(70, 70, 231, 551))
        
        
        self.groupbox2 = QtWidgets.QGroupBox(self)
        self.groupbox2.setTitle('Target')
        self.groupbox2.setGeometry(QtCore.QRect(270, 70, 231, 551))
        
        self.groupbox3 = QtWidgets.QGroupBox(self)
        self.groupbox3.setTitle('Result')
        self.groupbox3.setGeometry(QtCore.QRect(530, 70, 231, 551))
        
        mainMenu = self.menuBar() 
        fileMenu = mainMenu.addMenu('File')
        
        inputButton = QAction('Open Input',self)
        inputButton.triggered.connect(self.openInputImage)
        fileMenu.addAction(inputButton)
        
        
        targetButton = QAction('Open Target',self)
        targetButton.triggered.connect(self.openTargetImage)
        fileMenu.addAction(targetButton)
        
        exitButton = QAction('Exit', self)       
        exitButton.setStatusTip('Exit application')
        exitButton.triggered.connect(self.close)
        fileMenu.addAction(exitButton)
        

        extractAction = QAction('Equalize Histogram',self)
        extractAction.triggered.connect(self.histogramButtonClicked)
        self.toolbar = self.addToolBar('Equalize Histogram')
        self.toolbar.addAction(extractAction)
       
        self.show()

    def histogramButtonClicked(self):
        if not self.inputLoaded and not self.targetLoaded:
            # Error: "First load input and target images" in MessageBox
            return NotImplementedError
        if not self.inputLoaded:
            # Error: "Load input image" in MessageBox
            return NotImplementedError
        elif not self.targetLoaded:
            # Error: "Load target image" in MessageBox
            return NotImplementedError

    def calcHistogram(self, I):
        # Calculate histogram
        return NotImplementedError

class PlotCanvas(FigureCanvas):
    def __init__(self, hist, parent=None, width=5, height=4, dpi=100):
        return NotImplementedError
        # Init Canvas
        self.plotHistogram(hist)

    def plotHistogram(self, hist):
        return NotImplementedError
        # Plot histogram

        self.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())