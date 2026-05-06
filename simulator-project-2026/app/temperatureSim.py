from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QLabel, QLineEdit


class TemperatureSimulator:
    def __init__(self, centralwidget, gridLayout, zone_name="Room", grid_row_offset=0):
        self.centralwidget = centralwidget
        self.gridLayout = gridLayout
        self.zone_name = zone_name
        self.grid_row_offset = grid_row_offset
        self.numLamps = 0
        self.numHeaters = 0
        self.qLamp = 100  # Heat gain from each lamp in Watts
        self.qHeater = 2000  # Heat gain from each heater in Watts
        self.uValue = 0.2  # Overall heat transfer coefficient (W/m^2*K)
        self.wallArea = 100  # Area of the walls in m^2
        self.volume = 50  # Volume of the room in m^3
        self.cPair = 1005  # J/(kg*K) - Specific heat capacity of air
        self.density = 1.225  # kg/m^3 - Density of air
        self.qAC = 3500  # Capacity of the AC in Watts
        self.numACs = 0
        self._registered_sensors = []  # Sensors that will received the calculated temperature
        self.assetList = []
        self.setupTemperatureSimulator()

    def setupTemperatureSimulator(self):
        r = self.grid_row_offset

        self.zoneLabel = QLabel(f"--- {self.zone_name} ---", self.centralwidget)
        self.gridLayout.addWidget(self.zoneLabel, r, 0, 1, 2)

        self.roomTempLabel = QLabel("Room Temperature (°C):", self.centralwidget)
        self.roomTempInput = QLineEdit("25", self.centralwidget)
        self.gridLayout.addWidget(self.roomTempLabel, r + 1, 0, 1, 1)
        self.gridLayout.addWidget(self.roomTempInput, r + 1, 1, 1, 1)

        self.outsideTempLabel = QLabel("Outside Temperature (°C):", self.centralwidget)
        self.outsideTempInput = QLineEdit("20", self.centralwidget)
        self.gridLayout.addWidget(self.outsideTempLabel, r + 2, 0, 1, 1)
        self.gridLayout.addWidget(self.outsideTempInput, r + 2, 1, 1, 1)

        self.lampsLabel = QLabel("Number of Lamps:", self.centralwidget)
        self.lampsCountLabel = QLabel("0", self.centralwidget)
        self.gridLayout.addWidget(self.lampsLabel, r + 3, 0, 1, 1)
        self.gridLayout.addWidget(self.lampsCountLabel, r + 3, 1, 1, 1)

        self.heatersLabel = QLabel("Number of Heaters:", self.centralwidget)
        self.heatersCountLabel = QLabel("0", self.centralwidget)
        self.gridLayout.addWidget(self.heatersLabel, r + 4, 0, 1, 1)
        self.gridLayout.addWidget(self.heatersCountLabel, r + 4, 1, 1, 1)

        self.acLabel = QLabel("Number of ACs:", self.centralwidget)
        self.acCountLabel = QLabel("0", self.centralwidget)
        self.gridLayout.addWidget(self.acLabel, r + 5, 0, 1, 1)
        self.gridLayout.addWidget(self.acCountLabel, r + 5, 1, 1, 1)

        self.simulationTimer = QTimer()
        self.simulationTimer.timeout.connect(self.updateTemperature)
        self.simulationTimer.start(1000)  # Update every second

    def register_temperature_sensor(self, sensor_simulator):
        self._registered_sensors.append(sensor_simulator)

    def updateTemperature(self):
        try:
            tRoom = float(self.roomTempInput.text())
            tOut = float(self.outsideTempInput.text())
        except ValueError:
            return

        self.updateNumLampsHeatersTurnOn()

        qnet = (
            (self.qLamp * self.numLamps)
            + (self.qHeater * self.numHeaters)
            - (self.qAC * self.numACs)
        )
        qLoss = self.uValue * self.wallArea * (tRoom - tOut)
        deltaT = (qnet - qLoss) / (self.density * self.volume * self.cPair)
        tRoom += deltaT

        self.roomTempInput.setText(f"{tRoom:.4f}")

        for sensor_sim in self._registered_sensors:
            sensor_sim.set_external_value(tRoom)

    def updateNumLampsHeatersTurnOn(self):
        self.numLamps = self.numHeaters = self.numACs = 0

        for asset in self.assetList:
            t = asset.obj.get_type()
            s = asset.obj.get_status()
            if s == "ON":
                if t == "AssetLamp":
                    self.numLamps += 1
                elif t == "AssetHeat":
                    self.numHeaters += 1
                elif t == "AssetAirConditioning":
                    self.numACs += 1

        totalLamps = len([a for a in self.assetList if a.obj.get_type() == "AssetLamp"])
        totalHeats = len([a for a in self.assetList if a.obj.get_type() == "AssetHeat"])
        totalACs = len(
            [a for a in self.assetList if a.obj.get_type() == "AssetAirConditioning"]
        )

        self.lampsCountLabel.setText(
            f"ON: {self.numLamps} | OFF: {totalLamps - self.numLamps}"
        )
        self.heatersCountLabel.setText(
            f"ON: {self.numHeaters} | OFF: {totalHeats - self.numHeaters}"
        )
        self.acCountLabel.setText(f"ON: {self.numACs} | OFF: {totalACs - self.numACs}")

    def set_asset_list(self, assetList):
        self.assetList = assetList
