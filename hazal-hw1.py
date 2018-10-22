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
from matplotlib.backends.qt_compat import QtCore, QtWidgets, is_pyqt5
if is_pyqt5():
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
else:
    from matplotlib.backends.backend_qt4agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
##########################################
## Do not forget to delete "return NotImplementedError"
## while implementing a function
########################################

class App(QMainWindow):
    def __init__(self):
        super(App, self).__init__()
       # return NotImplementedError

        self.histogram_list1= None
        self.histogram_list2= None
        self.histogram_list3= None

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
        
        self.calc_hist1 = self.calcHistogram(self.img)
        
        self.histogram_list1 = self.calc_hist1

        vbox1.addWidget(self.canvas)
        self.canvas =self.plotHistogram1(self.histogram_list1[0],self.histogram_list1[1],self.histogram_list1[2])
        self.groupbox1.setLayout(vbox1)
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
            self.calc_hist = self.calcHistogram(img2)
            self.histogram_list2 = self.calc_hist
            vbox2.addWidget(self.canvas2)
            self.canvas2 =self.plotHistogram2(self.histogram_list2[0],self.histogram_list2[1],self.histogram_list2[2])
        self.groupbox2.setLayout(vbox2)
        
        
        

    def initUI(self):
      #  return NotImplementedError
        # Write GUI initialization code
        width = 4
        height = 2
        dpi = 100
        self.figure = plt.figure(figsize=(width, height), dpi=dpi)
        self.canvas = FigureCanvas(self.figure)
        self.figure2 = plt.figure(figsize=(width, height), dpi=dpi)
        self.canvas2 = FigureCanvas(self.figure2)
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        
        self.groupbox1 = QtWidgets.QGroupBox(self)
        self.groupbox1.setTitle('Input')
        self.groupbox1.setGeometry(QtCore.QRect(70, 70, 431, 951))
        
        
        self.groupbox2 = QtWidgets.QGroupBox(self)
        self.groupbox2.setTitle('Target')
        self.groupbox2.setGeometry(QtCore.QRect(570, 70, 431, 951))
        
        self.groupbox3 = QtWidgets.QGroupBox(self)
        self.groupbox3.setTitle('Result')
        self.groupbox3.setGeometry(QtCore.QRect(1070, 70, 431, 951))
        
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
        row, column, channel = I.shape
  
        #get r,g,b channels
        red_channel = I[:,:,0]
        green_channel = I[:,:,1]
        blue_channel = I[:,:,2]
       
        #histogram allocation
        red_hist = np.zeros([256,1])
        green_hist = np.zeros([256,1])
        blue_hist = np.zeros([256,1])
  
        for i in range(0,row):
            for j in range(0, column):
                pix_num_red = red_channel[i][j]
                red_hist[pix_num_red,0] = red_hist[pix_num_red,0] + 1
                
                pix_num_green = green_channel[i][j]
                green_hist[pix_num_green,0] = green_hist[pix_num_green,0] + 1
                
                pix_num_blue = blue_channel[i][j]
                blue_hist[pix_num_blue,0] = blue_hist[pix_num_blue,0] + 1
        
 #       x = range(0,256)
  #      plt.bar(x, blue_hist[:,0])
        return [red_hist,green_hist, blue_hist]
    def get_cdf(self, hist):
        
        total_sum = 0
        cdf = np.zeros([256,1])
        
        for i in range(0,256):
            total_sum = total_sum + hist[i,0]
        
        cdf[0,0] = (hist[0,0] / total_sum )
        
        for i in range(1,256):
            cdf[i,0]= (hist[i,0] / total_sum) + cdf[i-1,0]
        
        return cdf
    def get_lut(self,cdf1, cdf2):
        #histogram matching by using look up table
        LUT = np.zeros([256,1])
        
        for g in range (0,256):
            j = 1    
            while (j < 255 ):
                if (cdf1[g,0] > cdf2[j-1,0] and (cdf1[g,0] <= cdf2[j,0])):
                    break
                else:
                    j = j + 1
            
            LUT[g,0] = j
            
        return LUT
    def plotHistogram1(self, hist1,hist2,hist3):
 
        ax = self.figure.add_subplot(311)
        x = range(0, 256)   
        ax.bar(x, hist3[:,0], color = 'red')
        
        ax1 = self.figure.add_subplot(312)
        x = range(0, 256)
        ax1.bar(x, hist2[:,0], color = 'green')
        
        ax2 = self.figure.add_subplot(313)
        x = range(0, 256)
        ax2.bar(x, hist1[:,0], color = 'blue')
        
        self.canvas.draw_idle()
 
    def plotHistogram2(self, hist1,hist2,hist3):

        bx = self.figure2.add_subplot(311)
        x = range(0, 256)   
        bx.bar(x, hist3[:,0], color = 'red')
        
        bx1 = self.figure2.add_subplot(312)
        x = range(0, 256)
        bx1.bar(x, hist2[:,0], color = 'green')
        
        bx2 = self.figure2.add_subplot(313)
        x = range(0, 256)
        bx2.bar(x, hist1[:,0], color = 'blue')
        
        self.canvas2.draw_idle()
 
    def plotHistogram3(self, hist1,hist2,hist3):
     
        cx = self.figure3.add_subplot(311)
        x = range(0, 256)   
        cx.bar(x, hist3[:,0], color = 'red')
        
        cx1 = self.figure3.add_subplot(312)
        x = range(0, 256)
        cx1.bar(x, hist2[:,0], color = 'green')
        
        cx2 = self.figure3.add_subplot(313)
        x = range(0, 256)
        cx2.bar(x, hist1[:,0], color = 'blue')
        
        self.canvas3.draw_idle()
            

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())