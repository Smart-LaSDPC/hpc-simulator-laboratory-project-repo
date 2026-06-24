import datetime

import matplotlib
import matplotlib.dates as mdates
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget


class EnergyMonitorWindow(QMainWindow):
    def __init__(self, temp_simulators):
        super().__init__()
        self.setWindowTitle("Energy Monitoring")
        self.resize(900, 650)
        self.temp_simulators = temp_simulators

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        self.figure = Figure(figsize=(9, 6))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self._update_charts)
        self.refresh_timer.start(1000)

        self._update_charts()

    def _elapsed_seconds(self):
        all_ts = [
            ts
            for sim in self.temp_simulators
            for ts, _ in sim.temperature_history
        ]
        if len(all_ts) < 2:
            return 0
        return max(all_ts) - min(all_ts)

    def _apply_time_axis(self, ax, elapsed):
        if elapsed < 60:
            interval = max(1, int(elapsed / 10))
            ax.xaxis.set_major_locator(mdates.SecondLocator(interval=interval))
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        else:
            interval = max(1, int(elapsed / 600))
            ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=interval))
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))

    def _update_charts(self):
        self.figure.clear()
        ax_temp = self.figure.add_subplot(2, 1, 1)
        ax_energy = self.figure.add_subplot(2, 1, 2)

        elapsed = self._elapsed_seconds()

        for sim in self.temp_simulators:
            if sim.temperature_history:
                ts_list, temps = zip(*sim.temperature_history)
                dt_list = [datetime.datetime.fromtimestamp(t) for t in ts_list]
                ax_temp.plot(dt_list, temps, label=sim.zone_name)

            if sim.energy_history:
                ts_list, energies = zip(*sim.energy_history)
                dt_list = [datetime.datetime.fromtimestamp(t) for t in ts_list]
                ax_energy.plot(dt_list, energies, label=sim.zone_name)

        ax_temp.set_title("Room Temperature Over Time")
        ax_temp.set_ylabel("Temperature (°C)")
        ax_temp.legend()
        ax_temp.grid(True)
        self._apply_time_axis(ax_temp, elapsed)

        ax_energy.set_title("Cumulative Energy Consumption")
        ax_energy.set_ylabel("Energy (Wh)")
        ax_energy.legend()
        ax_energy.grid(True)
        self._apply_time_axis(ax_energy, elapsed)

        self.figure.autofmt_xdate()
        self.figure.tight_layout()
        self.canvas.draw()

    def closeEvent(self, event):
        self.refresh_timer.stop()
        super().closeEvent(event)
