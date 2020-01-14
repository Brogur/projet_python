'''
To Do:
	-define dt widget
	-change sensor server when connect
	-ask alexandre datasender to use?
	-add popup when connection error and stay at connection layout
'''

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

from datasend_Socket.DataSender import DatasendSocket

import Sensors.accelerometer as Accelerometer
from rockcomm.datasave import Data

accelerometer=Accelerometer.myAccelerometer()



class MyApp(App):
	def build(self):
		return Window()

class Window(GridLayout):

	def __init__(self):
		super(Window,self).__init__()
		self.cols=1
		self.current=ConnectionLayout(self)
		self.add_widget(self.current)

		
class ConnectionLayout(GridLayout):
	def __init__(self,upper_grid):
		super(ConnectionLayout,self).__init__()
		self.upper_grid=upper_grid
		
		self.cols=1

		self.state=Label(text="unconnected",font_size=50)
		self.add_widget(self.state)

		self.subgrid=GridLayout()
		self.subgrid.cols = 2 

		self.subgrid.add_widget(Label(text="Adresse IP: "))
		self.ip = TextInput(multiline=False)
		self.subgrid.add_widget(self.ip)

		self.subgrid.add_widget(Label(text="Port: "))
		self.port = TextInput(multiline=False)
		self.subgrid.add_widget(self.port)

		self.add_widget(self.subgrid)

		self.connect= Button(text ="connection")
		self.connect.bind(on_press=self.Trigerred)
		self.add_widget(self.connect)

	def Trigerred(self, instance):
		ip=self.ip.text
		port=self.port.text
		self.upper_grid.remove_widget(self.upper_grid.current)
		self.upper_grid.s=DatasendSocket(ip,int(port))
		self.upper_grid.current=InUseLayout(self.upper_grid)
		self.upper_grid.add_widget(self.upper_grid.current)

class InUseLayout(GridLayout):
	def __init__(self,upper_grid):
		self.upper_grid=upper_grid
		super(InUseLayout,self).__init__()
		self.cols=1

		self.state=Label(text="connected",font_size=50)
		self.add_widget(self.state)

		self.subgrid=GridLayout()
		self.subgrid.cols = 2 


		self.subgrid.add_widget(Label(text="Accelerometer"))

		self.send_data= TextInput(multiline=False)
		self.add_widget(self.send_data)
		self.envoie=Button(text='envoyer')
		self.envoie.bind(on_press=self.envoyer)
		self.add_widget(self.envoie)

		self.acc_activ_but = Button(text="OFF")
		self.acc_state=False
		self.acc_activ_but.bind(on_press=self.acc_activation)
		self.subgrid.add_widget(self.acc_activ_but)


		self.add_widget(self.subgrid)

		self.connect= Button(text ="disconnect")
		self.connect.bind(on_press=self.Trigerred)
		self.add_widget(self.connect)

	def Trigerred(self, instance):
		self.upper_grid.s.kill()
		self.upper_grid.remove_widget(self.upper_grid.current)
		self.upper_grid.current=ConnectionLayout(self.upper_grid)
		self.upper_grid.add_widget(self.upper_grid.current)

	def acc_activation(self, instance):
		if self.acc_state:
			self.acc_state = False
			accelerometer.kill()
			self.acc_activ_but.text= "OFF"

		else:
			self.acc_state = True
			accelerometer.running()
			self.acc_activ_but.text= "ON"

	def envoyer(self,instance):
		data=Data('acc',self.send_data.text)
		self.upper_grid.s.sendData(data)
		
if __name__ == "__main__":
	MyApp().run()
