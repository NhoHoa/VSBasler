from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from pypylon import pylon
# import Opencv module
import cv2,time,sys
import numpy as np
import utlis
from QT_Basler import Ui_MainWindow
from Basler_camera_setting import MyVideoCapture
from Step_editor import Ui_Dialog

class Window_form(Ui_MainWindow,QMainWindow):
	def __init__(self):
		super(Window_form, self).__init__()			
		self.camera_device = pylon.TlFactory.GetInstance().CreateFirstDevice()		
		self.camera = MyVideoCapture(self.camera_device)		
		self.live = True
		self.img = [0,0,0]
		self.subimg = [0, 0, 0]
		self.low_thresh = 125
		self.scaleFactor = 1
		

	def setupUi_more(self,MainWindow):
		self.setupUi(MainWindow)
		self.actionSetup.triggered.connect(self.zoomIn)
		self.actionAuto.triggered.connect(self.zoomOut)

		self.sldBinThreshold.valueChanged.connect(self.set_Threshold)
		self.sldCanny_lo.valueChanged.connect(self.set_Canny_lo)
		self.sldCanny_up.valueChanged.connect(self.set_Canny_up)

		# self.zoomInAct = QAction("Zoom &In (25%)", self, shortcut="Ctrl++", enabled=False, triggered=self.zoomIn)
		# self.zoomOutAct = QAction("Zoom &Out (25%)", self, shortcut="Ctrl+-", enabled=False, triggered=self.zoomOut)
		
		self.lblBinThresValue.setText(str(self.sldBinThreshold.value()))
		self.lblCanny_lo.setText(str(self.sldCanny_lo.value()))	
		self.lblCanny_up.setText(str(self.sldCanny_up.value()))	

		self.timer = QtCore.QTimer(self)
		self.timer.timeout.connect(self.update_frame)
		self.timer.start(30)

	def update_window(self):
		pass


	def update_frame(self):	
		rect = self.lblImage.getRect()
		ret, frame = self.camera.get_frame()
		if ret:
			self.img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
			resize = utlis.ResizeWithAspectRatio(self.img, height=self.lblSubImage.frameRect().height(),width=self.lblSubImage.frameRect().width())
			
			imageArray = utlis.find_image(self.img,self.sldCanny_lo.value(),self.sldCanny_up.value())
			height, width, channel = resize.shape
			step = channel * width
			qImg = QImage(resize.data, width, height, step, QImage.Format_RGB888)
			self.lblSubImage.setPixmap(QPixmap.fromImage(qImg))			
			_selectedImage = self.cbbSelectImage.currentText()
			if _selectedImage =="Image":
				utlis.Display_Qlable(imageArray[0][0],self.lblImage)
			elif _selectedImage =="Gray Image":
				utlis.Display_Qlable(imageArray[0][1],self.lblImage)
			elif _selectedImage =="Canny Image":
				utlis.Display_Qlable(imageArray[0][2],self.lblImage)
			elif _selectedImage =="Contour Image":
				utlis.Display_Qlable(imageArray[0][3],self.lblImage)
			elif _selectedImage =="Big contour Image":
				utlis.Display_Qlable(imageArray[1][0],self.lblImage)
			elif _selectedImage =="Sample Image":
				utlis.Display_Qlable(imageArray[1][1],self.lblImage)
				

			# coppyImage = cv2.resize(imageArray[1][1],(self.lblImage.frameRect().width(),self.lblImage.frameRect().height()),interpolation = cv2.INTER_AREA)
			coppyImage = cv2.resize(imageArray[1][1],(self.lblImage.frameRect().width(),self.lblImage.frameRect().height()),interpolation=cv2.INTER_CUBIC)
			self.subimg = coppyImage[self.lblImage.getRect().y():self.lblImage.getRect().y()+self.lblImage.getRect().height(),self.lblImage.getRect().x():self.lblImage.getRect().x()+self.lblImage.getRect().width()]

			# if self.lblImage.isstep_editor:
			# 	self.Show_Add_step()
			# 	self.lblImage.isstep_editor = False

	def set_Threshold(self):
		self.low_thresh= self.sldBinThreshold.value()
		self.lblBinThresValue.setText(str(self.sldBinThreshold.value()))	

	def set_Canny_lo(self):
		self.Cannylo= self.sldCanny_lo.value()
		self.lblCanny_lo.setText(str(self.sldCanny_lo.value()))

	def set_Canny_up(self):
		self.Cannyup= self.sldCanny_up.value()
		self.lblCanny_up.setText(str(self.sldCanny_up.value()))

	def Show_Add_step(self):
		Dialog = QtWidgets.QDialog()
		ui = Ui_Dialog()
		ui.setupUi(Dialog)
		utlis.Display_Qlable(self.subimg,ui.lblcheckingImage)
		Dialog.exec_()

	def scaleImage(self, factor):
		self.scaleFactor *= factor
		print("test")
		self.lblImage.resize(self.scaleFactor * self.lblImage.pixmap().size())

		self.adjustScrollBar(self.scrollArea.horizontalScrollBar(), factor)
		self.adjustScrollBar(self.scrollArea.verticalScrollBar(), factor)

		self.actionSetup.setEnabled(self.scaleFactor < 3.0)
		self.actionAuto.setEnabled(self.scaleFactor > 0.333)
	def zoomIn(self):
		self.scaleImage(1.25)

	def zoomOut(self):
		self.scaleImage(0.8)

	def adjustScrollBar(self, scrollBar, factor):
		scrollBar.setValue(int(factor * scrollBar.value()
		                       + ((factor - 1) * scrollBar.pageStep() / 2)))


if __name__ == "__main__":
	import sys
	app = QtWidgets.QApplication(sys.argv)
	MainWindow = QtWidgets.QMainWindow()
	ui = Window_form()    
	ui.setupUi_more(MainWindow)
	MainWindow.show()
	sys.exit(app.exec_())