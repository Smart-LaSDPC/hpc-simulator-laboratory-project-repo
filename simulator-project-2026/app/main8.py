import datetime
import json

import paho.mqtt.client as mqtt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Q_ARG, QMetaObject, QObject, QPointF, Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QAction,
    QComboBox,
    QGraphicsPixmapItem,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QToolBar,
)

from addAssetWindow import Ui_createAssetWindow
from addSensorWindow import Ui_createSensorWindow
from adminAssetWindow import Ui_adminAssetWindow
from adminSensorWindow import Ui_adminSensorWindow
from asset import Asset
from movingObject import MovingObject
from mqttConfig import MqttConfig
from sensor import Sensor
from temperatureSim import TemperatureSimulator
from testData import TestData
from user import User


class Ui_MainWindow(QMainWindow):
    update_signal = pyqtSignal(str, str)
    update_signal_sensor = pyqtSignal(str, str)

    def setupUi(self, mainWindow):
        mainWindow.resize(1300, 1000)
        self.scene_width = 959
        self.scene_height = 663
        self.centralwidget = QtWidgets.QWidget(mainWindow)
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)

        self.sensorList = []
        self.assetList = []
        self.userList = []
        self.person_item = None  # Add this line to track the person item
        self.image_asset_item = None  # Track the image asset item
        self.publish_timer = QTimer()  # Add a timer for publishing MQTT messages

        # Define platform coordinates
        self.platforms = {"Platform 1": (877, 36), "Platform 2": (657, 188)}

        # Define users dictionary
        self.users = {
            "Professor": User(
                "user_professor1",
                "Professor",
                "no description",
                188.0,
                544,
                "media/user/user_professor.png",
            ),
            "Postgraduate": User(
                "user_postgraduate1",
                "Postgraduate",
                "no description",
                188.0,
                544,
                "media/user/user_student_postgraduate.png",
            ),
            "Undergraduate": User(
                "user_underground1",
                "Undergraduate",
                "no description",
                188.0,
                544,
                "media/user/user_student_underground.png",
            ),
            "Unknown": User(
                "user_unknowing1",
                "Unknown",
                "no description",
                188.0,
                544,
                "media/user/user_unknowing.png",
            ),
        }

        self.setupGraphicsView()
        self.setupTextFieldAndButton()
        self.setupComboBoxAndChangeImageButton()
        self.setupToolBar(mainWindow)
        self.setupTemperatureSimulator()
        self.setupPersonButton()
        self.setupImageAssetButton()  # Setup the new button

        self.update_signal.connect(self.update_asset_state)
        self.update_signal_sensor.connect(self.update_sensor_values)

        self.setupMqttClient()

        self.centralwidget.setObjectName("centralwidget")
        mainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def setupGraphicsView(self):
        self.scene = QtWidgets.QGraphicsScene(self.centralwidget)
        self.graphicsView = QtWidgets.QGraphicsView(self.scene)
        self.graphicsView.setSceneRect(0, 0, self.scene_width, self.scene_height)
        self.graphicsView.setTransformationAnchor(
            QtWidgets.QGraphicsView.AnchorUnderMouse
        )
        self.gridLayout.addWidget(self.graphicsView, 0, 0, 1, 1)
        self.addBackgroundToScene()

    def setupTextFieldAndButton(self):
        self.horizontalLayout = QtWidgets.QHBoxLayout()

        self.textField = QLineEdit(self.centralwidget)
        self.textField.setPlaceholderText("Enter text here")
        self.horizontalLayout.addWidget(self.textField)

        self.addLampButton = QPushButton("Add Lamp", self.centralwidget)
        self.addLampButton.clicked.connect(self.addLamp)
        self.horizontalLayout.addWidget(self.addLampButton)

        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)

    def setupComboBoxAndChangeImageButton(self):
        self.verticalLayout = QtWidgets.QVBoxLayout()

        self.chargeTempTestButton = QPushButton(
            "Charge Temperature Test", self.centralwidget
        )
        self.chargeTempTestButton.clicked.connect(self.charge_temperature_test)
        self.verticalLayout.addWidget(self.chargeTempTestButton)

        self.bgComboBox = QComboBox(self.centralwidget)
        self.bgComboBox.addItem("1006 room", "media/room-1006.png")
        self.bgComboBox.addItem(
            "1006 temperature room", "media/room-1006-temperature.png"
        )  # Add more backgrounds as needed
        self.verticalLayout.addWidget(self.bgComboBox)

        self.changeBgButton = QPushButton("Change Background", self.centralwidget)
        self.changeBgButton.clicked.connect(self.change_background)
        self.verticalLayout.addWidget(self.changeBgButton)

        self.gridLayout.addLayout(self.verticalLayout, 2, 0, 1, 1)

    def setupToolBar(self, mainWindow):
        self.toolbar = QToolBar()
        self.toolbar.setMovable(False)
        mainWindow.addToolBar(self.toolbar)

        self.create_asset = QAction(
            QIcon("media/new_asset.png"), "Create Asset", mainWindow
        )
        self.admin_asset = QAction(
            QIcon("media/edit_asset.png"), "Administrate Asset", mainWindow
        )

        self.create_sensor = QAction(
            QIcon("media/new_sensor.png"), "Create Sensor", mainWindow
        )
        self.admin_sensor = QAction(
            QIcon("media/edit_sensor.png"), "Administrate Sensor", mainWindow
        )

        self.toolbar.addAction(self.create_asset)
        self.toolbar.addAction(self.admin_asset)
        self.toolbar.addAction(self.create_sensor)
        self.toolbar.addAction(self.admin_sensor)

        self.create_asset.triggered.connect(
            lambda: self.open_windows_create_asset(self)
        )
        self.admin_asset.triggered.connect(lambda: self.open_windows_admin_asset(self))
        self.create_sensor.triggered.connect(
            lambda: self.open_windows_create_sensor(self)
        )
        self.admin_sensor.triggered.connect(
            lambda: self.open_windows_admin_sensor(self)
        )

    def setupTemperatureSimulator(self):
        self.temperatureSimulator = TemperatureSimulator(
            self.centralwidget, self.gridLayout
        )
        self.temperatureSimulator.set_asset_list(self.assetList)

    def addLamp(self):
        self.temperatureSimulator.numLamps += 1
        self.temperatureSimulator.lampsCountLabel.setText(
            str(self.temperatureSimulator.numLamps)
        )
        self.create_asset_gi(Asset("lamp", "Lamp", "description"))

    def addBackgroundToScene(self, image_path="media/room-1006.png"):
        pix = QtGui.QPixmap(image_path)
        pix.scaled(self.scene_width, self.scene_height, Qt.KeepAspectRatio)
        self.bg_label = QLabel()
        self.bg_label.setGeometry(0, 0, self.scene_width, self.scene_height)
        self.bg_label.setPixmap(pix)

        self.proxy = QtWidgets.QGraphicsProxyWidget()
        self.proxy.setWidget(self.bg_label)
        self.scene.addItem(self.proxy)

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("MainWindow", "MainWindow-Simulator"))

    def open_windows_create_asset(self, p_Ui_MainWindow):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_createAssetWindow()
        self.ui.setupUi(self.window, p_Ui_MainWindow)
        self.window.show()

    def open_windows_create_sensor(self, p_Ui_MainWindow):
        self.window = QtWidgets.QMainWindow()
        self.ui2 = Ui_createSensorWindow()
        self.ui2.setupUi(self.window, p_Ui_MainWindow)
        self.window.show()

    def open_windows_admin_sensor(self, p_Ui_MainWindow):
        self.window = QtWidgets.QMainWindow()
        self.ui2 = Ui_adminSensorWindow()
        self.ui2.setupUi(self.window, p_Ui_MainWindow)
        self.window.show()

    def open_windows_admin_asset(self, p_Ui_MainWindow):
        self.window = QtWidgets.QMainWindow()
        self.ui2 = Ui_adminAssetWindow()
        self.ui2.setupUi(self.window, p_Ui_MainWindow)
        self.window.show()

    def create_sensor_gi(self, p_Sensor):
        move_object = MovingObject(p_Sensor, self)
        self.sensorList.append(move_object)
        self.scene.addItem(move_object)

    def create_asset_gi(self, p_Asset):
        move_object = MovingObject(p_Asset, self)
        self.assetList.append(move_object)
        self.scene.addItem(move_object)

    def create_user_gi(self, p_User):
        move_object = MovingObject(p_User, self)
        self.userList.append(move_object)
        self.scene.addItem(move_object)

    def get_sensor_list(self):
        return self.sensorList

    def get_asset_list(self):
        return self.assetList

    def charge_temperature_test(self):
        dataTest = TestData()
        list_test_sensors = dataTest.get_data_sensors()
        list_test_assets = dataTest.get_data_assets()

        for test_sensor in list_test_sensors:
            self.create_sensor_gi(test_sensor)

            if test_sensor.get_type() == "SensorTemperature":
                self.temperatureSimulator.register_temperature_sensor(
                    test_sensor.get_simulator_sensor()
                )

        for test_asset in list_test_assets:
            self.create_asset_gi(test_asset)

    def change_background(self):
        selected_bg = self.bgComboBox.currentData()
        self.scene.removeItem(self.proxy)  # Remove the old background
        self.addBackgroundToScene(selected_bg)  # Add the new background

    def setupPersonButton(self):
        self.verticalLayoutRight = QtWidgets.QVBoxLayout()

        # Add the first combo box for the categories
        self.personCategoryComboBox = QComboBox(self.centralwidget)
        self.personCategoryComboBox.addItems(
            ["Professor", "Postgraduate", "Undergraduate", "Unknown"]
        )
        self.verticalLayoutRight.addWidget(self.personCategoryComboBox)

        # Add the second combo box for the platforms
        self.platformComboBox = QComboBox(self.centralwidget)
        self.platformComboBox.addItems(["Platform 1", "Platform 2"])
        self.verticalLayoutRight.addWidget(self.platformComboBox)

        # Add the "Add User" button
        self.addUserButton = QPushButton("Add User", self.centralwidget)
        self.addUserButton.clicked.connect(self.addUser)
        self.verticalLayoutRight.addWidget(self.addUserButton)

        # remove the "remove one User" button
        self.removeOneUserButton = QPushButton("Remove User", self.centralwidget)
        self.removeOneUserButton.clicked.connect(self.removeOneUser)
        self.verticalLayoutRight.addWidget(self.removeOneUserButton)

        # remove the "remove all User" button
        self.removeUserButton = QPushButton("Remove Users", self.centralwidget)
        self.removeUserButton.clicked.connect(self.removeUsers)
        self.verticalLayoutRight.addWidget(self.removeUserButton)

        # Add the "Add Person" button
        self.addPersonButton = QPushButton("Add Person", self.centralwidget)
        self.addPersonButton.setCheckable(True)
        self.addPersonButton.clicked.connect(self.addPerson)
        self.verticalLayoutRight.addWidget(self.addPersonButton)

        self.gridLayout.addLayout(self.verticalLayoutRight, 0, 1, 1, 1)

    def addUser(self):
        # This function will print the selected values from both combo boxes
        personCategory = self.personCategoryComboBox.currentText()
        platform = self.platformComboBox.currentText()
        print(f"Selected Person Category: {personCategory}")
        print(f"Selected Platform: {platform}")

        # Get the platform's position (X, Y)
        posX, posY = self.platforms[platform]

        temp_user = self.users[personCategory]
        temp_user.set_posXY(
            posX, posY
        )  # Set the position (X, Y) of the user based on platform
        temp_user.set_platform(platform)

        # Create the user graphical interface
        self.create_user_gi(temp_user)

        if platform == "Platform 1":
            self.changeSensorValue2("sensor_presence1", 1, temp_user)
        else:
            self.changeSensorValue2("sensor_presence2", 1, temp_user)

    def removeUsers(self):
        print("removing users...")
        for user in self.userList:
            self.scene.removeItem(user)
        self.userList.clear()
        self.changeSensorValue2("sensor_presence1", 0, None)
        self.changeSensorValue2("sensor_presence2", 0, None)

    def removeOneUser(self):
        print("Removing one user...")

        # Get the selected person category and platform
        personCategory = self.personCategoryComboBox.currentText()
        platform = self.platformComboBox.currentText()

        # Use a temporary list to avoid modifying the list while iterating
        users_to_remove = [
            user
            for user in self.userList
            if user.obj.get_type() == personCategory
            and user.obj.get_platform() == platform
        ]

        # Remove the users from both the scene and the userList
        for user in users_to_remove:
            self.scene.removeItem(user)
            self.userList.remove(user)

        # Adjust the sensor value based on the platform
        if platform == "Platform 1":
            self.changeSensorValue2("sensor_presence1", 0, None)
        else:
            self.changeSensorValue2("sensor_presence2", 0, None)

    def addPerson(self):
        if self.addPersonButton.isChecked():
            if self.person_item is None:
                person_pixmap = QtGui.QPixmap("media/person.png")
                self.person_item = QGraphicsPixmapItem(person_pixmap)
                self.person_item.setPos(910, 10)
                self.scene.addItem(self.person_item)
                self.changeSensorValue("sensor_presence1", 1)

        else:
            if self.person_item is not None:
                self.scene.removeItem(self.person_item)
                self.person_item = None
                self.changeSensorValue("sensor_presence1", 0)

    def setupImageAssetButton(self):
        self.addAssetControllerButton = QPushButton(
            "Connect asset controller", self.centralwidget
        )
        self.addAssetControllerButton.setCheckable(True)
        self.addAssetControllerButton.clicked.connect(self.addAssetController)
        self.verticalLayoutRight.addWidget(self.addAssetControllerButton)

    def addAssetController(self):
        if self.addAssetControllerButton.isChecked():
            if self.image_asset_item is None:
                image_pixmap = QtGui.QPixmap("media/asset-controller.jpg")
                self.image_asset_item = QGraphicsPixmapItem(image_pixmap)
                self.image_asset_item.setPos(460, 358)  # Center of the scene
                self.scene.addItem(self.image_asset_item)
            self.startPublishing()
        else:
            if self.image_asset_item is not None:
                self.scene.removeItem(self.image_asset_item)
                self.image_asset_item = None
            self.stopPublishing()

    def startPublishing(self):
        self.publish_timer.timeout.connect(self.publishAssets)
        self.publish_timer.start(5000)  # 15 seconds interval

    def stopPublishing(self):
        self.publish_timer.stop()

    def publishAssets(self):
        # Create the payload with asset list
        asset_list = [
            {
                "id": asset.obj.get_id(),
                "status": asset.obj.get_status(),
                "type": asset.obj.get_type(),
            }
            for asset in self.assetList
        ]
        payload = {
            "id": "asset_controller",
            "assets": asset_list,
            "datetime": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        }

        # Convert payload to JSON string
        payload_json = json.dumps(payload)

        print("::> ", payload_json)

        # Publish the payload
        self.client.publish("lab1006/control/assets", payload_json)

    def changeSensorValue(self, id_sensor, new_value):
        #### Inform to the presence sensor that person is present
        for v_sensor in self.sensorList:
            if v_sensor.obj.get_id() == id_sensor:
                v_sensor.obj.get_simulator_sensor().change_reading(new_value)

    def changeSensorValue2(self, id_sensor, new_value, new_user):
        #### Inform to the presence sensor that person is present
        for v_sensor in self.sensorList:
            if v_sensor.obj.get_id() == id_sensor:
                v_sensor.obj.get_simulator_sensor().change_reading(new_value, new_user)

    def setupMqttClient(self):
        # Get data from mqtt config
        config = MqttConfig()
        mqtt_data = config.get_data_mqtt()
        user_mqtt = mqtt_data["user"]
        pass_mqtt = mqtt_data["password"]
        self.client = mqtt.Client("GUI-Subcriber-Publisher")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        if user_mqtt and pass_mqtt:
            self.client.username_pw_set(user_mqtt, pass_mqtt)
        self.client.connect(mqtt_data["host"], mqtt_data["port"], 60)
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        client.subscribe("lab1006/control/asset")
        client.subscribe(
            "lab1006/control/sensor"
        )  # Add this line to subscribe to the sensor topic

    def on_message(self, client, userdata, msg):
        payload = msg.payload.decode("utf-8")
        data = json.loads(payload)

        if msg.topic == "lab1006/control/asset":
            id_asset = data.get("id")
            new_value = data.get("state_value")
            self.update_signal.emit(id_asset, new_value)
        elif msg.topic == "lab1006/control/sensor":
            id_sensor = data.get("id")
            new_value = data.get("agent_monitor_id")
            self.update_signal_sensor.emit(
                id_sensor, new_value
            )  # Emit a signal to update sensor

    def update_sensor_values(self, id_sensor, new_value):
        print(f"Updating sensor... > {id_sensor} , {new_value}")
        for sensor in self.sensorList:
            if sensor.obj.get_id() == id_sensor:
                sensor.obj.get_simulator_sensor().change_agent_monitor(new_value)
                print(f"Updated sensor {id_sensor} to value {new_value}")
                break

    def update_asset_state(self, id_asset, new_value):
        print(f"Updating asset... > {id_asset} , {new_value}")
        for v_asset in self.assetList:
            if v_asset.obj.get_id() == id_asset:
                if new_value == "1":
                    v_asset.change_image(v_asset.obj.get_path_state1())
                    v_asset.obj.set_status("ON")
                else:
                    v_asset.change_image(v_asset.obj.get_path_state2())
                    v_asset.obj.set_status("OFF")

                print(f"Updated asset {id_asset} to state {new_value}")
                break


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
