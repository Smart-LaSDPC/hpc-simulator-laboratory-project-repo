from PyQt5.QtWidgets import QLabel, QLineEdit
from PyQt5.QtCore import QTimer

class TemperatureSimulator:
    def __init__(self, centralwidget, gridLayout):
        self.centralwidget = centralwidget
        self.gridLayout = gridLayout
        self.numLamps = 0
        self.numHeaters = 0
        self.qLamp = 100  # Heat gain from each lamp in Watts
        self.qHeater = 2000  # Heat gain from each heater in Watts
        self.uValue = 0.2  # Overall heat transfer coefficient (W/m^2*K)
        self.wallArea = 100  # Area of the walls in m^2
        self.volume = 50  # Volume of the room in m^3
        self.cPair = 1005  # J/(kg*K) - Specific heat capacity of air
        self.density = 1.225  # kg/m^3 - Density of air
        self.setupTemperatureSimulator()

    def setupTemperatureSimulator(self):
        self.roomTempLabel = QLabel("Room Temperature (°C):", self.centralwidget)
        self.roomTempInput = QLineEdit("25", self.centralwidget)

        self.outsideTempLabel = QLabel("Outside Temperature (°C):", self.centralwidget)
        self.outsideTempInput = QLineEdit("20", self.centralwidget)

        self.lampsLabel = QLabel("Number of Lamps:", self.centralwidget)
        self.lampsCountLabel = QLabel("0", self.centralwidget)

        self.heatersLabel = QLabel("Number of Heaters:", self.centralwidget)
        self.heatersCountLabel = QLabel("0", self.centralwidget)

        self.gridLayout.addWidget(self.roomTempLabel, 3, 0, 1, 1)
        self.gridLayout.addWidget(self.roomTempInput, 3, 1, 1, 1)

        self.gridLayout.addWidget(self.outsideTempLabel, 4, 0, 1, 1)
        self.gridLayout.addWidget(self.outsideTempInput, 4, 1, 1, 1)

        self.gridLayout.addWidget(self.lampsLabel, 5, 0, 1, 1)
        self.gridLayout.addWidget(self.lampsCountLabel, 5, 1, 1, 1)

        self.gridLayout.addWidget(self.heatersLabel, 6, 0, 1, 1)
        self.gridLayout.addWidget(self.heatersCountLabel, 6, 1, 1, 1)

        self.simulationTimer = QTimer()
        self.simulationTimer.timeout.connect(self.updateTemperature)
        self.simulationTimer.start(1000)  # Update every second

    def updateTemperature(self):
        try:
            tRoom = float(self.roomTempInput.text())
            tOut = float(self.outsideTempInput.text())
        except ValueError:
            return

        self.updateNumLampsHeatersTurnOn()

        qGainLamps = self.qLamp * self.numLamps  # Total heat gain from lamps
        qGainHeaters = self.qHeater * self.numHeaters  # Total heat gain from heaters
        qGain = qGainLamps + qGainHeaters  # Combined heat gain
        qLoss = self.uValue * self.wallArea * (tRoom - tOut)  # Heat loss to the outside environment

        # Calculate temperature change
        deltaT = (qGain - qLoss) / (self.density * self.volume * self.cPair)
        tRoom += deltaT  # Update room temperature

        self.roomTempInput.setText(f"{tRoom:.4f}")

    def updateNumLampsHeatersTurnOn(self):
        self.numLamps = 0
        self.numHeaters = 0
        for asset in self.assetList:
            if asset.obj.get_status() == "ON" and asset.obj.get_type() == "AssetLamp":
                self.numLamps += 1
            elif asset.obj.get_status() == "ON" and asset.obj.get_type() == "AssetHeater":
                self.numHeaters += 1

        turnOnLamps = self.numLamps
        turnOffLamps = len([asset for asset in self.assetList if asset.obj.get_type() == "AssetLamp"]) - self.numLamps

        turnOnHeaters = self.numHeaters
        turnOffHeaters = len([asset for asset in self.assetList if asset.obj.get_type() == "AssetHeater"]) - self.numHeaters

        self.lampsCountLabel.setText(f'ON: {turnOnLamps} | OFF: {turnOffLamps}')
        self.heatersCountLabel.setText(f'ON: {turnOnHeaters} | OFF: {turnOffHeaters}')

    def set_asset_list(self, assetList):
        self.assetList = assetList
