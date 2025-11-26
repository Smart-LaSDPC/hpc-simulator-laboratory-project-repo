import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout
from PyQt5.QtCore import QTimer

class RoomSimulator(QWidget):
    def __init__(self):
        super().__init__()
        
        # Initialize constants and initial values
        self.cPair = 1005  # J/(kg*K) - Specific heat capacity of air
        self.density = 1.225  # kg/m^3 - Density of air
        self.volume = 50  # Volume of the room in m^3
        self.tRoom = 25  # Initial room temperature in Celsius
        self.qLamp = 100  # Heat gain from each lamp in Watts
        
        # Heat loss parameters
        self.uValue = 0.2  # Overall heat transfer coefficient (W/m^2*K)
        self.wallArea = 100  # Area of the walls in m^2
        
        # Simulation settings
        self.dt = 1  # Time step in seconds
        self.timeElapsed = 0

        # Initialize UI elements
        self.initUI()
        
        # Timer for simulation
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateTemperature)

    def initUI(self):
        self.setWindowTitle('Room Temperature Simulator')
        
        self.layout = QVBoxLayout()
        
        self.tempLabel = QLabel(f'Room Temperature: {self.tRoom:.2f} °C', self)
        self.layout.addWidget(self.tempLabel)
        
        self.numLampsLayout = QHBoxLayout()
        self.numLampsLabel = QLabel('Number of Lamps:', self)
        self.numLampsInput = QLineEdit('12', self)
        self.numLampsLayout.addWidget(self.numLampsLabel)
        self.numLampsLayout.addWidget(self.numLampsInput)
        self.layout.addLayout(self.numLampsLayout)
        
        self.tOutLayout = QHBoxLayout()
        self.tOutLabel = QLabel('Outside Temperature (°C):', self)
        self.tOutInput = QLineEdit('20', self)
        self.tOutLayout.addWidget(self.tOutLabel)
        self.tOutLayout.addWidget(self.tOutInput)
        self.layout.addLayout(self.tOutLayout)
        
        self.startButton = QPushButton('Start Simulation', self)
        self.startButton.clicked.connect(self.startSimulation)
        self.layout.addWidget(self.startButton)
        
        self.setLayout(self.layout)
        self.resize(400, 300)
        
    def startSimulation(self):
        # Get user input
        self.numLamps = int(self.numLampsInput.text())
        self.tOut = float(self.tOutInput.text())
        
        # Reset time elapsed and room temperature
        self.timeElapsed = 0
        self.tRoom = 25  # Reset room temperature to initial value
        
        self.timer.start(self.dt * 1000)
        
    def updateTemperature(self):
        # Calculate heat gains
        qGain = self.qLamp * self.numLamps  # Q_gain = q_lamp * numLamps
        
        # Calculate heat loss
        qLoss = self.uValue * self.wallArea * (self.tRoom - self.tOut)  # Q_loss = U * A * (T_room - T_out)
        
        # Update room temperature
        self.tRoom += self.dt * (qGain - qLoss) / (self.density * self.volume * self.cPair)  # ΔT = (Q_gain - Q_loss) * Δt / (ρ * V * c_p)
        self.timeElapsed += self.dt
        
        # Update the label
        self.tempLabel.setText(f'Room Temperature: {self.tRoom:.2f} °C')
        
        # Optional: Stop simulation after a certain time
        if self.timeElapsed >= 3600:  # Stop after 1 hour
            self.timer.stop()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    sim = RoomSimulator()
    sim.show()
    sys.exit(app.exec_())
