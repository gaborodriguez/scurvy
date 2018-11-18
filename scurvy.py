import sys
import numpy as np

from PySide2.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QMainWindow, QWidget
from PySide2.QtCore import Qt, QSize, QRect
from PySide2.QtGui import QPainter, QPen

def interpolate(p0, p1, t) :
	return p0 + (p1 - p0) * t

def hermiteInterpolate(p0, p1, t) :
	s = np.array([t*t*t, t*t, t, 1])
	
	# Copy
	h1 =  2 * s[0] - 3 * s[1] + 1
	h2 = -2 * s[0] + 3 * s[1]
	h3 =      s[0] - 2 * s[1]   + s[2];
	h4 =      s[0] -     s[1]

	tan0 = np.array([200, 0])
	tan1 = np.array([200, 0])
	
	return h1*p0 + h2*p1 + h3*tan0 + h4 * tan1

class RenderWidget(QWidget):
	def __init__(self):
		super().__init__()
		self.points = []
		
	def paintEvent(self, event):
		painter = QPainter(self)
		painter.setRenderHint(QPainter.Antialiasing, True);

		pen = QPen(Qt.darkBlue, 3, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin);
		painter.setPen(pen);
		
		numberOfSegments = 100

		for pt in range(1, len(self.points)) :
			previousPoint = self.points[pt-1]
			for seg in range(numberOfSegments) :
				point = hermiteInterpolate(self.points[pt-1], self.points[pt], (seg + 1) / numberOfSegments)
				painter.drawLine(previousPoint[0], previousPoint[1], point[0], point[1])
				previousPoint = point

		pen = QPen(Qt.darkRed, 3, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin);
		painter.setPen(pen);

		for pt in range(0, len(self.points)):
			painter.drawEllipse(self.points[pt][0] - 3, self.points[pt][1] - 3, 6, 6)


	def mousePressEvent(self, event) :
		self.selectedPoint = self.findPoint(event.pos().x(), event.pos().y())
		if(self.selectedPoint == -1) :
			self.addPoint(event.pos().x(), event.pos().y())
		elif(event.button() == Qt.RightButton) :
			self.removePoint(self.selectedPoint)
		QWidget.update(self)

	def mouseMoveEvent(self, event) :
		if(self.selectedPoint != -1) :
			self.points[self.selectedPoint] = np.array([event.pos().x(), event.pos().y()])
			QWidget.update(self)
			

	######################
	# POINTS
	def addPoint(self, x, y) :
		self.points.append(np.array([x, y]))

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

resetButton = QPushButton("Reset")
resetButton.clicked.connect(renderAreaWidget.clearPoints)

layout.addWidget(resetButton)

layout.addWidget(renderAreaWidget)

mainWidget.setLayout(layout)

mainWindow.setCentralWidget(mainWidget)
mainWindow.setFixedSize(800, 600)
mainWindow.show()
app.exec_()
