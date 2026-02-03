class MqttConfig:
    def __init__(self):
        self.mqtt_data = {
            "user": "lasdpc",
            "password": "l@sdpC10",
            "host": "andromeda.lasdpc.icmc.usp.br",
            "port": 6183
        }
        
    def get_data_mqtt(self):
        return self.mqtt_data