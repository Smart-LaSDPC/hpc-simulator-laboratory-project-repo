from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QComboBox,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QMainWindow,
    QPushButton,
    QStatusBar,
    QTabWidget,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from influxConfig import InfluxConfig
from influxService import InfluxQueryWorker


class InfluxMonitorWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("InfluxDB Telemetry Monitor - Lab 1006")
        self.resize(1050, 680)

        self.config = InfluxConfig()
        self.worker = None

        self._setup_ui()
        self._start_worker()

    def _setup_ui(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # -----------------------------
        # Control Header Toolbar
        # -----------------------------
        controls_group = QGroupBox("Consultation options and frequency")
        controls_layout = QHBoxLayout(controls_group)

        # Interval combo
        lbl_interval = QLabel("Consultation interval:")
        self.combo_interval = QComboBox()
        self.combo_interval.addItem("3 seconds", 3)
        self.combo_interval.addItem("5 seconds (Recommended)", 5)
        self.combo_interval.addItem("10 seconds", 10)
        self.combo_interval.addItem("30 seconds", 30)
        self.combo_interval.setCurrentIndex(1)
        self.combo_interval.currentIndexChanged.connect(self._on_interval_changed)

        # Limit combo
        lbl_limit = QLabel("Row limit:")
        self.combo_limit = QComboBox()
        self.combo_limit.addItem("20 records", 20)
        self.combo_limit.addItem("50 records", 50)
        self.combo_limit.addItem("100 records", 100)
        self.combo_limit.setCurrentIndex(1)
        self.combo_limit.currentIndexChanged.connect(self._on_limit_changed)

        # Buttons
        self.btn_refresh = QPushButton("Consult now")
        self.btn_refresh.clicked.connect(self._on_manual_refresh)

        self.btn_pause = QPushButton("Pause Polling")
        self.btn_pause.setCheckable(True)
        self.btn_pause.clicked.connect(self._on_pause_toggled)

        # Status badge
        self.lbl_status_badge = QLabel("Starting...")
        self.lbl_status_badge.setStyleSheet(
            "padding: 4px 8px; border-radius: 4px; font-weight: bold; background-color: #888888; color: white;"
        )

        controls_layout.addWidget(lbl_interval)
        controls_layout.addWidget(self.combo_interval)
        controls_layout.addSpacing(15)
        controls_layout.addWidget(lbl_limit)
        controls_layout.addWidget(self.combo_limit)
        controls_layout.addSpacing(15)
        controls_layout.addWidget(self.btn_refresh)
        controls_layout.addWidget(self.btn_pause)
        controls_layout.addStretch()
        controls_layout.addWidget(self.lbl_status_badge)

        main_layout.addWidget(controls_group)

        # -----------------------------
        # Tabs for tables
        # -----------------------------
        self.tabs = QTabWidget()

        # Tab: Temperature
        self.tab_temp = QWidget()
        layout_temp = QVBoxLayout(self.tab_temp)
        self.table_temp = QTableWidget()
        self._configure_table(self.table_temp)
        layout_temp.addWidget(self.table_temp)
        self.tabs.addTab(self.tab_temp, "sensor_temperature")

        # Tab: Presence
        self.tab_presence = QWidget()
        layout_presence = QVBoxLayout(self.tab_presence)
        self.table_presence = QTableWidget()
        self._configure_table(self.table_presence)
        layout_presence.addWidget(self.table_presence)
        self.tabs.addTab(self.tab_presence, "sensor_presence")

        main_layout.addWidget(self.tabs)

        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage(f"Database: {self.config.database} @ {self.config.host_url}")

    def _configure_table(self, table: QTableWidget):
        table.setAlternatingRowColors(True)
        table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        table.horizontalHeader().setStretchLastSection(True)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

    def _start_worker(self):
        if self.worker is not None and self.worker.isRunning():
            self.worker.stop()

        self.worker = InfluxQueryWorker(self.config, self)
        self.worker.data_ready.connect(self._on_data_ready)
        self.worker.connection_status.connect(self._on_connection_status)
        self.worker.error_occurred.connect(self._on_error)
        self.worker.set_interval(self.combo_interval.currentData())
        self.worker.set_limit(self.combo_limit.currentData())
        self.worker.start()

    def _on_interval_changed(self):
        if self.worker:
            self.worker.set_interval(self.combo_interval.currentData())

    def _on_limit_changed(self):
        if self.worker:
            self.worker.set_limit(self.combo_limit.currentData())

    def _on_manual_refresh(self):
        # Trigger immediate run if paused or running
        if self.worker and not self.worker.isRunning():
            self._start_worker()

    def _on_pause_toggled(self, checked):
        if checked:
            self.btn_pause.setText("Resume Polling")
            if self.worker:
                self.worker.stop()
            self.lbl_status_badge.setText("On Paused")
            self.lbl_status_badge.setStyleSheet(
                "padding: 4px 8px; border-radius: 4px; font-weight: bold; background-color: #f39c12; color: white;"
            )
        else:
            self.btn_pause.setText("Pause Polling")
            self._start_worker()

    def _on_connection_status(self, is_connected, message):
        if is_connected:
            self.lbl_status_badge.setText("Connected")
            self.lbl_status_badge.setStyleSheet(
                "padding: 4px 8px; border-radius: 4px; font-weight: bold; background-color: #27ae60; color: white;"
            )
        else:
            self.lbl_status_badge.setText("Offline")
            self.lbl_status_badge.setStyleSheet(
                "padding: 4px 8px; border-radius: 4px; font-weight: bold; background-color: #c0392b; color: white;"
            )
        self.status_bar.showMessage(f"InfluxDB State: {message}")

    def _on_error(self, message):
        self.status_bar.showMessage(message)

    def _on_data_ready(self, table_name, columns, values):
        target_table = self.table_temp if table_name == "sensor_temperature" else self.table_presence

        if not columns:
            target_table.setRowCount(0)
            target_table.setColumnCount(1)
            target_table.setHorizontalHeaderLabels(["Message"])
            target_table.setItem(0, 0, QTableWidgetItem("No records were found in the table"))
            return

        target_table.setColumnCount(len(columns))
        target_table.setHorizontalHeaderLabels(columns)
        target_table.setRowCount(len(values))

        for row_idx, row_data in enumerate(values):
            for col_idx, col_value in enumerate(row_data):
                val_str = "" if col_value is None else str(col_value)
                item = QTableWidgetItem(val_str)
                # Align numbers right, text left
                if isinstance(col_value, (int, float)):
                    item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                else:
                    item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                target_table.setItem(row_idx, col_idx, item)

    def closeEvent(self, event):
        if self.worker:
            self.worker.stop()
        super().closeEvent(event)
