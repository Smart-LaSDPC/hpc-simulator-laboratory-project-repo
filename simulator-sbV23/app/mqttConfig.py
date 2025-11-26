class MqttConfig:
    def __init__(self):
        self.mqtt_data = {
            "user": "",
            "password": "",
            "host": "127.0.0.1",
            "port": 1883
        }
        
    def get_data_mqtt(self):
        return self.mqtt_data