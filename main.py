import sys
from port import PortReader
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import pyqtgraph as pg
min_width=120
class GuiPencere(QWidget):
	def __init__(self):
		super(GuiPencere, self).__init__()

		self.resize(800,480)
		self.setWindowTitle("MPU6050")

		self.mainLayout=QHBoxLayout(self)
		self.vLayoutL=QVBoxLayout(self)
		self.vLayoutR=QVBoxLayout(self)
		self.setLayout(self.mainLayout)



		self.GBInfo=QGroupBox("Info")
		self.GBInfoLayout=QVBoxLayout(self)
		self.GBInfoLayout.setAlignment(Qt.AlignCenter,)
		self.GBInfo.setLayout(self.GBInfoLayout)
		self.GBInfo.setMaximumWidth(min_width)
		self.GBInfo.setMinimumWidth(min_width)
		self.InfoLabelText=QLabel("STATUS")
		self.InfoLabel=QLabel("durum")
		self.GBInfoLayout.addWidget(self.InfoLabelText)
		self.GBInfoLayout.addWidget(self.InfoLabel)


		self.mainLayout.addLayout(self.vLayoutL)
		self.mainLayout.addLayout(self.vLayoutR)

		self.vLayoutL.addWidget(self.GBInfo)
		self.vLayoutL.addStretch(1)


		self.plotter1=pg.PlotWidget()
		self.plotter2=pg.PlotWidget()
		self.plotter3=pg.PlotWidget()
		self.plotter4=pg.PlotWidget()

		self.plotter1.setTitle("X Axis")
		self.plotter2.setTitle("Y Axis")
		self.plotter3.setTitle("Z Axis")
		self.plotter4.setTitle("Axis Combined")

		self.plotter1.setLabel("bottom","time(sec)")
		self.plotter2.setLabel("bottom","time(sec)")
		self.plotter3.setLabel("bottom","time(sec)")
		self.plotter4.setLabel("bottom","time(sec)")

		self.vLayoutR.addWidget(self.plotter1)
		self.vLayoutR.addWidget(self.plotter2)
		self.vLayoutR.addWidget(self.plotter3)
		self.vLayoutR.addWidget(self.plotter4)

		self.plotter1_curv=pg.PlotCurveItem(pen=(1,1))
		self.plotter1.addItem(self.plotter1_curv)

		self.plotter2_curv=pg.PlotCurveItem(pen=(1,2))
		self.plotter2.addItem(self.plotter2_curv)

		self.plotter3_curv=pg.PlotCurveItem(pen=(1,3))
		self.plotter3.addItem(self.plotter3_curv)

		self.plotter4_curv1=pg.PlotCurveItem(pen=(1,1))
		self.plotter4_curv2=pg.PlotCurveItem(pen=(1,2))
		self.plotter4_curv3=pg.PlotCurveItem(pen=(1,3))
		self.plotter4.addItem(self.plotter4_curv1)
		self.plotter4.addItem(self.plotter4_curv2)
		self.plotter4.addItem(self.plotter4_curv3)

		pg.setConfigOptions(antialias=True)

		self.timer=QTimer()
		self.timer.timeout.connect(self.cycle)
		self.timer.start(33)

	def cycle(self):
		[timeArray,AcXArray,AcYArray,AcZArray] = port.takeNpArray()
		if len(timeArray)>0:
			self.plotter1_curv.setData(x=timeArray,y=AcXArray)
			self.plotter2_curv.setData(x=timeArray,y=AcYArray)
			self.plotter3_curv.setData(x=timeArray,y=AcZArray)
			self.plotter4_curv1.setData(x=timeArray,y=AcXArray)
			self.plotter4_curv2.setData(x=timeArray,y=AcYArray)
			self.plotter4_curv3.setData(x=timeArray,y=AcZArray)

if __name__=="__main__":

	if(len(sys.argv)<3):
		print("port.py com_port baud_rate")
		sys.exit(0)
	else:
		port=PortReader(sys.argv[1],sys.argv[2])

		uygulama=QApplication(sys.argv)
		pencere=GuiPencere()
		pencere.show()
		uygulama.exec_()