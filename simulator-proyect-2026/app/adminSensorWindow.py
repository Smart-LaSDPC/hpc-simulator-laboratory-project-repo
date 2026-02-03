from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys, random
import os
import threading

from sensor import Sensor
from simulatorSensor import TemperatureSensor

class Ui_adminSensorWindow(object):

    def turn_on_sensor(self, p_Ui_MainWindow, v_sensor):   
        print("Turn ON :", v_sensor.obj.get_id_sensor())
        print("starting ", v_sensor.obj.get_id_sensor())
        try:  
            v_sensor.obj.get_simulator_sensor().start()
            v_sensor.obj.set_status("ON")            
            v_sensor.change_image(v_sensor.obj.get_path_state1())
            pass   
        finally:
            pass 

    def turn_off_sensor(self, p_Ui_MainWindow, v_sensor):   
        print("Turn OFF :", v_sensor.obj.get_id_sensor())        
        v_sensor.obj.get_simulator_sensor().stop()
        v_sensor.obj.set_status("OFF")
        v_sensor.change_image(v_sensor.obj.get_path_state2())
        print("Simulation stopped.")

    def turn_on_all_sensors(self, p_Ui_MainWindow):   
        listVirtualSensors = p_Ui_MainWindow.get_sensor_list()
        for sensor in listVirtualSensors:
            self.turn_on_sensor(p_Ui_MainWindow, sensor)

    def turn_off_all_sensors(self, p_Ui_MainWindow):   
        listVirtualSensors = p_Ui_MainWindow.get_sensor_list()
        for sensor in listVirtualSensors:
            self.turn_off_sensor(p_Ui_MainWindow, sensor)

    def remove_sensor(self, p_Ui_MainWindow):   
        listVirtualSensors = p_Ui_MainWindow.get_sensor_list()
        sensor_to_remove = listVirtualSensors[self.index_sensor]
        print("Remove Sensor:", sensor_to_remove.get_id_sensor())
        p_Ui_MainWindow.remove_sensor(sensor_to_remove.get_id_sensor())
        self.sensorBox.removeItem(self.index_sensor)

    def remove_all_sensors(self, p_Ui_MainWindow):   
        listVirtualSensors = p_Ui_MainWindow.get_sensor_list()
        for sensor in listVirtualSensors:
            print("Remove Sensor:", sensor.get_id_sensor())
            p_Ui_MainWindow.remove_sensor(sensor.get_id_sensor())
        self.sensorBox.clear()

    def setupUi(self, SecondWindow, p_Ui_MainWindow):
        SecondWindow.setObjectName("SecondWindow")
        SecondWindow.resize(800, 600)
        self.centralwidget = QWidget(SecondWindow)
        self.centralwidget.setObjectName("centralwidget")
       
        SecondWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(SecondWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 543, 21))
        self.menubar.setObjectName("menubar")
        SecondWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(SecondWindow)
        self.statusbar.setObjectName("statusbar")
        SecondWindow.setStatusBar(self.statusbar)

        #################
        # create all widgets
        self.Label1 = QLabel("Administration of Sensor")
        font = QtGui.QFont()
        font.setPointSize(14)
        self.Label1.setFont(font) 

        self.sensorBox = QComboBox()
        self.sensorBox.currentIndexChanged.connect(self.selectionchange)

        
        # Loop thru sensors and add to screen
        listVirtualSensors = p_Ui_MainWindow.get_sensor_list()
        for v_sensor in listVirtualSensors:
            self.sensorBox.addItem(v_sensor.obj.get_id())

        #Turn ON button
        self.btnTurnOn = QPushButton(self.centralwidget, 
            clicked = lambda: self.turn_on_sensor(p_Ui_MainWindow, self.get_virtualSensorSelected(p_Ui_MainWindow)))
        self.btnTurnOn.setGeometry(QtCore.QRect(10, 70, 161, 61))
        self.btnTurnOn.setObjectName("btnTurnOn")

        #Turn OFF button
        self.btnTurnOff = QPushButton(self.centralwidget, 
            clicked = lambda: self.turn_off_sensor(p_Ui_MainWindow, self.get_virtualSensorSelected(p_Ui_MainWindow)))
        self.btnTurnOff.setGeometry(QtCore.QRect(10, 140, 161, 61))
        self.btnTurnOff.setObjectName("btnTurnOff")

        #Turn ON all sensors button
        self.btnTurnOnAll = QPushButton(self.centralwidget, 
            clicked = lambda: self.turn_on_all_sensors(p_Ui_MainWindow))
        self.btnTurnOnAll.setGeometry(QtCore.QRect(10, 210, 161, 61))
        self.btnTurnOnAll.setObjectName("btnTurnOnAll")

        #Turn OFF all sensors button
        self.btnTurnOffAll = QPushButton(self.centralwidget, 
            clicked = lambda: self.turn_off_all_sensors(p_Ui_MainWindow))
        self.btnTurnOffAll.setGeometry(QtCore.QRect(10, 280, 161, 61))
        self.btnTurnOffAll.setObjectName("btnTurnOffAll")

        #Remove sensor button
        self.btnRemoveSensor = QPushButton(self.centralwidget, 
            clicked = lambda: self.remove_sensor(p_Ui_MainWindow))
        self.btnRemoveSensor.setGeometry(QtCore.QRect(10, 350, 161, 61))
        self.btnRemoveSensor.setObjectName("btnRemoveSensor")

        #Remove all sensors button
        self.btnRemoveAllSensors = QPushButton(self.centralwidget, 
            clicked = lambda: self.remove_all_sensors(p_Ui_MainWindow))
        self.btnRemoveAllSensors.setGeometry(QtCore.QRect(10, 420, 161, 61))
        self.btnRemoveAllSensors.setObjectName("btnRemoveAllSensors")
        
        self.initUI(SecondWindow)
        self.retranslateUi(SecondWindow)
        QtCore.QMetaObject.connectSlotsByName(SecondWindow)

    def selectionchange(self,i):
        self.index_sensor = self.sensorBox.currentIndex()  
        print("Current index",i,"selection changed ",self.sensorBox.currentText())

    def get_virtualSensorSelected(self, p_Ui_MainWindow):
        selected_sensor_id = self.sensorBox.currentText()
        listVirtualSensors = p_Ui_MainWindow.get_sensor_list()

        for v_sensor in listVirtualSensors:
            if v_sensor.obj.get_id() == selected_sensor_id:                
                break
        return v_sensor

    def initUI(self, SecondWindow):
        upper_widget = self.create_upper_widget()
        lower_widget = self.create_lower_widget()
        
        main_layout = QVBoxLayout()
        main_layout.addWidget(upper_widget)
        main_layout.addWidget(lower_widget)
        main_layout.setStretch(0, 1)
        main_layout.setStretch(1, 4)
        main_widget = QWidget()
        main_widget.setLayout(main_layout)

        SecondWindow.setCentralWidget(main_widget)

    def create_upper_widget(self):
        upper_layout = QVBoxLayout()
        upper_layout.addWidget(self.Label1)
        upper_layout.addStretch(5)
        upper_widget = QWidget()
        upper_widget.setLayout(upper_layout)
        return upper_widget

    def create_lower_widget(self):
        lower_left_widget = QGroupBox("Sensor informations")

        lower_left_layout = QVBoxLayout()
        lower_left_layout.addWidget(QLabel("Choose sensor:"))
        lower_left_layout.addWidget(self.sensorBox)    

        lower_left_layout.addStretch(5)
        lower_left_layout.addWidget(self.btnTurnOn)
        lower_left_layout.addWidget(self.btnTurnOff)
        lower_left_layout.addWidget(self.btnTurnOnAll)
        lower_left_layout.addWidget(self.btnTurnOffAll)  # Add Turn OFF all sensors button
        lower_left_layout.addWidget(self.btnRemoveSensor)
        lower_left_layout.addWidget(self.btnRemoveAllSensors)

        lower_left_widget.setLayout(lower_left_layout)
        
        lower_right_layout = QVBoxLayout()
        lower_right_widget = QWidget()
        lower_right_widget.setLayout(lower_right_layout)

        lower_layout = QHBoxLayout()
        lower_layout.addWidget(lower_left_widget)
        lower_layout.addWidget(lower_right_widget)
        lower_layout.setStretch(0,1)
        lower_layout.setStretch(1,2)
        lower_widget = QWidget()
        lower_widget.setLayout(lower_layout)

        return lower_widget

    def retranslateUi(self, SecondWindow):
        _translate = QtCore.QCoreApplication.translate
        SecondWindow.setWindowTitle(_translate("SecondWindow", "Administration of Sensor - windows"))
        self.btnTurnOn.setText(_translate("SecondWindow", "Turn ON Sensor"))
        self.btnTurnOff.setText(_translate("SecondWindow", "Turn OFF Sensor"))
        self.btnTurnOnAll.setText(_translate("SecondWindow", "Turn ON all sensors"))
        self.btnTurnOffAll.setText(_translate("SecondWindow", "Turn OFF all sensors"))  # Set text for Turn OFF all sensors button
        self.btnRemoveSensor.setText(_translate("SecondWindow", "Remove sensor"))
        self.btnRemoveAllSensors.setText(_translate("SecondWindow", "Remove all sensors"))

    def add_it(self):
        pass
