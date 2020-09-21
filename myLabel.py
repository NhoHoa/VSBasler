from PyQt5.QtWidgets import QLabel, QSizePolicy, QScrollArea, QMessageBox, QMainWindow, QMenu, QAction, \
    qApp, QFileDialog
from PyQt5.QtCore import QRect, Qt
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QGuiApplication

import sys
class myLabel(QLabel):
    x0 = 0
    y0 = 0
    x1 = 0
    y1 = 0
    flag = False
    isMoving = False
    isstep_editor = False 
    rect = QRect()

    def mousePressEvent(self,event):
        self.flag = True
        self.isMoving = False
        self.isstep_editor = False 
        self.x0 = event.x()
        self.y0 = event.y()
         # 
    def mouseReleaseEvent(self,event):
        self.flag = False
        self.isMoving = False
        self.isstep_editor = True 

         # 
    def mouseMoveEvent(self,event):
        self.isstep_editor = False 
        self.isMoving = True
        if self.flag:
            self.x1 = event.x()
            self.y1 = event.y()            
            self.update()
         #  event
            

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.x1>self.x0:
            if self.y1>self.y0:
                self.rect =QRect(self.x0, self.y0, abs(self.x1-self.x0), abs(self.y1-self.y0))
            else:
                self.rect =QRect(self.x0, self.y1, abs(self.x1-self.x0), abs(self.y1-self.y0))
        else:
            if self.y1>self.y0:
                self.rect =QRect(self.x1, self.y0, abs(self.x1-self.x0), abs(self.y1-self.y0))
            else:
                self.rect =QRect(self.x1, self.y1, abs(self.x1-self.x0), abs(self.y1-self.y0))
       
        painter = QPainter(self)
        if self.isMoving:
            painter.setPen(QPen(Qt.red,2,Qt.SolidLine))
        else:
            painter.setPen(QPen(Qt.blue,2,Qt.SolidLine))
        painter.drawRect(self.rect)

    def getRect(self):
        return self.rect
    def getSubImage_from_Image(self,image):
        img = image[self.rect.x():self.rect.x()+self.rect.width(),self.rect.y():self.rect.y()+self.rect.height()]
        height, width, channel = img.shape
        step = channel * width
        qImg = QImage(img.data, width, height, step, QImage.Format_RGB888)
        return qImg

    