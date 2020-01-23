import sys
import port_lister
from port import PortReader
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import pyqtgraph as pg
min_width=120
serial_port_list=list()
baud_rate_list=["110", "300", "600", "1200", "2400", "4800", "9600", "14400", "19200", "38400", "57600", "115200", "128000", " 256000"]
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
		self.GBInfo.setAlignment(Qt.AlignCenter)
		self.GBInfoLayout=QVBoxLayout(self)
		self.GBInfoLayout.setAlignment(Qt.AlignCenter)
		self.GBInfo.setLayout(self.GBInfoLayout)
		self.GBInfo.setMaximumWidth(min_width)
		self.GBInfo.setMinimumWidth(min_width)
		self.InfoLabelText=QLabel("STATUS")
		self.InfoLabel=QLabel("<b>durum</b>")
		self.InfoLabel.setAlignment(Qt.AlignCenter)
		self.GBInfoLayout.addWidget(self.InfoLabelText)
		self.GBInfoLayout.addWidget(self.InfoLabel)

		self.GBSerial=QGroupBox("Serial Settings")
		self.GBSerial.setAlignment(Qt.AlignCenter)
		self.GBSerialLayout=QVBoxLayout(self)
		self.GBSerial.setLayout(self.GBSerialLayout)
		self.GBSerial.setMaximumWidth(min_width)
		self.GBSerial.setMinimumWidth(min_width)
		self.SerialPortCombo=QComboBox()
		self.SerialPortCombo.addItems(get_port_list())
		self.SerialBaudrateCombo=QComboBox()
		self.SerialBaudrateCombo.addItems(baud_rate_list)
		self.SerialBaudrateCombo.setCurrentIndex(11)
		self.SerialRefreshButon=QPushButton("REFRESH")
		self.SerialRefreshButon.clicked.connect(self.port_list_update)
		self.GBSerialLayout.addWidget(self.SerialPortCombo)
		self.GBSerialLayout.addWidget(self.SerialBaudrateCombo)
		self.GBSerialLayout.addWidget(self.SerialRefreshButon)

		self.GBClear=QGroupBox("Data")
		self.GBClear.setAlignment(Qt.AlignCenter)
		self.GBClearLayout=QVBoxLayout(self)
		self.GBClear.setLayout(self.GBClearLayout)
		self.GBClear.setMaximumWidth(min_width)
		self.GBClear.setMinimumWidth(min_width)
		self.ClearButon=QPushButton("CLEAR")
		self.GBClearLayout.addWidget(self.ClearButon)




		self.mainLayout.addLayout(self.vLayoutL)
		self.mainLayout.addLayout(self.vLayoutR)

		self.vLayoutL.addWidget(self.GBInfo)
		self.vLayoutL.addWidget(self.GBSerial)
		self.vLayoutL.addWidget(self.GBClear)
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

		#self.timer=QTimer()
		#self.timer.timeout.connect(self.cycle)
		#self.timer.start(33)

	def cycle(self):
		[timeArray,AcXArray,AcYArray,AcZArray] = port.takeNpArray()
		if len(timeArray)>0:
			self.plotter1_curv.setData(x=timeArray,y=AcXArray)
			self.plotter2_curv.setData(x=timeArray,y=AcYArray)
			self.plotter3_curv.setData(x=timeArray,y=AcZArray)
			self.plotter4_curv1.setData(x=timeArray,y=AcXArray)
			self.plotter4_curv2.setData(x=timeArray,y=AcYArray)
			self.plotter4_curv3.setData(x=timeArray,y=AcZArray)

	def port_list_update(self):
		self.SerialPortCombo.clear()
		self.SerialPortCombo.addItems(get_port_list())


def get_port_list():
	return port_lister.serial_ports()

if __name__=="__main__":

	
	

	uygulama=QApplication(sys.argv)
	pencere=GuiPencere()
	pencere.show()
	uygulama.exec_()
	port=PortReader(sys.argv[1],sys.argv[2])