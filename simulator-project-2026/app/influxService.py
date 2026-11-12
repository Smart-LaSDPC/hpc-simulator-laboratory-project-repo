import json
import urllib.parse
import urllib.request
from PyQt5.QtCore import QThread, pyqtSignal


class InfluxQueryWorker(QThread):
    # Signals:
    # data_ready(table_name, columns, rows)
    data_ready = pyqtSignal(str, list, list)
    # error_occurred(message)
    error_occurred = pyqtSignal(str)
    # connection_status(is_connected, message)
    connection_status = pyqtSignal(bool, str)

    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.config = config
        self.is_running = True
        self.interval = config.default_interval_seconds
        self.limit = config.default_query_limit
        self.tables = ["sensor_temperature", "sensor_presence"]

    def set_interval(self, seconds):
        self.interval = max(1, int(seconds))

    def set_limit(self, limit):
        self.limit = max(1, int(limit))

    def stop(self):
        self.is_running = False
        self.wait(2000)

    def query_table(self, table_name):
        query_sql = f"SELECT * FROM {table_name} ORDER BY time DESC LIMIT {self.limit}"
        endpoint = f"{self.config.host_url.rstrip('/')}/query"
        params = urllib.parse.urlencode({"db": self.config.database, "q": query_sql})
        url = f"{endpoint}?{params}"

        req = urllib.request.Request(
            url,
            headers={
                "Authorization": f"Bearer {self.config.token}",
                "Accept": "application/json",
            },
            method="POST",
        )

        with urllib.request.urlopen(req, timeout=5) as response:
            body = response.read().decode("utf-8")
            result = json.loads(body)
            # Response structure:
            # {"results": [{"series": [{"name": ..., "columns": [...], "values": [[...], ...]}]}]}
            results = result.get("results", [])
            if not results:
                return [], []
            series_list = results[0].get("series", [])
            if not series_list:
                return [], []
            columns = series_list[0].get("columns", [])
            values = series_list[0].get("values", [])
            return columns, values

    def run(self):
        while self.is_running:
            success = True
            error_msg = ""
            for table in self.tables:
                if not self.is_running:
                    break
                try:
                    columns, values = self.query_table(table)
                    self.data_ready.emit(table, columns, values)
                except Exception as e:
                    success = False
                    error_msg = str(e)
                    self.error_occurred.emit(f"Error querying {table}: {error_msg}")

            if success:
                self.connection_status.emit(True, "Connecting to InfluxDB 3")
            else:
                self.connection_status.emit(False, f"Error: {error_msg}")

            # Sleep in small slices to respond promptly to stop requests
            elapsed = 0
            while self.is_running and elapsed < self.interval:
                self.msleep(500)
                elapsed += 0.5
