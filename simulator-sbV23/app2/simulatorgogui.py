import sys
import paho.mqtt.client as mqtt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QListWidget, QListWidgetItem

MQTT_HOST = "192.3.239.200"
MQTT_PORT = 1883
MQTT_USER = "lasdpc"
MQTT_PASSWORD = "lasdpc"

class SensorGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

        self.sensor_data = {}

        # Main layout
        self.layout = QVBoxLayout(self)

        # Create Sensor button
        self.create_button = QPushButton("Create New Sensor", self)
        self.create_button.clicked.connect(self.create_sensor)
        self.layout.addWidget(self.create_button)

        # Turn Off Selected Sensor button
        self.turn_off_button = QPushButton("Turn Off Selected", self)
        self.turn_off_button.clicked.connect(self.turn_off_selected_sensor)
        self.layout.addWidget(self.turn_off_button)

        # List widget for displaying sensors
        self.sensor_list = QListWidget(self)
        self.layout.addWidget(self.sensor_list)

        # Table widget for displaying sensor data
        self.table = QTableWidget(self)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Sensor ID", "Client ID", "Temperature"])
        self.layout.addWidget(self.table)

        # Set up MQTT client
        self.client = mqtt.Client()
        self.client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(MQTT_HOST, MQTT_PORT, 60)  # Connect to the MQTT broker

        self.client.loop_start()  # Start the MQTT loop

    def initUI(self):
        self.setWindowTitle('Sensor Simulator GUI')
        self.setGeometry(100, 100, 600, 400)

    def on_connect(self, client, userdata, flags, rc):
        print("Connected to MQTT Broker")
        client.subscribe("sensors/temperature/#")  # Subscribe to all sensor topics

    def on_message(self, client, userdata, msg):
        payload = msg.payload.decode()
        print(f"Received message: {payload}")
        sensor_data = eval(payload)  # Convert string payload to dictionary
        sensor_id = sensor_data['sensor_id']
        temperature = sensor_data['temperature']
        client_id = f"sensor-{sensor_id}"  # Assume client ID is "sensor-<sensor_id>"

        if sensor_id in self.sensor_data:
            # Update the existing row
            row = self.sensor_data[sensor_id]['row']
            self.table.setItem(row, 2, QTableWidgetItem(f"{temperature}°C"))
        else:
            # Add a new row to the table
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(str(sensor_id)))
            self.table.setItem(row_position, 1, QTableWidgetItem(client_id))
            self.table.setItem(row_position, 2, QTableWidgetItem(f"{temperature}°C"))

            # Add sensor to the list widget
            list_item = QListWidgetItem(f"Sensor {sensor_id} - {client_id}")
            self.sensor_list.addItem(list_item)

            # Store sensor data (row in table and list item)
            self.sensor_data[sensor_id] = {'row': row_position, 'list_item': list_item}

    def create_sensor(self):
        self.client.publish("sensors/create", "Create")  # Publish a message to create a new sensor

    def turn_off_selected_sensor(self):
        selected_items = self.sensor_list.selectedItems()
        if selected_items:
            selected_item = selected_items[0]
            for sensor_id, data in self.sensor_data.items():
                if data['list_item'] == selected_item:
                    # Publish a message to the specific sensor's topic to turn it off
                    topic = f"sensors/turnoff/{sensor_id}"
                    self.client.publish(topic, "Turn Off")
                    print(f"Turn Off command sent to sensor {sensor_id}")

                    # Remove the sensor from the table and list widget
                    self.table.removeRow(data['row'])
                    self.sensor_list.takeItem(self.sensor_list.row(selected_item))
                    del self.sensor_data[sensor_id]
                    break


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SensorGUI()
    ex.show()
    sys.exit(app.exec_())
