import sys,csv,os
from PyQt5 import QtCore, QtGui, QtWidgets
from gui import Ui_MainWindow
import glob
import os.path


roi_list = []
if os.path.exists("roi.csv"):
	with open('roi.csv','r')as f:
		data = csv.reader(f)
		for row in data:
			roi_list.append(row)

def clear_roi():
	del roi_list[:]	
main_var = ''
filename = ''
class MyWidget(QtWidgets.QWidget):

	def __init__(self):
		super().__init__()
		self.rect_state=1
		self.rect_list = []
		self.rect_list1 = []
		self.ret= True
		self.setGeometry(30,30,200,200)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		#sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
		self.setSizePolicy(sizePolicy)

		self.begin = QtCore.QPoint()
		self.end = QtCore.QPoint()
		self.show()
		self.paintEvent(self)

		global roi_list
		global filename
	    

	def load_prev_box(self,qp):
		for brc in roi_list:
			qp.drawRect(QtCore.QRect(QtCore.QPoint(int(brc[0]),int(brc[1])),QtCore.QPoint(int(brc[2]), int(brc[3]))))
		

	def clear_boxes(self):
		self.rect_state=0
		self.rect_list = []
		self.rect_list1 = []
		global filename

		# opening the file with w+ mode truncates the file
		os.remove(filename)
		f = open(filename, "w+")
		f.close()
		roi_list = []
		clear_roi()
		#print("cleared")
	    

	def paintEvent(self, event):
		qp = QtGui.QPainter(self)
		#print('painting')
		#painter = QPainter(self)

		try:
			qp.drawPixmap(self.rect(), main_var)
	        

		except Exception as e:
			print(e,'**************',type(main_var))

		if self.rect_state ==1:
				#print('----------------------',self.rect_list,type(self.rect_list),len(self.rect_list))
			br = QtGui.QBrush(QtGui.QColor(255, 0, 0, 30))
			#qp.setPen(Qt.NoPen);
			qp.setBrush(br)
			for brc in range(0,len(self.rect_list) ):
				qp.drawRect(QtCore.QRect( self.rect_list[brc], self.rect_list1[brc] ))
			if self.ret:
				self.load_prev_box(qp)
				#self.ret = False

		#        br1 = QtGui.QBrush(QtGui.QColor(100, 10, 10, 40))
		#        qp.setBrush(br1)
		#        qp.drawRect(QtCore.QRect(self.begin-QtCore.QPoint(10, 10), self.end-QtCore.QPoint(10, 10)))

	def mousePressEvent(self, event):
		self.begin = event.pos()
		#print(self.begin)

	def mouseMoveEvent(self, event):
		pass

	def mouseReleaseEvent(self, event):
		self.end = event.pos()
		self.rect_list.append(self.begin)
		self.rect_list1.append(self.end)
		self.rect_state =1
		roi_list_temp =list(map(str,str(self.rect_list[-1])[20:-1].split(",")))+list(map(str,str(self.rect_list1[-1])[20:-1].split(",")))
		roi_list.append(roi_list_temp)
		global filename
		print(filename)
		with open('{}'.format(filename), 'a+') as writeFile:
			writer = csv.writer(writeFile)
			writer.writerows([roi_list_temp])
		self.update()

class MainWindow_exec(QtWidgets.QMainWindow, Ui_MainWindow):
	def __init__(self, parent=None):
		QtWidgets.QMainWindow.__init__(self, parent)
		self.u = 0
		self.v = 0
		
		#print(roi_list)
		self.setupUi(self)
		print("*"*40,self.image_view.height(),self.image_view.width())
		self.gridLayout_4.removeWidget(self.image_view)
		self.image_view.close()
		self.image_view = MyWidget()
		self.image_view.setStyleSheet("border: 10px solid black;")
		self.gridLayout_4.addWidget(self.image_view,1,1,1,1)

		self.image_view.setMinimumSize(200,200)
		self.img_browse.clicked.connect(self.getImagefolder)
		self.annotation_browse.clicked.connect(self.getAnnotationfolder)
		self.prev_btn.clicked.connect(self.prevImage)
		self.next_btn.clicked.connect(self.nextImage)
		self.counter =0
		self.image_list = None
		self.annotation_list  =None
		self.Dname = None


	def prevImage(self):
		if self.counter >=0:
			if self.counter !=0:
				self.counter -=1
			currIamge=self.image_list[self.counter]
			pix = QtGui.QPixmap(str(currIamge))
			global main_var 
			annotationName = self.Dname+"/"+str(currIamge.split(".")[-2].split("/")[-1])+".txt"
			self.load_Annotation(annotationName)
			main_var = pix
			self.image_view.update()
			self.label_index.setText("{}/{}".format(self.counter,len(self.image_list)-1))
			

	def nextImage(self):
		if self.counter < len(self.image_list)-1:
			self.counter +=1
			currIamge=self.image_list[self.counter]
			pix = QtGui.QPixmap(str(currIamge))
			global main_var 
			annotationName = self.Dname+"/"+str(currIamge.split(".")[-2].split("/")[-1])+".txt"
			self.load_Annotation(annotationName)
			main_var = pix
			self.image_view.update()
			self.label_index.setText("{}/{}".format(self.counter,len(self.image_list)-1))


	def getImagefolder(self):
		self.Dname = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select directory')
		self.label_4.setText(self.Dname)
		self.image_list = [item for i in [glob.glob('{}/*.{}'.format(self.Dname,ext)) for ext in ["jpg","gif","png","tga"]] for item in i]
		self.counter =0
		pix = QtGui.QPixmap(str(self.image_list[self.counter]))
		global main_var 
		main_var = pix
		self.image_view.update()
		self.label_index.setText("{}/{}".format(self.counter,len(self.image_list)-1))
		

	def getAnnotationfolder(self):
		print("browsing annotation")
		self.Dname = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select directory',"")
		self.label_5.setText(self.Dname)
		self.annotation_list = glob.glob('{}/*.txt'.format(self.Dname))
		annotationName = self.Dname+"/"+str(self.image_list[self.counter].split(".")[-2].split("/")[-1])+".txt"
		self.load_Annotation(annotationName)


	def load_Annotation(self,annotationName):
		global filename
		global roi_list
		load_roi = []
		roi_list =[]
		self.image_view.rect_list =[]
		self.image_view.rect_list1 =[]

		if os.path.isfile(annotationName):
			print ("File exist")
			filename = annotationName
			with open(filename) as fp:
				line = fp.readline()
				cnt = 1
				while line:
					load_roi.append([i for  i in map(float,line.strip().split(","))])
					line = fp.readline()
			roi_list = load_roi
			self.image_view.update()
		else:
			print ("File not exist")
			filename = annotationName
			self.image_view.update()
			
			


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow_exec()
    MainWindow.showMaximized()
    sys.exit(app.exec_())