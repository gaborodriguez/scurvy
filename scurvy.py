import sys
import random


from PySide2.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QMainWindow, QWidget
from PySide2.QtCore import Qt, QSize, QRect
from PySide2.QtGui import QPainter, QPen


class RenderWidget(QWidget):
	def __init__(self):
		super().__init__()
		self.points = [] # creates a new empty list for each widget

	def paintEvent(self, event):
		painter = QPainter(self)
		painter.setRenderHint(QPainter.Antialiasing, True);

		pen = QPen(Qt.darkBlue, 10, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin);
		painter.setPen(pen);

		for pt in range(1, len(self.points)):
			painter.drawLine(self.points[pt-1][0], self.points[pt-1][1], self.points[pt][0], self.points[pt][1])

		pen = QPen(Qt.darkRed, 20, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin);
		painter.setPen(pen);

		for pt in range(0, len(self.points)):
			painter.drawEllipse(self.points[pt][0] - 10, self.points[pt][1] - 10, 20, 20)

	def mousePressEvent(self, event) :
		self.selectedPoint = self.findPoint(event.pos().x(), event.pos().y())
		if(self.selectedPoint == -1) :
			self.addPoint(event.pos().x(), event.pos().y())
		elif(event.button() == Qt.RightButton) :
			self.removePoint(self.selectedPoint)
		QWidget.update(self)

	def mouseMoveEvent(self, event) :
		if(self.selectedPoint != -1) :
			self.points[self.selectedPoint] = [event.pos().x(), event.pos().y()]
			QWidget.update(self)
			

	######################
	# POINTS
	def addPoint(self, x, y) :
		self.points.append([x, y])

	def clearPoints(self) :
		self.points = []
		QWidget.update(self)

	def removePoint(self, index) :
		del(self.points[index])

	def findPoint(self, x, y) :
		for i in range(len(self.points)) :
			if(abs(self.points[i][0] - x) < 20 and abs(self.points[i][1] - y) < 20) :
				return i
		return -1
	######################

	


app = QApplication(sys.argv)
mainWindow = QMainWindow()
mainWidget = QWidget()

renderAreaWidget = RenderWidget()

layout = QVBoxLayout()

def newPoint() :
	renderAreaWidget.addPoint(random.randint(0, 200), random.randint(0, 200))

resetButton = QPushButton("Reset")
resetButton.clicked.connect(renderAreaWidget.clearPoints)

layout.addWidget(resetButton)

layout.addWidget(renderAreaWidget)

mainWidget.setLayout(layout)

mainWindow.setCentralWidget(mainWidget)
mainWindow.setFixedSize(1600, 1200)
mainWindow.show()
app.exec_()
