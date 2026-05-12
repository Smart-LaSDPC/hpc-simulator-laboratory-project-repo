from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QLabel, QLineEdit, QFrame, QVBoxLayout, QHBoxLayout


class TemperatureSimulator:
    def __init__(self, parent_widget, parent_layout, zone_name="Room",
             qLamp=100, qHeater=2000, qAC=3500,
             uValue=0.2, wallArea=100, volume=50):
        self.zone_name = zone_name
        self.qLamp = 100        # Heat gain from each lamp in Watts
        self.qHeater = 2000     # Heat gain from each heater in Watts
        self.qAC = 3500         # Cooling capacity of each AC in Watts
        self.uValue = 0.2       # Overall heat transfer coefficient (W/m^2*K)
        self.wallArea = 100     # Area of the walls in m^2
        self.volume = 50        # Volume of the room in m^3
        self.cPair = 1005       # J/(kg*K) - Specific heat capacity of air
        self.numHeaters = 0
        self.numACs = 0
        self.numLamps = 0
        self.density = 1.225    # kg/m^3 - Density of air
        self._registered_sensors = []
        self.assetList = []
        self._build_ui(parent_widget, parent_layout)

    def _build_ui(self, parent_widget, parent_layout):
        self.frame = QFrame(parent_widget)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.layout = QVBoxLayout(self.frame)
        self.layout.setSpacing(4)

        title = QLabel(f"<b>{self.zone_name}</b>", self.frame)
        title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(title)

        def add_row(label_text, widget):
            row = QHBoxLayout()
            row.addWidget(QLabel(label_text, self.frame))
            row.addWidget(widget)
            self.layout.addLayout(row)

        self.roomTempInput = QLineEdit("25", self.frame)
        add_row("Room Temp (°C):", self.roomTempInput)

        self.outsideTempInput = QLineEdit("20", self.frame)
        add_row("Outside Temp (°C):", self.outsideTempInput)

        self.lampsCountLabel = QLabel("ON: 0 | OFF: 0", self.frame)
        add_row("Lamps:", self.lampsCountLabel)

        self.heatersCountLabel = QLabel("ON: 0 | OFF: 0", self.frame)
        add_row("Heaters:", self.heatersCountLabel)

        self.acCountLabel = QLabel("ON: 0 | OFF: 0", self.frame)
        add_row("ACs:", self.acCountLabel)

        parent_layout.addWidget(self.frame)

        self.simulationTimer = QTimer()
        self.simulationTimer.timeout.connect(self.updateTemperature)
        self.simulationTimer.start(1000)

    def register_temperature_sensor(self, sensor_simulator):
        self._registered_sensors.append(sensor_simulator)

    def updateTemperature(self):
        try:
            tRoom = float(self.roomTempInput.text())
            tOut  = float(self.outsideTempInput.text())
        except ValueError:
            return

        self.updateNumLampsHeatersTurnOn()

        qNet   = (self.qLamp * self.numLamps) + (self.qHeater * self.numHeaters) - (self.qAC * self.numACs)
        qLoss  = self.uValue * self.wallArea * (tRoom - tOut)
        deltaT = (qNet - qLoss) / (self.density * self.volume * self.cPair)
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

        totalLamps   = sum(1 for a in self.assetList if a.obj.get_type() == "AssetLamp")
        totalHeaters = sum(1 for a in self.assetList if a.obj.get_type() == "AssetHeat")
        totalACs     = sum(1 for a in self.assetList if a.obj.get_type() == "AssetAirConditioning")

        self.lampsCountLabel.setText(f"ON: {self.numLamps} | OFF: {totalLamps - self.numLamps}")
        self.heatersCountLabel.setText(f"ON: {self.numHeaters} | OFF: {totalHeaters - self.numHeaters}")
        self.acCountLabel.setText(f"ON: {self.numACs} | OFF: {totalACs - self.numACs}")