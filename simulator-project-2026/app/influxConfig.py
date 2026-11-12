import os
from dotenv import load_dotenv

current_dir = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(current_dir, "..", ".env")
load_dotenv(dotenv_path=dotenv_path)


class InfluxConfig:
    def __init__(self):
        self.host_url = os.getenv("INFLUXDB3_URL", "http://localhost:8181")
        self.token = os.getenv(
            "INFLUXDB3_AUTH_TOKEN",
            "apiv3_",
        )
        self.database = os.getenv("INFLUXDB3_DATABASE_NAME", "smartlab")
        self.default_interval_seconds = 5
        self.default_query_limit = 50
