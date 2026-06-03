from sensor import Sensor
from asset import Asset
from user import User

class TestData(object):	

	def get_data_sensors(self):
		listSensors = []
		listSensors.append(Sensor('sensor_temperature1', 'SensorTemperature', 'no description', 171.0, 152.0,
													 "media/sensor/sensor_on.png", "media/sensor/sensor_off.png"))
		listSensors.append(Sensor('sensor_temperature2', 'SensorTemperature', 'no description', 358.0, 152.0,
													 "media/sensor/sensor_on.png", "media/sensor/sensor_off.png"))
		listSensors.append(Sensor('sensor_temperature3', 'SensorTemperature', 'no description', 543.0, 152.0,
													 "media/sensor/sensor_on.png", "media/sensor/sensor_off.png"))

		listSensors.append(Sensor('sensor_temperature4', 'SensorTemperature', 'no description', 195.0, 269.0,
													 "media/sensor/sensor_on.png", "media/sensor/sensor_off.png"))
		listSensors.append(Sensor('sensor_temperature5', 'SensorTemperature', 'no description', 714.0, 269.0,
													 "media/sensor/sensor_on.png", "media/sensor/sensor_off.png"))

		listSensors.append(Sensor('sensor_temperature6', 'SensorTemperature', 'no description', 195.0, 470.0,
													 "media/sensor/sensor_on.png", "media/sensor/sensor_off.png"))
		listSensors.append(Sensor('sensor_temperature7', 'SensorTemperature', 'no description', 714.0, 470.0,
													 "media/sensor/sensor_on.png", "media/sensor/sensor_off.png"))

		default_user = User('user_default', 'unknowing', 'no description', 0, 0, "media/user/user_unknowing.png")	
	
		listSensors.append(Sensor('sensor_presence1', 'SensorPresence', 'no description', 920.0, 115.00,
													 "media/sensor/sensor_on.png", "media/sensor/sensor_off.png", default_user))		
		listSensors.append(Sensor('sensor_presence2', 'SensorPresence', 'no description', 740.0, 150.00,
													 "media/sensor/sensor_on.png", "media/sensor/sensor_off.png", default_user))

		listSensors.append(Sensor('sensor_temperature_outside', 'SensorTemperature', 'no description', 930.0, 640.0,
													 "media/sensor/sensor_on.png", "media/sensor/sensor_off.png"))

		
		return listSensors

	def get_data_assets(self):
		listAssets = []

		listAssets.append(Asset('asset_lamp1', 'AssetLamp', 'no description', 37.0, 107.0, 
											"media/asset/asset_lamp_rotate_on.png", "media/asset/asset_lamp_rotate_off.png"))
		listAssets.append(Asset('asset_lamp2', 'AssetLamp', 'no description', 300.0, 107.0, 
											"media/asset/asset_lamp_rotate_on.png", "media/asset/asset_lamp_rotate_off.png"))
		listAssets.append(Asset('asset_lamp3', 'AssetLamp', 'no description', 560.0, 107.0, 
											"media/asset/asset_lamp_rotate_on.png", "media/asset/asset_lamp_rotate_off.png"))

		listAssets.append(Asset('asset_lamp4', 'AssetLamp', 'no description', 61.0, 188.0, 
											"media/asset/asset_lamp_on.png", "media/asset/asset_lamp_off.png"))
		listAssets.append(Asset('asset_lamp5', 'AssetLamp', 'no description', 313.0, 188.0, 
											"media/asset/asset_lamp_on.png", "media/asset/asset_lamp_off.png"))
		listAssets.append(Asset('asset_lamp6', 'AssetLamp', 'no description', 566.0, 188.0, 
											"media/asset/asset_lamp_on.png", "media/asset/asset_lamp_off.png"))
		listAssets.append(Asset('asset_lamp7', 'AssetLamp', 'no description', 818.0, 188.0, 
											"media/asset/asset_lamp_on.png", "media/asset/asset_lamp_off.png"))

		listAssets.append(Asset('asset_lamp8', 'AssetLamp', 'no description', 131.0, 310.0, 
											"media/asset/asset_lamp_on.png", "media/asset/asset_lamp_off.png"))
		listAssets.append(Asset('asset_lamp9', 'AssetLamp', 'no description', 383.0, 310.0, 
											"media/asset/asset_lamp_on.png", "media/asset/asset_lamp_off.png"))
		listAssets.append(Asset('asset_lamp10', 'AssetLamp', 'no description', 636.0, 310.0, 
											"media/asset/asset_lamp_on.png", "media/asset/asset_lamp_off.png"))
		listAssets.append(Asset('asset_lamp11', 'AssetLamp', 'no description', 888.0, 310.0, 
											"media/asset/asset_lamp_on.png", "media/asset/asset_lamp_off.png"))

		listAssets.append(Asset('asset_lamp12', 'AssetLamp', 'no description', 61.0, 443.0, 
											"media/asset/asset_lamp_on.png", "media/asset/asset_lamp_off.png"))
		listAssets.append(Asset('asset_lamp13', 'AssetLamp', 'no description', 313.0, 443.0, 
											"media/asset/asset_lamp_on.png", "media/asset/asset_lamp_off.png"))
		listAssets.append(Asset('asset_lamp14', 'AssetLamp', 'no description', 566.0, 443.0, 
											"media/asset/asset_lamp_on.png", "media/asset/asset_lamp_off.png"))
		listAssets.append(Asset('asset_lamp15', 'AssetLamp', 'no description', 818.0, 443.0, 
											"media/asset/asset_lamp_on.png", "media/asset/asset_lamp_off.png"))


		listAssets.append(Asset('asset_door_datacenter', "AssetDoor", "no description", 621.0, 166.50, 
											"media/asset/asset_door_datacenter_open.png", "media/asset/asset_door_datacenter_close.png" ))

		listAssets.append(Asset('asset_door_lab1006', "AssetDoor", "no description", 736.0, 2.50, 
											"media/asset/asset_door_lab1006_open.png", "media/asset/asset_door_lab1006_close.png" ))
		

		listAssets.append(Asset('asset_window1', 'AssetWindow', 'no description', 10.0, 595.5,
											"media/asset/asset_window_open.png", "media/asset/asset_window_close.png"))
		listAssets.append(Asset('asset_window2', 'AssetWindow', 'no description', 114.0, 595.5, 
											"media/asset/asset_window_open.png", "media/asset/asset_window_close.png"))
		listAssets.append(Asset('asset_window3', 'AssetWindow', 'no description', 219.0, 595.5, 
											"media/asset/asset_window_open.png", "media/asset/asset_window_close.png"))
		listAssets.append(Asset('asset_window4', 'AssetWindow', 'no description', 323.0, 595.5, 
											"media/asset/asset_window_open.png", "media/asset/asset_window_close.png"))
		listAssets.append(Asset('asset_window5', 'AssetWindow', 'no description', 428.0, 595.5, 
											"media/asset/asset_window_open.png", "media/asset/asset_window_close.png"))
		listAssets.append(Asset('asset_window6', 'AssetWindow', 'no description', 532.0, 595.5, 
											"media/asset/asset_window_open.png", "media/asset/asset_window_close.png"))
		listAssets.append(Asset('asset_window7', 'AssetWindow', 'no description', 637.0, 595.5, 
											"media/asset/asset_window_open.png", "media/asset/asset_window_close.png"))
		listAssets.append(Asset('asset_window8', 'AssetWindow', 'no description', 741.0, 595.5, 
											"media/asset/asset_window_open.png", "media/asset/asset_window_close.png"))
		listAssets.append(Asset('asset_window9', 'AssetWindow', 'no description', 845.0, 595.5, 
											"media/asset/asset_window_open.png", "media/asset/asset_window_close.png"))

		listAssets.append(Asset('asset_aircond1', 'AssetAirConditioning', 'no description', 118.0, 13.0, 
											"media/asset/asset_aircond_rotate_on.png", "media/asset/asset_aircond_rotate_off.png"))
		listAssets.append(Asset('asset_aircond2', 'AssetAirConditioning', 'no description', 304.0, 13.0, 
											"media/asset/asset_aircond_rotate_on.png", "media/asset/asset_aircond_rotate_off.png"))
		listAssets.append(Asset('asset_aircond3', 'AssetAirConditioning', 'no description', 478.0, 13.0, 
											"media/asset/asset_aircond_rotate_on.png", "media/asset/asset_aircond_rotate_off.png"))

		listAssets.append(Asset('asset_aircond4', 'AssetAirConditioning', 'no description', 188.0, 544, 
											"media/asset/asset_aircond_on.png", "media/asset/asset_aircond_off.png"))
		listAssets.append(Asset('asset_aircond5', 'AssetAirConditioning', 'no description', 647.0, 544, 
											"media/asset/asset_aircond_on.png", "media/asset/asset_aircond_off.png"))

		listAssets.append(Asset('asset_heat1', 'AssetHeat', 'no description', 456.0, 562.0,
											"media/asset/asset_heat_on.png", "media/asset/asset_heat_off.png"))

		listAssets.append(Asset('asset_datacenter1', 'AssetDatacenter', 'Datacenter 1 (14 racks)', 150.0, 70.0,
										"media/asset/asset_datacenter_on.png", "media/asset/asset_datacenter_off.png"))
		listAssets.append(Asset('asset_datacenter2', 'AssetDatacenter', 'Datacenter 2 (14 racks)', 320.0, 70.0,
										"media/asset/asset_datacenter_on.png", "media/asset/asset_datacenter_off.png"))
		listAssets.append(Asset('asset_datacenter3', 'AssetDatacenter', 'Datacenter 3 (14 racks)', 490.0, 70.0,
										"media/asset/asset_datacenter_on.png", "media/asset/asset_datacenter_off.png"))

		return listAssets

	def get_data_users(self):
		listUsers = []
		listUsers.append(User('user_professor1', 'professor', 'no description', 188.0, 544, "media/user/user_professor.png"))
		listUsers.append(User('user_postgraduate1', 'student_postgraduate', 'no description', 188.0, 544, "media/user/user_student_postgraduate.png"))
		listUsers.append(User('user_underground1', 'student_underground', 'no description', 188.0, 544, "media/user/user_student_underground.png"))
		listUsers.append(User('user_unknowing1', 'unknowing', 'no description', 188.0, 544, "media/user/user_unknowing.png"))

		return listUsers



		