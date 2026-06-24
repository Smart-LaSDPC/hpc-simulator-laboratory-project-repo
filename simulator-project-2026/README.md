# HPC Simulator - Laboratory Project 2026

A graphical simulator for lab room 1006, modeling assets (lamps, ACs, heaters, datacenters), temperature sensors, and presence sensors. It publishes sensor readings over MQTT and simulates room temperature physics in real time.

---

## Requirements

- Python 3.12+
- [Poetry](https://python-poetry.org/) (recommended) or pip
- An MQTT broker running locally (e.g. Mosquitto)

---

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd simulator-project-2026
```

### 2. Install dependencies

Using Poetry:

```bash
poetry install
poetry shell
```

Or manually with pip:

```bash
pip install PyQt5 "paho-mqtt==1.6.1"
```

## Running the simulator

The application must be launched from the `app/` directory so it can find its media assets:

```bash
cd app
poetry run python main8.py
```

A window titled **MainWindow-Simulator** will open showing a floor plan of lab 1006.

---

## Tutorial: Running the Temperature Test

The temperature test loads a pre-configured set of sensors and assets that represent the real lab layout. Follow these steps:

### Step 1 - Load the test data

Click the **"Charge Temperature Test"** button on the left side of the window.

This populates the scene with:

| Type | IDs | Count |
|---|---|---|
| Temperature sensors | `sensor_temperature1` to `sensor_temperature7` | 7 |
| Presence sensors | `sensor_presence1`, `sensor_presence2` | 2 |
| Outside temperature sensor | `sensor_temperature_outside` | 1 |
| Lamps | `asset_lamp1` to `asset_lamp15` | 15 |
| Air conditioners | `asset_aircond1` to `asset_aircond5` | 5 |
| Heater | `asset_heat1` | 1 |
| Datacenters (14 racks each) | `asset_datacenter1` to `asset_datacenter3` | 3 |
| Doors | `asset_door_datacenter`, `asset_door_lab1006` | 2 |
| Windows | `asset_window1` to `asset_window9` | 9 |

### Step 2 - Observe the temperature simulators

At the bottom of the window there is a scroll area with two temperature simulator panels:

- **Datacenter** - tracks the enclosed datacenter zone (sensors 1-3, ACs 1-3, datacenters 1-3)
- **Laboratorio** - tracks the rest of the lab (sensors 4-7, ACs 4-5, lamps, heater)

Each panel shows:
- **Room Temp (°C)** - current simulated temperature, updated every second
- **Outside Temp (°C)** - editable baseline outside temperature
- Counts of lamps, heaters, ACs, and datacenters that are ON / OFF

### Step 3 - Interact with assets

Assets placed on the scene can be toggled ON/OFF. The temperature model reacts immediately:

- Turning **ACs ON** lowers the room temperature (cooling effect)
- Turning **lamps or heaters ON** raises the room temperature (heat gain)
- Turning **datacenters ON** adds significant heat (500 W per rack x 14 racks each)

To control an asset remotely via MQTT, publish to the topic `lab1006/control/asset`:

```json
{
  "id": "asset_aircond1",
  "state_value": "1"
}
```

Use `"state_value": "1"` for ON and `"state_value": "0"` for OFF.

Example using the `mosquitto_pub` CLI:

```bash
mosquitto_pub -h localhost -p 1883 -u mqtt -P lasdpc \
  -t "lab1006/control/asset" \
  -m '{"id": "asset_aircond1", "state_value": "1"}'
```

### Step 4 - Monitor sensor readings via MQTT

Temperature sensors publish their current reading continuously. Subscribe to watch them:

```bash
mosquitto_sub -h localhost -p 1883 -u mqtt -P lasdpc -t "lab1006/#" -v
```

### Step 5 - Change the background view

Use the dropdown on the left to switch between:
- **1006 temperature room** - default temperature-focused overlay
- **1006 room** - floor plan view

Then click **"Change Background"**.

### Step 6 - Add users / presence simulation

Use the right-side panel to:
1. Select a person category: `Professor`, `Postgraduate`, `Undergraduate`, or `Unknown`
2. Select a platform: `Platform 1` or `Platform 2`
3. Click **"Add User"** to place the person on the scene

This triggers the corresponding presence sensor (`sensor_presence1` or `sensor_presence2`).

To control presence remotely via MQTT, publish to `lab1006/control/sensor`:

```json
{
  "id": "sensor_presence1",
  "agent_monitor_id": "user_professor1"
}
```

### Step 7 - Connect the asset controller (optional)

Click **"Connect asset controller"** to start publishing the full asset state list every 5 seconds to the topic `lab1006/control/assets`. This simulates a physical asset controller reporting to a backend.

---

## MQTT Topics Summary

| Topic | Direction | Description |
|---|---|---|
| `lab1006/control/asset` | Subscribe (inbound) | Toggle a single asset ON/OFF |
| `lab1006/control/sensor` | Subscribe (inbound) | Update a sensor's monitored agent |
| `lab1006/control/assets` | Publish (outbound) | Full asset status list (every 5 s) |

---

## Project Structure

```
simulator-project-2026/
├── app/
│   ├── main8.py              # Entry point
│   ├── temperatureSim.py     # Temperature physics model + UI panel
│   ├── testData.py           # Pre-configured test assets and sensors
│   ├── mqttConfig.py         # MQTT broker connection settings
│   ├── asset.py              # Asset model
│   ├── sensor.py             # Sensor model
│   ├── simulatorSensor.py    # Sensor simulator (reads & publishes)
│   ├── movingObject.py       # Draggable scene item
│   ├── user.py               # User model
│   └── media/                # Images for assets, sensors, users
├── pyproject.toml
└── README.md
```

---

## Adjusting the MQTT broker settings

Edit `app/mqttConfig.py` to point at a different broker:

```python
self.mqtt_data = {
    "user": "mqtt",
    "password": "lasdpc",
    "host": "localhost",   # change to broker IP if remote
    "port": 1883
}
```
