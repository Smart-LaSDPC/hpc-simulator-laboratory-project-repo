from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys, random

from sensor import Sensor

class Ui_createSensorWindow(object):

    def create_sensor(self, p_Ui_MainWindow):
        self.generate_id_sensor()
        p1 = self.idSensorBox.text()     
        p2 = "temperature"
        p3 = "for default create temperature sensor"
        new_sensor = Sensor(p1, p2, p3)        
        p_Ui_MainWindow.create_sensor_gi(new_sensor)
        #print(":)")

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
        self.Label1 = QLabel("Add sensor form")
        font = QtGui.QFont()
        font.setPointSize(14)
        self.Label1.setFont(font)
        
        self.idSensorBox = QLineEdit()        

        self.typeSensorBox = QComboBox()
        self.typeSensorBox.addItem('Temperature')
        self.typeSensorBox.addItem('Humidity')
        self.typeSensorBox.addItem('Motion')
        self.typeSensorBox.addItem('Touch')       


        self.btn = QPushButton(self.centralwidget, clicked = lambda: self.create_sensor(p_Ui_MainWindow))
        self.btn.setGeometry(QtCore.QRect(10, 70, 161, 61))
        self.btn.setObjectName("btn")


        ###########List of Sensors######
        self.mylist_listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.mylist_listWidget.setGeometry(QtCore.QRect(10, 90, 501, 231))
        self.mylist_listWidget.setObjectName("mylist_listWidget")
        ###############
        
        self.initUI(SecondWindow)
        self.retranslateUi(SecondWindow)
        QtCore.QMetaObject.connectSlotsByName(SecondWindow)


        ####Fill created Sensor Box
        listVirtualSensors = p_Ui_MainWindow.get_sensor_list()
        for v_sensor in listVirtualSensors:
            self.mylist_listWidget.addItem(v_sensor.obj.get_id())

    def initUI(self, SecondWindow):
        # setting up layout of main window
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
        upper_layout.addStretch(5)
        upper_widget = QWidget()
        upper_widget.setLayout(upper_layout)
        return upper_widget

    def create_lower_widget(self):
        lower_left_widget = QGroupBox("Sensor informations")

        lower_left_layout = QVBoxLayout()
        lower_left_layout.addWidget(QLabel("Choose sensor:"))
        lower_left_layout.addWidget(self.typeSensorBox)

        lower_left_layout.addWidget(QLabel("id:"))
        lower_left_layout.addWidget(self.idSensorBox)
        
        lower_left_layout.addWidget(QLabel("Description:"))
        #lower_left_layout.addWidget(self.descriptionSensorBox)        

        lower_left_layout.addStretch(5)
        lower_left_layout.addWidget(self.btn)
        lower_left_widget.setLayout(lower_left_layout)
        
        lower_right_layout = QVBoxLayout()
        lower_right_layout.addWidget(self.mylist_listWidget)
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
        SecondWindow.setWindowTitle(_translate("SecondWindow", "Add sensor windows"))
        self.btn.setText(_translate("SecondWindow", "Add Sensor"))

    # Add Item To List
    def generate_id_sensor(self):
        new_sensor_id = f'sensor_id_{random.randint(0, 1000)}'
        self.idSensorBox.setText(new_sensor_id)
        # Grab the item from the list box
        item = self.idSensorBox.text()
        # Add item to list
        self.mylist_listWidget.addItem(item)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    SecondWindow = QMainWindow()
    ui = Ui_SecondWindow()
    ui.setupUi(SecondWindow)
    SecondWindow.show()
    sys.exit(app.exec_())