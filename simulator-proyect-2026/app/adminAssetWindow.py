from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys, random

from asset import Asset  # Import Asset class instead of Sensor class

class Ui_adminAssetWindow(object):

    def turn_on_asset(self, p_Ui_MainWindow, v_asset):   
        print("Turn ON :", v_asset.obj.get_id())
        try:
            v_asset.obj.set_status("ON")  
            v_asset.change_image(v_asset.obj.get_path_state1())
        finally:
            pass 

    def turn_off_asset(self, p_Ui_MainWindow, v_asset):   
        print("Turn OFF:", v_asset.obj.get_id())
        v_asset.obj.set_status("OFF")
        v_asset.change_image(v_asset.obj.get_path_state2())
        
    def disconnect_asset(self, p_Ui_MainWindow, v_asset):   
        print("Disconnecting...:", v_asset.obj.get_id())
        print("Simulation stopped.")
        v_asset.obj.get_simulator_asset().stop()
        self.turn_off_asset(p_Ui_MainWindow, v_asset)
        
    def connect_asset(self, p_Ui_MainWindow, v_asset):   
        print("Connecting...:", v_asset.obj.get_id())
        try:
            v_asset.obj.get_simulator_asset().start()  
            self.turn_on_asset(p_Ui_MainWindow, v_asset) 
        finally:
            pass 
        print("Asset connected.")
        
    def turn_on_all_assets(self, p_Ui_MainWindow):   
        listVirtualAssets = p_Ui_MainWindow.get_asset_list()
        for asset in listVirtualAssets:
            self.turn_on_asset(p_Ui_MainWindow, asset)

    def turn_off_all_assets(self, p_Ui_MainWindow):   
        listVirtualAssets = p_Ui_MainWindow.get_asset_list()
        for asset in listVirtualAssets:
            self.turn_off_asset(p_Ui_MainWindow, asset)

    def disconnect_all_assets(self, p_Ui_MainWindow):   
        listVirtualAssets = p_Ui_MainWindow.get_asset_list()
        for asset in listVirtualAssets:
            self.disconnect_asset(p_Ui_MainWindow, asset)
            
    def connect_all_assets(self, p_Ui_MainWindow):   
        listVirtualAssets = p_Ui_MainWindow.get_asset_list()
        for asset in listVirtualAssets:
            self.connect_asset(p_Ui_MainWindow, asset)

    def remove_asset(self, p_Ui_MainWindow):   
        listVirtualAssets = p_Ui_MainWindow.get_asset_list()
        asset_to_remove = listVirtualAssets[self.index_asset]
        print("Remove Asset:", asset_to_remove.get_id())
        p_Ui_MainWindow.remove_asset(asset_to_remove.get_id())
        self.assetBox.removeItem(self.index_asset)

    def remove_all_assets(self, p_Ui_MainWindow):   
        listVirtualAssets = p_Ui_MainWindow.get_asset_list()
        for asset in listVirtualAssets:
            print("Remove Asset:", asset.get_id())
            p_Ui_MainWindow.remove_asset(asset.get_id())
        self.assetBox.clear()

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
        self.Label1 = QLabel("Administration of Assets")
        font = QtGui.QFont()
        font.setPointSize(14)
        self.Label1.setFont(font) 

        self.assetBox = QComboBox()
        self.assetBox.currentIndexChanged.connect(self.selectionchange)

        
        # Loop thru assets and add to screen
        listVirtualAssets = p_Ui_MainWindow.get_asset_list()
        for v_asset in listVirtualAssets:
            self.assetBox.addItem(v_asset.obj.get_id())

        #Turn ON button
        self.btnTurnOn = QPushButton(self.centralwidget, 
            clicked = lambda: self.turn_on_asset(p_Ui_MainWindow, self.get_virtualAssetSelected(p_Ui_MainWindow)))
        self.btnTurnOn.setGeometry(QtCore.QRect(10, 70, 161, 61))
        self.btnTurnOn.setObjectName("btnTurnOn")

        #Turn OFF button
        self.btnTurnOff = QPushButton(self.centralwidget, 
            clicked = lambda: self.turn_off_asset(p_Ui_MainWindow, self.get_virtualAssetSelected(p_Ui_MainWindow)))
        self.btnTurnOff.setGeometry(QtCore.QRect(10, 140, 161, 61))
        self.btnTurnOff.setObjectName("btnTurnOff")

        #Turn ON all assets button
        self.btnTurnOnAll = QPushButton(self.centralwidget, 
            clicked = lambda: self.turn_on_all_assets(p_Ui_MainWindow))
        self.btnTurnOnAll.setGeometry(QtCore.QRect(180, 70, 161, 61))
        self.btnTurnOnAll.setObjectName("btnTurnOnAll")

        #Turn OFF all assets button
        self.btnTurnOffAll = QPushButton(self.centralwidget, 
            clicked = lambda: self.turn_off_all_assets(p_Ui_MainWindow))
        self.btnTurnOffAll.setGeometry(QtCore.QRect(180, 140, 161, 61))
        self.btnTurnOffAll.setObjectName("btnTurnOffAll")

        #Remove asset button
        self.btnRemoveAsset = QPushButton(self.centralwidget, 
            clicked = lambda: self.remove_asset(p_Ui_MainWindow))
        self.btnRemoveAsset.setGeometry(QtCore.QRect(10, 350, 161, 61))
        self.btnRemoveAsset.setObjectName("btnRemoveAsset")

        #Remove all assets button
        self.btnRemoveAllAssets = QPushButton(self.centralwidget, 
            clicked = lambda: self.remove_all_assets(p_Ui_MainWindow))
        self.btnRemoveAllAssets.setGeometry(QtCore.QRect(10, 420, 161, 61))
        self.btnRemoveAllAssets.setObjectName("btnRemoveAllAssets")
        
        self.initUI(SecondWindow)
        self.retranslateUi(SecondWindow)
        QtCore.QMetaObject.connectSlotsByName(SecondWindow)

    def selectionchange(self, i):
        self.index_asset = self.assetBox.currentIndex()  
        print("Current index", i, "selection changed", self.assetBox.currentText())

    def get_virtualAssetSelected(self, p_Ui_MainWindow):
        selected_asset_id = self.assetBox.currentText()
        listVirtualAssets = p_Ui_MainWindow.get_asset_list()

        for v_asset in listVirtualAssets:
            if v_asset.obj.get_id() == selected_asset_id:                
                break
        return v_asset

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
        lower_left_widget = QGroupBox("Asset informations")

        lower_left_layout = QVBoxLayout()
        lower_left_layout.addWidget(QLabel("Choose asset:"))
        lower_left_layout.addWidget(self.assetBox)    

        lower_left_layout.addStretch(9)
        lower_left_layout.addWidget(self.btnTurnOn)
        lower_left_layout.addWidget(self.btnTurnOff)

        lower_left_layout.addWidget(self.btnTurnOnAll)
        lower_left_layout.addWidget(self.btnTurnOffAll)

        lower_left_layout.addWidget(self.btnRemoveAsset)
        lower_left_layout.addWidget(self.btnRemoveAllAssets)

        lower_left_widget.setLayout(lower_left_layout)
        
        lower_right_layout = QVBoxLayout()
        lower_right_widget = QWidget()
        lower_right_widget.setLayout(lower_right_layout)

        lower_layout = QHBoxLayout()
        lower_layout.addWidget(lower_left_widget)
        lower_layout.addWidget(lower_right_widget)
        lower_layout.setStretch(0, 1)
        lower_layout.setStretch(1, 2)
        lower_widget = QWidget()
        lower_widget.setLayout(lower_layout)

        return lower_widget

    def retranslateUi(self, SecondWindow):
        _translate = QtCore.QCoreApplication.translate
        SecondWindow.setWindowTitle(_translate("SecondWindow", "Administration of Assets"))
        self.btnTurnOn.setText(_translate("SecondWindow", "Turn ON Asset"))
        self.btnTurnOff.setText(_translate("SecondWindow", "Turn OFF Asset"))

        self.btnTurnOnAll.setText(_translate("SecondWindow", "Turn ON all assets"))
        self.btnTurnOffAll.setText(_translate("SecondWindow", "Turn OFF all assets"))

        self.btnRemoveAsset.setText(_translate("SecondWindow", "Remove asset"))
        self.btnRemoveAllAssets.setText(_translate("SecondWindow", "Remove all assets"))

    def add_it(self):
        pass


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    SecondWindow = QMainWindow()
    ui = Ui_adminAssetWindow()
    ui.setupUi(SecondWindow)
    SecondWindow.show()
    sys.exit(app.exec_())
