import sys,csv,os
from PyQt5 import QtCore, QtGui, QtWidgets
from gui import Ui_MainWindow
roi_list = []
if os.path.exists("roi.csv"):
	with open('roi.csv','r')as f:
		data = csv.reader(f)
		for row in data:
			roi_list.append(row)

def clear_roi():
	del roi_list[:]	
main_var = ''
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
	    

	def load_prev_box(self,qp):
		for brc in roi_list:
			qp.drawRect(QtCore.QRect(QtCore.QPoint(int(brc[0]),int(brc[1])),QtCore.QPoint(int(brc[2]), int(brc[3]))))
		

	def clear_boxes(self):
		self.rect_state=0
		self.rect_list = []
		self.rect_list1 = []
		filename = "roi.csv"
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
		with open('roi.csv', 'a+') as writeFile:
			writer = csv.writer(writeFile)
			writer.writerows([roi_list_temp])
			self.update()

class MainWindow_exec(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.u = 0
        self.v = 0
        global roi_list
        #print(roi_list)
        self.setupUi(self)
        print("*"*40,self.image_view.height(),self.image_view.width())
        self.gridLayout_4.removeWidget(self.image_view)
        self.image_view.close()
        self.image_view = MyWidget()
        self.image_view.setStyleSheet("border: 10px solid black;")
        self.gridLayout_4.addWidget(self.image_view,0,1,1,1)
        pix = QtGui.QPixmap(str("/home/ratan/Downloads/Screenshot_20191208_210211.png"))
        global main_var 
        main_var = pix
        self.image_view.setMinimumSize(200,200)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow_exec()
    MainWindow.showMaximized()
    sys.exit(app.exec_())