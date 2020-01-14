from plyer import accelerometer
from kivy.clock import Clock

from rockcomm.datasave import Data

class myAccelerometer():
	"""
	Object base on plyer accelerometer class
	dt is the wanted intervall between 2 measurments in miliseconds
	Implemented a method to pick data at an define intervall dt
	Enable and Disable methods are already implemented
	"""
	dt=25
	def __init__(self,dt=None,server=None):
		if dt != None:
			self.dt= dt
		self.server = server
		event = None
	def running(self,sever=None):
		'''
		when call start accelerometer and pick data at the intervall dt
		precise server in wich data as to be send (sever as an object with func send)
		if server nor precised data will be printed in the console
		'''
		accelerometer.enable()
		self.event=Clock.schedule_interval(self.pick_data,self.dt/1000)

	def pick_data(self,dt):
		'''
		pick data and send it to precised server
		if server not precised data will be printed

		WARNING: accelerometer as to be enable before picking data
		'''
		data=Data('acceleration',accelerometer.acceleration)
		if self.server != None:
			self.server.sendData(data)

	def kill(self):
		'''
		function call to kill the current running
		'''
		if self.event != None:
			self.event.cancel()
		accelerometer.disable()
