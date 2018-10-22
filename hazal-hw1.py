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
    from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
else:
    from matplotlib.backends.backend_qt4agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
import PIL
##########################################
## Since opencv read images backward, i had to dedicated 0: channel for blue
## 2: for red, all implementations done according to this
########################################

class App(QMainWindow):    
    def __init__(self):
        super(App, self).__init__()
       # return NotImplementedError

        self.histogram_list1= None
        self.histogram_list2= None
        self.histogram_list3= None

        self.check_input_flag = False
        self.check_target_flag = False
        self.title = 'Histogram Equalization'
        # You can define other things in here
        self.left = 70
        self.top = 70
        self.width = 640
        self.height = 400
        self.initUI()

    def openInputImage(self):
        # This function is called when the user clicks File->Input Image.
        
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        self.img = cv2.imread(fileName)
        
        if not(self.img is None):
            self.check_input_flag = True
        self.label_image = QLabel(self)
        input_img = QImage(fileName)
        self.label_image.setPixmap(QPixmap.fromImage(input_img))
        vbox1 = QVBoxLayout()
        vbox1.addWidget(self.label_image)
     
        self.calc_hist1 = self.calcHistogram(self.img)
        
        self.histogram_list1 = self.calc_hist1
        
     #   self.red_band = self.calc_hist1[0]
     #   self.green_band  = self.calc_hist1[1]
     #   self.blue_band = self.calc_hist1[2]
        vbox1.addWidget(self.canvas)
        self.canvas =self.plotHistogram1(self.histogram_list1[0],self.histogram_list1[1],self.histogram_list1[2])
        self.groupbox1.setLayout(vbox1)
      
    def openTargetImage(self):
        # This function is called when the user clicks File->Target Image.
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        self.label_image = QLabel(self)
        
        img2 = cv2.imread(fileName)
        if not(img2 is None):
            self.check_target_flag = True
        target_img = QImage(fileName)
        self.label_image.setPixmap(QPixmap.fromImage(target_img))
        vbox2 = QVBoxLayout()
        vbox2.addWidget(self.label_image)
            
        if not(img2 is None):
            self.calc_hist = self.calcHistogram(img2)
            self.histogram_list2 = self.calc_hist
            vbox2.addWidget(self.canvas2)
            self.canvas2 =self.plotHistogram2(self.histogram_list2[0],self.histogram_list2[1],self.histogram_list2[2])
        self.groupbox2.setLayout(vbox2)
        
    def openResultImage(self,K):
        
        cv2.imwrite('result.jpg', K.astype(np.uint8))

        self.label_image = QLabel(self)
        pixmap = QPixmap('result.jpg')
        self.label_image.setPixmap(pixmap)
       
        vbox3 = QVBoxLayout()
        vbox3.addWidget(self.label_image)
        
        self.calc_hist = self.calcHistogram(K)
        self.histogram_list3 = self.calc_hist
        
        vbox3.addWidget(self.canvas3)
        self.canvas3 =self.plotHistogram3(self.histogram_list3[0],self.histogram_list3[1],self.histogram_list3[2])
        self.groupbox3.setLayout(vbox3)     
         
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
        self.figure3 = plt.figure(figsize=(width, height), dpi=dpi)
        self.canvas3 = FigureCanvas(self.figure3)
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
        
        self.error_dialog1 = QtWidgets.QErrorMessage()
        self.error_dialog2 = QtWidgets.QErrorMessage()
        self.error_dialog3 = QtWidgets.QErrorMessage()
        self.show()

    def inputLoaded(self):
        if(self.check_input_flag == True):
            return True
        else:
            return False
    def targetLoaded(self):
        if(self.check_target_flag == True):
            return True
        else:
            return False
    def histogramButtonClicked(self):       
        if (self.inputLoaded() == False  and  self.targetLoaded() == False):
            self.error_dialog1.showMessage('Error: "First load input and target images')
        elif not(self.inputLoaded()):
            self.error_dialog2.showMessage('Error: Load input image')
        elif not(self.targetLoaded()):
            self.error_dialog3.showMessage('Error: "Load target image')
        else:
            self.matchHistogram(self.img)
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
    
    def matchHistogram(self,I):
        
        row, column, channel = I.shape
        
        
        self.Lut_red = np.zeros([256,1]) 
        self.input_red_cdf = self.get_cdf(self.histogram_list1[0])
        self.target_red_cdf = self.get_cdf(self.histogram_list2[0])
        
       
        
        self.Lut_red = self.get_lut(self.input_red_cdf,self.target_red_cdf)
       
        self.Lut_green = np.zeros( [256,1]) 
        self.input_green_cdf = self.get_cdf(self.histogram_list1[1])
        self.target_green_cdf = self.get_cdf(self.histogram_list2[1])
        
        self.Lut_green = self.get_lut(self.input_green_cdf,self.target_green_cdf)
          
        self.Lut_blue = np.zeros( [256,1]) 
        self.input_blue_cdf = self.get_cdf(self.histogram_list1[2])
        self.target_blue_cdf = self.get_cdf(self.histogram_list2[2])
        
        self.Lut_blue = self.get_lut(self.input_blue_cdf,self.target_blue_cdf)
        
        K = np.zeros([row,column,channel], dtype=np.uint8)
        
        for i in range(0,row):
            for j in range(0,column):
                red_band_val  = I[i][j][0]
                new_val_red = self.Lut_red[red_band_val,0]
                K[i][j][0] = new_val_red
                
                green_band_val  = I[i][j][1]
                new_val_green = self.Lut_green[green_band_val,0]
                K[i][j][1] = new_val_green
                
                blue_band_val  = I[i][j][2]
                new_val_blue = self.Lut_blue[blue_band_val,0]
                K[i][j][2] = new_val_blue
        
        self.openResultImage(K.astype(np.uint8))
    
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