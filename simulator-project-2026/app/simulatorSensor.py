import json
import random
import threading
import time
from datetime import datetime

import paho.mqtt.client as mqtt


class SensorSimulator:
    def __init__(
        self,
        sensor_type,
        broker,
        port,
        topic_base,
        sensor_id,
        agent_monitor_id,
        username,
        password,
        interval=5,
        user_object=None,
    ):
        self.sensor_id = sensor_id
        self.sensor_type = sensor_type
        self.broker = broker
        self.port = port
        self.topic = f"{topic_base}/{sensor_type}"
        self.interval = interval
        self.client_id = f"{sensor_type}-sensor-{random.randint(0, 1000)}"
        self.client = mqtt.Client(self.client_id)
        self.mqtt_username = username
        self.mqtt_password = password
        self.stop_event = threading.Event()
        self.thread = None
        self.agent_monitor_id = agent_monitor_id
        self.user_object = user_object  # Only to presence sensor

    def connect(self):
        if self.mqtt_username and self.mqtt_password:
            self.client.username_pw_set(self.mqtt_username, self.mqtt_password)
        self.client.connect(self.broker, self.port)
        self.client.loop_start()

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()

    def simulate_reading(self):
        raise NotImplementedError("Must be implemented by subclass")

    def change_reading(self, new_value, new_user):
        raise NotImplementedError("Must be implemented by subclass")

    def change_agent_monitor(self, new_agent_id):
        self.agent_monitor_id = new_agent_id

    def publish_reading(self):
        while not self.stop_event.is_set():
            reading = self.simulate_reading()
            now = datetime.now()
            date_time = now.strftime("%m/%d/%Y %H:%M:%S")

            # Create the payload as a dictionary
            payload_dict = {
                "type": self.sensor_type,
                "id": self.sensor_id,
                "mqtt_client_id": self.client_id,
                "agent_monitor_id": self.agent_monitor_id,
                "sensed_value": reading,
                "date_time": date_time,
            }

            # Add presence information if the sensor type is "presence" and user_object is not None
            if self.sensor_type == "presence" and self.user_object is not None:
                # Assuming user_object.get_valuesInJson() returns a dictionary
                payload_dict["presence"] = self.user_object.get_valuesInJson()

            # Convert the dictionary to a JSON string
            payload = json.dumps(payload_dict)

            # Publish the payload
            self.client.publish(self.topic, payload)
            print(f"Published: {payload}")

            # Wait for the next interval
            time.sleep(self.interval)

    def start(self):
        if self.thread and self.thread.is_alive():
            self.stop()

        self.stop_event.clear()
        self.thread = threading.Thread(target=self.publish_reading)
        self.connect()
        self.thread.start()

    def stop(self):
        self.stop_event.set()
        if self.thread:
            self.thread.join()
        self.disconnect()
        self.agent_monitor_id = "AGENTX"

    def get_statusONOFF(self):
        if self.thread and self.thread.is_alive():
            print("ON")
        else:
            print("OFF")


class TemperatureSensor(SensorSimulator):
    def __init__(
        self,
        type,
        broker,
        port,
        topic_base,
        sensor_id,
        agent_id,
        mqtt_username,
        mqtt_password,
        interval=5,
    ):
        super().__init__(
            type,
            broker,
            port,
            topic_base,
            sensor_id,
            agent_id,
            mqtt_username,
            mqtt_password,
            int(interval),
        )
        self._external_value = None

    def set_external_value(self, value):
        """Called from TemperatureSim to have the real value"""
        self._external_value = value

    def simulate_reading(self):
        if self._external_value is not None:
            return round(self._external_value, 2)
        return round(random.uniform(20.0, 30.0), 2)

    def change_reading(self, new_value, new_user=None):
        self._external_value = new_value


class HumiditySensor(SensorSimulator):
    def __init__(
        self,
        type,
        broker,
        port,
        topic_base,
        sensor_id,
        agent_id,
        mqtt_username,
        mqtt_password,
        interval=5,
    ):
        super().__init__(
            type,
            broker,
            port,
            topic_base,
            sensor_id,
            agent_id,
            mqtt_username,
            mqtt_password,
            int(interval),
        )

    def simulate_reading(self):
        return round(random.uniform(30.0, 70.0), 2)

    def change_reading(self, new_value, new_user):
        pass


class PresenceSensor(SensorSimulator):
    def __init__(
        self,
        type,
        broker,
        port,
        topic_base,
        sensor_id,
        agent_id,
        mqtt_username,
        mqtt_password,
        interval=5,
        defaultUser=None,
    ):
        super().__init__(
            type,
            broker,
            port,
            topic_base,
            sensor_id,
            agent_id,
            mqtt_username,
            mqtt_password,
            int(interval),
            defaultUser,
        )
        self.value = 0

    def simulate_reading(self):
        return self.value

    def change_reading(self, new_value, new_user):
        self.value = new_value
        self.user_object = new_user


def main():
    broker = "127.0.0.1"
    port = 1883
    topic_base = "home/sensor"

    temperature_sensor = TemperatureSensor(
        broker, port, topic_base, "sensor_0", "AGENTX"
    )
    humidity_sensor = HumiditySensor(broker, port, topic_base, "sensor_1", "AGENTX")

    try:
        temperature_sensor.start()
        humidity_sensor.start()

        # Run for a certain amount of time (e.g., 30 seconds) for demonstration
        time.sleep(30)

        # Restart the sensors to demonstrate multiple starts
        print("Restarting sensors...")
        temperature_sensor.start()
        humidity_sensor.start()

        # Run for another period of time
        time.sleep(30)

    except KeyboardInterrupt:
        print("Simulation interrupted.")
    finally:
        # Stop the sensors
        temperature_sensor.stop()
        humidity_sensor.stop()
        print("Simulation stopped.")


if __name__ == "__main__":
    main()
