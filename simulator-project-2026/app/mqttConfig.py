class MqttConfig:
    def __init__(self):
        self.mqtt_data = {
            "user": "mqtt",
            "password": "lasdpc",
            "host": "localhost",
            "port": 1883
        }
        
    def get_data_mqtt(self):
        return self.mqtt_data