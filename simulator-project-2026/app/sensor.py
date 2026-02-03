from simulatorSensor import *
from mqttConfig import MqttConfig

class Sensor(object):

	def __init__(self, id_sensor, type_, description, posX, posY, path_state1, path_state2, default_user = None):
		#Get data from mqtt config 
		config = MqttConfig()
		mqtt_data = config.get_data_mqtt()
		self.id_sensor = id_sensor
		self.type = type_
		self.description = description
		self.posX = posX
		self.posY = posY
		self.status = "OFF"
		self.agent_monitor_id = "AGENTX"

		self.interval = 5 #interval of period to generate values
		self.path_state1 = path_state1 #active state
		self.path_state2 = path_state2 #desactive state		

		if type_ == "SensorTemperature":
			self.simuMQTT = TemperatureSensor(type_, mqtt_data['host'], mqtt_data['port'], "lab1006/sensor/temperature", id_sensor, 
												self.agent_monitor_id, mqtt_data['user'], mqtt_data['password'], self.interval)
		elif type_ == "SensorHumidity":
			self.simuMQTT = HumiditySensorSensor(type_, mqtt_data['host'], mqtt_data['port'], "lab1006/sensor/humidity", id_sensor, 
												self.agent_monitor_id, mqtt_data['user'], mqtt_data['password'], self.interval)
		elif type_ == "SensorPresence":
			self.simuMQTT = PresenceSensor(type_, mqtt_data['host'], mqtt_data['port'], "lab1006/sensor/presence", id_sensor, 
												self.agent_monitor_id, mqtt_data['user'], mqtt_data['password'], self.interval, default_user)
		else:
			pass
				
			
	def set_posXY(self, posX, posY):
		self.posX = posX
		self.posY = posY

	def get_id(self):
		return self.id_sensor

	def get_id_sensor(self):
		return self.id_sensor

	def get_type(self):
		return self.type

	def get_description(self):
		return self.description

	def get_posX(self):
		return self.posX

	def get_posY(self):
		return self.posY

	def get_simulator_sensor(self):
		return self.simuMQTT	
	
	def get_status(self):
		return self.status	

	def get_path_state1(self):
		return self.path_state1

	def get_path_state2(self):
		return self.path_state2

	def set_status(self, new_status):
		self.status = new_status	

	def get_agent_monitor_id(self):
		return self.agent_monitor_id

	def set_agent_monitor_id(self, agent_id):
		self.agent_monitor_id = agent_id

	def display(self):
		print('Sensor: ', self.id_sensor, self.type, self.description)
