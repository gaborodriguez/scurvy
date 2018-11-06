import sys

from PySide2.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QMainWindow, QWidget
from PySide2.QtCore import QSize, QRect
from PySide2.QtGui import QPainter

class RenderWidget(QWidget):
	def __init__(self):
		super().__init__()
		self.points = [] # creates a new empty list for each widget

	def paintEvent(self, event):
		rect = QRect(1, 0, 1, 150)
		currentSize = self.size()
		painter = QPainter(self)
		painter.setRenderHint(QPainter.Antialiasing, True);
		painter.drawLine(0, 0, currentSize.width(), currentSize.height())

	def addPoint(self, x, y) :
		self.points.append([x, y])

	def clearPoints(self) :
		self.points = []


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
mainWindow.setFixedSize(1600, 1200)
mainWindow.show()
app.exec_()
