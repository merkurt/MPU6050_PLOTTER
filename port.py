import sys
import serial
import time
import threading
import struct
import numpy as np
from datetime import datetime

class PortReader(object):
	def __init__(self, port, baudrate):
		self.readout=list()
		self.timeArray=list()
		self.AcXArray=list()
		self.AcYArray=list()
		self.AcZArray=list()
		self.start_time=datetime.now()
		try:
			self.sp=serial.Serial(port,baudrate,timeout=0.1)
			self.sp.flush()
			self.buffer_lock=threading.Lock()
			self.thread= threading.Thread(target=self.thread_foo,args=())
			self.thread.daemon=True
			self.thread.start()
			print("it's fine")
		except Exception:
			print("Serial port can't open!")
			sys.exit(0)

	def clear_array(self):
		self.buffer_lock.acquire()
		self.start_time=datetime.now()
		self.timeArray = []
		self.AcXArray = []
		self.AcYArray = []
		self.AcZArray = []
		self.buffer_lock.release()

	def thread_foo(self):
		time.sleep(1)

		while self.sp.isOpen()==True:
			
			self.buffer_lock.acquire()
			buff = self.sp.readline().split(b"/")
			
			if(len(buff)==3):
				AcX=int(buff[0])
				AcY=int(buff[1])
				AcZ=int(buff[2])

				time_now=datetime.now()
				timeCounter= (time_now-self.start_time).total_seconds()


				self.readout=[timeCounter,AcX,AcY,AcZ]

				self.timeArray=np.append(self.timeArray,timeCounter)
				self.AcXArray=np.append(self.AcXArray,AcX)
				self.AcYArray=np.append(self.AcYArray,AcY)
				self.AcZArray=np.append(self.AcZArray,AcZ)


			self.buffer_lock.release()

			time.sleep(0.01)


	def takeReadout(self):
		self.buffer_lock.acquire()
		back= self.readout
		self.buffer_lock.release()
		return back

	def takeNpArray(self):
		self.buffer_lock.acquire()
		back = [self.timeArray,self.AcXArray,self.AcYArray,self.AcZArray]
		self.buffer_lock.release()
		return back

	def close_PortReader(self):
		self.sp.close()

if __name__=="__main__":

	if(len(sys.argv)<3):
		print("port.py com_port baud_rate")
		sys.exit(0)
	else:
		pr=PortReader(sys.argv[1],sys.argv[2])

		while 1:
			
			time.sleep(0.1)
			print(pr.takeReadout())
			